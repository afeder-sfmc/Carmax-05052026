# CarMax Demo Plan v2

## Overview
- **Demo style:** Harbor cruise (one connected narrative with explicit transitions).
- **Primary focus:** Marketing Cloud Advanced (MC on Core / MCA).
- **Secondary focus:** Data Cloud only where it directly supports targeting decisions (Einstein Segmentation, Calculated Insights, engagement signals, waterfall prioritization).
- **Target duration:** 90 minutes (+10-15 minutes Q&A buffer).
- **Audience:** Marketing leaders, lifecycle/CRM operators, campaign managers, and journey owners.

## Demo Narrative
CarMax marketers launch and optimize a high-priority re-engagement campaign using MCA.  
The flow starts with campaign intent, then moves into AI-assisted build, audience construction, CI/engagement enrichment, and waterfall campaign prioritization before orchestration, activation, and performance review.

## Demo Outcomes to Prove
1. Marketers can move from brief to executable campaign quickly in MCA.
2. Einstein Segmentation is intuitive and can be refined with CIs and engagement logic.
3. Waterfall segmentation supports practical campaign prioritization and message-pressure control.
4. Dynamic content (including loop/repeater constructs) enables scale personalization.
5. Reporting closes the loop for continuous audience and journey optimization.

## Scope Guardrails
- Keep Data Cloud discussion tightly tied to send decisions:
  - Segment criteria and attribute availability
  - Calculated Insights used in eligibility/ranking
  - Engagement data used for suppressions/prioritization
  - Waterfall method for campaign conflict resolution
- Avoid deep ingestion/identity internals unless asked.

## Proposed Use Cases
### Use Case A: Expiring Credits Re-engagement (Primary)
- Audience: customers with expiring rewards value and low recent purchase activity.
- Offer: service-ready bundle + urgency window.
- Goal: reactivation with controlled frequency and relevance.

### Use Case B: Dynamic Loop Email Personalization (Feature Moment)
- Demonstrate repeating blocks for product/service recommendations.
- Inputs: nearest store, vehicle/service context, points/tier, engagement propensity.
- Goal: prove 1:1 content logic at scale.

### Use Case C: Prioritization + Suppression Governance
- Show waterfall segmentation and suppression criteria:
  - eligible for Campaign A/B/C
  - prioritize highest business value campaign first
  - suppress low-engagement/high-frequency risk customers

## Harbor Cruise Run of Show (90 minutes)
1. **Dock & Business Framing (8 min)**
   - Frame objectives, KPI targets, and the live walkthrough path.
2. **Stop 1: Campaign Agent in MCA (15 min)**
   - Draft campaign from prompt and validate strategic brief elements.
3. **Stop 2: Segmentation + CIs + Engagement + Waterfall (22 min)**
   - Einstein segment creation in natural language.
   - Rules refinement with loyalty/recency/value fields.
   - Add CIs (value, recency, risk/propensity indicators).
   - Overlay engagement/frequency signals.
   - Demonstrate waterfall segmentation as campaign prioritization.
4. **Stop 3: Content & Dynamic Loop Email (14 min)**
   - Show loop/repeater blocks and persona-based previews.
5. **Stop 4: Flow Orchestration in MCA (14 min)**
   - Entry logic, branching, waits, suppressions, and fallback paths.
6. **Stop 5: Activation Controls & QA Validation (8 min)**
   - Show approvals, audience sanity checks, and preflight checks.
7. **Stop 6: Reporting, Learnings, Next Actions (6 min)**
   - Campaign/journey performance and iterative optimization actions.
8. **Wrap: Executive Recap (3 min)**
   - Summarize business impact and operational confidence.

## Data Cloud Elements to Prepare (Decision-Critical)
- **Segment-ready attributes**
  - Rewards balance and expiry window
  - Last purchase date / recency buckets
  - Service affinity or inferred maintenance intent
  - Channel consent/status
- **Calculated Insights (examples)**
  - `ciValue90d`
  - `ciDaysSincePurchase`
  - `ciEngagementIndex30d`
  - `ciLapseRiskBand`
- **Engagement + pressure signals**
  - Recent open/click indicators
  - Recent conversion/non-conversion
  - Frequency marker / suppression status
- **Waterfall setup**
  - Ordered priority list across overlapping campaigns
  - Exclusion logic after assignment

## Demo Environment Checklist
- Campaign and flow prebuilt in draft as backup.
- Seed segment and CI fields validated for realistic counts.
- At least 3 persona records ready for dynamic content previews.
- Waterfall segmentation scenario preconfigured with overlap.
- Reporting screen has seeded data or explicit fallback narration.

## Talk Track Anchors
- “This is marketer-speed campaign execution with controls.”
- “Segmentation starts in plain language and becomes business-rigorous.”
- “Calculated Insights and engagement data improve each send decision.”
- “Waterfall prioritization prevents collisions and over-messaging.”
- “Every outcome feeds the next campaign iteration.”

## Risks and Mitigations
- **Risk:** AI generation latency.  
  **Mitigation:** Keep fallback campaign/segment tabs pre-opened.
- **Risk:** Sparse engagement metrics in demo org.  
  **Mitigation:** Use seeded/historical view and expected optimization loop.
- **Risk:** Scope drift into deep Data Cloud architecture.  
  **Mitigation:** Re-anchor to “what changes the send decision.”

## Success Criteria
- Audience can describe MCA + Data Cloud in one practical workflow.
- Audience sees segmentation maturity: Einstein -> CI/engagement -> waterfall.
- Audience sees dynamic personalization and governance together.
- Stakeholders leave with confidence in both scale and control.
