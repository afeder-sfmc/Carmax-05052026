# CarMax Demo Plan v3

## Overview
- **Demo style:** Harbor cruise (single narrative, feature-forward flow).
- **Primary focus:** Marketing Cloud Advanced (MC on Core / MCA).
- **Secondary focus:** Data Cloud only where it supports targeting decisions (Einstein Segmentation, Calculated Insights, engagement signals, waterfall prioritization).
- **Target duration:** 60 minutes (+10 minutes Q&A).
- **Audience:** Marketing leaders, lifecycle/CRM owners, campaign operators, and journey stakeholders.

## Demo Narrative
CarMax marketers launch and optimize lifecycle campaigns in MCA using website engagement signals as inbound data streams (without demoing the website itself).  
The story moves from AI-assisted campaign build to segmentation depth (Einstein + CIs + engagement + waterfall), then into dynamic email content, MCA Flow orchestration with SMS, reporting, and a late-stage concept stop for dynamic feedback loops.

## Demo Outcomes to Prove
1. Campaign creation in MCA is fast and marketer-driven.
2. Segmentation can start in natural language and become business-rigorous.
3. Calculated Insights and engagement data improve targeting quality.
4. Waterfall prioritization prevents campaign collisions and over-messaging.
5. Dynamic content and orchestration execute at scale with clear outcomes.

## Scope Guardrails
- Keep Data Cloud discussion tied to send decisions:
  - Segment criteria
  - CI-driven qualification
  - Engagement/suppression logic
  - Waterfall prioritization method
- Avoid deep engineering internals unless asked.

## Proposed Use Cases
### Use Case A: Expiring Credits Re-engagement (Primary)
- Audience: customers with expiring rewards value and low recent purchase activity.
- Offer: service-ready bundle plus urgency window.

### Use Case B: Web Engagement-Triggered Email + Dynamic Content Blocks
- Trigger source: web engagement data stream (for example, "view a car page").
- Assumption for demo: web events are already available in Data Cloud via data streams; no website walkthrough required.
- Email moment: show dynamic content blocks personalized by browsing behavior and completion state.

### Use Case C: Upper Funnel SMS in MCA
- Show that SMS content can be authored in MCA (MC on Core).
- Show SMS steps can be added into MCA campaign flow for nurture/status-style messaging.
- Keep scope to channel inclusion and authoring workflow.

### Use Case D: Dynamic Feedback Loop (Concept Only, Late Demo Stop)
- Reference dynamic feedback loop patterns (heart/thumbs and recommendation refinement).
- Use concept explanation (no live feature demo).
- Reserve a late stop for a visual/graphic narrative.

### Use Case E: Dynamic Loop Email Personalization
- Demonstrate repeaters/loop blocks for multi-offer personalization.
- Inputs: nearest store, service context, tier/points status, engagement propensity.

### Use Case F: Prioritization + Suppression Governance
- Show overlapping-campaign resolution via waterfall logic.
- Show suppression for low-engagement/high-frequency risk customers.

## Harbor Cruise Run of Show (60 minutes)
1. **Dock & Business Framing (4 min)**
   - Frame business objective, KPI intent, and the live walkthrough.
2. **Stop 1: Campaign Agent in MCA (9 min)**
   - Draft campaign from prompt and validate brief elements.
3. **Stop 2: Segmentation + CIs + Engagement + Waterfall (16 min)**
   - Einstein segmentation in natural language.
   - Rules refinement with recency/value/loyalty fields.
   - Overlay CIs and engagement signals.
   - Demonstrate waterfall prioritization in overlap scenarios.
4. **Stop 3: Content & Dynamic Loop Email (10 min)**
   - Show web-engagement-triggered email scenario ("view a car page") using stream-fed events.
   - Show dynamic content blocks and loop/repeater blocks with persona-based previews.
5. **Stop 4: Flow Orchestration in MCA + Upper Funnel SMS (9 min)**
   - Entry criteria, branching, waits, suppressions, and fallback path.
   - Show SMS message authoring in MCA and SMS step inclusion in campaign flow.
6. **Stop 5: Reporting, Learnings, Next Actions (5 min)**
   - Show campaign/journey outcomes and optimization next steps.
7. **Stop 6: Dynamic Feedback Loop Concept Stop (5 min)**
   - Present a concept graphic for feedback-loop interactions and recommendation refinement.
   - Clarify this is explanatory only, not a live demo step.
8. **Wrap: Executive Recap (2 min)**
   - Summarize business value and operational confidence.

## Data Cloud Elements to Prepare (Decision-Critical)
- **Segment-ready attributes**
  - Rewards balance and expiry window
  - Last purchase date / recency buckets
  - Service affinity or inferred intent
  - Channel consent/status
- **Calculated Insights**
  - `ciValue90d`
  - `ciDaysSincePurchase`
  - `ciEngagementIndex30d`
  - `ciLapseRiskBand`
- **Engagement + pressure signals**
  - Recent open/click indicators
  - Recent conversion/non-conversion
  - Frequency marker / suppression status
- **Waterfall setup**
  - Priority order across overlapping campaigns
  - Exclusion rules after assignment

## Demo Environment Checklist
- Fallback campaign and segment tabs pre-opened.
- CI fields and engagement flags populated.
- Waterfall overlap scenario configured.
- 3 persona records ready for dynamic content previews.
- Reporting view has seeded data or fallback narrative.

## Talk Track Anchors
- “This is marketer-speed campaign execution.”
- “Einstein gets us started; CIs and engagement make it precise.”
- “Waterfall logic keeps communication relevant and controlled.”
- “Website behavior is already streaming in, so marketers can act on it immediately in MCA.”
- “SMS lives in the same campaign flow and authoring experience.”
- “Dynamic feedback loops are part of the future-state interaction model we are illustrating conceptually.”
- “The same workflow closes with measurement and optimization.”

## Risks and Mitigations
- **Risk:** AI generation latency.  
  **Mitigation:** Keep fallback assets open.
- **Risk:** Sparse reporting data.  
  **Mitigation:** Use seeded/historical examples and optimization framing.
- **Risk:** Scope drift into architecture detail.  
  **Mitigation:** Re-anchor to send-decision impact.

## Success Criteria
- Audience can explain the end-to-end MCA workflow in one pass.
- Audience sees segmentation depth (Einstein -> CI/engagement -> waterfall).
- Audience sees web-engagement-triggered personalization, SMS in flow, and reporting in a single story.
- Audience understands the dynamic feedback loop concept and where it fits in the journey.
