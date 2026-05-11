# Phase 6: Campaigns & Campaign Briefs — Implementation Plan

## Overview

Create 10 Campaign records and their associated Campaign Briefs to support the MCA demo's AI-powered campaign creation workflow. In MCA, the campaign lifecycle starts with a **Campaign Brief** — an AI-generated specification that captures audience, channels, messaging, and success metrics. Campaign Agent (Demo Stop 1) generates these briefs from natural language prompts.

**Why this phase was refactored (v1 vs v2):**
The original Phase 2 treated Campaign SObjects and CampaignMember records as the primary artifact — essentially recreating the MC Engagement model inside Salesforce Core. In v2, campaigns are REPOSITIONED as marketing constructs that complement the MCA workflow. The Campaign Brief Builder (`DICE_CBB`) is the new centerpiece. Campaign records become organizational containers; Campaign Briefs become the AI-generated specs that drive content creation. CampaignMember assignments are retained for demo convenience but explicitly de-emphasized.

**The MCA Campaign Workflow:**
1. Marketer describes business intent in natural language
2. Campaign Agent generates a Campaign Brief (audience, channels, messaging, KPIs)
3. Brief connects to a Campaign record for organizational tracking
4. Segments (Phase 5) provide the audience — they are NOT derived from Campaign records
5. Content (Phase 7) is created based on the brief's messaging specs
6. Flows (Phase 8) use segments as entry criteria, not campaigns

**Org:** `carmax-sdo-mm-app-wz95pw`
**Prerequisite:** Phase 5 complete (Segments published with members)

---

## MCA Context: Campaigns in MCA vs MC Engagement

| Aspect | MC Engagement | MCA (Marketing Cloud Advanced) |
|--------|--------------|-------------------------------|
| Audience source | Lists, Data Extensions | Data Cloud Segments |
| Journey entry | List membership | Segment membership (segment-triggered flows) |
| Campaign creation | Manual setup in Marketing Cloud | Campaign Agent AI generates brief |
| Campaign brief | N/A | `DICE_CBB_CampaignBrief__c` — structured AI output |
| Content linkage | Via Journey Builder data | Via Data Graph + CMS |
| Overlap resolution | Manual exclusion rules | Waterfall segment (automatic) |

**Key reframe:** In MCA, segments are the audience engine (Phase 5). Campaigns are organizational containers that connect briefs, content, and reporting. Campaign Briefs are the AI-generated specs that drive content creation. CampaignMember assignments are OPTIONAL — kept for demo purposes but de-emphasized.

---

## Step 1: Create Campaign Records

Each campaign is created as a standard Salesforce Campaign record. These serve as organizational containers — the actual targeting and orchestration happens through segments and flows.

### 1A: Create All 10 Campaigns

```bash
# Campaign 1: Hearted Vehicle Follow-Up
sf data create record --sobject Campaign \
  --values "Name='Hearted Vehicle Follow-Up' Type='Email' Status='Active' IsActive=true Description='Re-engage customers who have hearted vehicles but not purchased. Triggered by Vehicle Interest Waterfall segment P1.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 2: Test Drive - No Purchase Nurture
sf data create record --sobject Campaign \
  --values "Name='Test Drive - No Purchase Nurture' Type='Email' Status='Active' IsActive=true Description='Nurture customers who completed a test drive but did not purchase. Triggered by Vehicle Interest Waterfall segment P2.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 3: New Email Subscriber Welcome
sf data create record --sobject Campaign \
  --values "Name='New Email Subscriber Welcome' Type='Email' Status='Active' IsActive=true Description='Welcome series for newly subscribed email contacts. Triggered by New Email Subscribers segment.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 4: Pre-Qualification Completion
sf data create record --sobject Campaign \
  --values "Name='Pre-Qualification Completion' Type='Email' Status='Active' IsActive=true Description='Follow-up for customers who completed online pre-qualification. Encourage next steps toward purchase.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 5: Price Drop Alert
sf data create record --sobject Campaign \
  --values "Name='Price Drop Alert' Type='Email' Status='Active' IsActive=true Description='Alert customers when a vehicle they have viewed or hearted drops in price. Real-time trigger.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 6: Saved Search Match
sf data create record --sobject Campaign \
  --values "Name='Saved Search Match' Type='Email' Status='Active' IsActive=true Description='Notify customers when new inventory matches their saved search criteria.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 7: Trade-In and Upgrade
sf data create record --sobject Campaign \
  --values "Name='Trade-In and Upgrade' Type='Email' Status='Active' IsActive=true Description='Target owners of aging vehicles with trade-in offers and upgrade incentives. Einstein-segmented audience.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 8: EV Consideration Nurture
sf data create record --sobject Campaign \
  --values "Name='EV Consideration Nurture' Type='Email' Status='Active' IsActive=true Description='Educate and nurture customers showing interest in electric vehicles. Einstein-segmented audience.'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 9: Seasonal Push - Memorial Day
sf data create record --sobject Campaign \
  --values "Name='Seasonal Push - Memorial Day' Type='Multi-Channel' Status='Planned' IsActive=true Description='Memorial Day weekend promotion. Multi-channel: email, SMS, digital. Triggered by Vehicle Interest Waterfall segment P3 (catch-all).'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Campaign 10: Instant Offer Abandonment
sf data create record --sobject Campaign \
  --values "Name='Instant Offer Abandonment' Type='Email' Status='Active' IsActive=true Description='Re-engage customers who started but did not complete the Instant Offer (sell/trade) flow.'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

### 1B: Verify Campaign Creation

```bash
sf data query --query "SELECT Id, Name, Type, Status, IsActive FROM Campaign ORDER BY Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Expected: 10 Campaign records. Save the IDs — they are needed in Step 2 (Brief linkage) and Step 3 (CampaignMember creation).

---

## Step 2: Create Campaign Briefs (MCA-Native)

This is the NEW content that makes this phase MCA-focused. Campaign Brief Builder (`DICE_CBB`) is a managed package that ships with MCA-enabled SDO orgs. It provides the `DICE_CBB_CampaignBrief__c` object, which Campaign Agent uses to store AI-generated campaign specifications.

### Campaign Brief Builder Data Model

**Object:** `DICE_CBB_CampaignBrief__c` (managed, from DICE_CBB package)

| Field API Name | Type | Purpose |
|----------------|------|---------|
| `Name` | Text | Brief title |
| `DICE_CBB_Brand_Voice__c` | Long Text | Tone/voice guidelines for content generation |
| `DICE_CBB_Campaign__c` | Lookup(Campaign) | Links brief to its Campaign container |
| `DICE_CBB_Channels__c` | Picklist (Multi) | Target channels (Email, SMS, Digital, etc.) |
| `DICE_CBB_Description__c` | Long Text | Brief description / executive summary |
| `DICE_CBB_End_Date__c` | Date | Campaign end date |
| `DICE_CBB_Launch_Date__c` | Date | Campaign launch date |
| `DICE_CBB_Product_Focus__c` | Text | Product/service being marketed |
| `DICE_CBB_Headlines_and_Captions__c` | Long Text | Headline options for email/ad creative |
| `DICE_CBB_Key_Messages__c` | Long Text | Core messaging pillars |
| `DICE_CBB_Objectives__c` | Long Text | Campaign objectives and goals |
| `DICE_CBB_Status__c` | Picklist | Brief status (Draft, In Review, Approved, etc.) |
| `DICE_CBB_Subject_Line_Options__c` | Long Text | Email subject line variants |
| `DICE_CBB_Success_Metrics__c` | Long Text | KPIs and success criteria |
| `DICE_CBB_Target_Audience__c` | Long Text | Audience definition (references segments) |
| `DICE_CBB_CTAs__c` | Long Text | Call-to-action options |
| `DICE_CBB_Body_Copy_Variants__c` | Long Text | Body copy alternatives for A/B testing |
| `DICE_CBB_Updated_By__c` | Lookup(User) | Last modified by |
| `DICE_CBB_Updated_Date__c` | DateTime | Last modified date |

### 2A: Verify Campaign Brief Builder is Installed

```bash
# Check if the DICE_CBB managed package is present
sf data query --query "SELECT Id, Name FROM DICE_CBB_CampaignBrief__c LIMIT 1" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**If the query returns an error** (e.g., "sObject type 'DICE_CBB_CampaignBrief__c' is not supported"), the DICE_CBB package is not installed. In that case:
- Skip Step 2 entirely
- Campaign records from Step 1 still work — they provide the organizational container
- Campaign Agent may generate briefs differently (or store them in a different location) without the DICE_CBB package
- Document the absence and proceed to Step 3

**If the query succeeds** (returns 0 or more rows), proceed with brief creation.

### 2B: Get Required IDs

```bash
# Get the current user ID (for Updated_By field)
sf data query --query "SELECT Id, Name FROM User WHERE IsActive = true AND Profile.Name = 'System Administrator' LIMIT 1" \
  --target-org carmax-sdo-mm-app-wz95pw

# Get Campaign IDs for brief linkage
sf data query --query "SELECT Id, Name FROM Campaign WHERE Name IN ('Hearted Vehicle Follow-Up','Test Drive - No Purchase Nurture','New Email Subscriber Welcome','Price Drop Alert') ORDER BY Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Save these IDs as variables:
- `ADMIN_USER_ID` — the System Administrator user ID
- `CAMPAIGN_HEARTED_ID` — Hearted Vehicle Follow-Up campaign ID
- `CAMPAIGN_TESTDRIVE_ID` — Test Drive - No Purchase Nurture campaign ID
- `CAMPAIGN_WELCOME_ID` — New Email Subscriber Welcome campaign ID
- `CAMPAIGN_PRICEDROP_ID` — Price Drop Alert campaign ID

### 2C: Create the Flagship Campaign Brief — Hearted Vehicle Re-Engagement

This is the primary brief. It is the one that Demo Stop 1 (Campaign Agent) will reference, and it drives the flagship email in Demo Stop 3.

```bash
sf data create record --sobject DICE_CBB_CampaignBrief__c \
  --values "Name='Hearted Vehicle Re-Engagement Brief' \
DICE_CBB_Brand_Voice__c='Warm, helpful, customer-first. CarMax tone: confident but not pushy. We are on the customers side — no haggling, no pressure. Use conversational language. Avoid salesy urgency tactics. Emphasize transparency and the Love Your Car Guarantee.' \
DICE_CBB_Campaign__c='CAMPAIGN_HEARTED_ID' \
DICE_CBB_Channels__c='Email;Digital' \
DICE_CBB_Description__c='Re-engage customers who have hearted at least one vehicle on carmax.com but have not completed a purchase. This campaign uses the Vehicle Interest Waterfall P1 segment to target the highest-intent browsers. The goal is to resurface their saved favorites, highlight availability, and provide a clear path to test drive or pre-qualification.' \
DICE_CBB_Launch_Date__c='2026-05-15' \
DICE_CBB_End_Date__c='2026-06-30' \
DICE_CBB_Product_Focus__c='Used Vehicle Sales' \
DICE_CBB_Headlines_and_Captions__c='Your favorites are still on the lot\nStill thinking about that {{Vehicle_Make}} {{Vehicle_Model}}?\nReady to take the next step?\nYour hearted vehicles, one click away' \
DICE_CBB_Key_Messages__c='Your hearted vehicles are still available\nSchedule a test drive in minutes — online or in-store\nGet pre-qualified with no credit impact in as little as 2 minutes\nLove Your Car Guarantee: 30-day money-back, no questions asked\nEvery CarMax vehicle comes with a full 150-point inspection' \
DICE_CBB_Objectives__c='Drive hearted-vehicle customers back to their saved listings\nIncrease test drive bookings by 20% among hearted-vehicle segment\nConvert browser intent to showroom visits\nReinforce the CarMax value proposition (no-haggle, guarantee) at the consideration stage' \
DICE_CBB_Status__c='Draft' \
DICE_CBB_Subject_Line_Options__c='Your favorites are waiting, {{FirstName}}\nStill thinking about that {{Vehicle_Make}}?\nCompare your top picks side by side\nYour {{Vehicle_Make}} {{Vehicle_Model}} is still available\nDont let your favorites get away' \
DICE_CBB_Success_Metrics__c='Email open rate > 35%\nClick-to-listing rate > 12%\nTest drive booking rate > 5%\nPre-qualification start rate > 8%\nConversion to purchase within 30 days > 3%' \
DICE_CBB_Target_Audience__c='Customers who have hearted at least 1 vehicle on carmax.com but have not completed a purchase in the last 90 days. Sourced from Data Cloud segment: Vehicle Interest Waterfall — Priority 1 (Hearted Vehicle). Estimated audience size: ~45,000 unified individuals. Exclusions: customers with an open finance application, customers who purchased in the last 30 days.' \
DICE_CBB_CTAs__c='View Your Favorites\nSchedule a Test Drive\nGet Pre-Qualified\nCompare Your Top Picks' \
DICE_CBB_Body_Copy_Variants__c='VARIANT A (Conversational):\nHi {{FirstName}}, we noticed you have been eyeing some great vehicles. Good news — they are still available and waiting for you. Whether you are ready to schedule a test drive or just want to browse your favorites again, we have made it easy. Plus, every CarMax vehicle comes with our Love Your Car Guarantee.\n\nVARIANT B (Urgency-lite):\n{{FirstName}}, your hearted vehicles are still on the lot — but inventory moves fast. Take another look at your favorites, compare them side by side, or take the next step with a free, no-impact pre-qualification. With CarMax, there is no haggling and no pressure — just a great car-buying experience.' \
DICE_CBB_Updated_By__c='ADMIN_USER_ID' \
DICE_CBB_Updated_Date__c='2026-05-09T12:00:00Z'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

> **Important:** Replace `CAMPAIGN_HEARTED_ID` and `ADMIN_USER_ID` with actual IDs from Step 2B before running.

### 2D: Create Additional Campaign Briefs

Create briefs for 2-3 more key campaigns. These are less critical for the demo but show breadth and support secondary demo stops.

#### Brief 2: Test Drive Follow-Up

```bash
sf data create record --sobject DICE_CBB_CampaignBrief__c \
  --values "Name='Test Drive Follow-Up Brief' \
DICE_CBB_Brand_Voice__c='Warm, helpful, customer-first. CarMax tone: confident but not pushy.' \
DICE_CBB_Campaign__c='CAMPAIGN_TESTDRIVE_ID' \
DICE_CBB_Channels__c='Email' \
DICE_CBB_Description__c='Follow up with customers who completed a test drive but did not purchase. Reinforce the positive test drive experience and reduce purchase friction.' \
DICE_CBB_Launch_Date__c='2026-05-15' \
DICE_CBB_End_Date__c='2026-06-30' \
DICE_CBB_Product_Focus__c='Used Vehicle Sales' \
DICE_CBB_Key_Messages__c='How was your test drive?\nStill have questions? We have answers.\nYour test-driven vehicle is still available\nPre-qualify in minutes with no credit impact\n24-hour test drives available' \
DICE_CBB_Objectives__c='Convert test drive completers to purchasers\nReduce time between test drive and purchase decision\nAddress common post-test-drive objections' \
DICE_CBB_Status__c='Draft' \
DICE_CBB_Subject_Line_Options__c='How was your test drive, {{FirstName}}?\nYour {{Vehicle_Make}} is still waiting\nReady to make it official?' \
DICE_CBB_Success_Metrics__c='Email open rate > 40%\nReturn visit rate > 15%\nPurchase conversion within 14 days > 8%' \
DICE_CBB_Target_Audience__c='Customers who completed a test drive in the last 30 days but have not initiated a purchase. Sourced from Data Cloud segment: Vehicle Interest Waterfall — Priority 2 (Test Drive No Purchase).' \
DICE_CBB_CTAs__c='View Your Test-Driven Vehicle\nSchedule Another Test Drive\nGet Pre-Qualified\nChat With Us' \
DICE_CBB_Updated_By__c='ADMIN_USER_ID' \
DICE_CBB_Updated_Date__c='2026-05-09T12:00:00Z'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

#### Brief 3: Welcome Series

```bash
sf data create record --sobject DICE_CBB_CampaignBrief__c \
  --values "Name='Welcome Series Brief' \
DICE_CBB_Brand_Voice__c='Warm, welcoming, educational. Introduce the CarMax difference without being salesy.' \
DICE_CBB_Campaign__c='CAMPAIGN_WELCOME_ID' \
DICE_CBB_Channels__c='Email' \
DICE_CBB_Description__c='Welcome new email subscribers with a multi-touch series introducing the CarMax experience, tools, and value proposition.' \
DICE_CBB_Launch_Date__c='2026-05-15' \
DICE_CBB_End_Date__c='2026-12-31' \
DICE_CBB_Product_Focus__c='Brand Awareness and Engagement' \
DICE_CBB_Key_Messages__c='Welcome to CarMax — car buying, reimagined\nExplore our online tools: search, compare, pre-qualify\nThe CarMax difference: no-haggle pricing, Love Your Car Guarantee\nOver 50,000 vehicles available nationwide' \
DICE_CBB_Objectives__c='Introduce new subscribers to the CarMax brand and tools\nDrive first website visit or app download\nEstablish email engagement habits early' \
DICE_CBB_Status__c='Draft' \
DICE_CBB_Subject_Line_Options__c='Welcome to CarMax, {{FirstName}}!\nYour car-buying journey starts here\nDiscover the CarMax difference' \
DICE_CBB_Success_Metrics__c='Welcome email open rate > 50%\nClick-through rate > 15%\nSecond email open rate > 35%' \
DICE_CBB_Target_Audience__c='Newly subscribed email contacts. Sourced from Data Cloud segment: New Email Subscribers (subscribed within last 7 days).' \
DICE_CBB_CTAs__c='Start Browsing\nGet Pre-Qualified\nFind a Store Near You\nDownload the App' \
DICE_CBB_Updated_By__c='ADMIN_USER_ID' \
DICE_CBB_Updated_Date__c='2026-05-09T12:00:00Z'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

#### Brief 4: Price Drop Alert

```bash
sf data create record --sobject DICE_CBB_CampaignBrief__c \
  --values "Name='Price Drop Alert Brief' \
DICE_CBB_Brand_Voice__c='Excited but authentic. Share genuine good news without manufactured urgency.' \
DICE_CBB_Campaign__c='CAMPAIGN_PRICEDROP_ID' \
DICE_CBB_Channels__c='Email;Digital' \
DICE_CBB_Description__c='Real-time alerts when a vehicle the customer has viewed or hearted drops in price. High-intent, high-conversion trigger.' \
DICE_CBB_Launch_Date__c='2026-05-15' \
DICE_CBB_End_Date__c='2026-12-31' \
DICE_CBB_Product_Focus__c='Used Vehicle Sales — Price Sensitive Segment' \
DICE_CBB_Key_Messages__c='Great news — a vehicle you have been watching just dropped in price\nCarMax prices are upfront and haggle-free\nThis price is good while the vehicle is in stock\nSee updated price and vehicle details' \
DICE_CBB_Objectives__c='Capitalize on high-intent price sensitivity signals\nDrive immediate return visits to listings\nIncrease purchase conversion among price-watching customers' \
DICE_CBB_Status__c='Draft' \
DICE_CBB_Subject_Line_Options__c='Price drop on your {{Vehicle_Make}} {{Vehicle_Model}}!\nGood news: a vehicle you like just got more affordable\nYour watched vehicle is now ${{Price_Drop_Amount}} less' \
DICE_CBB_Success_Metrics__c='Email open rate > 45%\nClick-to-listing rate > 25%\nPurchase conversion within 7 days > 10%' \
DICE_CBB_Target_Audience__c='Customers who have viewed or hearted a vehicle that has received a price reduction. Sourced from Data Cloud segment: Price Drop Alert. Real-time trigger based on inventory pricing events.' \
DICE_CBB_CTAs__c='See Updated Price\nView Vehicle Details\nSchedule a Test Drive\nGet Pre-Qualified' \
DICE_CBB_Updated_By__c='ADMIN_USER_ID' \
DICE_CBB_Updated_Date__c='2026-05-09T12:00:00Z'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

> **Important:** Replace all `CAMPAIGN_*_ID` and `ADMIN_USER_ID` placeholders with actual IDs from Step 2B before running.

---

## Step 3: Add Campaign Members for Demo Personas (Supporting Only)

**Context:** In MCA, CampaignMember records are NOT required for targeting — segments handle that. However, they provide useful organizational tracking and are visible in Campaign reports.

> **These CampaignMember records are for organizational tracking only.** The actual audience targeting uses Data Cloud segments (Phase 5). The waterfall overlap demo at Stop 2 shows segment membership, not CampaignMember status.

### 3A: Get Contact IDs for Demo Personas

```bash
sf data query --query "SELECT Id, FirstName, LastName, Email FROM Contact WHERE LastName IN ('Dawson','Thompson','Garcia','Patel','Williams','Chen','Rodriguez','Kim') ORDER BY LastName" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Save the Contact IDs for each persona.

### 3B: Get Campaign IDs

```bash
sf data query --query "SELECT Id, Name FROM Campaign ORDER BY Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Save the Campaign IDs for assignment.

### 3C: Create CampaignMember Records

**Jane Dawson — 3 campaigns (KEY: drives waterfall overlap narrative)**

Jane is the focal persona for the waterfall demo. She appears in 3 campaigns, which mirrors her presence in 3 overlapping segments (Hearted Vehicle, Test Drive, Memorial Day). The demo shows how the waterfall resolves this overlap at the segment level.

```bash
# Jane Dawson → Hearted Vehicle Follow-Up (highest priority — waterfall P1)
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_HEARTED_ID' ContactId='JANE_DAWSON_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Jane Dawson → Test Drive - No Purchase Nurture (waterfall P2)
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_TESTDRIVE_ID' ContactId='JANE_DAWSON_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Jane Dawson → Seasonal Push - Memorial Day (waterfall P3 catch-all)
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_MEMORIAL_ID' ContactId='JANE_DAWSON_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Other Persona Assignments (1 campaign each)**

```bash
# Marcus Thompson → Test Drive - No Purchase Nurture
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_TESTDRIVE_ID' ContactId='MARCUS_THOMPSON_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Aisha Garcia → New Email Subscriber Welcome
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_WELCOME_ID' ContactId='AISHA_GARCIA_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Raj Patel → Pre-Qualification Completion
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_PREQUAL_ID' ContactId='RAJ_PATEL_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Sarah Williams → Price Drop Alert
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_PRICEDROP_ID' ContactId='SARAH_WILLIAMS_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw

# David Chen → Trade-In and Upgrade
sf data create record --sobject CampaignMember \
  --values "CampaignId='CAMPAIGN_TRADEIN_ID' ContactId='DAVID_CHEN_ID' Status='Sent'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

> **Note:** Replace all placeholder IDs (`CAMPAIGN_*_ID`, `*_ID`) with actual IDs from Steps 3A and 3B before running.

### Campaign Member Summary

| Persona | Campaigns | Count | Demo Purpose |
|---------|-----------|-------|-------------|
| Jane Dawson | Hearted Vehicle, Test Drive, Memorial Day | 3 | Waterfall overlap focal persona |
| Marcus Thompson | Test Drive | 1 | Secondary test drive persona |
| Aisha Garcia | Welcome | 1 | Welcome series / contrasting email |
| Raj Patel | Pre-Qualification | 1 | Finance journey persona |
| Sarah Williams | Price Drop | 1 | Price sensitivity persona |
| David Chen | Trade-In | 1 | Trade-in journey persona |

**Total CampaignMember records:** 8

---

## Step 4: Verification

### 4A: Count Campaigns

```bash
sf data query --query "SELECT COUNT(Id) total FROM Campaign" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** 10 (may be higher if SDO pre-loaded campaigns exist)

### 4B: List Campaigns with Member Counts

```bash
sf data query --query "SELECT Name, Type, Status, NumberOfContacts FROM Campaign ORDER BY Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected results:**

| Campaign | Type | Status | Members |
|----------|------|--------|---------|
| EV Consideration Nurture | Email | Active | 0 |
| Hearted Vehicle Follow-Up | Email | Active | 1 |
| Instant Offer Abandonment | Email | Active | 0 |
| New Email Subscriber Welcome | Email | Active | 1 |
| Pre-Qualification Completion | Email | Active | 1 |
| Price Drop Alert | Email | Active | 1 |
| Saved Search Match | Email | Active | 0 |
| Seasonal Push - Memorial Day | Multi-Channel | Planned | 1 |
| Test Drive - No Purchase Nurture | Email | Active | 2 |
| Trade-In and Upgrade | Email | Active | 1 |

### 4C: Verify Jane Dawson's 3-Campaign Overlap

```bash
sf data query --query "SELECT Campaign.Name, Status FROM CampaignMember WHERE Contact.LastName = 'Dawson' ORDER BY Campaign.Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** 3 records — Hearted Vehicle Follow-Up, Seasonal Push - Memorial Day, Test Drive - No Purchase Nurture.

**Demo significance:** This mirrors Jane's presence in 3 overlapping segments. At Demo Stop 2, the waterfall segment resolves this overlap: Jane is assigned to Waterfall P1 (Hearted Vehicle) because it is highest priority, and excluded from P2 and P3.

### 4D: Verify Campaign Brief Records

```bash
sf data query --query "SELECT Id, Name, DICE_CBB_Status__c, DICE_CBB_Campaign__r.Name, DICE_CBB_Channels__c FROM DICE_CBB_CampaignBrief__c ORDER BY Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** 4 records (if DICE_CBB is installed):

| Brief Name | Status | Linked Campaign | Channels |
|------------|--------|----------------|----------|
| Hearted Vehicle Re-Engagement Brief | Draft | Hearted Vehicle Follow-Up | Email;Digital |
| Price Drop Alert Brief | Draft | Price Drop Alert | Email;Digital |
| Test Drive Follow-Up Brief | Draft | Test Drive - No Purchase Nurture | Email |
| Welcome Series Brief | Draft | New Email Subscriber Welcome | Email |

### 4E: Count Campaign Briefs

```bash
sf data query --query "SELECT COUNT(Id) total FROM DICE_CBB_CampaignBrief__c" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** 4 (or 0 if DICE_CBB is not installed)

### 4F: Verify Flagship Brief Detail

```bash
sf data query --query "SELECT Name, DICE_CBB_Target_Audience__c, DICE_CBB_Objectives__c, DICE_CBB_Key_Messages__c, DICE_CBB_CTAs__c, DICE_CBB_Success_Metrics__c FROM DICE_CBB_CampaignBrief__c WHERE Name = 'Hearted Vehicle Re-Engagement Brief'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** Full brief content with audience referencing "Vehicle Interest Waterfall — Priority 1", objectives including test drive booking targets, and success metrics with specific percentage thresholds.

---

## Campaign > Segment > Brief > Demo Stop Mapping

| Campaign | Segment (Phase 5) | Brief | Demo Stop | Purpose |
|----------|-------------------|-------|-----------|---------|
| Hearted Vehicle Follow-Up | Waterfall P1: Hearted Vehicle | Hearted Vehicle Re-Engagement Brief | Stop 1, Stop 3 | Campaign Agent demo + flagship email |
| Test Drive - No Purchase Nurture | Waterfall P2: Test Drive No Purchase | Test Drive Follow-Up Brief | Stop 2, Stop 4 | Waterfall demo + flow orchestration |
| New Email Subscriber Welcome | New Email Subscribers | Welcome Series Brief | Stop 3 | Aisha's contrasting email preview |
| Pre-Qualification Completion | PreQual Shoppers | (Optional — create if time) | Stop 3 | "Stop Wondering" email |
| Price Drop Alert | Price Drop Alert | Price Drop Alert Brief | Stop 3 | "Ready to Save?" email |
| Saved Search Match | Saved Search Match | (Optional — create if time) | Stop 3 | "It's a Match!" email |
| Trade-In and Upgrade | Trade-In (Einstein) | (Optional — create if time) | Stop 2 | Einstein segmentation demo |
| EV Consideration Nurture | EV (Einstein) | (Optional — create if time) | Stop 2 | Einstein segmentation demo |
| Seasonal Push - Memorial Day | Waterfall P3: Catch-All | (Optional — create if time) | Stop 2 | Waterfall catch-all |
| Instant Offer Abandonment | Instant Offer Abandonment | (Optional — create if time) | Stop 3 | Abandonment recovery email |

**Legend:**
- Briefs marked as created are the 4 from Step 2C/2D
- "(Optional — create if time)" briefs can be added later but are not required for demo functionality
- Campaign Agent (Stop 1) can generate briefs live, so pre-created briefs serve as fallback/reference

---

## Critical Notes

### 1. Campaign Brief Builder May Not Be Installed
`DICE_CBB_CampaignBrief__c` is a managed package that ships with certain SDO builds. Always verify with the query in Step 2A before attempting brief creation. If not available:
- Campaign records from Step 1 still work as organizational containers
- Campaign Agent may generate briefs differently or store them in an alternative location
- The demo can proceed — Stop 1 can show Campaign Agent generating a brief live

### 2. Campaign Members Use ContactId, Not LeadId
CarMax does not use Leads in its Salesforce data model. All demo personas are Contact records. The `CampaignMember.ContactId` field is used exclusively. Do not attempt to assign via `LeadId`.

### 3. CampaignMember Status Values
- **"Sent"** — Initial assignment. The persona has been targeted by the campaign.
- **"Responded"** — Engagement recorded. Use for personas who have clicked/opened (can be updated later if needed for demo narrative).

### 4. Jane Dawson in 3 Campaigns — Waterfall Setup
This is the key setup for Demo Stop 2. Jane appears in 3 campaigns, mirroring her membership in 3 overlapping segments. The demo SHOWS segment membership and waterfall resolution — the CampaignMember records are supporting context, not the primary demo artifact.

### 5. Campaign Type Picklist Values
- **"Email"** — Standard SDO picklist value for email-only campaigns.
- **"Multi-Channel"** — Standard SDO picklist value for campaigns spanning email, SMS, digital. Used only for Memorial Day.

### 6. Briefs Are Generated by Campaign Agent AI
The pre-created briefs in Step 2 are a FALLBACK. During the live demo at Stop 1, the intent is to generate the Hearted Vehicle brief live via Campaign Agent using a natural language prompt like: *"Create a campaign to re-engage customers who have hearted vehicles but haven't purchased."* The pre-created brief ensures the demo has content even if the AI generation step is skipped or produces unexpected results.

### 7. Brief > Campaign Relationship
`DICE_CBB_Campaign__c` is a lookup from the brief to the Campaign record. This is a many-to-one relationship — multiple briefs can link to the same campaign (e.g., different versions or A/B variants). In this implementation, each campaign has at most one brief.

### 8. MCA Workflow Order
In MCA, the workflow is: **Brief FIRST, then content, then orchestration.** This is the reverse of MC Engagement, where campaigns were set up after content was built. The brief is the "blueprint" that Campaign Agent generates, and subsequent steps (content creation in Phase 7, flow building in Phase 8) reference the brief's specifications.

### 9. Segment Membership vs Campaign Membership
To be absolutely clear:
- **Segments** (Phase 5) determine WHO receives communications. They are the audience engine.
- **Campaigns** (this phase) are organizational containers for tracking and reporting.
- **Campaign Briefs** (this phase) are AI-generated specs that define WHAT to communicate.
- **CampaignMember** records link contacts to campaigns for reporting but do NOT control targeting.

### 10. Date Ranges
- Most campaigns: 2026-05-15 to 2026-06-30 (short-term, demonstrable window)
- Evergreen campaigns (Welcome, Price Drop): 2026-05-15 to 2026-12-31 (ongoing programs)
- Memorial Day: 2026-05-15 to 2026-06-01 (event-specific)

---

## Estimated Execution Time

| Step | Duration | Notes |
|------|----------|-------|
| Step 1: Create 10 Campaigns | 3-5 min | 10 sequential sf data create record commands |
| Step 2A: Verify DICE_CBB | 1 min | Single query — determines if Step 2 proceeds |
| Step 2B: Get IDs | 1 min | Two queries for User and Campaign IDs |
| Step 2C-2D: Create 4 Briefs | 5-8 min | 4 sequential commands with long --values strings |
| Step 3: CampaignMember records | 3-5 min | 8 sequential sf data create record commands |
| Step 4: Verification | 3-5 min | 6 verification queries |
| **Total** | **15-25 min** | Assumes DICE_CBB is installed |

---

## Rollback

If any step needs to be undone:

```bash
# Delete all CampaignMember records
sf data query --query "SELECT Id FROM CampaignMember WHERE Contact.LastName IN ('Dawson','Thompson','Garcia','Patel','Williams','Chen')" \
  --target-org carmax-sdo-mm-app-wz95pw --result-format csv | tail -n +2 | while read id; do
  sf data delete record --sobject CampaignMember --record-id "$id" --target-org carmax-sdo-mm-app-wz95pw
done

# Delete all Campaign Brief records
sf data query --query "SELECT Id FROM DICE_CBB_CampaignBrief__c" \
  --target-org carmax-sdo-mm-app-wz95pw --result-format csv | tail -n +2 | while read id; do
  sf data delete record --sobject DICE_CBB_CampaignBrief__c --record-id "$id" --target-org carmax-sdo-mm-app-wz95pw
done

# Delete all Campaign records created by this phase
sf data query --query "SELECT Id FROM Campaign WHERE Name IN ('Hearted Vehicle Follow-Up','Test Drive - No Purchase Nurture','New Email Subscriber Welcome','Pre-Qualification Completion','Price Drop Alert','Saved Search Match','Trade-In and Upgrade','EV Consideration Nurture','Seasonal Push - Memorial Day','Instant Offer Abandonment')" \
  --target-org carmax-sdo-mm-app-wz95pw --result-format csv | tail -n +2 | while read id; do
  sf data delete record --sobject Campaign --record-id "$id" --target-org carmax-sdo-mm-app-wz95pw
done
```

---

## Phase Completion Checklist

- [ ] 10 Campaign records created and verified
- [ ] DICE_CBB installation confirmed (or documented as absent)
- [ ] 4 Campaign Briefs created (if DICE_CBB available)
- [ ] Flagship brief (Hearted Vehicle Re-Engagement) has full content
- [ ] 8 CampaignMember records created
- [ ] Jane Dawson confirmed in 3 campaigns
- [ ] All verification queries pass
- [ ] Campaign > Segment > Brief mapping documented and cross-referenced with Phase 5
