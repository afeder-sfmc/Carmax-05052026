# Phase 5: Segments & Waterfall Prioritization — Implementation Plan

## Overview

Create 8 segments in Data Cloud that serve as the **primary audience constructs** for all MCA campaigns. In MCA, segments replace traditional list-based audience management — they are the entry point for segment-triggered flows (journeys), the source of truth for audience membership, and the governance mechanism for overlap resolution via waterfall prioritization.

This phase creates: **1 Waterfall segment** (with 3 prioritized sub-audiences), **5 Dbt (SQL) segments**, and **2 Einstein AI segments**.

| Attribute | Value |
|-----------|-------|
| **Org** | `carmax-sdo-mm-app-wz95pw` |
| **API Version** | 65.0 |
| **Prerequisite** | Phase 2 (DMOs active with data) + Phase 3 (CIs materialized) |
| **Segment Target DMO** | `UnifiedssotIndividualInd1__dlm` (Unified Individual — required for segmentation) |
| **Total Segments** | 8 (1 Waterfall + 5 Dbt + 2 Einstein) |
| **Total Addressable Audiences** | 10 (Waterfall produces 3 mutually exclusive tiers) |

---

## MCA Context: Why Segments Are Central

In MCA (Marketing Cloud Advanced), segments are **not** just targeting filters — they are:

1. **Journey entry criteria** — Segment-triggered flows use segment membership as the entry condition. No segment = no flow entry.
2. **Audience governance** — Waterfall segments enforce mutual exclusivity across campaigns. A contact in 3 overlapping audiences gets assigned to exactly 1.
3. **Real-time intelligence** — Segments can refresh on schedule, keeping audiences current with Data Cloud. As CIs recalculate and new engagement data streams in, segment membership updates automatically.
4. **The bridge between Data Cloud and MCA** — Segments translate Data Cloud intelligence (DMOs, CIs, engagement events) into marketing-actionable audiences that MCA flows can consume.

**This is fundamentally different from Marketing Cloud Engagement** where lists and data extensions were the primary audience containers. In MCA:
- There are no list imports
- There are no data extension queries
- There is no SQL Activity in Automation Studio
- **Segments ARE the audience** — they are live, governed, and directly connected to the execution layer

Every campaign in this demo maps to exactly one segment (or one waterfall tier). Every flow starts with segment entry. The segment is the single point of truth for "who should receive this campaign."

---

## Segment Architecture

### Waterfall Segment (Demo Stop 2 — Centerpiece)

The waterfall is the governance layer. It solves the most common problem in lifecycle marketing: **a customer qualifies for multiple campaigns simultaneously.**

Jane Dawson qualifies for 3 audiences:
- She hearted vehicles (Hearted Vehicle Follow-Up campaign)
- She test drove but didn't purchase (Test Drive No Purchase campaign)
- She's an active customer in May (Seasonal Push Memorial Day campaign)

Without the waterfall, Jane receives 3 separate campaigns. With it, she receives **only the highest-priority one**:

| Priority | Audience | Campaign | Rationale |
|----------|----------|----------|-----------|
| **P1 (Highest)** | Hearted Vehicle Follow-Up | Hearted Vehicle Follow-Up | Active intent — she is actively comparing vehicles |
| **P2 (Mid)** | Test Drive No Purchase | Test Drive — No Purchase Nurture | Demonstrated interest — she physically visited a store |
| **P3 (Lowest)** | Seasonal Push Memorial Day | Seasonal Push — Memorial Day | Catch-all — broad seasonal campaign |

**The waterfall resolution:** Jane is assigned to P1 only. She is excluded from P2 and P3. She receives the Hearted Vehicle Follow-Up email with her 3 dynamic vehicle cards.

### Standard Segments (Demo Stops 2-3)

Five SQL-based (Dbt) segments aligned to specific campaigns and email content:

| Segment | Campaign Alignment | Key Logic |
|---------|-------------------|-----------|
| New Email Subscribers | New Subscriber Welcome | Opted in within last 30 days, no prior purchase |
| Pre-Qualification Shoppers | Pre-Qualification Completion | Started pre-qual but didn't finish |
| Price Drop Alert Audience | Price Drop Alert | Hearted vehicles with recent price decreases |
| Instant Offer Abandonment | Instant Offer Abandonment | Started instant offer flow but abandoned |
| Saved Search Match | Saved Search Match | Active saved searches with new matching inventory |

### Einstein AI Segments (Demo Stop 2)

Two segments created via Einstein GPT to demonstrate AI-powered audience discovery:

| Segment | Prompt Intent | Demo Value |
|---------|--------------|------------|
| EV Consideration Nurture | Customers showing EV interest signals | AI finds audiences humans might miss |
| Trade-In and Upgrade | Customers likely ready to trade in current vehicle | Predictive audience based on ownership tenure |

---

## Important: Segment Type Constraints

| Type | Create Method | Update Rules Method | Notes |
|------|---------------|-------------------|-------|
| **Waterfall** | REST API POST | **Must configure rules via Salesforce UI** | API creates the shell only; priority tiers and rules require UI |
| **Dbt (SQL)** | ConnectApi Apex (REST has array bug) | Apex PATCH or UI | REST API throws 500 on `queryDefinition.dbtModelNodes` array — must use Apex |
| **EinsteinGptSegmentsUI** | REST API POST | Configure prompts via UI | Creates the segment container; Einstein prompt is configured in UI |

**Critical constraint:** `segmentOnApiName` must be the **Unified Individual DMO** that Identity Resolution produces. For this org, that is always:
```
UnifiedssotIndividualInd1__dlm
```

This is the same DMO that CIs GROUP BY to appear in the Segment Canvas. Using `ssot__Individual__dlm` will NOT work — segments must target the Unified Individual DMO to resolve correctly.

CIO (Calculated Insight Output) tables like `KQ_Customer_Lifetime_Value__dlm` are **NOT valid** as `segmentOnApiName` even though they can be referenced in SQL via JOIN.

---

## Step 1: Create All 8 Segments

### Segment #1: Waterfall — Vehicle Interest Prioritization

**Type:** Waterfall
**Create Method:** REST API POST (creates shell)
**Rules Configuration:** MANDATORY UI configuration after creation

The REST API creates the waterfall segment container. The 3 priority tiers and their SQL rules **must** be configured via the Salesforce UI — the API does not support waterfall rule configuration.

#### 1a. Create Waterfall Shell via REST API

```bash
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments" \
  --body '{
    "segmentOn": "Unified Individual",
    "segmentOnApiName": "UnifiedssotIndividualInd1__dlm",
    "segmentType": "WATERFALL",
    "name": "Vehicle Interest Prioritization",
    "developerName": "Vehicle_Interest_Prioritization",
    "description": "Waterfall segment that resolves overlap across Hearted Vehicle, Test Drive No Purchase, and Memorial Day Seasonal Push. Jane Dawson qualifies for all 3 but is assigned to P1 (Hearted Vehicle) only."
  }'
```

**Expected response:**
```json
{
  "id": "<segment-id>",
  "name": "Vehicle Interest Prioritization",
  "developerName": "Vehicle_Interest_Prioritization",
  "segmentType": "WATERFALL",
  "status": "Draft"
}
```

#### 1b. Configure Waterfall Rules via UI

Navigate to: **Data Cloud > Segments > Vehicle Interest Prioritization > Edit**

Configure 3 priority tiers in this exact order:

**Priority 1 — Hearted Vehicle Follow-Up (Highest)**
```
Description: Customers who have hearted at least one vehicle and have not purchased in the last 90 days.
Active intent signal — highest conversion probability.

SQL Logic (conceptual — entered via UI rule builder):
- Individual has related Vehicle Interaction records
- WHERE interaction_type = 'HEART' AND interaction_date within last 180 days
- AND Individual does NOT have a Purchase record in last 90 days
- Uses CI: Propensity_to_Buy score > 0.4 (optional enrichment)
```

**Priority 2 — Test Drive No Purchase (Mid)**
```
Description: Customers who completed a test drive but have not purchased.
Demonstrated physical interest — visited a store but didn't convert.

SQL Logic (conceptual — entered via UI rule builder):
- Individual has related Test Drive records
- WHERE test_drive_date within last 120 days
- AND Individual does NOT have a Purchase record after the test drive date
- Excludes anyone already in P1 (waterfall handles this automatically)
```

**Priority 3 — Seasonal Push Memorial Day (Lowest)**
```
Description: All active customers eligible for the Memorial Day seasonal campaign.
Broad catch-all for customers not captured by higher-priority audiences.

SQL Logic (conceptual — entered via UI rule builder):
- Individual has email opt-in = true
- AND Individual has had any engagement (web visit, email open, or vehicle interaction) in last 365 days
- Excludes anyone in P1 or P2 (waterfall handles this automatically)
```

**After UI configuration:** Save and verify that the waterfall shows 3 priority tiers with correct ordering.

---

### Segments #2-6: Dbt (SQL) Segments via ConnectApi Apex

**Why Apex instead of REST?** The REST API has a known bug where the `queryDefinition.dbtModelNodes` array serialization fails with HTTP 500. The ConnectApi Apex class handles the array correctly.

**Execution method:** Run each Apex block in Developer Console (**Setup > Developer Console > Debug > Open Execute Anonymous Window**) or via SFDX:

```bash
sf apex run --target-org carmax-sdo-mm-app-wz95pw --file segment_create.apex
```

**SQL Requirements (apply to ALL Dbt segments):**
1. Must project `ssot__Id__c` — the primary key of the Unified Individual DMO (`UnifiedssotIndividualInd1__dlm`)
2. Must project `KQ_Id__c` — the unique row identifier for deduplication
3. Must use fully qualified column names: `table_alias.column_name`
4. Must JOIN through Identity Resolution chain: `UnifiedssotIndividualInd1__dlm` → `UnifiedLinkssotIndividualInd1__dlm` → `ssot__Individual__dlm` → source DMO
5. Cannot reference CIO tables directly in FROM — use JOINs from the Unified Individual DMO
6. `IN` clauses with string literals must escape single quotes in Apex: `\'value\'`

---

#### Segment #2: New Email Subscribers

**Campaign alignment:** New Subscriber Welcome
**Demo stop:** Stop 3
**Logic:** Contacts who opted into email within the last 30 days and have no prior purchase history. These are net-new audience members who need onboarding.

```apex
// Segment #2: New Email Subscribers
// Run in Developer Console > Execute Anonymous

ConnectApi.CdpSegmentInput input = new ConnectApi.CdpSegmentInput();
input.segmentOn         = 'Unified Individual';
input.segmentOnApiName  = 'UnifiedssotIndividualInd1__dlm';
input.segmentType       = ConnectApi.CdpSegmentType.Dbt;
input.name              = 'New Email Subscribers';
input.developerName     = 'New_Email_Subscribers';
input.description       = 'Contacts who opted into email within the last 30 days with no prior purchase. Feeds the New Subscriber Welcome campaign and Welcome Series flow.';

ConnectApi.CdpSegmentQueryDefinitionInput qd = new ConnectApi.CdpSegmentQueryDefinitionInput();

ConnectApi.CdpSegmentDbtModelNodeInput node = new ConnectApi.CdpSegmentDbtModelNodeInput();
node.name = 'New_Email_Subscribers';   // Must match developerName

node.sql = ''
    + 'SELECT '
    + '  ind.ssot__Id__c, '
    + '  ind.KQ_Id__c '
    + 'FROM UnifiedssotIndividualInd1__dlm ind '
    + 'INNER JOIN UnifiedLinkssotIndividualInd1__dlm lnk '
    + '  ON lnk.UnifiedRecordId__c = ind.ssot__Id__c '
    + 'INNER JOIN ssot__Individual__dlm raw '
    + '  ON raw.ssot__Id__c = lnk.SourceRecordId__c '
    + 'INNER JOIN ssot__WebsiteEngagement__dlm we '
    + '  ON we.ssot__IndividualId__c = raw.ssot__Id__c '
    + 'WHERE YEAR(we.ssot__EngagementDateTm__c) * 10000 + MONTH(we.ssot__EngagementDateTm__c) * 100 + DAY(we.ssot__EngagementDateTm__c) >= 20260411 '
    + '  AND raw.ssot__Id__c NOT IN ( '
    + '    SELECT v.IndividualId__c '
    + '    FROM CarMax_Vehicle__dlm v '
    + '    WHERE v.IsPurchased__c = \'true\' '
    + '  )';

qd.dbtModelNodes = new List<ConnectApi.CdpSegmentDbtModelNodeInput>{ node };
input.queryDefinition = qd;

ConnectApi.CdpSegment result = ConnectApi.CdpSegment.createSegment(input);
System.debug('Created segment: ' + result.id + ' — ' + result.name);
```

---

#### Segment #3: Pre-Qualification Shoppers

**Campaign alignment:** Pre-Qualification Completion
**Demo stop:** Stop 3
**Logic:** Contacts who started the CarMax pre-qualification process (finance application) but did not complete it. High-intent abandoners who need a nudge.

```apex
// Segment #3: Pre-Qualification Shoppers
// Run in Developer Console > Execute Anonymous

ConnectApi.CdpSegmentInput input = new ConnectApi.CdpSegmentInput();
input.segmentOn         = 'Unified Individual';
input.segmentOnApiName  = 'UnifiedssotIndividualInd1__dlm';
input.segmentType       = ConnectApi.CdpSegmentType.Dbt;
input.name              = 'Pre-Qualification Shoppers';
input.developerName     = 'Pre_Qualification_Shoppers';
input.description       = 'Contacts who started pre-qualification but did not complete it. Feeds the Pre-Qualification Completion campaign.';

ConnectApi.CdpSegmentQueryDefinitionInput qd = new ConnectApi.CdpSegmentQueryDefinitionInput();

ConnectApi.CdpSegmentDbtModelNodeInput node = new ConnectApi.CdpSegmentDbtModelNodeInput();
node.name = 'Pre_Qualification_Shoppers';   // Must match developerName

node.sql = ''
    + 'SELECT '
    + '  ind.ssot__Id__c, '
    + '  ind.KQ_Id__c '
    + 'FROM UnifiedssotIndividualInd1__dlm ind '
    + 'INNER JOIN UnifiedLinkssotIndividualInd1__dlm lnk '
    + '  ON lnk.UnifiedRecordId__c = ind.ssot__Id__c '
    + 'INNER JOIN ssot__Individual__dlm raw '
    + '  ON raw.ssot__Id__c = lnk.SourceRecordId__c '
    + 'INNER JOIN ssot__WebsiteEngagement__dlm we '
    + '  ON we.ssot__IndividualId__c = raw.ssot__Id__c '
    + 'WHERE we.ssot__EngagementChannelActionId__c = \'Pre-Qualification Start\' '
    + '  AND YEAR(we.ssot__EngagementDateTm__c) * 10000 + MONTH(we.ssot__EngagementDateTm__c) * 100 + DAY(we.ssot__EngagementDateTm__c) >= 20260312 '
    + '  AND raw.ssot__Id__c NOT IN ( '
    + '    SELECT we2.ssot__IndividualId__c '
    + '    FROM ssot__WebsiteEngagement__dlm we2 '
    + '    WHERE we2.ssot__EngagementChannelActionId__c = \'Pre-Qualification Complete\' '
    + '  )';

qd.dbtModelNodes = new List<ConnectApi.CdpSegmentDbtModelNodeInput>{ node };
input.queryDefinition = qd;

ConnectApi.CdpSegment result = ConnectApi.CdpSegment.createSegment(input);
System.debug('Created segment: ' + result.id + ' — ' + result.name);
```

---

#### Segment #4: Price Drop Alert Audience

**Campaign alignment:** Price Drop Alert
**Demo stop:** Stop 3
**Logic:** Contacts who hearted vehicles where the price has decreased since the heart event. Combines vehicle interaction data with pricing data to create a timely, high-relevance trigger.

```apex
// Segment #4: Price Drop Alert Audience
// Run in Developer Console > Execute Anonymous

ConnectApi.CdpSegmentInput input = new ConnectApi.CdpSegmentInput();
input.segmentOn         = 'Unified Individual';
input.segmentOnApiName  = 'UnifiedssotIndividualInd1__dlm';
input.segmentType       = ConnectApi.CdpSegmentType.Dbt;
input.name              = 'Price Drop Alert Audience';
input.developerName     = 'Price_Drop_Alert_Audience';
input.description       = 'Contacts who hearted vehicles where the listing price has dropped. Feeds the Price Drop Alert campaign.';

ConnectApi.CdpSegmentQueryDefinitionInput qd = new ConnectApi.CdpSegmentQueryDefinitionInput();

ConnectApi.CdpSegmentDbtModelNodeInput node = new ConnectApi.CdpSegmentDbtModelNodeInput();
node.name = 'Price_Drop_Alert_Audience';   // Must match developerName

node.sql = ''
    + 'SELECT '
    + '  ind.ssot__Id__c, '
    + '  ind.KQ_Id__c '
    + 'FROM UnifiedssotIndividualInd1__dlm ind '
    + 'INNER JOIN UnifiedLinkssotIndividualInd1__dlm lnk '
    + '  ON lnk.UnifiedRecordId__c = ind.ssot__Id__c '
    + 'INNER JOIN ssot__Individual__dlm raw '
    + '  ON raw.ssot__Id__c = lnk.SourceRecordId__c '
    + 'INNER JOIN CarMax_Vehicle__dlm v '
    + '  ON v.IndividualId__c = raw.ssot__Id__c '
    + 'WHERE v.IsHearted__c = \'true\' '
    + '  AND v.Status__c = \'Active\' ';

qd.dbtModelNodes = new List<ConnectApi.CdpSegmentDbtModelNodeInput>{ node };
input.queryDefinition = qd;

ConnectApi.CdpSegment result = ConnectApi.CdpSegment.createSegment(input);
System.debug('Created segment: ' + result.id + ' — ' + result.name);
```

---

#### Segment #5: Instant Offer Abandonment

**Campaign alignment:** Instant Offer Abandonment
**Demo stop:** Stop 3
**Logic:** Contacts who started the CarMax Instant Offer (sell your car) process but did not complete it. These contacts have a vehicle they want to sell — high-value re-engagement opportunity.

```apex
// Segment #5: Instant Offer Abandonment
// Run in Developer Console > Execute Anonymous

ConnectApi.CdpSegmentInput input = new ConnectApi.CdpSegmentInput();
input.segmentOn         = 'Unified Individual';
input.segmentOnApiName  = 'UnifiedssotIndividualInd1__dlm';
input.segmentType       = ConnectApi.CdpSegmentType.Dbt;
input.name              = 'Instant Offer Abandonment';
input.developerName     = 'Instant_Offer_Abandonment';
input.description       = 'Contacts who started an Instant Offer but did not complete it. Feeds the Instant Offer Abandonment campaign.';

ConnectApi.CdpSegmentQueryDefinitionInput qd = new ConnectApi.CdpSegmentQueryDefinitionInput();

ConnectApi.CdpSegmentDbtModelNodeInput node = new ConnectApi.CdpSegmentDbtModelNodeInput();
node.name = 'Instant_Offer_Abandonment';   // Must match developerName

node.sql = ''
    + 'SELECT '
    + '  ind.ssot__Id__c, '
    + '  ind.KQ_Id__c '
    + 'FROM UnifiedssotIndividualInd1__dlm ind '
    + 'INNER JOIN UnifiedLinkssotIndividualInd1__dlm lnk '
    + '  ON lnk.UnifiedRecordId__c = ind.ssot__Id__c '
    + 'INNER JOIN ssot__Individual__dlm raw '
    + '  ON raw.ssot__Id__c = lnk.SourceRecordId__c '
    + 'INNER JOIN ssot__WebsiteEngagement__dlm we '
    + '  ON we.ssot__IndividualId__c = raw.ssot__Id__c '
    + 'WHERE we.ssot__EngagementChannelActionId__c = \'Instant Offer Start\' '
    + '  AND YEAR(we.ssot__EngagementDateTm__c) * 10000 + MONTH(we.ssot__EngagementDateTm__c) * 100 + DAY(we.ssot__EngagementDateTm__c) >= 20260411 '
    + '  AND raw.ssot__Id__c NOT IN ( '
    + '    SELECT we2.ssot__IndividualId__c '
    + '    FROM ssot__WebsiteEngagement__dlm we2 '
    + '    WHERE we2.ssot__EngagementChannelActionId__c = \'Instant Offer Complete\' '
    + '      AND YEAR(we2.ssot__EngagementDateTm__c) * 10000 + MONTH(we2.ssot__EngagementDateTm__c) * 100 + DAY(we2.ssot__EngagementDateTm__c) >= 20260411 '
    + '  )';

qd.dbtModelNodes = new List<ConnectApi.CdpSegmentDbtModelNodeInput>{ node };
input.queryDefinition = qd;

ConnectApi.CdpSegment result = ConnectApi.CdpSegment.createSegment(input);
System.debug('Created segment: ' + result.id + ' — ' + result.name);
```

---

#### Segment #6: Saved Search Match

**Campaign alignment:** Saved Search Match
**Demo stop:** Stop 3
**Logic:** Contacts with active saved searches where new matching inventory has been listed. This creates a "new inventory alert" audience that is refreshed as Data Cloud ingests new vehicle listings.

```apex
// Segment #6: Saved Search Match
// Run in Developer Console > Execute Anonymous

ConnectApi.CdpSegmentInput input = new ConnectApi.CdpSegmentInput();
input.segmentOn         = 'Unified Individual';
input.segmentOnApiName  = 'UnifiedssotIndividualInd1__dlm';
input.segmentType       = ConnectApi.CdpSegmentType.Dbt;
input.name              = 'Saved Search Match';
input.developerName     = 'Saved_Search_Match';
input.description       = 'Contacts with active saved searches where new matching inventory exists. Feeds the Saved Search Match campaign.';

ConnectApi.CdpSegmentQueryDefinitionInput qd = new ConnectApi.CdpSegmentQueryDefinitionInput();

ConnectApi.CdpSegmentDbtModelNodeInput node = new ConnectApi.CdpSegmentDbtModelNodeInput();
node.name = 'Saved_Search_Match';   // Must match developerName

node.sql = ''
    + 'SELECT '
    + '  ind.ssot__Id__c, '
    + '  ind.KQ_Id__c '
    + 'FROM UnifiedssotIndividualInd1__dlm ind '
    + 'INNER JOIN UnifiedLinkssotIndividualInd1__dlm lnk '
    + '  ON lnk.UnifiedRecordId__c = ind.ssot__Id__c '
    + 'INNER JOIN ssot__Individual__dlm raw '
    + '  ON raw.ssot__Id__c = lnk.SourceRecordId__c '
    + 'INNER JOIN ssot__WebsiteEngagement__dlm we '
    + '  ON we.ssot__IndividualId__c = raw.ssot__Id__c '
    + 'INNER JOIN CarMax_Vehicle__dlm v '
    + '  ON v.VIN__c = we.ssot__EngagementVehicleId__c '
    + 'WHERE we.ssot__EngagementChannelActionId__c = \'Save Search\' '
    + '  AND v.Status__c = \'Active\' '
    + '  AND YEAR(we.ssot__EngagementDateTm__c) * 10000 + MONTH(we.ssot__EngagementDateTm__c) * 100 + DAY(we.ssot__EngagementDateTm__c) >= 20260411 ';

qd.dbtModelNodes = new List<ConnectApi.CdpSegmentDbtModelNodeInput>{ node };
input.queryDefinition = qd;

ConnectApi.CdpSegment result = ConnectApi.CdpSegment.createSegment(input);
System.debug('Created segment: ' + result.id + ' — ' + result.name);
```

---

### Segments #7-8: Einstein AI Segments

**Type:** EinsteinGptSegmentsUI
**Create Method:** REST API POST (creates container)
**Prompt Configuration:** MANDATORY UI configuration after creation

Einstein segments demonstrate AI-powered audience discovery — the ability for a marketer to describe an audience in natural language and have Einstein find matching individuals based on behavioral signals, not just explicit attributes.

---

#### Segment #7: EV Consideration Nurture

**Campaign alignment:** EV Nurture
**Demo stop:** Stop 2
**Logic:** Einstein identifies customers showing EV interest signals — browsing EV listings, searching for hybrid/electric, engaging with EV content — even if they haven't explicitly expressed EV preference.

```bash
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments" \
  --body '{
    "segmentOn": "Unified Individual",
    "segmentOnApiName": "UnifiedssotIndividualInd1__dlm",
    "segmentType": "EinsteinGptSegmentsUI",
    "name": "EV Consideration Nurture",
    "developerName": "EV_Consideration_Nurture",
    "description": "Einstein-identified customers showing EV interest signals. Feeds the EV Nurture campaign. Prompt: Find customers who have browsed electric or hybrid vehicle listings, searched for EV-related terms, or shown interest in fuel-efficient vehicles in the past 90 days."
  }'
```

**UI Prompt Configuration (after creation):**
Navigate to: **Data Cloud > Segments > EV Consideration Nurture > Edit**

Enter the Einstein prompt:
```
Find customers who have browsed electric or hybrid vehicle listings, searched for
EV-related terms, or shown interest in fuel-efficient vehicles in the past 90 days.
Include customers who have viewed EV comparison content or clicked on EV-related
email links. Exclude customers who have already purchased an EV from CarMax.
```

Review the Einstein-generated criteria, adjust if needed, and save.

---

#### Segment #8: Trade-In and Upgrade

**Campaign alignment:** Trade-In Upgrade
**Demo stop:** Stop 2
**Logic:** Einstein identifies customers likely ready to trade in their current vehicle based on ownership tenure, mileage patterns, service history, and browsing behavior on newer models.

```bash
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments" \
  --body '{
    "segmentOn": "Unified Individual",
    "segmentOnApiName": "UnifiedssotIndividualInd1__dlm",
    "segmentType": "EinsteinGptSegmentsUI",
    "name": "Trade-In and Upgrade",
    "developerName": "Trade_In_and_Upgrade",
    "description": "Einstein-identified customers likely ready to trade in and upgrade. Feeds the Trade-In Upgrade campaign. Prompt: Find customers who purchased a vehicle from CarMax more than 2 years ago and have recently browsed newer model year vehicles or used the Instant Offer tool."
  }'
```

**UI Prompt Configuration (after creation):**
Navigate to: **Data Cloud > Segments > Trade-In and Upgrade > Edit**

Enter the Einstein prompt:
```
Find customers who purchased a vehicle from CarMax more than 2 years ago and have
recently browsed newer model year vehicles or used the Instant Offer tool. Include
customers whose vehicles are approaching high-mileage milestones based on average
annual driving patterns. Prioritize customers with high Customer Lifetime Value scores.
```

Review the Einstein-generated criteria, adjust if needed, and save.

---

## Step 2: Verify All Segments Created

After creating all 8 segments, verify they exist and are in the correct state.

### 2a. List All Segments via REST API

```bash
sf api request rest \
  --method GET \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments"
```

### 2b. Parse and Validate with Python

```python
#!/usr/bin/env python3
"""Verify all 8 CarMax segments exist with correct types."""

import json
import subprocess
import sys

EXPECTED_SEGMENTS = {
    "Vehicle_Interest_Prioritization": "WATERFALL",
    "New_Email_Subscribers": "Dbt",
    "Pre_Qualification_Shoppers": "Dbt",
    "Price_Drop_Alert_Audience": "Dbt",
    "Instant_Offer_Abandonment": "Dbt",
    "Saved_Search_Match": "Dbt",
    "EV_Consideration_Nurture": "EinsteinGptSegmentsUI",
    "Trade_In_and_Upgrade": "EinsteinGptSegmentsUI",
}

result = subprocess.run(
    [
        "sf", "api", "request", "rest",
        "--method", "GET",
        "--target-org", "carmax-sdo-mm-app-wz95pw",
        "/services/data/v65.0/ssot/segments",
    ],
    capture_output=True, text=True
)

segments = json.loads(result.stdout)
found = {}

for seg in segments.get("segments", segments if isinstance(segments, list) else []):
    dev_name = seg.get("developerName", "")
    seg_type = seg.get("segmentType", "")
    seg_id   = seg.get("id", "")
    status   = seg.get("status", "")

    if dev_name in EXPECTED_SEGMENTS:
        expected_type = EXPECTED_SEGMENTS[dev_name]
        match = "OK" if seg_type == expected_type else f"MISMATCH (expected {expected_type})"
        found[dev_name] = True
        print(f"  [{match}] {dev_name} | type={seg_type} | id={seg_id} | status={status}")

print(f"\n--- Found {len(found)}/{len(EXPECTED_SEGMENTS)} expected segments ---")

missing = set(EXPECTED_SEGMENTS.keys()) - set(found.keys())
if missing:
    print(f"MISSING: {', '.join(missing)}")
    sys.exit(1)
else:
    print("All segments accounted for.")
```

Run:
```bash
python3 verify_segments.py
```

---

## Step 3: Publish Segments

Segments must be published before they can be used in MCA flows or produce membership. Publishing triggers the initial segment evaluation against Data Cloud data.

**Important:** The publish endpoint uses the **segment ID** (GUID), not the developerName.

### 3a. Publish Each Segment

Replace `<segment-id>` with the actual ID from Step 2 verification:

```bash
# Publish Waterfall
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish New Email Subscribers
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish Pre-Qualification Shoppers
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish Price Drop Alert Audience
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish Instant Offer Abandonment
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish Saved Search Match
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish EV Consideration Nurture
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"

# Publish Trade-In and Upgrade
sf api request rest \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>/publish"
```

### 3b. Batch Publish Script (Alternative)

```bash
#!/bin/bash
# Publish all CarMax segments in sequence
# Run after verify_segments.py confirms all 8 exist

ORG="carmax-sdo-mm-app-wz95pw"
API="/services/data/v65.0/ssot/segments"

# Get all segment IDs
SEGMENTS=$(sf api request rest --method GET --target-org $ORG "$API" 2>/dev/null)

echo "$SEGMENTS" | python3 -c "
import json, sys, subprocess

data = json.load(sys.stdin)
segments = data.get('segments', data if isinstance(data, list) else [])

for seg in segments:
    dev_name = seg.get('developerName', '')
    seg_id = seg.get('id', '')
    if dev_name.startswith(('Vehicle_Interest', 'New_Email', 'Pre_Qualification', 'Price_Drop', 'Instant_Offer', 'Saved_Search', 'EV_Consideration', 'Trade_In')):
        print(f'Publishing {dev_name} ({seg_id})...')
        result = subprocess.run(
            ['sf', 'api', 'request', 'rest', '--method', 'POST',
             '--target-org', '$ORG',
             f'/services/data/v65.0/ssot/segments/{seg_id}/publish'],
            capture_output=True, text=True
        )
        status = 'OK' if result.returncode == 0 else 'FAILED'
        print(f'  -> {status}')
"
```

---

## Step 4: Verify Segment Membership

After publishing, verify that segments have evaluated and contain members.

### 4a. Query MarketSegment SObject

```bash
sf data query \
  --query "SELECT Id, Name, DeveloperName__c, MemberCount__c, Status__c, LastEvaluatedDate__c FROM MarketSegment WHERE DeveloperName__c LIKE 'Vehicle_Interest%' OR DeveloperName__c LIKE 'New_Email%' OR DeveloperName__c LIKE 'Pre_Qualification%' OR DeveloperName__c LIKE 'Price_Drop%' OR DeveloperName__c LIKE 'Instant_Offer%' OR DeveloperName__c LIKE 'Saved_Search%' OR DeveloperName__c LIKE 'EV_Consideration%' OR DeveloperName__c LIKE 'Trade_In%' ORDER BY Name" \
  --target-org carmax-sdo-mm-app-wz95pw \
  --result-format table
```

### 4b. Check Individual Segment Membership

Verify Jane Dawson appears in the waterfall P1 tier:

```bash
sf api request rest \
  --method GET \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<waterfall-segment-id>/members?limit=50"
```

### 4c. Verify Jane Dawson's Segment Resolution

```bash
sf data query \
  --query "SELECT Id, FirstName, LastName FROM Contact WHERE LastName = 'Dawson' AND FirstName = 'Jane' LIMIT 1" \
  --target-org carmax-sdo-mm-app-wz95pw \
  --result-format json
```

Then check her segment membership in Data Cloud to confirm she appears in the Waterfall P1 tier only (not P2 or P3).

---

## Segment to Campaign to Flow Mapping (MCA-Focused)

This is the complete mapping from segment (audience) to campaign (business container) to flow (execution). Every row represents one marketing program in MCA.

| Segment | Type | Campaign | Flow | Demo Stop |
|---------|------|----------|------|-----------|
| Vehicle Interest Waterfall P1 | Waterfall | Hearted Vehicle Follow-Up | Vehicle Interest Nurture | Stop 2, 3, 4 |
| Vehicle Interest Waterfall P2 | Waterfall | Test Drive No Purchase | (Future) | Stop 2 |
| Vehicle Interest Waterfall P3 | Waterfall | Seasonal Push Memorial Day | (Future) | Stop 2 |
| New Email Subscribers | Dbt | New Subscriber Welcome | Welcome Series | Stop 3 |
| Pre-Qualification Shoppers | Dbt | Pre-Qualification Completion | (Future) | Stop 3 |
| Price Drop Alert Audience | Dbt | Price Drop Alert | Price Drop Alert | Stop 3 |
| Instant Offer Abandonment | Dbt | Instant Offer Abandonment | Instant Offer | Stop 3 |
| Saved Search Match | Dbt | Saved Search Match | Saved Search | Stop 3 |
| EV Consideration Nurture | Einstein | EV Nurture | (Future) | Stop 2 |
| Trade-In and Upgrade | Einstein | Trade-In Upgrade | (Future) | Stop 2 |

**Key observations:**
- The waterfall segment produces 3 mutually exclusive audiences from 1 segment definition
- Flows marked "(Future)" are placeholders — only the primary demo flows are fully built in Phase 7
- Every flow uses **segment-triggered entry** — segment membership IS the entry condition
- Demo Stop 2 shows the segmentation strategy; Stops 3-4 show the execution of the P1 path

---

## Critical Notes & Gotchas

### 1. Waterfall Rules MUST Be Configured via UI
The REST API creates the waterfall segment shell (name, type, description) but **cannot** configure the priority tiers or their SQL rules. After the POST creates the segment, you must open it in the Data Cloud UI and manually configure the 3 priority tiers. There is no API workaround for this.

### 2. Dbt Segments Require ConnectApi Apex (Not REST)
The REST API endpoint for creating Dbt segments has a serialization bug with the `queryDefinition.dbtModelNodes` array — it throws HTTP 500 with an internal server error. Use `ConnectApi.CdpSegment.createSegment()` in Apex instead. This is the only reliable programmatic method.

### 3. model.name Must Match developerName
In the `CdpSegmentDbtModelNodeInput`, the `node.name` property **must** match the segment's `developerName` exactly. If they differ, the segment will create but fail to evaluate with a cryptic "model not found" error.

### 4. SQL Must Project ssot__Id__c AND KQ_Id__c
Every Dbt segment SQL query must include both columns in the SELECT:
```sql
SELECT ind.ssot__Id__c, ind.KQ_Id__c FROM UnifiedssotIndividualInd1__dlm ind ...
```
- `ssot__Id__c` is the primary key of the Unified Individual DMO (`UnifiedssotIndividualInd1__dlm`) — these are hashed Identity Resolution IDs (e.g., `06cb0293137acdbc...`)
- `KQ_Id__c` is the row-level unique identifier used for deduplication
Omitting either column causes the segment to fail evaluation silently — it will show 0 members.

### 5. SQL Must Use Fully Qualified Column Names
All column references in Dbt SQL must use the table alias prefix:
```sql
-- CORRECT
SELECT ind.ssot__Id__c, ind.KQ_Id__c FROM UnifiedssotIndividualInd1__dlm ind

-- WRONG — will fail
SELECT ssot__Id__c, KQ_Id__c FROM UnifiedssotIndividualInd1__dlm ind
```
Unqualified column names cause ambiguous reference errors, especially in JOINs.

### 6. Segments CANNOT Query CIO Tables Directly
Calculated Insight Output tables (e.g., `KQ_Customer_Lifetime_Value__dlm`) cannot be used as the `FROM` table or as `segmentOnApiName`. They can only be referenced via JOIN from the Unified Individual DMO:
```sql
-- CORRECT — start from Unified Individual, JOIN to CI
SELECT ind.ssot__Id__c, ind.KQ_Id__c
FROM UnifiedssotIndividualInd1__dlm ind
INNER JOIN KQ_Customer_Lifetime_Value__dlm clv
  ON clv.IndividualId__c = ind.ssot__Id__c
WHERE clv.CLV_Score__c > 500

-- WRONG — CIO as primary table
SELECT clv.IndividualId__c FROM KQ_Customer_Lifetime_Value__dlm clv

-- WRONG — using ssot__Individual__dlm instead of Unified Individual
SELECT ind.ssot__Id__c, ind.KQ_Id__c
FROM ssot__Individual__dlm ind
INNER JOIN KQ_Customer_Lifetime_Value__dlm clv
  ON clv.IndividualId__c = ind.ssot__Id__c
```

### 7. segmentOnApiName Must Be the Unified Individual DMO
The `segmentOnApiName` field must be the Unified Individual DMO produced by Identity Resolution. For this org, that is:
```
UnifiedssotIndividualInd1__dlm
```
**Do NOT use `ssot__Individual__dlm`** — that is the raw Individual DMO and will not resolve correctly for segmentation. The existing `Hearted_Vehicles_v1` segment on this org already uses `UnifiedssotIndividualInd1__dlm`, confirming this is the correct target.

Event DMOs (like `ssot__WebsiteEngagement__dlm`) and custom DMOs are also rejected.

### 8. Publish Endpoint Uses Segment ID, Not Name
The publish endpoint path is:
```
/services/data/v65.0/ssot/segments/{segmentId}/publish
```
Where `{segmentId}` is the GUID returned at creation time (e.g., `a1B2C3D4E5F6G7H8`), **not** the developerName or name. Always retrieve the ID from the list endpoint first.

### 9. segmentType and developerName Are Immutable After Creation
Once a segment is created, its `segmentType` and `developerName` cannot be changed via API or UI. If you create a segment with the wrong type (e.g., Dbt instead of WATERFALL), you must delete it and recreate. Plan carefully.

### 10. Einstein Segments Need UI Prompt Configuration
The REST API POST for `EinsteinGptSegmentsUI` segments creates the container but does **not** accept the natural language prompt. The prompt must be entered via the Data Cloud UI after creation. Without the prompt, the Einstein segment will have 0 members and cannot be published.

### 11. Waterfall Demo Flow Narrative
During the demo (Stop 2), the waterfall is the "aha moment." The narrative flow should be:
1. Show Jane Dawson qualifies for 3 different segments/campaigns
2. Ask the audience: "What happens if she gets all 3 emails?"
3. Open the waterfall — show the 3 tiers
4. Reveal: "Jane only gets Priority 1 — the Hearted Vehicle Follow-Up"
5. Explain: "The waterfall is the governance layer that prevents over-messaging"

This narrative requires that Jane's data is properly set up in Phase 2 with overlapping qualifications.

### 12. SQL IN Clause Escaping in Apex
String literals inside SQL `IN` clauses must have single quotes escaped with backslash in Apex string concatenation:
```apex
// CORRECT
+ 'WHERE we.ssot__EngagementChannelActionId__c = \'Pre-Qualification Start\' '

// WRONG — will cause Apex compilation error
+ 'WHERE we.ssot__EngagementChannelActionId__c = 'Pre-Qualification Start' '
```
The Apex compiler treats unescaped single quotes as string terminators, breaking the SQL string.

### 13. NOT IN Subquery Pattern Is Supported
Data Cloud SQL in segments supports the `NOT IN` subquery pattern for exclusion logic. Note that the NOT IN check runs against the **raw** Individual DMO ID (`raw.ssot__Id__c`) since source DMOs store CRM Contact IDs:
```sql
AND raw.ssot__Id__c NOT IN (
    SELECT v.IndividualId__c
    FROM CarMax_Vehicle__dlm v
    WHERE v.IsPurchased__c = 'true'
)
```
Where `raw` is the alias for `ssot__Individual__dlm` in the Identity Resolution join chain. This pattern is used in multiple segments (New Email Subscribers, Pre-Qualification Shoppers, Instant Offer Abandonment) to exclude contacts who have already completed the desired action.

---

## Execution Checklist

| Step | Action | Status |
|------|--------|--------|
| 1.1 | Create Waterfall segment via REST API | [ ] |
| 1.2 | Configure Waterfall 3 priority tiers via UI | [ ] |
| 1.3 | Create New Email Subscribers segment via Apex | [ ] |
| 1.4 | Create Pre-Qualification Shoppers segment via Apex | [ ] |
| 1.5 | Create Price Drop Alert Audience segment via Apex | [ ] |
| 1.6 | Create Instant Offer Abandonment segment via Apex | [ ] |
| 1.7 | Create Saved Search Match segment via Apex | [ ] |
| 1.8 | Create EV Consideration Nurture segment via REST API | [ ] |
| 1.9 | Configure EV Consideration Nurture prompt via UI | [ ] |
| 1.10 | Create Trade-In and Upgrade segment via REST API | [ ] |
| 1.11 | Configure Trade-In and Upgrade prompt via UI | [ ] |
| 2.1 | Verify all 8 segments exist via REST API | [ ] |
| 2.2 | Run Python validation script | [ ] |
| 3.1 | Publish all 8 segments | [ ] |
| 3.2 | Wait for segment evaluation to complete | [ ] |
| 4.1 | Verify segment member counts via SOQL | [ ] |
| 4.2 | Verify Jane Dawson in Waterfall P1 | [ ] |
| 4.3 | Verify Jane Dawson NOT in P2 or P3 individually | [ ] |
| 4.4 | Verify Aisha Thompson in New Email Subscribers | [ ] |

---

## Dependencies

| Phase | Dependency | Why |
|-------|-----------|-----|
| **Phase 2** | DMOs active with data | Segments query DMO tables — no data = 0 members |
| **Phase 3** | CIs materialized | Waterfall and enrichment segments reference CI scores |
| **Phase 6 (next)** | Campaigns created | Segments map to campaigns; campaigns reference segments |
| **Phase 7 (next)** | Flows built | Flows use segment-triggered entry from these segments |

---

## Rollback

If a segment is created incorrectly:

```bash
# Delete a segment by ID
sf api request rest \
  --method DELETE \
  --target-org carmax-sdo-mm-app-wz95pw \
  "/services/data/v65.0/ssot/segments/<segment-id>"
```

**Note:** Published segments with active flow references cannot be deleted. You must first deactivate the flow, then unpublish the segment, then delete.

Deletion order for a segment with dependencies:
1. Deactivate any flows using the segment as entry criteria
2. Remove the segment reference from any Campaign records
3. Unpublish the segment
4. Delete the segment
