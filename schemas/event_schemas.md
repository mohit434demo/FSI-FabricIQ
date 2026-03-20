# Event Stream Schemas — Insurance Claims Intelligence

All events are structured as JSON and ingested into Eventhouse KQL tables via the Kusto Python SDK. Each event includes a standard envelope with event-specific payload fields.

## Common Envelope

```json
{
  "event_id": "UUID",
  "event_type": "string",
  "timestamp": "ISO 8601 datetime",
  "source": "string (system identifier)",
  "body": { ... }
}
```

---

## 1. ClaimStatusEvent

Claim lifecycle status transitions — tracks a claim as it moves through processing stages from initial review through payment or denial.

```json
{
  "event_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "event_type": "ClaimStatusEvent",
  "timestamp": "2026-03-15T08:15:00Z",
  "source": "claims-system",
  "body": {
    "claim_id": "UUID",
    "claim_number": "CLM-70001",
    "policy_id": "UUID",
    "adjuster_id": "UUID",
    "previous_status": "initial_review",
    "new_status": "site_inspection",
    "priority": "standard",
    "incident_latitude": 33.7815,
    "incident_longitude": -84.3834,
    "notes": "Claim transitioned to site_inspection"
  }
}
```

| Field | Type | Description |
|---|---|---|
| claim_id | string | Claim being processed |
| claim_number | string | Human-readable claim reference |
| policy_id | string | Associated policy |
| adjuster_id | string | Adjuster handling the claim |
| previous_status | string | Status before transition |
| new_status | string | Status after transition |
| priority | string | low, medium, high |
| incident_latitude | real | Latitude of incident location |
| incident_longitude | real | Longitude of incident location |
| notes | string | Notes on the status change |

### Claim Lifecycle Flow

```
open → initial_review → site_inspection → document_request → estimate_prepared → payment_issued
                                                                                └→ denial_issued
```

---

## 2. FraudAlertEvent

Automated fraud detection alerts raised when a claim triggers suspicious-pattern rules. Includes confidence scoring and recommended actions.

```json
{
  "event_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "event_type": "FraudAlertEvent",
  "timestamp": "2026-03-15T14:32:15Z",
  "source": "fraud-detection-engine",
  "body": {
    "claim_id": "UUID",
    "policy_id": "UUID",
    "policyholder_id": "UUID",
    "alert_type": "duplicate_claim",
    "severity": "high",
    "confidence_score": 0.92,
    "description": "Potential duplicate claim detected — similar incident details found on another policy",
    "recommended_action": "refer_to_siu"
  }
}
```

| Field | Type | Description |
|---|---|---|
| claim_id | string | Claim flagged for fraud |
| policy_id | string | Associated policy |
| policyholder_id | string | Policyholder on the claim |
| alert_type | string | Type of fraud indicator (see table below) |
| severity | string | low, medium, high |
| confidence_score | real | Model confidence (0.0–1.0) |
| description | string | Human-readable description of the fraud indicator |
| recommended_action | string | `refer_to_siu` or `flag_for_review` |

### Fraud Alert Types

| alert_type | Description | Severity |
|---|---|---|
| duplicate_claim | Similar incident details found on another policy | high |
| excessive_amount | Claimed loss significantly exceeds asset valuation | high |
| recent_policy | Claim filed within 90 days of policy inception | medium |
| frequency_spike | Policyholder claim frequency exceeds historical baseline | medium |
| address_mismatch | Incident location inconsistent with registered address | low |
| late_reporting | Significant delay between incident date and filing date | low |

---

## 3. InspectionEvent

Asset inspection scheduling, execution, and results. Generated when a claim reaches the site inspection stage or when a standalone inspection is triggered.

```json
{
  "event_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "event_type": "InspectionEvent",
  "timestamp": "2026-03-16T10:00:00Z",
  "source": "inspection-service",
  "body": {
    "claim_id": "UUID",
    "asset_id": "UUID",
    "adjuster_id": "UUID",
    "inspection_type": "field_inspection",
    "result": "completed",
    "damage_estimate": 8250.00,
    "latitude": 33.7815,
    "longitude": -84.3834,
    "notes": "Field Inspection — completed"
  }
}
```

| Field | Type | Description |
|---|---|---|
| claim_id | string | Associated claim |
| asset_id | string | Asset being inspected |
| adjuster_id | string | Adjuster conducting or ordering the inspection |
| inspection_type | string | field_inspection, desk_review, photo_appraisal, independent_appraisal |
| result | string | scheduled, in_progress, completed |
| damage_estimate | real | Estimated damage amount (null until completed) |
| latitude | real | Inspection location latitude |
| longitude | real | Inspection location longitude |
| notes | string | Inspection notes |

---

## 4. PolicyChangeEvent

Policy modifications triggered during claim processing — endorsements, coverage updates, deductible changes, and renewals.

```json
{
  "event_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "event_type": "PolicyChangeEvent",
  "timestamp": "2026-03-17T11:30:00Z",
  "source": "policy-admin-system",
  "body": {
    "policy_id": "UUID",
    "policyholder_id": "UUID",
    "change_type": "deductible_changed",
    "previous_value": "1000",
    "new_value": "1500",
    "effective_date": "2026-03-17T11:30:00Z",
    "notes": "Automated deductible changed during claim processing"
  }
}
```

| Field | Type | Description |
|---|---|---|
| policy_id | string | Policy being modified |
| policyholder_id | string | Policyholder on the policy |
| change_type | string | endorsement_added, coverage_updated, deductible_changed, renewal_processed |
| previous_value | string | Value before change |
| new_value | string | Value after change |
| effective_date | datetime | When the change takes effect |
| notes | string | Description of the change |

---

## 5. PaymentEvent

Claim payment processing and disbursements — generated when a claim reaches the payment stage.

```json
{
  "event_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
  "event_type": "PaymentEvent",
  "timestamp": "2026-03-18T14:00:00Z",
  "source": "payment-processing",
  "body": {
    "claim_id": "UUID",
    "policy_id": "UUID",
    "payee_id": "UUID",
    "payment_type": "claim_settlement",
    "amount": 7650.00,
    "currency": "USD",
    "payment_status": "processed",
    "payment_method": "ACH",
    "notes": "Settlement payment for claim CLM-70001"
  }
}
```

| Field | Type | Description |
|---|---|---|
| claim_id | string | Claim being paid |
| policy_id | string | Associated policy |
| payee_id | string | Recipient (typically the policyholder) |
| payment_type | string | claim_settlement |
| amount | real | Payment amount in USD |
| currency | string | Currency code (USD) |
| payment_status | string | processed |
| payment_method | string | ACH, check, wire_transfer |
| notes | string | Payment description |

---

## Demo Scenarios

The event generation notebook (`02_generate_events.ipynb`) injects 5 demo scenarios that produce distinctive event patterns:

| Scenario | Trigger | Events Produced |
|---|---|---|
| **Late Resolution** | Claim open past SLA target days | `ClaimStatusEvent` with SLA breach note |
| **Major Loss** | Estimated loss > $100,000 | `FraudAlertEvent` (high severity) + `ClaimStatusEvent` (priority escalation) |
| **Adjuster Overload** | Adjuster at max capacity - 2 | `ClaimStatusEvent` with capacity warning |
| **Inspection Due** | Claim reaches site_inspection stage | `InspectionEvent` (field_inspection, scheduled) |
| **Claim Reassignment** | Major loss + document/estimate stage | `ClaimStatusEvent` with reassignment note |

### Querying Scenarios in KQL

```kql
// Late Resolution
ClaimStatusEvent | where notes has "SLA breach"

// Major Loss
FraudAlertEvent | where severity == "high"
ClaimStatusEvent | where notes has "Major loss"

// Adjuster Overload
ClaimStatusEvent | where notes has "capacity"

// Inspection Due
InspectionEvent | where result == "scheduled"

// Claim Reassignment
ClaimStatusEvent | where notes has "reassigned"
```
