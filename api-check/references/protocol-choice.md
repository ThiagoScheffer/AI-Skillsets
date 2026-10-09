# REST vs GraphQL vs gRPC

Choose based on client topology, coupling, latency, schema needs, streaming, browser constraints, observability, and operational maturity.

## REST / HTTP resource APIs

Prefer when:
- external/public interoperability matters;
- HTTP semantics, caching, proxies, CDNs, and simple debugging are valuable;
- the domain maps naturally to resources;
- broad tooling/client compatibility matters more than client-defined response shape.

Watch for:
- over-fetching or under-fetching on screen-specific data;
- multiple round trips for graph-shaped views;
- inconsistent endpoint-by-endpoint conventions;
- ad hoc RPC disguised as REST.

Do not assume REST responses must always be fixed and over-fetching: sparse fieldsets, expansions, purpose-built read models, and aggregation endpoints can address this when appropriate.

## GraphQL

Prefer when:
- clients need materially different projections of the same connected domain graph;
- product teams benefit from typed schema discovery and client-selected fields;
- reducing front-end orchestration/round trips is important;
- the organization can operate query complexity, authorization, caching, resolver performance, and schema governance well.

Watch for:
- resolver N+1 patterns and hidden backend fan-out;
- unbounded query depth/complexity/cost;
- field-level authorization mistakes;
- difficult HTTP/CDN caching compared with simple REST resources;
- schema changes that are syntactically additive but operationally expensive.

A single GraphQL request is not automatically one backend call and is not automatically faster.

## gRPC

Prefer when:
- service-to-service RPC dominates;
- strongly typed contracts and generated clients are valuable;
- low overhead and high request rates matter under measured workloads;
- client/server/bidirectional streaming is required;
- cross-language internal service contracts benefit from Protocol Buffers.

Watch for:
- browser access constraints and the need for gRPC-Web/proxies where applicable;
- harder manual inspection than plain JSON/HTTP;
- load-balancing, deadlines, retries, backpressure, and long-lived stream behavior;
- protobuf compatibility rules and field-number discipline.

gRPC uses Protocol Buffers by default, but the conceptual framework is RPC/service-oriented rather than “binary therefore always faster.” Benchmark representative payload sizes, concurrency, serialization costs, and network conditions when performance is a deciding factor.

## Hybrid architectures

Using more than one style can be correct. Typical examples:
- REST for public partner APIs, GraphQL for product front ends, gRPC internally;
- REST externally with gRPC behind an API gateway;
- GraphQL as an aggregation layer over REST/gRPC services.

Avoid protocol proliferation unless each additional interface solves a concrete problem worth its operational cost.

## Decision matrix

Score each candidate against the actual system:

| Criterion | REST | GraphQL | gRPC |
| --- | --- | --- | --- |
| Public/browser interoperability | High | High | Medium/Low without gRPC-Web |
| Client-selected field shape | Medium with conventions | High | Low |
| HTTP caching/CDN friendliness | High | Medium/complex | Low/architecture-specific |
| Strong generated service contracts | Medium/High with OpenAPI | High with schema/tooling | High |
| Streaming | Medium with SSE/WebSocket/etc. | Medium via subscriptions/transports | High/native RPC model |
| Human inspectability | High | High | Lower |
| Internal high-throughput RPC | Medium | Medium | Often High |
| Operational simplicity for small APIs | High | Medium | Medium |

Treat this matrix as a starting heuristic, not a benchmark result.
