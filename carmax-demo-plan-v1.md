# CarMax Demo Plan v1

## Overview
- **Demo style:** Harbor cruise (single connected story, no dead-end feature tours).
- **Primary focus:** Marketing Cloud Advanced (MC on Core / MCA).
- **Secondary focus:** Data Cloud only where it powers MCA outcomes: segmentation, Calculated Insights, and engagement-driven targeting.
- **Target duration:** 45 minutes (+10 minutes Q&A buffer).
- **Audience:** Marketing leadership, campaign operators, lifecycle/CRM owners, and digital experience stakeholders.

## Demo Narrative
CarMax marketers launch a high-value, seasonally relevant campaign to drive service conversion and repeat engagement while controlling message pressure.  
The demo starts with campaign intent, uses AI to draft campaign assets, validates audience strategy in Data Cloud, orchestrates in MCA Flow, and closes with measurement plus next-best action.

## Demo Outcomes to Prove
1. Marketers can go from brief to campaign quickly with AI assistance.
2. Segmentation is business-friendly (natural language + rules refinement).
3. Data Cloud outputs (segments + Calculated Insights + engagement) directly improve targeting precision.
4. MCA orchestration supports cross-channel execution with governance.
5. Performance signals feed back into future segmentation decisions.

## Scope Guardrails
- Keep Data Cloud discussion tightly bounded to:
  - Unified profile context needed for segmentation.
  - Calculated Insights used as audience criteria.
  - Engagement events used for suppression/inclusion and recency logic.
- Avoid deep implementation internals (identity graph internals, ingestion engineering deep dive, broad CDP replacement narratives).

## Proposed Use Cases
### Use Case A: Expiring Credits Re-engagement (Primary)
- Audience: customers with expiring rewards value and low recent purchase activity.
- Offer: service-ready bundle recommendation and incentive.
- Channel mix: email first, optional SMS follow-up for non-openers (if provisioned).

### Use Case B: Dynamic Loop Email Personalization (Feature Moment)
- Show dynamic/repeating content blocks (for multi-item recommendations or offer rows).
- Personalization inputs: nearest store, vehicle context, tier/points status, and engagement propensity.
- Goal: prove scale personalization without manual one-off creative builds.

### Use Case C: Message Pressure + Engagement Governance
- Use engagement metrics + frequency status to suppress over-messaged customers.
- Show explicit “do not send now” path for low-engagement/high-frequency risk profiles.

## Harbor Cruise Run of Show (45 minutes)
1. **Dock & Business Framing (3 min)**
   - Frame business objective, success criteria, and what will be shown live.
2. **Stop 1: Campaign Agent in MCA (8 min)**
   - Draft campaign from prompt.
   - Confirm brief, content intent, and channel plan.
3. **Stop 2: Segment Creation (8 min)**
   - Start with natural-language segment draft.
   - Refine with loyalty + recency + value + engagement predicates.
4. **Stop 3: Calculated Insights + Engagement Overlay (6 min)**
   - Add CI metrics (example: 90-day value, lapse risk proxy, service propensity).
   - Add engagement suppression logic.
5. **Stop 4: Content & Dynamic Loop Email (8 min)**
   - Open email asset; show repeater loop and personalization tokens.
   - Preview by 2-3 persona records.
6. **Stop 5: Flow Orchestration in MCA (7 min)**
   - Entry criteria, branching, wait steps, fallback path, send controls.
7. **Stop 6: Performance & Optimization (3 min)**
   - Show campaign/journey reporting and “what we do next.”
8. **Wrap: Business Value Recap (2 min)**
   - Restate cycle: brief -> audience -> orchestration -> measurement -> continuous improvement.

## Data Cloud Elements to Prepare (Minimal but High Impact)
- **Segment-ready attributes**
  - Rewards balance/expiry window
  - Last purchase date
  - Service-category affinity or inferred intent
  - Channel consent/status
- **Calculated Insights (examples)**
  - `ciValue90d`: spend in last 90 days
  - `ciDaysSincePurchase`
  - `ciEngagementIndex30d`
  - `ciLapseRiskBand`
- **Engagement signals**
  - Recent open/click
  - Recent conversion event
  - Send frequency marker (or equivalent policy flag)

## Demo Environment Checklist
- Campaign and flow are pre-created in draft state (for backup if generation is slow).
- Segment seed audience exists with realistic cardinality.
- At least 3 persona records available for preview:
  - High value / high engagement
  - Mid value / neutral engagement
  - At-risk / low engagement
- Dynamic email content renders correctly for each persona.
- Reporting view contains either seeded engagement data or clear verbal framing if live data is sparse.

## Talk Track Anchors
- “This is marketer-speed execution, not an IT-dependent workflow.”
- “Data Cloud is powering this decision in context, not adding complexity.”
- “We can personalize deeply while still honoring message pressure controls.”
- “Every engagement outcome improves the next targeting decision.”

## Risks and Mitigations
- **Risk:** Live generation lag.  
  **Mitigation:** Keep prebuilt fallback campaign and segment tabs open.
- **Risk:** Sparse demo engagement data.  
  **Mitigation:** Use prepared historical campaign view + explain expected learning loop.
- **Risk:** Over-indexing on Data Cloud details.  
  **Mitigation:** Time-box Data Cloud commentary to criteria that impact the send decision.

## Success Criteria
- Audience can clearly explain how MCA and Data Cloud work together in one workflow.
- Audience sees at least one concrete personalization moment (dynamic loop email).
- Audience sees at least one governance moment (engagement/frequency suppression).
- Audience leaves with confidence that the platform supports both scale and control.

## Optional Extensions (If Time Allows)
- B2B-style branch (CarMax commercial buyer profile variant).
- A/B path optimizer example.
- Follow-up journey trigger based on non-conversion after 7 days.
