"""Validate referential integrity of generated JSONL reference data."""
import json, os, sys

data_dir = os.path.join(os.path.dirname(__file__), "..", "reference_data")
files = {
    "offices": "office_id",
    "policyholders": "policyholder_id",
    "insured_assets": "asset_id",
    "adjusters": "adjuster_id",
    "policies": "policy_id",
    "claims": "claim_id",
    "claim_events": "claim_event_id",
    "asset_inspections": "inspection_id",
}

all_data = {}
all_ids = {}
errors = []

print("Record counts & PK uniqueness:")
for name, pk in files.items():
    path = os.path.join(data_dir, f"{name}.jsonl")
    records = []
    with open(path, "r") as f:
        for line_num, line in enumerate(f, 1):
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                errors.append(f"{name}.jsonl line {line_num}: Invalid JSON: {e}")
    all_data[name] = records
    ids = [r[pk] for r in records]
    all_ids[name] = set(ids)
    unique = len(ids) == len(set(ids))
    if not unique:
        errors.append(f"{name}: DUPLICATE primary keys detected!")
    print(f"  {name:<25} {len(records):>4} records, PK unique: {unique}")

print("\nForeign key validation:")
fk_checks = [
    ("adjusters", "home_office_id", "offices"),
    ("policies", "policyholder_id", "policyholders"),
    ("policies", "asset_id", "insured_assets"),
    ("claims", "policy_id", "policies"),
    ("claims", "policyholder_id", "policyholders"),
    ("claims", "asset_id", "insured_assets"),
    ("claims", "adjuster_id", "adjusters"),
    ("claims", "office_id", "offices"),
    ("claim_events", "claim_id", "claims"),
    ("claim_events", "adjuster_id", "adjusters"),
    ("asset_inspections", "asset_id", "insured_assets"),
    ("asset_inspections", "office_id", "offices"),
]

for table, fk_col, ref_table in fk_checks:
    ref_ids = all_ids[ref_table]
    orphans = sum(1 for rec in all_data[table] if rec.get(fk_col) and rec[fk_col] not in ref_ids)
    status = "OK" if orphans == 0 else f"FAIL ({orphans} orphans)"
    print(f"  {table}.{fk_col} -> {ref_table}: {status}")
    if orphans > 0:
        errors.append(f"{table}.{fk_col} has {orphans} orphan references to {ref_table}")

print("\nClaim status distribution:")
statuses = {}
for c in all_data["claims"]:
    statuses[c["status"]] = statuses.get(c["status"], 0) + 1
for s, count in sorted(statuses.items()):
    print(f"  {s}: {count}")

print("\nPolicy type distribution:")
ptypes = {}
for p in all_data["policies"]:
    ptypes[p["policy_type"]] = ptypes.get(p["policy_type"], 0) + 1
for t, count in sorted(ptypes.items()):
    print(f"  {t}: {count}")

print()
if errors:
    print(f"ERRORS FOUND: {len(errors)}")
    for e in errors:
        print(f"  ! {e}")
    sys.exit(1)
else:
    print("ALL VALIDATION PASSED")
