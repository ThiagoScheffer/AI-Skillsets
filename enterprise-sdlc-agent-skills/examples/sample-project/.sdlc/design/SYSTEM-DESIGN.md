# System Design

Status: Draft
Requirements covered: FR-001, NFR-001
Risk tier: R2

## Architecture drivers
Normalize heterogeneous event-provider data while retaining source provenance.

## Proposed architecture
A provider-adapter boundary normalizes external event records before persistence and presentation.

## Open questions
Storage and caching choices remain intentionally undecided in this example.
