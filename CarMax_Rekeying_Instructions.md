# CarMax Data Cloud — Re-Keying Instructions for New SDO Import

> **Generated:** May 13, 2026 | **Source Org:** Carmax MM

---

## The Problem

The exported CarMax data CSVs contain **Contact IDs from the source org** as the `IndividualId` field. When you import Contacts into a new SDO, they'll get **different Contact IDs**. All data records (Vehicles, Test Drives, Web Engagements) need to be updated with the new IDs before ingestion into Data Cloud.

---

## How It Works

Every data CSV now includes a **`ContactEmail`** column right next to `IndividualId`. Since each of the 60 demo contacts has a unique email address, you can use email as the stable lookup key to swap old Contact IDs for new ones.

---

## Export File Inventory

| File | Records | Size | Description |
|------|---------|------|-------------|
| `CarMax_Contacts.csv` | 60 | 4.5 KB | The 60 demo Contact records — **import these first** |
| `CarMax_Vehicle_Data.csv` | 320 | 92 KB | Vehicle inventory + customer associations |
| `CarMax_TestDrive_Data.csv` | 144 | 31 KB | Test drive events |
| `CarMax_WebEngagement_Data.csv` | 12,743 | 2.5 MB | Web engagement events |

---

## Step-by-Step Re-Keying Process

### Step 1: Import Contacts to the New SDO

Import `CarMax_Contacts.csv` into the new SDO as Contact records. The CSV contains:

| Column | Example |
|--------|---------|
| FirstName | Brandon |
| LastName | Adams |
| Email | brandon.adams73@yahoo.com |
| Phone | (555) 234-5678 |
| MailingCity | Charlotte |
| MailingState | NC |
| MailingPostalCode | 28202 |

Use Data Loader, Data Import Wizard, or any preferred method to create these 60 Contacts.

### Step 2: Export the New Contact IDs

After import, query the new SDO to get a mapping of Email → new Contact ID:

```
SELECT Id, Email FROM Contact WHERE Email != null
```

Export this as a CSV or keep it as a lookup table. You'll have 60 rows like:

| Email | New Contact ID |
|-------|---------------|
| brandon.adams73@yahoo.com | 003xx00001ABCDEF |
| megan.adams36@gmail.com | 003xx00001GHIJKL |
| ... | ... |

### Step 3: Re-Key Each Data CSV

For each of the 3 data CSVs, replace the old `IndividualId` with the new Contact ID using `ContactEmail` as the matching key.

#### Vehicle CSV (`CarMax_Vehicle_Data.csv`)

- **320 total rows**
- **150 rows** have an `IndividualId` and `ContactEmail` — replace `IndividualId` with the new Contact ID matching that email
- **170 rows** have a blank `IndividualId` and blank `ContactEmail` — these are **inventory-only vehicles** with no owner. Leave `IndividualId` blank.

#### TestDrive CSV (`CarMax_TestDrive_Data.csv`)

- **144 total rows**
- **All 144 rows** have an `IndividualId` and `ContactEmail` — replace every `IndividualId` with the new Contact ID matching that email

#### WebEngagement CSV (`CarMax_WebEngagement_Data.csv`)

- **12,743 total rows**
- **12,314 rows** have a valid `ContactEmail` (e.g., `brandon.adams73@yahoo.com`) — replace `IndividualId` with the new Contact ID matching that email
- **429 rows** have `ContactEmail` = `SDO_ORIGINAL:stewart.anderson` or `SDO_ORIGINAL:unknown.customer` — these belong to the SDO's built-in default contacts (who have no email). You have two options:
  - **Option A:** Drop these 429 rows (they're from the original SDO, not the CarMax demo)
  - **Option B:** Re-map them to equivalent default contacts in the new SDO if they exist

### Step 4: Remove the ContactEmail Column

Before ingesting into Data Cloud, **remove the `ContactEmail` column** from all 3 data CSVs. It was only included as a lookup aid — it's not part of the DMO schema and should not be ingested.

### Step 5: Ingest via Data Cloud Streaming API

Once re-keyed, follow the standard ingestion process:

1. Create an IngestAPI connection in the new SDO
2. Define the schemas (matching the DMO field structures)
3. Create the 3 data streams
4. Exchange your Salesforce token for a CDP token
5. Ingest each CSV via the Streaming Ingestion API using `OperationType: "upsert"`

---

## Re-Keying Script Example (Python)

Here's a ready-to-use Python script that automates the re-keying:

```python
import csv

# Step 1: Build the email-to-new-ID mapping
# (Export from new SDO: SELECT Id, Email FROM Contact)
new_id_map = {}
with open('new_sdo_contacts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_id_map[row['Email'].lower()] = row['Id']

# Step 2: Re-key a data CSV
def rekey_csv(input_file, output_file, drop_sdo_original=True):
    with open(input_file, 'r') as fin:
        reader = csv.DictReader(fin)
        fieldnames = [f for f in reader.fieldnames if f != 'ContactEmail']

        with open(output_file, 'w', newline='') as fout:
            writer = csv.DictWriter(fout, fieldnames=fieldnames)
            writer.writeheader()

            skipped = 0
            updated = 0
            unchanged = 0

            for row in reader:
                email = row.pop('ContactEmail', '')

                if email.startswith('SDO_ORIGINAL'):
                    if drop_sdo_original:
                        skipped += 1
                        continue
                elif email:
                    new_id = new_id_map.get(email.lower())
                    if new_id:
                        row['IndividualId'] = new_id
                        updated += 1
                    else:
                        print(f"WARNING: No match for {email}")
                        unchanged += 1
                else:
                    unchanged += 1  # Blank IndividualId (inventory-only)

                writer.writerow(row)

            print(f"{input_file}: {updated} re-keyed, {unchanged} unchanged, {skipped} dropped")

# Step 3: Run on all 3 files
rekey_csv('CarMax_Vehicle_Data.csv', 'CarMax_Vehicle_Data_REKEYED.csv')
rekey_csv('CarMax_TestDrive_Data.csv', 'CarMax_TestDrive_Data_REKEYED.csv')
rekey_csv('CarMax_WebEngagement_Data.csv', 'CarMax_WebEngagement_Data_REKEYED.csv')
```

### How to Use the Script

1. Import `CarMax_Contacts.csv` into the new SDO
2. Export the new Contact IDs as `new_sdo_contacts.csv` with columns: `Id`, `Email`
3. Place all CSV files in the same directory
4. Run the script — it creates 3 `_REKEYED` output files
5. Ingest the `_REKEYED` files into Data Cloud

---

## Data Linkage Summary

```
                    ┌──────────────────────────┐
                    │     60 Demo Contacts      │
                    │   (CarMax_Contacts.csv)   │
                    │   Lookup Key: Email       │
                    └──────┬───┬───┬────────────┘
                           │   │   │
              IndividualId │   │   │ IndividualId
              (Contact ID) │   │   │ (Contact ID)
                           │   │   │
          ┌────────────────┘   │   └────────────────┐
          ▼                    ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌──────────────────────┐
│  Vehicle Data    │  │  TestDrive Data │  │  WebEngagement Data  │
│  320 records     │  │  144 records    │  │  12,743 records      │
│  150 linked      │  │  144 linked     │  │  12,314 linked       │
│  170 inventory   │  │                 │  │  429 SDO original    │
└─────────────────┘  └─────────────────┘  └──────────────────────┘
```

---

## Quick Reference: ContactEmail Values

| ContactEmail Value | Meaning | Action |
|-------------------|---------|--------|
| `brandon.adams73@yahoo.com` | Demo contact email | Replace IndividualId with new Contact ID matching this email |
| *(blank)* | No linked contact (inventory vehicle) | Leave IndividualId blank |
| `SDO_ORIGINAL:stewart.anderson` | SDO built-in contact (no email) | Drop row or re-map manually |
| `SDO_ORIGINAL:unknown.customer` | SDO built-in contact (no email) | Drop row or re-map manually |
