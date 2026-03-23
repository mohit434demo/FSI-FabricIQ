"""
Generate synthetic reference data for the Insurance Claims Intelligence demo.
Produces 8 JSONL files in the ../reference_data/ folder.

Usage:
    cd scripts
    python generate_reference_data.py
"""

import json
import uuid
import random
import os
from datetime import datetime, timedelta, date

random.seed(42)

OUTPUT_DIR = os.environ.get(
    "REFERENCE_OUTPUT_DIR",
    os.path.join(os.path.dirname(__file__), "..", "reference_data"),
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def new_id():
    return str(uuid.uuid4())

def write_jsonl(filename, records):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, default=str) + "\n")
    print(f"  Wrote {len(records):>4} records → {filename}")

def random_date(start, end):
    """Random date between start and end (date objects)."""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def random_datetime(start, end):
    """Random datetime between start and end (datetime objects)."""
    delta = (end - start).total_seconds()
    return start + timedelta(seconds=random.randint(0, int(delta)))

def random_phone():
    return f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"

def random_zip(state):
    """Return a plausible ZIP code prefix for a US state."""
    zip_prefixes = {
        "GA": "303", "IL": "606", "TX": "752", "CO": "802", "IN": "462",
        "FL": "322", "MO": "641", "CA": "900", "TN": "372", "NJ": "071",
        "AZ": "850", "UT": "841", "WA": "981", "OH": "432", "PA": "152",
        "NE": "681", "MA": "021", "MI": "482", "MD": "212", "NC": "287",
        "OR": "972", "KS": "672", "LA": "708", "WI": "532", "VA": "232",
        "NY": "100", "MN": "554",
    }
    prefix = zip_prefixes.get(state, "100")
    return prefix + f"{random.randint(0, 99):02d}"

# ---------------------------------------------------------------------------
# Name pools (shared across policyholders, adjusters, underwriters)
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "James","Robert","John","Michael","David","William","Richard","Joseph","Thomas","Christopher",
    "Daniel","Matthew","Anthony","Mark","Steven","Paul","Andrew","Joshua","Kenneth","Kevin",
    "Maria","Jennifer","Linda","Patricia","Elizabeth","Susan","Jessica","Sarah","Karen","Lisa",
    "Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna","Michelle",
    "Carlos","Miguel","Juan","Luis","Jorge","Pedro","Rafael","Diego","Antonio","Fernando",
    "Aisha","Fatima","Priya","Wei","Yuki","Olga","Svetlana","Ingrid","Amara","Kenji",
    "Marcus","Tyrone","Deshawn","Jamal","Terrance",
]

LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
    "Patel","Kim","Singh","Chen","O'Brien","Murphy","Sullivan","Cohen","Yamamoto","Petrov",
    "Okafor","Washington","Freeman","Brooks","Howard",
]

UNDERWRITER_NAMES = [
    "Maria Chen", "David Park", "Lisa Thompson", "James O'Brien",
    "Priya Patel", "Robert Sullivan", "Angela Torres", "Kenneth Adams",
]

# ---------------------------------------------------------------------------
# 1. Offices – 15 regional insurance offices
# ---------------------------------------------------------------------------

OFFICE_DATA = [
    ("Atlanta Regional Office",      "regional",       "200 Peachtree St NE, Suite 800",   "Atlanta",        "GA", 33.7590, -84.3880, "America/New_York"),
    ("Chicago Claims Center",        "claims_center",  "233 S Wacker Dr, Suite 1200",      "Chicago",        "IL", 41.8788, -87.6359, "America/Chicago"),
    ("Dallas Branch Office",         "branch",         "1700 Pacific Ave, Suite 300",       "Dallas",         "TX", 32.7876, -96.7985, "America/Chicago"),
    ("Denver Regional Office",       "regional",       "1801 California St, Suite 500",     "Denver",         "CO", 39.7471, -104.9887, "America/Denver"),
    ("Houston Claims Center",        "claims_center",  "1000 Main St, Suite 600",           "Houston",        "TX", 29.7523, -95.3655, "America/Chicago"),
    ("Indianapolis Branch Office",   "branch",         "101 W Washington St, Suite 400",    "Indianapolis",   "IN", 39.7684, -86.1581, "America/Indiana/Indianapolis"),
    ("Jacksonville Branch Office",   "branch",         "50 N Laura St, Suite 200",          "Jacksonville",   "FL", 30.3274, -81.6602, "America/New_York"),
    ("Kansas City Regional Office",  "regional",       "920 Main St, Suite 700",            "Kansas City",    "MO", 39.0997, -94.5786, "America/Chicago"),
    ("Los Angeles Claims Center",    "claims_center",  "515 S Flower St, Suite 1800",       "Los Angeles",    "CA", 34.0494, -118.2641, "America/Los_Angeles"),
    ("Memphis Branch Office",        "branch",         "6075 Poplar Ave, Suite 350",        "Memphis",        "TN", 35.1028, -89.8659, "America/Chicago"),
    ("Nashville Branch Office",      "branch",         "333 Commerce St, Suite 200",        "Nashville",      "TN", 36.1659, -86.7844, "America/Chicago"),
    ("Newark Regional Office",       "regional",       "1 Gateway Center, Suite 1000",      "Newark",         "NJ", 40.7357, -74.1724, "America/New_York"),
    ("Phoenix Branch Office",        "branch",         "2 N Central Ave, Suite 400",        "Phoenix",        "AZ", 33.4502, -112.0733, "America/Phoenix"),
    ("Salt Lake City Branch Office", "branch",         "111 S Main St, Suite 300",          "Salt Lake City", "UT", 40.7608, -111.8910, "America/Denver"),
    ("Seattle Regional Office",      "regional",       "1201 Third Ave, Suite 800",         "Seattle",        "WA", 47.6075, -122.3364, "America/Los_Angeles"),
]

def generate_offices():
    offices = []
    for name, otype, address, city, state, lat, lon, tz in OFFICE_DATA:
        offices.append({
            "office_id": new_id(),
            "name": name,
            "office_type": otype,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": random_zip(state),
            "latitude": lat,
            "longitude": lon,
            "timezone": tz,
            "phone": random_phone(),
            "adjuster_capacity": random.choice([15, 20, 25, 30, 35, 40]),
            "has_siu_unit": otype in ("regional", "claims_center"),
        })
    return offices

# ---------------------------------------------------------------------------
# 2. Policyholders – 20 individuals and businesses
# ---------------------------------------------------------------------------

BUSINESS_NAMES = [
    ("Heartland Foods Inc.",         "Des Moines",    "IA"),
    ("Pacific Coast Electronics",    "San Jose",      "CA"),
    ("Southern Timber Co.",          "Savannah",      "GA"),
    ("Great Plains Agriculture",     "Omaha",         "NE"),
    ("Midwest Auto Parts",           "Detroit",       "MI"),
    ("Sunshine Beverages",           "Orlando",       "FL"),
    ("Liberty Steel Works",          "Pittsburgh",    "PA"),
    ("Cascade Paper Products",       "Portland",      "OR"),
    ("Lakeshore Retail Group",       "Milwaukee",     "WI"),
    ("Canyon Construction LLC",      "Flagstaff",     "AZ"),
]

INDIVIDUAL_CITIES = [
    ("Atlanta", "GA"), ("Chicago", "IL"), ("Dallas", "TX"), ("Denver", "CO"),
    ("Houston", "TX"), ("Jacksonville", "FL"), ("Los Angeles", "CA"),
    ("Nashville", "TN"), ("Phoenix", "AZ"), ("Seattle", "WA"),
]

def generate_policyholders():
    policyholders = []
    used_names = set()

    # 10 individuals
    for i in range(10):
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            if (first, last) not in used_names:
                used_names.add((first, last))
                break
        city, state = random.choice(INDIVIDUAL_CITIES)
        dob = random_date(date(1955, 1, 1), date(2000, 12, 31))
        policyholders.append({
            "policyholder_id": new_id(),
            "policyholder_number": f"PH-{10001 + i}",
            "full_name": f"{first} {last}",
            "policyholder_type": "individual",
            "email": f"{first.lower()}.{last.lower()}@email.com",
            "phone": random_phone(),
            "address": f"{random.randint(100, 9999)} {random.choice(['Oak', 'Elm', 'Maple', 'Pine', 'Cedar', 'Main', 'Park', 'Lake'])} {random.choice(['St', 'Ave', 'Dr', 'Blvd', 'Ln'])}",
            "city": city,
            "state": state,
            "zip_code": random_zip(state),
            "date_of_birth": str(dob),
            "risk_score": random.randint(10, 85),
        })

    # 10 businesses
    for i, (bname, city, state) in enumerate(BUSINESS_NAMES):
        policyholders.append({
            "policyholder_id": new_id(),
            "policyholder_number": f"PH-{10011 + i}",
            "full_name": bname,
            "policyholder_type": "business",
            "email": f"insurance@{bname.split()[0].lower()}.com",
            "phone": random_phone(),
            "address": f"{random.randint(100, 9999)} {random.choice(['Industrial', 'Commerce', 'Corporate', 'Enterprise'])} {random.choice(['Blvd', 'Dr', 'Pkwy'])}",
            "city": city,
            "state": state,
            "zip_code": random_zip(state),
            "date_of_birth": None,
            "risk_score": random.randint(25, 90),
        })

    return policyholders

# ---------------------------------------------------------------------------
# 3. Insured Assets – 50 vehicles, homes, and commercial properties
# ---------------------------------------------------------------------------

VEHICLE_MAKES = [
    ("Toyota", "Camry"),  ("Toyota", "RAV4"),   ("Honda", "Civic"),
    ("Honda", "CR-V"),    ("Ford", "F-150"),     ("Ford", "Explorer"),
    ("Chevrolet", "Silverado"), ("Chevrolet", "Equinox"),
    ("Tesla", "Model 3"), ("Tesla", "Model Y"),
    ("BMW", "X5"),        ("Mercedes-Benz", "C-Class"),
    ("Jeep", "Grand Cherokee"), ("Subaru", "Outback"),
    ("Hyundai", "Tucson"), ("Nissan", "Altima"),
]

def random_vin():
    """Generate a plausible 17-char VIN."""
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return "".join(random.choices(chars, k=17))

def generate_insured_assets(policyholders):
    assets = []
    idx = 0

    # 20 vehicles
    for i in range(20):
        make, model = random.choice(VEHICLE_MAKES)
        year = random.randint(2017, 2025)
        ph = policyholders[i % len(policyholders)]
        assets.append({
            "asset_id": new_id(),
            "asset_number": f"AST-{20001 + idx}",
            "asset_type": "vehicle",
            "asset_description": f"{year} {make} {model}",
            "make": make,
            "model": model,
            "year": year,
            "vin": random_vin(),
            "address": None,
            "city": ph["city"],
            "state": ph["state"],
            "estimated_value": round(random.uniform(12000, 85000), 2),
            "condition": random.choice(["excellent", "good", "good", "fair"]),
            "last_inspection_date": str(random_date(date(2024, 6, 1), date(2026, 2, 28))),
        })
        idx += 1

    # 20 residential properties
    for i in range(20):
        year = random.randint(1960, 2023)
        sqft = random.choice([1200, 1600, 1800, 2000, 2400, 2800, 3200, 3600])
        ph = policyholders[i % len(policyholders)]
        assets.append({
            "asset_id": new_id(),
            "asset_number": f"AST-{20001 + idx}",
            "asset_type": "residential_property",
            "asset_description": f"Single-family home — {sqft:,} sq ft",
            "make": None,
            "model": None,
            "year": year,
            "vin": None,
            "address": f"{random.randint(100, 9999)} {random.choice(['Oak', 'Elm', 'Maple', 'Pine', 'Birch', 'Willow', 'Hickory'])} {random.choice(['St', 'Ave', 'Dr', 'Ct', 'Way'])}",
            "city": ph["city"],
            "state": ph["state"],
            "estimated_value": round(random.uniform(180000, 750000), 2),
            "condition": random.choice(["excellent", "good", "good", "fair", "fair"]),
            "last_inspection_date": str(random_date(date(2024, 1, 1), date(2026, 2, 28))),
        })
        idx += 1

    # 10 commercial properties
    for i in range(10):
        year = random.randint(1975, 2020)
        sqft = random.choice([10000, 20000, 30000, 50000, 75000, 100000])
        ph = [p for p in policyholders if p["policyholder_type"] == "business"]
        ph = ph[i % len(ph)]
        desc_type = random.choice(["Office building", "Warehouse", "Manufacturing facility", "Retail space", "Mixed-use building"])
        assets.append({
            "asset_id": new_id(),
            "asset_number": f"AST-{20001 + idx}",
            "asset_type": "commercial_property",
            "asset_description": f"{desc_type} — {sqft:,} sq ft",
            "make": None,
            "model": None,
            "year": year,
            "vin": None,
            "address": f"{random.randint(100, 9999)} {random.choice(['Industrial', 'Commerce', 'Corporate', 'Enterprise', 'Business'])} {random.choice(['Blvd', 'Dr', 'Pkwy', 'Way'])}",
            "city": ph["city"],
            "state": ph["state"],
            "estimated_value": round(random.uniform(500000, 5000000), 2),
            "condition": random.choice(["excellent", "good", "good", "fair"]),
            "last_inspection_date": str(random_date(date(2024, 1, 1), date(2026, 2, 28))),
        })
        idx += 1

    return assets

# ---------------------------------------------------------------------------
# 4. Adjusters – 25 claims adjusters
# ---------------------------------------------------------------------------

ADJUSTER_SPECIALIZATIONS = [
    "auto",
    "auto",
    "auto, liability",
    "property",
    "property, commercial_property",
    "auto, property",
    "auto, property, liability",
    "commercial_property",
    "liability",
    "auto, liability",
]

# Map policy_type → which specialization tokens qualify
POLICY_TYPE_TO_SPECS = {
    "auto":                {"auto"},
    "homeowners":          {"property"},
    "commercial_property": {"commercial_property", "property"},
    "renters":             {"property"},
}

def generate_adjusters(offices):
    adjusters = []
    used_names = set()

    for i in range(25):
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            if (first, last) not in used_names:
                used_names.add((first, last))
                break

        office = random.choice(offices)
        lic_state = office["state"]
        hire_date = random_date(date(2015, 1, 1), date(2025, 6, 1))
        specializations = random.choice(ADJUSTER_SPECIALIZATIONS)

        adjusters.append({
            "adjuster_id": new_id(),
            "employee_id": f"ADJ-{3001 + i}",
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}@insuranceco.com",
            "phone": random_phone(),
            "license_number": f"{lic_state}-ADJ-{random.randint(10000, 99999)}",
            "license_state": lic_state,
            "specializations": specializations,
            "hire_date": str(hire_date),
            "status": "available",  # updated after claims are assigned
            "home_office_id": office["office_id"],
            "supervisor_email": f"supervisor.{office['city'].lower().replace(' ', '')}@insuranceco.com",
            "max_active_claims": random.choice([10, 12, 15, 18, 20]),
        })
    return adjusters


def find_matching_adjuster(adjusters, policy_type, exclude_ids=None):
    """Find an adjuster whose specializations match the policy type."""
    needed = POLICY_TYPE_TO_SPECS.get(policy_type, {"auto"})
    exclude_ids = exclude_ids or set()
    candidates = [
        a for a in adjusters
        if needed & {s.strip() for s in a["specializations"].split(",")} and a["adjuster_id"] not in exclude_ids
    ]
    if candidates:
        return random.choice(candidates)
    # Fallback: any adjuster not excluded
    fallback = [a for a in adjusters if a["adjuster_id"] not in exclude_ids]
    return random.choice(fallback) if fallback else random.choice(adjusters)

# ---------------------------------------------------------------------------
# 5. Policies – 45 insurance policies
# ---------------------------------------------------------------------------

POLICY_TYPES = ["auto", "auto", "auto", "homeowners", "homeowners", "commercial_property", "renters"]

COVERAGE_RANGES = {
    "auto":                (25000, 100000),
    "homeowners":          (200000, 800000),
    "commercial_property": (500000, 5000000),
    "renters":             (15000, 50000),
}

DEDUCTIBLE_RANGES = {
    "auto":                (250, 2000),
    "homeowners":          (500, 5000),
    "commercial_property": (5000, 25000),
    "renters":             (250, 1000),
}

PREMIUM_RANGES = {
    "auto":                (600, 3000),
    "homeowners":          (1200, 5000),
    "commercial_property": (8000, 50000),
    "renters":             (150, 600),
}

# Status weights: ~75% active, ~10% pending_renewal, ~10% expired, ~5% cancelled
POLICY_STATUS_WEIGHTS = (
    ["active"] * 15
    + ["pending_renewal"] * 2
    + ["expired"] * 2
    + ["cancelled"] * 1
)

def _pick_policy_type_for_asset(asset):
    """Choose a policy type compatible with an asset type."""
    at = asset["asset_type"]
    if at == "vehicle":
        return "auto"
    elif at == "commercial_property":
        return "commercial_property"
    elif at == "residential_property":
        return random.choice(["homeowners", "renters"])
    return random.choice(POLICY_TYPES)

def _make_policy(idx, ph, asset, ptype):
    """Build a single policy dict."""
    cov_lo, cov_hi = COVERAGE_RANGES[ptype]
    ded_lo, ded_hi = DEDUCTIBLE_RANGES[ptype]
    prem_lo, prem_hi = PREMIUM_RANGES[ptype]

    eff_date = random_date(date(2025, 1, 1), date(2026, 2, 28))
    exp_date = eff_date + timedelta(days=365)
    status = random.choice(POLICY_STATUS_WEIGHTS)

    return {
        "policy_id": new_id(),
        "policy_number": f"POL-{50001 + idx}",
        "policyholder_id": ph["policyholder_id"],
        "asset_id": asset["asset_id"],
        "policy_type": ptype,
        "coverage_amount": round(random.uniform(cov_lo, cov_hi), 2),
        "deductible": round(random.uniform(ded_lo, ded_hi), 2),
        "premium_annual": round(random.uniform(prem_lo, prem_hi), 2),
        "effective_date": str(eff_date),
        "expiration_date": str(exp_date),
        "status": status,
        "underwriter": random.choice(UNDERWRITER_NAMES),
    }

def generate_policies(policyholders, assets):
    policies = []
    idx = 0
    covered_ph_ids = set()
    covered_asset_ids = set()

    # Build asset pools by type for matching
    vehicle_assets = [a for a in assets if a["asset_type"] == "vehicle"]
    residential_assets = [a for a in assets if a["asset_type"] == "residential_property"]
    commercial_assets = [a for a in assets if a["asset_type"] == "commercial_property"]
    biz_phs = [p for p in policyholders if p["policyholder_type"] == "business"]

    # --- Pass 1: Guarantee every asset has at least one policy ---
    random.shuffle(assets)  # avoid predictable ordering
    for asset in assets:
        ptype = _pick_policy_type_for_asset(asset)
        if ptype == "commercial_property" and biz_phs:
            ph = random.choice(biz_phs)
        else:
            ph = random.choice(policyholders)
        policies.append(_make_policy(idx, ph, asset, ptype))
        covered_ph_ids.add(ph["policyholder_id"])
        covered_asset_ids.add(asset["asset_id"])
        idx += 1

    # --- Pass 2: Guarantee every policyholder has at least one policy ---
    for ph in policyholders:
        if ph["policyholder_id"] not in covered_ph_ids:
            if ph["policyholder_type"] == "business":
                asset = random.choice(commercial_assets) if commercial_assets else random.choice(assets)
            else:
                asset = random.choice(vehicle_assets + residential_assets)
            ptype = _pick_policy_type_for_asset(asset)
            policies.append(_make_policy(idx, ph, asset, ptype))
            covered_ph_ids.add(ph["policyholder_id"])
            idx += 1

    # --- Pass 3: Fill remaining to reach ~55 total (extra headroom for claims) ---
    target = max(55, idx)
    while idx < target:
        ptype = random.choice(POLICY_TYPES)
        if ptype == "commercial_property" and biz_phs:
            ph = random.choice(biz_phs)
        else:
            ph = random.choice(policyholders)
        pool = {"auto": vehicle_assets, "homeowners": residential_assets,
                "commercial_property": commercial_assets, "renters": residential_assets}
        asset_list = pool.get(ptype, vehicle_assets)
        asset = random.choice(asset_list) if asset_list else random.choice(assets)
        policies.append(_make_policy(idx, ph, asset, ptype))
        idx += 1

    return policies

# ---------------------------------------------------------------------------
# 6. Claims – 30 insurance claims (central entity)
# ---------------------------------------------------------------------------

CLAIM_TYPES = [
    "auto_collision", "auto_collision", "auto_collision",
    "auto_theft",
    "property_damage", "property_damage",
    "fire",
    "water_damage", "water_damage",
    "liability",
    "weather", "weather",
]

CLAIM_DESCRIPTIONS = {
    "auto_collision":  [
        "Rear-ended at traffic light intersection",
        "Side-impact collision in parking lot",
        "Multi-vehicle accident on highway during rain",
        "Single-vehicle accident — hit guardrail on curve",
        "T-bone collision at uncontrolled intersection",
        "Fender bender in drive-through lane",
    ],
    "auto_theft":      [
        "Vehicle stolen from apartment parking garage overnight",
        "Catalytic converter theft from parking lot",
        "Vehicle stolen from street parking — recovered damaged",
    ],
    "property_damage": [
        "Fallen tree damaged roof and siding after storm",
        "Burst pipe caused flooding in basement",
        "Vandalism — broken windows and graffiti",
        "Sewer backup caused interior damage",
    ],
    "fire":            [
        "Electrical fire in kitchen — smoke and water damage",
        "Warehouse fire from electrical fault in section B",
        "Grease fire in restaurant kitchen — structural damage",
    ],
    "water_damage":    [
        "Roof leak during heavy rainfall — ceiling and wall damage",
        "Washing machine overflow — hardwood floor damage",
        "Flash flooding in ground-floor commercial space",
    ],
    "liability":       [
        "Customer slip and fall on wet floor in retail space",
        "Contractor injury on commercial property",
        "Dog bite incident at insured residential property",
    ],
    "weather":         [
        "Hail damage to roof and siding from severe storm",
        "Wind damage — lost shingles and damaged gutters",
        "Tornado damage to detached garage and fencing",
        "Ice storm caused tree to collapse on roof",
    ],
}

CLAIM_STATUSES = ["filed", "under_review", "investigation", "approved", "denied", "paid", "closed"]

def generate_claims(policies, policyholders, assets, adjusters, offices):
    claims = []
    now = datetime(2026, 3, 17, 12, 0, 0)

    # Build lookup dicts
    ph_map = {p["policyholder_id"]: p for p in policyholders}
    asset_map = {a["asset_id"]: a for a in assets}

    # Two policy pools: open claims require active/pending_renewal policies
    open_policies = [p for p in policies if p["status"] in ("active", "pending_renewal")]
    all_policies = policies  # closed claims can reference any policy

    # Priority plan: exactly 1 catastrophe, 5 high, rest standard/low
    num_high = random.randint(4, 5)
    priority_schedule = (
        ["catastrophe"]
        + ["high"] * num_high
        + ["standard"] * (30 - 1 - num_high)
    )
    random.shuffle(priority_schedule)

    for i in range(30):
        # Determine claim status first (to choose policy pool)
        if i < 8:
            claim_status = "paid"
        elif i < 12:
            claim_status = "approved"
        elif i < 15:
            claim_status = "denied"
        elif i < 22:
            claim_status = "under_review"
        elif i < 27:
            claim_status = "investigation"
        else:
            claim_status = "filed"

        # Open claims → only active/pending_renewal policies
        if claim_status in ("filed", "under_review", "investigation"):
            pool = open_policies
        else:
            pool = all_policies
        policy = pool[i % len(pool)]
        ph = ph_map.get(policy["policyholder_id"], random.choice(policyholders))
        asset = asset_map.get(policy["asset_id"], random.choice(assets))
        adjuster = find_matching_adjuster(adjusters, policy["policy_type"])
        office = random.choice(offices)

        # Pick claim type compatible with asset type
        if asset["asset_type"] == "vehicle":
            ctype = random.choice(["auto_collision", "auto_collision", "auto_theft"])
        elif asset["asset_type"] == "commercial_property":
            ctype = random.choice(["property_damage", "fire", "liability"])
        else:
            ctype = random.choice(CLAIM_TYPES)

        description = random.choice(CLAIM_DESCRIPTIONS[ctype])

        # Timing: incident within last 60 days, filed 0-3 days after
        incident = now - timedelta(hours=random.randint(24, 60 * 24))
        filed = incident + timedelta(hours=random.randint(1, 72))

        # Priority for this claim (from pre-built schedule)
        priority = priority_schedule[i]

        # Estimate loss — catastrophe claims get high values
        if priority == "catastrophe":
            est_loss = round(random.uniform(150000, 500000), 2)
        elif ctype in ("auto_collision", "auto_theft"):
            est_loss = round(random.uniform(2000, 45000), 2)
        elif ctype in ("fire", "liability"):
            est_loss = round(random.uniform(10000, 500000), 2)
        else:
            est_loss = round(random.uniform(3000, 80000), 2)

        # Approved amount depends on claim status
        status = claim_status
        if status == "paid":
            approved_amount = round(est_loss * random.uniform(0.6, 1.0), 2)
        elif status == "approved":
            approved_amount = round(est_loss * random.uniform(0.7, 1.0), 2)
        else:
            approved_amount = None

        # Update adjuster status for active claims
        if status in ("under_review", "investigation", "filed"):
            adjuster["status"] = "on_assignment"

        # Use asset location for incident, with slight jitter
        if asset.get("city"):
            # Find matching office for approximate lat/lon
            matching_offices = [o for o in offices if o["state"] == asset["state"]]
            ref_office = matching_offices[0] if matching_offices else offices[0]
            inc_lat = round(ref_office["latitude"] + random.uniform(-0.1, 0.1), 4)
            inc_lon = round(ref_office["longitude"] + random.uniform(-0.1, 0.1), 4)
        else:
            inc_lat = round(random.uniform(29.0, 47.0), 4)
            inc_lon = round(random.uniform(-122.0, -75.0), 4)

        # Downgrade remaining standard slots to low ~30% of the time
        if priority == "standard" and random.random() < 0.3:
            priority = "low"

        claims.append({
            "claim_id": new_id(),
            "claim_number": f"CLM-{70001 + i}",
            "policy_id": policy["policy_id"],
            "policyholder_id": ph["policyholder_id"],
            "asset_id": asset["asset_id"],
            "adjuster_id": adjuster["adjuster_id"],
            "office_id": office["office_id"],
            "claim_type": ctype,
            "description": description,
            "incident_date": incident.isoformat() + "Z",
            "filed_date": filed.isoformat() + "Z",
            "status": status,
            "estimated_loss": est_loss,
            "approved_amount": approved_amount,
            "priority": priority,
            "incident_latitude": inc_lat,
            "incident_longitude": inc_lon,
        })

    return claims

# ---------------------------------------------------------------------------
# 7. Claim Events – 25 lifecycle events on claims
# ---------------------------------------------------------------------------

CLAIM_EVENT_TYPES = [
    "initial_review", "initial_review",
    "site_inspection", "site_inspection",
    "document_request",
    "estimate_prepared", "estimate_prepared",
    "payment_issued",
    "denial_issued",
    "appeal_received",
    "subrogation_filed",
]

CLAIM_EVENT_DESCRIPTIONS = {
    "initial_review":     [
        "Reviewed police report and photos submitted by policyholder",
        "Initial claim intake and documentation review completed",
        "Reviewed incident report and witness statements",
    ],
    "site_inspection":    [
        "On-site inspection of damaged property completed",
        "Vehicle inspection at approved body shop",
        "Property damage assessment conducted at insured location",
    ],
    "document_request":   [
        "Requested additional photos of damage from policyholder",
        "Requested contractor repair estimates",
        "Requested medical records for liability claim",
    ],
    "estimate_prepared":  [
        "Repair estimate prepared based on inspection findings",
        "Replacement value estimate prepared for total loss",
        "Damage assessment and cost estimate finalized",
    ],
    "payment_issued":     [
        "Payment issued to policyholder for approved claim amount",
        "Payment sent to approved repair vendor",
        "Final settlement payment processed",
    ],
    "denial_issued":      [
        "Claim denied — damage predates policy effective date",
        "Claim denied — excluded peril under policy terms",
    ],
    "appeal_received":    [
        "Policyholder appeal received with additional documentation",
        "Appeal filed with supplemental evidence from contractor",
    ],
    "subrogation_filed":  [
        "Subrogation filed against at-fault driver's insurer",
        "Subrogation initiated for manufacturer defect claim",
    ],
}

def generate_claim_events(claims, adjusters):
    events = []
    now = datetime(2026, 3, 17, 12, 0, 0)
    counter = 0

    # Early-stage steps (middle step chosen randomly per claim)
    early_stages = ["initial_review", "site_inspection", "document_request", "estimate_prepared"]

    notes_options = [
        "Damage consistent with reported incident. Proceeding to estimate.",
        "All required documentation received. Claim advancing to next stage.",
        "Additional follow-up needed with policyholder.",
        "Coordinating with third-party vendor for assessment.",
        "Adjuster notes: standard processing, no anomalies detected.",
        None,
    ]

    for claim in claims:
        adjuster = random.choice(adjusters)
        status = claim["status"]

        # Build lifecycle sequence based on claim status
        middle = random.choice(["site_inspection", "document_request"])
        if status == "paid":
            # 2 or 3 events, always ending with payment_issued
            if random.random() < 0.5:
                sequence = ["initial_review", middle, "payment_issued"]
            else:
                sequence = ["initial_review", "estimate_prepared", "payment_issued"]
        elif status == "denied":
            # 2 or 3 events, always ending with denial_issued
            if random.random() < 0.5:
                sequence = ["initial_review", middle, "denial_issued"]
            else:
                sequence = ["initial_review", "denial_issued"]
        else:
            # Open / filed / under_review / investigation / approved — early stages only
            num = random.randint(2, 3)
            sequence = ["initial_review", middle, "estimate_prepared"][:num]

        # Parse filed_date for event timing
        try:
            filed = datetime.fromisoformat(claim["filed_date"].replace("Z", ""))
        except (ValueError, AttributeError):
            filed = now - timedelta(days=30)

        # Generate one event per lifecycle step, spaced sequentially
        # Pre-compute capped filed time so all events fit before now
        max_span_hours = 48 * len(sequence)
        if filed + timedelta(hours=max_span_hours) > now:
            filed = now - timedelta(hours=max_span_hours + 1)
        step_time = filed
        for etype in sequence:
            step_time = step_time + timedelta(hours=random.randint(4, 48))

            is_completed = random.random() < 0.75
            completed = step_time + timedelta(hours=random.randint(1, 48)) if is_completed else None

            cost = None
            if etype == "payment_issued" and is_completed:
                cost = round(random.uniform(1000, 100000), 2)

            events.append({
                "claim_event_id": new_id(),
                "event_number": f"CE-{40001 + counter}",
                "claim_id": claim["claim_id"],
                "adjuster_id": adjuster["adjuster_id"],
                "event_type": etype,
                "description": random.choice(CLAIM_EVENT_DESCRIPTIONS[etype]),
                "status": "completed" if is_completed else random.choice(["pending", "cancelled"]),
                "created_at": step_time.isoformat() + "Z",
                "completed_at": completed.isoformat() + "Z" if completed else None,
                "notes": random.choice(notes_options) if is_completed else None,
                "cost_usd": cost,
            })
            counter += 1

    return events

# ---------------------------------------------------------------------------
# 8. Asset Inspections – 100 historical inspection/appraisal records
# ---------------------------------------------------------------------------

INSPECTION_TYPES = ["initial_appraisal", "annual_review", "claim_related", "underwriting"]

def generate_asset_inspections(assets, offices):
    inspections = []

    for i in range(100):
        asset = random.choice(assets)
        office = random.choice(offices)
        itype = random.choice(INSPECTION_TYPES)

        sched_date = random_date(date(2024, 6, 1), date(2026, 2, 28))
        completed = random.random() < 0.85
        comp_date = sched_date + timedelta(days=random.randint(0, 5)) if completed else None

        base_value = asset["estimated_value"]
        appraised = round(base_value * random.uniform(0.85, 1.15), 2) if completed else None

        notes_options = [
            "Property in good condition. No significant issues found.",
            "Minor wear consistent with age. Maintained well.",
            "Recommended repairs to exterior — minor cosmetic issues.",
            "Inspection completed. Value consistent with prior appraisal.",
            "Some deferred maintenance noted. Follow-up recommended in 6 months.",
            "Excellent condition. Above-average maintenance.",
        ]

        inspections.append({
            "inspection_id": new_id(),
            "asset_id": asset["asset_id"],
            "office_id": office["office_id"],
            "inspection_type": itype,
            "status": "completed" if completed else random.choice(["scheduled", "cancelled"]),
            "scheduled_date": str(sched_date),
            "completed_date": str(comp_date) if comp_date else None,
            "appraised_value": appraised,
            "inspector_notes": random.choice(notes_options) if completed else None,
            "condition_rating": random.choice(["excellent", "good", "good", "fair", "poor"]) if completed else None,
        })
    return inspections

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Generating insurance claims reference data...\n")

    # Generate in dependency order
    offices = generate_offices()
    write_jsonl("offices.jsonl", offices)

    policyholders = generate_policyholders()
    write_jsonl("policyholders.jsonl", policyholders)

    insured_assets = generate_insured_assets(policyholders)
    write_jsonl("insured_assets.jsonl", insured_assets)

    adjusters = generate_adjusters(offices)
    # NOTE: adjusters.jsonl written AFTER generate_claims so statuses reflect assignments

    policies = generate_policies(policyholders, insured_assets)
    write_jsonl("policies.jsonl", policies)

    claims = generate_claims(policies, policyholders, insured_assets, adjusters, offices)
    write_jsonl("claims.jsonl", claims)

    # Write adjusters after claims so on_assignment statuses are persisted
    write_jsonl("adjusters.jsonl", adjusters)

    claim_events = generate_claim_events(claims, adjusters)
    write_jsonl("claim_events.jsonl", claim_events)

    asset_inspections = generate_asset_inspections(insured_assets, offices)
    write_jsonl("asset_inspections.jsonl", asset_inspections)

    print(f"\nDone! All files written to: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
