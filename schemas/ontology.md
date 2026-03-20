# Ontology Schema — Insurance Claims Intelligence

8 entity types and 10 relationships, created programmatically by `03_create_ontology.ipynb` via the Fabric REST API. All entities are backed by Delta tables in the `lh_insurance` Lakehouse and exposed through the `InsuranceSM` semantic model.

---

## Entity Definitions

---

### Office

Regional insurance office or claims processing center where adjusters are based.

| Field | Type | Nullable | Description |
|---|---|---|---|
| office_id | string | No | **Primary key** |
| name | string | No | Office name (e.g., "Atlanta Regional Office") |
| office_type | string | No | `regional` · `branch` · `claims_center` |
| address | string | No | Street address |
| city | string | No | City |
| state | string | No | US state (2-letter) |
| zip_code | string | No | ZIP code |
| latitude | double | No | GPS latitude |
| longitude | double | No | GPS longitude |
| timezone | string | No | IANA timezone (e.g., "America/New_York") |
| phone | string | Yes | Main office phone |
| adjuster_capacity | int | Yes | Maximum adjusters at this office |
| has_siu_unit | boolean | Yes | Whether this office has a Special Investigations Unit |

**Referenced by:** `adjusters.home_office_id`, `claims.office_id`

---

### Policyholder

Individual or business holding one or more insurance policies.

| Field | Type | Nullable | Description |
|---|---|---|---|
| policyholder_id | string | No | **Primary key** |
| policyholder_number | string | No | Human-readable ID (e.g., "PH-10001") |
| full_name | string | No | Individual or business name |
| policyholder_type | string | No | `individual` · `business` |
| email | string | Yes | Contact email |
| phone | string | Yes | Contact phone |
| address | string | Yes | Street address |
| city | string | Yes | City |
| state | string | Yes | US state |
| zip_code | string | Yes | ZIP code |
| date_of_birth | string | Yes | Date of birth (null for businesses) |
| risk_score | int | Yes | Underwriting risk score (1–100) |

**Referenced by:** `policies.policyholder_id`, `claims.policyholder_id`

---

### InsuredAsset

Property, vehicle, or item covered by an insurance policy.

| Field | Type | Nullable | Description |
|---|---|---|---|
| asset_id | string | No | **Primary key** |
| asset_number | string | No | Human-readable ID (e.g., "AST-20001") |
| asset_type | string | No | `vehicle` · `residential_property` · `commercial_property` · `personal_property` |
| asset_description | string | No | Short description (e.g., "2022 Toyota Camry SE") |
| make | string | Yes | Manufacturer/builder (vehicles only) |
| model | string | Yes | Model (vehicles only) |
| year | int | No | Year built/manufactured |
| vin | string | Yes | VIN for vehicles, null otherwise |
| address | string | Yes | Property address (null for vehicles) |
| city | string | Yes | City where asset is located |
| state | string | Yes | US state |
| estimated_value | double | Yes | Current estimated value in USD |
| condition | string | Yes | `excellent` · `good` · `fair` · `poor` |
| last_inspection_date | string | Yes | Most recent inspection/appraisal date |

**Referenced by:** `policies.asset_id`, `claims.asset_id`

---

### Adjuster

Licensed claims adjuster who investigates, evaluates, and settles insurance claims.

| Field | Type | Nullable | Description |
|---|---|---|---|
| adjuster_id | string | No | **Primary key** |
| employee_id | string | No | Employee number (e.g., "ADJ-3001") |
| first_name | string | No | First name |
| last_name | string | No | Last name |
| email | string | Yes | Work email |
| phone | string | Yes | Work phone |
| license_number | string | No | Adjuster license number |
| license_state | string | No | State of licensure |
| specializations | array[string] | Yes | e.g., `["auto","property","liability"]` |
| hire_date | string | Yes | Employment start date |
| status | string | No | `available` · `on_assignment` · `on_leave` · `inactive` |
| home_office_id | string | No | **FK → Office** |
| supervisor_email | string | Yes | Manager's email |
| max_active_claims | int | Yes | Maximum concurrent claim assignments |

**References:** `offices.office_id`
**Referenced by:** `claims.adjuster_id`, `claim_events.adjuster_id`

---

### Policy

Insurance policy linking a policyholder to coverage on an insured asset.

| Field | Type | Nullable | Description |
|---|---|---|---|
| policy_id | string | No | **Primary key** |
| policy_number | string | No | Human-readable ID (e.g., "POL-50001") |
| policyholder_id | string | No | **FK → Policyholder** |
| asset_id | string | No | **FK → InsuredAsset** |
| policy_type | string | No | `auto` · `homeowners` · `commercial_property` · `renters` |
| coverage_amount | double | Yes | Maximum coverage in USD |
| deductible | double | Yes | Policyholder deductible in USD |
| premium_annual | double | Yes | Annual premium in USD |
| effective_date | string | Yes | Policy start date |
| expiration_date | string | Yes | Policy end date |
| status | string | No | `active` · `expired` · `cancelled` · `pending_renewal` |
| underwriter | string | Yes | Name of underwriter |

**References:** `policyholders.policyholder_id`, `insured_assets.asset_id`
**Referenced by:** `claims.policy_id`

---

### Claim

Insurance claim filed by a policyholder for a covered loss event. **Central entity** — all other entities radiate from it.

| Field | Type | Nullable | Description |
|---|---|---|---|
| claim_id | string | No | **Primary key** |
| claim_number | string | No | Human-readable ID (e.g., "CLM-70001") |
| policy_id | string | No | **FK → Policy** |
| policyholder_id | string | No | **FK → Policyholder** (denormalized) |
| asset_id | string | No | **FK → InsuredAsset** |
| adjuster_id | string | No | **FK → Adjuster** |
| office_id | string | No | **FK → Office** |
| claim_type | string | No | `auto_collision` · `auto_theft` · `property_damage` · `fire` · `water_damage` · `liability` · `weather` |
| description | string | Yes | Free-text description of the incident |
| incident_date | string | Yes | When the incident occurred |
| filed_date | string | Yes | When the claim was filed |
| status | string | No | `filed` · `under_review` · `investigation` · `approved` · `denied` · `paid` · `closed` |
| estimated_loss | double | Yes | Initial estimated loss amount |
| approved_amount | double | Yes | Approved payout (null until approved) |
| priority | string | Yes | `low` · `standard` · `high` · `catastrophe` |
| incident_latitude | double | Yes | Latitude of incident |
| incident_longitude | double | Yes | Longitude of incident |

**References:** `policies.policy_id`, `policyholders.policyholder_id`, `insured_assets.asset_id`, `adjusters.adjuster_id`, `offices.office_id`
**Referenced by:** `claim_events.claim_id`

---

### ClaimEvent

Discrete event in a claim's lifecycle — initial reviews, inspections, document requests, estimates, payments, and denials.

| Field | Type | Nullable | Description |
|---|---|---|---|
| claim_event_id | string | No | **Primary key** |
| event_number | string | No | Human-readable ID (e.g., "CE-40001") |
| claim_id | string | No | **FK → Claim** |
| adjuster_id | string | No | **FK → Adjuster** |
| event_type | string | No | `initial_review` · `site_inspection` · `document_request` · `estimate_prepared` · `payment_issued` · `denial_issued` · `appeal_received` · `subrogation_filed` |
| description | string | Yes | Details of the event |
| status | string | No | `pending` · `completed` · `cancelled` |
| created_at | string | Yes | When the event was created |
| completed_at | string | Yes | When the event was completed |
| notes | string | Yes | Adjuster notes |
| cost_usd | double | Yes | Cost associated with event (e.g., payment amount) |

**References:** `claims.claim_id`, `adjusters.adjuster_id`

---

### AssetInspection

Field inspection or appraisal of an insured asset, conducted by or on behalf of a regional office.

| Field | Type | Nullable | Description |
|---|---|---|---|
| inspection_id | string | No | **Primary key** |
| asset_id | string | No | **FK → InsuredAsset** |
| office_id | string | No | **FK → Office** |
| inspection_type | string | No | `initial_appraisal` · `annual_review` · `claim_related` · `underwriting` |
| status | string | No | `scheduled` · `completed` · `cancelled` |
| scheduled_date | string | Yes | When inspection is planned |
| completed_date | string | Yes | When inspection occurred |
| appraised_value | double | Yes | Value determined by inspection |
| inspector_notes | string | Yes | Free-text notes |
| condition_rating | string | Yes | `excellent` · `good` · `fair` · `poor` |

**References:** `insured_assets.asset_id`, `offices.office_id`

---

## Ontology Relationships (10)

Defined in `03_create_ontology.ipynb` and bound via contextualizations to Lakehouse tables.

| Relationship | Source Entity | Target Entity | Join Column |
|---|---|---|---|
| PolicyCoversPolicyholder | Policy | Policyholder | policyholder_id |
| PolicyCoversAsset | Policy | InsuredAsset | asset_id |
| ClaimUnderPolicy | Claim | Policy | policy_id |
| ClaimInvolvesAsset | Claim | InsuredAsset | asset_id |
| ClaimAssignedToAdjuster | Claim | Adjuster | adjuster_id |
| ClaimFiledByPolicyholder | Claim | Policyholder | policyholder_id |
| ClaimEventForClaim | ClaimEvent | Claim | claim_id |
| AdjusterAtOffice | Adjuster | Office | home_office_id |
| InspectionForAsset | AssetInspection | InsuredAsset | asset_id |
| InspectionAtOffice | AssetInspection | Office | office_id |

---

## Relationship Diagram

```
                    ┌──────────────┐
                    │ Policyholder │
                    └──────┬───────┘
                           │ PolicyCoversPolicyholder
                           │ ClaimFiledByPolicyholder
                           │
                    ┌──────┴───────┐
      ┌─────────── │    Policy     │ ───────────┐
      │            └──────────────┘              │
      │ ClaimUnderPolicy            PolicyCoversAsset
      ▼                                         ▼
┌──────────────┐                        ┌──────────────┐
│    Claim     │── ClaimInvolvesAsset ─→│ InsuredAsset │◀─── InspectionForAsset ───┐
└──────┬───┬───┘                        └──────────────┘                           │
       │   │                                                                ┌──────┴────────────┐
       │   │ ClaimAssignedToAdjuster                                        │ AssetInspection    │
       │   ▼                                                                └──────┬────────────┘
       │  ┌──────────────┐                                                         │
       │  │   Adjuster   │── AdjusterAtOffice ─→┐                                  │
       │  └──────────────┘                       │                                  │
       │                                         │           InspectionAtOffice     │
       │         ┌──────────────┐                │                                  │
       │         │    Office    │◀───────────────┘◀─────────────────────────────────┘
       │         └──────────────┘
       │
       │  ClaimEventForClaim
       ▼
┌──────────────┐
│  ClaimEvent  │
└──────────────┘
```
