#!/usr/bin/env python3
"""Dependency-free subset JSON Schema validator + KX semantic integrity checks.

For *full* Draft 2020-12 JSON Schema compliance, use a dedicated validator.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'schemas' / 'motion-blueprint.schema.json'


def _is_type(value: Any, kind: str) -> bool:
    return {
        'object': lambda: isinstance(value, dict),
        'array': lambda: isinstance(value, list),
        'string': lambda: isinstance(value, str),
        'boolean': lambda: isinstance(value, bool),
        'integer': lambda: isinstance(value, int) and not isinstance(value, bool),
        'number': lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
        'null': lambda: value is None,
    }[kind]()


def _validate(value: Any, schema: dict, path: str, errors: list[str]) -> None:
    if 'type' in schema:
        kinds = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(_is_type(value, kind) for kind in kinds):
            errors.append(f'{path}: expected {kinds}, got {type(value).__name__}')
            return
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: must be {schema["const"]!r}')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: invalid enum {value!r}; allowed={schema["enum"]}')
    if isinstance(value, str) and len(value) < schema.get('minLength', 0):
        errors.append(f'{path}: string too short')
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 'minimum' in schema and value < schema['minimum']:
            errors.append(f'{path}: below minimum {schema["minimum"]}')
        if 'maximum' in schema and value > schema['maximum']:
            errors.append(f'{path}: above maximum {schema["maximum"]}')
    if isinstance(value, dict):
        required = schema.get('required', [])
        for key in required:
            if key not in value:
                errors.append(f'{path}.{key}: missing required field')
        props = schema.get('properties', {})
        for key, child in value.items():
            if key not in props:
                if schema.get('additionalProperties') is False:
                    errors.append(f'{path}.{key}: unsupported field')
            else:
                _validate(child, props[key], f'{path}.{key}', errors)
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{path}: expected at least {schema["minItems"]} item(s)')
        if 'maxItems' in schema and len(value) > schema['maxItems']:
            errors.append(f'{path}: too many items')
        if 'items' in schema:
            for idx, child in enumerate(value):
                _validate(child, schema['items'], f'{path}[{idx}]', errors)


def validate_blueprint(document: Any, schema: dict | None = None) -> list[str]:
    """Return user-readable validation problems; empty means checks passed."""
    schema = schema or json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    errors: list[str] = []
    _validate(document, schema, '$', errors)
    if not isinstance(document, dict):
        return errors
    transitions = document.get('transitions')
    if isinstance(transitions, list):
        ids: set[str] = set()
        for index, item in enumerate(transitions):
            if not isinstance(item, dict):
                continue
            name = item.get('id')
            if isinstance(name, str):
                if name in ids:
                    errors.append(f'$.transitions[{index}].id: duplicate transition ID {name!r}')
                ids.add(name)
            beats = item.get('beats')
            if isinstance(beats, list):
                labels: set[str] = set()
                for beat_idx, beat in enumerate(beats):
                    if not isinstance(beat, dict):
                        continue
                    ident = beat.get('id')
                    if isinstance(ident, str):
                        if ident in labels:
                            errors.append(f'$.transitions[{index}].beats[{beat_idx}].id: duplicate beat ID')
                        labels.add(ident)
                for beat_idx, beat in enumerate(beats):
                    if not isinstance(beat, dict):
                        continue
                    at = beat.get('at')
                    if isinstance(at, str) and at.startswith('after:') and at[6:] not in labels:
                        errors.append(f'$.transitions[{index}].beats[{beat_idx}].at: missing beat reference {at[6:]!r}')
    ownership = document.get('ownership')
    if isinstance(ownership, list):
        seen: dict[tuple[str, str], str] = {}
        for idx, item in enumerate(ownership):
            if not isinstance(item, dict):
                continue
            key = (str(item.get('target')), str(item.get('property')))
            if key in seen and seen[key] != item.get('owner'):
                errors.append(f'$.ownership[{idx}]: conflicting owners for {key[0]}.{key[1]}')
            else:
                seen[key] = str(item.get('owner'))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', type=Path, nargs='+', help='One or more JSON blueprints')
    args = ap.parse_args()
    failed = False
    for file in args.files:
        try:
            data = json.loads(file.read_text(encoding='utf-8'))
            errors = validate_blueprint(data)
        except (OSError, json.JSONDecodeError) as exc:
            errors = [str(exc)]
        print(f'{"FAIL" if errors else "PASS"}: {file}')
        for error in errors:
            print(f'  - {error}')
        failed |= bool(errors)
    if not failed:
        print('All selected blueprints passed KX subset checks (not full JSON Schema compliance).')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
