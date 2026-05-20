# CarMax DMO Definitions

> **Generated:** May 13, 2026 | **Org:** Carmax MM

Complete Data Model Object (DMO) definitions for the three CarMax data streams, including all fields, data types, mapping status, and relationships.

---

## Overview

| DMO | API Name | Category | Type | Total Fields | Mapped | Active Relationships |
|-----|----------|----------|------|-------------|--------|---------------------|
| CarMax Test Drive | `CarMax_TestDrive__dlm` | ENGAGEMENT | Custom | 16 | 15 | 2 |
| CarMax Vehicle | `CarMax_Vehicle__dlm` | PROFILE | Custom | 27 | 26 | 4 |
| Website Engagement | `ssot__WebsiteEngagement__dlm` | ENGAGEMENT | Standard | 132 | 29 | 3 |

---

## 1. CarMax Test Drive

- **API Name:** `CarMax_TestDrive__dlm`
- **Category:** ENGAGEMENT
- **Creation Type:** Custom
- **Data Space:** default
- **Total Fields:** 16
- **Mapped Fields:** 15
- **Segmentable:** No
- **Editable:** Yes
- **Description:** CarMax test drive events linked to Individual and Vehicle

### Fields

| # | Field Name | Label | Data Type | Mapped | Usage Tag |
|---|------------|-------|-----------|--------|-----------|
| 1 | `CarMaxStore__c` | CarMax Store | Text | ✅ Yes | None |
| 2 | `ConvertedToPurchase__c` | Converted to Purchase | Text | ✅ Yes | None |
| 3 | `DataSourceObject__c` | Data Source Object | Text | ✅ Yes | None |
| 4 | `DataSource__c` | Data Source | Text | ✅ Yes | None |
| 5 | `EventDateTime__c` | Event DateTime | DateTime | ✅ Yes | None |
| 6 | `IndividualId__c` | Individual Id | Text | ✅ Yes | None |
| 7 | `KQ_IndividualId__c` | Key Qualifier Individual Id | Text | ✅ Yes | KeyQualifier |
| 8 | `KQ_TestDriveId__c` | Key Qualifier Test Drive Id | Text | ✅ Yes | KeyQualifier |
| 9 | `KQ_VehicleId__c` | Key Qualifier Vehicle Id | Text | ✅ Yes | KeyQualifier |
| 10 | `Notes__c` | Notes | Text | ✅ Yes | None |
| 11 | `Outcome__c` | Outcome | Text | ✅ Yes | None |
| 12 | `TestDriveDate__c` | Test Drive Date | Text | ✅ Yes | None |
| 13 | `TestDriveId__c` | Test Drive Id | Text | ✅ Yes | None |
| 14 | `VIN__c` | VIN | Text | ✅ Yes | None |
| 15 | `VehicleId__c` | Vehicle Id | Text | ✅ Yes | None |
| 16 | `InternalOrganization__c` | Internal Organization | Text | ❌ No | None |

### Relationships (2 active, 0 inactive)

**Active Relationships:**

| Relationship Name | Source Field | → | Target Object | Target Field | Cardinality | Type |
|-------------------|-------------|---|---------------|-------------|-------------|------|
| CarMax_TestDrive_IndividualId_map_Individual_Id_N_1 | `IndividualId__c` | → | `ssot__Individual__dlm` | `ssot__Id__c` | ManyToOne | Custom |
| CarMax_TestDrive_VehicleId_map_CarMax_Vehicle_VehicleId_N_1 | `VehicleId__c` | → | `CarMax_Vehicle__dlm` | `VehicleId__c` | ManyToOne | Custom |

---

## 2. CarMax Vehicle

- **API Name:** `CarMax_Vehicle__dlm`
- **Category:** PROFILE
- **Creation Type:** Custom
- **Data Space:** default
- **Total Fields:** 27
- **Mapped Fields:** 26
- **Segmentable:** Yes
- **Editable:** Yes
- **Description:** CarMax vehicle inventory linked to Individual

### Fields

| # | Field Name | Label | Data Type | Mapped | Usage Tag |
|---|------------|-------|-----------|--------|-----------|
| 1 | `BodyType__c` | Body Type | Text | ✅ Yes | None |
| 2 | `CarMaxStore__c` | CarMax Store | Text | ✅ Yes | None |
| 3 | `Color__c` | Color | Text | ✅ Yes | None |
| 4 | `DataSourceObject__c` | Data Source Object | Text | ✅ Yes | None |
| 5 | `DataSource__c` | Data Source | Text | ✅ Yes | None |
| 6 | `Doors__c` | Doors | Text | ✅ Yes | None |
| 7 | `FuelType__c` | Fuel Type | Text | ✅ Yes | None |
| 8 | `HeartedById__c` | Hearted By Id | Text | ✅ Yes | None |
| 9 | `HeartedDate__c` | Hearted Date | Text | ✅ Yes | None |
| 10 | `IndividualId__c` | Individual Id | Text | ✅ Yes | None |
| 11 | `IsHearted__c` | Is Hearted | Text | ✅ Yes | None |
| 12 | `IsPurchased__c` | Is Purchased | Text | ✅ Yes | None |
| 13 | `KQ_IndividualId__c` | Key Qualifier Individual Id | Text | ✅ Yes | KeyQualifier |
| 14 | `KQ_VehicleId__c` | Key Qualifier Vehicle Id | Text | ✅ Yes | KeyQualifier |
| 15 | `LastModified__c` | Last Modified | DateTime | ✅ Yes | None |
| 16 | `ListingURL__c` | Listing URL | Text | ✅ Yes | None |
| 17 | `Make__c` | Make | Text | ✅ Yes | None |
| 18 | `Mileage__c` | Mileage | Number | ✅ Yes | None |
| 19 | `Model__c` | Model | Text | ✅ Yes | None |
| 20 | `Price__c` | Price | Number | ✅ Yes | None |
| 21 | `PurchaseDate__c` | Purchase Date | Text | ✅ Yes | None |
| 22 | `Status__c` | Status | Text | ✅ Yes | None |
| 23 | `Transmission__c` | Transmission | Text | ✅ Yes | None |
| 24 | `VIN__c` | VIN | Text | ✅ Yes | None |
| 25 | `VehicleId__c` | Vehicle Id | Text | ✅ Yes | None |
| 26 | `Year__c` | Year | Number | ✅ Yes | None |
| 27 | `InternalOrganization__c` | Internal Organization | Text | ❌ No | None |

### Relationships (4 active, 0 inactive)

**Active Relationships:**

| Relationship Name | Source Field | → | Target Object | Target Field | Cardinality | Type |
|-------------------|-------------|---|---------------|-------------|-------------|------|
| CarMax_TestDrive_VehicleId_map_CarMax_Vehicle_VehicleId_N_1 | `VehicleId__c` | → | `CarMax_Vehicle__dlm` | `VehicleId__c` | ManyToOne | Custom |
| CarMax_Vehicle_IndividualId_map_Individual_Id_N_1 | `IndividualId__c` | → | `ssot__Individual__dlm` | `ssot__Id__c` | ManyToOne | Custom |
| Vehicle_Preference_Affinity_PreferredBodyType_map_CarMax_Veh | `PreferredBodyType__c` | → | `CarMax_Vehicle__dlm` | `BodyType__c` | ManyToOne | CalculatedInsight |
| Vehicle_Preference_Affinity_PreferredFuelType_map_CarMax_Veh | `PreferredFuelType__c` | → | `CarMax_Vehicle__dlm` | `FuelType__c` | ManyToOne | CalculatedInsight |

---

## 3. Website Engagement

- **API Name:** `ssot__WebsiteEngagement__dlm`
- **Category:** ENGAGEMENT
- **Creation Type:** Standard
- **Data Space:** default
- **Total Fields:** 132
- **Mapped Fields:** 29
- **Segmentable:** No
- **Editable:** Yes

> **Note:** This is a standard Salesforce DMO with 132 fields. The table below shows all fields, sorted by mapped status (mapped first).

### Fields

| # | Field Name | Label | Data Type | Mapped | Usage Tag |
|---|------------|-------|-----------|--------|-----------|
| 1 | `KQ_EngagementChannelTypeId__c` | Key Qualifier Engagement Channel Type | Text | ✅ Yes | KeyQualifier |
| 2 | `KQ_Id__c` | Key Qualifier Website Engagement Id | Text | ✅ Yes | KeyQualifier |
| 3 | `KQ_IndividualId__c` | Key Qualifier Individual | Text | ✅ Yes | KeyQualifier |
| 4 | `KQ_WebsitePublicationId__c` | Key Qualifier Website Publication | Text | ✅ Yes | KeyQualifier |
| 5 | `ssot__BrowserName__c` | Browser Name | Text | ✅ Yes | None |
| 6 | `ssot__DataSourceId__c` | Data Source | Text | ✅ Yes | None |
| 7 | `ssot__DataSourceObjectId__c` | Data Source Object | Text | ✅ Yes | None |
| 8 | `ssot__DeviceModelName__c` | Device Model Name | Text | ✅ Yes | None |
| 9 | `ssot__DeviceTypeTxt__c` | Device Type | Text | ✅ Yes | None |
| 10 | `ssot__EngagementChannelActionId__c` | Engagement Channel Action | Text | ✅ Yes | None |
| 11 | `ssot__EngagementChannelTypeId__c` | Engagement Channel Type | Text | ✅ Yes | None |
| 12 | `ssot__EngagementDateTm__c` | Engagement Date Time | DateTime | ✅ Yes | None |
| 13 | `ssot__EngagementTypeId__c` | Engagement Type | Text | ✅ Yes | None |
| 14 | `ssot__EngagementVehicleId__c` | Engagement Vehicle | Text | ✅ Yes | None |
| 15 | `ssot__ExternalSourceId__c` | External Source Id | Text | ✅ Yes | None |
| 16 | `ssot__Id__c` | Website Engagement Id | Text | ✅ Yes | None |
| 17 | `ssot__IndividualId__c` | Individual | Text | ✅ Yes | None |
| 18 | `ssot__InternalOrganizationId__c` | Internal Organization | Text | ✅ Yes | None |
| 19 | `ssot__LinkURL__c` | Link URL | Text | ✅ Yes | None |
| 20 | `ssot__PageName__c` | Page Name | Text | ✅ Yes | None |
| 21 | `ssot__PagePublicTitleName__c` | Page Public Title | Text | ✅ Yes | None |
| 22 | `ssot__PageURL__c` | Page URL | Text | ✅ Yes | None |
| 23 | `ssot__ReferrerURL__c` | Referrer URL | Text | ✅ Yes | None |
| 24 | `ssot__SessionId__c` | Session | Text | ✅ Yes | None |
| 25 | `ssot__UtmCampaignName__c` | UTM Campaign | Text | ✅ Yes | None |
| 26 | `ssot__UtmMediumName__c` | UTM Medium | Text | ✅ Yes | None |
| 27 | `ssot__UtmSourceName__c` | UTM Source | Text | ✅ Yes | None |
| 28 | `ssot__WebsiteCatalogObjectType__c` | Website Catalog Object Type | Text | ✅ Yes | None |
| 29 | `ssot__WebsitePublicationId__c` | Website Publication | Text | ✅ Yes | None |
| 30 | `ssot__AccountContactId__c` | Account Contact | Text | ❌ No | None |
| 31 | `ssot__ActionCadenceStepId__c` | Action Cadence Step | Text | ❌ No | None |
| 32 | `ssot__AnchorLinkId__c` | Anchor Link Id | Text | ❌ No | None |
| 33 | `ssot__AnchorLinkLabelText__c` | Anchor Link Label | Text | ❌ No | None |
| 34 | `ssot__AnchorLinkRelText__c` | Anchor Link Rel Label | Text | ❌ No | None |
| 35 | `ssot__AnchorLinkTargetText__c` | Anchor Link Target | Text | ❌ No | None |
| 36 | `ssot__AnchorReferrerPolicyText__c` | Anchor Referrer Policy | Text | ❌ No | None |
| 37 | `ssot__BrowserRenderEngineName__c` | Browser Render Engine Name | Text | ❌ No | None |
| 38 | `ssot__BrowserVendorName__c` | Browser Vendor Name | Text | ❌ No | None |
| 39 | `ssot__BrowserVersionNumber__c` | Browser Version Number | Text | ❌ No | None |
| 40 | `ssot__CaseId__c` | Case | Text | ❌ No | None |
| 41 | `ssot__ContactPointId__c` | Contact Point | Text | ❌ No | None |
| 42 | `ssot__CorrelationId__c` | Correlation Id | Text | ❌ No | None |
| 43 | `ssot__CountryId__c` | Country | Text | ❌ No | None |
| 44 | `ssot__CountryRegionId__c` | Country Region | Text | ❌ No | None |
| 45 | `ssot__CreatedDate__c` | Created Date | DateTime | ❌ No | None |
| 46 | `ssot__DeviceCountryId__c` | Device Country | Text | ❌ No | None |
| 47 | `ssot__DeviceIPAddress__c` | Device IP Address | Text | ❌ No | None |
| 48 | `ssot__DeviceLatitude__c` | Device Latitude | Number | ❌ No | None |
| 49 | `ssot__DeviceLocaleId__c` | Device Locale | Text | ❌ No | None |
| 50 | `ssot__DeviceLongitude__c` | Device Longitude | Number | ❌ No | None |
| 51 | `ssot__DeviceOSName__c` | Device OS Name | Text | ❌ No | None |
| 52 | `ssot__DevicePostalCode__c` | Device Postal Code | Text | ❌ No | None |
| 53 | `ssot__DeviceVendorName__c` | Device Vendor | Text | ❌ No | None |
| 54 | `ssot__DisplayButtonId__c` | Display Button Id | Text | ❌ No | None |
| 55 | `ssot__DisplayButtonLabelText__c` | Display Button Label | Text | ❌ No | None |
| 56 | `ssot__DisplayButtonTypeName__c` | Display Button Type Name | Text | ❌ No | None |
| 57 | `ssot__DomainName__c` | Domain Name | Text | ❌ No | None |
| 58 | `ssot__EngagementAssetId__c` | Engagement Asset | Text | ❌ No | None |
| 59 | `ssot__EngagementChannelId__c` | Engagement Channel | Text | ❌ No | None |
| 60 | `ssot__EngagementEventDirectionId__c` | Engagement Event Direction | Text | ❌ No | None |
| 61 | `ssot__EngagementNbr__c` | Engagement Number | Text | ❌ No | None |
| 62 | `ssot__EngagementNotesTxt__c` | Engagement Notes | Text | ❌ No | None |
| 63 | `ssot__EngagementPublicationId__c` | Engagement Publication | Text | ❌ No | None |
| 64 | `ssot__EngagementTimeMilliseconds__c` | Engagement Time Milliseconds | Number | ❌ No | None |
| 65 | `ssot__EngmtChannelActionStatus__c` | Engagement Channel Action Status | Text | ❌ No | None |
| 66 | `ssot__ExternalRecordId__c` | External Record Id | Text | ❌ No | None |
| 67 | `ssot__FileExtensionText__c` | File Extension | Text | ❌ No | None |
| 68 | `ssot__FileName__c` | File Name | Text | ❌ No | None |
| 69 | `ssot__FormDestinationURL__c` | Form Destination URL | Text | ❌ No | None |
| 70 | `ssot__FormId__c` | Form Id | Text | ❌ No | None |
| 71 | `ssot__FormName__c` | Form Name | Text | ❌ No | None |
| 72 | `ssot__FormSubmitText__c` | Form Submit Text | Text | ❌ No | None |
| 73 | `ssot__IPAddr__c` | IP Address | Text | ❌ No | None |
| 74 | `ssot__InternalEngagementActorId__c` | Internal Engagement Actor | Text | ❌ No | None |
| 75 | `ssot__IsOutbound__c` | Is Outbound | Boolean | ❌ No | None |
| 76 | `ssot__IsPageView__c` | Is Page View | Text | ❌ No | None |
| 77 | `ssot__IsRecognizedBrowser__c` | Is Recognized Browser | Boolean | ❌ No | None |
| 78 | `ssot__IsTestSend__c` | Is Test Send | Text | ❌ No | None |
| 79 | `ssot__ItemListId__c` | Item List Id | Text | ❌ No | None |
| 80 | `ssot__ItemListName__c` | Item List Name | Text | ❌ No | None |
| 81 | `ssot__LastModifiedDate__c` | Last Modified Date | DateTime | ❌ No | None |
| 82 | `ssot__LeadlId__c` | Lead | Text | ❌ No | None |
| 83 | `ssot__LinkClassesText__c` | Link Classes | Text | ❌ No | None |
| 84 | `ssot__LinkDomainName__c` | Link Domain | Text | ❌ No | None |
| 85 | `ssot__MarketAudienceId__c` | Market Audience | Text | ❌ No | None |
| 86 | `ssot__MarketJourneyActivityId__c` | Market Journey Activity | Text | ❌ No | None |
| 87 | `ssot__MarketSegmentId__c` | Market Segment | Text | ❌ No | None |
| 88 | `ssot__MarketingEmailListId__c` | Marketing Email List | Text | ❌ No | None |
| 89 | `ssot__Name__c` | Name | Text | ❌ No | None |
| 90 | `ssot__OSModelName__c` | OS Model Name | Text | ❌ No | None |
| 91 | `ssot__OSName__c` | OS Name | Text | ❌ No | None |
| 92 | `ssot__OSVendor__c` | OS Vendor | Text | ❌ No | None |
| 93 | `ssot__OSVersionNumber__c` | OS Version Number | Text | ❌ No | None |
| 94 | `ssot__OfferId__c` | Offer | Text | ❌ No | None |
| 95 | `ssot__OfferTreatmentId__c` | Offer Treatment | Text | ❌ No | None |
| 96 | `ssot__PageId__c` | Page Id | Text | ❌ No | None |
| 97 | `ssot__ParentWebsitePublicationId__c` | Parent Website Publication | Text | ❌ No | None |
| 98 | `ssot__PerslServiceProviderName__c` | Personalization Service Provider | Text | ❌ No | None |
| 99 | `ssot__PersonalizationContentId__c` | Personalization Content | Text | ❌ No | None |
| 100 | `ssot__PersonalizationId__c` | Personalization | Text | ❌ No | None |
| 101 | `ssot__PersonalizationRequestId__c` | Personalization Request | Text | ❌ No | None |
| 102 | `ssot__PromotionId__c` | Promotion | Text | ❌ No | None |
| 103 | `ssot__Referrer__c` | Referrer | Text | ❌ No | None |
| 104 | `ssot__SalesOrderId__c` | Sales Order | Text | ❌ No | None |
| 105 | `ssot__ScreenHeightPixelsQuantity__c` | Screen Height Pixels | Number | ❌ No | None |
| 106 | `ssot__ScreenWidthPixelsQuantity__c` | Screen Width Pixels | Number | ❌ No | None |
| 107 | `ssot__SearchResultId__c` | Search Result Id | Text | ❌ No | None |
| 108 | `ssot__SearchResultPageNumber__c` | Search Result Page Number | Number | ❌ No | None |
| 109 | `ssot__SearchResultPositionInPageNumber__c` | Search Result Position in Page | Number | ❌ No | None |
| 110 | `ssot__SearchResultPositionNumber__c` | Search Result Position | Number | ❌ No | None |
| 111 | `ssot__SearchResultTitleText__c` | Search Result Title | Text | ❌ No | None |
| 112 | `ssot__SentDateTm__c` | Sent Date Time | DateTime | ❌ No | None |
| 113 | `ssot__ShoppingCartId__c` | Shopping Cart | Text | ❌ No | None |
| 114 | `ssot__TargetEngagementActorId__c` | Target Engagement Actor | Text | ❌ No | None |
| 115 | `ssot__TaskId__c` | Task | Text | ❌ No | None |
| 116 | `ssot__TotalAmount__c` | Total Amount | Number | ❌ No | None |
| 117 | `ssot__UIComponentId__c` | UI Component Id | Text | ❌ No | None |
| 118 | `ssot__UserAgentText__c` | User Agent | Text | ❌ No | None |
| 119 | `ssot__UtmContentDescription__c` | UTM Content | Text | ❌ No | None |
| 120 | `ssot__UtmId__c` | UTM Id | Text | ❌ No | None |
| 121 | `ssot__UtmSourcePlatformName__c` | UTM Source Platform | Text | ❌ No | None |
| 122 | `ssot__UtmTermDescription__c` | UTM Term | Text | ❌ No | None |
| 123 | `ssot__VisitEndTm__c` | Website Visit End Time | DateTime | ❌ No | None |
| 124 | `ssot__VisitStartTm__c` | Website Visit Start Time | DateTime | ❌ No | None |
| 125 | `ssot__WebCookieId__c` | Web Cookie | Text | ❌ No | None |
| 126 | `ssot__WebSessionId__c` | Web Session ID | Text | ❌ No | None |
| 127 | `ssot__WebSession__c` | Web Session | Text | ❌ No | None |
| 128 | `ssot__WebpageType__c` | Webpage Type | Text | ❌ No | None |
| 129 | `ssot__WebsiteCatalogCategoryId__c` | Website Catalog Category | Text | ❌ No | None |
| 130 | `ssot__WebsiteCatalogObjectId__c` | Website Catalog Object Id | Text | ❌ No | None |
| 131 | `ssot__WebsiteId__c` | Website | Text | ❌ No | None |
| 132 | `ssot__WorkflowId__c` | Workflow | Text | ❌ No | None |

### Relationships (3 active, 45 inactive)

**Active Relationships:**

| Relationship Name | Source Field | → | Target Object | Target Field | Cardinality | Type |
|-------------------|-------------|---|---------------|-------------|-------------|------|
| EngagementChannelType_Id_map_WebsiteEngagement_EngagementCha | `ssot__EngagementChannelTypeId__c` | → | `ssot__EngagementChannelType__dlm` | `ssot__Id__c` | ManyToOne | Standard |
| Individual_Id_map_WebsiteEngagement_IndividualId_N_1_1645552 | `ssot__IndividualId__c` | → | `ssot__Individual__dlm` | `ssot__Id__c` | ManyToOne | Standard |
| WebsiteEngagement_WebsitePublicationId_map_WebsitePublicatio | `ssot__WebsitePublicationId__c` | → | `ssot__WebsitePublication__dlm` | `ssot__Id__c` | ManyToOne | Standard |

<details><summary>Show 45 inactive relationships</summary>

| Relationship Name | Source Field | Target Object | Target Field | Cardinality |
|-------------------|-------------|---------------|-------------|-------------|
| AccountContact_Id_map_WebsiteEngagement_AccountContactId_N_1 | `ssot__AccountContactId__c` | `ssot__AccountContact__dlm` | `ssot__Id__c` | ManyToOne |
| Case_Id_map_WebsiteEngagement_CaseId_N_1_1645552387279 | `ssot__CaseId__c` | `ssot__Case__dlm` | `ssot__Id__c` | ManyToOne |
| ContactPointAddress_Id_map_WebsiteEngagement_ContactPointId_ | `ssot__ContactPointId__c` | `ssot__ContactPointAddress__dlm` | `ssot__Id__c` | ManyToOne |
| ContactPointApp_Id_map_WebsiteEngagement_ContactPointId_N_1_ | `ssot__ContactPointId__c` | `ssot__ContactPointApp__dlm` | `ssot__Id__c` | ManyToOne |
| ContactPointEmail_Id_map_WebsiteEngagement_ContactPointId_N_ | `ssot__ContactPointId__c` | `ssot__ContactPointEmail__dlm` | `ssot__Id__c` | ManyToOne |
| ContactPointPhone_Id_map_WebsiteEngagement_ContactPointId_N_ | `ssot__ContactPointId__c` | `ssot__ContactPointPhone__dlm` | `ssot__Id__c` | ManyToOne |
| ContactPointSocial_Id_map_WebsiteEngagement_ContactPointId_N | `ssot__ContactPointId__c` | `ssot__ContactPointSocial__dlm` | `ssot__Id__c` | ManyToOne |
| DeviceApplicationTemplate_Id_map_WebsiteEngagement_Engagemen | `ssot__EngagementAssetId__c` | `ssot__DeviceApplicationTemplate__dlm` | `ssot__Id__c` | ManyToOne |
| EmailPublication_Id_map_WebsiteEngagement_EngagementPublicat | `ssot__EngagementPublicationId__c` | `ssot__EmailPublication__dlm` | `ssot__Id__c` | ManyToOne |
| EmailTemplate_Id_map_WebsiteEngagement_EngagementAssetId_N_1 | `ssot__EngagementAssetId__c` | `ssot__EmailTemplate__dlm` | `ssot__Id__c` | ManyToOne |
| EngagementTopic_EngagementId_map_WebsiteEngagement_Id_N_1_16 | `ssot__EngagementId__c` | `ssot__WebsiteEngagement__dlm` | `ssot__Id__c` | ManyToOne |
| Lead_Id_map_WebsiteEngagement_LeadlId_N_1_1645552387797 | `ssot__LeadlId__c` | `ssot__Lead__dlm` | `ssot__Id__c` | ManyToOne |
| LoyaltyTransactionJournal_EngagementId_map_WebsiteEngagement | `ssot__EngagementId__c` | `ssot__WebsiteEngagement__dlm` | `ssot__Id__c` | ManyToOne |
| MarketJourneyActivity_Id_map_WebsiteEngagement_MarketJourney | `ssot__MarketJourneyActivityId__c` | `ssot__MarketJourneyActivity__dlm` | `ssot__Id__c` | ManyToOne |
| MarketSegment_Id_map_WebsiteEngagement_MarketSegmentId_N_1_1 | `ssot__MarketSegmentId__c` | `ssot__MarketSegment__dlm` | `ssot__Id__c` | ManyToOne |
| SalesOrder_Id_map_WebsiteEngagement_SalesOrderId_N_1_1645552 | `ssot__SalesOrderId__c` | `ssot__SalesOrder__dlm` | `ssot__Id__c` | ManyToOne |
| SMSPublication_Id_map_WebsiteEngagement_EngagementPublicatio | `ssot__EngagementPublicationId__c` | `ssot__SMSPublication__dlm` | `ssot__Id__c` | ManyToOne |
| SMSTemplate_Id_map_WebsiteEngagement_EngagementAssetId_N_1_1 | `ssot__EngagementAssetId__c` | `ssot__SMSTemplate__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_AccountContactId_map_AccountContact_Id_N_1 | `ssot__AccountContactId__c` | `ssot__AccountContact__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_CaseId_map_Case_Id_N_1_1645552389379 | `ssot__CaseId__c` | `ssot__Case__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_ContactPointId_map_ContactPointAddress_Id_ | `ssot__ContactPointId__c` | `ssot__ContactPointAddress__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_ContactPointId_map_ContactPointApp_Id_N_1_ | `ssot__ContactPointId__c` | `ssot__ContactPointApp__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_ContactPointId_map_ContactPointEmail_Id_N_ | `ssot__ContactPointId__c` | `ssot__ContactPointEmail__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_ContactPointId_map_ContactPointPhone_Id_N_ | `ssot__ContactPointId__c` | `ssot__ContactPointPhone__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_ContactPointId_map_ContactPointSocial_Id_N | `ssot__ContactPointId__c` | `ssot__ContactPointSocial__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_EngagementAssetId_map_DeviceApplicationTem | `ssot__EngagementAssetId__c` | `ssot__DeviceApplicationTemplate__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_EngagementAssetId_map_EmailTemplate_Id_N_1 | `ssot__EngagementAssetId__c` | `ssot__EmailTemplate__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_EngagementAssetId_map_SMSTemplate_Id_N_1_1 | `ssot__EngagementAssetId__c` | `ssot__SMSTemplate__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_EngagementChannelTypeId_map_EngagementChan | `ssot__EngagementChannelTypeId__c` | `ssot__EngagementChannelType__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_EngagementPublicationId_map_EmailPublicati | `ssot__EngagementPublicationId__c` | `ssot__EmailPublication__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_EngagementPublicationId_map_SMSPublication | `ssot__EngagementPublicationId__c` | `ssot__SMSPublication__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_Id_map_EngagementTopic_EngagementId_N_1_16 | `ssot__EngagementId__c` | `ssot__WebsiteEngagement__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_Id_map_LoyaltyTransactionJournal_Engagemen | `ssot__EngagementId__c` | `ssot__WebsiteEngagement__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_IndividualId_map_Individual_Id_N_1_1645552 | `ssot__IndividualId__c` | `ssot__Individual__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_LeadlId_map_Lead_Id_N_1_1645552389233 | `ssot__LeadlId__c` | `ssot__Lead__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_MarketJourneyActivityId_map_MarketJourneyA | `ssot__MarketJourneyActivityId__c` | `ssot__MarketJourneyActivity__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_MarketSegmentId_map_MarketSegment_Id_N_1_1 | `ssot__MarketSegmentId__c` | `ssot__MarketSegment__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_OfferId_map_Offer_Id_N_1 | `ssot__OfferId__c` | `ssot__Offer__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_OfferTreatmentId_map_OfferTreatment_Id_N_1 | `ssot__OfferTreatmentId__c` | `ssot__OfferTreatment__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_ParentWebsitePublicationId_map_WebsitePubl | `ssot__ParentWebsitePublicationId__c` | `ssot__WebsitePublication__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_PersonalizationContentId_map_Personalizati | `ssot__PersonalizationContentId__c` | `ssot__PersonalizationLog__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_PromotionId_map_Promotion_Id_N_1 | `ssot__PromotionId__c` | `ssot__Promotion__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_SalesOrderId_map_SalesOrder_Id_N_1_1645552 | `ssot__SalesOrderId__c` | `ssot__SalesOrder__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteEngagement_UtmId_map_Campaign_Id_N_1 | `ssot__UtmId__c` | `ssot__Campaign__dlm` | `ssot__Id__c` | ManyToOne |
| WebsiteItemEngagement_WebsiteEngagementId_map_WebsiteEngagem | `ssot__WebsiteEngagementId__c` | `ssot__WebsiteEngagement__dlm` | `ssot__Id__c` | ManyToOne |

</details>

---
