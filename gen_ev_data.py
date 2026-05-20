import csv, random
from datetime import datetime, timedelta
from collections import Counter

contact_ids = [
    "003ak00001MvUAfAAN","003ak00001MvUAgAAN","003ak00001MvUAhAAN","003ak00001MvUAiAAN","003ak00001MvUAjAAN",
    "003ak00001MvUAkAAN","003ak00001MvUAlAAN","003ak00001MvUAmAAN","003ak00001MvUAnAAN","003ak00001MvUAoAAN",
    "003ak00001MvUApAAN","003ak00001MvUAqAAN","003ak00001MvUArAAN","003ak00001MvUAsAAN","003ak00001MvUAtAAN",
    "003ak00001MvUAuAAN","003ak00001MvUAvAAN","003ak00001MvUAwAAN","003ak00001MvUAxAAN","003ak00001MvUAyAAN",
    "003ak00001MvUAzAAN","003ak00001MvUB0AAN","003ak00001MvUB1AAN","003ak00001MvUB2AAN","003ak00001MvUB3AAN",
    "003ak00001MvUB4AAN","003ak00001MvUB5AAN","003ak00001MvUB6AAN","003ak00001MvUB7AAN","003ak00001MvUB8AAN",
    "003ak00001MvUB9AAN","003ak00001MvUBAAA3","003ak00001MvUBBAA3","003ak00001MvUBCAA3","003ak00001MvUBDAA3",
    "003ak00001MvUBEAA3","003ak00001MvUBFAA3","003ak00001MvUBGAA3","003ak00001MvUBHAA3","003ak00001MvUBIAA3",
    "003ak00001MvUBJAA3","003ak00001MvUBKAA3","003ak00001MvUBLAA3","003ak00001MvUBMAA3","003ak00001MvUBNAA3",
    "003ak00001MvUBOAA3","003ak00001MvUBPAA3","003ak00001MvUBQAA3","003ak00001MvUBRAA3","003ak00001MvUBSAA3",
    "003ak00001MvUBTAA3","003ak00001MvUBUAA3","003ak00001MvUBVAA3","003ak00001MvUBWAA3","003ak00001MvUBXAA3",
    "003ak00001MvUBYAA3","003ak00001MvUBZAA3","003ak00001MvUBaAAN","003ak00001MvUBbAAN","003ak00001MvUBcAAN",
    "003ak00001MvUBdAAN","003ak00001MvUBeAAN","003ak00001MvUBfAAN","003ak00001MvUBgAAN","003ak00001MvUBhAAN",
    "003ak00001MvUBiAAN","003ak00001MvUBjAAN","003ak00001MvUBkAAN","003ak00001MvUBlAAN","003ak00001MvUBmAAN",
    "003ak00001MvUBnAAN","003ak00001MvUBoAAN","003ak00001MvUBpAAN","003ak00001MvUBqAAN","003ak00001MvUBrAAN",
    "003ak00001MvUBsAAN","003ak00001MvUBtAAN","003ak00001MvUBuAAN","003ak00001MvUBvAAN","003ak00001MvUBwAAN",
    "003ak00001MvUBxAAN","003ak00001MvUByAAN","003ak00001MvUBzAAN","003ak00001MvUC0AAN","003ak00001MvUC1AAN",
    "003ak00001MvUC2AAN","003ak00001MvUC3AAN","003ak00001MvUC4AAN","003ak00001MvUC5AAN","003ak00001MvUC6AAN",
    "003ak00001MvUC7AAN","003ak00001MvUC8AAN","003ak00001MvUC9AAN","003ak00001MvUCAAA3","003ak00001MvUCBAA3",
    "003ak00001MvUCCAA3","003ak00001MvUCDAA3","003ak00001MvUCEAA3","003ak00001MvUCFAA3","003ak00001MvUCGAA3",
]

ev_vins = [
    "KMXTE202100069590","KMXTE202400076235","KMXHY202400107951","KMXKI202500151710","KMXTE202500312633",
    "KMXHY202300336795","KMXCH202300498276","KMXTE202400555985","KMXTO202000824764","KMXCH202300896936",
    "KMXTO201900906914","KMXTE202500929762","KMXKI201900932391","KMXTE202501267839","KMXTO202501432204",
    "KMXTE202101509544","KMXTE202501589303","KMXKI202001666994","KMXTO202001675479","KMXHY202001704352",
    "KMXRI202201738740","KMXTE201901773703","KMXTO201901991911","KMXTE202502103138","KMXHY202402126728",
    "KMXRI202002169449","KMXRI202302438677","KMXTE202102522921","KMXRI202602561771","KMXTE202002577410",
    "KMXRI202102606844","KMXRI202102666183","KMXHY202202717587","5NMS3DAJ0RH234567","7SAYGDEE5RF789012",
    "KM8KRDAF9PU890123","2T3F1RFV0RW901234",
]

ev_page_urls = [
    "https://www.carmax.com/cars/electric",
    "https://www.carmax.com/cars/hybrid",
    "https://www.carmax.com/electric-cars",
    "https://www.carmax.com/cars/tesla",
    "https://www.carmax.com/cars/rivian",
    "https://www.carmax.com/cars/hyundai/ioniq-5",
    "https://www.carmax.com/cars/chevrolet/bolt-euv",
    "https://www.carmax.com/cars/kia/ev6",
    "https://www.carmax.com/articles/can-an-ev-fit-my-lifestyle",
    "https://www.carmax.com/articles/ev-buying-guide",
    "https://www.carmax.com/articles/best-used-electric-cars",
]

event_types = ["Page View","Vehicle Detail View","Search","Save Vehicle","Schedule Test Drive",
               "Chat Started","Finance Application","Share","Get Directions","Instant Offer Start"]
event_weights = [30, 25, 15, 10, 5, 5, 3, 3, 2, 2]
devices = ["Desktop","Mobile","Tablet"]
device_weights = [45, 40, 15]
utm_sources = ["email","google","facebook","carmax_app","direct","instagram"]
utm_mediums = ["display","social","cpc","email","app_notification","organic"]

today = datetime(2026, 5, 14)
random.seed(42)

contacts_shuffled = contact_ids[:]
random.shuffle(contacts_shuffled)
hot_contacts  = contacts_shuffled[:30]
warm_contacts = contacts_shuffled[30:60]
cool_contacts = contacts_shuffled[60:]

def random_dt(days_min, days_max):
    delta_days = random.uniform(days_min, days_max)
    dt = today - timedelta(days=delta_days, seconds=random.randint(0, 86400))
    return dt.strftime("%Y-%m-%d %H:%M:%S.000 UTC")

def make_vin(event_type):
    if event_type in ("Vehicle Detail View","Save Vehicle","Schedule Test Drive"):
        return random.choice(ev_vins)
    elif event_type in ("Finance Application","Instant Offer Start"):
        return random.choice(ev_vins) if random.random() < 0.7 else ""
    else:
        return random.choice(ev_vins) if random.random() < 0.3 else ""

def make_url(event_type, vin):
    if event_type == "Vehicle Detail View" and vin:
        return f"https://www.carmax.com/car/{vin}"
    elif event_type == "Finance Application":
        return "https://www.carmax.com/finance/apply"
    elif event_type == "Instant Offer Start":
        return "https://www.carmax.com/sell-my-car/instant-offer"
    elif event_type == "Schedule Test Drive" and vin:
        return f"https://www.carmax.com/car/{vin}/test-drive"
    else:
        return random.choice(ev_page_urls)

records = []
rec_num = [12744]  # mutable container

def add_records(contact_list, days_min, days_max, total_target):
    per_contact = total_target // len(contact_list)
    remainder = total_target - (per_contact * len(contact_list))
    for i, contact_id in enumerate(contact_list):
        count = max(5, per_contact + (1 if i < remainder else 0) + random.randint(-15, 15))
        sessions = [f"SES-EV-{random.randint(100000,999999)}" for _ in range(random.randint(1,3))]
        for _ in range(count):
            rec_num[0] += 1
            et = random.choices(event_types, weights=event_weights)[0]
            vin = make_vin(et)
            records.append({
                "EngagementId": f"WE-EV-{rec_num[0]:06d}",
                "EventType": et,
                "EventDateTime": random_dt(days_min, days_max),
                "IndividualId": contact_id,
                "PageURL": make_url(et, vin),
                "SessionId": random.choice(sessions),
                "DeviceType": random.choices(devices, weights=device_weights)[0],
                "VehicleVIN": vin,
                "UTMSource": random.choice(utm_sources),
                "UTMMedium": random.choice(utm_mediums),
                "UTMCampaign": "electric_vehicle_promo",
            })

add_records(hot_contacts,  0.5,  7,  3000)
add_records(warm_contacts, 8,   30,  3000)
add_records(cool_contacts, 31,  90,  4000)

out_path = "/Users/afeder/Projects/CarMax/CarMax_EV_WebEngagement_Mock.csv"
fieldnames = ["EngagementId","EventType","EventDateTime","IndividualId","PageURL",
              "SessionId","DeviceType","VehicleVIN","UTMSource","UTMMedium","UTMCampaign"]
with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

c = Counter(r["IndividualId"] for r in records)
print(f"Total records: {len(records)}")
print(f"Hot (last 7d):   {len(hot_contacts)} contacts")
print(f"Warm (8-30d):    {len(warm_contacts)} contacts")
print(f"Cool (31-90d):   {len(cool_contacts)} contacts")
print(f"Unique contacts: {len(c)}")
print(f"Min/max records per contact: {min(c.values())} / {max(c.values())}")
print(f"Written to: {out_path}")
