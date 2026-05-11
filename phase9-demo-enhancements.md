# Phase 9: Demo Day Enhancements & Verification — Implementation Plan

## Overview

Polish and configure the final demo-day elements: Campaign Agent brief for Stop 1, waterfall overlap verification for Stop 2, persona preview setup for Stop 3, SMS live-authoring prep for Stop 4, Data Cloud 360 walkthrough prep for Stop 5 (NEW in v4), reporting setup for Stop 6, and the dynamic feedback loop explainer for Stop 7. These enhancements transform the technical build (Phases 1-8) into a polished **90-minute** MCA Harbor Cruise demo.

**Org:** `carmax-sdo-mm-app-wz95pw`
**Prerequisite:** All of Phases 1-8 complete
**Demo Duration:** 90 minutes (expanded from 60 min in v3)

---

## Enhancement #1: Campaign Agent Brief (Demo Stop 1 -- 12 min)

### Purpose

Stop 1 opens the demo with Campaign Agent generating a campaign brief from a natural-language prompt. This is the "zero to one" moment -- the audience sees AI translate business intent into an actionable marketing specification. The pre-created brief from Phase 6 serves as a fallback if live generation stalls.

### Step 1: Verify Campaign Brief Builder Installation

```bash
sf data query --query "SELECT Id, Name FROM DICE_CBB_CampaignBrief__c LIMIT 1" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**If the query succeeds** (returns 0 or more rows): DICE_CBB is installed. Proceed with Steps 2-4.

**If the query fails** (sObject not supported error): DICE_CBB is not installed. Skip to Step 5 and use Option B (narrative-only) for Stop 1.

### Step 2: Get Required IDs

```bash
# Get the System Administrator user ID (for brief's Updated_By field)
sf data query --query "SELECT Id, Name FROM User WHERE IsActive = true AND Profile.Name = 'System Administrator' LIMIT 1" \
  --target-org carmax-sdo-mm-app-wz95pw

# Get the Hearted Vehicle Follow-Up campaign ID
sf data query --query "SELECT Id, Name FROM Campaign WHERE Name = 'Hearted Vehicle Follow-Up'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Save these values:
- `ADMIN_USER_ID` -- the System Administrator user ID
- `CAMPAIGN_HEARTED_ID` -- the Hearted Vehicle Follow-Up campaign record ID

### Step 3: Verify or Pre-Create the Demo Campaign Brief

Check if the flagship brief already exists from Phase 6:

```bash
sf data query --query "SELECT Id, Name, DICE_CBB_Status__c, DICE_CBB_Campaign__r.Name FROM DICE_CBB_CampaignBrief__c WHERE Name = 'Hearted Vehicle Re-Engagement Brief'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**If it exists:** Confirm Status, Campaign linkage, and content. Skip to Step 4.

**If it does not exist:** Create it now. This is the same command from Phase 6, repeated here for demo-day convenience so the implementer does not need to cross-reference:

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

> **Important:** Replace `CAMPAIGN_HEARTED_ID` and `ADMIN_USER_ID` with the actual IDs from Step 2 before running.

### Step 4: Verify Brief Content Is Complete

```bash
sf data query --query "SELECT Name, DICE_CBB_Target_Audience__c, DICE_CBB_Key_Messages__c, DICE_CBB_Success_Metrics__c, DICE_CBB_CTAs__c, DICE_CBB_Subject_Line_Options__c, DICE_CBB_Body_Copy_Variants__c FROM DICE_CBB_CampaignBrief__c WHERE Name = 'Hearted Vehicle Re-Engagement Brief'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Confirm all fields are populated. The brief should reference:
- Target Audience: "Vehicle Interest Waterfall -- Priority 1 (Hearted Vehicle)"
- Success Metrics: specific percentage thresholds (open > 35%, click > 12%, etc.)
- CTAs: 4 distinct call-to-action options
- Body Copy: 2 variants (Conversational + Urgency-lite)

### Step 5: Demo Narrative for Stop 1

**Option A -- Live Generation (preferred, 12 min):**

1. Open Campaign Agent in the Marketing App
2. Type the prompt live:

   > "Create a campaign targeting customers who hearted vehicles but haven't purchased. Use email as the primary channel. The tone should be warm and helpful -- CarMax style. Include dynamic vehicle cards with their favorited cars, pricing, and a CTA to schedule a test drive."

3. Watch Campaign Agent generate the brief -- audience, channels, messaging, subject lines, success metrics
4. Walk through each section of the generated brief:
   - **Target Audience:** Hearted vehicle customers, no purchase in 90 days
   - **Channels:** Email (primary), SMS (follow-up)
   - **Key Messages:** Vehicle cards, pricing, scheduling CTAs
   - **Success Metrics:** Open rate >35%, click-to-listing >12%, test drive booking >5%
5. Show how the brief connects to the Campaign record
6. Highlight the brand voice and tone settings

**Talk Track:**
- "The marketer didn't write SQL or build a segment -- they described the business intent"
- "Campaign Agent translated business language into actionable marketing specs"
- "This brief now becomes the single source of truth for the campaign"

**Option B -- Pre-Loaded Brief (fallback if Agent is slow or DICE_CBB unavailable):**

1. Navigate to the Hearted Vehicle Follow-Up campaign record
2. Show the linked Campaign Brief record
3. Walk through each section: "Here is what Campaign Agent would generate..."
4. Point out the AI-friendly structure: audience, messaging, KPIs, brand voice

**Transition to Stop 2:** "Now that we have our brief, let's build the audience it describes."

---

## Enhancement #2: Waterfall Overlap Verification (Demo Stop 2 -- 18 min)

### Purpose

Verify that Jane Dawson appears in all 3 overlapping segments, and that the waterfall resolves her to Priority 1 only. This is the "aha moment" of Stop 2 -- the audience sees governance in action.

### Step 1: Verify Jane Dawson Exists in Data Cloud

```bash
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT ssot__Id__c, ssot__FirstName__c, ssot__LastName__c FROM ssot__Individual__dlm WHERE ssot__LastName__c = '"'"'Dawson'"'"' AND ssot__FirstName__c = '"'"'Jane'"'"' LIMIT 5"}'
```

**Expected:** At least 1 row for Jane Dawson. Record the `ssot__Id__c` value as `JANE_INDIVIDUAL_ID`.

### Step 2: Verify Jane's Qualifying Data for Each Segment Tier

**Priority 1 -- Hearted Vehicle Follow-Up (requires IsHearted = 'true' vehicles):**

```bash
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT VehicleId__c, Make__c, Model__c, Year__c, Price__c, IsHearted__c FROM CarMax_Vehicle__dlm WHERE IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"' AND IsHearted__c = '"'"'true'"'"'"}'
```

**Expected:** 3 rows:
| Make | Model | Year | IsHearted |
|------|-------|------|------------|
| Ford | Expedition XLT | 2024 | true |
| Toyota | 4Runner SR5 | 2023 | true |
| Hyundai | Santa Fe SEL | 2025 | true |

**Priority 2 -- Test Drive No Purchase (requires test drive with no purchase):**

```bash
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT TestDriveId__c, VIN__c, TestDriveDate__c, Outcome__c, ConvertedToPurchase__c FROM CarMax_TestDrive__dlm WHERE IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"'"}'
```

**Expected:** At least 1 row with `ConvertedToPurchase__c = 'false'` (the Ford Expedition test drive she took but did not purchase).

**Priority 3 -- Seasonal Push Memorial Day (catch-all, all active contacts qualify):**

Jane qualifies by default as an active contact in the system.

### Step 3: Verify Waterfall Resolution

Check segment membership to confirm Jane is ONLY in the Priority 1 segment. The exact method depends on how segments were built in Phase 5.

**Query segment membership (if segments expose membership via SSOT):**

```bash
# Check P1 segment membership (Jane should be IN this segment)
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT COUNT(*) AS cnt FROM ssot__SegmentMembership__dlm WHERE ssot__IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"'"}'
```

**Alternative -- verify via UI:**
1. Navigate to Data Cloud > Segments
2. Open each segment (P1, P2, P3)
3. Use the "Preview Members" function to search for Jane Dawson
4. Confirm: Jane appears in P1 membership, and is NOT in P2 or P3

**Expected Result:**
- P1 (Hearted Vehicle Follow-Up): Jane IS a member
- P2 (Test Drive No Purchase): Jane is NOT a member (excluded by waterfall)
- P3 (Seasonal Push Memorial Day): Jane is NOT a member (excluded by waterfall)

### Step 4: Verify Calculated Insights for Jane

Jane's CI scores should be visible and meaningful for the Stop 2 narrative:

```bash
# Customer Lifetime Value
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Customer_Lifetime_Value__cio/data?limit=50" \
  --target-org carmax-sdo-mm-app-wz95pw 2>&1 | grep -v "^Warning:" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for row in data.get('data', []):
    if 'Dawson' in str(row) or 'Jane' in str(row):
        print(json.dumps(row, indent=2))
"

# Propensity to Buy
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Propensity_to_Buy__cio/data?limit=50" \
  --target-org carmax-sdo-mm-app-wz95pw 2>&1 | grep -v "^Warning:" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for row in data.get('data', []):
    if 'Dawson' in str(row) or 'Jane' in str(row):
        print(json.dumps(row, indent=2))
"

# Engagement Velocity
sf api request rest \
  --url "/services/data/v65.0/ssot/calculated-insights/Engagement_Velocity__cio/data?limit=50" \
  --target-org carmax-sdo-mm-app-wz95pw 2>&1 | grep -v "^Warning:" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for row in data.get('data', []):
    if 'Dawson' in str(row) or 'Jane' in str(row):
        print(json.dumps(row, indent=2))
"
```

**Expected for Jane Dawson:**
- CLV: `HeartedCount__c` = 3, `PurchaseCount__c` >= 1
- Propensity: `PropensityScore__c` > 50, `UniqueEventTypes__c` >= 4
- Velocity: `RecentWeekEvents__c` > `PriorWeekEvents__c` (accelerating)

### Demo Narrative for Stop 2

**Part A -- Einstein Segmentation (6 min):**
1. Navigate to Data Cloud > Segments
2. Show the "EV Consideration Nurture" Einstein segment -- demonstrate natural-language audience discovery
3. Show how Einstein translates the prompt into segment criteria
4. Preview membership count and sample members

**Part B -- Calculated Insight Enrichment (5 min):**
1. Navigate to Calculated Insights
2. Show the 4 CarMax CIs: Customer Lifetime Value, Propensity to Buy, Vehicle Preference Affinity, Engagement Velocity
3. Click into Jane Dawson's profile to show her CI scores
4. Explain how CIs power segment qualification and flow decisioning

**Part C -- Waterfall Prioritization (7 min):**
1. Open the "Vehicle Interest Waterfall" segment configuration
2. Show the 3 priority tiers:
   - **Priority 1:** Hearted Vehicle Follow-Up (highest value -- active intent)
   - **Priority 2:** Test Drive No Purchase (mid-value -- demonstrated interest)
   - **Priority 3:** Seasonal Push Memorial Day (lowest -- catch-all)
3. **The "aha moment":** Show that Jane Dawson qualifies for ALL 3 tiers
4. Show the waterfall resolution -- Jane is assigned to Priority 1 ONLY
5. Explain: "Without the waterfall, Jane would receive 3 separate campaigns. With it, she gets the single most relevant message."

**Talk Track:**
- "Einstein discovers audiences that a marketer might miss -- like EV-curious shoppers who haven't been targeted yet"
- "Calculated Insights turn raw data into marketing-ready signals -- propensity, velocity, lifetime value"
- "The waterfall is the governance layer -- it ensures every customer gets exactly one campaign, the most relevant one"

**Transition to Stop 3:** "Jane is now in the Hearted Vehicle segment. Let's see what email she'll receive."

---

## Enhancement #3: Persona Preview Setup (Demo Stop 3 -- 14 min)

### Purpose

Set up persona previews in the MCA Email Builder so the presenter can instantly switch between Jane Dawson (power shopper, 3 vehicle cards) and Aisha Thompson (new subscriber, fallback content). The contrast between the two previews is the visual proof of 1:1 personalization at scale.

### Persona 1: Jane Dawson (Power Shopper)

**Profile:**
- 3 hearted SUVs: Ford Expedition XLT ($52,998), Toyota 4Runner SR5 ($41,998), Hyundai Santa Fe SEL ($33,498)
- Pre-qualified (completed online pre-qualification)
- Test drove the Ford Expedition at CarMax Richmond
- Active email subscriber with high engagement
- In Waterfall P1 segment (Hearted Vehicle Follow-Up)

**Expected Email Rendering:**
- Greeting: "Hi Jane,"
- 3 dynamic vehicle cards rendered from Data Graph repeater (each showing Make, Model, Year, Price, Image, CTA)
- Pre-qualification block is HIDDEN (she already pre-qualified)
- CTA: "Schedule a Test Drive"
- Footer: Standard CarMax legal + unsubscribe

### Persona 2: Aisha Thompson (New Subscriber)

**Profile:**
- New email subscriber (subscribed within last 7 days)
- Viewed 3 sedan pages on carmax.com (browsing behavior only)
- No account created
- No pre-qualification started
- No vehicles hearted
- In New Email Subscribers segment

**Expected Email Rendering:**
- Greeting: "Hi Aisha,"
- 0 hearted vehicles -- fallback "Browse Our Top Picks" static section renders
- "Create an Account" block SHOWS (she has no account)
- "Get Pre-Qualified" block SHOWS (she has not pre-qualified)
- CTA: "Start Browsing"
- Footer: Standard CarMax legal + unsubscribe

### Step 1: Verify Persona Data Exists in Data Cloud

```bash
# Jane Dawson -- Individual record
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT ssot__Id__c, ssot__FirstName__c, ssot__LastName__c FROM ssot__Individual__dlm WHERE ssot__LastName__c = '"'"'Dawson'"'"' AND ssot__FirstName__c = '"'"'Jane'"'"'"}'

# Jane Dawson -- Hearted vehicles (must be exactly 3)
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT Make__c, Model__c, Year__c, Price__c, IsHearted__c FROM CarMax_Vehicle__dlm WHERE IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"' AND IsHearted__c = '"'"'true'"'"'"}'

# Aisha Thompson -- Individual record
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT ssot__Id__c, ssot__FirstName__c, ssot__LastName__c FROM ssot__Individual__dlm WHERE ssot__LastName__c = '"'"'Thompson'"'"' AND ssot__FirstName__c = '"'"'Aisha'"'"'"}'

# Aisha Thompson -- Hearted vehicles (must be 0)
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT COUNT(*) AS cnt FROM CarMax_Vehicle__dlm WHERE IndividualId__c = '"'"'AISHA_INDIVIDUAL_ID'"'"' AND IsHearted__c = '"'"'true'"'"'"}'
```

**Expected:**
- Jane: 3 hearted vehicles (Ford Expedition XLT, Toyota 4Runner SR5, Hyundai Santa Fe SEL)
- Aisha: 0 hearted vehicles

### Step 2: Verify Data Graph Contains Both Personas

The Data Graph must be built and operational for the dynamic loop to render vehicle cards:

```bash
# Verify graph status
sf data query --query "SELECT Id, Name, Status, DataGraphType FROM DataGraph WHERE Name = 'CarMax Customer 360'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:** Status = `Built` (or `BUILT`), DataGraphType = `NONE`

If Status is not `Built`, the graph must be built via the UI before the demo:
1. Setup > Data Cloud > Data Graphs
2. Click "CarMax Customer 360"
3. Click "Save and Build"
4. Wait 2-5 minutes for build to complete

### Step 3: Preview Instructions (In-App)

To preview the flagship email with persona switching:

1. Navigate to Marketing App > Content > Emails
2. Open the "Hearted Vehicle Follow-Up" email (or "Compare What Matters" -- depending on naming from Phase 7)
3. Click **Preview** in the Email Builder toolbar
4. In the Preview panel, select **Contact** as the preview source
5. Search for "Jane Dawson" and select her
6. Verify: 3 vehicle cards render, pre-qual block hidden, "Schedule a Test Drive" CTA visible
7. Switch preview to "Aisha Thompson"
8. Verify: fallback content renders, "Create an Account" and "Get Pre-Qualified" blocks visible, "Start Browsing" CTA

**Note:** The email MUST be in Published state for persona preview to work with Data Graph data. If the email is in Draft, the dynamic loop may not resolve against the graph.

### Demo Narrative for Stop 3

**Part A -- Email Structure (5 min):**
1. Open the Hearted Vehicle Follow-Up email in MCA Email Builder
2. Walk through the modular structure: Header, Greeting, Intro, Dynamic Vehicle Cards, CTA, Footer
3. Show how the email mixes component blocks (header, footer) with HTML blocks (dynamic loop)

**Part B -- Data Graph Connection (4 min):**
1. Show the CarMax Customer 360 Data Graph configuration
2. Explain the graph structure: Individual > Vehicle, Test Drive, Web Engagement
3. Show how the repeater references graph field devNames: `{{CX360_Vehicle_Make}}`, `{{CX360_Vehicle_Model}}`, `{{CX360_Vehicle_Price}}`, etc.
4. Explain the filter: `IsHearted = 'true'` -- only hearted vehicles appear in the cards

**Part C -- Persona Previews (5 min):**
1. **Preview as Jane Dawson:**
   - 3 vehicle cards render (Ford Expedition XLT, Toyota 4Runner SR5, Hyundai Santa Fe SEL)
   - Pre-qualification block is HIDDEN (she already pre-qualified)
   - CTA: "Schedule a Test Drive"
2. **Switch to Aisha Thompson:**
   - 0 hearted vehicles -- fallback "Browse Our Top Picks" static section
   - "Create an Account" and "Get Pre-Qualified" blocks SHOW
   - CTA: "Start Browsing"
3. Side-by-side comparison: "Same template, completely different experience"

**Talk Track:**
- "The dynamic loop is pulling live data from the Data Graph -- not static content"
- "Jane sees her actual hearted vehicles with real pricing"
- "Aisha sees a completely different experience because she hasn't taken those steps yet"
- "This is true 1:1 personalization at scale, powered by Data Cloud"

**Transition to Stop 4:** "Now let's see how this email gets delivered -- and what happens when Jane engages or doesn't."

---

## Enhancement #4: SMS Live-Authoring Prep (Demo Stop 4 -- 14 min)

### Purpose

Prepare the SMS content and navigation path so the presenter can author an SMS message live during the demo. The SMS is part of the MCA Flow -- it triggers for customers who opened the email but didn't click (openers-who-didn't-click branch).

### Step 1: Verify SMS Channel Configuration

Before the demo, confirm that SMS messaging is enabled and a sender profile exists:

1. Navigate to Marketing App > Messaging
2. Verify at least one SMS sender profile is configured
3. If no sender profile exists, document the absence and prepare to skip the live SMS portion of Stop 4 (fallback: focus on flow walkthrough only)

### Step 2: Pre-Stage SMS Content

**Full SMS text to type during demo:**

> Hi {{FirstName}}! Still thinking about the {{Vehicle_Year}} {{Vehicle_Make}} you test drove at CarMax {{Store}}? Your 24-hour test drive is still available. Book again: {{ShortLink}} Reply STOP to opt out.

**Character count:** ~155 characters (1 SMS segment)

**Personalization tokens used:**
- `{{FirstName}}` -- from Contact/Individual
- `{{Vehicle_Year}}` -- from Data Cloud Vehicle DMO via Data Graph
- `{{Vehicle_Make}}` -- from Data Cloud Vehicle DMO via Data Graph
- `{{Store}}` -- from Data Cloud Test Drive DMO (CarMaxStore__c)
- `{{ShortLink}}` -- auto-generated by MCA messaging

### Step 3: Navigation Path

1. Open Marketing App > Messaging > Create New SMS
2. Select the configured sender profile
3. Type the SMS content from Step 2
4. Use the personalization token picker (thunderbolt icon) to insert tokens from Data Cloud
5. Show character count in the preview panel
6. Save the SMS content
7. Return to the Flow Builder and connect the SMS element to the appropriate branch

### Demo Narrative for Stop 4

**Part A -- Flow Canvas Walkthrough (7 min):**
1. Open the "CarMax Vehicle Interest Nurture" flow in Flow Builder
2. Walk through the canvas step by step:
   - **Segment Entry:** Vehicle Interest Waterfall > Priority 1 (Hearted Vehicle)
   - **Wait 2 Hours:** Delay before first touchpoint
   - **Decision -- Recent Purchaser?** Suppress customers who purchased since entering the segment
   - **Send Email:** "Compare What Matters" Hearted Vehicle Follow-Up
   - **Wait Until Event:** Email Link Click -- 3-day timeout
   - **Branch -- Clicked?** If yes, end (engaged, let retargeting handle)
   - **Branch -- Not Clicked, Opened?** If opened but no click, send SMS. If no open, send softer reminder email
3. Highlight the suppression logic: "Recent purchasers are automatically excluded"
4. Highlight multi-channel: "The flow intelligently chooses between SMS and email based on actual engagement behavior"

**Part B -- SMS Live Authoring (5 min):**
1. Navigate to Marketing App > Messaging > New SMS
2. Author the SMS live (type from prepared content)
3. Show the personalization token picker pulling from Data Cloud
4. Show character count: ~155 characters (1 SMS segment)
5. Save and connect to the flow

**Part C -- Supporting Flows (2 min):**
1. Quickly show the other 4 flows: Welcome Series, Price Drop Alert, Instant Offer Abandonment, Saved Search Match
2. "Each segment has its own orchestration -- all built on the same MCA Flow infrastructure"

**Talk Track:**
- "This isn't a journey builder from scratch -- it's a Flow, the same platform your admins already know"
- "The Wait Until Event is watching for real engagement, not just waiting a fixed time"
- "SMS and email work together in one flow -- no separate journey for each channel"

**Transition to Stop 5:** "We've seen campaign creation, audience building, content, and orchestration. Let's look at how Data Cloud ties it all together."

---

## Enhancement #5: Data Cloud Customer 360 Walkthrough (Demo Stop 5 -- 8 min) -- NEW IN v4

### Purpose

This is a NEW dedicated stop in v4 (90 min) that was NOT in v3 (60 min). In v3, Data Cloud context was woven into other stops. In v4, Stop 5 is a standalone moment to show Jane Dawson's unified customer profile and demonstrate how Data Cloud powers every previous stop. This is the "connecting the dots" moment.

### Step 1: Pre-Stage -- Navigate to Jane Dawson's Profile

Before the demo, pre-open the tab:

1. Navigate to Data Cloud > Individuals
2. Search for "Jane Dawson"
3. Open her Individual profile page
4. Leave this tab open in the browser (do not close it)

### Step 2: Verify All Data Layers Are Populated

Run these queries to confirm all data that will be visible on Jane's 360 profile:

**Vehicle Records (3 hearted + 1 test driven + potentially 1 purchased):**

```bash
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT VehicleId__c, Make__c, Model__c, Year__c, Price__c, IsHearted__c, IsPurchased__c FROM CarMax_Vehicle__dlm WHERE IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"'"}'
```

**Expected:** 4-5 rows. At minimum: 3 hearted (Ford Expedition XLT, Toyota 4Runner SR5, Hyundai Santa Fe SEL) + 1 test-driven.

**Test Drive Records:**

```bash
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT TestDriveId__c, VIN__c, TestDriveDate__c, CarMaxStore__c, Outcome__c FROM CarMax_TestDrive__dlm WHERE IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"'"}'
```

**Expected:** At least 1 test drive record (Ford Expedition at CarMax Richmond).

**Web Engagement Records:**

```bash
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{"sql":"SELECT ssot__EngagementChannelActionId__c, ssot__EngagementVehicleId__c, ssot__EngagementDateTm__c, ssot__PageURL__c FROM ssot__WebsiteEngagement__dlm WHERE ssot__IndividualId__c = '"'"'JANE_INDIVIDUAL_ID'"'"' ORDER BY ssot__EngagementDateTm__c DESC LIMIT 10"}'
```

**Expected:** Multiple rows showing diverse event types (Vehicle Detail View, Heart Vehicle, Schedule Test Drive, Pre-Qual Complete, etc.).

**Calculated Insight Scores (all 4 CarMax CIs):**

```bash
echo "=== Jane Dawson CI Scores ==="

for CI_NAME in Customer_Lifetime_Value Propensity_to_Buy Vehicle_Preference_Affinity Engagement_Velocity; do
  echo ""
  echo "--- ${CI_NAME} ---"
  sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio/data?limit=100" \
    --target-org carmax-sdo-mm-app-wz95pw 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
for row in data.get('data', []):
    vals = list(row.values()) if isinstance(row, dict) else []
    row_str = str(row)
    if 'JANE_INDIVIDUAL_ID' in row_str:
        print(json.dumps(row, indent=2))
" 2>/dev/null
done
```

> **Note:** Replace `JANE_INDIVIDUAL_ID` with the actual ID from Enhancement #2 Step 1.

**Segment Memberships:**

Verify Jane is in the P1 segment via the UI or SSOT query (same as Enhancement #2 Step 3).

### Step 3: Verify Data Graph Is Built

The Data Graph provides the visual relationship view on the 360 profile:

```bash
sf data query --query "SELECT Id, Name, Status, DataGraphType FROM DataGraph WHERE Name = 'CarMax Customer 360'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Required:** Status = `Built`. If not built, navigate to Data Cloud > Data Graphs > CarMax Customer 360 > Save and Build.

### Demo Narrative for Stop 5

1. **Navigate to Jane Dawson's Individual profile** (pre-opened tab)
2. **Show the Customer 360 view:**
   - **Identity:** Unified Individual from CRM Contact + web engagement data
   - **Vehicle Interactions:** 5 vehicles (3 hearted, 1 test driven, 1 purchased previously)
   - **Web Engagement:** Recent browsing sessions with event types (Vehicle Detail View, Heart Vehicle, Schedule Test Drive, Pre-Qual Complete)
   - **Calculated Insights:** CLV tier, Propensity score, Vehicle Preference (SUV), Engagement Velocity (accelerating)
   - **Segment Membership:** Vehicle Interest Waterfall (Priority 1)
3. **Show the Data Graph:** Individual > Vehicle, Test Drive, Web Engagement relationships
4. **Explain:** "Everything the email personalized, the flow decided, the segment qualified -- it all comes from this unified profile"

**Talk Track:**
- "This is the single source of truth -- CRM data, web behavior, engagement history, AI scores -- all unified"
- "The marketer never had to think about data plumbing -- they just used it through segments, emails, and flows"
- "Data Cloud is the intelligence layer that makes MCA campaigns smarter"

**Transition to Stop 6:** "Now let's see how the campaign performed."

---

## Enhancement #6: Reporting Setup (Demo Stop 6 -- 7 min)

### Purpose

Prepare reporting screens or narrative for campaign performance metrics. Reporting data may be sparse in a demo org, so this enhancement prepares both a live-data path and a narrative fallback.

### Step 1: Check Available Reporting Data

```bash
# Check if any email send/engagement data exists
sf data query --query "SELECT COUNT(Id) total FROM Campaign WHERE NumberSent > 0" \
  --target-org carmax-sdo-mm-app-wz95pw

# Check campaign member response status
sf data query --query "SELECT Campaign.Name, Status, COUNT(Id) cnt FROM CampaignMember GROUP BY Campaign.Name, Status ORDER BY Campaign.Name" \
  --target-org carmax-sdo-mm-app-wz95pw
```

### Step 2A: If Reporting Data Exists -- Pre-Open Tabs

1. Navigate to the Hearted Vehicle Follow-Up campaign record
2. Click the "Campaign Statistics" or reporting tab
3. Leave this tab open
4. Navigate to Setup > Flows > CarMax Vehicle Interest Nurture flow
5. Click the flow analytics/reporting tab (if available)
6. Leave this tab open

### Step 2B: If Reporting Data Is Sparse -- Prepare Narrative Fallback

When the demo org has not had actual sends, use these example metrics for the narrative. These are industry-realistic numbers that demonstrate the optimization story:

| Metric | Value | Industry Benchmark | CarMax Target |
|--------|-------|--------------------|---------------|
| Send Volume | ~1,000 emails | N/A | N/A |
| Open Rate | 42% | 35% (automotive) | >35% |
| Click-to-Listing Rate | 8.5% | 5% (automotive) | >12% |
| SMS Follow-Up Conversion | 22% | 15% (cross-channel) | >15% |
| Test Drive Booking Rate | 6.1% | 3% (automotive) | >5% |
| Pre-Qual Start Rate | 9.2% | N/A | >8% |
| Purchase Conversion (30-day) | 3.4% | 2% (automotive) | >3% |

**Flow Branch Breakdown (narrative):**
- 100% entered flow from P1 segment
- 4% suppressed (recent purchasers)
- 96% received email
- 42% opened email
- 8.5% clicked (engaged -- exited flow)
- 33.5% opened but didn't click (sent SMS follow-up)
- 54% didn't open (sent softer reminder email)

**Key Optimization Insight:**
"The SMS follow-up for openers-who-didn't-click has a 22% conversion rate -- significantly higher than the reminder email at 4.8%. This tells us SMS is the more effective channel for engaged-but-not-converted customers. Recommendation: shift more traffic to the SMS branch."

### Demo Narrative for Stop 6

1. **Campaign-Level Reporting:** Show send volume, open rates, click rates (live data or narrative fallback)
2. **Flow-Level Analytics:** How many entered, how many suppressed, how many engaged at each branch
3. **Branch Breakdown:** What percentage clicked, opened-no-click (got SMS), didn't open (got reminder)
4. **Optimization Opportunity:** "The SMS follow-up for openers-who-didn't-click has a 22% conversion rate -- higher than the reminder email. Let's shift more traffic to SMS."
5. **Segment Growth:** Show member count trends over time

**Talk Track:**
- "Reporting closes the loop -- every decision in the flow becomes a data point for optimization"
- "The marketer can see which branch is performing and adjust in real-time"
- "This isn't just reporting -- it's the foundation for continuous optimization"

**Transition to Stop 7:** "What if the campaign could optimize itself?"

---

## Enhancement #7: Dynamic Feedback Loop Concept (Demo Stop 7 -- 6 min)

### Purpose

Present the vision of self-improving campaigns where in-email interactions feed back into Data Cloud. This stop is conceptual -- no live demonstration of the writeback loop. The architecture from Phases 1-8 provides the foundation; this stop paints the future-state vision.

### Visual Explainer -- The Feedback Loop Cycle

```
  [1] Customer receives email with vehicle cards
        |
        v
  [2] Customer clicks "heart" on a vehicle in the email
        |
        v
  [3] Click event captured by MCA email tracking
        |
        v
  [4] Event flows back to Data Cloud via streaming ingestion
        |
        v
  [5] Data Cloud updates IsHearted on Vehicle DMO (CarMax_Vehicle__dlm)
        |
        v
  [6] Data Graph refreshes -- new heart reflected in Customer 360
        |
        v
  [7] Calculated Insights recalculate -- Propensity score increases
        |
        v
  [8] Next email send includes the newly hearted vehicle
        |
        v
  [9] Cycle repeats -- each interaction makes the next one smarter
        |
        v
  [Back to 1]
```

### Technical Foundation (Already Built in Phases 1-8)

These components are in place and support the feedback loop concept:

| Component | Phase | Status | Role in Loop |
|-----------|-------|--------|-------------|
| Email click tracking | Phase 7 (Email) | Built | Captures the click event |
| Web Engagement DMO | Phase 2 (Data Cloud) | Built | Stores engagement events |
| IngestAPI connection | Phase 2 (Data Cloud) | Built (if used) | Real-time ingestion path |
| Data Graph | Phase 4 | Built | Reflects updated vehicle data |
| Dynamic loop email | Phase 7 (Email) | Built | Renders personalized content from graph |
| Calculated Insights | Phase 3 | Materialized | Recalculates scores from updated data |
| Segment qualification | Phase 5 | Published | Audience membership adjusts dynamically |

### What Would Complete the Loop (Future Implementation)

These components would close the loop in a production implementation:

1. **Custom click handler:** An MCA-triggered automation that captures the specific vehicle clicked and writes it back to Data Cloud as a new web engagement event
2. **Real-time data stream:** An IngestAPI event stream that accepts click events in near-real-time (vs batch CRM sync)
3. **Real-time graph type:** Upgrading the Data Graph from `NONE` (standard/warm) to `REALTIME` for sub-second data freshness
4. **Automated CI refresh:** Triggering Calculated Insight materialization after each data update (currently on 6-hour schedule)

### Demo Narrative for Stop 7

1. Show the feedback loop diagram (whiteboard, slide, or verbal walkthrough)
2. Connect each step to what was already built: "The Data Graph, the dynamic loop email, the click tracking -- all the pieces are in place"
3. Explain the missing piece: "The writeback -- getting the click event from the email back into Data Cloud -- is the last mile"
4. Future vision: "Imagine a marketing engine that gets smarter with every send. Every click updates the profile, every profile update changes the next email. This is the vision of a self-improving marketing system."

**Talk Track:**
- "Every interaction becomes a data signal that improves the next touchpoint"
- "This isn't theory -- the architecture is already here. The writeback is the last piece."
- "Imagine a marketing engine that gets smarter with every send"

**Note:** This stop is conceptual. Do NOT attempt to demonstrate the writeback live -- it is not yet implemented.

**Transition to Stop 8:** "Let's wrap up with the executive view."

---

## Enhancement #8: Demo Day Checklist

### Pre-Demo Verification Script (Run 1 hour before demo)

This comprehensive script checks ALL demo components across all phases:

```bash
#!/bin/bash
# ============================================
# CarMax MCA Demo -- Pre-Demo Verification
# Run 1 hour before demo
# ============================================

ORG="carmax-sdo-mm-app-wz95pw"

echo "============================================"
echo "  CarMax MCA Demo -- Pre-Demo Verification"
echo "  Run at: $(date)"
echo "============================================"
echo ""

# --- 1. Contacts exist ---
echo "=== CHECK 1: Demo Contacts ==="
sf data query --query "SELECT FirstName, LastName, Email FROM Contact WHERE LastName IN ('Dawson','Thompson') ORDER BY LastName" \
  --target-org $ORG
echo ""

# --- 2. Campaigns exist ---
echo "=== CHECK 2: Campaigns (expect 10) ==="
sf data query --query "SELECT Name, Type, Status, IsActive, NumberOfContacts FROM Campaign ORDER BY Name" \
  --target-org $ORG
echo ""

# --- 3. DMOs have data ---
echo "=== CHECK 3: DMO Record Counts ==="

echo "--- Individual ---"
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST --target-org $ORG \
  --body '{"sql":"SELECT COUNT(*) AS cnt FROM ssot__Individual__dlm"}' 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Count: {data}')
except: print('  ERROR reading response')
"

echo "--- Vehicle ---"
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST --target-org $ORG \
  --body '{"sql":"SELECT COUNT(*) AS cnt FROM CarMax_Vehicle__dlm"}' 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Count: {data}')
except: print('  ERROR reading response')
"

echo "--- Test Drive ---"
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST --target-org $ORG \
  --body '{"sql":"SELECT COUNT(*) AS cnt FROM CarMax_TestDrive__dlm"}' 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Count: {data}')
except: print('  ERROR reading response')
"

echo "--- Web Engagement ---"
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST --target-org $ORG \
  --body '{"sql":"SELECT COUNT(*) AS cnt FROM ssot__WebsiteEngagement__dlm"}' 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Count: {data}')
except: print('  ERROR reading response')
"
echo ""

# --- 4. CIs are materialized ---
echo "=== CHECK 4: Calculated Insights (expect all ACTIVE/SUCCESS) ==="
for CI_NAME in Customer_Lifetime_Value Propensity_to_Buy Vehicle_Preference_Affinity Engagement_Velocity; do
  echo "--- ${CI_NAME} ---"
  sf api request rest \
    --url "/services/data/v65.0/ssot/calculated-insights/${CI_NAME}__cio" \
    --target-org $ORG 2>/dev/null | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(f'  Status: {d.get(\"calculatedInsightStatus\",\"UNKNOWN\")}')
    print(f'  Last Run: {d.get(\"lastRunStatus\",\"UNKNOWN\")}')
except: print('  ERROR reading response')
" 2>/dev/null
done
echo ""

# --- 5. Data Graph exists and is built ---
echo "=== CHECK 5: Data Graph ==="
sf data query --query "SELECT Id, Name, Status, DataGraphType FROM DataGraph WHERE Name LIKE '%CarMax%'" \
  --target-org $ORG
echo ""

# --- 6. Segments exist ---
echo "=== CHECK 6: Segments ==="
sf data query --query "SELECT Id, Name, Status FROM Segment WHERE Name LIKE '%CarMax%' OR Name LIKE '%Vehicle Interest%' OR Name LIKE '%Hearted%' OR Name LIKE '%Test Drive%' OR Name LIKE '%Memorial%' ORDER BY Name" \
  --target-org $ORG 2>/dev/null || echo "  (Segment query failed -- verify via UI)"
echo ""

# --- 7. Flow exists ---
echo "=== CHECK 7: Flows ==="
sf data query --query "SELECT Id, MasterLabel, Status, ProcessType FROM FlowDefinition WHERE MasterLabel LIKE '%CarMax%' OR MasterLabel LIKE '%Vehicle Interest%'" \
  --target-org $ORG 2>/dev/null || echo "  (FlowDefinition query may need adjustment -- verify via UI)"
echo ""

# --- 8. Campaign Brief exists (if DICE_CBB available) ---
echo "=== CHECK 8: Campaign Brief ==="
sf data query --query "SELECT Id, Name, DICE_CBB_Status__c FROM DICE_CBB_CampaignBrief__c WHERE Name = 'Hearted Vehicle Re-Engagement Brief'" \
  --target-org $ORG 2>/dev/null || echo "  DICE_CBB not installed -- brief check skipped"
echo ""

# --- 9. Jane Dawson hearted vehicles ---
echo "=== CHECK 9: Jane Dawson Hearted Vehicles (expect 3) ==="
sf api request rest '/services/data/v58.0/ssot/query' \
  --method POST --target-org $ORG \
  --body '{"sql":"SELECT Make__c, Model__c, Year__c, IsHearted__c FROM CarMax_Vehicle__dlm WHERE IsHearted__c = '"'"'true'"'"'"}' 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Result: {data}')
except: print('  ERROR reading response')
"
echo ""

echo "============================================"
echo "  Verification Complete"
echo "  Review each check above for PASS/FAIL"
echo "============================================"
```

### Readiness Checklist (Manual Verification)

Run through this checklist after the script completes. Check each item in the Salesforce UI where indicated:

- [ ] **Campaign Agent brief pre-created** (fallback for Stop 1) -- verify DICE_CBB record exists or narrative fallback prepared
- [ ] **Einstein and Waterfall segments published with members** -- Data Cloud > Segments > verify Published status and member counts > 0
- [ ] **Calculated Insights materialized with data** -- all 4 CarMax CIs show ACTIVE status and SUCCESS last run
- [ ] **Data Graph built and operational** -- Data Cloud > Data Graphs > CarMax Customer 360 shows Built status (Save and Build completed in UI)
- [ ] **Flagship email built with dynamic loop previewing correctly** -- Marketing App > Content > Emails > open email > Preview > select Jane Dawson > 3 vehicle cards render
- [ ] **Jane Dawson has 3 hearted vehicles** -- verified in DMO query (Ford Expedition XLT, Toyota 4Runner SR5, Hyundai Santa Fe SEL)
- [ ] **Aisha Thompson has 0 hearted vehicles** -- verified in DMO query (count = 0)
- [ ] **Primary flow deployed and activated** -- Setup > Flows > CarMax Vehicle Interest Nurture > Status = Active
- [ ] **SMS channel configured and tested** -- Marketing App > Messaging > sender profile exists
- [ ] **Supporting flows created** -- 4 additional flows visible in flow list (Welcome, Price Drop, Instant Offer, Saved Search)
- [ ] **All demo tabs pre-opened in browser** -- see Browser Tab Strategy below
- [ ] **Reporting screens seeded or fallback narrative ready** -- either real data visible in reports or narrative metrics memorized
- [ ] **Session timeout verified** -- logged in fresh within 15 minutes of demo start

### Browser Tab Strategy (Pre-Open Before Demo)

Open these tabs in order. This is the sequence you will navigate during the demo:

| Tab # | Content | Demo Stop | URL Path |
|-------|---------|-----------|----------|
| 1 | Campaign Agent / Campaign List | Stop 1 | `/lightning/o/Campaign/list` |
| 2 | Campaign Brief record | Stop 1 (fallback) | `/lightning/r/DICE_CBB_CampaignBrief__c/{ID}/view` |
| 3 | Data Cloud Segments | Stop 2 | Data Cloud > Segments |
| 4 | Calculated Insights | Stop 2 | Data Cloud > Calculated Insights |
| 5 | Jane Dawson Individual profile | Stop 2 + Stop 5 | Data Cloud > Individuals > Jane Dawson |
| 6 | Flagship email in Email Builder | Stop 3 | Marketing App > Content > Emails > Hearted Vehicle Follow-Up |
| 7 | Data Graph definition | Stop 3 + Stop 5 | Data Cloud > Data Graphs > CarMax Customer 360 |
| 8 | Flow Builder | Stop 4 | Setup > Flows > CarMax Vehicle Interest Nurture |
| 9 | Marketing App Messaging | Stop 4 | Marketing App > Messaging |
| 10 | Campaign Reporting | Stop 6 | Campaign > Hearted Vehicle Follow-Up > Statistics |

**Tab management tips:**
- Use Chrome tab groups: "Stop 1-2", "Stop 3-4", "Stop 5-6", "Stop 7-8"
- Pin the most-used tabs (Individual profile, Email Builder, Flow Builder)
- Pre-load all tabs BEFORE the demo starts to avoid load time during stops

---

## Demo Stop Quick-Nav URLs (Updated for v4 -- 90 min)

| Stop | Topic | Duration | URL Path / Navigation |
|------|-------|----------|----------------------|
| Dock | Business Framing | 5 min | N/A (presentation) |
| Stop 1 | Campaign Agent | 12 min | `/lightning/o/Campaign/list` > Campaign Agent |
| Stop 2 | Segmentation + CIs + Waterfall | 18 min | Data Cloud > Segments + CIs + Individual Profile |
| Stop 3 | Dynamic Email + Data Graph | 14 min | Marketing App > Content > Emails |
| Stop 4 | MCA Flow + SMS | 14 min | Setup > Flows + Marketing App > Messaging |
| Stop 5 | Data Cloud Customer 360 | 8 min | Data Cloud > Individuals > Jane Dawson + Data Graphs |
| Stop 6 | Reporting & Optimization | 7 min | Campaign > Hearted Vehicle Follow-Up > Statistics |
| Stop 7 | Dynamic Feedback Loop | 6 min | Concept presentation (whiteboard/slide) |
| Stop 8 | Wrap & Executive Recap | 4 min | N/A (presentation) |
| Buffer | Q&A | 2 min | Any stop for deep dives |

---

## Demo Flow Timing Guide (v4 -- 90 min)

| Stop | Topic | Target Duration | Cumulative | Key Action |
|------|-------|----------------|------------|------------|
| Dock | Business Framing | 5 min | 5 min | Set context, introduce personas |
| 1 | Campaign Agent Brief | 12 min | 17 min | Live prompt or pre-loaded brief walkthrough |
| 2 | Segmentation + CIs + Waterfall | 18 min | 35 min | 3-segment overlap, Jane Dawson waterfall resolution |
| 3 | Dynamic Email + Data Graph | 14 min | 49 min | Jane vs Aisha persona preview, dynamic loop |
| 4 | MCA Flow + SMS | 14 min | 63 min | Flow canvas walkthrough, live SMS authoring |
| 5 | Data Cloud Customer 360 | 8 min | 71 min | Jane's unified profile, Data Graph visual |
| 6 | Reporting & Optimization | 7 min | 78 min | Performance metrics, SMS optimization insight |
| 7 | Dynamic Feedback Loop | 6 min | 84 min | Concept pitch, future vision |
| 8 | Wrap & Executive Recap | 4 min | 88 min | 5-point recap |
| -- | Buffer/Q&A | 2 min | 90 min | Questions, deeper dives |

**Timing discipline:**
- Stop 2 (18 min) is the longest stop. If it runs over, borrow from Stop 5 (reduce to 6 min) or Stop 6 (reduce to 5 min).
- Stop 1 has a natural escape valve: switch from live generation (Option A) to pre-loaded brief (Option B) to save 3-4 minutes.
- The 2-min buffer is genuinely 2 minutes. If running late, skip the buffer and close with the 5-point recap.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Campaign Agent slow or unresponsive | Stop 1 stalls, audience loses momentum | Show pre-created brief as fallback. Transition: "Here's what Campaign Agent would generate." |
| Segment membership empty | Stop 2 loses the waterfall "aha moment" | Show segment rules and explain the logic. Use Jane's qualifying data queries to prove she would qualify. |
| Email preview broken or dynamic loop not rendering | Stop 3 breaks -- no vehicle cards visible | Show email in builder mode (component view). Walk through the HTML blocks and explain what would render. |
| Data Graph not built (status is READY, not BUILT) | Stop 3 + Stop 5 break -- graph data unavailable | Show graph definition and explain the architecture. If time permits, trigger build in UI (takes 2-5 min). |
| Flow not activating (stays in Draft or has validation errors) | Stop 4 breaks -- cannot show active flow | Walk through canvas in Draft mode. Explain each element's purpose. "In production, this would be activated." |
| SMS channel not configured (no sender profile) | Stop 4 SMS portion cannot be demonstrated | Focus on flow walkthrough. Skip live SMS authoring. Verbally describe the SMS branch behavior. |
| Data Cloud query latency (SSOT queries take 5-10 seconds) | Awkward pauses during Stops 2 and 5 | Pre-open ALL query-dependent tabs before the demo. Never run a live SSOT query during the demo. |
| Reporting data sparse (no actual email sends in demo org) | Stop 6 appears thin or empty | Use seeded/historical example metrics from Enhancement #6 narrative fallback. Verbalize the numbers confidently. |
| Session timeout during demo | Demo interruption requiring re-authentication | Log in fresh 15 minutes before demo start. Verify session is active by navigating to a page. Some SDO orgs have 2-hour timeout; some have 30 minutes. |

---

## Critical Notes & Gotchas

### 1. Campaign Brief Builder May Not Be Installed
`DICE_CBB_CampaignBrief__c` is a managed package that ships with certain SDO builds. Always verify with the query in Enhancement #1 Step 1 before attempting brief operations. If not available, Stop 1 uses a narrative-only approach.

### 2. Persona Previews Require Published Email
The email must be in Published (not Draft) state for persona preview to work with Data Graph data. If the email is in Draft, the dynamic loop may not resolve against the graph. Verify email status before the demo.

### 3. Jane Dawson MUST Have 3 Hearted Vehicles
This is non-negotiable. The entire persona preview and waterfall demo depends on Jane having exactly 3 hearted SUVs in the Vehicle DMO (`CarMax_Vehicle__dlm`). If she has fewer, the vehicle cards will not render as expected. Verify with the SSOT query in Enhancement #2 Step 2.

### 4. Aisha Thompson MUST NOT Have Hearted Vehicles
The contrast between Jane and Aisha is the visual proof of personalization. If Aisha has hearted vehicles, the fallback content will not render and the "Create an Account" / "Get Pre-Qualified" blocks will not show. Verify count = 0.

### 5. SMS Authoring Requires SMS Channel Setup
The live SMS authoring in Stop 4 requires a configured SMS sender profile in the Marketing App. If SMS is not configured, prepare to skip the live authoring and focus on the flow canvas walkthrough. The SMS branch in the flow is still demonstrable as architecture even without a configured channel.

### 6. Data Cloud Query Latency -- Pre-Open Tabs
SSOT queries can take 3-10 seconds depending on data volume and org load. NEVER run a live SSOT query during the demo. Pre-open all Data Cloud tabs (Individual profile, Segments, CIs) before the demo. The data will be cached in the browser.

### 7. Flow Builder Load Time -- Pre-Open Tab
MCA Flow Builder can take 10-15 seconds to load the canvas, especially for flows with many elements. Pre-open the Flow Builder tab with the CarMax Vehicle Interest Nurture flow before the demo.

### 8. Browser Tab Strategy
With 10 pre-opened tabs, use Chrome tab groups to organize by demo stop. Label groups: "Stop 1-2", "Stop 3-4", "Stop 5-6", "Stop 7-8". This prevents fumbling between stops. Practice the tab switching order during rehearsal.

### 9. Fallback Plan for Each Stop
Every stop has a fallback. Memorize them:
- Stop 1: Pre-loaded brief instead of live generation
- Stop 2: Show segment rules instead of live membership
- Stop 3: Show builder mode instead of rendered preview
- Stop 4: Walk through Draft flow instead of Active flow
- Stop 5: Show SSOT query results instead of UI profile (pre-queried)
- Stop 6: Narrative metrics instead of live reports
- Stop 7: Always conceptual (no fallback needed)

### 10. Demo Org Session Timeout
SDO orgs have variable session timeout settings (30 min to 2 hours). Log in fresh 15 minutes before the demo. Do not rely on a session from earlier in the day. After logging in, navigate to at least 3 different pages to confirm the session is warm.

### 11. Data Cloud 360 Stop (Stop 5) Requires All DMO Data Populated and CIs Materialized -- NEW in v4
This is the NEW dedicated stop that was not in v3. It requires ALL data layers to be populated: Vehicle records, Test Drive records, Web Engagement records, all 4 CIs materialized, Data Graph built, and segments published. If any layer is missing, the Customer 360 view will appear incomplete. Run the full verification script (Enhancement #8) to confirm.

### 12. 90-Minute Timing Is Tight -- Practice Transitions Between Stops -- NEW in v4
At 90 minutes with 9 stops + buffer, transitions between stops must be smooth and fast. Each transition should take less than 15 seconds (one tab switch + one sentence). Practice the full run-through at least twice before demo day. The first rehearsal will likely run 100-110 minutes. Use that to identify which stops need tightening.

---

## Phase 9 Completion Checklist

- [ ] Enhancement #1 complete: Campaign Brief verified or created, Stop 1 narrative prepared
- [ ] Enhancement #2 complete: Jane Dawson waterfall data verified across all 3 tiers, CI scores confirmed
- [ ] Enhancement #3 complete: Both persona previews verified (Jane = 3 cards, Aisha = fallback), email in Published state
- [ ] Enhancement #4 complete: SMS content pre-staged, navigation path documented, SMS channel verified (or fallback noted)
- [ ] Enhancement #5 complete: Jane's 360 profile pre-opened, all data layers verified, Data Graph built
- [ ] Enhancement #6 complete: Reporting tabs pre-opened or narrative fallback metrics memorized
- [ ] Enhancement #7 complete: Feedback loop diagram prepared, talk track rehearsed
- [ ] Enhancement #8 complete: Pre-demo verification script run successfully, all readiness checklist items checked, browser tabs pre-opened in correct order
- [ ] Full 90-minute run-through completed at least once
- [ ] All fallback plans documented and memorized for each stop

---

## Estimated Execution Time

| Enhancement | Duration | Notes |
|-------------|----------|-------|
| #1: Campaign Agent Brief | 10-15 min | Mostly verification; creation only if brief missing |
| #2: Waterfall Verification | 15-20 min | Multiple SSOT queries + CI data checks |
| #3: Persona Preview Setup | 10-15 min | Data verification + email preview testing |
| #4: SMS Prep | 5-10 min | Channel verification + content staging |
| #5: Data Cloud 360 Prep | 15-20 min | Comprehensive data layer verification (NEW) |
| #6: Reporting Setup | 10-15 min | Tab pre-loading or narrative preparation |
| #7: Feedback Loop Prep | 5-10 min | Diagram/slide preparation + talk track review |
| #8: Demo Day Checklist | 15-20 min | Full verification script + manual checklist |
| **Total** | **85-125 min** | First pass; faster on subsequent runs |

---

## Phase > Demo Stop Cross-Reference (All Phases)

| Phase | Component | Demo Stop(s) | Critical for Demo? |
|-------|-----------|-------------|-------------------|
| Phase 1 | Custom Objects + Demo Data | All | YES -- foundation layer |
| Phase 2 | Data Cloud DMOs + Mappings | Stop 2, 3, 4, 5 | YES -- powers segmentation and personalization |
| Phase 3 | Calculated Insights (4 CIs) | Stop 2, 5 | YES -- scoring and enrichment |
| Phase 4 | Data Graph (CarMax Customer 360) | Stop 3, 5 | YES -- powers dynamic email loop |
| Phase 5 | Segments (Waterfall + Einstein) | Stop 2, 4 | YES -- audience targeting |
| Phase 6 | Campaigns + Briefs | Stop 1 | YES (brief) / Supporting (campaigns) |
| Phase 7 | Email Content | Stop 3 | YES -- flagship email |
| Phase 8 | Flows + SMS | Stop 4 | YES -- orchestration |
| **Phase 9** | **Demo Enhancements** | **All** | **YES -- polish and verification** |
