# Phase 3: Calculated Insights — Implementation Plan

## Overview

Create 4 Calculated Insights (CIs) that power the MCA demo's personalization, segmentation, and decisioning layers. These CIs aggregate data from the custom DMOs (Phase 2) into actionable metrics per customer — enabling segments (Phase 5) and MCA Flow decisions (Phase 8).

Each CI runs a SQL expression against Data Cloud's `__dlm` tables, materializes results into a `__cio` queryable table, and exposes columns (all suffixed `__c`) that downstream segments and flows reference by name.

**Org:** `carmax-sdo-mm-app-wz95pw`
**API Version:** 65.0
**Prerequisite:** Phase 2 complete (DMOs verified, WebEng mapped, data populated)

> **IMPORTANT: Field Name Conventions in This Phase**
>
> - **CarMax_Vehicle__dlm** uses CamelCase IngestAPI field names: `IndividualId__c`, `IsHearted__c`, `IsPurchased__c`, `BodyType__c`, `FuelType__c`, `HeartedById__c`
> - **CarMax_TestDrive__dlm** uses CamelCase: `IndividualId__c`, `ConvertedToPurchase__c`, `TestDriveDate__c`
> - **ssot__WebsiteEngagement__dlm** uses `ssot__` prefixed standard field names: `ssot__IndividualId__c`, `ssot__EngagementChannelActionId__c` (event type), `ssot__EngagementDateTm__c` (timestamp), `ssot__EngagementVehicleId__c` (VIN), `ssot__SessionId__c`
> - These are NOT CRM custom object field names (no `Is_Purchased__c`, `Body_Type__c`, etc.)

> **CRITICAL: CI-to-Unified Individual Connection for Segmentation**
>
> Segments in this org are based on **`UnifiedssotIndividualInd1__dlm`** (the Unified Individual DMO from Identity Resolution ruleset `Ind1`). For CIs to appear as segment filters, the CI SQL must JOIN all the way through the Identity Resolution link table to `UnifiedssotIndividualInd1__dlm` and GROUP BY its `ssot__Id__c` field. This is a **4-table join chain**:
>
> ```
> Source DMO → ssot__Individual__dlm → UnifiedLinkssotIndividualInd1__dlm → UnifiedssotIndividualInd1__dlm
> ```
>
> **ID Format Chain:**
> - Source DMOs (`CarMax_Vehicle__dlm.IndividualId__c`, `ssot__WebsiteEngagement__dlm.ssot__IndividualId__c`) hold CRM Contact IDs (e.g., `003ak00001QQSQzAAP`)
> - `ssot__Individual__dlm.ssot__Id__c` holds CRM Contact IDs (same format)
> - `UnifiedLinkssotIndividualInd1__dlm` maps `SourceRecordId__c` (CRM) → `UnifiedRecordId__c` (hashed)
> - `UnifiedssotIndividualInd1__dlm.ssot__Id__c` holds hashed Unified IDs (e.g., `06cb0293137acdbc...`)
>
> All 4 CIs follow this join pattern:
> - **CI #1** (CLV): `CarMax_Vehicle__dlm → Individual → Link → UnifiedIndividual`
> - **CI #2** (Propensity): `WebsiteEngagement → Individual → Link → UnifiedIndividual`
> - **CI #3** (Preference): `WebsiteEngagement → Individual → Link → UnifiedIndividual ← LEFT JOIN Vehicle`
> - **CI #4** (Velocity): `WebsiteEngagement → Individual → Link → UnifiedIndividual`
>
> **Proof:** The existing `Hearted_Vehicles_v1` segment uses `segmentOnApiName: "UnifiedssotIndividualInd1__dlm"`. Both join paths (Vehicle-based and WebEng-based) were tested and verified to return correct hashed Unified IDs.

---

## Existing CIs (Do NOT Modify)

These CIs are pre-installed in the SDO org. Do not delete, rename, or overwrite them:

- Marketing Engagement Score
- Marketing Fit Score
- Marketing Overall Score
- (1 additional system CI)

All 4 new CIs below use unique names that will not collide.

---

## Step 1: Create All 4 Calculated Insights

### CI #1: Customer Lifetime Value (CLV)

**Purpose:** Aggregates purchase history and vehicle interaction data per customer. Powers high-value customer identification in the waterfall segment (Stop 2) and provides lifetime metrics for the Customer 360 profile (Stop 5).

**SQL Expression (readable):**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c,
  COUNT(1)                     AS VehicleInteractions__c,
  SUM(
    CASE WHEN CarMax_Vehicle__dlm.IsPurchased__c = 'true' THEN CarMax_Vehicle__dlm.Price__c ELSE 0 END
  )                            AS TotalPurchaseValue__c,
  SUM(
    CASE WHEN CarMax_Vehicle__dlm.IsPurchased__c = 'true' THEN 1 ELSE 0 END
  )                            AS PurchaseCount__c,
  SUM(
    CASE WHEN CarMax_Vehicle__dlm.IsHearted__c = 'true' THEN 1 ELSE 0 END
  )                            AS HeartedCount__c,
  AVG(CarMax_Vehicle__dlm.Price__c) AS AvgVehiclePrice__c
FROM
  CarMax_Vehicle__dlm
JOIN
  ssot__Individual__dlm
ON
  CarMax_Vehicle__dlm.IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN
  UnifiedLinkssotIndividualInd1__dlm
ON
  ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN
  UnifiedssotIndividualInd1__dlm
ON
  UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY
  UnifiedssotIndividualInd1__dlm.ssot__Id__c
```

> **Note:** `IsPurchased__c` and `IsHearted__c` are Text fields (stored as `'true'`/`'false'` strings), not Boolean. The 4-table join chain resolves CRM Contact IDs in `CarMax_Vehicle__dlm.IndividualId__c` through Identity Resolution to hashed Unified Individual IDs in `UnifiedssotIndividualInd1__dlm.ssot__Id__c`. All column references use full table-qualified names (no aliases — Data Cloud SQL does not support table aliases).

**Create command:**

```bash
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights" \
  --body '{
    "label": "Customer Lifetime Value",
    "name": "Customer_Lifetime_Value",
    "description": "Aggregates purchase history and vehicle interaction metrics per customer for lifetime value scoring.",
    "definitionType": "CALCULATED_METRIC",
    "expression": "SELECT UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c, COUNT(1) AS VehicleInteractions__c, SUM(CASE WHEN CarMax_Vehicle__dlm.IsPurchased__c = '"'"'true'"'"' THEN CarMax_Vehicle__dlm.Price__c ELSE 0 END) AS TotalPurchaseValue__c, SUM(CASE WHEN CarMax_Vehicle__dlm.IsPurchased__c = '"'"'true'"'"' THEN 1 ELSE 0 END) AS PurchaseCount__c, SUM(CASE WHEN CarMax_Vehicle__dlm.IsHearted__c = '"'"'true'"'"' THEN 1 ELSE 0 END) AS HeartedCount__c, AVG(CarMax_Vehicle__dlm.Price__c) AS AvgVehiclePrice__c FROM CarMax_Vehicle__dlm JOIN ssot__Individual__dlm ON CarMax_Vehicle__dlm.IndividualId__c = ssot__Individual__dlm.ssot__Id__c JOIN UnifiedLinkssotIndividualInd1__dlm ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c JOIN UnifiedssotIndividualInd1__dlm ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c",
    "publishScheduleInterval": "SIX"
  }' \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected response:**

```json
{
  "name": "Customer_Lifetime_Value",
  "calculatedInsightStatus": "DRAFT"
}
```

---

### CI #2: Propensity to Buy

**Purpose:** Multi-factor behavioral score combining event-type weighting and time-decay. Powers segment qualification (Stop 2) and MCA Flow decision splits (Stop 4). A higher score indicates stronger purchase intent.

**Scoring logic:**

| Event Type | Weight |
|------------|--------|
| Vehicle Detail View | 3 |
| Save Search | 4 |
| Heart Vehicle | 5 |
| Pre-Qual Start | 6 |
| Pre-Qual Complete | 8 |
| Schedule Test Drive | 7 |
| Instant Offer Start | 5 |
| Instant Offer Complete | 8 |
| Finance Application | 9 |
| (all other events) | 1 |

**Time-decay logic:**

The date comparison uses the `YEAR * 10000 + MONTH * 100 + DAY` integer pattern because Data Cloud SQL does not support direct date arithmetic or `DATEDIFF`. Each engagement is multiplied by a recency factor:

| Date Window | Integer Threshold | Multiplier | Meaning |
|-------------|-------------------|------------|---------|
| On or after May 1, 2026 | >= 20260501 | 3x | Last ~1 week (hot) |
| On or after Apr 24, 2026 | >= 20260424 | 2x | Last ~2 weeks (warm) |
| On or after Apr 8, 2026 | >= 20260408 | 1x | Last ~1 month (baseline) |
| Before Apr 8, 2026 | < 20260408 | 0.5x | Older than 1 month (decayed) |

**SQL Expression (readable):**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c          AS IndividualId__c,
  SUM(
    CASE
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Vehicle Detail View'        THEN 3
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Save Search'                THEN 4
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Heart Vehicle'              THEN 5
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Pre-Qualification Start'    THEN 6
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Pre-Qualification Complete' THEN 8
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Schedule Test Drive'        THEN 7
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Instant Offer Start'        THEN 5
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Instant Offer Complete'     THEN 8
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = 'Finance Application'        THEN 9
      ELSE 1
    END
    *
    CASE
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260501 THEN 3
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260424 THEN 2
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260408 THEN 1
      ELSE 0.5
    END
  )                                                   AS PropensityScore__c,
  COUNT(1)                                            AS TotalEngagements__c,
  APPROX_COUNT_DISTINCT(ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c) AS UniqueEventTypes__c,
  MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS LastEngagementDate__c
FROM
  ssot__WebsiteEngagement__dlm
JOIN
  ssot__Individual__dlm
ON
  ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN
  UnifiedLinkssotIndividualInd1__dlm
ON
  ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN
  UnifiedssotIndividualInd1__dlm
ON
  UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY
  UnifiedssotIndividualInd1__dlm.ssot__Id__c
```

> **Note:** Event type values use the full names as ingested (e.g., `'Pre-Qualification Complete'` not `'Pre-Qual Complete'`). The standard DMO field `ssot__EngagementChannelActionId__c` holds the event type string, and `ssot__EngagementDateTm__c` holds the timestamp.

**Create command:**

```bash
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights" \
  --body '{
    "label": "Propensity to Buy",
    "name": "Propensity_to_Buy",
    "description": "Multi-factor behavioral propensity score with event-type weighting and time-decay. Higher scores indicate stronger purchase intent.",
    "definitionType": "CALCULATED_METRIC",
    "expression": "SELECT UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c, SUM(CASE WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Vehicle Detail View'"'"' THEN 3 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Save Search'"'"' THEN 4 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Heart Vehicle'"'"' THEN 5 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Pre-Qualification Start'"'"' THEN 6 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Pre-Qualification Complete'"'"' THEN 8 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Schedule Test Drive'"'"' THEN 7 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Instant Offer Start'"'"' THEN 5 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Instant Offer Complete'"'"' THEN 8 WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c = '"'"'Finance Application'"'"' THEN 9 ELSE 1 END * CASE WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260501 THEN 3 WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260424 THEN 2 WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260408 THEN 1 ELSE 0.5 END) AS PropensityScore__c, COUNT(1) AS TotalEngagements__c, APPROX_COUNT_DISTINCT(ssot__WebsiteEngagement__dlm.ssot__EngagementChannelActionId__c) AS UniqueEventTypes__c, MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS LastEngagementDate__c FROM ssot__WebsiteEngagement__dlm JOIN ssot__Individual__dlm ON ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c JOIN UnifiedLinkssotIndividualInd1__dlm ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c JOIN UnifiedssotIndividualInd1__dlm ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c",
    "publishScheduleInterval": "SIX"
  }' \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected response:**

```json
{
  "name": "Propensity_to_Buy",
  "calculatedInsightStatus": "DRAFT"
}
```

---

### CI #3: Vehicle Preference Affinity

**Purpose:** Determines each customer's preferred vehicle body type, fuel type, average browsed price, and interaction depth by joining web engagement data against the vehicle catalog. Powers vehicle card selection in personalized emails (Stop 3).

**SQL Expression (readable):**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c          AS IndividualId__c,
  CarMax_Vehicle__dlm.BodyType__c                     AS PreferredBodyType__c,
  CarMax_Vehicle__dlm.FuelType__c                     AS PreferredFuelType__c,
  COUNT(1)                                            AS InteractionCount__c,
  AVG(CarMax_Vehicle__dlm.Price__c)                   AS AvgBrowsedPrice__c,
  MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS LastBrowseDate__c
FROM
  ssot__WebsiteEngagement__dlm
JOIN
  ssot__Individual__dlm
ON
  ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN
  UnifiedLinkssotIndividualInd1__dlm
ON
  ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN
  UnifiedssotIndividualInd1__dlm
ON
  UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
LEFT JOIN
  CarMax_Vehicle__dlm
ON
  ssot__WebsiteEngagement__dlm.ssot__EngagementVehicleId__c = CarMax_Vehicle__dlm.VIN__c
GROUP BY
  UnifiedssotIndividualInd1__dlm.ssot__Id__c,
  CarMax_Vehicle__dlm.BodyType__c,
  CarMax_Vehicle__dlm.FuelType__c
```

> **Note:** This CI joins five tables: `ssot__WebsiteEngagement__dlm` → `ssot__Individual__dlm` → `UnifiedLinkssotIndividualInd1__dlm` → `UnifiedssotIndividualInd1__dlm` (the Identity Resolution chain), plus a LEFT JOIN to `CarMax_Vehicle__dlm` for vehicle attributes. The GROUP BY uses `UnifiedssotIndividualInd1__dlm.ssot__Id__c` — the hashed Unified Individual ID — which is what makes this CI available as a segment filter.

**Important:** Table aliases are NOT supported in Data Cloud SQL. Use the full table name (`ssot__WebsiteEngagement__dlm`, `CarMax_Vehicle__dlm`) for every column reference.

**Create command:**

```bash
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights" \
  --body '{
    "label": "Vehicle Preference Affinity",
    "name": "Vehicle_Preference_Affinity",
    "description": "Determines preferred vehicle body type, fuel type, and average browsed price per customer by joining web engagements against the vehicle catalog.",
    "definitionType": "CALCULATED_METRIC",
    "expression": "SELECT UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c, CarMax_Vehicle__dlm.BodyType__c AS PreferredBodyType__c, CarMax_Vehicle__dlm.FuelType__c AS PreferredFuelType__c, COUNT(1) AS InteractionCount__c, AVG(CarMax_Vehicle__dlm.Price__c) AS AvgBrowsedPrice__c, MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS LastBrowseDate__c FROM ssot__WebsiteEngagement__dlm JOIN ssot__Individual__dlm ON ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c JOIN UnifiedLinkssotIndividualInd1__dlm ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c JOIN UnifiedssotIndividualInd1__dlm ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c LEFT JOIN CarMax_Vehicle__dlm ON ssot__WebsiteEngagement__dlm.ssot__EngagementVehicleId__c = CarMax_Vehicle__dlm.VIN__c GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c, CarMax_Vehicle__dlm.BodyType__c, CarMax_Vehicle__dlm.FuelType__c",
    "publishScheduleInterval": "SIX"
  }' \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected response:**

```json
{
  "name": "Vehicle_Preference_Affinity",
  "calculatedInsightStatus": "DRAFT"
}
```

---

### CI #4: Engagement Velocity

**Purpose:** Compares week-over-week engagement volume to identify accelerating (hot) shoppers. Powers the "hot shopper" identification in the waterfall segment (Stop 2) for priority outreach.

**Date windows:**

| Window | Condition | Meaning |
|--------|-----------|---------|
| RecentWeek | `>= 20260501` | May 1, 2026 and later (current week) |
| PriorWeek | `>= 20260424 AND < 20260501` | Apr 24 – Apr 30, 2026 (previous week) |

**SQL Expression (readable):**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c,
  SUM(
    CASE
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260501
      THEN 1 ELSE 0
    END
  )                                          AS RecentWeekEvents__c,
  SUM(
    CASE
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260424
       AND YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) <  20260501
      THEN 1 ELSE 0
    END
  )                                          AS PriorWeekEvents__c,
  COUNT(1)                                   AS TotalEvents__c,
  APPROX_COUNT_DISTINCT(ssot__WebsiteEngagement__dlm.ssot__SessionId__c) AS UniqueSessions__c,
  MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS MostRecentEvent__c
FROM
  ssot__WebsiteEngagement__dlm
JOIN
  ssot__Individual__dlm
ON
  ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN
  UnifiedLinkssotIndividualInd1__dlm
ON
  ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN
  UnifiedssotIndividualInd1__dlm
ON
  UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY
  UnifiedssotIndividualInd1__dlm.ssot__Id__c
```

> **Note:** This CI joins through the full 4-table Identity Resolution chain to GROUP BY `UnifiedssotIndividualInd1__dlm.ssot__Id__c` — the hashed Unified Individual ID. This is required for the CI to appear in the Segment Canvas. All column references use full table names (no aliases — Data Cloud SQL does not support table aliases).

**Create command:**

```bash
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights" \
  --body '{
    "label": "Engagement Velocity",
    "name": "Engagement_Velocity",
    "description": "Week-over-week engagement comparison to identify accelerating shoppers. RecentWeek vs PriorWeek event counts for velocity calculation.",
    "definitionType": "CALCULATED_METRIC",
    "expression": "SELECT UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c, SUM(CASE WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260501 THEN 1 ELSE 0 END) AS RecentWeekEvents__c, SUM(CASE WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260424 AND YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000 + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100 + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) < 20260501 THEN 1 ELSE 0 END) AS PriorWeekEvents__c, COUNT(1) AS TotalEvents__c, APPROX_COUNT_DISTINCT(ssot__WebsiteEngagement__dlm.ssot__SessionId__c) AS UniqueSessions__c, MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS MostRecentEvent__c FROM ssot__WebsiteEngagement__dlm JOIN ssot__Individual__dlm ON ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c JOIN UnifiedLinkssotIndividualInd1__dlm ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c JOIN UnifiedssotIndividualInd1__dlm ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c",
    "publishScheduleInterval": "SIX"
  }' \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected response:**

```json
{
  "name": "Engagement_Velocity",
  "calculatedInsightStatus": "DRAFT"
}
```

---

## Step 2: Wait for ACTIVE Status

After creation, each CI transitions through states: `DRAFT` -> `PROCESSING` -> `ACTIVE` (or `FAILED`). You must wait for `ACTIVE` before triggering materialization.

**Poll all 4 CIs:**

```bash
echo "=== Polling CI Status ==="
for CI_NAME in Customer_Lifetime_Value Propensity_to_Buy Vehicle_Preference_Affinity Engagement_Velocity; do
  echo ""
  echo "--- ${CI_NAME} ---"
  sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio" \
    --target-org carmax-sdo-mm-app-wz95pw \
    | grep -E '"calculatedInsightStatus"|"name"'
done
```

**Expected output (when ready):**

```
--- Customer_Lifetime_Value ---
  "name": "Customer_Lifetime_Value",
  "calculatedInsightStatus": "ACTIVE"

--- Propensity_to_Buy ---
  "name": "Propensity_to_Buy",
  "calculatedInsightStatus": "ACTIVE"

--- Vehicle_Preference_Affinity ---
  "name": "Vehicle_Preference_Affinity",
  "calculatedInsightStatus": "ACTIVE"

--- Engagement_Velocity ---
  "name": "Engagement_Velocity",
  "calculatedInsightStatus": "ACTIVE"
```

**Timing:** CIs typically reach ACTIVE within 2-5 minutes. If a CI stays in PROCESSING for more than 10 minutes, it may be stuck.

### If a CI Fails: Delete and Recreate

If a CI shows `FAILED` status, you must delete it and recreate it. You CANNOT PATCH a CI that is in `PROCESSING` or `FAILED` state.

**Delete a failed CI:**

```bash
sf api request rest \
  --method DELETE \
  --url "/services/data/v65.0/ssot/calculated-insights/FAILED_CI_NAME__cio" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Then re-run the corresponding creation command from Step 1.

**Common failure causes:**
- Column name missing `__c` suffix
- Table name missing `__dlm` suffix
- Using `COUNT(DISTINCT x)` instead of `APPROX_COUNT_DISTINCT(x)`
- Using table aliases (e.g., `e.ssot__IndividualId__c` instead of `ssot__WebsiteEngagement__dlm.ssot__IndividualId__c`)
- Referencing a DMO field that doesn't exist or is misspelled
- Including `measures` or `dimensions` fields in the JSON body

---

## Step 3: Trigger Materialization

Once all 4 CIs are in `ACTIVE` status, trigger materialization for each. This runs the SQL expression and writes results to the `__cio` queryable table.

**Trigger all 4 materializations:**

```bash
echo "=== Triggering CI Materialization ==="
for CI_NAME in Customer_Lifetime_Value Propensity_to_Buy Vehicle_Preference_Affinity Engagement_Velocity; do
  echo ""
  echo "--- Triggering ${CI_NAME} ---"
  sf api request rest \
    --method POST \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio/actions/run" \
    --body '{}' \
    --target-org carmax-sdo-mm-app-wz95pw
  echo "Triggered: ${CI_NAME}"
done
```

**Critical:** The `--body '{}'` is required — an empty JSON body. Omitting the body or sending no body will cause a 400 error.

---

## Step 4: Poll for Materialization Completion

After triggering, each CI will materialize asynchronously. Poll until `lastRunStatus` shows `SUCCESS`.

**Poll materialization status:**

```bash
echo "=== Polling Materialization Status ==="
for CI_NAME in Customer_Lifetime_Value Propensity_to_Buy Vehicle_Preference_Affinity Engagement_Velocity; do
  echo ""
  echo "--- ${CI_NAME} ---"
  sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio" \
    --target-org carmax-sdo-mm-app-wz95pw \
    | grep -E '"lastRunStatus"|"lastRunDate"|"name"'
done
```

**Expected output (when complete):**

```
--- Customer_Lifetime_Value ---
  "name": "Customer_Lifetime_Value",
  "lastRunStatus": "SUCCESS",
  "lastRunDate": "2026-05-09T..."

--- Propensity_to_Buy ---
  "name": "Propensity_to_Buy",
  "lastRunStatus": "SUCCESS",
  "lastRunDate": "2026-05-09T..."

--- Vehicle_Preference_Affinity ---
  "name": "Vehicle_Preference_Affinity",
  "lastRunStatus": "SUCCESS",
  "lastRunDate": "2026-05-09T..."

--- Engagement_Velocity ---
  "name": "Engagement_Velocity",
  "lastRunStatus": "SUCCESS",
  "lastRunDate": "2026-05-09T..."
```

**Timing:** Materialization typically completes in 3-8 minutes depending on data volume.

---

## Step 5: Verify CI Output Data

Query each materialized CIO table to confirm data is present and correct.

### Verify CI #1: Customer Lifetime Value

```bash
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Customer_Lifetime_Value__cio/data?limit=5" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected columns in each row:**
- `IndividualId__c` — the hashed Unified Individual identifier (from `UnifiedssotIndividualInd1__dlm.ssot__Id__c`)
- `VehicleInteractions__c` — total vehicle records per customer
- `TotalPurchaseValue__c` — sum of purchase prices (0 if no purchases)
- `PurchaseCount__c` — number of purchased vehicles
- `HeartedCount__c` — number of hearted vehicles
- `AvgVehiclePrice__c` — average price across all vehicles

**Spot check — Jane Dawson should show:**
- `VehicleInteractions__c` >= 5 (3 hearted + 1 test driven + 1 purchased)
- `PurchaseCount__c` >= 1
- `HeartedCount__c` = 3

### Verify CI #2: Propensity to Buy

```bash
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Propensity_to_Buy__cio/data?limit=5" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected columns in each row:**
- `IndividualId__c` — the hashed Unified Individual identifier (from `UnifiedssotIndividualInd1__dlm.ssot__Id__c`)
- `PropensityScore__c` — weighted, time-decayed score (higher = stronger intent)
- `TotalEngagements__c` — raw count of all engagement events
- `UniqueEventTypes__c` — approximate number of distinct event types
- `LastEngagementDate__c` — most recent engagement timestamp

**Spot check — Jane Dawson should show:**
- `PropensityScore__c` > 50 (active shopper with multiple high-weight events)
- `UniqueEventTypes__c` >= 4 (Vehicle Detail View, Heart Vehicle, Schedule Test Drive, Pre-Qual Complete, etc.)

### Verify CI #3: Vehicle Preference Affinity

```bash
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Vehicle_Preference_Affinity__cio/data?limit=5" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected columns in each row:**
- `IndividualId__c` — the hashed Unified Individual identifier (from `UnifiedssotIndividualInd1__dlm.ssot__Id__c`)
- `PreferredBodyType__c` — e.g., "SUV", "Sedan", "Truck"
- `PreferredFuelType__c` — e.g., "Gasoline", "Hybrid", "Electric"
- `InteractionCount__c` — number of web engagements for this body/fuel combo
- `AvgBrowsedPrice__c` — average vehicle price in this preference group
- `LastBrowseDate__c` — most recent browse for this combo

**Spot check — Jane Dawson should show:**
- At least one row with `PreferredBodyType__c` = "SUV" (her 3 hearted vehicles are all SUVs)
- `InteractionCount__c` >= 3 for the SUV row

### Verify CI #4: Engagement Velocity

```bash
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Engagement_Velocity__cio/data?limit=5" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected columns in each row:**
- `IndividualId__c` — the hashed Unified Individual identifier (from `UnifiedssotIndividualInd1__dlm.ssot__Id__c`)
- `RecentWeekEvents__c` — events from May 1, 2026 onward
- `PriorWeekEvents__c` — events from Apr 24-30, 2026
- `TotalEvents__c` — all-time event count
- `UniqueSessions__c` — approximate distinct session count
- `MostRecentEvent__c` — timestamp of most recent event

**Spot check — Jane Dawson should show:**
- `RecentWeekEvents__c` > 0 (she has recent activity)
- `RecentWeekEvents__c` > `PriorWeekEvents__c` (she's an accelerating shopper)

### Full Verification Summary Script

```bash
echo "============================================"
echo "  Phase 3 — CI Verification Summary"
echo "============================================"
echo ""

for CI_NAME in Customer_Lifetime_Value Propensity_to_Buy Vehicle_Preference_Affinity Engagement_Velocity; do
  echo "--- ${CI_NAME} ---"

  # Get status
  STATUS=$(sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio" \
    --target-org carmax-sdo-mm-app-wz95pw 2>/dev/null \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('calculatedInsightStatus','UNKNOWN'))" 2>/dev/null)

  RUN_STATUS=$(sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio" \
    --target-org carmax-sdo-mm-app-wz95pw 2>/dev/null \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('lastRunStatus','UNKNOWN'))" 2>/dev/null)

  # Get row count
  ROW_COUNT=$(sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio/data?limit=1" \
    --target-org carmax-sdo-mm-app-wz95pw 2>/dev/null \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('totalSize','0'))" 2>/dev/null)

  echo "  CI Status:       ${STATUS}"
  echo "  Last Run Status: ${RUN_STATUS}"
  echo "  Row Count:       ${ROW_COUNT}"
  echo ""
done

echo "============================================"
echo "  Expected: All ACTIVE, All SUCCESS, All > 0"
echo "============================================"
```

---

## CI → Demo Stop Mapping

This table shows exactly where each CI is referenced in the demo and why it exists.

| CI | CIO Table Name | Demo Stop | Purpose |
|----|---------------|-----------|---------|
| Customer Lifetime Value | `Customer_Lifetime_Value__cio` | Stop 2 (Segmentation) | High-value customer identification for waterfall priority. CLV tier determines whether a customer gets premium outreach. |
| Propensity to Buy | `Propensity_to_Buy__cio` | Stop 2 (Segmentation) + Stop 4 (MCA Flow) | Behavioral scoring for segment qualification. Flow decision splits use PropensityScore__c to route high-intent vs. low-intent customers. |
| Vehicle Preference Affinity | `Vehicle_Preference_Affinity__cio` | Stop 3 (Dynamic Email) | Powers vehicle card selection in personalized emails. PreferredBodyType__c and AvgBrowsedPrice__c enable "Compare What Matters" content. |
| Engagement Velocity | `Engagement_Velocity__cio` | Stop 2 (Segmentation) | Hot shopper identification for priority outreach. When RecentWeekEvents > PriorWeekEvents, customer is accelerating — qualifies for urgent segments. |

---

## Critical Notes & Gotchas

These 13 rules were discovered through direct testing against the Data Cloud CI API. Violating any of them will cause CI creation to fail, produce incorrect results, or prevent CIs from being usable for segmentation.

### 1. `definitionType` must be `CALCULATED_METRIC`

The only supported value for CIs created via the REST API is `CALCULATED_METRIC`. Do not use `CALCULATED_INSIGHT`, `METRIC`, or any other value.

```json
"definitionType": "CALCULATED_METRIC"
```

### 2. Column aliases MUST end with `__c`

Every column in the SELECT clause must have an alias ending in `__c`. This is a Data Cloud naming convention for custom columns. Without it, the CI will fail to create or the column will not be queryable.

```sql
-- CORRECT
COUNT(1) AS VehicleInteractions__c

-- WRONG — will fail
COUNT(1) AS VehicleInteractions
COUNT(1) AS vehicle_interactions
```

### 3. Use `APPROX_COUNT_DISTINCT` instead of `COUNT(DISTINCT)`

Data Cloud SQL does not support the standard `COUNT(DISTINCT column)` syntax. Use `APPROX_COUNT_DISTINCT(column)` instead, which returns an approximate distinct count using HyperLogLog.

```sql
-- CORRECT
APPROX_COUNT_DISTINCT(Event_Type__c) AS UniqueEventTypes__c

-- WRONG — will fail
COUNT(DISTINCT Event_Type__c) AS UniqueEventTypes__c
```

### 4. Table names must include `__dlm` suffix

All Data Model Object tables in Data Cloud are referenced with the `__dlm` suffix. This is the "data lake materialized" suffix that identifies the queryable version of the DMO.

```sql
-- CORRECT
FROM CarMax_Vehicle__dlm

-- WRONG
FROM CarMax_Vehicle
FROM CarMax_Vehicle__c
FROM CarMax_Vehicle__dlo
```

### 5. No table aliases allowed — use full table names

Data Cloud SQL does not support table aliases in CI expressions. Every column reference in a JOIN must use the full table name.

```sql
-- CORRECT
ssot__WebsiteEngagement__dlm.ssot__IndividualId__c

-- WRONG — will fail
e.ssot__IndividualId__c
eng.ssot__IndividualId__c
```

### 6. Date comparison requires `YEAR * 10000 + MONTH * 100 + DAY` pattern

Data Cloud SQL does not support `DATEDIFF`, `DATE_SUB`, `INTERVAL`, or direct date arithmetic. To compare dates against fixed thresholds, decompose the date into an integer using the YYYYMMDD pattern.

```sql
-- CORRECT
YEAR(Event_Date__c) * 10000 + MONTH(Event_Date__c) * 100 + DAY(Event_Date__c) >= 20260501

-- WRONG — not supported
DATEDIFF(NOW(), Event_Date__c) <= 7
Event_Date__c >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
Event_Date__c >= '2026-05-01'
```

### 7. `MAX` / `MIN` only work on Number and Date/DateTime

Do not attempt `MAX(string_column)` or `MIN(string_column)`. If you need the "most recent" value of a string column, use a subquery or restructure to use the date column instead.

```sql
-- CORRECT
MAX(Event_Date__c) AS LastEngagementDate__c

-- WRONG — will fail on string columns
MAX(Event_Type__c) AS LastEventType__c
```

### 8. Do NOT include `measures` or `dimensions` fields

The CI REST API body should contain only: `label`, `name`, `description`, `definitionType`, `expression`, and `publishScheduleInterval`. Do NOT include `measures`, `dimensions`, `filters`, or other fields that appear in older documentation.

```json
// CORRECT — only these fields
{
  "label": "...",
  "name": "...",
  "description": "...",
  "definitionType": "CALCULATED_METRIC",
  "expression": "...",
  "publishScheduleInterval": "SIX"
}

// WRONG — do not include these
{
  "measures": [...],
  "dimensions": [...],
  "filters": [...]
}
```

### 9. Do NOT PATCH a CI in `PROCESSING` state

If a CI is in `PROCESSING` state, you cannot update it with a PATCH request. You must wait for it to reach `ACTIVE` or `FAILED`. If it fails, DELETE it and recreate from scratch.

```bash
# Check state first
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/CI_NAME__cio" \
  --target-org carmax-sdo-mm-app-wz95pw

# If PROCESSING — WAIT. Do not PATCH.
# If FAILED — DELETE, then re-POST.
# If ACTIVE — safe to PATCH or trigger run.
```

### 10. Materialization trigger: POST `/actions/run` with empty body `{}`

The materialization endpoint requires a POST with an empty JSON body. Omitting the body entirely will cause a 400 error. The URL includes the `__cio` suffix.

```bash
# CORRECT
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights/CI_NAME__cio/actions/run" \
  --body '{}' \
  --target-org carmax-sdo-mm-app-wz95pw

# WRONG — missing body
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights/CI_NAME__cio/actions/run" \
  --target-org carmax-sdo-mm-app-wz95pw

# WRONG — missing __cio suffix in URL
sf api request rest \
  --method POST \
  --url "/services/data/v65.0/ssot/calculated-insights/CI_NAME/actions/run" \
  --body '{}' \
  --target-org carmax-sdo-mm-app-wz95pw
```

### 11. Date thresholds are hardcoded — update if demo date changes

The Propensity to Buy and Engagement Velocity CIs use hardcoded date thresholds (20260501, 20260424, 20260408). If the demo date shifts, these thresholds must be updated:

| CI | Fields to Update | Current Values |
|----|-----------------|----------------|
| Propensity to Buy | All 3 time-decay CASE thresholds | 20260501, 20260424, 20260408 |
| Engagement Velocity | RecentWeek and PriorWeek boundaries | 20260501, 20260424 |

**To update:** Delete the CI, modify the expression SQL, and recreate it.

### 12. LEFT JOIN is supported

Data Cloud SQL supports `LEFT JOIN` in CI expressions. This is used by CI #3 (Vehicle Preference Affinity) to join web engagements against the vehicle catalog. If a web engagement references a VIN that doesn't exist in the vehicle table, the vehicle columns will be NULL — the row is still included in the output.

```sql
-- This works
FROM ssot__WebsiteEngagement__dlm
LEFT JOIN CarMax_Vehicle__dlm
ON ssot__WebsiteEngagement__dlm.ssot__EngagementVehicleId__c = CarMax_Vehicle__dlm.VIN__c
```

### 13. CIs MUST JOIN through Identity Resolution to `UnifiedssotIndividualInd1__dlm` for segmentation

**This is the most critical gotcha.** Segments in this org are based on `UnifiedssotIndividualInd1__dlm` (the Unified Individual DMO from Identity Resolution ruleset `Ind1`). For a CI to appear as a segment filter, the CI SQL must:

1. **JOIN through the full 4-table Identity Resolution chain** — source DMO → `ssot__Individual__dlm` → `UnifiedLinkssotIndividualInd1__dlm` → `UnifiedssotIndividualInd1__dlm`
2. **SELECT `UnifiedssotIndividualInd1__dlm.ssot__Id__c`** as a dimension (aliased to `IndividualId__c`)
3. **GROUP BY `UnifiedssotIndividualInd1__dlm.ssot__Id__c`** — NOT by `ssot__Individual__dlm.ssot__Id__c` or any source DMO field

Simply JOINing to `ssot__Individual__dlm` is **NOT sufficient** — that DMO holds CRM Contact IDs (e.g., `003ak...`), not the hashed Unified IDs (e.g., `06cb02...`) that the segment is built on. You must go all the way through the Link table to the Unified Individual DMO.

```sql
-- CORRECT — CI will be available for segmentation (4-table join)
SELECT UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c, COUNT(1) AS metric__c
FROM CarMax_Vehicle__dlm
JOIN ssot__Individual__dlm
  ON CarMax_Vehicle__dlm.IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN UnifiedLinkssotIndividualInd1__dlm
  ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN UnifiedssotIndividualInd1__dlm
  ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c

-- WRONG — CI will NOT be available for segmentation (stops at Individual, not Unified Individual)
SELECT ssot__Individual__dlm.ssot__Id__c AS IndividualId__c, COUNT(1) AS metric__c
FROM CarMax_Vehicle__dlm
JOIN ssot__Individual__dlm ON CarMax_Vehicle__dlm.IndividualId__c = ssot__Individual__dlm.ssot__Id__c
GROUP BY ssot__Individual__dlm.ssot__Id__c

-- WRONG — CI will NOT be available for segmentation (no JOIN at all)
SELECT IndividualId__c, COUNT(1) AS metric__c
FROM CarMax_Vehicle__dlm
GROUP BY IndividualId__c
```

---

## Troubleshooting Playbook

### CI stuck in PROCESSING for > 10 minutes

```bash
# Check current status
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/CI_NAME__cio" \
  --target-org carmax-sdo-mm-app-wz95pw

# If still PROCESSING after 10+ min, delete and recreate
sf api request rest \
  --method DELETE \
  --url "/services/data/v65.0/ssot/calculated-insights/CI_NAME__cio" \
  --target-org carmax-sdo-mm-app-wz95pw

# Then re-run the create command from Step 1
```

### Materialization returns 0 rows

This means the SQL expression ran but matched no data. Common causes:
1. **Phase 2 data not loaded** — check that the DMO tables have data
2. **Field names misspelled** — verify exact field API names against Phase 2 DMO definitions
3. **JOIN condition mismatch** — verify that `ssot__EngagementVehicleId__c` values in web engagements match `VIN__c` values in the vehicle table

```bash
# Check if source DMO tables have data
sf api request rest \
  --url "/services/data/v65.0/ssot/query?sql=SELECT COUNT(1) AS cnt__c FROM CarMax_Vehicle__dlm" \
  --target-org carmax-sdo-mm-app-wz95pw

sf api request rest \
  --url "/services/data/v65.0/ssot/query?sql=SELECT COUNT(1) AS cnt__c FROM ssot__WebsiteEngagement__dlm" \
  --target-org carmax-sdo-mm-app-wz95pw
```

### CI creation returns 400 error

Read the error message carefully. Common patterns:

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Invalid column alias` | Missing `__c` suffix | Add `__c` to all column aliases |
| `Table not found` | Missing `__dlm` suffix or misspelled table | Verify table name with `__dlm` |
| `Unknown function COUNT_DISTINCT` | Used `COUNT(DISTINCT x)` | Replace with `APPROX_COUNT_DISTINCT(x)` |
| `Cannot resolve column` | Misspelled field name | Check exact API name in DMO definition |
| `Unexpected token` | SQL syntax error | Check for missing commas, unmatched parentheses |

---

## Quick Reference: All CI Names and Their CIO Table Names

| CI Label | CI Name (API) | CIO Table (for queries) |
|----------|---------------|------------------------|
| Customer Lifetime Value | `Customer_Lifetime_Value` | `Customer_Lifetime_Value__cio` |
| Propensity to Buy | `Propensity_to_Buy` | `Propensity_to_Buy__cio` |
| Vehicle Preference Affinity | `Vehicle_Preference_Affinity` | `Vehicle_Preference_Affinity__cio` |
| Engagement Velocity | `Engagement_Velocity` | `Engagement_Velocity__cio` |

---

## Phase 3 Completion Checklist

- [ ] CI #1 (Customer Lifetime Value) created, ACTIVE, materialized, data verified
- [ ] CI #2 (Propensity to Buy) created, ACTIVE, materialized, data verified
- [ ] CI #3 (Vehicle Preference Affinity) created, ACTIVE, materialized, data verified
- [ ] CI #4 (Engagement Velocity) created, ACTIVE, materialized, data verified
- [ ] All 4 existing system CIs still present and unmodified
- [ ] Jane Dawson spot-check passed (CLV shows 3 hearted, Propensity > 50, Preference shows SUV)
- [ ] Verification summary script shows all ACTIVE / SUCCESS / row count > 0
- [ ] Ready for Phase 4 (Data Graph) and Phase 5 (Segments) to reference these CIO tables
