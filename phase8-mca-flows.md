# Phase 8: MCA Flows (Segment-Triggered Journeys) — Implementation Plan

## Overview
Build the primary MCA segment-triggered flow ("Vehicle Interest Nurture") and 4 supporting flows that orchestrate email/SMS sends, decision splits, wait elements, and suppression logic. In MCA, flows ARE the journey orchestration engine — they replace Journey Builder from MC Engagement. Segment-triggered flows use Data Cloud segment membership as entry criteria, making segments (Phase 5) the bridge between audience intelligence and execution.

**Org:** `carmax-sdo-mm-app-wz95pw`
**Flow Type:** Segment-Triggered Flow (AutoLaunchedFlow with triggerType: Segment)
**Prerequisite:** Phase 5 (Segments published) + Phase 7 (Email content created in CMS)

---

## MCA Context: Flows vs Journey Builder

| Aspect | MC Engagement Journey Builder | MCA Segment-Triggered Flows |
|--------|------------------------------|----------------------------|
| Platform | Marketing Cloud infrastructure | Salesforce Flow infrastructure |
| Entry | List/DE membership, API events | Data Cloud segment membership |
| Builder | Journey Builder canvas | Flow Builder (same as admin flows) |
| Actions | MC activities (email, SMS, wait) | Flow actions (sendEmailMessage, wait, decision) |
| Data context | Data Extensions, AMPscript | Data Graph, Handlebars JS |
| Engagement events | Journey Analytics | Wait Until Event (EmailLinkClickEvent, etc.) |
| Knowledge base | Marketing team only | Same Flow Builder admins already know |

**Key reframe:** MCA Flows are NOT a separate system. They are standard Salesforce Flows (`processType: AutoLaunchedFlow`) with a `triggerType: Segment` start element. Any admin who has built a record-triggered or scheduled flow already knows the builder. The only new concepts are the marketing-specific actions (Send Email Message, Send SMS Message) and the Wait Until Event element that listens for engagement signals (opens, clicks, bounces). This is a massive adoption advantage over Journey Builder, which required dedicated Marketing Cloud expertise.

---

## Architecture Overview

MCA Flows are Salesforce Flows with `processType: AutoLaunchedFlow` and `triggerType: Segment`. They are entered by members of a Data Cloud segment and support:
- **Send Email Message** action (sends CMS email content)
- **Wait** elements (time-based delays)
- **Wait Until Event** elements (wait for email open, click, bounce)
- **Decision** elements (branching logic)
- **Send SMS** action (for multi-channel flows)

### Primary Flow: Vehicle Interest Nurture

```
SEGMENT ENTRY (Vehicle Interest Waterfall — Priority 1: Hearted Vehicle)
    │
    ├── [Wait 2 Hours]
    │
    ├── [Decision: Recent Purchaser?]
    │   ├── YES → END (Suppress)
    │   └── NO → Continue
    │
    ├── [Send Email: "Compare What Matters" — Hearted Vehicle Follow-Up]
    │
    ├── [Wait Until Event: Email Link Click — 3 day timeout]
    │   ├── CLICKED → END (Engaged — let retargeting handle)
    │   └── TIMEOUT (No Click) → Continue
    │
    ├── [Decision: Did Customer Open Email?]
    │   ├── YES (opened but no click) → [Send SMS: Test Drive Reminder]
    │   └── NO (no open) → [Send Email: "Still Thinking It Over?" — Softer Reminder]
    │
    └── END
```

This flow demonstrates 6 MCA capabilities in a single canvas:
1. **Segment entry** — Data Cloud audience as trigger
2. **Time-based wait** — 2-hour cooling period
3. **Suppression logic** — Recent purchaser exclusion via decision element
4. **Email send** — CMS content with Data Graph personalization
5. **Engagement-based wait** — Wait Until Event listening for link clicks
6. **Multi-channel branching** — SMS for openers, email for non-openers

---

## Important: Flow Build Approach

MCA segment-triggered flows can be built two ways:

| Method | Pros | Cons |
|--------|------|------|
| **Metadata Deploy** (XML) | Repeatable, version-controlled, automated | Requires exact IDs for email content, sender, subscriptions |
| **Flow Builder UI** | Visual, drag-and-drop, easier to configure send elements | Manual, not version-controlled |

**Recommended:** Use a **hybrid approach** —
1. Deploy the flow skeleton via metadata (start element, wait elements, decision elements)
2. Configure the Send Email Message actions via the Flow Builder UI (requires selecting CMS content, sender, and subscription from pickers)

**Why hybrid?** The `sendEmailMessage` action requires Salesforce IDs for:
- `contentId` — CMS email content reference (format: `marketing--Default_Content_Workspace.sfdc_cms__email--{API_NAME}`)
- `senderId` — OrgWideEmailAddress ID (prefix: `35a`)
- `communicationSubscriptionId` — Communication Subscription ID (prefix: `0Xl`)
- `commSubscriptionChannelTypeId` — Channel Type ID (prefix: `0eB`)

These IDs vary per org and must be looked up at build time. The metadata approach gives us a repeatable skeleton; the UI pass lets us wire in org-specific IDs without manual XML surgery.

---

## Step 1: Look Up Required IDs

Before building the flow, gather the IDs needed for email send configuration.

### 1A. OrgWideEmailAddress (Sender)

```bash
sf data query --query "SELECT Id, Address, DisplayName FROM OrgWideEmailAddress" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Record the `Id` (35a prefix) for the sender you want to use. This is the "From" address on every email sent by the flow.

### 1B. Communication Subscription

```bash
sf data query --query "SELECT Id, Name FROM MessagingChannel WHERE IsActive = true" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Also check for Communication Subscriptions:
```bash
sf data query --query "SELECT Id, Name FROM CommSubscription" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Record the `Id` (0Xl prefix) for the email subscription. Communication Subscriptions are the consent management layer — every Send Email Message element MUST reference one.

### 1C. Communication Subscription Channel Type

```bash
sf data query --query "SELECT Id, Name, CommSubscriptionId FROM CommSubscriptionChannelType" \
  --target-org carmax-sdo-mm-app-wz95pw
```

Record the `Id` (0eB prefix) matching the email channel. This links the subscription to the specific channel (email vs SMS vs push).

### 1D. Segment ID

```bash
sf api request rest '/services/data/v65.0/ssot/segments?batchSize=20' \
  --target-org carmax-sdo-mm-app-wz95pw 2>&1 | grep -v "^Warning:" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for s in data.get('segments', []):
    name = s.get('displayName', '')
    if 'Waterfall' in name or 'Vehicle Interest' in name:
        print(f'{name}: {s.get(\"marketSegmentId\", \"\")}')
"
```

Record the `marketSegmentId` for the Vehicle Interest Waterfall segment. This is the segment that triggers flow entry — members of this segment (Priority 1: Hearted Vehicle) will enter the flow.

### 1E. CMS Email Content Keys

The email content references use the format:
```
marketing--Default_Content_Workspace.sfdc_cms__email--{EMAIL_API_NAME}
```

After Phase 7 emails are built in the CMS workspace, list them:
```bash
sf data query --query "SELECT Id, Name, ContentKey FROM ManagedContent WHERE Name LIKE '%CarMax%' OR Name LIKE '%Hearted%' OR Name LIKE '%Compare%'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

---

## Step 2: Deploy Flow via Metadata

### 2A. Create Project Structure

```bash
mkdir -p /tmp/carmax-flow/force-app/main/default/flows
```

### 2B. Create sfdx-project.json

```json
{
  "packageDirectories": [{ "path": "force-app", "default": true }],
  "name": "carmax-flow",
  "namespace": "",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "65.0"
}
```

Write to `/tmp/carmax-flow/sfdx-project.json`.

### 2C. Create Flow XML

**File:** `/tmp/carmax-flow/force-app/main/default/flows/CarMax_Vehicle_Interest_Nurture.flow-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">

    <!-- ===== ACTION CALLS ===== -->

    <!-- Send Email: Hearted Vehicle Follow-Up (flagship email) -->
    <actionCalls>
        <name>Send_Hearted_Vehicle_Email</name>
        <label>Send Hearted Vehicle Follow-Up</label>
        <locationX>176</locationX>
        <locationY>518</locationY>
        <actionName>sendEmailMessage</actionName>
        <actionType>sendEmailMessage</actionType>
        <connector>
            <targetReference>Wait_For_Link_Click</targetReference>
        </connector>
        <flowTransactionModel>CurrentTransaction</flowTransactionModel>
        <inputParameters>
            <name>contentId</name>
            <value>
                <stringValue>marketing--Default_Content_Workspace.sfdc_cms__email--CarMax_Hearted_Vehicle_FollowUp</stringValue>
            </value>
        </inputParameters>
        <inputParameters>
            <name>isTemplate</name>
            <value><booleanValue>false</booleanValue></value>
        </inputParameters>
        <inputParameters>
            <name>senderId</name>
            <value><stringValue>SENDER_ID_HERE</stringValue></value>
        </inputParameters>
        <inputParameters>
            <name>clickTracking</name>
            <value><booleanValue>true</booleanValue></value>
        </inputParameters>
        <inputParameters>
            <name>openTracking</name>
            <value><booleanValue>true</booleanValue></value>
        </inputParameters>
        <inputParameters>
            <name>communicationSubscriptionId</name>
            <value><stringValue>COMM_SUBSCRIPTION_ID_HERE</stringValue></value>
        </inputParameters>
        <inputParameters>
            <name>commSubscriptionChannelTypeId</name>
            <value><stringValue>CHANNEL_TYPE_ID_HERE</stringValue></value>
        </inputParameters>
        <inputParameters><name>outreachSourceCodeId</name></inputParameters>
        <inputParameters><name>selectedOfferIds</name></inputParameters>
        <nameSegment>sendEmailMessage</nameSegment>
        <offset>0</offset>
    </actionCalls>

    <!-- Send Email: Still Thinking It Over (softer reminder for non-openers) -->
    <actionCalls>
        <name>Send_Reminder_Email</name>
        <label>Send Still Thinking It Over</label>
        <locationX>440</locationX>
        <locationY>950</locationY>
        <actionName>sendEmailMessage</actionName>
        <actionType>sendEmailMessage</actionType>
        <flowTransactionModel>CurrentTransaction</flowTransactionModel>
        <inputParameters>
            <name>contentId</name>
            <value>
                <stringValue>marketing--Default_Content_Workspace.sfdc_cms__email--CarMax_Test_Drive_Nurture</stringValue>
            </value>
        </inputParameters>
        <inputParameters>
            <name>isTemplate</name>
            <value><booleanValue>false</booleanValue></value>
        </inputParameters>
        <inputParameters>
            <name>senderId</name>
            <value><stringValue>SENDER_ID_HERE</stringValue></value>
        </inputParameters>
        <inputParameters>
            <name>clickTracking</name>
            <value><booleanValue>true</booleanValue></value>
        </inputParameters>
        <inputParameters>
            <name>openTracking</name>
            <value><booleanValue>true</booleanValue></value>
        </inputParameters>
        <inputParameters>
            <name>communicationSubscriptionId</name>
            <value><stringValue>COMM_SUBSCRIPTION_ID_HERE</stringValue></value>
        </inputParameters>
        <inputParameters>
            <name>commSubscriptionChannelTypeId</name>
            <value><stringValue>CHANNEL_TYPE_ID_HERE</stringValue></value>
        </inputParameters>
        <inputParameters><name>outreachSourceCodeId</name></inputParameters>
        <inputParameters><name>selectedOfferIds</name></inputParameters>
        <nameSegment>sendEmailMessage</nameSegment>
        <offset>0</offset>
    </actionCalls>

    <!-- ===== DECISIONS ===== -->

    <!-- Decision: Is this a recent purchaser? (Suppression) -->
    <decisions>
        <name>Check_Recent_Purchase</name>
        <label>Recent Purchaser?</label>
        <locationX>176</locationX>
        <locationY>398</locationY>
        <defaultConnector>
            <targetReference>Send_Hearted_Vehicle_Email</targetReference>
        </defaultConnector>
        <defaultConnectorLabel>No — Continue</defaultConnectorLabel>
        <rules>
            <name>Is_Recent_Purchaser</name>
            <conditionLogic>and</conditionLogic>
            <conditions>
                <leftValueReference>$Record.ssot__Id__c</leftValueReference>
                <operator>IsNull</operator>
                <rightValue>
                    <booleanValue>false</booleanValue>
                </rightValue>
            </conditions>
            <label>Yes — Suppress</label>
        </rules>
    </decisions>

    <!-- Decision: Did customer open the email? (Post-wait branching) -->
    <decisions>
        <name>Check_Email_Opened</name>
        <label>Email Opened?</label>
        <locationX>308</locationX>
        <locationY>830</locationY>
        <defaultConnector>
            <targetReference>Send_Reminder_Email</targetReference>
        </defaultConnector>
        <defaultConnectorLabel>No Open — Send Reminder</defaultConnectorLabel>
        <rules>
            <name>Email_Was_Opened</name>
            <conditionLogic>and</conditionLogic>
            <conditions>
                <leftValueReference>$Record.ssot__Id__c</leftValueReference>
                <operator>IsNull</operator>
                <rightValue>
                    <booleanValue>false</booleanValue>
                </rightValue>
            </conditions>
            <label>Yes — Send SMS</label>
            <connector>
                <targetReference>Send_SMS_Follow_Up</targetReference>
            </connector>
        </rules>
    </decisions>

    <!-- ===== WAITS ===== -->

    <!-- Wait: 2-hour delay before first action -->
    <waits>
        <name>Wait_2_Hours</name>
        <label>Wait 2 Hours</label>
        <locationX>176</locationX>
        <locationY>278</locationY>
        <defaultConnectorLabel>Timeout</defaultConnectorLabel>
        <waitEvents>
            <name>Two_Hour_Delay</name>
            <conditionLogic>and</conditionLogic>
            <connector>
                <targetReference>Check_Recent_Purchase</targetReference>
            </connector>
            <eventType>AlarmEvent</eventType>
            <inputParameters>
                <name>AlarmTime</name>
                <value>
                    <elementReference>$Flow.CurrentDateTime</elementReference>
                </value>
            </inputParameters>
            <inputParameters>
                <name>TimeOffset</name>
                <value>
                    <numberValue>2</numberValue>
                </value>
            </inputParameters>
            <inputParameters>
                <name>TimeOffsetUnit</name>
                <value>
                    <stringValue>Hours</stringValue>
                </value>
            </inputParameters>
            <label>After 2 Hours</label>
        </waitEvents>
    </waits>

    <!-- Wait Until Event: Email Link Click (3-day timeout) -->
    <waits>
        <name>Wait_For_Link_Click</name>
        <label>Wait for Link Click</label>
        <locationX>176</locationX>
        <locationY>638</locationY>
        <defaultConnector>
            <targetReference>Check_Email_Opened</targetReference>
        </defaultConnector>
        <defaultConnectorLabel>Timeout — No Click</defaultConnectorLabel>
        <waitEvents>
            <name>Link_Clicked</name>
            <conditionLogic>and</conditionLogic>
            <eventType>EmailLinkClickEvent</eventType>
            <inputParameters>
                <name>FlowActionToMonitor</name>
                <value>
                    <stringValue>Send_Hearted_Vehicle_Email</stringValue>
                </value>
            </inputParameters>
            <inputParameters>
                <name>Link</name>
                <value>
                    <stringValue>AnyLink</stringValue>
                </value>
            </inputParameters>
            <inputParameters>
                <name>TimeoutDays</name>
                <value>
                    <numberValue>3</numberValue>
                </value>
            </inputParameters>
            <label>Email Link Clicked</label>
        </waitEvents>
    </waits>

    <!-- ===== PLACEHOLDER: SMS SEND ===== -->
    <!-- SMS sends are configured via UI — placeholder assignment to mark the flow path -->
    <assignments>
        <name>Send_SMS_Follow_Up</name>
        <label>Send SMS Follow-Up (Configure in UI)</label>
        <locationX>176</locationX>
        <locationY>950</locationY>
        <assignmentItems>
            <assignToReference>$Flow.CurrentDateTime</assignToReference>
            <operator>Assign</operator>
            <value>
                <elementReference>$Flow.CurrentDateTime</elementReference>
            </value>
        </assignmentItems>
    </assignments>

    <!-- ===== FLOW METADATA ===== -->
    <apiVersion>65.0</apiVersion>
    <areMetricsLoggedToDataCloud>true</areMetricsLoggedToDataCloud>
    <dataSpace>default</dataSpace>
    <environments>Default</environments>
    <interviewLabel>CarMax Vehicle Interest Nurture {!$Flow.CurrentDateTime}</interviewLabel>
    <label>CarMax Vehicle Interest Nurture</label>
    <processMetadataValues>
        <name>BuilderType</name>
        <value><stringValue>LightningFlowBuilder</stringValue></value>
    </processMetadataValues>
    <processMetadataValues>
        <name>CanvasMode</name>
        <value><stringValue>AUTO_LAYOUT_CANVAS</stringValue></value>
    </processMetadataValues>
    <processMetadataValues>
        <name>OriginBuilderType</name>
        <value><stringValue>LightningFlowBuilder</stringValue></value>
    </processMetadataValues>
    <processType>AutoLaunchedFlow</processType>
    <start>
        <locationX>50</locationX>
        <locationY>0</locationY>
        <connector>
            <targetReference>Wait_2_Hours</targetReference>
        </connector>
        <dataGraph>Marketing_Content_Personalizat</dataGraph>
        <object>UnifiedssotIndividualInd1__dlm</object>
        <publishSegment>true</publishSegment>
        <schedule>
            <dayOfMonthToRun>0</dayOfMonthToRun>
            <frequency>OnActivate</frequency>
            <frequencyNumber>0</frequencyNumber>
        </schedule>
        <segment>SEGMENT_ID_HERE</segment>
        <triggerType>Segment</triggerType>
    </start>
    <status>Draft</status>
    <timeZoneSidKey>America/New_York</timeZoneSidKey>
</Flow>
```

### 2D. Replace Placeholder IDs

Before deploying, replace these placeholders in the XML with actual IDs from Step 1:

| Placeholder | Source | Example |
|-------------|--------|---------|
| `SENDER_ID_HERE` | Step 1A — OrgWideEmailAddress.Id | `35aXXXXXXXXXXXXXXX` |
| `COMM_SUBSCRIPTION_ID_HERE` | Step 1B — CommSubscription.Id | `0XlXXXXXXXXXXXXXXX` |
| `CHANNEL_TYPE_ID_HERE` | Step 1C — CommSubscriptionChannelType.Id | `0eBXXXXXXXXXXXXXXX` |
| `SEGMENT_ID_HERE` | Step 1D — Waterfall segment marketSegmentId | Actual segment ID |

Use sed commands to replace:
```bash
cd /tmp/carmax-flow
sed -i 's/SENDER_ID_HERE/35aActualIdHere/g' force-app/main/default/flows/CarMax_Vehicle_Interest_Nurture.flow-meta.xml
sed -i 's/COMM_SUBSCRIPTION_ID_HERE/0XlActualIdHere/g' force-app/main/default/flows/CarMax_Vehicle_Interest_Nurture.flow-meta.xml
sed -i 's/CHANNEL_TYPE_ID_HERE/0eBActualIdHere/g' force-app/main/default/flows/CarMax_Vehicle_Interest_Nurture.flow-meta.xml
sed -i 's/SEGMENT_ID_HERE/ActualSegmentIdHere/g' force-app/main/default/flows/CarMax_Vehicle_Interest_Nurture.flow-meta.xml
```

### 2E. Deploy

```bash
cd /tmp/carmax-flow
sf project deploy start --source-dir force-app --target-org carmax-sdo-mm-app-wz95pw --wait 10
```

**Expected:** `Status: Succeeded` — Flow deploys in Draft status.

---

## Step 3: Configure Flow in UI (Post-Deploy)

After metadata deployment, open the flow in Flow Builder to complete configuration. The metadata gives us the skeleton; the UI pass wires in org-specific references that are difficult to manage in XML.

### 3A. Open Flow Builder

Navigate to: Setup → Flows → "CarMax Vehicle Interest Nurture" → Open Latest Version

Or direct URL: `https://{instance}.lightning.force.com/builder_platform_interaction/flowBuilder.app?flowId={FlowId}`

### 3B. Verify Start Element

Click the Start element and confirm:
- **Object:** UnifiedssotIndividualInd1__dlm
- **Segment:** Vehicle Interest Waterfall (or the segment name you chose)
- **Run Type:** Sync
- **Schedule:** On Activate (or configure a recurring schedule)
- **Data Graph:** Marketing_Content_Personalizat
- **Specify Email:** Contact Point Email DMO = Included (ssot__ContactPointEmail__dlm)

**CRITICAL:** If Contact Point Email DMO is NOT included in the Start element, the flow cannot resolve email addresses and emails will not send. This is the single most common configuration error in MCA Flow setup. The "Specify Email" section is in the Start element properties panel — scroll down to find it. The Contact Point Email DMO must be explicitly set to "Included" with `ssot__ContactPointEmail__dlm` selected.

### 3C. Configure SMS Action (Replace Placeholder)

The metadata deployed a placeholder assignment element for the SMS send path. Replace it with a real Send SMS Message action:

1. Click the "Send SMS Follow-Up (Configure in UI)" assignment element
2. Delete it
3. Add a new **Send SMS Message** element in its place
4. Configure:
   - **SMS Content:** Select the Test Drive Reminder SMS from CMS
   - **From Number:** Select the configured SMS sender
   - **Communication Subscription:** Same subscription as email

### 3D. Refine Decision: Recent Purchaser

The deployed decision uses a placeholder condition (`$Record.ssot__Id__c IsNull false` — always true). In the UI, update it to:
- **Condition:** Use a formula or Data Cloud attribute to check if the Individual has a Vehicle record where `IsPurchased__c = 'true'` AND `PurchaseDate__c` is within the last 30 days
- **True path:** End (suppress)
- **False path:** Continue to email send

**Note:** MCA Flow decisions can reference Data Cloud attributes through the data graph. The exact field path depends on how the graph exposes the Vehicle relationship.

### 3E. Refine Decision: Email Opened

Update this decision to use the Wait Until Event's output:
- **Condition:** Check if the email open event occurred (based on the Wait Until Event's event data)
- **True path (opened, no click):** Send SMS
- **False path (no open):** Send reminder email

**Note:** The Wait Until Event element for EmailLinkClickEvent has two outcomes: (1) the event fires (link clicked) or (2) the timeout expires. When the timeout expires, the flow continues to the "Email Opened?" decision. At this point, you can check whether an EmailOpenEvent occurred during the wait period to distinguish "opened but didn't click" from "never opened at all."

---

## Step 4: Build Additional Supporting Flows

Beyond the primary nurture flow, create 4 simpler flows for the remaining campaigns. These are built directly in Flow Builder UI rather than via metadata deploy — they are simple enough (2-4 elements each) that the visual builder is faster.

### 4A. Welcome Series Flow

```
SEGMENT ENTRY: New Email Subscribers
    │
    ├── [Send Email: "Welcome to CarMax"]
    │
    ├── [Wait 3 Days]
    │
    ├── [Decision: Engaged with Welcome Email?]
    │   ├── YES → [Send Email: "Get Pre-Qualified"]
    │   └── NO → END
    │
    └── END
```

**Build instructions:**
1. New Flow → Segment-Triggered Flow
2. Start element: Object = UnifiedssotIndividualInd1__dlm, Segment = New Email Subscribers
3. Data Graph = Marketing_Content_Personalizat, Contact Point Email DMO = Included
4. Add Send Email Message → Welcome to CarMax email from CMS
5. Add Wait → 3 Days (AlarmEvent, TimeOffset=3, TimeOffsetUnit=Days)
6. Add Decision → "Engaged?" — check for email open or click
7. YES path: Add Send Email Message → Get Pre-Qualified email from CMS
8. NO path: End
9. Save, keep in Draft

### 4B. Price Drop Alert Flow

```
SEGMENT ENTRY: Price Drop Alert Audience
    │
    ├── [Send Email: "Ready to Save?" — Price Drop Alert]
    │
    ├── [Wait Until Event: Email Link Click — 2 day timeout]
    │   ├── CLICKED → END (Engaged)
    │   └── TIMEOUT → [Send SMS: Price Drop Alert]
    │
    └── END
```

**Build instructions:**
1. New Flow → Segment-Triggered Flow
2. Start element: Object = UnifiedssotIndividualInd1__dlm, Segment = Price Drop Alert
3. Data Graph = Marketing_Content_Personalizat, Contact Point Email DMO = Included
4. Add Send Email Message → Price Drop Alert email from CMS
5. Add Wait Until Event → EmailLinkClickEvent, FlowActionToMonitor = Send Email action, TimeoutDays = 2
6. CLICKED path: End (engaged)
7. TIMEOUT path: Add Send SMS Message → Price Drop SMS
8. Save, keep in Draft

### 4C. Instant Offer Abandonment Flow

```
SEGMENT ENTRY: Instant Offer Abandonment
    │
    ├── [Wait 4 Hours]
    │
    ├── [Send Email: "Your Online Offer is Waiting"]
    │
    ├── [Wait 2 Days]
    │
    ├── [Send SMS: "Instant Offer Expiring"]
    │
    └── END
```

**Build instructions:**
1. New Flow → Segment-Triggered Flow
2. Start element: Object = UnifiedssotIndividualInd1__dlm, Segment = Instant Offer Abandonment
3. Data Graph = Marketing_Content_Personalizat, Contact Point Email DMO = Included
4. Add Wait → 4 Hours (AlarmEvent, TimeOffset=4, TimeOffsetUnit=Hours)
5. Add Send Email Message → Instant Offer Abandonment email from CMS
6. Add Wait → 2 Days (AlarmEvent, TimeOffset=2, TimeOffsetUnit=Days)
7. Add Send SMS Message → Instant Offer Expiring SMS
8. Save, keep in Draft

### 4D. Saved Search Match Flow

```
SEGMENT ENTRY: Saved Search Match
    │
    ├── [Send Email: "It's a Match!"]
    │
    ├── [Wait Until Event: Email Link Click — 3 day timeout]
    │   ├── CLICKED → END
    │   └── TIMEOUT → [Send SMS: Saved Search Match]
    │
    └── END
```

**Build instructions:**
1. New Flow → Segment-Triggered Flow
2. Start element: Object = UnifiedssotIndividualInd1__dlm, Segment = Saved Search Match
3. Data Graph = Marketing_Content_Personalizat, Contact Point Email DMO = Included
4. Add Send Email Message → Saved Search Match email from CMS
5. Add Wait Until Event → EmailLinkClickEvent, FlowActionToMonitor = Send Email action, TimeoutDays = 3
6. CLICKED path: End
7. TIMEOUT path: Add Send SMS Message → Saved Search Match SMS
8. Save, keep in Draft

**Note for all supporting flows:** Every Send Email Message element must have Communication Subscription set. Every Start element must have Contact Point Email DMO = Included. These two requirements are non-negotiable — missing either one causes silent send failures.

---

## Step 5: Activate and Test

### 5A. Activate the Primary Flow

In Flow Builder:
1. Click **"Activate"** in the top toolbar
2. Confirm activation

**Pre-activation checklist:**
- [ ] Run Type = Sync
- [ ] Contact Point Email DMO = Included
- [ ] Communication Subscription = set on ALL Send Email elements
- [ ] All email content is Published (not Draft)
- [ ] Sender address is verified
- [ ] Segment is in ACTIVE/PUBLISHED status
- [ ] All decision element conditions are valid
- [ ] Data Graph = Marketing_Content_Personalizat is selected
- [ ] SMS sender is configured (if SMS elements exist)
- [ ] Schedule frequency = OnActivate (for demo) or Daily (for recurring)

### 5B. Test with Jane Dawson

After activation:
1. Verify Jane Dawson is in the Vehicle Interest Waterfall segment (Priority 1)
2. Trigger the flow (the segment-triggered flow will execute on next publish cycle)
3. Check Flow execution history: Setup → Flows → CarMax Vehicle Interest Nurture → View Interviews
4. Verify email was sent to Jane Dawson's email
5. Confirm the 2-hour wait element is holding the flow (interview status = Waiting)

### 5C. Verify Flow Execution

```bash
# Check flow definition status
sf data query --query "SELECT Id, Status, ActiveVersionId, LatestVersionId FROM FlowDefinition WHERE DeveloperName='CarMax_Vehicle_Interest_Nurture'" \
  --target-org carmax-sdo-mm-app-wz95pw

# Check flow interviews (executions)
sf data query --query "SELECT Id, Status, CreatedDate FROM FlowInterview WHERE FlowDeveloperName='CarMax_Vehicle_Interest_Nurture' ORDER BY CreatedDate DESC LIMIT 10" \
  --target-org carmax-sdo-mm-app-wz95pw
```

---

## Flow → Segment → Demo Stop Mapping

| Flow | Entry Segment | Demo Stop | Purpose |
|------|--------------|-----------|---------|
| Vehicle Interest Nurture | Waterfall P1: Hearted Vehicle | Stop 4 | Main demo — decisions, waits, suppression, multi-channel |
| Welcome Series | New Email Subscribers | Stop 4 | Simple segment → email → wait → decision |
| Price Drop Alert | Price Drop Alert | Stop 4 | Urgency: email → wait for click → SMS |
| Instant Offer Abandonment | Instant Offer | Stop 4 | Time-delayed abandonment recovery |
| Saved Search Match | Saved Search | Stop 4 | Event-driven with engagement wait |

**Why all flows map to Stop 4:** In the harbor cruise demo (v4 plan), Stop 4 is "MCA Flow Orchestration." The primary flow is the walkthrough centerpiece (7 minutes). The supporting flows are shown briefly (2 minutes) to demonstrate that each segment has its own orchestration — all built on the same MCA Flow infrastructure.

---

## Demo Narrative for Stop 4

This is the 6-step walkthrough script for the primary Vehicle Interest Nurture flow during the harbor cruise demo:

1. **Open the primary flow** in Flow Builder — "Let's look at how MCA orchestrates the campaign we just built. This is the Vehicle Interest Nurture flow. Notice it's a standard Salesforce Flow — same builder your admins already know."

2. **Walk through the canvas** — Show the visual flow: segment entry → wait → decision → email → wait for click → branch. "The flow starts when someone enters the Vehicle Interest Waterfall segment as Priority 1 — that's our Hearted Vehicle audience. Jane Dawson is in here."

3. **Highlight suppression** — Click the "Recent Purchaser?" decision element. "Notice how recent purchasers are automatically suppressed. If Jane bought a car yesterday and somehow re-entered the segment, she would exit here. No irrelevant emails after a purchase — that's governance built into the flow."

4. **Highlight the email send** — Click the Send Email element. "This sends the 'Compare What Matters' email we just saw — with Jane's actual hearted vehicles, real pricing, and dynamic CTAs. The email content comes from CMS, personalized by the Data Graph."

5. **Highlight the Wait Until Event** — Click the Wait for Link Click element. "This is where MCA gets smart. We're not just waiting a fixed number of days. We're waiting for Jane to actually click a link in the email. If she clicks within 3 days, she's engaged — we stop. If she doesn't click, we branch to a softer approach."

6. **Highlight multi-channel branching** — Click the "Email Opened?" decision. "If Jane opened the email but didn't click, we follow up via SMS — a different channel. If she never opened it, we send a softer reminder email. The flow intelligently chooses the next best action based on actual engagement behavior, not just time."

**Optional live SMS authoring (if time permits):** Navigate to the SMS editor and author the Test Drive Reminder SMS live, showing Data Cloud personalization tokens being inserted from the thunderbolt picker.

---

## Critical Notes & Gotchas

1. **`processType` must be `AutoLaunchedFlow`** — NOT `Journey`. MCA uses Flow infrastructure, not Journey Builder infrastructure. If you see `processType: Journey` in any documentation, that is MC Engagement-specific and does NOT apply to MCA.

2. **`triggerType: Segment` is required** — This is what makes it a segment-triggered flow. It must appear in the `<start>` element of the flow XML. Without it, the flow will not appear in the MCA Flow list and cannot be triggered by segment membership.

3. **`dataGraph: Marketing_Content_Personalizat`** — This is the MCA system data graph (NOT the custom CarMax Customer 360 graph from Phase 4). It provides the email personalization context. The Start element must reference this data graph. The truncated name is correct — it is system-generated and matches the 35-character limit.

4. **`object: UnifiedssotIndividualInd1__dlm`** — This is the Unified Individual DMO that segment-triggered flows operate on. It is NOT `ssot__Individual__dlm` (that is the base Individual DMO before identity resolution). The `UnifiedssotIndividualInd1__dlm` object represents the resolved, unified individual and is the correct entry point for segment-triggered flows.

5. **Contact Point Email DMO must be Included** — In the Start element's "Specify Email" section, the Contact Point Email DMO must be set to "Included" with `ssot__ContactPointEmail__dlm`. Without this, the flow cannot resolve email addresses and emails will not send. This is the #1 configuration error in MCA Flow setup. The setting is found by scrolling down in the Start element properties panel.

6. **Communication Subscription is REQUIRED on every Send Email Message** — On every Send Email Message element, the Communication Subscription and Channel Type must be set. These fields are at the bottom of the properties panel — easy to miss. Without them, the email send fails silently. The subscription is the consent/preference management layer (0Xl prefix ID) and the channel type links it to the email channel (0eB prefix ID).

7. **Email content must be Published (not Draft)** — If CMS email content is in Draft status, the flow will show: "We can't send unpublished content. Publish your content, and then try again." Ensure all emails referenced by flow Send Email Message actions have been published in Phase 7 before activating the flow.

8. **Flow deploys in Draft status** — The metadata deployment creates the flow in Draft. You must activate it via the UI or API after deploying and verifying configuration. This is by design — it forces a manual verification step before any emails are sent.

9. **Wait Until Event requires a preceding action** — The EmailLinkClickEvent must reference a Send Email Message action that comes before it in the flow via the `FlowActionToMonitor` parameter. You cannot wait for a click on an email that has not been sent yet in the same flow. The `FlowActionToMonitor` value must match the `name` attribute of the preceding `actionCalls` element exactly (e.g., `Send_Hearted_Vehicle_Email`).

10. **SMS sends require phone number resolution** — The Send SMS Message action in MCA Flow requires a phone number resolution (Contact Point Phone DMO) and SMS-specific subscription. Configure these in the Start element's "Specify Phone" section. If the flow includes any SMS send elements, the Start element must include BOTH Contact Point Email DMO (for email sends) AND Contact Point Phone DMO (for SMS sends).

11. **Flow Builder saves take 15-30 seconds** — Especially after modifying email configurations or adding new elements. Wait for the "Saving..." indicator in the top toolbar to complete before making additional changes. Clicking other elements during a save can cause unsaved changes to be lost.

12. **Toolbox panel can intercept clicks** — When using browser automation in Flow Builder, hide the Errors/Warnings Toolbox panel first (click the collapse arrow on the left side panel) to prevent it from intercepting clicks on canvas elements. This is especially important when trying to click elements near the left edge of the canvas.

13. **IDs are org-specific** — All the `SENDER_ID_HERE`, `COMM_SUBSCRIPTION_ID_HERE`, `CHANNEL_TYPE_ID_HERE`, and `SEGMENT_ID_HERE` placeholders must be replaced with actual IDs from the target org. Do NOT hardcode IDs from one org into another. The Step 1 queries provide the commands to look up these IDs at build time.

14. **Schedule frequency `OnActivate`** — The flow runs once when activated, processing all current members of the entry segment. For recurring execution (e.g., processing new segment members daily), change the schedule to `Daily` with a specific time. For demo purposes, `OnActivate` is sufficient — it will process Jane Dawson and any other current segment members immediately upon activation.
