# CarMax MCA Harbor Cruise Demo Plan v4

## Overview

A **90-minute**, business-first harbor cruise demonstrating how CarMax moves from campaign brief to segmentation, dynamic content, orchestration, and optimization in MCA (Marketing Cloud Advanced), powered by Data Cloud intelligence. This plan expands from v3 (60 min) to allow deeper dives at each stop, live interaction time, and a dedicated Data Cloud 360 walkthrough.

| Attribute | Value |
|-----------|-------|
| **Duration** | 90 minutes |
| **Harbor Stops** | 9 (expanded from 8) |
| **Primary Focus** | MCA — Marketing Cloud Advanced |
| **Data Cloud Role** | Decisioning + intelligence layer |
| **Key Persona** | Jane Dawson (waterfall overlap hero) |
| **Contrast Persona** | Aisha Thompson (new subscriber) |

---

## Storyline

CarMax marketers launch lifecycle campaigns in MCA. They draft with Campaign Agent, build audiences using Einstein Segmentation, enrich and prioritize with Calculated Insights, engagement data, and waterfall logic, then deliver web-engagement-triggered dynamic email content, orchestrate cross-channel with SMS in MCA Flow, analyze outcomes with reporting, and close with a dynamic feedback loop vision.

**Positioning line (use consistently):**
> Data Cloud supports the decisioning layer; MCA is the execution center, with web engagement already stream-fed for activation.

---

## Run of Show — 90 Minutes

### Dock: Business Framing (5 min)

**Objective:** Set the business context and preview the end-to-end flow.

- Welcome and introductions
- Frame the demo objective: "Today we'll build a complete campaign lifecycle in MCA — from idea to execution to optimization — in under 90 minutes"
- Set the business KPI intent: increase test drive bookings from vehicle browsers
- Introduce the "Harbor Cruise" format: 9 stops, each building on the last
- Name-drop the key personas: Jane Dawson (power shopper) and Aisha Thompson (new subscriber)

**Transition:** "Let's start where every campaign starts — with a brief."

---

### Stop 1: Campaign Agent & Brief (12 min)

**Objective:** Show AI-assisted campaign creation from natural language.

**Demo Actions:**
1. Open Campaign Agent in the Marketing App
2. Type the prompt live: *"Create a campaign targeting customers who hearted vehicles but haven't purchased. Use email as the primary channel. The tone should be warm and helpful — CarMax style. Include dynamic vehicle cards with their favorited cars, pricing, and a CTA to schedule a test drive."*
3. Watch Campaign Agent generate the brief — audience, channels, messaging, subject lines, success metrics
4. Walk through each section of the generated brief:
   - **Target Audience:** Hearted vehicle customers, no purchase in 90 days
   - **Channels:** Email (primary), SMS (follow-up)
   - **Key Messages:** Vehicle cards, pricing, scheduling CTAs
   - **Success Metrics:** Open rate >35%, click-to-listing >12%, test drive booking >5%
5. Show how the brief connects to the Campaign record
6. Highlight the brand voice and tone settings

**Talk Track Highlights:**
- "The marketer didn't write SQL or build a segment — they described the business intent"
- "Campaign Agent translated business language into actionable marketing specs"
- "This brief now becomes the single source of truth for the campaign"

**Fallback:** If Campaign Agent is slow, show the pre-created brief and walk through it as "here's what Campaign Agent would generate."

**Transition:** "Now that we have our brief, let's build the audience it describes."

---

### Stop 2: Segmentation, CIs, and Waterfall (18 min)

**Objective:** Show Einstein segmentation, Calculated Insight enrichment, and waterfall prioritization for overlapping audiences.

**Part A — Einstein Segmentation (6 min):**
1. Navigate to Data Cloud Segments
2. Show the "EV Consideration Nurture" Einstein segment — demonstrate natural-language audience discovery
3. Show how Einstein translates the prompt into segment criteria
4. Preview membership count and sample members

**Part B — Calculated Insight Enrichment (5 min):**
1. Navigate to Calculated Insights
2. Show the 4 CarMax CIs:
   - **Customer Lifetime Value** — purchase history + vehicle interactions
   - **Propensity to Buy** — behavioral scoring with time-decay weighting
   - **Vehicle Preference Affinity** — preferred body type, fuel type, price range
   - **Engagement Velocity** — week-over-week engagement acceleration
3. Click into Jane Dawson's profile to show her CI scores
4. Explain how CIs power segment qualification and flow decisioning

**Part C — Waterfall Prioritization (7 min):**
1. Open the "Vehicle Interest Waterfall" segment
2. Show the 3 priority tiers:
   - **Priority 1:** Hearted Vehicle Follow-Up (highest value — active intent)
   - **Priority 2:** Test Drive No Purchase (mid-value — demonstrated interest)
   - **Priority 3:** Seasonal Push Memorial Day (lowest — catch-all)
3. **The "aha moment":** Show that Jane Dawson qualifies for ALL 3 tiers
4. Show the waterfall resolution — Jane is assigned to Priority 1 ONLY
5. Explain: "Without the waterfall, Jane would receive 3 separate campaigns. With it, she gets the single most relevant message."

**Talk Track Highlights:**
- "Einstein discovers audiences that a marketer might miss — like EV-curious shoppers who haven't been targeted yet"
- "Calculated Insights turn raw data into marketing-ready signals — propensity, velocity, lifetime value"
- "The waterfall is the governance layer — it ensures every customer gets exactly one campaign, the most relevant one"

**Transition:** "Jane is now in the Hearted Vehicle segment. Let's see what email she'll receive."

---

### Stop 3: Dynamic Email with Data Graph (14 min)

**Objective:** Show the flagship "Compare What Matters" email with dynamic vehicle cards pulled from the Data Graph repeater.

**Part A — Email Structure (5 min):**
1. Open the Hearted Vehicle Follow-Up email in the MCA Email Builder
2. Walk through the modular structure:
   - Header: CarMax logo + "Compare What Matters" headline
   - Greeting: Dynamic — "Hi {{FirstName}},"
   - Intro copy
   - **Dynamic vehicle cards** — repeater block pulling from Data Graph
   - CTA section: "Schedule a Test Drive"
   - Footer: Legal, unsubscribe
3. Show how the email mixes component blocks (header, footer) with HTML blocks (dynamic loop)

**Part B — Data Graph Connection (4 min):**
1. Show the CarMax Customer 360 Data Graph configuration
2. Explain the graph structure: Individual → Vehicle, Test Drive, Web Engagement
3. Show how the repeater references graph field devNames: `{{CX360_Vehicle_Make}}`, `{{CX360_Vehicle_Price}}`, etc.
4. Explain the filter: `Is_Hearted = true` — only hearted vehicles appear

**Part C — Persona Previews (5 min):**
1. **Preview as Jane Dawson:**
   - 3 vehicle cards render (Ford Expedition XLT, Toyota 4Runner SR5, Hyundai Santa Fe SEL)
   - Pre-qualification block is HIDDEN (she already pre-qualified)
   - CTA: "Schedule a Test Drive"
2. **Switch to Aisha Thompson:**
   - 0 hearted vehicles → fallback "Browse Our Top Picks" static section
   - "Create an Account" and "Get Pre-Qualified" blocks SHOW
   - CTA: "Start Browsing"
3. Side-by-side comparison: "Same template, completely different experience"

**Talk Track Highlights:**
- "The dynamic loop is pulling live data from the Data Graph — not static content"
- "Jane sees her actual hearted vehicles with real pricing"
- "Aisha sees a completely different experience because she hasn't taken those steps yet"
- "This is true 1:1 personalization at scale, powered by Data Cloud"

**Transition:** "Now let's see how this email gets delivered — and what happens when Jane engages or doesn't."

---

### Stop 4: MCA Flow Orchestration (14 min)

**Objective:** Show the segment-triggered flow with decision splits, wait elements, suppression logic, and multi-channel branching.

**Part A — Flow Canvas Walkthrough (7 min):**
1. Open the "CarMax Vehicle Interest Nurture" flow in Flow Builder
2. Walk through the canvas step by step:
   - **Segment Entry:** Vehicle Interest Waterfall → Priority 1 (Hearted Vehicle)
   - **Wait 2 Hours:** Delay before first touchpoint
   - **Decision — Recent Purchaser?** Suppress customers who purchased since entering the segment
   - **Send Email:** "Compare What Matters" Hearted Vehicle Follow-Up
   - **Wait Until Event:** Email Link Click — 3-day timeout
   - **Branch — Clicked?** If yes → End (engaged, let retargeting handle)
   - **Branch — Not Clicked, Opened?** If opened but no click → Send SMS. If no open → Send softer reminder email
3. Highlight the suppression logic: "Recent purchasers are automatically excluded — no more irrelevant emails after buying"
4. Highlight multi-channel: "The flow intelligently chooses between SMS and email based on actual engagement behavior"

**Part B — SMS Live Authoring (5 min):**
1. Navigate to Marketing App → Messaging → New SMS
2. Author the SMS live: *"Hi {{FirstName}}! Still thinking about the {{Vehicle_Year}} {{Vehicle_Make}} you test drove at CarMax {{Store}}? Your 24-hour test drive is still available. Book again: {{ShortLink}} Reply STOP to opt out."*
3. Show the personalization token picker (thunderbolt icon) pulling from Data Cloud
4. Show character count: ~155 characters (1 SMS segment)
5. Save and connect to the flow

**Part C — Supporting Flows (2 min):**
1. Quickly show the other 4 flows in the list: Welcome Series, Price Drop Alert, Instant Offer Abandonment, Saved Search Match
2. "Each segment has its own orchestration — all built on the same MCA Flow infrastructure"

**Talk Track Highlights:**
- "This isn't a journey builder from scratch — it's a Flow, the same platform your admins already know"
- "The Wait Until Event is watching for real engagement, not just waiting a fixed time"
- "SMS and email work together in one flow — no separate journey for each channel"

**Transition:** "We've seen campaign creation, audience building, content, and orchestration. Let's look at how Data Cloud ties it all together."

---

### Stop 5: Data Cloud Customer 360 (8 min)

**Objective:** Show the unified customer profile and how Data Cloud powers every previous stop.

**Demo Actions:**
1. Navigate to Jane Dawson's Individual profile
2. Show the Customer 360 view:
   - **Identity:** Unified Individual from CRM Contact + web engagement data
   - **Vehicle Interactions:** 5 vehicles (3 hearted, 1 test driven, 1 purchased previously)
   - **Web Engagement:** Recent browsing sessions with event types
   - **Calculated Insights:** CLV tier, Propensity score, Vehicle Preference, Engagement Velocity
   - **Segment Membership:** Vehicle Interest Waterfall (Priority 1)
3. Show the Data Graph: Individual → Vehicle, Test Drive, Web Engagement relationships
4. Explain: "Everything the email personalized, the flow decided, the segment qualified — it all comes from this unified profile"

**Talk Track Highlights:**
- "This is the single source of truth — CRM data, web behavior, engagement history, AI scores — all unified"
- "The marketer never had to think about data plumbing — they just used it through segments, emails, and flows"
- "Data Cloud is the intelligence layer that makes MCA campaigns smarter"

**Transition:** "Now let's see how the campaign performed."

---

### Stop 6: Reporting and Optimization (7 min)

**Objective:** Show campaign and journey outcomes, identify optimization opportunities.

**Demo Actions:**
1. Show campaign-level reporting: send volume, open rates, click rates
2. Show flow-level analytics: how many entered, how many suppressed, how many engaged
3. Show the branch breakdown: what percentage clicked, opened-no-click (got SMS), didn't open (got reminder)
4. Identify optimization opportunity: "The SMS follow-up for openers-who-didn't-click has a 22% conversion rate — higher than the reminder email. Let's shift more traffic to SMS."
5. Show segment member count and growth trends

**Talk Track Highlights:**
- "Reporting closes the loop — every decision in the flow becomes a data point for optimization"
- "The marketer can see which branch is performing and adjust in real-time"
- "This isn't just reporting — it's the foundation for continuous optimization"

**Transition:** "What if the campaign could optimize itself?"

---

### Stop 7: Dynamic Feedback Loop Concept (6 min)

**Objective:** Present the vision of self-improving campaigns where in-email interactions feed back into Data Cloud.

**Concept Presentation:**
1. Show the feedback loop diagram:
   - Customer receives email with vehicle cards
   - Customer clicks heart on a vehicle in the email
   - Click event captured by MCA tracking
   - Event flows back to Data Cloud → updates Is_Hearted on Vehicle DMO
   - Data Graph refreshes → new heart reflected in Customer 360
   - Next email send includes the newly hearted vehicle
   - Cycle repeats — each interaction makes the next one smarter
2. Connect to what's already built: "The Data Graph, the dynamic loop email, the click tracking — all the pieces are in place"
3. Future vision: "This is the vision of a self-improving marketing system"

**Talk Track Highlights:**
- "Every interaction becomes a data signal that improves the next touchpoint"
- "This isn't theory — the architecture is already here. The writeback is the last piece."
- "Imagine a marketing engine that gets smarter with every send"

**Note:** This stop is conceptual — no live demonstration of the writeback loop.

**Transition:** "Let's wrap up with the executive view."

---

### Stop 8: Wrap and Executive Recap (4 min)

**Objective:** Summarize the end-to-end journey and close with adoption confidence.

**Recap:**
1. **Speed:** "In 90 minutes we went from a blank brief to a fully orchestrated, multi-channel, personalized campaign"
2. **Intelligence:** "Every decision was powered by Data Cloud — segments, CIs, engagement velocity, waterfall prioritization"
3. **Precision:** "Jane Dawson got ONE email — the most relevant one — not three. And it was personalized with her actual hearted vehicles."
4. **Scale:** "This same infrastructure works for all 10 campaigns simultaneously"
5. **Control:** "Waterfall governance, suppression logic, consent management — all built in"

**Closing line:** "MCA isn't just a migration from Marketing Cloud Engagement — it's a step change in what your marketing team can do."

---

### Buffer: Q&A and Deep Dives (2 min)

**Objective:** Handle questions and offer deeper dives on any stop.

- Field questions from the audience
- Offer to go deeper on any specific stop
- Share next steps for evaluation or proof of concept

---

## Timing Summary

| Stop | Topic | Duration | Cumulative |
|------|-------|----------|------------|
| Dock | Business Framing | 5 min | 5 min |
| Stop 1 | Campaign Agent & Brief | 12 min | 17 min |
| Stop 2 | Segmentation + CIs + Waterfall | 18 min | 35 min |
| Stop 3 | Dynamic Email + Data Graph | 14 min | 49 min |
| Stop 4 | MCA Flow + SMS | 14 min | 63 min |
| Stop 5 | Data Cloud Customer 360 | 8 min | 71 min |
| Stop 6 | Reporting & Optimization | 7 min | 78 min |
| Stop 7 | Dynamic Feedback Loop | 6 min | 84 min |
| Stop 8 | Wrap & Executive Recap | 4 min | 88 min |
| Buffer | Q&A | 2 min | 90 min |
| | **Total** | **90 min** | |

---

## Key Changes from v3 (60 min) → v4 (90 min)

| Change | v3 (60 min) | v4 (90 min) |
|--------|-------------|-------------|
| Total stops | 8 (Dock + 6 + Wrap) | 10 (Dock + 8 + Buffer) |
| Stop 1 (Campaign Agent) | 9 min | 12 min — deeper brief walkthrough |
| Stop 2 (Segmentation) | 16 min | 18 min — split into 3 parts (Einstein, CIs, Waterfall) |
| Stop 3 (Dynamic Email) | 10 min | 14 min — added Data Graph walkthrough |
| Stop 4 (MCA Flow) | 9 min | 14 min — deeper flow walkthrough + live SMS |
| Stop 5 (Data Cloud 360) | N/A (combined in Stop 5) | 8 min — NEW dedicated stop |
| Stop 6 (Reporting) | 5 min | 7 min — optimization focus added |
| Stop 7 (Feedback Loop) | 5 min | 6 min — slightly expanded |
| Wrap | 2 min | 4 min — fuller recap |
| Buffer | N/A | 2 min — NEW Q&A buffer |

---

## Data Cloud Scope (Deliberately Narrow)

### Show This
- Einstein segment logic and output quality
- Calculated Insights used in qualification and decisioning
- Engagement signals for suppression/exclusion
- Waterfall campaign prioritization method
- Customer 360 unified profile (NEW in v4 — dedicated stop)
- Data Graph powering dynamic email content

### Avoid This
- Ingestion and identity architecture detours
- Broad CDP replacement debates
- Execution-heavy process details not needed for demo value
- Deep technical DLO/DMO mapping discussions

---

## Readiness Checklist

- [ ] Campaign Agent brief pre-created (fallback for Stop 1)
- [ ] Einstein and Waterfall segments published with members
- [ ] Calculated Insights materialized with data
- [ ] Data Graph built and operational (Save and Build completed in UI)
- [ ] Flagship email built with dynamic loop previewing correctly
- [ ] Jane Dawson has 3 hearted vehicles (verified in DMO)
- [ ] Aisha Thompson has 0 hearted vehicles (verified)
- [ ] Primary flow deployed and activated
- [ ] SMS channel configured and tested
- [ ] Supporting flows (Welcome, Price Drop, Instant Offer, Saved Search) created
- [ ] All demo tabs pre-opened in browser
- [ ] Reporting screens seeded or fallback narrative ready
- [ ] Session timeout verified (logged in fresh 15 min before)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Campaign Agent slow/unresponsive | Stop 1 stalls | Show pre-created brief as fallback |
| Segment membership empty | Stop 2 loses impact | Show segment rules and explain logic |
| Email preview broken | Stop 3 breaks | Show email in builder mode (component view) |
| Data Graph not built | Stop 3 + 5 break | Show graph definition and explain architecture |
| Flow not activating | Stop 4 breaks | Walk through canvas in Draft mode |
| SMS channel not configured | Stop 4 SMS portion | Focus on flow walkthrough, skip live SMS |
| Data Cloud query latency | Awkward pauses | Pre-open all query-dependent tabs |
| Reporting data sparse | Stop 6 thin | Use seeded/historical examples |
| Session timeout | Demo interruption | Log in fresh 15 min before |

---

## Persona Reference

### Jane Dawson — Power Shopper
- 3 hearted SUVs (Ford Expedition XLT, Toyota 4Runner SR5, Hyundai Santa Fe SEL)
- Pre-qualified
- Test drove Ford Expedition
- Active email subscriber
- In 3 segments (Hearted Vehicle, Test Drive, Memorial Day) → waterfall resolves to P1
- Email shows: 3 dynamic vehicle cards, no pre-qual block, "Schedule a Test Drive" CTA

### Aisha Thompson — New Subscriber
- New email subscriber
- Viewed 3 sedan pages
- No account created
- No pre-qualification
- Email shows: "Browse Our Top Picks" fallback, "Create an Account" block, "Get Pre-Qualified" block, "Start Browsing" CTA

---

## Campaign Architecture (10 Campaigns)

| Campaign | Type | Segment | Priority |
|----------|------|---------|----------|
| Hearted Vehicle Follow-Up | Email | Waterfall P1 | Highest |
| Test Drive — No Purchase Nurture | Email | Waterfall P2 | High |
| New Email Subscriber Welcome | Email | New Email Subscribers | Medium |
| Pre-Qualification Completion | Email | PreQual Shoppers | Medium |
| Price Drop Alert | Email | Price Drop Alert | Medium |
| Saved Search Match | Email | Saved Search Match | Medium |
| Trade-In and Upgrade | Email | Trade-In (Einstein) | Medium |
| EV Consideration Nurture | Email | EV (Einstein) | Medium |
| Seasonal Push — Memorial Day | Multi-Channel | Waterfall P3 | Lowest |
| Instant Offer Abandonment | Email | Instant Offer Abandon | Medium |
