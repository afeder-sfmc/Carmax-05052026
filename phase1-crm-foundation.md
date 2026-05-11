# Phase 1: Demo Persona Data — IngestAPI Bulk Ingestion

## Overview

This phase populates Salesforce with the 8 demo persona Contact records and ingests persona-specific vehicle and test drive data into Data Cloud via the **existing IngestAPI connections**. No CRM custom objects are created — Vehicle, Test Drive, and Web Engagement data lives exclusively in Data Cloud as DMOs mapped from IngestAPI data streams.

The org already has:
- ✅ 3 IngestAPI connections (Vehicle, TestDrive, WebEng) — active and connected
- ✅ 3 DLOs with data streams — active with bulk data (300 vehicles, 140 test drives, 12,700 web engagements)
- ✅ 3 custom DMOs (CarMax_Vehicle__dlm, CarMax_TestDrive__dlm) — mapped with FK relationships
- ✅ ssot__WebsiteEngagement__dlm — standard DMO with 46,400 records
- ✅ 8 demo persona Contacts — already exist in the org

**What's missing:** The existing vehicle and test drive records are linked to non-demo contacts. Jane Dawson has 0 vehicles and 0 test drives. We need to ingest **persona-specific** records via the existing IngestAPI connections so the demo data is properly linked to our 8 personas.

| Attribute | Value |
|-----------|-------|
| **Phase** | 1 of 9 |
| **Org Alias** | `carmax-sdo-mm-app-wz95pw` |
| **API Version** | 65.0 |
| **Estimated Duration** | 20–30 minutes |
| **Prerequisite** | Authenticated SF CLI session |
| **Outcome** | Demo persona-specific vehicles and test drives in Data Cloud, linked to the 8 existing contacts |

---

## Prerequisites

1. **SF CLI v2** installed and on PATH.
2. **Org authenticated:** Listed in `sf org list` with alias `carmax-sdo-mm-app-wz95pw`.
3. **curl** available (for CDP token exchange and Bulk Ingest API calls).
4. **python3** available (for JSON parsing in scripts).

---

## Phase → Demo Stop Mapping

Every record ingested in this phase directly supports one or more demo stops. If a record is missing, the corresponding stop breaks.

| Phase 1 Data | Demo Stop | Why It Matters |
|-------------|-----------|----------------|
| Jane Dawson Contact | Stops 2, 3, 4, 5 | Hero persona for waterfall, email preview, flow, and 360 |
| Aisha Thompson Contact | Stop 3 | Contrast persona for email preview comparison |
| Jane's 3 Hearted Vehicles | Stop 3 | Dynamic vehicle cards in the Data Graph repeater email |
| Jane's Test Drive (Expedition) | Stops 2, 4 | Qualifies her for Test Drive No Purchase segment (waterfall P2) |
| Jane's Web Engagements | Stops 2, 5 | Pre-Qualification Complete drives CI scoring; browsing history in 360 |
| James's 2 Hearted Trucks | Stop 2 | Additional waterfall P1 member for segment count |
| David's Purchased Vehicle | Stop 2 | Suppression logic demo — recent purchaser excluded from flow |
| Sarah's Test Drive | Stop 2 | Waterfall P2 member |
| Emily's Instant Offer Start | Stop 4 | Instant Offer Abandonment supporting flow |
| All Web Engagements | Stops 2, 5, 6 | Engagement Velocity CI, Data Cloud 360 timeline, reporting |
| All Vehicles (~20) | Stops 3, 5 | Inventory for Data Graph, 360 vehicle interaction panel |

---

## Existing Org State (Verified)

### Contacts (All 8 Exist ✅)

| Persona | Contact ID | City | Role |
|---------|-----------|------|------|
| Jane Dawson | 003ak00001QOw50AAD | Richmond, VA | HERO — Power Shopper |
| Marcus Chen | 003ak00001QQSKXAA5 | Charlotte, NC | Trade-in / Upgrade |
| Emily Foster | 003ak00001QNeTZAA1 | Richmond, VA | Instant Offer Abandonment |
| David Kim | 003ak00001QQSUDAA5 | Nashville, TN | Recent Purchaser (Suppression) |
| Priya Patel | 003ak00001QQSQzAAP | Raleigh, NC | EV Enthusiast |
| James Rodriguez | 003ak00001QQSPNAA5 | Atlanta, GA | Truck Enthusiast |
| Aisha Thompson | 003ak00001QQSSbAAP | Orlando, FL | CONTRAST — New Subscriber |
| Sarah Williams | 003ak00001QQO2UAAX | Virginia Beach, VA | Test Drive No Purchase |

### IngestAPI Connections (All 3 Active ✅)

| Connection | Label | Full Name (for bulk job sourceName) | Schema Object |
|-----------|-------|--------------------------------------|---------------|
| Vehicle | CarMax_Vehicle_Ingest | CarMax_Vehicle_Ingest | VehicleProfile |
| TestDrive | CarMax_TestDrive_Ingest | CarMax_TestDrive_Ingest | TestDriveEvent |
| WebEng | CarMax_WebEng_Ingest | CarMax_WebEng_Ingest | WebEngagementEvent |

### DLO Field Names (CamelCase — IngestAPI Convention)

**Vehicle DLO** (`CarMax_Vehicle_Stream_VehiclePr_0AB19D2B__dll`):
`VehicleId__c` (PK), `VIN__c`, `Make__c`, `Model__c`, `Year__c`, `Color__c`, `BodyType__c`, `Price__c`, `FuelType__c`, `Doors__c`, `Transmission__c`, `Mileage__c`, `Status__c`, `CarMaxStore__c`, `IndividualId__c`, `IsPurchased__c`, `IsHearted__c`, `HeartedById__c`, `HeartedDate__c`, `PurchaseDate__c`, `ListingURL__c`, `LastModified__c`

**TestDrive DLO** (`CarMax_TestDrive_Stream_TestDri_0AB23050__dll`):
`TestDriveId__c` (PK), `IndividualId__c`, `VehicleId__c`, `VIN__c`, `TestDriveDate__c`, `CarMaxStore__c`, `Outcome__c`, `ConvertedToPurchase__c`, `Notes__c`, `EventDateTime__c`

**WebEng DLO** (`CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll`):
`EngagementId__c` (PK), `IndividualId__c`, `EventType__c`, `VehicleVIN__c`, `EventDateTime__c`, `PageURL__c`, `DeviceType__c`, `SessionId__c`, `UTMSource__c`, `UTMMedium__c`, `UTMCampaign__c`

---

## Step 1: Resolve Contact IDs to Unified Individual IDs

IngestAPI data links to Data Cloud's **Unified Individual**, not Salesforce Contact IDs directly. The `IndividualId` field in the CSV must be the `ssot__Individual__dlm.ssot__Id__c` value that corresponds to each Contact.

```bash
# Query Unified Individual IDs for all 8 personas
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT ssot__Id__c, ssot__FirstName__c, ssot__LastName__c FROM ssot__Individual__dlm WHERE ssot__LastName__c IN ('"'"'Dawson'"'"','"'"'Chen'"'"','"'"'Foster'"'"','"'"'Kim'"'"','"'"'Patel'"'"','"'"'Rodriguez'"'"','"'"'Thompson'"'"','"'"'Williams'"'"') ORDER BY ssot__LastName__c"}'
```

Save the `ssot__Id__c` values. They look like `003ak00001QOw50AAD-2` or similar unified IDs. You need these for the CSV `IndividualId` column.

> **If Individual IDs match Contact IDs:** In many SDO orgs, the Unified Individual ID is derived from the Contact ID via identity resolution. If the query returns values matching the Contact IDs in the table above, use those directly.

**Store the Individual IDs in shell variables for CSV generation:**

```bash
# Replace with actual values from the query above
JANE_IND="<Jane's Individual ID>"
MARCUS_IND="<Marcus's Individual ID>"
SARAH_IND="<Sarah's Individual ID>"
JAMES_IND="<James's Individual ID>"
PRIYA_IND="<Priya's Individual ID>"
AISHA_IND="<Aisha's Individual ID>"
DAVID_IND="<David's Individual ID>"
EMILY_IND="<Emily's Individual ID>"
```

---

## Step 2: Exchange SF Token for CDP Token

The Bulk Ingest API requires a CDP token, NOT a standard Salesforce access token.

```bash
SF_TOKEN=$(sf org display --target-org carmax-sdo-mm-app-wz95pw --json 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['accessToken'])")
INSTANCE_URL=$(sf org display --target-org carmax-sdo-mm-app-wz95pw --json 2>/dev/null | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['instanceUrl'])")

CDP_RESPONSE=$(curl -s -X POST "${INSTANCE_URL}/services/a360/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:salesforce:grant-type:external:cdp" \
  -d "subject_token=${SF_TOKEN}" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:access_token")

CDP_TOKEN=$(echo "$CDP_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
CDP_INSTANCE=$(echo "$CDP_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['instance_url'])")

echo "CDP Instance: ${CDP_INSTANCE}"
echo "CDP Token acquired (length: ${#CDP_TOKEN})"
```

---

## Step 3: Generate Vehicle CSV

Create the CSV with demo persona-specific vehicles. The CSV header must use bare CamelCase field names matching the IngestAPI schema — no `__c` suffix.

```bash
cat > /tmp/carmax-vehicles.csv << 'CSVEOF'
VehicleId,VIN,Make,Model,Year,Color,BodyType,Price,FuelType,Doors,Transmission,Mileage,Status,CarMaxStore,IndividualId,IsPurchased,IsHearted,HeartedById,HeartedDate,PurchaseDate,ListingURL,LastModified
VEH-DEMO-001,1FMJU1KT4REA12345,Ford,Expedition XLT,2024,Oxford White,SUV,52990,Gas,4-Door,Automatic,8423,Available,CarMax Richmond,${JANE_IND},false,true,${JANE_IND},2026-04-15,,https://www.carmax.com/car/24680135,2026-05-01T00:00:00Z
VEH-DEMO-002,JTEBU5JR5P5123456,Toyota,4Runner SR5,2023,Magnetic Gray Metallic,SUV,39990,Gas,4-Door,Automatic,22156,Available,CarMax Richmond,${JANE_IND},false,true,${JANE_IND},2026-04-18,,https://www.carmax.com/car/24680136,2026-05-01T00:00:00Z
VEH-DEMO-003,5NMS3DAJ0RH234567,Hyundai,Santa Fe SEL,2024,Hampton Gray,SUV,34990,Hybrid,4-Door,Automatic,5890,Available,CarMax Richmond,${JANE_IND},false,true,${JANE_IND},2026-04-22,,https://www.carmax.com/car/24680137,2026-05-01T00:00:00Z
VEH-DEMO-004,1FTFW1E85PKA34567,Ford,F-150 XLT,2023,Iconic Silver,Truck,41990,Gas,4-Door,Automatic,18743,Available,CarMax Phoenix,${JAMES_IND},false,true,${JAMES_IND},2026-04-20,,https://www.carmax.com/car/24680138,2026-05-01T00:00:00Z
VEH-DEMO-005,1C6SRFFT0RN345678,RAM,1500 Big Horn,2024,Patriot Blue,Truck,44990,Gas,4-Door,Automatic,11204,Available,CarMax Phoenix,${JAMES_IND},false,true,${JAMES_IND},2026-04-25,,https://www.carmax.com/car/24680139,2026-05-01T00:00:00Z
VEH-DEMO-006,5UXTY5C09R9B56789,BMW,X3 xDrive30i,2022,Alpine White,SUV,36490,Gas,4-Door,Automatic,31245,Sold,CarMax Denver,${DAVID_IND},true,false,,,2025-11-15,https://www.carmax.com/car/24680140,2026-05-01T00:00:00Z
VEH-DEMO-007,2HKRS4H77RH456789,Honda,CR-V EX-L,2024,Radiant Red Metallic,SUV,33490,Gas,4-Door,CVT,12456,Available,CarMax Charlotte,${SARAH_IND},false,false,,,,,2026-05-01T00:00:00Z
VEH-DEMO-008,1HGCV1F34LA567890,Honda,Accord Sport,2020,Lunar Silver Metallic,Sedan,24990,Gas,4-Door,Automatic,48230,Sold,CarMax Austin,${MARCUS_IND},true,false,,,2023-03-10,https://www.carmax.com/car/24680142,2026-05-01T00:00:00Z
VEH-DEMO-009,4T1K61AK0RU678901,Toyota,Camry XSE,2024,Reservoir Blue,Sedan,31490,Gas,4-Door,Automatic,9876,Available,CarMax Austin,${MARCUS_IND},false,false,,,,https://www.carmax.com/car/24680143,2026-05-01T00:00:00Z
VEH-DEMO-010,7SAYGDEE5RF789012,Tesla,Model Y Long Range,2024,Pearl White,SUV,44990,Electric,4-Door,Automatic,6234,Available,CarMax Seattle,,false,false,,,,https://www.carmax.com/car/24680144,2026-05-01T00:00:00Z
VEH-DEMO-011,KM8KRDAF9PU890123,Hyundai,Ioniq 5 SEL,2023,Lucid Blue,SUV,36990,Electric,4-Door,Automatic,15678,Available,CarMax Seattle,,false,false,,,,https://www.carmax.com/car/24680145,2026-05-01T00:00:00Z
VEH-DEMO-012,2T3F1RFV0RW901234,Toyota,RAV4 Prime SE,2024,Blueprint,SUV,41490,Hybrid,4-Door,CVT,8901,Available,CarMax Seattle,,false,false,,,,https://www.carmax.com/car/24680146,2026-05-01T00:00:00Z
VEH-DEMO-013,JTDBBRBE5PJ012345,Toyota,Corolla LE,2023,Celestite Gray,Sedan,22490,Gas,4-Door,CVT,19345,Available,CarMax Atlanta,,false,false,,,,https://www.carmax.com/car/24680147,2026-05-01T00:00:00Z
VEH-DEMO-014,2HGFE2F56RH123456,Honda,Civic Sport,2024,Rallye Red,Sedan,25990,Gas,4-Door,CVT,7890,Available,CarMax Atlanta,,false,false,,,,https://www.carmax.com/car/24680148,2026-05-01T00:00:00Z
VEH-DEMO-015,3MZBPAEM5PM234567,Mazda,Mazda3 Select,2023,Machine Gray Metallic,Sedan,23990,Gas,4-Door,Automatic,24567,Available,CarMax Atlanta,,false,false,,,,https://www.carmax.com/car/24680149,2026-05-01T00:00:00Z
VEH-DEMO-016,5N1AT3BB8MC345678,Nissan,Rogue SV,2021,Scarlet Ember,SUV,23990,Gas,4-Door,CVT,42367,Available,CarMax Houston,${EMILY_IND},false,false,,,,https://www.carmax.com/car/24680150,2026-05-01T00:00:00Z
VEH-DEMO-017,1GNSKBKD0RR456789,Chevrolet,Tahoe LT,2024,Black,SUV,56990,Gas,4-Door,Automatic,14567,Available,CarMax Richmond,,false,false,,,,https://www.carmax.com/car/24680151,2026-05-01T00:00:00Z
VEH-DEMO-018,4S4BTACC5P3567890,Subaru,Outback Premium,2023,Autumn Green Metallic,SUV,29990,Gas,4-Door,CVT,27890,Available,CarMax Charlotte,,false,false,,,,https://www.carmax.com/car/24680152,2026-05-01T00:00:00Z
VEH-DEMO-019,5XYP5DHC0RG678901,Kia,Telluride SX,2024,Everlasting Silver,SUV,47990,Gas,4-Door,Automatic,10234,Available,CarMax Phoenix,,false,false,,,,https://www.carmax.com/car/24680153,2026-05-01T00:00:00Z
VEH-DEMO-020,1FA6P8CF5P5789012,Ford,Mustang GT,2023,Grabber Blue,Coupe,38990,Gas,2-Door,Manual,16789,Available,CarMax Houston,,false,false,,,,https://www.carmax.com/car/24680154,2026-05-01T00:00:00Z
CSVEOF

echo "Vehicle CSV created: $(wc -l < /tmp/carmax-vehicles.csv) lines (header + 20 data rows)"
```

> **Note on shell variable expansion:** The `${JANE_IND}`, `${JAMES_IND}` etc. placeholders in the heredoc above will be expanded by the shell if the variables from Step 1 are set. If using a `'CSVEOF'` (single-quoted) delimiter, the variables will NOT expand — use a script to substitute them or switch to unquoted `CSVEOF`.

### Vehicle Data Summary

| Persona | Vehicle | Key Attributes |
|---------|---------|---------------|
| **Jane Dawson** | 2024 Ford Expedition XLT ($52,990) | ❤️ Hearted + Test Driven |
| **Jane Dawson** | 2023 Toyota 4Runner SR5 ($39,990) | ❤️ Hearted |
| **Jane Dawson** | 2024 Hyundai Santa Fe SEL ($34,990) | ❤️ Hearted |
| **James Rodriguez** | 2023 Ford F-150 XLT ($41,990) | ❤️ Hearted |
| **James Rodriguez** | 2024 RAM 1500 Big Horn ($44,990) | ❤️ Hearted |
| **David Kim** | 2022 BMW X3 xDrive30i ($36,490) | 🛒 Purchased 2025-11-15 |
| **Sarah Williams** | 2024 Honda CR-V EX-L ($33,490) | Test drive vehicle |
| **Marcus Chen** | 2020 Honda Accord Sport ($24,990) | 🛒 Purchased (trade-in candidate) |
| **Marcus Chen** | 2024 Toyota Camry XSE ($31,490) | Browsing upgrade |
| Priya Patel (browsed) | Tesla Model Y, Ioniq 5, RAV4 Prime | EV/Hybrid browsed |
| Aisha Thompson (viewed) | Corolla, Civic, Mazda3 | Sedans — unowned inventory |
| Emily Foster | 2021 Nissan Rogue SV ($23,990) | Instant offer trade-in |
| (Inventory) | Tahoe, Outback, Telluride, Mustang | Unowned inventory filler |

---

## Step 4: Ingest Vehicle CSV via Bulk API

### 4A. Create Bulk Job

```bash
VEH_JOB=$(curl -s -X POST "https://${CDP_INSTANCE}/api/v1/ingest/jobs" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "VehicleProfile",
    "sourceName": "CarMax_Vehicle_Ingest",
    "operation": "upsert"
  }')

VEH_JOB_ID=$(echo "$VEH_JOB" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
echo "Vehicle Job ID: ${VEH_JOB_ID}"
```

> **Important:** `object` is the schema name (`VehicleProfile`), not the DLO name. `sourceName` is the connection **label** (`CarMax_Vehicle_Ingest`), not the full UUID name.

### 4B. Upload CSV

```bash
curl -s -w "\nHTTP:%{http_code}" -X PUT \
  "https://${CDP_INSTANCE}/api/v1/ingest/jobs/${VEH_JOB_ID}/batches" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: text/csv" \
  --data-binary @/tmp/carmax-vehicles.csv
```

**Expected:** HTTP 202 with `{"accepted":true}`

### 4C. Close Job

```bash
curl -s -X PATCH "https://${CDP_INSTANCE}/api/v1/ingest/jobs/${VEH_JOB_ID}" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"state": "UploadComplete"}'
```

---

## Step 5: Generate Test Drive CSV

```bash
cat > /tmp/carmax-testdrives.csv << 'CSVEOF'
TestDriveId,IndividualId,VehicleId,VIN,TestDriveDate,CarMaxStore,Outcome,ConvertedToPurchase,Notes,EventDateTime
TD-DEMO-001,${JANE_IND},VEH-DEMO-001,1FMJU1KT4REA12345,2026-04-28,CarMax Richmond,Completed,false,Loved the space and towing capacity. Wants to compare with 4Runner before deciding.,2026-04-28T14:00:00Z
TD-DEMO-002,${SARAH_IND},VEH-DEMO-007,2HKRS4H77RH456789,2026-04-22,CarMax Charlotte,Completed,false,Good drive but wants to explore more options. Still comparing with Outback.,2026-04-22T11:00:00Z
TD-DEMO-003,${DAVID_IND},VEH-DEMO-006,5UXTY5C09R9B56789,2025-11-12,CarMax Denver,Completed,true,Great experience. Customer purchased same day.,2025-11-12T15:00:00Z
TD-DEMO-004,${MARCUS_IND},VEH-DEMO-009,4T1K61AK0RU678901,2026-05-15,CarMax Austin,Scheduled,false,Upcoming test drive. Interested in trading in current Accord.,2026-05-15T10:00:00Z
CSVEOF

echo "Test Drive CSV created: $(wc -l < /tmp/carmax-testdrives.csv) lines (header + 4 data rows)"
```

### Test Drive Data Summary

| Persona | Vehicle Tested | Outcome | Demo Purpose |
|---------|---------------|---------|--------------|
| **Jane Dawson** | Ford Expedition XLT | Completed, not converted | Waterfall P2 qualification |
| **Sarah Williams** | Honda CR-V EX-L | Completed, not converted | Waterfall P2 member |
| **David Kim** | BMW X3 xDrive30i | Completed, converted to purchase | Suppression — recent buyer |
| **Marcus Chen** | Toyota Camry XSE | Scheduled (upcoming) | Active prospect, not suppressed |

---

## Step 6: Ingest Test Drive CSV via Bulk API

### 6A. Create Bulk Job

```bash
TD_JOB=$(curl -s -X POST "https://${CDP_INSTANCE}/api/v1/ingest/jobs" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "TestDriveEvent",
    "sourceName": "CarMax_TestDrive_Ingest",
    "operation": "upsert"
  }')

TD_JOB_ID=$(echo "$TD_JOB" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
echo "Test Drive Job ID: ${TD_JOB_ID}"
```

### 6B. Upload CSV

```bash
curl -s -w "\nHTTP:%{http_code}" -X PUT \
  "https://${CDP_INSTANCE}/api/v1/ingest/jobs/${TD_JOB_ID}/batches" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: text/csv" \
  --data-binary @/tmp/carmax-testdrives.csv
```

### 6C. Close Job

```bash
curl -s -X PATCH "https://${CDP_INSTANCE}/api/v1/ingest/jobs/${TD_JOB_ID}" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"state": "UploadComplete"}'
```

---

## Step 7: Generate & Ingest Web Engagement CSV

The WebEng DLO already has 12,700 records with 184-226 events per demo persona. However, we need to verify these events have the correct event types for our demo scenarios. If they do, skip this step. If not, ingest additional persona-specific events.

### 7A. Check Existing Web Engagement Data for Demo Personas

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT IndividualId__c, EventType__c, COUNT(*) AS cnt FROM CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll GROUP BY IndividualId__c, EventType__c ORDER BY IndividualId__c, cnt DESC"}'
```

If the existing data already includes the required event types (Heart Vehicle, Pre-Qualification Complete, Schedule Test Drive, Instant Offer Start, etc.) for the correct personas, **skip the web engagement ingestion** — the existing 12,700 records are sufficient.

### 7B. Generate Web Engagement CSV (If Needed)

Only generate this CSV if Step 7A shows missing event types for demo personas:

```bash
cat > /tmp/carmax-webengagements.csv << 'CSVEOF'
EngagementId,IndividualId,EventType,VehicleVIN,EventDateTime,PageURL,DeviceType,SessionId,UTMSource,UTMMedium,UTMCampaign
WE-DEMO-001,${JANE_IND},Vehicle Detail View,1FMJU1KT4REA12345,2026-04-12T10:23:00Z,https://www.carmax.com/car/24680135,Desktop,sess-jd-001,google,cpc,suv-spring-2026
WE-DEMO-002,${JANE_IND},Vehicle Detail View,JTEBU5JR5P5123456,2026-04-12T10:31:00Z,https://www.carmax.com/car/24680136,Desktop,sess-jd-001,google,cpc,suv-spring-2026
WE-DEMO-003,${JANE_IND},Heart Vehicle,1FMJU1KT4REA12345,2026-04-15T14:05:00Z,https://www.carmax.com/car/24680135,Mobile,sess-jd-002,,,
WE-DEMO-004,${JANE_IND},Heart Vehicle,JTEBU5JR5P5123456,2026-04-18T09:12:00Z,https://www.carmax.com/car/24680136,Mobile,sess-jd-003,,,
WE-DEMO-005,${JANE_IND},Vehicle Detail View,5NMS3DAJ0RH234567,2026-04-20T19:45:00Z,https://www.carmax.com/car/24680137,Desktop,sess-jd-004,,,
WE-DEMO-006,${JANE_IND},Heart Vehicle,5NMS3DAJ0RH234567,2026-04-22T11:30:00Z,https://www.carmax.com/car/24680137,Mobile,sess-jd-005,,,
WE-DEMO-007,${JANE_IND},Vehicle Detail View,1GNSKBKD0RR456789,2026-04-23T16:00:00Z,https://www.carmax.com/car/24680151,Desktop,sess-jd-006,,,
WE-DEMO-008,${JANE_IND},Vehicle Detail View,5XYP5DHC0RG678901,2026-04-23T16:14:00Z,https://www.carmax.com/car/24680153,Desktop,sess-jd-006,,,
WE-DEMO-009,${JANE_IND},Pre-Qualification Complete,,2026-04-25T13:22:00Z,https://www.carmax.com/pre-qualification/complete,Desktop,sess-jd-007,,,
WE-DEMO-010,${JANE_IND},Schedule Test Drive,1FMJU1KT4REA12345,2026-04-26T10:45:00Z,https://www.carmax.com/car/24680135/schedule-test-drive,Desktop,sess-jd-008,,,
WE-DEMO-011,${MARCUS_IND},Vehicle Detail View,4T1K61AK0RU678901,2026-04-18T20:15:00Z,https://www.carmax.com/car/24680143,Mobile,sess-mc-001,,,
WE-DEMO-012,${MARCUS_IND},Vehicle Detail View,2HGFE2F56RH123456,2026-04-18T20:28:00Z,https://www.carmax.com/car/24680148,Mobile,sess-mc-001,,,
WE-DEMO-013,${MARCUS_IND},Vehicle Detail View,4T1K61AK0RU678901,2026-04-25T12:30:00Z,https://www.carmax.com/car/24680143,Desktop,sess-mc-002,,,
WE-DEMO-014,${MARCUS_IND},Instant Offer Start,1HGCV1F34LA567890,2026-04-28T09:45:00Z,https://www.carmax.com/sell-my-car/instant-offer,Desktop,sess-mc-003,email,crm,trade-in-spring
WE-DEMO-015,${SARAH_IND},Vehicle Detail View,2HKRS4H77RH456789,2026-04-10T15:00:00Z,https://www.carmax.com/car/24680141,Desktop,sess-sw-001,,,
WE-DEMO-016,${SARAH_IND},Vehicle Detail View,4S4BTACC5P3567890,2026-04-10T15:18:00Z,https://www.carmax.com/car/24680152,Desktop,sess-sw-001,,,
WE-DEMO-017,${SARAH_IND},Vehicle Detail View,2HKRS4H77RH456789,2026-04-14T11:30:00Z,https://www.carmax.com/car/24680141,Mobile,sess-sw-002,,,
WE-DEMO-018,${SARAH_IND},Pre-Qualification Start,,2026-04-16T09:00:00Z,https://www.carmax.com/pre-qualification/start,Desktop,sess-sw-003,,,
WE-DEMO-019,${SARAH_IND},Pre-Qualification Complete,,2026-04-16T09:15:00Z,https://www.carmax.com/pre-qualification/complete,Desktop,sess-sw-003,,,
WE-DEMO-020,${SARAH_IND},Schedule Test Drive,2HKRS4H77RH456789,2026-04-18T14:30:00Z,https://www.carmax.com/car/24680141/schedule-test-drive,Desktop,sess-sw-004,,,
WE-DEMO-021,${JAMES_IND},Vehicle Detail View,1FTFW1E85PKA34567,2026-04-14T18:30:00Z,https://www.carmax.com/car/24680138,Mobile,sess-jr-001,,,
WE-DEMO-022,${JAMES_IND},Vehicle Detail View,1C6SRFFT0RN345678,2026-04-14T18:45:00Z,https://www.carmax.com/car/24680139,Mobile,sess-jr-001,,,
WE-DEMO-023,${JAMES_IND},Heart Vehicle,1FTFW1E85PKA34567,2026-04-20T10:00:00Z,https://www.carmax.com/car/24680138,Desktop,sess-jr-002,,,
WE-DEMO-024,${JAMES_IND},Vehicle Detail View,1FTFW1E85PKA34567,2026-04-22T20:00:00Z,https://www.carmax.com/car/24680138,Mobile,sess-jr-003,,,
WE-DEMO-025,${JAMES_IND},Heart Vehicle,1C6SRFFT0RN345678,2026-04-25T12:15:00Z,https://www.carmax.com/car/24680139,Desktop,sess-jr-004,,,
WE-DEMO-026,${JAMES_IND},Vehicle Detail View,5XYP5DHC0RG678901,2026-04-27T17:30:00Z,https://www.carmax.com/car/24680153,Mobile,sess-jr-005,,,
WE-DEMO-027,${JAMES_IND},Save Search,,2026-04-28T09:00:00Z,https://www.carmax.com/cars/trucks?price=0-50000&location=phoenix,Desktop,sess-jr-006,,,
WE-DEMO-028,${PRIYA_IND},Vehicle Detail View,7SAYGDEE5RF789012,2026-04-15T11:00:00Z,https://www.carmax.com/car/24680144,Desktop,sess-pp-001,google,organic,
WE-DEMO-029,${PRIYA_IND},Vehicle Detail View,KM8KRDAF9PU890123,2026-04-15T11:20:00Z,https://www.carmax.com/car/24680145,Desktop,sess-pp-001,,,
WE-DEMO-030,${PRIYA_IND},Vehicle Detail View,2T3F1RFV0RW901234,2026-04-20T14:30:00Z,https://www.carmax.com/car/24680146,Mobile,sess-pp-002,,,
WE-DEMO-031,${PRIYA_IND},Vehicle Detail View,7SAYGDEE5RF789012,2026-04-26T19:00:00Z,https://www.carmax.com/car/24680144,Mobile,sess-pp-003,,,
WE-DEMO-032,${PRIYA_IND},Save Search,,2026-04-28T10:00:00Z,https://www.carmax.com/cars/suv?fuel=electric%2Chybrid&location=seattle,Desktop,sess-pp-004,,,
WE-DEMO-033,${AISHA_IND},Email Signup,,2026-04-22T16:00:00Z,https://www.carmax.com/email-signup,Mobile,sess-at-001,instagram,social,spring-deals
WE-DEMO-034,${AISHA_IND},Vehicle Detail View,JTDBBRBE5PJ012345,2026-04-24T12:30:00Z,https://www.carmax.com/car/24680147,Mobile,sess-at-002,,,
WE-DEMO-035,${AISHA_IND},Vehicle Detail View,2HGFE2F56RH123456,2026-04-24T12:42:00Z,https://www.carmax.com/car/24680148,Mobile,sess-at-002,,,
WE-DEMO-036,${AISHA_IND},Vehicle Detail View,3MZBPAEM5PM234567,2026-04-26T18:15:00Z,https://www.carmax.com/car/24680149,Mobile,sess-at-003,,,
WE-DEMO-037,${DAVID_IND},Vehicle Detail View,5XYP5DHC0RG678901,2026-04-20T10:00:00Z,https://www.carmax.com/car/24680153,Desktop,sess-dk-001,,,
WE-DEMO-038,${DAVID_IND},Vehicle Detail View,1GNSKBKD0RR456789,2026-04-25T14:30:00Z,https://www.carmax.com/car/24680151,Desktop,sess-dk-002,,,
WE-DEMO-039,${DAVID_IND},Vehicle Detail View,1FMJU1KT4REA12345,2026-04-28T11:00:00Z,https://www.carmax.com/car/24680135,Desktop,sess-dk-003,,,
WE-DEMO-040,${DAVID_IND},Finance Application,,2026-05-01T09:30:00Z,https://www.carmax.com/finance/apply,Desktop,sess-dk-004,,,
WE-DEMO-041,${EMILY_IND},Vehicle Detail View,5N1AT3BB8MC345678,2026-04-22T15:00:00Z,https://www.carmax.com/car/24680150,Mobile,sess-ef-001,,,
WE-DEMO-042,${EMILY_IND},Vehicle Detail View,1FA6P8CF5P5789012,2026-04-22T15:12:00Z,https://www.carmax.com/car/24680154,Mobile,sess-ef-001,,,
WE-DEMO-043,${EMILY_IND},Instant Offer Start,5N1AT3BB8MC345678,2026-04-26T11:00:00Z,https://www.carmax.com/sell-my-car/instant-offer,Desktop,sess-ef-002,,,
CSVEOF

echo "Web Engagement CSV created: $(wc -l < /tmp/carmax-webengagements.csv) lines (header + 43 data rows)"
```

### Web Engagement Data Summary

| Persona | Events | Key Event Types |
|---------|--------|----------------|
| Jane Dawson | 10 | 3× Heart Vehicle, Pre-Qual Complete, Schedule Test Drive |
| Marcus Chen | 4 | Instant Offer Start (for trade-in) |
| Sarah Williams | 6 | Pre-Qual Start + Complete, Schedule Test Drive |
| James Rodriguez | 7 | 2× Heart Vehicle, Save Search |
| Priya Patel | 5 | EV browsing, Save Search |
| Aisha Thompson | 4 | Email Signup only, light browsing (contrast persona) |
| David Kim | 4 | Browsing after recent purchase, Finance Application |
| Emily Foster | 3 | Instant Offer Start (abandoned — no Complete) |

### 7C. Ingest Web Engagement CSV

```bash
# Create bulk job
WE_JOB=$(curl -s -X POST "https://${CDP_INSTANCE}/api/v1/ingest/jobs" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "WebEngagementEvent",
    "sourceName": "CarMax_WebEng_Ingest",
    "operation": "upsert"
  }')

WE_JOB_ID=$(echo "$WE_JOB" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
echo "WebEng Job ID: ${WE_JOB_ID}"

# Upload CSV
curl -s -w "\nHTTP:%{http_code}" -X PUT \
  "https://${CDP_INSTANCE}/api/v1/ingest/jobs/${WE_JOB_ID}/batches" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: text/csv" \
  --data-binary @/tmp/carmax-webengagements.csv

# Close job
curl -s -X PATCH "https://${CDP_INSTANCE}/api/v1/ingest/jobs/${WE_JOB_ID}" \
  -H "Authorization: Bearer ${CDP_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"state": "UploadComplete"}'
```

---

## Step 8: Verification (Wait ~3 Minutes for Propagation)

After closing all bulk jobs, wait approximately 3 minutes for data to propagate through DLO → DMO mapping.

### 8A. Verify Vehicle Data in DMO

```bash
# Total vehicle count (should include existing 300 + 20 new demo)
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT COUNT(*) AS cnt FROM CarMax_Vehicle__dlm"}'
```

**Expected:** ~320 total (300 existing + 20 demo)

### 8B. Verify Jane's Hearted Vehicles (Critical — Drives Dynamic Email)

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT Make__c, Model__c, Price__c, Color__c, VIN__c, IsHearted__c FROM CarMax_Vehicle__dlm WHERE IsHearted__c = '"'"'true'"'"' AND IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"'"}'
```

**Expected:** 3 rows — Ford Expedition XLT ($52,990), Toyota 4Runner SR5 ($39,990), Hyundai Santa Fe SEL ($34,990)

### 8C. Verify Test Drive Data

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT TestDriveId__c, IndividualId__c, VIN__c, Outcome__c, ConvertedToPurchase__c FROM CarMax_TestDrive__dlm WHERE TestDriveId__c LIKE '"'"'TD-DEMO%'"'"'"}'
```

**Expected:** 4 rows — Jane (Completed/false), Sarah (Completed/false), David (Completed/true), Marcus (Scheduled/false)

### 8D. Verify Web Engagement Data (If Ingested)

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT COUNT(*) AS cnt FROM CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll WHERE EngagementId__c LIKE '"'"'WE-DEMO%'"'"'"}'
```

**Expected:** 43 rows (if web engagement CSV was ingested)

### 8E. Purchased Vehicle Count

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT COUNT(*) AS cnt FROM CarMax_Vehicle__dlm WHERE IsPurchased__c = '"'"'true'"'"' AND VehicleId__c LIKE '"'"'VEH-DEMO%'"'"'"}'
```

**Expected:** 2 (David's BMW X3 + Marcus's Honda Accord)

---

## Gotchas & Critical Notes

### IngestAPI Bulk Ingestion

1. **CDP Token expires.** The token from Step 2 expires after ~1 hour. If Step 4-7 take longer, re-run Step 2 to get a fresh token.
2. **CSV headers are bare CamelCase.** Use `VehicleId` not `VehicleId__c`. The `__c` suffix is only in the DLO/DMO — the IngestAPI schema uses bare names.
3. **Boolean fields in CSV use string `true`/`false`.** Not `1`/`0` or `TRUE`/`FALSE`.
4. **Empty fields in CSV.** Leave the field blank (two consecutive commas). Do NOT use `null` or `NULL`.
5. **`sourceName` is the connection LABEL**, not the full UUID name. Use `CarMax_Vehicle_Ingest`, not `CarMax_Vehicle_Ingest_0185a0a9_...`.
6. **`object` is the schema name**, not the DLO or DMO name. Use `VehicleProfile`, not `CarMax_Vehicle__dlm`.
7. **Upsert mode is idempotent.** If you need to re-run, the same VehicleId/TestDriveId/EngagementId will be updated, not duplicated.

### Data Integrity

8. **Jane's 3 hearted vehicles are the most critical records.** These render as dynamic vehicle cards in the flagship email (Stop 3). Verify with query 8B after ingestion.
9. **David Kim's purchase date (2025-11-15) is intentionally 6 months old.** This puts him inside the "recent purchaser" suppression window for the MCA Flow (Stop 4).
10. **Aisha Thompson has NO vehicles linked to her IndividualId.** She only has web engagement events pointing to unowned inventory VINs. Her email preview at Stop 3 must show the fallback "Browse Our Top Picks" section.
11. **Emily Foster has only an Instant Offer Start, no Instant Offer Complete.** The gap qualifies her for the Instant Offer Abandonment flow (Stop 4).

### Existing Data Coexistence

12. **Demo records coexist with existing bulk data.** The 300 existing vehicles and 140 test drives remain untouched. Demo-specific records use `VEH-DEMO-*` and `TD-DEMO-*` IDs for easy identification.
13. **Web engagement records use `WE-DEMO-*` IDs.** This allows querying only demo events while keeping the existing 12,700 records.

---

## Record Summary

| Data Entity | New Demo Records | Existing Records | Total After |
|-------------|-----------------|-----------------|-------------|
| Contact (CRM) | 0 (already exist) | 8 | 8 |
| Vehicle (Data Cloud) | 20 | 300 | ~320 |
| Test Drive (Data Cloud) | 4 | 140 | ~144 |
| Web Engagement (Data Cloud) | 43 (if needed) | 12,700 | ~12,743 |

---

## What Comes Next

This phase produces the demo persona-specific data in Data Cloud. The subsequent phases consume it:

| Next Phase | Consumes | Purpose |
|------------|----------|---------|
| **Phase 2: Data Cloud Config** | Verify DMOs, mappings, FKs, WebEng mapping | Confirm infrastructure is correct |
| **Phase 3: Calculated Insights** | Vehicle + TestDrive + WebEng DMO data | CI scoring for CLV, Propensity, Velocity |
| **Phase 4: Data Graph** | DMO FK relationships | Data Graph for dynamic email repeater |
| **Phase 5: Segments** | DMOs + CIs | Waterfall prioritization + SQL segments |
