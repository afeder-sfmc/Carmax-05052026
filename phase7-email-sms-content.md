# Phase 7: Email & SMS Content — Implementation Plan

## Overview

Build 8 emails (4 component-first, 4 HTML-heavy) and 4 SMS messages that align to the 10 campaigns (Phase 6) and segments (Phase 5). The flagship email — "Hearted Vehicle Follow-Up" — uses a dynamic loop/repeater pulling vehicle cards from the CarMax Customer 360 Data Graph (Phase 4). All content is created in an MCA CMS Workspace and referenced by segment-triggered flows (Phase 8).

**Org:** `carmax-sdo-mm-app-wz95pw`
**Content Builder:** Marketing Cloud on Core (MCA) CMS Workspace
**Prerequisite:** Phase 4 (Data Graph built) + Phase 5 (Segments published)

---

## MCA Context: Content in MCA vs MC Engagement

In MCA, email content lives in CMS Workspaces (not Content Builder from MC Engagement). Emails use the `sfdc_cms__email` content type and are referenced by segment-triggered flows via content keys in the format:
`marketing--Default_Content_Workspace.sfdc_cms__email--{EMAIL_API_NAME}`

| Aspect | MC Engagement | MCA (Marketing Cloud on Core) |
|--------|--------------|-------------------------------|
| Content home | Content Builder | CMS Workspace |
| Email format | Email Template + Content Blocks | `sfdc_cms__email` content type |
| Dynamic content | AMPscript (`%%FirstName%%`) | Handlebars JS (`{{CX360_First_Name}}`) |
| Data source for merge | Data Extensions, Sendable DE | Data Graph (Phase 4) related objects |
| Dynamic loops | Guide Template Language (GTL) | Handlebars `{{#each}}` over graph related objects |
| Conditional logic | AMPscript `IF/ELSEIF` | Handlebars `{{#if}}` / `{{#unless}}` |
| Builder | Content Builder drag-and-drop | MCA Email Builder (component blocks + HTML blocks) |
| Flow reference | Journey Builder content card | Content key: `marketing--{Workspace}.sfdc_cms__email--{API_NAME}` |

**Key differences:**
- MCA uses Handlebars JS for dynamic content (not AMPscript)
- Data Graph provides personalization context (not data extensions)
- Dynamic loops/repeaters iterate over graph related objects
- Component blocks (drag-and-drop) and HTML blocks can be mixed in one email

---

## Content Strategy: 50/50 Split

| Category | Count | Approach | Emails |
|----------|-------|----------|--------|
| Component-First | 4 | Built using MCA Email Builder drag-and-drop components with Data Cloud merge fields | #2, #3, #4, #7 |
| HTML-Heavy | 4 | Custom HTML blocks with Handlebars JS personalization tokens from Data Graph | #1, #5, #6, #8 |
| SMS | 4 | Short-form messages with personalization and CTA links | SMS #1–#4 |

**Why 50/50?** The demo needs to show BOTH capabilities:
- Component-first emails demonstrate the MCA drag-and-drop builder (accessible to non-technical marketers)
- HTML-heavy emails demonstrate advanced personalization with Handlebars JS and Data Graph repeaters (power-user use case)
- Mixing both in the same workspace shows MCA's flexibility

---

## Email #1: Hearted Vehicle Follow-Up (HTML-Heavy / Flagship)

**Campaign:** Hearted Vehicle Follow-Up
**Segment:** Vehicle Interest Waterfall — Priority 1 (Hearted Vehicle)
**Demo Stop:** Stop 3 — Dynamic Email with Data Graph repeater
**Persona:** Jane Dawson
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--Hearted_Vehicle_FollowUp`

### Content Concept

"Compare What Matters" — Displays a personalized grid of vehicles the customer has hearted, with key specs and CTA to view each listing. Uses dynamic loop to render 1-N vehicle cards from the Data Graph.

**Why this is the flagship:** This email is the single best demonstration of MCA's differentiated capability — pulling related object data from a Data Graph into a repeating template block. It shows:
1. Data Cloud as the personalization engine (not a data extension)
2. Handlebars JS dynamic loops (not AMPscript)
3. Graph traversal from Individual to Vehicle (one-to-many)
4. Conditional rendering (only hearted vehicles, not all vehicles)

### Dynamic Loop / Repeater Architecture

```
Data Source:  CarMax_Customer_360 graph (Phase 4)
Root Object:  ssot__Individual__dlm
Related Object: CarMax_Vehicle__dlm
Relationship: CarMax_Vehicle__dlm_ssot__Individual__dlm

Filter:       CX360_Vehicle_IsHearted = true
Sort:         Most recently hearted first (by Hearted_Date__c DESC)
Max Items:    6 (prevent email from becoming too long)
```

The repeater iterates over the `CarMax_Vehicle__dlm` related object on the Data Graph. For each vehicle where `IsHearted__c` is true, it renders a vehicle card with the fields defined in the graph's entity payload (Phase 4, Step 2D).

### Handlebars Template (Vehicle Card Block)

This is the HTML content for the dynamic repeater block. It is entered as a single HTML block in the MCA Email Builder.

```html
<!-- Hearted Vehicle Follow-Up — Full Email Template -->
<!-- Enter this as an HTML block in MCA Email Builder -->

<div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">

  <!-- Header -->
  <div style="background-color: #003468; padding: 24px 32px; text-align: center;">
    <span style="color: #ffffff; font-size: 24px; font-weight: 700; letter-spacing: 1px;">CARMAX</span>
  </div>

  <!-- Hero Section -->
  <div style="background-color: #f0f7ff; padding: 32px; text-align: center;">
    <h1 style="color: #003468; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;">
      Compare What Matters
    </h1>
    <p style="color: #333333; font-size: 16px; line-height: 1.5; margin: 0;">
      Hi {{CX360_First_Name}}, your favorites are still on the lot.
    </p>
  </div>

  <!-- Intro Copy -->
  <div style="padding: 24px 32px;">
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0;">
      You've been eyeing some great vehicles — and they're still available. Here's a quick
      look at your top picks with the details that matter most. Whether you're ready to
      schedule a test drive or just want to compare, we've made it easy.
    </p>
  </div>

  <!-- Dynamic Vehicle Cards — Repeater Block -->
  {{#each CX360_Vehicle}}
    {{#if CX360_Vehicle_IsHearted}}
    <div style="margin: 0 32px 16px 32px; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">

      <!-- Vehicle Header -->
      <div style="background-color: #003468; padding: 12px 16px;">
        <span style="color: #ffffff; font-size: 18px; font-weight: 600;">
          {{CX360_Vehicle_Year}} {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}}
        </span>
      </div>

      <!-- Vehicle Details Grid -->
      <div style="padding: 16px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
          <tr>
            <td style="padding: 4px 8px; color: #666666; font-size: 13px; width: 50%;">Color</td>
            <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600; width: 50%;">{{CX360_Vehicle_Color}}</td>
          </tr>
          <tr>
            <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Body Type</td>
            <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;">{{CX360_Vehicle_BodyType}}</td>
          </tr>
          <tr>
            <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Fuel Type</td>
            <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;">{{CX360_Vehicle_FuelType}}</td>
          </tr>
          <tr>
            <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Mileage</td>
            <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;">{{CX360_Vehicle_Mileage}} mi</td>
          </tr>
          <tr>
            <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Store</td>
            <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;">CarMax {{CX360_Vehicle_Store}}</td>
          </tr>
        </table>

        <!-- Price -->
        <div style="margin-top: 12px; padding: 12px; background-color: #f0f7ff; border-radius: 4px; text-align: center;">
          <span style="color: #003468; font-size: 24px; font-weight: 700;">${{CX360_Vehicle_Price}}</span>
          <br/>
          <span style="color: #666666; font-size: 11px;">No-Haggle Price</span>
        </div>

        <!-- CTA Button -->
        <div style="margin-top: 12px; text-align: center;">
          <a href="{{CX360_Vehicle_ListingURL}}" style="display: inline-block; background-color: #d4001a; color: #ffffff; padding: 12px 32px; border-radius: 4px; text-decoration: none; font-size: 14px; font-weight: 600;">
            View Details
          </a>
        </div>
      </div>
    </div>
    {{/if}}
  {{/each}}

  <!-- Bottom CTA Section -->
  <div style="padding: 32px; text-align: center; background-color: #f0f7ff;">
    <h2 style="color: #003468; font-size: 20px; font-weight: 700; margin: 0 0 8px 0;">
      Ready to take the next step?
    </h2>
    <p style="color: #333333; font-size: 14px; line-height: 1.5; margin: 0 0 16px 0;">
      Schedule a test drive online or visit your nearest CarMax store.
      Every vehicle comes with our Love Your Car Guarantee.
    </p>
    <a href="https://www.carmax.com/schedule-test-drive" style="display: inline-block; background-color: #003468; color: #ffffff; padding: 14px 40px; border-radius: 4px; text-decoration: none; font-size: 15px; font-weight: 600;">
      Schedule a Test Drive
    </a>
  </div>

  <!-- Trust Bar -->
  <div style="padding: 16px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
    <span style="color: #666666; font-size: 12px;">
      No-Haggle Pricing &bull; Love Your Car Guarantee &bull; 150-Point Inspection
    </span>
  </div>

  <!-- Footer -->
  <div style="background-color: #f5f5f5; padding: 24px 32px; text-align: center;">
    <p style="color: #999999; font-size: 11px; line-height: 1.5; margin: 0;">
      CarMax, Inc. | 12800 Tuckahoe Creek Pkwy, Richmond, VA 23238<br/>
      You received this email because you have a CarMax.com account.<br/>
      <a href="{{unsubscribe_url}}" style="color: #003468; text-decoration: underline;">Unsubscribe</a> |
      <a href="https://www.carmax.com/privacy" style="color: #003468; text-decoration: underline;">Privacy Policy</a>
    </p>
  </div>

</div>
```

### Email Structure Summary

| Section | Type | Content |
|---------|------|---------|
| Header | Static | CarMax logo text + navy background (#003468) |
| Hero | Static + Merge | "Compare What Matters" + `{{CX360_First_Name}}` greeting |
| Intro Copy | Static | Conversational copy, CarMax tone |
| Vehicle Cards | Dynamic Loop | `{{#each CX360_Vehicle}}` with `{{#if CX360_Vehicle_IsHearted}}` filter |
| Bottom CTA | Static | "Schedule a Test Drive" button |
| Trust Bar | Static | No-Haggle, Guarantee, Inspection |
| Footer | Static | Legal, unsubscribe |

### Brand Colors Used

| Color | Hex | Usage |
|-------|-----|-------|
| CarMax Primary Blue | `#003468` | Header, hero background text, headings, CTA buttons |
| CarMax Red Accent | `#d4001a` | Vehicle card "View Details" CTA button |
| Light Blue Background | `#f0f7ff` | Hero section, price callout, bottom CTA section |
| Body Text | `#333333` | Paragraph text, vehicle detail values |
| Secondary Text | `#666666` | Detail labels, trust bar |
| Muted Text | `#999999` | Footer legal copy |

### Build in MCA — Step-by-Step UI Instructions

1. **Navigate:** Setup > Digital Experiences > CMS Workspaces > "CarMax Demo Content" (or Default Content Workspace)
2. **Create new content:** Click "Add Content" > Select "Email" (`sfdc_cms__email`)
3. **Name:** `Hearted Vehicle Follow-Up`
4. **API Name:** `Hearted_Vehicle_FollowUp` (this becomes part of the content key)
5. **Subject line:** `Your favorites are waiting, {{CX360_First_Name}}`
6. **Preheader:** `Compare your top picks side by side — they're still available`
7. **Email body — Add an HTML block:**
   - Click "+" to add a new block
   - Select "HTML" (custom HTML block)
   - Paste the full Handlebars template from above
8. **Connect Data Graph:**
   - In the email builder, open the "Data" panel
   - Select Data Source > "CarMax Customer 360" graph
   - This makes all `CX360_*` tokens available for merge fields
9. **Preview:** Use "Preview as Contact" and select Jane Dawson to verify:
   - Her first name renders in the greeting
   - Her 3 hearted vehicles render as cards (2023 Honda CR-V, 2024 Hyundai Tucson, 2022 Toyota RAV4)
   - Each card shows correct specs and price
10. **Save and Publish**

### Demo Stop 3 Script (Talking Points)

When presenting this email at Demo Stop 3:

1. "This email pulls Jane's hearted vehicles directly from the Data Graph — no data extension, no manual segmentation."
2. "The Handlebars loop iterates over each vehicle in the graph where IsHearted is 'true'."
3. "If Jane hearts a new vehicle tomorrow, the next send automatically includes it — no content update needed."
4. "Notice the CTA on each card links to the actual listing URL from the graph. Every element is personalized."
5. "This is one email template serving thousands of customers, each seeing their own unique vehicles."

---

## Email #2: Test Drive — No Purchase Nurture (Component-First)

**Campaign:** Test Drive - No Purchase Nurture
**Segment:** Vehicle Interest Waterfall — Priority 2 (Test Drive No Purchase)
**Demo Stop:** Stop 3 (secondary preview)
**Persona:** Jane Dawson (waterfall P2) / Marcus Thompson
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--Test_Drive_NoPurchase_Nurture`

### Content Concept

"Still Thinking It Over?" — A warm follow-up that references the specific vehicle test-driven, includes social proof (customer reviews), and highlights the CarMax no-pressure buying experience.

### Merge Fields

| Token | Graph devName | Source DMO Field |
|-------|---------------|-----------------|
| `{{CX360_First_Name}}` | CX360_First_Name | ssot__FirstName__c |
| `{{CX360_TestDrive_Store}}` | CX360_TestDrive_Store | CarMaxStore__c |
| `{{CX360_TestDrive_Date}}` | CX360_TestDrive_Date | TestDriveDate__c |
| `{{CX360_Vehicle_Make}}` | CX360_Vehicle_Make | Make__c |
| `{{CX360_Vehicle_Model}}` | CX360_Vehicle_Model | Model__c |

### Email Structure (Component Blocks)

Build this email entirely using the MCA Email Builder drag-and-drop components:

| # | Block Type | Content |
|---|-----------|---------|
| 1 | **Image Block** | CarMax logo (centered, navy background) |
| 2 | **Text Block** | Headline: "Still Thinking It Over, {{CX360_First_Name}}?" |
| 3 | **Text Block** | Body: "We hope you enjoyed your test drive of the {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}} at CarMax {{CX360_TestDrive_Store}}. There's no pressure — take all the time you need. But we wanted to make sure you have everything you need to make a confident decision." |
| 4 | **Divider** | Thin line separator |
| 5 | **Text Block** | Section header: "What Other Customers Are Saying" |
| 6 | **Text Block** | Review 1: "The whole experience was stress-free. I never felt pressured." — Sarah M., Richmond VA |
| 7 | **Text Block** | Review 2: "I test-drove 3 vehicles and took my time. That's the CarMax difference." — David K., Charlotte NC |
| 8 | **Divider** | Thin line separator |
| 9 | **Text Block** | Section header: "The CarMax Difference" |
| 10 | **Text Block** | Three bullet points: No-Haggle Pricing, Love Your Car Guarantee (30-day return), 150-Point Inspection |
| 11 | **Button Block** | Primary CTA: "View Your Test-Driven Vehicle" (background: #003468, text: #ffffff) |
| 12 | **Button Block** | Secondary CTA: "Get Pre-Qualified" (background: #ffffff, text: #003468, border: #003468) |
| 13 | **Text Block** | Footer: Legal, unsubscribe link |

### Build in MCA

1. Create new email content: `Test_Drive_NoPurchase_Nurture`
2. Subject line: `How was your test drive, {{CX360_First_Name}}?`
3. Preheader: `Your {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}} is still available at CarMax {{CX360_TestDrive_Store}}`
4. Add each component block in order (drag-and-drop)
5. For each text block with merge fields, use the "Insert Merge Field" button and select from the CarMax Customer 360 graph
6. Style all text blocks with CarMax brand fonts and colors
7. Preview with Jane Dawson or Marcus Thompson
8. Save and Publish

---

## Email #3: New Email Subscriber Welcome (Component-First)

**Campaign:** New Email Subscriber Welcome
**Segment:** New Email Subscribers
**Demo Stop:** Stop 3 — Aisha Thompson's email preview (contrasting email)
**Persona:** Aisha Thompson
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--Welcome_Email`

### Content Concept

"Welcome to CarMax" — A clean, feature-forward introduction to the CarMax digital experience. Three-column feature cards highlight key tools: Heart vehicles, Get Pre-Qualified, and the CarMax App.

**Demo purpose:** This email is shown alongside the Hearted Vehicle Follow-Up email at Demo Stop 3 to contrast a simple component-first email (Welcome) with a complex HTML-heavy email (Hearted Vehicle). The narrator can say: "Aisha is a new subscriber, so she gets a simple welcome. Jane, who has been browsing and hearting vehicles, gets a personalized vehicle comparison."

### Merge Fields

| Token | Graph devName | Source DMO Field |
|-------|---------------|-----------------|
| `{{CX360_First_Name}}` | CX360_First_Name | ssot__FirstName__c |

### Email Structure (Component Blocks)

| # | Block Type | Content |
|---|-----------|---------|
| 1 | **Image Block** | CarMax logo (centered, navy background) |
| 2 | **Text Block** | Headline: "Welcome to CarMax, {{CX360_First_Name}}!" |
| 3 | **Text Block** | Body: "You've just joined a community of smart car shoppers. At CarMax, we believe buying a car should be easy, transparent, and — dare we say — enjoyable. Here's how to get started." |
| 4 | **Divider** | Thin line separator |
| 5 | **Text Block** | Section header: "Three Things to Try First" |
| 6 | **Multi-Column Block** | Three columns, each containing: |
| | Column 1 | **Heart Your Favorites** — Browse over 50,000 vehicles and heart the ones you love. We'll keep track so you can compare later. |
| | Column 2 | **Get Pre-Qualified** — See your personalized financing options in as little as 2 minutes — with no impact to your credit score. |
| | Column 3 | **Download the App** — Search, save, and schedule test drives from your phone. Available on iOS and Android. |
| 7 | **Button Block** | Primary CTA: "Start Browsing" (background: #003468) |
| 8 | **Divider** | Thin line separator |
| 9 | **Text Block** | Trust copy: "Every CarMax vehicle comes with a 150-point inspection, no-haggle pricing, and our Love Your Car Guarantee — 30 days to return, no questions asked." |
| 10 | **Text Block** | Footer: Legal, unsubscribe |

### Build in MCA

1. Create new email content: `Welcome_Email`
2. Subject line: `Welcome to CarMax, {{CX360_First_Name}}!`
3. Preheader: `Your car-buying journey starts here. Browse 50,000+ vehicles.`
4. Use the multi-column component for the three feature cards
5. Style feature cards with light blue (#f0f7ff) background and navy (#003468) headers
6. Preview with Aisha Thompson
7. Save and Publish

---

## Email #4: Pre-Qualification Completion (Component-First)

**Campaign:** Pre-Qualification Completion
**Segment:** PreQual Shoppers
**Demo Stop:** Stop 3 (ancillary)
**Persona:** Raj Patel
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--PreQual_Completion`

### Content Concept

"Stop Wondering, Start Shopping" — Congratulates the customer on completing pre-qualification and provides clear next steps. Includes a pre-qualified "badge" visual element and an FAQ section addressing common post-qualification questions.

### Merge Fields

| Token | Graph devName | Source DMO Field |
|-------|---------------|-----------------|
| `{{CX360_First_Name}}` | CX360_First_Name | ssot__FirstName__c |

### Email Structure (Component Blocks)

| # | Block Type | Content |
|---|-----------|---------|
| 1 | **Image Block** | CarMax logo (centered, navy background) |
| 2 | **Text Block** | Headline: "You're Pre-Qualified, {{CX360_First_Name}}!" |
| 3 | **Text Block** | Badge area: Large checkmark icon + "Pre-Qualified" text on light blue (#f0f7ff) background |
| 4 | **Text Block** | Body: "Great news — you've taken a big step toward your next vehicle. Your pre-qualification is ready, which means you can shop with confidence knowing your financing options upfront. No surprises, no stress." |
| 5 | **Divider** | Thin line separator |
| 6 | **Text Block** | Section header: "What Happens Next?" |
| 7 | **Text Block** | Step 1: "Browse with confidence" — Your pre-qualified amount is ready. Search vehicles that fit your budget. |
| 8 | **Text Block** | Step 2: "Schedule a test drive" — Found something you love? Book a test drive online or in-store. |
| 9 | **Text Block** | Step 3: "Complete your purchase" — Financing is already in progress. We'll finalize the details at the store. |
| 10 | **Button Block** | Primary CTA: "Shop Within Your Budget" (background: #003468) |
| 11 | **Divider** | Thin line separator |
| 12 | **Text Block** | FAQ Section header: "Common Questions" |
| 13 | **Text Block** | Q1: "Does pre-qualification affect my credit score?" A: "No. Pre-qualification uses a soft pull that does not impact your credit." |
| 14 | **Text Block** | Q2: "How long is my pre-qualification valid?" A: "Your pre-qualification is valid for 30 days from completion." |
| 15 | **Text Block** | Q3: "Can I use this at any CarMax store?" A: "Yes. Your pre-qualification works at all 240+ CarMax locations nationwide." |
| 16 | **Text Block** | Footer: Legal, unsubscribe |

### Build in MCA

1. Create new email content: `PreQual_Completion`
2. Subject line: `You're pre-qualified, {{CX360_First_Name}}! Here's what's next.`
3. Preheader: `Shop with confidence — your financing options are ready.`
4. Build using drag-and-drop component blocks
5. Use a styled text block with background color for the "badge" area
6. Preview with Raj Patel
7. Save and Publish

---

## Email #5: Price Drop Alert (HTML-Heavy)

**Campaign:** Price Drop Alert
**Segment:** Price Drop Alert
**Demo Stop:** Stop 3 (ancillary)
**Persona:** Sarah Williams
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--Price_Drop_Alert`

### Content Concept

"Ready to Save?" — An attention-grabbing price drop notification with visual emphasis on the savings. Uses strikethrough styling on the old price and a highlighted new price. The urgency is authentic (inventory moves fast) rather than manufactured.

### Handlebars Template

```html
<!-- Price Drop Alert — Full Email Template -->
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">

  <!-- Header -->
  <div style="background-color: #003468; padding: 24px 32px; text-align: center;">
    <span style="color: #ffffff; font-size: 24px; font-weight: 700; letter-spacing: 1px;">CARMAX</span>
  </div>

  <!-- Price Drop Banner -->
  <div style="background-color: #d4001a; padding: 16px; text-align: center;">
    <span style="color: #ffffff; font-size: 20px; font-weight: 700;">PRICE DROP ALERT</span>
  </div>

  <!-- Greeting -->
  <div style="padding: 24px 32px 0 32px;">
    <p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0;">
      Hi {{CX360_First_Name}},<br/><br/>
      Great news — a vehicle you've been watching just dropped in price. At CarMax, our prices
      are upfront and no-haggle, so when the price drops, the savings are real.
    </p>
  </div>

  <!-- Vehicle + Price Card -->
  <div style="margin: 24px 32px; border: 2px solid #d4001a; border-radius: 8px; overflow: hidden;">

    <!-- Vehicle Name -->
    <div style="background-color: #003468; padding: 12px 16px;">
      <span style="color: #ffffff; font-size: 18px; font-weight: 600;">
        {{CX360_Vehicle_Year}} {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}}
      </span>
    </div>

    <!-- Price Comparison -->
    <div style="padding: 24px; text-align: center;">
      <div style="margin-bottom: 8px;">
        <span style="color: #999999; font-size: 14px; text-decoration: line-through;">
          Was: ${{CX360_Vehicle_OriginalPrice}}
        </span>
      </div>
      <div style="margin-bottom: 8px;">
        <span style="color: #d4001a; font-size: 32px; font-weight: 700;">
          Now: ${{CX360_Vehicle_Price}}
        </span>
      </div>
      <div style="background-color: #f0f7ff; padding: 8px 16px; border-radius: 4px; display: inline-block;">
        <span style="color: #003468; font-size: 16px; font-weight: 600;">
          You save ${{CX360_Vehicle_PriceDrop}}
        </span>
      </div>
    </div>

    <!-- Vehicle Specs -->
    <div style="padding: 0 24px 16px 24px;">
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
        <tr>
          <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Color</td>
          <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;">{{CX360_Vehicle_Color}}</td>
          <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Mileage</td>
          <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;">{{CX360_Vehicle_Mileage}} mi</td>
        </tr>
        <tr>
          <td style="padding: 4px 8px; color: #666666; font-size: 13px;">Store</td>
          <td style="padding: 4px 8px; color: #333333; font-size: 13px; font-weight: 600;" colspan="3">CarMax {{CX360_Vehicle_Store}}</td>
        </tr>
      </table>
    </div>

    <!-- CTA -->
    <div style="padding: 0 24px 24px 24px; text-align: center;">
      <a href="{{CX360_Vehicle_ListingURL}}" style="display: inline-block; background-color: #d4001a; color: #ffffff; padding: 14px 40px; border-radius: 4px; text-decoration: none; font-size: 15px; font-weight: 600;">
        See Updated Price
      </a>
    </div>
  </div>

  <!-- Secondary CTA -->
  <div style="padding: 0 32px 32px 32px; text-align: center;">
    <p style="color: #333333; font-size: 14px; margin: 0 0 12px 0;">
      Want to lock this in? Schedule a test drive today.
    </p>
    <a href="https://www.carmax.com/schedule-test-drive" style="display: inline-block; background-color: #003468; color: #ffffff; padding: 12px 32px; border-radius: 4px; text-decoration: none; font-size: 14px; font-weight: 600;">
      Schedule a Test Drive
    </a>
  </div>

  <!-- Footer -->
  <div style="background-color: #f5f5f5; padding: 24px 32px; text-align: center;">
    <p style="color: #999999; font-size: 11px; line-height: 1.5; margin: 0;">
      CarMax, Inc. | 12800 Tuckahoe Creek Pkwy, Richmond, VA 23238<br/>
      Prices are subject to change and vehicle availability is not guaranteed.<br/>
      <a href="{{unsubscribe_url}}" style="color: #003468; text-decoration: underline;">Unsubscribe</a> |
      <a href="https://www.carmax.com/privacy" style="color: #003468; text-decoration: underline;">Privacy Policy</a>
    </p>
  </div>

</div>
```

### Build in MCA

1. Create new email content: `Price_Drop_Alert`
2. Subject line: `Price drop on your {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}}!`
3. Preheader: `A vehicle you've been watching just got more affordable.`
4. Add as a single HTML block with the full Handlebars template
5. Connect to CarMax Customer 360 Data Graph
6. Preview with Sarah Williams
7. Save and Publish

**Note:** The `CX360_Vehicle_OriginalPrice` and `CX360_Vehicle_PriceDrop` tokens reference fields that may need to be added to the Data Graph if they are not already present. If the graph only has `CX360_Vehicle_Price`, the original price and savings amount can be hard-coded for demo purposes or computed via a Calculated Insight (Phase 3).

---

## Email #6: Saved Search Match (HTML-Heavy)

**Campaign:** Saved Search Match
**Segment:** Saved Search Match
**Demo Stop:** Stop 3 (ancillary)
**Persona:** (Generic — any customer with a saved search)
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--Saved_Search_Match`

### Content Concept

"It's a Match!" — A dating-app-inspired design that makes finding a matching vehicle feel exciting and personal. Uses a dynamic loop to show multiple matched vehicles. The playful tone differentiates this email from the more straightforward vehicle alerts.

### Handlebars Template

```html
<!-- Saved Search Match — Full Email Template -->
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">

  <!-- Header -->
  <div style="background-color: #003468; padding: 24px 32px; text-align: center;">
    <span style="color: #ffffff; font-size: 24px; font-weight: 700; letter-spacing: 1px;">CARMAX</span>
  </div>

  <!-- Match Banner -->
  <div style="background-color: #f0f7ff; padding: 32px; text-align: center;">
    <div style="font-size: 48px; margin-bottom: 8px;">&#10084;</div>
    <h1 style="color: #003468; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;">
      It's a Match!
    </h1>
    <p style="color: #333333; font-size: 16px; line-height: 1.5; margin: 0;">
      Hi {{CX360_First_Name}}, new inventory just arrived that matches your saved search.
    </p>
  </div>

  <!-- Matched Vehicles Loop -->
  {{#each MatchedVehicles}}
  <div style="margin: 16px 32px; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">

    <div style="padding: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color: #003468; font-size: 16px; font-weight: 600;">
          {{CX360_Vehicle_Year}} {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}}
        </span>
        <span style="color: #d4001a; font-size: 11px; font-weight: 700; background-color: #fff0f0; padding: 4px 8px; border-radius: 12px;">
          NEW
        </span>
      </div>
      <div style="margin-top: 8px;">
        <span style="color: #666666; font-size: 13px;">
          {{CX360_Vehicle_Color}} &bull; {{CX360_Vehicle_Mileage}} mi &bull; {{CX360_Vehicle_FuelType}}
        </span>
      </div>
      <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
        <span style="color: #003468; font-size: 20px; font-weight: 700;">${{CX360_Vehicle_Price}}</span>
        <a href="{{CX360_Vehicle_ListingURL}}" style="background-color: #003468; color: #ffffff; padding: 8px 20px; border-radius: 4px; text-decoration: none; font-size: 13px; font-weight: 600;">
          View Details
        </a>
      </div>
    </div>
  </div>
  {{/each}}

  <!-- Bottom CTA -->
  <div style="padding: 32px; text-align: center;">
    <p style="color: #333333; font-size: 14px; line-height: 1.5; margin: 0 0 16px 0;">
      Want to see all matches? View your full saved search results.
    </p>
    <a href="https://www.carmax.com/saved-searches" style="display: inline-block; background-color: #003468; color: #ffffff; padding: 14px 40px; border-radius: 4px; text-decoration: none; font-size: 15px; font-weight: 600;">
      View All Matches
    </a>
  </div>

  <!-- Footer -->
  <div style="background-color: #f5f5f5; padding: 24px 32px; text-align: center;">
    <p style="color: #999999; font-size: 11px; line-height: 1.5; margin: 0;">
      CarMax, Inc. | 12800 Tuckahoe Creek Pkwy, Richmond, VA 23238<br/>
      You're receiving this because you have an active saved search on CarMax.com.<br/>
      <a href="{{unsubscribe_url}}" style="color: #003468; text-decoration: underline;">Unsubscribe</a> |
      <a href="https://www.carmax.com/privacy" style="color: #003468; text-decoration: underline;">Privacy Policy</a>
    </p>
  </div>

</div>
```

### Build in MCA

1. Create new email content: `Saved_Search_Match`
2. Subject line: `It's a Match! New vehicles fit your search, {{CX360_First_Name}}`
3. Preheader: `New inventory just arrived that matches what you're looking for.`
4. Add as an HTML block
5. Connect to Data Graph — the `{{#each MatchedVehicles}}` loop iterates over matched vehicle records
6. Save and Publish

**Note on `MatchedVehicles`:** This loop name is conceptual. In the actual Data Graph, the loop iterates over `CX360_Vehicle` related objects. The filter criteria (matching saved search parameters) would be applied at the segment/flow level, not in the Handlebars template. For demo purposes, all vehicles associated with the contact in the graph will render.

---

## Email #7: Trade-In and Upgrade (Component-First)

**Campaign:** Trade-In and Upgrade
**Segment:** Trade-In (Einstein)
**Demo Stop:** Stop 2 (Einstein segmentation example)
**Persona:** David Chen
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--TradeIn_Upgrade`

### Content Concept

"Time for an Upgrade?" — A cross-sell email targeting owners of aging vehicles. Emphasizes the simplicity of the CarMax trade-in process and the availability of newer models. The tone is helpful rather than pushy — suggesting rather than pressuring.

### Merge Fields

| Token | Graph devName | Source DMO Field |
|-------|---------------|-----------------|
| `{{CX360_First_Name}}` | CX360_First_Name | ssot__FirstName__c |

### Email Structure (Component Blocks)

| # | Block Type | Content |
|---|-----------|---------|
| 1 | **Image Block** | CarMax logo (centered, navy background) |
| 2 | **Text Block** | Headline: "Time for an Upgrade, {{CX360_First_Name}}?" |
| 3 | **Text Block** | Body: "We know you love your current ride — but what if your next one could be even better? With CarMax, trading in is as easy as 1-2-3. Get an instant online offer, bring your vehicle to any store, and drive away in something new." |
| 4 | **Divider** | Thin line separator |
| 5 | **Text Block** | Section header: "How CarMax Trade-In Works" |
| 6 | **Text Block** | Step 1: "Get Your Instant Offer" — Answer a few questions about your vehicle and get a real offer in minutes. Valid for 7 days. |
| 7 | **Text Block** | Step 2: "Bring It In" — Visit any CarMax store. We'll verify the vehicle condition and finalize your offer. |
| 8 | **Text Block** | Step 3: "Get Paid or Upgrade" — Take the cash, or apply it toward your next vehicle. Either way, you're in control. |
| 9 | **Button Block** | Primary CTA: "Get Your Instant Offer" (background: #d4001a) |
| 10 | **Divider** | Thin line separator |
| 11 | **Text Block** | Section header: "Why Trade In With CarMax?" |
| 12 | **Text Block** | Bullet 1: "Competitive offers" — Based on real market data, not guesswork. |
| 13 | **Text Block** | Bullet 2: "No obligation" — You can sell to us even if you don't buy from us. |
| 14 | **Text Block** | Bullet 3: "Tax savings" — In most states, your trade-in value reduces the taxable amount on your next purchase. |
| 15 | **Button Block** | Secondary CTA: "Browse Upgrade Options" (background: #003468) |
| 16 | **Text Block** | Footer: Legal, unsubscribe |

### Build in MCA

1. Create new email content: `TradeIn_Upgrade`
2. Subject line: `Thinking about upgrading, {{CX360_First_Name}}?`
3. Preheader: `Get an instant offer on your current vehicle — it takes minutes.`
4. Build with drag-and-drop component blocks
5. Preview with David Chen
6. Save and Publish

---

## Email #8: Instant Offer Abandonment (HTML-Heavy)

**Campaign:** Instant Offer Abandonment
**Segment:** Instant Offer Abandonment
**Demo Stop:** Stop 3 (ancillary)
**Persona:** (Generic — any customer who abandoned the Instant Offer flow)
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__email--Instant_Offer_Abandonment`

### Content Concept

"Your Online Offer Is Almost Ready" — A recovery email for customers who started but did not complete the Instant Offer flow. Uses a progress indicator to show how close they were to completion, creating a gentle pull back to the flow. Includes a countdown element showing offer validity.

### Handlebars Template

```html
<!-- Instant Offer Abandonment — Full Email Template -->
<div style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">

  <!-- Header -->
  <div style="background-color: #003468; padding: 24px 32px; text-align: center;">
    <span style="color: #ffffff; font-size: 24px; font-weight: 700; letter-spacing: 1px;">CARMAX</span>
  </div>

  <!-- Hero -->
  <div style="padding: 32px; text-align: center;">
    <h1 style="color: #003468; font-size: 26px; font-weight: 700; margin: 0 0 8px 0;">
      Your Online Offer Is Almost Ready
    </h1>
    <p style="color: #333333; font-size: 16px; line-height: 1.5; margin: 0;">
      Hi {{CX360_First_Name}}, it looks like you started getting an Instant Offer
      but didn't finish. No worries — we saved your progress.
    </p>
  </div>

  <!-- Progress Indicator -->
  <div style="margin: 0 32px 24px 32px; padding: 20px; background-color: #f0f7ff; border-radius: 8px;">
    <p style="color: #003468; font-size: 14px; font-weight: 600; margin: 0 0 12px 0; text-align: center;">
      Your Progress
    </p>
    <!-- Progress Bar -->
    <div style="background-color: #e0e0e0; border-radius: 12px; height: 24px; overflow: hidden;">
      <div style="background-color: #003468; height: 24px; width: 65%; border-radius: 12px; text-align: center; line-height: 24px;">
        <span style="color: #ffffff; font-size: 12px; font-weight: 600;">65% Complete</span>
      </div>
    </div>
    <p style="color: #666666; font-size: 12px; margin: 8px 0 0 0; text-align: center;">
      Just a few more details and you'll have your offer.
    </p>
  </div>

  <!-- Countdown / Validity -->
  <div style="margin: 0 32px 24px 32px; padding: 16px; border: 2px solid #d4001a; border-radius: 8px; text-align: center;">
    <p style="color: #333333; font-size: 14px; margin: 0 0 4px 0;">
      Your saved progress expires in
    </p>
    <span style="color: #d4001a; font-size: 28px; font-weight: 700;">
      {{CX360_WebEng_OfferExpiryDays}} days
    </span>
    <p style="color: #666666; font-size: 12px; margin: 4px 0 0 0;">
      After that, you'll need to start over.
    </p>
  </div>

  <!-- CTA -->
  <div style="padding: 0 32px 24px 32px; text-align: center;">
    <a href="https://www.carmax.com/sell-my-car" style="display: inline-block; background-color: #d4001a; color: #ffffff; padding: 14px 40px; border-radius: 4px; text-decoration: none; font-size: 15px; font-weight: 600;">
      Finish Your Offer
    </a>
  </div>

  <!-- Why Complete Section -->
  <div style="padding: 0 32px 32px 32px;">
    <h3 style="color: #003468; font-size: 16px; font-weight: 600; margin: 0 0 12px 0;">
      Why finish your offer?
    </h3>
    <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
      <tr>
        <td style="padding: 8px 0; color: #333333; font-size: 14px; line-height: 1.5;">
          <strong style="color: #003468;">Real offer, no obligation</strong><br/>
          Get a competitive offer based on market data. You're never obligated to sell.
        </td>
      </tr>
      <tr>
        <td style="padding: 8px 0; color: #333333; font-size: 14px; line-height: 1.5;">
          <strong style="color: #003468;">Valid for 7 days</strong><br/>
          Once you have your offer, it's good for a full week. Plenty of time to decide.
        </td>
      </tr>
      <tr>
        <td style="padding: 8px 0; color: #333333; font-size: 14px; line-height: 1.5;">
          <strong style="color: #003468;">Any CarMax store</strong><br/>
          Redeem your offer at any of our 240+ locations nationwide.
        </td>
      </tr>
    </table>
  </div>

  <!-- Footer -->
  <div style="background-color: #f5f5f5; padding: 24px 32px; text-align: center;">
    <p style="color: #999999; font-size: 11px; line-height: 1.5; margin: 0;">
      CarMax, Inc. | 12800 Tuckahoe Creek Pkwy, Richmond, VA 23238<br/>
      You started an Instant Offer on CarMax.com. This is a reminder to complete it.<br/>
      <a href="{{unsubscribe_url}}" style="color: #003468; text-decoration: underline;">Unsubscribe</a> |
      <a href="https://www.carmax.com/privacy" style="color: #003468; text-decoration: underline;">Privacy Policy</a>
    </p>
  </div>

</div>
```

### Build in MCA

1. Create new email content: `Instant_Offer_Abandonment`
2. Subject line: `You're 65% done — finish your CarMax Instant Offer`
3. Preheader: `Your saved progress won't last forever. Complete your offer in minutes.`
4. Add as an HTML block
5. Connect to Data Graph
6. Save and Publish

**Note:** The `CX360_WebEng_OfferExpiryDays` token is conceptual. In production this would be a computed field. For demo purposes, hard-code "5" or use a static value in the template.

---

## SMS Messages (4)

SMS messages are created in the MCA CMS Workspace using the `sfdc_cms__sms` content type (or the SMS authoring interface within Marketing Cloud on Core). Each message must stay under 160 characters for a single SMS segment.

### SMS #1: Test Drive Reminder

**Campaign:** Test Drive - No Purchase Nurture
**Segment:** Vehicle Interest Waterfall — Priority 2
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__sms--TestDrive_Reminder`

```
Hi {{CX360_First_Name}}, your {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}} is still at CarMax {{CX360_TestDrive_Store}}. Ready for another look? Book here: https://cmx.co/td
```

**Character count:** ~155 (varies with merge field values)
**Merge fields:** CX360_First_Name, CX360_Vehicle_Make, CX360_Vehicle_Model, CX360_TestDrive_Store
**CTA:** Shortened URL to test drive scheduling page

---

### SMS #2: Price Drop Alert

**Campaign:** Price Drop Alert
**Segment:** Price Drop Alert
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__sms--PriceDrop_SMS`

```
{{CX360_First_Name}}, price drop! Your hearted {{CX360_Vehicle_Make}} {{CX360_Vehicle_Model}} just got more affordable. See the new price: https://cmx.co/pd ❤️
```

**Character count:** ~145 (varies with merge field values)
**Merge fields:** CX360_First_Name, CX360_Vehicle_Make, CX360_Vehicle_Model
**CTA:** Shortened URL to vehicle listing
**Emoji:** Heart emoji aligns with the "hearted vehicle" concept

---

### SMS #3: Instant Offer Expiring

**Campaign:** Instant Offer Abandonment
**Segment:** Instant Offer Abandonment
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__sms--InstantOffer_Expiring`

```
{{CX360_First_Name}}, your CarMax Instant Offer progress expires soon. Finish in minutes and get a real offer: https://cmx.co/io
```

**Character count:** ~130 (varies with merge field values)
**Merge fields:** CX360_First_Name
**CTA:** Shortened URL to Instant Offer resume page

---

### SMS #4: Saved Search Match

**Campaign:** Saved Search Match
**Segment:** Saved Search Match
**Content Key:** `marketing--Default_Content_Workspace.sfdc_cms__sms--SavedSearch_Match`

```
{{CX360_First_Name}}, new vehicles matching your saved search just arrived at CarMax! See your matches: https://cmx.co/ss
```

**Character count:** ~120 (varies with merge field values)
**Merge fields:** CX360_First_Name
**CTA:** Shortened URL to saved search results

---

## Build Order

Content should be built in priority order to support the demo narrative:

### Phase 7A: Flagship Email (Build First)

| Item | Priority | Reason |
|------|----------|--------|
| Email #1: Hearted Vehicle Follow-Up | CRITICAL | Demo Stop 3 focal point, Data Graph repeater demo |

**Estimated time:** 30-45 min (HTML template entry + Data Graph connection + preview verification)

### Phase 7B: Waterfall-Related Content

| Item | Priority | Reason |
|------|----------|--------|
| Email #2: Test Drive No Purchase Nurture | HIGH | Waterfall P2, Jane Dawson alternate path |
| SMS #1: Test Drive Reminder | HIGH | Paired with Email #2 in multi-channel flow |

**Estimated time:** 20-30 min

### Phase 7C: Remaining Content

| Item | Priority | Reason |
|------|----------|--------|
| Email #3: Welcome Email | MEDIUM | Aisha Thompson's Demo Stop 3 contrasting email |
| Email #4: Pre-Qualification Completion | MEDIUM | Raj Patel journey |
| Email #5: Price Drop Alert | MEDIUM | Shows HTML-heavy personalization |
| Email #6: Saved Search Match | LOW | Ancillary |
| Email #7: Trade-In and Upgrade | LOW | Einstein segment tie-in |
| Email #8: Instant Offer Abandonment | LOW | Abandonment recovery pattern |
| SMS #2: Price Drop Alert | LOW | Paired with Email #5 |
| SMS #3: Instant Offer Expiring | LOW | Paired with Email #8 |
| SMS #4: Saved Search Match | LOW | Paired with Email #6 |

**Estimated time:** 60-90 min for all remaining content

---

## CMS Workspace Setup

Before building content, ensure the CMS Workspace exists and is properly configured.

### Create Workspace (if Default Content Workspace is not suitable)

1. **Navigate:** Setup > Digital Experiences > CMS Workspaces
2. **Click:** "Add Workspace"
3. **Name:** `CarMax Demo Content`
4. **Language:** English (US)
5. **Channels:** Select "Marketing" (this enables `sfdc_cms__email` and `sfdc_cms__sms` content types)

### Folder Structure

Organize content within the workspace for clarity:

```
CarMax Demo Content (Workspace)
├── /emails/
│   ├── Hearted_Vehicle_FollowUp
│   ├── Test_Drive_NoPurchase_Nurture
│   ├── Welcome_Email
│   ├── PreQual_Completion
│   ├── Price_Drop_Alert
│   ├── Saved_Search_Match
│   ├── TradeIn_Upgrade
│   └── Instant_Offer_Abandonment
├── /sms/
│   ├── TestDrive_Reminder
│   ├── PriceDrop_SMS
│   ├── InstantOffer_Expiring
│   └── SavedSearch_Match
├── /images/
│   └── (placeholder for any uploaded brand images)
└── /shared-components/
    └── (reusable header/footer blocks, if supported)
```

### Verify Content Types Are Available

After creating the workspace, confirm that the email and SMS content types are available:

1. Click into the workspace
2. Click "Add Content"
3. Verify "Email" (`sfdc_cms__email`) appears in the content type list
4. Verify "SMS" (`sfdc_cms__sms`) appears in the content type list (if SMS is licensed)

**If content types are missing:** Marketing content types require the Marketing Cloud on Core license to be provisioned. Check Setup > Feature Settings > Marketing to confirm MCA is enabled.

---

## Data Graph to Email Field Mapping

Complete mapping of every personalization token used across all 8 emails and 4 SMS messages back to the Data Graph fields defined in Phase 4.

### Individual (Root Object) Fields

| Token in Template | Graph devName | Source DMO | Source Field | Used In |
|-------------------|---------------|-----------|-------------|---------|
| `{{CX360_First_Name}}` | CX360_First_Name | ssot__Individual__dlm | ssot__FirstName__c | All 8 emails, all 4 SMS |
| `{{CX360_Last_Name}}` | CX360_Last_Name | ssot__Individual__dlm | ssot__LastName__c | (Available, not used in templates) |
| `{{CX360_PersonName}}` | CX360_PersonName | ssot__Individual__dlm | ssot__PersonName__c | (Available, not used in templates) |

### Vehicle (Related Object) Fields

| Token in Template | Graph devName | Source DMO | Source Field | Used In |
|-------------------|---------------|-----------|-------------|---------|
| `{{CX360_Vehicle_Make}}` | CX360_Vehicle_Make | CarMax_Vehicle__dlm | Make__c | Email #1, #2, #5, #6; SMS #1, #2 |
| `{{CX360_Vehicle_Model}}` | CX360_Vehicle_Model | CarMax_Vehicle__dlm | Model__c | Email #1, #2, #5, #6; SMS #1, #2 |
| `{{CX360_Vehicle_Year}}` | CX360_Vehicle_Year | CarMax_Vehicle__dlm | Year__c | Email #1, #5, #6 |
| `{{CX360_Vehicle_Price}}` | CX360_Vehicle_Price | CarMax_Vehicle__dlm | Price__c | Email #1, #5, #6 |
| `{{CX360_Vehicle_Color}}` | CX360_Vehicle_Color | CarMax_Vehicle__dlm | Color__c | Email #1, #5, #6 |
| `{{CX360_Vehicle_BodyType}}` | CX360_Vehicle_BodyType | CarMax_Vehicle__dlm | BodyType__c | Email #1 |
| `{{CX360_Vehicle_FuelType}}` | CX360_Vehicle_FuelType | CarMax_Vehicle__dlm | FuelType__c | Email #1, #6 |
| `{{CX360_Vehicle_Mileage}}` | CX360_Vehicle_Mileage | CarMax_Vehicle__dlm | Mileage__c | Email #1, #5, #6 |
| `{{CX360_Vehicle_Store}}` | CX360_Vehicle_Store | CarMax_Vehicle__dlm | CarMaxStore__c | Email #1, #5 |
| `{{CX360_Vehicle_IsHearted}}` | CX360_Vehicle_IsHearted | CarMax_Vehicle__dlm | Is_Hearted__c | Email #1 (loop filter) |
| `{{CX360_Vehicle_ListingURL}}` | CX360_Vehicle_ListingURL | CarMax_Vehicle__dlm | ListingURL__c | Email #1, #5, #6 |

### Test Drive (Related Object) Fields

| Token in Template | Graph devName | Source DMO | Source Field | Used In |
|-------------------|---------------|-----------|-------------|---------|
| `{{CX360_TestDrive_Store}}` | CX360_TestDrive_Store | CarMax_TestDrive__dlm | CarMaxStore__c | Email #2; SMS #1 |
| `{{CX360_TestDrive_Date}}` | CX360_TestDrive_Date | CarMax_TestDrive__dlm | TestDriveDate__c | Email #2 |

### Web Engagement (Related Object) Fields

| Token in Template | Graph devName | Source DMO | Source Field | Used In |
|-------------------|---------------|-----------|-------------|---------|
| `{{CX360_WebEng_EventType}}` | CX360_WebEng_EventType | ssot__WebsiteEngagement__dlm | ssot__EngagementChannelActionId__c | (Available for future use) |
| `{{CX360_WebEng_OfferExpiryDays}}` | *Conceptual* | *Not in graph* | *Computed* | Email #8 (hard-code for demo) |

### Tokens NOT in Data Graph (Demo Workarounds)

| Token | Status | Workaround |
|-------|--------|-----------|
| `{{CX360_Vehicle_OriginalPrice}}` | Not in Phase 4 graph | Hard-code in demo template OR add field to graph |
| `{{CX360_Vehicle_PriceDrop}}` | Not in Phase 4 graph | Hard-code in demo template OR compute via CI |
| `{{CX360_WebEng_OfferExpiryDays}}` | Not in Phase 4 graph | Hard-code "5" in template for demo |
| `{{unsubscribe_url}}` | System-provided | MCA injects this automatically at send time |
| `{{MatchedVehicles}}` | Alias for CX360_Vehicle | Use `{{#each CX360_Vehicle}}` in actual implementation |

---

## Content to Campaign to Segment Alignment

Complete alignment table showing how every content piece maps to its campaign, segment, and content type.

| Email / SMS | Campaign (Phase 6) | Segment (Phase 5) | Type | Demo Stop | Content Key |
|-------------|--------------------|--------------------|------|-----------|-------------|
| Email #1: Hearted Vehicle Follow-Up | Hearted Vehicle Follow-Up | Waterfall P1: Hearted Vehicle | HTML-Heavy | Stop 3 (flagship) | `Hearted_Vehicle_FollowUp` |
| Email #2: Test Drive No Purchase | Test Drive - No Purchase Nurture | Waterfall P2: Test Drive No Purchase | Component-First | Stop 3 | `Test_Drive_NoPurchase_Nurture` |
| Email #3: Welcome Email | New Email Subscriber Welcome | New Email Subscribers | Component-First | Stop 3 (Aisha) | `Welcome_Email` |
| Email #4: Pre-Qual Completion | Pre-Qualification Completion | PreQual Shoppers | Component-First | Stop 3 | `PreQual_Completion` |
| Email #5: Price Drop Alert | Price Drop Alert | Price Drop Alert | HTML-Heavy | Stop 3 | `Price_Drop_Alert` |
| Email #6: Saved Search Match | Saved Search Match | Saved Search Match | HTML-Heavy | Stop 3 | `Saved_Search_Match` |
| Email #7: Trade-In Upgrade | Trade-In and Upgrade | Trade-In (Einstein) | Component-First | Stop 2 | `TradeIn_Upgrade` |
| Email #8: Instant Offer Abandon | Instant Offer Abandonment | Instant Offer Abandonment | HTML-Heavy | Stop 3 | `Instant_Offer_Abandonment` |
| SMS #1: Test Drive Reminder | Test Drive - No Purchase Nurture | Waterfall P2 | SMS | Stop 4 | `TestDrive_Reminder` |
| SMS #2: Price Drop | Price Drop Alert | Price Drop Alert | SMS | Stop 4 | `PriceDrop_SMS` |
| SMS #3: Instant Offer Expiring | Instant Offer Abandonment | Instant Offer Abandonment | SMS | Stop 4 | `InstantOffer_Expiring` |
| SMS #4: Saved Search Match | Saved Search Match | Saved Search Match | SMS | Stop 4 | `SavedSearch_Match` |

### Campaigns WITHOUT Dedicated Content (Phase 7)

These campaigns from Phase 6 do not have email/SMS content built in Phase 7:

| Campaign | Reason |
|----------|--------|
| EV Consideration Nurture | Einstein segment demo only (Stop 2); no email needed for demo |
| Seasonal Push - Memorial Day | Waterfall P3 catch-all; serves as a concept, not a sent email |

---

## Critical Notes & Gotchas

### 1. Dynamic Loop Requires Built Data Graph
The `{{#each CX360_Vehicle}}` loop in Email #1 will NOT render vehicle cards unless the Data Graph (Phase 4) has been built via the UI (Step 4 in Phase 4). A deployed-but-unbuilt graph has the definition but no operational data. If the graph is not built, the loop renders zero items and the email shows only the static greeting and CTA.

### 2. Handlebars JS Syntax (Not AMPscript)
MCA uses Handlebars JS, not AMPscript. Key syntax:
- **Merge field:** `{{CX360_First_Name}}` (double curly braces, no `%%` or `=` prefix)
- **Loop:** `{{#each CX360_Vehicle}}...{{/each}}`
- **Conditional:** `{{#if CX360_Vehicle_IsHearted}}...{{/if}}`
- **Negation:** `{{#unless CX360_Vehicle_IsPurchased}}...{{/unless}}`
- **Comment:** `{{!-- This is a comment --}}`

Common mistake: Using AMPscript syntax (`%%FirstName%%` or `=FirstName`) will render as literal text, not merge fields.

### 3. Component-First Emails Use Drag-and-Drop Builder
Emails #2, #3, #4, and #7 are built using the MCA Email Builder's drag-and-drop component blocks. These do NOT require writing HTML. Merge fields are inserted via the builder's "Insert Merge Field" button, which connects to the Data Graph and presents available fields in a picker UI.

### 4. HTML Blocks Can Mix with Component Blocks
Within a single email, you can combine drag-and-drop component blocks with custom HTML blocks. This means you could build Email #1's header and footer as component blocks and insert the vehicle card repeater as an HTML block in between. The build instructions above use a single HTML block for simplicity, but mixing is supported.

### 5. SMS Character Limit (160 per segment)
A single SMS segment is 160 characters for GSM-7 encoding (standard Latin characters). If merge fields resolve to long values (e.g., a long vehicle model name), the message may spill into a second segment. Keep base template text short and account for the longest plausible merge field values.

Special characters and emojis use UCS-2 encoding, which reduces the segment limit to 70 characters. SMS #2 includes a heart emoji — verify that the total resolved message stays under 70 chars per segment or remove the emoji.

### 6. Image References — Do Not Reference Non-Existent Images
The email templates above do NOT include `<img>` tags pointing to external URLs. This is intentional. In a demo environment, referencing images that do not exist (e.g., `https://cdn.carmax.com/vehicle-images/123.jpg`) will show broken image icons. Instead:
- Use text-based "CarMax" header instead of a logo image
- Use the heart HTML entity (`&#10084;`) in Email #6 instead of an image
- Vehicle images are omitted from vehicle cards — the specs and price are the demo focus

If images are needed, upload them to the CMS Workspace's `/images/` folder first and reference the CMS-hosted URL.

### 7. CarMax Brand Colors
All emails use a consistent color palette. If colors look wrong in preview, verify the hex codes:

| Element | Correct Hex | Common Mistake |
|---------|------------|----------------|
| Primary Blue (header, CTA) | `#003468` | Using `#0052CC` (Salesforce blue) |
| Red Accent (vehicle CTA) | `#d4001a` | Using `#FF0000` (pure red) |
| Light Blue Background | `#f0f7ff` | Using `#EAF5FF` (too saturated) |
| Body Text | `#333333` | Using `#000000` (pure black, too harsh) |

### 8. Test with Jane Dawson
Jane Dawson is the primary test persona for Email #1 (Hearted Vehicle Follow-Up). Her Data Graph record should include:
- First Name: Jane
- 3 hearted vehicles: 2023 Honda CR-V, 2024 Hyundai Tucson, 2022 Toyota RAV4
- Each vehicle has IsHearted = 'true', with Price, Color, Mileage, Store, and Listing URL populated

Use the "Preview as Contact" feature in the MCA Email Builder and select Jane Dawson to verify the dynamic loop renders her 3 vehicle cards correctly.

### 9. Email Build Is Entirely UI-Based
There is no CLI command to create email content in MCA. The `sf` CLI does not support `sfdc_cms__email` content creation. All email and SMS content must be built through the Salesforce UI:
- Navigate: Setup > Digital Experiences > CMS Workspaces > [Workspace] > Add Content > Email
- This is a MANUAL process — plan for 15-30 minutes per email

### 10. SMS Authoring Path
SMS content in MCA may be authored through:
- **CMS Workspace:** Setup > Digital Experiences > CMS Workspaces > Add Content > SMS
- **Flow Builder:** Directly within the Send SMS action in a segment-triggered flow
- **Marketing Home:** If the Marketing Home app is enabled, SMS templates may be accessible there

The exact path depends on the org configuration. Try the CMS Workspace path first. If `sfdc_cms__sms` is not available as a content type, the SMS messages can be authored inline within the flow actions (Phase 8).

---

## Estimated Execution Time

| Phase | Items | Duration | Notes |
|-------|-------|----------|-------|
| CMS Workspace Setup | 1 workspace, folders | 5-10 min | One-time setup |
| Phase 7A: Flagship Email (#1) | 1 email | 30-45 min | HTML entry, Data Graph connection, preview verification |
| Phase 7B: Waterfall Content (#2, SMS #1) | 1 email, 1 SMS | 20-30 min | Component-first email is faster than HTML |
| Phase 7C: Remaining Emails (#3-#8) | 6 emails | 60-90 min | Mix of component-first and HTML-heavy |
| Phase 7C: Remaining SMS (#2-#4) | 3 SMS | 10-15 min | Short messages, quick to author |
| Verification & Preview | All 12 items | 15-20 min | Preview each as target persona |
| **Total** | **8 emails + 4 SMS** | **~2.5-3.5 hours** | **All UI-based, no CLI** |

---

## Verification Checklist

After building all content, verify each item:

### Email Verification

- [ ] Email #1 (Hearted Vehicle Follow-Up): Dynamic loop renders Jane Dawson's 3 vehicle cards
- [ ] Email #1: Each vehicle card shows correct Make, Model, Year, Price, Color, Mileage, Store
- [ ] Email #1: "View Details" CTA links to correct Listing URL from graph
- [ ] Email #2 (Test Drive Nurture): Merge fields resolve for Jane/Marcus
- [ ] Email #3 (Welcome): Renders for Aisha Thompson with first name
- [ ] Email #4 (Pre-Qual): Renders for Raj Patel
- [ ] Email #5 (Price Drop): Price display with strikethrough renders correctly
- [ ] Email #6 (Saved Search Match): Vehicle loop renders
- [ ] Email #7 (Trade-In): Component layout renders cleanly
- [ ] Email #8 (Instant Offer): Progress bar renders, countdown displays

### SMS Verification

- [ ] SMS #1 (Test Drive): Under 160 characters with resolved merge fields
- [ ] SMS #2 (Price Drop): Character count verified (emoji may push to UCS-2)
- [ ] SMS #3 (Instant Offer): Under 160 characters
- [ ] SMS #4 (Saved Search): Under 160 characters

### Cross-Phase Verification

- [ ] Data Graph (Phase 4) is built (not just deployed)
- [ ] All CX360_* tokens in templates match devNames in the graph entity payload
- [ ] Content keys match the format expected by Phase 8 flows
- [ ] Segments (Phase 5) referenced by each email are published with members

---

## Phase Completion Checklist

- [ ] CMS Workspace created with folder structure
- [ ] Email #1 (Hearted Vehicle Follow-Up) built and verified with Jane Dawson preview
- [ ] Email #2 (Test Drive No Purchase) built with component blocks
- [ ] Email #3 (Welcome) built — Aisha Thompson preview confirmed
- [ ] Email #4 (Pre-Qual Completion) built
- [ ] Email #5 (Price Drop Alert) built with HTML template
- [ ] Email #6 (Saved Search Match) built with HTML template
- [ ] Email #7 (Trade-In Upgrade) built with component blocks
- [ ] Email #8 (Instant Offer Abandonment) built with HTML template
- [ ] SMS #1 (Test Drive Reminder) authored
- [ ] SMS #2 (Price Drop) authored
- [ ] SMS #3 (Instant Offer Expiring) authored
- [ ] SMS #4 (Saved Search Match) authored
- [ ] All content published in CMS Workspace
- [ ] Data Graph to Email field mapping verified
- [ ] Content keys documented for Phase 8 flow integration
