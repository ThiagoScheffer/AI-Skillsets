#!/usr/bin/env python3
"""Heuristic OpenAPI contract checker for the api-check Codex skill.

This script intentionally checks a small set of high-signal API design issues.
It is not a complete OpenAPI validator and does not replace semantic review.
Supports JSON and YAML when PyYAML is installed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
ACTION_SEGMENT = re.compile(r"^(get|create|update|delete|remove|add|set|approve|reject|cancel)[-_]?[a-z0-9]", re.I)
MUTATING_OPERATION = re.compile(r"^(create|update|delete|remove|set|approve|reject|cancel|patch|put)", re.I)
LOWER_PATH_SEGMENT = re.compile(r"^[a-z0-9][a-z0-9._~-]*$")
CAMEL = re.compile(r"^[a-z][A-Za-z0-9]*$")
SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")
KEBAB = re.compile(r"^[a-z][a-z0-9-]*$")


class Finding:
    def __init__(self, severity: str, code: str, location: str, message: str):
        self.severity = severity
        self.code = code
        self.location = location
        self.message = message

    def __str__(self) -> str:
        return f"{self.severity} {self.code} {self.location}: {self.message}"


def load_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise RuntimeError("YAML input requires PyYAML; use JSON or install pyyaml") from exc
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("OpenAPI document root must be an object")
    return data


def iter_operations(doc: dict[str, Any]):
    paths = doc.get("paths", {})
    if not isinstance(paths, dict):
        return
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            method_l = str(method).lower()
            if method_l in HTTP_METHODS and isinstance(operation, dict):
                yield str(path), method_l, operation


def response_codes(operation: dict[str, Any]) -> set[str]:
    responses = operation.get("responses", {})
    if not isinstance(responses, dict):
        return set()
    return {str(code).upper() for code in responses.keys()}


def has_2xx(codes: set[str]) -> bool:
    return any(code.startswith("2") or code == "2XX" for code in codes)


def collect_schema_property_styles(node: Any, styles: Counter[str]) -> None:
    if isinstance(node, dict):
        props = node.get("properties")
        if isinstance(props, dict):
            for name in props:
                if CAMEL.fullmatch(str(name)) and "_" not in str(name) and "-" not in str(name):
                    styles["camelCase"] += 1
                if SNAKE.fullmatch(str(name)) and "_" in str(name):
                    styles["snake_case"] += 1
                if KEBAB.fullmatch(str(name)) and "-" in str(name):
                    styles["kebab-case"] += 1
        for value in node.values():
            collect_schema_property_styles(value, styles)
    elif isinstance(node, list):
        for value in node:
            collect_schema_property_styles(value, styles)


def check(doc: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    openapi = str(doc.get("openapi", ""))
    if not openapi:
        findings.append(Finding("P1", "OAS001", "openapi", "Missing OpenAPI version field."))
    elif not openapi.startswith("3."):
        findings.append(Finding("P2", "OAS002", "openapi", f"Version {openapi!r} is not OpenAPI 3.x; review with version-appropriate tooling."))

    operation_ids: dict[str, str] = {}
    secured_ops = 0

    for path, method, op in iter_operations(doc):
        loc = f"{method.upper()} {path}"

        # Path heuristics.
        for segment in (s for s in path.strip("/").split("/") if s and not s.startswith("{")):
            if ACTION_SEGMENT.match(segment):
                findings.append(Finding("P3", "PATH001", loc, f"Action-like path segment {segment!r}; verify that HTTP method/resource modeling would be clearer."))
            if not LOWER_PATH_SEGMENT.fullmatch(segment):
                findings.append(Finding("P3", "PATH002", loc, f"Path segment {segment!r} is not lowercase/predictable; verify naming consistency."))

        params = []
        if isinstance(op.get("parameters"), list):
            params.extend(op["parameters"])
        for param in params:
            if isinstance(param, dict) and str(param.get("in", "")).lower() == "query" and str(param.get("name", "")).lower() == "action":
                findings.append(Finding("P1" if method == "get" else "P2", "QUERY001", loc, "Query parameter named 'action' can hide operation semantics; do not use GET query parameters for state-changing commands."))

        if method == "get" and "requestBody" in op:
            findings.append(Finding("P2", "HTTP001", loc, "GET defines requestBody; GET content has no generally defined semantics and has poor interoperability."))

        operation_id = op.get("operationId")
        if isinstance(operation_id, str) and operation_id:
            if operation_id in operation_ids:
                findings.append(Finding("P2", "OAS003", loc, f"Duplicate operationId {operation_id!r}; first seen at {operation_ids[operation_id]}."))
            else:
                operation_ids[operation_id] = loc
            if method in {"get", "head"} and MUTATING_OPERATION.match(operation_id):
                findings.append(Finding("P1", "HTTP002", loc, f"Safe method has mutating-looking operationId {operation_id!r}; verify there is no state change."))

        codes = response_codes(op)
        if not codes:
            findings.append(Finding("P2", "RESP001", loc, "No responses are defined."))
        elif not has_2xx(codes):
            findings.append(Finding("P2", "RESP002", loc, "No successful 2xx response is documented."))

        if method == "delete" and codes and not ({"200", "202", "204"} & codes or "2XX" in codes):
            findings.append(Finding("P3", "RESP003", loc, "DELETE has no documented 200/202/204 success response; verify intended semantics."))

        if method == "post" and isinstance(operation_id, str) and operation_id.lower().startswith("create"):
            if "201" not in codes and "2XX" not in codes:
                findings.append(Finding("P3", "RESP004", loc, "Create-like POST does not document 201 Created; verify whether it creates a resource or performs another command."))

        effective_security = op.get("security", doc.get("security"))
        if isinstance(effective_security, list) and effective_security:
            secured_ops += 1
            if "401" not in codes and "4XX" not in codes and "DEFAULT" not in codes:
                findings.append(Finding("P3", "AUTH001", loc, "Protected operation does not explicitly document a 401/authentication failure response."))
            if "403" not in codes and "4XX" not in codes and "DEFAULT" not in codes:
                findings.append(Finding("P3", "AUTH002", loc, "Protected operation does not explicitly document a 403/authorization failure response."))

        # Error-format heuristic.
        responses = op.get("responses", {})
        if isinstance(responses, dict):
            for code, response in responses.items():
                code_s = str(code).upper()
                if not (code_s.startswith("4") or code_s.startswith("5") or code_s in {"4XX", "5XX", "DEFAULT"}):
                    continue
                if not isinstance(response, dict):
                    continue
                content = response.get("content", {})
                if isinstance(content, dict) and content and "application/problem+json" not in content:
                    findings.append(Finding("P3", "ERR001", f"{loc} response {code_s}", "Error response uses a custom media type/envelope; verify that the API has a consistent stable error contract (RFC 9457 is preferred for new HTTP APIs)."))

    components = doc.get("components", {})
    if isinstance(components, dict):
        sec = components.get("securitySchemes", {})
        if isinstance(sec, dict):
            for name, scheme in sec.items():
                if not isinstance(scheme, dict):
                    continue
                typ = str(scheme.get("type", "")).lower()
                http_scheme = str(scheme.get("scheme", "")).lower()
                loc = f"components.securitySchemes.{name}"
                if typ == "http" and http_scheme == "basic":
                    findings.append(Finding("P2", "AUTH003", loc, "HTTP Basic is configured; require TLS and verify this simple credential model fits the threat model and rotation requirements."))
                if typ == "apikey" and str(scheme.get("in", "")).lower() == "query":
                    findings.append(Finding("P1", "AUTH004", loc, "API key is sent in the query string, which increases leakage through URLs/logs/history; prefer a header or stronger mechanism."))

    styles: Counter[str] = Counter()
    collect_schema_property_styles(doc.get("components", {}).get("schemas", {}) if isinstance(doc.get("components"), dict) else {}, styles)
    used_styles = [style for style, count in styles.items() if count >= 2]
    if len(used_styles) > 1:
        findings.append(Finding("P3", "STYLE001", "components.schemas", f"Mixed JSON property naming conventions detected: {dict(styles)}. Verify this is intentional or normalize new API surfaces."))

    if secured_ops == 0 and isinstance(doc.get("components"), dict) and doc.get("components", {}).get("securitySchemes"):
        findings.append(Finding("P3", "AUTH005", "security", "Security schemes exist but no protected operations were detected; verify global/operation security requirements."))

    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    findings.sort(key=lambda f: (order.get(f.severity, 9), f.code, f.location))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristic OpenAPI contract checker")
    parser.add_argument("spec", type=Path, help="OpenAPI JSON/YAML file")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    args = parser.parse_args()

    try:
        doc = load_document(args.spec)
        findings = check(doc)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([f.__dict__ for f in findings], indent=2))
    else:
        if not findings:
            print("No heuristic findings. This is not a full OpenAPI or security validation.")
        else:
            for finding in findings:
                print(finding)
            counts = Counter(f.severity for f in findings)
            print("\nSummary: " + ", ".join(f"{sev}={counts.get(sev, 0)}" for sev in ("P0", "P1", "P2", "P3")))
            print("Note: heuristic output; perform semantic and security review before changing a public contract.")
    return 1 if any(f.severity in {"P0", "P1"} for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
