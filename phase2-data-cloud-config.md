# Phase 2: Data Cloud Configuration — Verification & WebEng Mapping

## Overview

This phase verifies the existing Data Cloud infrastructure and addresses the one known gap: the CarMax WebEng DLO is **not yet mapped** to `ssot__WebsiteEngagement__dlm`. All other infrastructure (IngestAPI connections, DLOs, DMOs for Vehicle and TestDrive, FK relationships, identity resolution) is already in place and working.

**What's already done (Do NOT recreate):**
- ✅ 3 IngestAPI connections (Vehicle, TestDrive, WebEng) — active and connected
- ✅ Vehicle DLO → CarMax_Vehicle__dlm DMO — mapped with FK to Individual
- ✅ TestDrive DLO → CarMax_TestDrive__dlm DMO — mapped with FK to Individual + Vehicle
- ✅ CRM Connector active — ingesting Account, Contact, Campaign, Lead, Opportunity
- ✅ Identity Resolution — Contacts resolve to Unified Individuals
- ✅ Standard DMOs — Individual (1,021), Contact Point Email (1,021), Account (92)

**What needs to be done:**
- 🔧 Map CarMax WebEng DLO → `ssot__WebsiteEngagement__dlm` (standard WebsiteEngagement DMO)
- 🔍 Verify all FK relationships are correct
- 🔍 Verify DMO data propagation from Phase 1 ingestion

| Attribute | Value |
|-----------|-------|
| **Phase** | 2 of 9 |
| **Org Alias** | `carmax-sdo-mm-app-wz95pw` |
| **API Version** | 65.0 |
| **Estimated Duration** | 15–20 minutes |
| **Prerequisite** | Phase 1 complete (demo persona data ingested) |
| **Outcome** | All 3 data entities mapped and verified, WebEng flowing to standard DMO |

---

## Existing Infrastructure Reference

### IngestAPI Connections

| Connection | ID | Label | Status | DLO |
|-----------|-----|-------|--------|-----|
| Vehicle | 1WMak0000002vwfGAA | CarMax_Vehicle_Ingest | CONNECTED | CarMax_Vehicle_Stream_VehiclePr_0AB19D2B__dll |
| TestDrive | 1WMak0000002vyHGAQ | CarMax_TestDrive_Ingest | CONNECTED | CarMax_TestDrive_Stream_TestDri_0AB23050__dll |
| WebEng | 1WMak0000002vztGAA | CarMax_WebEng_Ingest | CONNECTED | CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll |

### DMOs

| DMO | Dev Name | Category | Records | FK to Individual |
|-----|----------|----------|---------|-----------------|
| CarMax Vehicle | CarMax_Vehicle__dlm | Profile | ~320 | ✅ IndividualId → Individual.Id |
| CarMax TestDrive | CarMax_TestDrive__dlm | Engagement | ~144 | ✅ IndividualId → Individual.Id |
| Website Engagement | ssot__WebsiteEngagement__dlm | Engagement | 46,400 | ✅ ssot__IndividualId__c → Individual.Id |

### DLO-to-DMO Mapping Status

| DLO | Target DMO | Mapping Status |
|-----|-----------|---------------|
| CarMax_Vehicle_Stream_VehiclePr_0AB19D2B__dll | CarMax_Vehicle__dlm | ✅ Mapped |
| CarMax_TestDrive_Stream_TestDri_0AB23050__dll | CarMax_TestDrive__dlm | ✅ Mapped |
| CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll | ssot__WebsiteEngagement__dlm | ❌ **NOT MAPPED** |

---

## Step 1: Map CarMax WebEng DLO → ssot__WebsiteEngagement__dlm

The CarMax WebEng DLO has 12,700+ records but they are NOT flowing to any DMO. We need to create the field mapping from the DLO to the standard `ssot__WebsiteEngagement__dlm` DMO.

### 1A. Review Field Mapping Table

The CarMax WebEng DLO uses CamelCase IngestAPI names. The standard WebsiteEngagement DMO uses `ssot__` prefixed names. Here's the mapping:

| WebEng DLO Field | ssot__WebsiteEngagement__dlm Field | Notes |
|-------------------|-----------------------------------|-------|
| EngagementId__c | ssot__Id__c | Primary key |
| IndividualId__c | ssot__IndividualId__c | FK to Individual |
| EventType__c | ssot__EngagementChannelActionId__c | Event type identifier |
| VehicleVIN__c | ssot__EngagementVehicleId__c | Vehicle reference |
| EventDateTime__c | ssot__EngagementDateTm__c | Event timestamp |
| PageURL__c | ssot__PageURL__c | Page URL |
| DeviceType__c | ssot__DeviceTypeTxt__c | Device type |
| SessionId__c | ssot__SessionId__c | Session grouping |
| UTMSource__c | ssot__UtmSourceName__c | UTM source |
| UTMMedium__c | ssot__UtmMediumName__c | UTM medium |
| UTMCampaign__c | ssot__UtmCampaignName__c | UTM campaign |

### 1B. Create the DLO → DMO Mapping

```bash
sf api request rest '/services/data/v65.0/ssot/data-model-object-mappings' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{
    "sourceEntityDeveloperName": "CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll",
    "targetEntityDeveloperName": "ssot__WebsiteEngagement__dlm",
    "fieldMapping": [
      {"sourceFieldDeveloperName": "EngagementId__c", "targetFieldDeveloperName": "ssot__Id__c"},
      {"sourceFieldDeveloperName": "IndividualId__c", "targetFieldDeveloperName": "ssot__IndividualId__c"},
      {"sourceFieldDeveloperName": "EventType__c", "targetFieldDeveloperName": "ssot__EngagementChannelActionId__c"},
      {"sourceFieldDeveloperName": "VehicleVIN__c", "targetFieldDeveloperName": "ssot__EngagementVehicleId__c"},
      {"sourceFieldDeveloperName": "EventDateTime__c", "targetFieldDeveloperName": "ssot__EngagementDateTm__c"},
      {"sourceFieldDeveloperName": "PageURL__c", "targetFieldDeveloperName": "ssot__PageURL__c"},
      {"sourceFieldDeveloperName": "DeviceType__c", "targetFieldDeveloperName": "ssot__DeviceTypeTxt__c"},
      {"sourceFieldDeveloperName": "SessionId__c", "targetFieldDeveloperName": "ssot__SessionId__c"},
      {"sourceFieldDeveloperName": "UTMSource__c", "targetFieldDeveloperName": "ssot__UtmSourceName__c"},
      {"sourceFieldDeveloperName": "UTMMedium__c", "targetFieldDeveloperName": "ssot__UtmMediumName__c"},
      {"sourceFieldDeveloperName": "UTMCampaign__c", "targetFieldDeveloperName": "ssot__UtmCampaignName__c"}
    ]
  }'
```

### 1C. Verify Mapping Was Created

```bash
sf api request rest '/services/data/v65.0/ssot/data-model-object-mappings?sourceObjectName=CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll' \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** Response should show `objectSourceTargetMaps` with 11 field mappings (not empty `[]`).

### 1D. Wait for Data Propagation (~3-5 minutes)

After the mapping is created, Data Cloud will begin propagating the 12,700+ WebEng DLO records into `ssot__WebsiteEngagement__dlm`. This takes a few minutes.

```bash
# Check if CarMax WebEng records are now in the DMO
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT COUNT(*) AS cnt FROM ssot__WebsiteEngagement__dlm WHERE ssot__DataSourceId__c LIKE '"'"'CarMax%'"'"'"}'
```

**Expected:** Count should grow from 0 toward ~12,700+ as propagation completes.

---

## Step 2: Verify Vehicle DMO Data & FK

### 2A. Vehicle Record Count

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT COUNT(*) AS cnt FROM CarMax_Vehicle__dlm"}'
```

**Expected:** ~320 (300 existing + 20 demo from Phase 1)

### 2B. Vehicle FK to Individual

```bash
# Verify FK relationship exists
sf api request rest "/services/data/v65.0/tooling/query/?q=SELECT+Id,DeveloperName,RefAttrDeveloperName,IsDynamicLookup+FROM+MktDataModelField+WHERE+MktDataModelObjectId+IN+(SELECT+Id+FROM+MktDataModelObject+WHERE+DeveloperName='CarMax_Vehicle')+AND+IsDynamicLookup=true" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** `IndividualId` field with `RefAttrDeveloperName: "Id"` and `IsDynamicLookup: true`

### 2C. Jane's Hearted Vehicles Verification

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT Make__c, Model__c, Price__c, IsHearted__c FROM CarMax_Vehicle__dlm WHERE VehicleId__c LIKE '"'"'VEH-DEMO%'"'"' AND IsHearted__c = '"'"'true'"'"'"}'
```

**Expected:** 5 rows (3 Jane SUVs + 2 James trucks)

---

## Step 3: Verify TestDrive DMO Data & FKs

### 3A. TestDrive Record Count

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT COUNT(*) AS cnt FROM CarMax_TestDrive__dlm"}'
```

**Expected:** ~144 (140 existing + 4 demo from Phase 1)

### 3B. TestDrive FKs (Individual + Vehicle)

```bash
# Check FK relationships
sf api request rest "/services/data/v65.0/tooling/query/?q=SELECT+Id,DeveloperName,RefAttrDeveloperName,IsDynamicLookup+FROM+MktDataModelField+WHERE+MktDataModelObjectId+IN+(SELECT+Id+FROM+MktDataModelObject+WHERE+DeveloperName='CarMax_TestDrive')+AND+IsDynamicLookup=true" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** Two FK fields:
- `IndividualId` → Individual.Id
- `VehicleId` → Vehicle.VehicleId (or VIN)

---

## Step 4: Verify Identity Resolution

Confirm that the demo persona Contacts resolve to Unified Individuals, which is required for the FK relationships to work.

```bash
sf api request rest '/services/data/v65.0/ssot/queryv2' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql": "SELECT ssot__Id__c, ssot__FirstName__c, ssot__LastName__c FROM ssot__Individual__dlm WHERE ssot__LastName__c IN ('"'"'Dawson'"'"','"'"'Chen'"'"','"'"'Foster'"'"','"'"'Kim'"'"','"'"'Patel'"'"','"'"'Rodriguez'"'"','"'"'Thompson'"'"','"'"'Williams'"'"') ORDER BY ssot__LastName__c"}'
```

**Expected:** 8 rows, one per demo persona. The `ssot__Id__c` values should match the IndividualId values used in the Phase 1 CSV ingestion.

---

## Step 5: WebEng DLO Mapping Decision Point

> **IMPORTANT:** The mapping in Step 1 maps CarMax WebEng DLO fields to standard `ssot__WebsiteEngagement__dlm` fields. This means subsequent phases (CIs, Segments, Data Graph) should reference `ssot__WebsiteEngagement__dlm` with `ssot__` prefixed field names for web engagement data, NOT a custom CarMax_WebEngagement DMO.

### Field Name Reference for Downstream Phases

When writing Calculated Insights SQL, Segment criteria, or Data Graph queries against web engagement data, use these field names:

| Business Concept | DMO Field Name | DLO Field Name |
|-----------------|---------------|----------------|
| Record ID | ssot__Id__c | EngagementId__c |
| Individual Link | ssot__IndividualId__c | IndividualId__c |
| Event Type | ssot__EngagementChannelActionId__c | EventType__c |
| Vehicle VIN | ssot__EngagementVehicleId__c | VehicleVIN__c |
| Event Timestamp | ssot__EngagementDateTm__c | EventDateTime__c |
| Page URL | ssot__PageURL__c | PageURL__c |
| Device Type | ssot__DeviceTypeTxt__c | DeviceType__c |
| Session ID | ssot__SessionId__c | SessionId__c |
| UTM Source | ssot__UtmSourceName__c | UTMSource__c |
| UTM Medium | ssot__UtmMediumName__c | UTMMedium__c |
| UTM Campaign | ssot__UtmCampaignName__c | UTMCampaign__c |

---

## Critical Notes & Gotchas

1. **Do NOT create a custom CarMax_WebEngagement DMO.** The standard `ssot__WebsiteEngagement__dlm` already exists with 46,400 records from other sources. Mapping the CarMax WebEng DLO to it adds our data without creating unnecessary custom infrastructure.

2. **Field name conventions differ between DMOs:**
   - CarMax Vehicle DMO: CamelCase (`IsHearted__c`, `BodyType__c`, `FuelType__c`)
   - CarMax TestDrive DMO: CamelCase (`ConvertedToPurchase__c`, `TestDriveDate__c`)
   - WebsiteEngagement DMO: ssot__ prefix (`ssot__EngagementChannelActionId__c`, `ssot__EngagementDateTm__c`)

3. **FK relationships via Tooling API** use `RefAttrDeveloperName` (bare name without `__c`) and `IsDynamicLookup: true`. These are already established for Vehicle and TestDrive. If the WebsiteEngagement FK to Individual needs to be created, use the same Tooling API pattern.

4. **Data propagation after mapping creation** takes 3-5 minutes. The 12,700 WebEng DLO records will flow into `ssot__WebsiteEngagement__dlm` incrementally. Subsequent data ingested via the CarMax WebEng IngestAPI connection will also flow through.

5. **Identity Resolution is already working.** No new rules are needed. The CRM Contact data stream resolves contacts to Unified Individuals automatically.

---

## Phase → Demo Stop Mapping

| Component | Demo Stop | Purpose |
|-----------|-----------|---------|
| Vehicle DMO (verified) | Stop 2, 3, 5 | Segment qualification, email vehicle cards, Customer 360 |
| TestDrive DMO (verified) | Stop 2, 3, 4, 5 | Waterfall qualification, flow suppression, Customer 360 |
| WebEng DMO (newly mapped) | Stop 2, 4, 5 | CI scoring, flow engagement signals, Customer 360 |
| FK Relationships (verified) | Stop 5 | Data Graph requires DMO FKs to link objects |
| Identity Resolution (verified) | All Stops | All DMO data must link to Unified Individuals |
