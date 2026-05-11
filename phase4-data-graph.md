# Phase 4: Data Graph — Implementation Plan

## Overview
Create the "CarMax Customer 360" Data Graph connecting Unified Individual to the 3 DMOs (Vehicle, Test Drive, Web Engagement). This graph powers the dynamic loop/repeater email at Demo Stop 3, where vehicle cards are pulled from the graph to render personalized "Compare What Matters" content.

**Org:** `carmax-sdo-mm-app-wz95pw`
**Prerequisite:** Phase 2 complete (DMOs verified with FK relationships) + Phase 3 (CIs materialized)

---

## Architecture

```
Individual (ssot__Individual__dlm)
├── CarMax Vehicle (CarMax_Vehicle__dlm)
│     └── linked via IndividualId__c → Individual.ssot__Id__c
├── CarMax TestDrive (CarMax_TestDrive__dlm)
│     └── linked via IndividualId__c → Individual.ssot__Id__c
└── Website Engagement (ssot__WebsiteEngagement__dlm)
      └── linked via ssot__IndividualId__c → Individual.ssot__Id__c
```

**Graph Type:** `NONE` (Standard/Warm — suitable for batch email personalization)

**Note on REALTIME vs NONE:** We use `NONE` (standard) because the demo emails are batch-triggered from MCA Flow. Real-time graphs are for sub-second API lookups (e.g., web personalization). The dynamic loop email pulls data at send time from the warm graph, which is sufficient.

> **DMO Name & Field Reference:**
> - **CarMax_Vehicle__dlm** — CamelCase fields: `VehicleId__c`, `VIN__c`, `Make__c`, `Model__c`, `Year__c`, `Color__c`, `BodyType__c`, `Price__c`, `FuelType__c`, `Mileage__c`, `Status__c`, `CarMaxStore__c`, `IsHearted__c`, `IsPurchased__c`, `ListingURL__c`
> - **CarMax_TestDrive__dlm** — CamelCase fields: `TestDriveId__c`, `VIN__c`, `TestDriveDate__c`, `CarMaxStore__c`, `Outcome__c`, `ConvertedToPurchase__c`
> - **ssot__WebsiteEngagement__dlm** — Standard ssot__ fields: `ssot__Id__c`, `ssot__EngagementChannelActionId__c`, `ssot__EngagementVehicleId__c`, `ssot__EngagementDateTm__c`, `ssot__PageURL__c`, `ssot__DeviceTypeTxt__c`, `ssot__UtmSourceName__c`, `ssot__UtmCampaignName__c`

---

## Step 1: Create DataGraphDefinition via Tooling API

This creates the DataGraph SObject record shell:

```bash
sf api request rest "/services/data/v65.0/tooling/sobjects/DataGraphDefinition" \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{
    "DeveloperName": "CarMax_Customer_360",
    "MasterLabel": "CarMax Customer 360",
    "Language": "en_US"
  }'
```

**Expected Response:**
```json
{"id": "0dAXXXXXXXXXXXXXXX", "success": true, "errors": []}
```

### Verify

```bash
sf data query --query "SELECT Id, Name, Status, DataGraphType FROM DataGraph WHERE Name='CarMax Customer 360'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Note:** The DataGraph SObject record may not appear until BOTH the DataGraphDefinition AND DataKitObjectTemplate are deployed. If the query returns 0 records after Step 1, proceed to Step 2 — it will appear after deployment.

---

## Step 2: Deploy DataKitObjectTemplate via Metadata

### 2A. Create Project Structure

```bash
mkdir -p /tmp/carmax-datagraph/force-app/main/default/dataKitObjectTemplates
```

### 2B. Create sfdx-project.json

```json
{
  "packageDirectories": [{ "path": "force-app", "default": true }],
  "name": "carmax-datagraph",
  "namespace": "",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "65.0"
}
```

Write to `/tmp/carmax-datagraph/sfdx-project.json`.

### 2C. Create DataKitObjectTemplate XML

**File:** `/tmp/carmax-datagraph/force-app/main/default/dataKitObjectTemplates/CarMax_Customer_360.dataKitObjectTemplate-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DataKitObjectTemplate xmlns="http://soap.sforce.com/2006/04/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <developerName xsi:nil="true"/>
    <entityPayload>ENTITY_PAYLOAD_JSON_HERE</entityPayload>
    <masterLabel>CarMax_Customer_360</masterLabel>
    <parentDataPackageKitDefinitionName xsi:nil="true"/>
    <sourceObject>CarMax_Customer_360</sourceObject>
    <sourceObjectType>DataGraph</sourceObjectType>
    <templateVersion>1</templateVersion>
</DataKitObjectTemplate>
```

### 2D. Entity Payload JSON

The `entityPayload` XML element contains a JSON string. Here is the full JSON (to be inserted as a single line in the XML):

```json
{
  "type": "NONE",
  "dataspaceName": "default",
  "primaryObjectName": "ssot__Individual__dlm",
  "primaryObjectLabel": "Individual",
  "label": "CarMax Customer 360",
  "name": "CarMax_Customer_360",
  "sourceObject": {
    "name": "ssot__Individual__dlm",
    "type": "Standard",
    "label": "Individual",
    "fields": [
      {
        "devName": "CX360_Individual_Id",
        "sourceFieldName": "ssot__Id__c",
        "isKeyColumn": true,
        "usageTag": "NONE",
        "dataType": "Text"
      },
      {
        "devName": "CX360_First_Name",
        "sourceFieldName": "ssot__FirstName__c",
        "isKeyColumn": false,
        "usageTag": "NONE",
        "dataType": "Text"
      },
      {
        "devName": "CX360_Last_Name",
        "sourceFieldName": "ssot__LastName__c",
        "isKeyColumn": false,
        "usageTag": "NONE",
        "dataType": "Text"
      },
      {
        "devName": "CX360_PersonName",
        "sourceFieldName": "ssot__PersonName__c",
        "isKeyColumn": false,
        "usageTag": "NONE",
        "dataType": "Text"
      }
    ],
    "relatedObjects": [
      {
        "name": "CarMax_Vehicle__dlm",
        "type": "Custom",
        "label": "CarMax Vehicle",
        "relationshipName": "CarMax_Vehicle__dlm_ssot__Individual__dlm",
        "fields": [
          {
            "devName": "CX360_Vehicle_Id",
            "sourceFieldName": "VehicleId__c",
            "isKeyColumn": true,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_VIN",
            "sourceFieldName": "VIN__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_Make",
            "sourceFieldName": "Make__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_Model",
            "sourceFieldName": "Model__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_Year",
            "sourceFieldName": "Year__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Number"
          },
          {
            "devName": "CX360_Vehicle_Color",
            "sourceFieldName": "Color__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_BodyType",
            "sourceFieldName": "BodyType__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_Price",
            "sourceFieldName": "Price__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Number"
          },
          {
            "devName": "CX360_Vehicle_FuelType",
            "sourceFieldName": "FuelType__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_Mileage",
            "sourceFieldName": "Mileage__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Number"
          },
          {
            "devName": "CX360_Vehicle_Status",
            "sourceFieldName": "Status__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_Store",
            "sourceFieldName": "CarMaxStore__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_IsHearted",
            "sourceFieldName": "IsHearted__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_IsPurchased",
            "sourceFieldName": "IsPurchased__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_Vehicle_ListingURL",
            "sourceFieldName": "ListingURL__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          }
        ],
        "relatedObjects": []
      },
      {
        "name": "CarMax_TestDrive__dlm",
        "type": "Custom",
        "label": "CarMax TestDrive",
        "relationshipName": "CarMax_TestDrive__dlm_ssot__Individual__dlm",
        "fields": [
          {
            "devName": "CX360_TestDrive_Id",
            "sourceFieldName": "TestDriveId__c",
            "isKeyColumn": true,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_TestDrive_VIN",
            "sourceFieldName": "VIN__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_TestDrive_Date",
            "sourceFieldName": "TestDriveDate__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_TestDrive_Store",
            "sourceFieldName": "CarMaxStore__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_TestDrive_Outcome",
            "sourceFieldName": "Outcome__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_TestDrive_Converted",
            "sourceFieldName": "ConvertedToPurchase__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          }
        ],
        "relatedObjects": []
      },
      {
        "name": "ssot__WebsiteEngagement__dlm",
        "type": "Standard",
        "label": "Website Engagement",
        "relationshipName": "ssot__WebsiteEngagement__dlm_ssot__Individual__dlm",
        "fields": [
          {
            "devName": "CX360_WebEng_Id",
            "sourceFieldName": "ssot__Id__c",
            "isKeyColumn": true,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_WebEng_EventType",
            "sourceFieldName": "ssot__EngagementChannelActionId__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_WebEng_VehicleVIN",
            "sourceFieldName": "ssot__EngagementVehicleId__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_WebEng_DateTime",
            "sourceFieldName": "ssot__EngagementDateTm__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "DateTime"
          },
          {
            "devName": "CX360_WebEng_PageURL",
            "sourceFieldName": "ssot__PageURL__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_WebEng_Device",
            "sourceFieldName": "ssot__DeviceTypeTxt__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_WebEng_UTMSource",
            "sourceFieldName": "ssot__UtmSourceName__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          },
          {
            "devName": "CX360_WebEng_UTMCampaign",
            "sourceFieldName": "ssot__UtmCampaignName__c",
            "isKeyColumn": false,
            "usageTag": "NONE",
            "dataType": "Text"
          }
        ],
        "relatedObjects": []
      }
    ]
  },
  "status": "Ready"
}
```

> **Key changes from earlier drafts:**
> - Vehicle fields use CamelCase: `BodyType__c` (not `Body_Type__c`), `FuelType__c` (not `Fuel_Type__c`), `IsHearted__c` (not `Is_Hearted__c`), `IsPurchased__c` (not `Is_Purchased__c`), `ListingURL__c` (not `Listing_URL__c`), `CarMaxStore__c` (not `CarMax_Store__c`)
> - `IsHearted__c` and `IsPurchased__c` are `dataType: "Text"` (not Boolean) — they store `'true'`/`'false'` strings
> - TestDrive DMO is `CarMax_TestDrive__dlm` (no underscore between Test and Drive)
> - TestDrive fields use CamelCase: `TestDriveDate__c` (not `Test_Drive_Date__c`), `ConvertedToPurchase__c` (not `Converted_to_Purchase__c`), `CarMaxStore__c` (not `CarMax_Store__c`)
> - `ConvertedToPurchase__c` is `dataType: "Text"` (not Boolean)
> - Web Engagement uses the **standard** `ssot__WebsiteEngagement__dlm` DMO (type: `"Standard"`, NOT `"Custom"`) with `ssot__` prefixed field names
> - The `relationshipName` for WebEng is `ssot__WebsiteEngagement__dlm_ssot__Individual__dlm` (matching the actual FK relationship)

### 2E. Generate the Final XML File

The entityPayload JSON must be escaped and placed on a single line within the `<entityPayload>` XML element. Use a Python script to generate the final XML:

```python
# generate_datagraph_xml.py
import json

entity_payload = {
    # ... (full JSON from 2D above)
}

# Escape for XML: & → &amp;, < → &lt;, > → &gt;, ' → &apos;, " → &quot;
payload_str = json.dumps(entity_payload, separators=(',', ':'))
xml_escaped = (payload_str
    .replace('&', '&amp;')
    .replace('<', '&lt;')
    .replace('>', '&gt;')
    .replace('"', '&quot;')
    .replace("'", '&apos;'))

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<DataKitObjectTemplate xmlns="http://soap.sforce.com/2006/04/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <developerName xsi:nil="true"/>
    <entityPayload>{xml_escaped}</entityPayload>
    <masterLabel>CarMax_Customer_360</masterLabel>
    <parentDataPackageKitDefinitionName xsi:nil="true"/>
    <sourceObject>CarMax_Customer_360</sourceObject>
    <sourceObjectType>DataGraph</sourceObjectType>
    <templateVersion>1</templateVersion>
</DataKitObjectTemplate>'''

with open('/tmp/carmax-datagraph/force-app/main/default/dataKitObjectTemplates/CarMax_Customer_360.dataKitObjectTemplate-meta.xml', 'w') as f:
    f.write(xml)

print("XML generated successfully")
```

### 2F. Deploy

```bash
cd /tmp/carmax-datagraph
sf project deploy start --source-dir force-app --target-org carmax-sdo-mm-app-wz95pw --wait 10
```

**Expected:** `Status: Succeeded`

---

## Step 3: Verify Graph Deployment

### 3A. Check DataGraph SObject

```bash
sf data query --query "SELECT Id, Name, Status, DataGraphType FROM DataGraph WHERE Name LIKE '%CarMax%'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

**Expected:**
```
Name: CarMax Customer 360
Status: READY
DataGraphType: NONE
```

### 3B. Check DataKitObjectTemplate

```bash
sf api request rest "/services/data/v65.0/tooling/query?q=SELECT+Id,DeveloperName,MasterLabel,SourceObjectType+FROM+DataKitObjectTemplate+WHERE+MasterLabel='CarMax_Customer_360'" \
  --target-org carmax-sdo-mm-app-wz95pw
```

### 3C. Check EntityPayload Content

```bash
sf api request rest "/services/data/v65.0/tooling/query?q=SELECT+Id,EntityPayload+FROM+DataKitObjectTemplate+WHERE+MasterLabel='CarMax_Customer_360'" \
  --target-org carmax-sdo-mm-app-wz95pw 2>&1 | grep -v "^Warning:" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('records', []):
    payload = json.loads(r['EntityPayload'])
    print(f'Graph: {payload[\"name\"]}')
    print(f'Root: {payload[\"primaryObjectName\"]}')
    print(f'Type: {payload[\"type\"]}')
    src = payload['sourceObject']
    print(f'Root fields: {len(src[\"fields\"])}')
    for ro in src.get('relatedObjects', []):
        print(f'  Related: {ro[\"name\"]} ({len(ro[\"fields\"])} fields)')
"
```

**Expected output:**
```
Graph: CarMax_Customer_360
Root: ssot__Individual__dlm
Type: NONE
Root fields: 4
  Related: CarMax_Vehicle__dlm (15 fields)
  Related: CarMax_TestDrive__dlm (6 fields)
  Related: ssot__WebsiteEngagement__dlm (8 fields)
```

---

## Step 4: Build/Activate Graph via Salesforce UI

**IMPORTANT:** Metadata-deployed graphs create the definition but are NOT fully operational in the SSOT layer until built via the UI. The REST API refresh endpoint returns "Unable to refresh now" for newly deployed graphs.

### Browser Navigation Path:
1. Setup → Data Cloud → Data Graphs
2. Find "CarMax Customer 360" in the list
3. Click into the graph
4. Click "Save and Build" (or "Build" if already saved)
5. Wait for build to complete (typically 2-5 minutes)
6. Status should change from READY to BUILT

### Verify Build via SSOT

After UI build, the graph should be accessible via the SSOT layer:

```bash
# Try refresh (should work after build)
sf api request rest "/services/data/v65.0/ssot/data-graphs/CarMax Customer 360/actions/refresh" \
  --method POST \
  --target-org carmax-sdo-mm-app-wz95pw \
  --body '{}'
```

**Note:** The refresh endpoint URL uses the MasterLabel (display name) with spaces, NOT the DeveloperName.

---

## Graph → Demo Stop Mapping

| Graph Component | Demo Stop | Purpose |
|----------------|-----------|---------|
| Individual (root) | Stop 3 | Customer name/greeting in emails |
| Vehicle (related) | Stop 3 | Dynamic loop: vehicle cards in "Compare What Matters" email |
| Test Drive (related) | Stop 3 + Stop 4 | Test drive history for follow-up email decisions |
| Web Engagement (related) | Stop 3 | Browsing context for personalized recommendations |

### Dynamic Loop Email Usage

At Demo Stop 3, the "Hearted Vehicle Follow-Up" email uses a dynamic loop (repeater) that:
1. Queries the CarMax Customer 360 graph for Jane Dawson's record
2. Iterates over her `CarMax_Vehicle` related objects where `IsHearted = 'true'`
3. Renders a vehicle card for each hearted vehicle showing: Make, Model, Year, Price, Image, "View Details" CTA

The Handlebars JS template references graph field devNames:
- `{{CX360_Vehicle_Make}}`, `{{CX360_Vehicle_Model}}`, `{{CX360_Vehicle_Year}}`
- `{{CX360_Vehicle_Price}}`, `{{CX360_Vehicle_Color}}`
- `{{CX360_Vehicle_ListingURL}}` for the CTA link

---

## Critical Notes & Gotchas

1. **REST API for data graphs returns INTERNAL_ERROR** — `POST /ssot/data-graphs` does not work. Always use the two-step metadata approach (DataGraphDefinition + DataKitObjectTemplate).

2. **Two components required** — The DataGraph SObject record only appears after BOTH the DataGraphDefinition (Tooling API) and DataKitObjectTemplate (metadata deploy) exist.

3. **Graph must be built via UI** — After metadata deployment, the graph exists as a definition only. You must click "Save and Build" in the Data Cloud UI for it to become operational. The refresh endpoint returns "Unable to refresh now" until this is done.

4. **`sourceObject.type` values** — `"Standard"` for ssot__ DMOs (Individual, WebsiteEngagement), `"Custom"` for custom DMOs (Vehicle, TestDrive). Capitalize the first letter.

5. **`devName` must be unique within the graph** — Convention: `{GraphPrefix}_{ObjectName}_{FieldLabel}`. We use `CX360_` prefix throughout.

6. **Exactly one `isKeyColumn: true` per object** — Each object in the graph needs exactly one key column designated.

7. **`relationshipName` convention** — `{ChildDMO}_{ParentDMO}` (e.g., `CarMax_Vehicle__dlm_ssot__Individual__dlm`). This must match an existing FK relationship between the DMOs.

8. **DMO FK relationships must exist first** — The graph references relationships between DMOs. Phase 2 must be complete (IndividualId FK → Individual established on Vehicle and TestDrive DMOs, ssot__IndividualId__c FK on WebsiteEngagement DMO).

9. **entityPayload must be XML-escaped** — The JSON string in the XML file must escape `"` → `&quot;`, `<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`. Use the Python script to generate the file reliably.

10. **SSOT refresh uses MasterLabel, not DeveloperName** — The URL path for refresh is the display name with spaces: `/ssot/data-graphs/CarMax Customer 360/actions/refresh`.

11. **`dataspaceName` uses lowercase 's'** — It's `dataspaceName`, not `dataSpaceName`. This is different from the DMO creation API which uses `dataSpaceName`.

12. **IsHearted__c and IsPurchased__c are Text fields** — In both the DMO and the Data Graph, these store `'true'`/`'false'` as strings, NOT booleans. The `dataType` in the graph entityPayload must be `"Text"`, not `"Boolean"`. Any filter logic (e.g., in the dynamic loop email) must compare against the string `'true'`.

13. **WebsiteEngagement is a Standard DMO** — The web engagement data flows into `ssot__WebsiteEngagement__dlm`, which is a standard (ssot__) DMO. In the graph's entityPayload, its `type` must be `"Standard"`, not `"Custom"`. Its field names all use the `ssot__` prefix.
