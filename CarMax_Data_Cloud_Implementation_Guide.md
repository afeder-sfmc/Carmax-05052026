# CarMax Data Cloud Implementation Guide

> **Generated:** May 13, 2026 | **Org:** Carmax MM

---

## Overview

| Metric | Value |
|--------|-------|
| Custom Data Streams | 3 |
| Total Records Ingested | 13,207 |
| All Streams Active | ✅ Yes |
| Unified Profiles | 1,063 |
| Identity Resolution | ✅ Running |
| All Linked to Individual | ✅ Yes |
| Calculated Insights | 4 |

The CarMax org has **3 custom data streams** ingested via the Ingestion API. All are active, successfully running, and fully mapped to custom or standard DMOs. Additionally, **4 Calculated Insights** derive behavioral and preference metrics from the ingested data.

---

## Custom Data Stream Inventory

| Stream | Category | Status | Records | Target DMO | Fields Mapped |
|--------|----------|--------|---------|------------|---------------|
| CarMax Test Drive | Engagement | ✅ Active | 144 | CarMax_TestDrive__dlm | 15 / 17 |
| CarMax Vehicle | Profile | ✅ Active | 320 | CarMax_Vehicle__dlm | 26 / 27 |
| CarMax Web Engagement | Engagement | ✅ Active | 12,743 | ssot__WebsiteEngagement__dlm | 15 / 17 |

---

## Stream 1: CarMax Test Drive

- **DLO:** CarMax_TestDrive_Stream_TestDri_0AB23050__dll
- **Target DMO:** CarMax_TestDrive__dlm (Custom — Engagement)
- **Records:** 144

Captures test drive events at CarMax stores, including vehicle tested, outcome, and conversion tracking.

### Field Mappings (DLO → DMO)

| Source Field (DLO) | Target Field (DMO) | Purpose |
|--------------------|-------------------|---------|
| TestDriveId__c | TestDriveId__c | Primary Key |
| IndividualId__c | IndividualId__c | 🔗 Links to Individual DMO |
| VehicleId__c | VehicleId__c | 🔗 Links to Vehicle DMO |
| TestDriveDate__c | TestDriveDate__c | Date of test drive |
| EventDateTime__c | EventDateTime__c | Event timestamp |
| VIN__c | VIN__c | Vehicle VIN |
| CarMaxStore__c | CarMaxStore__c | Store location |
| ConvertedToPurchase__c | ConvertedToPurchase__c | Conversion flag |
| Outcome__c | Outcome__c | Drive outcome |
| Notes__c | Notes__c | Additional notes |
| DataSource__c | DataSource__c | System — data source |
| DataSourceObject__c | DataSourceObject__c | System — source object |
| KQ_TestDriveId__c | KQ_TestDriveId__c | System — key qualifier |
| KQ_IndividualId__c | KQ_IndividualId__c | System — key qualifier |
| KQ_VehicleId__c | KQ_VehicleId__c | System — key qualifier |

---

## Stream 2: CarMax Vehicle

- **DLO:** CarMax_Vehicle_Stream_VehiclePr_0AB19D2B__dll
- **Target DMO:** CarMax_Vehicle__dlm (Custom — Profile)
- **Records:** 320

Vehicle inventory/profile data including make, model, pricing, mileage, and customer "hearting" (favoriting) activity.

### Field Mappings (DLO → DMO)

| Source Field (DLO) | Target Field (DMO) | Purpose |
|--------------------|-------------------|---------|
| VehicleId__c | VehicleId__c | Primary Key |
| IndividualId__c | IndividualId__c | 🔗 Links to Individual DMO |
| Make__c | Make__c | Vehicle make |
| Model__c | Model__c | Vehicle model |
| Year__c | Year__c | Model year |
| VIN__c | VIN__c | Vehicle VIN |
| Price__c | Price__c | Price |
| Mileage__c | Mileage__c | Odometer mileage |
| Color__c | Color__c | Exterior color |
| BodyType__c | BodyType__c | Body type (SUV, sedan, etc.) |
| FuelType__c | FuelType__c | Fuel type |
| Transmission__c | Transmission__c | Transmission type |
| Doors__c | Doors__c | Number of doors |
| Status__c | Status__c | Listing status |
| IsPurchased__c | IsPurchased__c | Purchase flag |
| PurchaseDate__c | PurchaseDate__c | Date purchased |
| IsHearted__c | IsHearted__c | Favorited flag |
| HeartedById__c | HeartedById__c | Who favorited |
| HeartedDate__c | HeartedDate__c | Favorite date |
| ListingURL__c | ListingURL__c | Listing URL |
| CarMaxStore__c | CarMaxStore__c | Store location |
| LastModified__c | LastModified__c | Last modified timestamp |
| DataSource__c | DataSource__c | System — data source |
| DataSourceObject__c | DataSourceObject__c | System — source object |
| KQ_VehicleId__c | KQ_VehicleId__c | System — key qualifier |
| KQ_IndividualId__c | KQ_IndividualId__c | System — key qualifier |

---

## Stream 3: CarMax Web Engagement

- **DLO:** CarMax_WebEng_Stream_WebEngagem_0AB285C2__dll
- **Target DMO:** ssot__WebsiteEngagement__dlm (Standard — Engagement)
- **Records:** 12,743

Web engagement events mapped to the **standard WebsiteEngagement DMO**, including UTM parameters, device type, and vehicle VIN for product-level tracking.

### Field Mappings (DLO → DMO)

| Source Field (DLO) | Target Field (DMO) | Purpose |
|--------------------|-------------------|---------|
| EngagementId__c | ssot__Id__c | Primary Key |
| IndividualId__c | ssot__IndividualId__c | 🔗 Links to Individual DMO |
| EventDateTime__c | ssot__EngagementDateTm__c | Event timestamp |
| EventType__c | ssot__EngagementTypeId__c | Engagement type |
| PageURL__c | ssot__PageURL__c | Page URL visited |
| SessionId__c | ssot__SessionId__c | Browser session ID |
| DeviceType__c | ssot__DeviceTypeTxt__c | Device type |
| VehicleVIN__c | ssot__EngagementVehicleId__c | Vehicle VIN viewed |
| UTMSource__c | ssot__UtmSourceName__c | UTM source |
| UTMMedium__c | ssot__UtmMediumName__c | UTM medium |
| UTMCampaign__c | ssot__UtmCampaignName__c | UTM campaign |
| DataSource__c | ssot__DataSourceId__c | System — data source |
| DataSourceObject__c | ssot__DataSourceObjectId__c | System — source object |
| KQ_EngagementId__c | KQ_Id__c | System — key qualifier |
| KQ_IndividualId__c | KQ_IndividualId__c | System — key qualifier |

---

## Connection to Unified Individual DMO

All three CarMax custom streams connect to the **Unified Individual** (ssot__Individual__dlm) through established relationships. The Individual DMO is populated from 4 sources: CRM Contact, CRM Lead, CRM Prospect, and uploaded Individual data.

### DMO → Unified Individual Linkage

| DMO | Link Field | Target | Cardinality | Status | Path Type |
|-----|-----------|--------|-------------|--------|-----------|
| CarMax Test Drive | IndividualId__c → ssot__Id__c | Individual DMO | Many-to-One | ✅ Active | Direct FK |
| CarMax Test Drive | VehicleId__c → VehicleId__c | CarMax Vehicle DMO | Many-to-One | ✅ Active | Cross-DMO FK |
| CarMax Vehicle | IndividualId__c → ssot__Id__c | Individual DMO | Many-to-One | ✅ Active | Direct FK |
| Website Engagement | ssot__IndividualId__c → ssot__Id__c | Individual DMO | Many-to-One | ✅ Active | Standard FK |

### Relationship Diagram

```
                    ┌──────────────────────┐
                    │   Unified Individual  │
                    │  ssot__Individual__dlm│
                    │   (1,063 profiles)    │
                    └──────┬───┬───┬────────┘
                           │   │   │
              IndividualId │   │   │ ssot__IndividualId__c
                           │   │   │
          ┌────────────────┘   │   └────────────────┐
          ▼                    ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌──────────────────────┐
│  CarMax Vehicle  │  │ CarMax TestDrive│  │  Website Engagement  │
│ CarMax_Vehicle   │  │ CarMax_TestDrive│  │ ssot__WebsiteEngage  │
│   __dlm          │  │   __dlm         │  │   ment__dlm          │
│  (320 records)   │  │  (144 records)  │  │  (12,743 records)    │
└────────┬─────────┘  └────────┬────────┘  └──────────────────────┘
         │    ▲                │
         │    │  VehicleId     │
         │    └────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Vehicle Preference       │
│ Affinity (Calc. Insight) │
│ Vehicle_Preference_      │
│ Affinity__cio            │
└─────────────────────────┘
```

---

## Identity Resolution

Identity resolution is configured and running successfully, producing **1,063 known unified profiles** with a consolidation rate of 2 (meaning on average 2 source records merge into 1 unified profile).

### Configuration

| Property | Value |
|----------|-------|
| Ruleset | Individual Identity Resolution |
| Last Run | May 11, 2026 — SUCCESS |
| Unified Profiles | 1,063 known |
| Consolidation Rate | 2x |
| Match Rule | Fuzzy First Name + Exact Last Name + Normalized Email |
| Individual DMO Sources | Contact, Lead, Prospect, Individual (uploaded) |
| ContactPointEmail Sources | Contact, Lead, Prospect, ContactPointEmail (uploaded) |
| ContactPointPhone Sources | Contact, Lead, Account, Prospect, ContactPointPhone (uploaded) |

---

## Data Graph: CarMax Customer 360

A **CarMax Customer 360** data graph is configured with the Unified Individual as the primary object. It joins across:

**Unified Individual IND1** → CarMax Vehicle → CarMax Test Drive → Website Engagement

This provides a complete 360° view of each customer's vehicle interests, test drives, and web browsing behavior, all linked through the unified identity.

- **Primary Object:** Unified Individual IND1
- **Refresh:** Hourly (full) + Incremental enabled
- **Description:** CarMax Customer 360 Data Graph for unified customer profile with vehicles, test drives, and web engagement

---

## Calculated Insights

The CarMax org has **4 custom Calculated Insights** that derive behavioral and preference metrics from the ingested data. All are active and running successfully.

### Calculated Insight Inventory

| Calculated Insight | API Name | Status | Last Run | Schedule | Dimensions | Measures |
|--------------------|----------|--------|----------|----------|------------|----------|
| Customer Lifetime Value | Customer_Lifetime_Value__cio | ✅ ACTIVE | SUCCESS (2026-05-12) | NOT_SCHEDULED | 1 | 5 |
| Propensity to Buy | Propensity_to_Buy__cio | ✅ ACTIVE | SUCCESS (2026-05-12) | NOT_SCHEDULED | 1 | 4 |
| Vehicle Preference Affinity | Vehicle_Preference_Affinity__cio | ✅ ACTIVE | SUCCESS (2026-05-12) | NOT_SCHEDULED | 3 | 3 |
| Engagement Velocity | Engagement_Velocity__cio | ✅ ACTIVE | SUCCESS (2026-05-12) | NOT_SCHEDULED | 1 | 5 |

---

### CI 1: Customer Lifetime Value

- **API Name:** `Customer_Lifetime_Value__cio`
- **Description:** Aggregates purchase history and vehicle interaction metrics per customer for lifetime value scoring.
- **Status:** ✅ Active — Last run SUCCESS on 2026-05-12
- **Schedule:** NOT_SCHEDULED

**Dimension:** `IndividualId__c` (Unified Individual ID)

**Measures:**

| Measure | API Name | Data Type | Formula |
|---------|----------|-----------|---------|
| VehicleInteractions | VehicleInteractions__c | Number | COUNT(1) |
| TotalPurchaseValue | TotalPurchaseValue__c | Number | SUM(CASE WHEN IsPurchased = 'true' THEN Price ELSE 0 END) |
| PurchaseCount | PurchaseCount__c | Number | SUM(CASE WHEN IsPurchased = 'true' THEN 1 ELSE 0 END) |
| HeartedCount | HeartedCount__c | Number | SUM(CASE WHEN IsHearted = 'true' THEN 1 ELSE 0 END) |
| AvgVehiclePrice | AvgVehiclePrice__c | Number | AVG(Price) |

**SQL Expression:**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c,
  COUNT(1) AS VehicleInteractions__c,
  SUM(CASE WHEN CarMax_Vehicle__dlm.IsPurchased__c = 'true'
      THEN CarMax_Vehicle__dlm.Price__c ELSE 0 END) AS TotalPurchaseValue__c,
  SUM(CASE WHEN CarMax_Vehicle__dlm.IsPurchased__c = 'true'
      THEN 1 ELSE 0 END) AS PurchaseCount__c,
  SUM(CASE WHEN CarMax_Vehicle__dlm.IsHearted__c = 'true'
      THEN 1 ELSE 0 END) AS HeartedCount__c,
  AVG(CarMax_Vehicle__dlm.Price__c) AS AvgVehiclePrice__c
FROM CarMax_Vehicle__dlm
JOIN ssot__Individual__dlm
  ON CarMax_Vehicle__dlm.IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN UnifiedLinkssotIndividualInd1__dlm
  ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN UnifiedssotIndividualInd1__dlm
  ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c
```

**Join Path:** CarMax Vehicle → Individual → UnifiedLink → Unified Individual

---

### CI 2: Propensity to Buy

- **API Name:** `Propensity_to_Buy__cio`
- **Description:** Multi-factor behavioral propensity score with event-type weighting and time-decay. Higher scores indicate stronger purchase intent.
- **Status:** ✅ Active — Last run SUCCESS on 2026-05-12
- **Schedule:** NOT_SCHEDULED

**Dimension:** `IndividualId__c` (Unified Individual ID)

**Measures:**

| Measure | API Name | Data Type | Description |
|---------|----------|-----------|-------------|
| PropensityScore | PropensityScore__c | Number | Weighted sum of event types × time-decay multiplier |
| TotalEngagements | TotalEngagements__c | Number | COUNT of all web engagement records |
| UniqueEventTypes | UniqueEventTypes__c | Number | APPROX_COUNT_DISTINCT of event types |
| LastEngagementDate | LastEngagementDate__c | DateTime | MAX engagement timestamp |

**Event-Type Weights:**

| Weight | Event Types |
|--------|------------|
| 9 | Finance Application |
| 8 | Pre-Qualification Complete |
| 7 | Schedule Test Drive |
| 6 | Pre-Qualification Start |
| 5 | Vehicle Hearted, Heart Vehicle, Add to Favorites, Instant Offer Start |
| 4 | Save Search, Compare, Trade-In Estimate, Finance Calculator |
| 3 | Vehicle Detail View |
| 2 | Search, Chat Started, Review View, Share |
| 1 | All other event types |

**Time-Decay Multipliers:**

| Multiplier | Date Range |
|------------|-----------|
| 3× | On or after May 1, 2026 (most recent) |
| 2× | Apr 24 – Apr 30, 2026 |
| 1× | Apr 8 – Apr 23, 2026 |
| 0.5× | Before Apr 8, 2026 |

**SQL Expression:**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c,
  SUM(
    CASE
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Finance Application' THEN 9
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Pre-Qualification Complete' THEN 8
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Schedule Test Drive' THEN 7
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Pre-Qualification Start' THEN 6
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Vehicle Hearted' THEN 5
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Heart Vehicle' THEN 5
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Add to Favorites' THEN 5
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Instant Offer Start' THEN 5
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Save Search' THEN 4
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Compare' THEN 4
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Trade-In Estimate' THEN 4
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Finance Calculator' THEN 4
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Vehicle Detail View' THEN 3
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Search' THEN 2
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Chat Started' THEN 2
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Review View' THEN 2
      WHEN ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c = 'Share' THEN 2
      ELSE 1
    END
    *
    CASE
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000
         + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100
         + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260501 THEN 3
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000
         + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100
         + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260424 THEN 2
      WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000
         + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100
         + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260408 THEN 1
      ELSE 0.5
    END
  ) AS PropensityScore__c,
  COUNT(1) AS TotalEngagements__c,
  APPROX_COUNT_DISTINCT(ssot__WebsiteEngagement__dlm.ssot__EngagementTypeId__c) AS UniqueEventTypes__c,
  MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS LastEngagementDate__c
FROM ssot__WebsiteEngagement__dlm
JOIN ssot__Individual__dlm
  ON ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN UnifiedLinkssotIndividualInd1__dlm
  ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN UnifiedssotIndividualInd1__dlm
  ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c
```

**Join Path:** Website Engagement → Individual → UnifiedLink → Unified Individual

---

### CI 3: Vehicle Preference Affinity

- **API Name:** `Vehicle_Preference_Affinity__cio`
- **Description:** Determines preferred vehicle body type, fuel type, and average browsed price per customer by joining web engagements against the vehicle catalog.
- **Status:** ✅ Active — Last run SUCCESS on 2026-05-12
- **Schedule:** NOT_SCHEDULED

**Dimensions:**

| Dimension | API Name | Source |
|-----------|----------|--------|
| IndividualId | IndividualId__c | Unified Individual ID |
| PreferredBodyType | PreferredBodyType__c | CarMax_Vehicle__dlm.BodyType__c |
| PreferredFuelType | PreferredFuelType__c | CarMax_Vehicle__dlm.FuelType__c |

**Measures:**

| Measure | API Name | Data Type | Formula |
|---------|----------|-----------|---------|
| InteractionCount | InteractionCount__c | Number | COUNT(1) |
| AvgBrowsedPrice | AvgBrowsedPrice__c | Number | AVG(Vehicle Price) |
| LastBrowseDate | LastBrowseDate__c | DateTime | MAX(Engagement timestamp) |

**SQL Expression:**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c,
  CarMax_Vehicle__dlm.BodyType__c AS PreferredBodyType__c,
  CarMax_Vehicle__dlm.FuelType__c AS PreferredFuelType__c,
  COUNT(1) AS InteractionCount__c,
  AVG(CarMax_Vehicle__dlm.Price__c) AS AvgBrowsedPrice__c,
  MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS LastBrowseDate__c
FROM ssot__WebsiteEngagement__dlm
JOIN ssot__Individual__dlm
  ON ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN UnifiedLinkssotIndividualInd1__dlm
  ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN UnifiedssotIndividualInd1__dlm
  ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
LEFT JOIN CarMax_Vehicle__dlm
  ON ssot__WebsiteEngagement__dlm.ssot__EngagementVehicleId__c = CarMax_Vehicle__dlm.VIN__c
GROUP BY
  UnifiedssotIndividualInd1__dlm.ssot__Id__c,
  CarMax_Vehicle__dlm.BodyType__c,
  CarMax_Vehicle__dlm.FuelType__c
```

**Join Path:** Website Engagement → Individual → UnifiedLink → Unified Individual; LEFT JOIN to CarMax Vehicle via VIN

---

### CI 4: Engagement Velocity

- **API Name:** `Engagement_Velocity__cio`
- **Description:** Week-over-week engagement comparison to identify accelerating shoppers. RecentWeek vs PriorWeek event counts for velocity calculation.
- **Status:** ✅ Active — Last run SUCCESS on 2026-05-12
- **Schedule:** NOT_SCHEDULED

**Dimension:** `IndividualId__c` (Unified Individual ID)

**Measures:**

| Measure | API Name | Data Type | Description |
|---------|----------|-----------|-------------|
| RecentWeekEvents | RecentWeekEvents__c | Number | Events on or after May 1, 2026 |
| PriorWeekEvents | PriorWeekEvents__c | Number | Events from Apr 24 – Apr 30, 2026 |
| TotalEvents | TotalEvents__c | Number | COUNT of all engagements |
| UniqueSessions | UniqueSessions__c | Number | APPROX_COUNT_DISTINCT of sessions |
| MostRecentEvent | MostRecentEvent__c | DateTime | MAX engagement timestamp |

**SQL Expression:**

```sql
SELECT
  UnifiedssotIndividualInd1__dlm.ssot__Id__c AS IndividualId__c,
  SUM(CASE
    WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000
       + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100
       + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260501
    THEN 1 ELSE 0
  END) AS RecentWeekEvents__c,
  SUM(CASE
    WHEN YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000
       + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100
       + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) >= 20260424
     AND YEAR(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 10000
       + MONTH(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) * 100
       + DAY(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) < 20260501
    THEN 1 ELSE 0
  END) AS PriorWeekEvents__c,
  COUNT(1) AS TotalEvents__c,
  APPROX_COUNT_DISTINCT(ssot__WebsiteEngagement__dlm.ssot__SessionId__c) AS UniqueSessions__c,
  MAX(ssot__WebsiteEngagement__dlm.ssot__EngagementDateTm__c) AS MostRecentEvent__c
FROM ssot__WebsiteEngagement__dlm
JOIN ssot__Individual__dlm
  ON ssot__WebsiteEngagement__dlm.ssot__IndividualId__c = ssot__Individual__dlm.ssot__Id__c
JOIN UnifiedLinkssotIndividualInd1__dlm
  ON ssot__Individual__dlm.ssot__Id__c = UnifiedLinkssotIndividualInd1__dlm.SourceRecordId__c
JOIN UnifiedssotIndividualInd1__dlm
  ON UnifiedLinkssotIndividualInd1__dlm.UnifiedRecordId__c = UnifiedssotIndividualInd1__dlm.ssot__Id__c
GROUP BY UnifiedssotIndividualInd1__dlm.ssot__Id__c
```

**Join Path:** Website Engagement → Individual → UnifiedLink → Unified Individual

---

## Importing to Another SDO

The following three CSV files contain all the mock data from the CarMax custom data streams and can be used to replicate this implementation in another Sales Demo Org (SDO):

| CSV File | Records | Source Stream |
|----------|---------|---------------|
| `CarMax_TestDrive_Data.csv` | 144 | CarMax Test Drive |
| `CarMax_Vehicle_Data.csv` | 320 | CarMax Vehicle |
| `CarMax_WebEngagement_Data.csv` | 12,743 | CarMax Web Engagement |

### Prerequisites for Import

Before importing the CSV data into a new SDO, ensure the following are configured in the target org:

1. **IngestAPI Connection** — Create an Ingestion API connection (e.g., "CarMax Data Connector")
2. **Custom DMOs** — Define the two custom Data Model Objects:
   - `CarMax_TestDrive__dlm` (Engagement category) with all 15 fields listed in Stream 1 above
   - `CarMax_Vehicle__dlm` (Profile category) with all 26 fields listed in Stream 2 above
3. **Data Streams** — Create 3 data streams mapping to the DMOs:
   - CarMax Test Drive → `CarMax_TestDrive__dlm`
   - CarMax Vehicle → `CarMax_Vehicle__dlm`
   - CarMax Web Engagement → `ssot__WebsiteEngagement__dlm` (standard DMO)
4. **Field Mappings** — Map all DLO fields to DMO fields as documented in the Field Mappings tables above
5. **DMO Relationships** — Establish the foreign key relationships:
   - CarMax Test Drive → Individual (via IndividualId)
   - CarMax Test Drive → CarMax Vehicle (via VehicleId)
   - CarMax Vehicle → Individual (via IndividualId)
   - Website Engagement → Individual (via ssot__IndividualId__c)
6. **Identity Resolution** — Configure with Fuzzy First Name + Exact Last Name + Normalized Email matching

### Import Steps

1. **Obtain a CDP token** by exchanging your Salesforce access token via the `/services/a360/token` endpoint
2. **Ingest each CSV** via the Streaming Ingestion API (`/api/v1/ingest/sources/{connectorLabel}/{schemaName}`):
   - Map CSV column headers to the schema field names (without `__c` suffix)
   - Send records in JSON batches (max 200KB per request)
   - Use `OperationType: "upsert"` for all 3 streams
3. **Run Identity Resolution** after ingestion completes to produce unified profiles
4. **Create the Calculated Insights** using the SQL expressions documented above
5. **Configure the Data Graph** ("CarMax Customer 360") with Unified Individual as the primary object, joining Vehicle, Test Drive, and Web Engagement

> **Note:** The Web Engagement CSV has already been normalized — all "Add to Favorites" and "Heart Vehicle" EventType values have been corrected to "Vehicle Hearted" for consistency.

---

## Data Pipeline Health

> ✅ **Fully Operational** — All 3 CarMax custom data streams are active with successful last runs. All fields are mapped to their target DMOs, all DMOs are linked to the Unified Individual via direct foreign key relationships, and identity resolution is producing unified profiles. The CarMax Customer 360 data graph ties everything together for a complete customer view.
