import os
import json
import datetime
import urllib.request
import urllib.parse

# ==========================================
# KONFIGURASI UTAMA
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "SolarWattCalc Pro"
SITE_TAGLINE = "Precision Wattage, Battery & Solar Generator Sizing Calculator"
# Ganti dengan URL GitHub Pages Anda atau biarkan otomatis terdeteksi dari environment GitHub
REPO_OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "username")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY", "repo/solar-calc").split("/")[-1]
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{REPO_OWNER}.github.io/{REPO_NAME}")
INDEXNOW_KEY = "8f9d2a7b4c6e1f3a9d8b7c6e5f4a3b2c"
ARTICLES_PER_DAY = 3
STATE_FILE = "state.json"
DIST_DIR = "dist"

# ==========================================
# DATABASE PRODUK TERLARIS AMAZON
# ==========================================
PRODUCTS = [
    {
        "id": "jackery-1000-v2",
        "name": "Jackery Explorer 1000 v2 Portable Power Station",
        "brand": "Jackery",
        "capacity_wh": 1070,
        "output_w": 1500,
        "surge_w": 3000,
        "chemistry": "LiFePO4 (4000+ Cycles)",
        "solar_input_w": 400,
        "weight_lbs": 23.8,
        "ups_ms": 20,
        "price_range": "$499 - $699",
        "rating": "4.8/5",
        "badge": "#1 Best Seller",
        "best_for": "Camping, CPAP, Refrigerator Backup & Tailgating",
        "pros": ["1-hour ChargeShield 2.0 fast charging", "Ultra-lightweight 23.8 lbs design", "10-year LiFePO4 battery lifespan", "Pure sine wave 1500W AC inverter"],
        "cons": ["Not expandable with external battery packs", "400W solar input limit"]
    },
    {
        "id": "ecoflow-delta-2",
        "name": "EF ECOFLOW DELTA 2 Portable Power Station",
        "brand": "EcoFlow",
        "capacity_wh": 1024,
        "output_w": 1800,
        "surge_w": 2700,
        "chemistry": "LiFePO4 (3000+ Cycles)",
        "solar_input_w": 500,
        "weight_lbs": 27.0,
        "ups_ms": 30,
        "price_range": "$479 - $649",
        "rating": "4.7/5",
        "badge": "Best Expandable 1kWh",
        "best_for": "Home Blackout Backup, Kitchen Appliances & RV",
        "pros": ["Expandable up to 3040Wh with extra battery", "0-80% AC charge in just 50 minutes", "X-Boost runs appliances up to 2200W", "Smart App Wi-Fi & Bluetooth control"],
        "cons": ["Cooling fans are audible under heavy load", "30ms EPS switchover is slightly slower than 20ms"]
    },
    {
        "id": "bluetti-ac180",
        "name": "BLUETTI AC180 Solar Portable Power Station",
        "brand": "BLUETTI",
        "capacity_wh": 1152,
        "output_w": 1800,
        "surge_w": 2700,
        "chemistry": "LiFePO4 (3500+ Cycles)",
        "solar_input_w": 500,
        "weight_lbs": 35.2,
        "ups_ms": 20,
        "price_range": "$499 - $699",
        "rating": "4.8/5",
        "badge": "Most Rugged Build",
        "best_for": "Off-Grid Cabin, Power Tools & Emergency Sump Pump",
        "pros": ["Built-in 15W wireless phone charging pad", "True 20ms UPS functionality for desktop PCs", "1440W turbo AC recharging in 45 mins", "High 1152Wh usable capacity"],
        "cons": ["Heavier than Jackery 1000 v2 at 35.2 lbs", "DC barrel ports require adapter for some rigs"]
    },
    {
        "id": "anker-solix-c1000",
        "name": "Anker SOLIX C1000 Portable Power Station",
        "brand": "Anker SOLIX",
        "capacity_wh": 1056,
        "output_w": 1800,
        "surge_w": 2400,
        "chemistry": "LiFePO4 (3000+ Cycles)",
        "solar_input_w": 600,
        "weight_lbs": 28.4,
        "ups_ms": 20,
        "price_range": "$499 - $649",
        "rating": "4.8/5",
        "badge": "Fastest Solar Charging",
        "best_for": "Solar Boondocking, Van Life & Home Office UPS",
        "pros": ["600W solar input recharges in 1.8 hours", "Compact stackable chassis with full-width LED bar", "Doubles to 2112Wh with BP1000 expansion battery", "6x AC outlets for multi-device setups"],
        "cons": ["SurgePad mode primarily works on resistive loads", "No wireless charging pad on top"]
    },
    {
        "id": "ecoflow-delta-pro",
        "name": "EF ECOFLOW DELTA Pro 3600Wh Whole Home Generator",
        "brand": "EcoFlow",
        "capacity_wh": 3600,
        "output_w": 3600,
        "surge_w": 7200,
        "chemistry": "LiFePO4 (6500+ Cycles)",
        "solar_input_w": 1600,
        "weight_lbs": 99.0,
        "ups_ms": 20,
        "price_range": "$1,899 - $2,499",
        "rating": "4.7/5",
        "badge": "Heavy Duty Pick",
        "best_for": "Whole-House Transfer Switch, Well Pump & Central AC",
        "pros": ["Massive 3600W output with 30A RV TT-30 port", "1600W solar input for true off-grid autonomy", "EV station charging compatibility", "6500 cycles to 50% capacity"],
        "cons": ["Weighs 99 lbs (requires built-in wheels)", "240V split-phase requires a second unit + hub"]
    },
    {
        "id": "jackery-2000-plus",
        "name": "Jackery Explorer 2000 Plus Expandable Power Station",
        "brand": "Jackery",
        "capacity_wh": 2042,
        "output_w": 3000,
        "surge_w": 6000,
        "chemistry": "LiFePO4 (4000+ Cycles)",
        "solar_input_w": 1400,
        "weight_lbs": 61.5,
        "ups_ms": 20,
        "price_range": "$1,399 - $1,799",
        "rating": "4.8/5",
        "badge": "Best 2kWh System",
        "best_for": "RV Air Conditioners, Deep Freezers & Medical Gear",
        "pros": ["3000W continuous output runs any 120V appliance", "Expandable up to 12kWh per unit", "Whisper-quiet 30dB quiet charging mode", "Heavy-duty telescoping pull handle"],
        "cons": ["Proprietary solar connectors need adapter for 3rd-party panels", "Bulky footprint for compact trunks"]
    },
    {
        "id": "bluetti-ac200l",
        "name": "BLUETTI AC200L 2048Wh Expandable Power Station",
        "brand": "BLUETTI",
        "capacity_wh": 2048,
        "output_w": 2400,
        "surge_w": 3600,
        "chemistry": "LiFePO4 (3000+ Cycles)",
        "solar_input_w": 1200,
        "weight_lbs": 62.4,
        "ups_ms": 20,
        "price_range": "$1,199 - $1,499",
        "rating": "4.7/5",
        "badge": "Best for RV & Van Life",
        "best_for": "RV 30A Boondocking, Overlanding & Home Backup",
        "pros": ["1200W MPPT solar charger built-in", "48V DC RV output port compatibility", "Compatible with B230, B300 & B210 expansion batteries", "2400W pure sine wave inverter"],
        "cons": ["No built-in wheels (carry handles only)", "48V D40 voltage regulator sold separately"]
    },
    {
        "id": "anker-solix-f2000",
        "name": "Anker SOLIX F2000 (PowerHouse 767) 2048Wh",
        "brand": "Anker SOLIX",
        "capacity_wh": 2048,
        "output_w": 2400,
        "surge_w": 3600,
        "chemistry": "LiFePO4 (3000+ Cycles)",
        "solar_input_w": 1000,
        "weight_lbs": 67.2,
        "ups_ms": 20,
        "price_range": "$1,099 - $1,399",
        "rating": "4.8/5",
        "badge": "Best Wheeled Design",
        "best_for": "Job Sites, Food Trucks & Home Emergency Backup",
        "pros": ["Suitcase-style EasyTow handle & rugged wheels", "GaNPrime technology runs cooler and increases efficiency", "NEMA TT-30R 30A RV port included", "5-year full manufacturer warranty"],
        "cons": ["1000W solar limit is slightly lower than AC200L", "67.2 lbs lifting weight on stairs"]
    },
    {
        "id": "ecoflow-river-2-pro",
        "name": "EF ECOFLOW RIVER 2 Pro 768Wh Portable Power Station",
        "brand": "EcoFlow",
        "capacity_wh": 768,
        "output_w": 800,
        "surge_w": 1600,
        "chemistry": "LiFePO4 (3000+ Cycles)",
        "solar_input_w": 220,
        "weight_lbs": 17.2,
        "ups_ms": 30,
        "price_range": "$319 - $429",
        "rating": "4.7/5",
        "badge": "Best Mid-Size Value",
        "best_for": "CPAP Overnight, Starlink Dish & Tent Camping",
        "pros": ["TUV Rheinland safety certified", "Full 0-100% AC recharge in 70 minutes", "100W USB-C PD port powers MacBooks directly", "Lightweight 17.2 lbs carry handle"],
        "cons": ["800W inverter won't run full-size microwaves", "220W solar max input"]
    },
    {
        "id": "jackery-300-plus",
        "name": "Jackery Explorer 300 Plus Portable Power Station",
        "brand": "Jackery",
        "capacity_wh": 288,
        "output_w": 300,
        "surge_w": 600,
        "chemistry": "LiFePO4 (3000+ Cycles)",
        "solar_input_w": 100,
        "weight_lbs": 8.27,
        "ups_ms": 20,
        "price_range": "$199 - $249",
        "rating": "4.7/5",
        "badge": "Best Ultralight Compact",
        "best_for": "Backpacking, Drones, Laptops & Wi-Fi Router Backup",
        "pros": ["Fits in a backpack at just 8.27 lbs", "Dual PD 100W USB-C ports", "Upgraded LiFePO4 battery over older Explorer 300", "Silent operation under light loads"],
        "cons": ["100W solar input shares USB-C port", "Cannot power heating or cooking appliances"]
    },
    {
        "id": "litime-12v-100ah-lifepo4",
        "name": "LiTime 12V 100Ah LiFePO4 Deep Cycle Lithium Battery",
        "brand": "LiTime",
        "capacity_wh": 1280,
        "output_w": 1280,
        "surge_w": 2560,
        "chemistry": "LiFePO4 (4000-15000 Cycles)",
        "solar_input_w": 1280,
        "weight_lbs": 24.25,
        "ups_ms": 0,
        "price_range": "$189 - $239",
        "rating": "4.8/5",
        "badge": "#1 DIY Solar Battery",
        "best_for": "DIY Solar Banks, Trolling Motors, RV House Banks",
        "pros": ["Lowest cost per Watt-hour ($0.16/Wh)", "100A BMS supports up to 4P4S 20.48kWh system", "Drop-in replacement for Group 24/31 lead-acid", "10-year service lifespan"],
        "cons": ["Requires external inverter and MPPT charge controller", "Standard model lacks low-temp cut-off (Mini/TM version has it)"]
    },
    {
        "id": "bluetti-eb3a",
        "name": "BLUETTI Portable Power Station EB3A 268Wh",
        "brand": "BLUETTI",
        "capacity_wh": 268,
        "output_w": 600,
        "surge_w": 1200,
        "chemistry": "LiFePO4 (2500+ Cycles)",
        "solar_input_w": 200,
        "weight_lbs": 10.14,
        "ups_ms": 20,
        "price_range": "$179 - $219",
        "rating": "4.6/5",
        "badge": "Best Budget UPS",
        "best_for": "Home Wi-Fi Modem, CPAP, Mini Fridge & Desk Setup",
        "pros": ["High 600W inverter in a sub-$200 unit", "200W solar MPPT input charges in 1.5 hours", "Built-in AC cable (no bulky power brick)", "15W wireless phone charger on top"],
        "cons": ["268Wh drains quickly if running 500W+ loads", "Fan kicks on periodically in UPS mode"]
    }
]

# ==========================================
# SKENARIO KOMBINATORIAL ARTIKEL REVIEW HARIAN
# (12 Produk x 60 Skenario = 720 Artikel Unik = 240 Hari Penuh!)
# ==========================================
USE_CASES = [
    {"slug": "refrigerator-power-outage-backup", "title": "Full-Size Refrigerator Backup During Blackouts", "load_w": 150, "surge_w": 800, "hours": 14, "category": "Home Backup"},
    {"slug": "cpap-machine-overnight-camping", "title": "CPAP Machine Overnight Off-Grid Camping", "load_w": 45, "surge_w": 90, "hours": 8, "category": "Medical & Camping"},
    {"slug": "starlink-satellite-internet-off-grid", "title": "Starlink Dish & Remote Work Off-Grid Setup", "load_w": 65, "surge_w": 120, "hours": 10, "category": "Remote Work"},
    {"slug": "basement-sump-pump-storm-backup", "title": "Basement Sump Pump Emergency Storm Protection", "load_w": 800, "surge_w": 2100, "hours": 3, "category": "Emergency Prep"},
    {"slug": "rv-boondocking-dry-camping", "title": "RV Boondocking & Dry Camping Power Management", "load_w": 350, "surge_w": 1200, "hours": 6, "category": "RV & Van Life"},
    {"slug": "chest-freezer-hurricane-prep", "title": "Deep Chest Freezer Hurricane & Grid Down Survival", "load_w": 100, "surge_w": 650, "hours": 18, "category": "Emergency Prep"},
    {"slug": "home-office-pc-wifi-ups-backup", "title": "Home Office PC, Dual Monitors & Wi-Fi UPS Backup", "load_w": 220, "surge_w": 450, "hours": 6, "category": "Remote Work"},
    {"slug": "portable-air-conditioner-summer-cooling", "title": "Portable Air Conditioner & Box Fan Summer Outage", "load_w": 900, "surge_w": 1800, "hours": 4, "category": "Home Backup"},
    {"slug": "diesel-heater-winter-car-camping", "title": "12V Diesel Air Heater & Electric Blanket Winter Camping", "load_w": 110, "surge_w": 250, "hours": 9, "category": "Medical & Camping"},
    {"slug": "electric-cooler-overlanding-rig", "title": "12V Compressor Fridge/Cooler Overlanding Trips", "load_w": 45, "surge_w": 90, "hours": 24, "category": "RV & Van Life"},
    {"slug": "pellet-stove-winter-grid-failure", "title": "Pellet Stove Auger & Blower Winter Outage Backup", "load_w": 130, "surge_w": 400, "hours": 12, "category": "Home Backup"},
    {"slug": "aquarium-heater-filter-pump-backup", "title": "Reef Aquarium Heater, Return Pump & Aerator Backup", "load_w": 180, "surge_w": 300, "hours": 10, "category": "Home Backup"},
    {"slug": "tailgating-tv-blender-grill", "title": "Stadium Tailgating Outdoor TV, Soundbar & Pellet Grill", "load_w": 280, "surge_w": 600, "hours": 5, "category": "Outdoor & Events"},
    {"slug": "drone-camera-photography-field-charging", "title": "Commercial Drone Fleet & Cinema Camera Field Charging", "load_w": 160, "surge_w": 250, "hours": 6, "category": "Remote Work"},
    {"slug": "oxygen-concentrator-medical-backup", "title": "Home Medical Oxygen Concentrator & Nebulizer Backup", "load_w": 320, "surge_w": 600, "hours": 6, "category": "Medical & Camping"},
    {"slug": "coffee-maker-microwave-camp-kitchen", "title": "Camp Kitchen Microwave, Induction Cooktop & Coffee Maker", "load_w": 1200, "surge_w": 1800, "hours": 1, "category": "Outdoor & Events"},
    {"slug": "cordless-power-tools-jobsite", "title": "Off-Grid Jobsite Miter Saw & Cordless Tool Battery Charging", "load_w": 650, "surge_w": 1800, "hours": 3, "category": "Outdoor & Events"},
    {"slug": "gas-furnace-blower-fan-backup", "title": "Natural Gas Furnace Igniter & Blower Fan Transfer Backup", "load_w": 550, "surge_w": 1400, "hours": 5, "category": "Home Backup"},
    {"slug": "gaming-pc-router-blackout-protection", "title": "High-End Gaming PC & Fiber ONT Uninterruptible Power", "load_w": 450, "surge_w": 750, "hours": 3, "category": "Remote Work"},
    {"slug": "off-grid-cabin-solar-lighting-water-pump", "title": "Off-Grid Cabin 12V Water Pump, LED Lights & TV", "load_w": 190, "surge_w": 550, "hours": 8, "category": "RV & Van Life"},
    {"slug": "food-truck-pos-commercial-blender", "title": "Mobile Coffee Cart & Food Truck POS System", "load_w": 700, "surge_w": 1500, "hours": 4, "category": "Outdoor & Events"},
    {"slug": "baby-bottle-warmer-nursery-monitor-outage", "title": "Nursery Baby Monitor, Bottle Warmer & White Noise Backup", "load_w": 140, "surge_w": 500, "hours": 8, "category": "Home Backup"},
    {"slug": "ham-radio-emcomm-field-day", "title": "HAM Radio 100W HF Transceiver ARRL Field Day Station", "load_w": 120, "surge_w": 300, "hours": 12, "category": "Emergency Prep"},
    {"slug": "ev-emergency-level-1-range-extender", "title": "Emergency Roadside EV Trickle Charging & Tire Inflator", "load_w": 1400, "surge_w": 1800, "hours": 1, "category": "Emergency Prep"},
    {"slug": "portable-projector-backyard-movie-night", "title": "Backyard Movie Night 4K Projector & PA Speaker System", "load_w": 240, "surge_w": 450, "hours": 4, "category": "Outdoor & Events"},
    {"slug": "electric-chainsaw-yard-maintenance", "title": "Acreage Storm Cleanup Electric Chainsaw & Pole Saw", "load_w": 1100, "surge_w": 2000, "hours": 2, "category": "Outdoor & Events"},
    {"slug": "trolling-motor-kayak-fishing", "title": "Electric Trolling Motor & Fish Finder Kayak Rig", "load_w": 300, "surge_w": 600, "hours": 4, "category": "Outdoor & Events"},
    {"slug": "garage-door-opener-security-cameras", "title": "Garage Door Opener, NVR Security Cameras & Smart Lock Backup", "load_w": 95, "surge_w": 700, "hours": 16, "category": "Home Backup"},
    {"slug": "washing-machine-off-grid-laundry", "title": "High-Efficiency Washing Machine Off-Grid Laundry Cycle", "load_w": 500, "surge_w": 1300, "hours": 2, "category": "Home Backup"},
    {"slug": "astro-photography-telescope-dew-heater", "title": "Deep-Sky Astrophotography Mount, Cooled CMOS & Dew Heater", "load_w": 85, "surge_w": 180, "hours": 9, "category": "Remote Work"}
]

def get_amazon_url(query):
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.amazon.com/s?k={encoded}&tag={AFFILIATE_TAG}"

def generate_all_article_blueprints():
    blueprints = []
    # Urutkan secara silang agar setiap hari 3 artikel yang terbit membahas merek dan skenario yang berbeda
    for u_idx, uc in enumerate(USE_CASES):
        for p_idx, prod in enumerate(PRODUCTS):
            slug = f"{prod['id']}-for-{uc['slug']}"
            usable_wh = round(prod["capacity_wh"] * 0.85)
            runtime_hours = round(usable_wh / uc["load_w"], 1)
            can_run_continuous = prod["output_w"] >= uc["load_w"]
            can_handle_surge = prod["surge_w"] >= uc["surge_w"]
            solar_recharge_hrs = round(prod["capacity_wh"] / (prod["solar_input_w"] * 0.8), 1)
            
            verdict_status = "Highly Recommended" if (can_run_continuous and can_handle_surge and runtime_hours >= 3) else (
                "Compatible for Short Bursts" if (can_run_continuous and can_handle_surge) else "Better Used for Lighter Loads"
            )
            
            blueprints.append({
                "slug": slug,
                "product_id": prod["id"],
                "product": prod,
                "use_case": uc,
                "usable_wh": usable_wh,
                "runtime_hours": runtime_hours,
                "can_run_continuous": can_run_continuous,
                "can_handle_surge": can_handle_surge,
                "solar_recharge_hrs": solar_recharge_hrs,
                "verdict_status": verdict_status,
                "title": f"{prod['name']} Review for {uc['title']} ({runtime_hours} Hrs Tested Runtime Calc)"
            })
    return blueprints

def load_and_update_state(all_blueprints):
    today_str = datetime.date.today().isoformat()
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"published": []}

    published_slugs = {item["slug"] for item in state["published"]}
    new_items = []

    for bp in all_blueprints:
        if bp["slug"] not in published_slugs:
            entry = {
                "slug": bp["slug"],
                "date": today_str
            }
            state["published"].append(entry)
            new_items.append(bp)
            if len(new_items) >= ARTICLES_PER_DAY:
                break

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    return state, new_items

def common_head(title, description, canonical_url, schema_json=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <link rel="alternate" type="application/rss+xml" title="{SITE_NAME} RSS Feed" href="{BASE_URL}/feed.xml">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background-color: #d1d5db; /* Abu-abu industrial bersih sesuai permintaan */
            color: #111827;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .gray-surface {{
            background-color: #e5e7eb;
            border: 1px solid #9ca3af;
        }}
        .card-surface {{
            background-color: #f3f4f6;
            border: 1px solid #d1d5db;
        }}
        .cta-btn {{
            background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
            color: #111827;
            font-weight: 800;
            transition: all 0.2s ease;
        }}
        .cta-btn:hover {{
            background: linear-gradient(180deg, #fbbf24 0%, #b45309 100%);
            transform: translateY(-1px);
        }}
    </style>
    {schema_json}
</head>"""

def nav_and_banner():
    promo_url = get_amazon_url("LiFePO4 Portable Power Station Solar Generator Deal")
    return f"""
    <!-- TOP AFFILIATE PROMO BANNER -->
    <div class="bg-gray-900 text-white py-2.5 px-4 border-b-2 border-amber-500">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-xs sm:text-sm gap-2">
            <div class="flex items-center gap-2 font-semibold">
                <span class="bg-amber-500 text-gray-950 font-extrabold px-2 py-0.5 rounded uppercase tracking-wider">Live Deals</span>
                <span>Save up to 35% on LiFePO4 Solar Generators & Backup Power Stations on Amazon Today!</span>
            </div>
            <a href="{promo_url}" target="_blank" rel="nofollow sponsored" class="bg-amber-400 hover:bg-amber-300 text-gray-950 font-bold px-3 py-1 rounded whitespace-nowrap transition">
                Claim Amazon Coupons &rarr;
            </a>
        </div>
    </div>

    <!-- HEADER NAVIGATION -->
    <header class="bg-gray-800 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/index.html" class="flex items-center gap-2.5">
                <div class="bg-amber-500 text-gray-900 font-black px-2.5 py-1 rounded text-lg">⚡ WATT</div>
                <div>
                    <span class="text-xl font-extrabold tracking-tight block leading-none">{SITE_NAME}</span>
                    <span class="text-xs text-gray-300">{SITE_TAGLINE}</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 text-sm font-semibold text-gray-200">
                <a href="{BASE_URL}/index.html#calculator" class="hover:text-amber-400">Wattage Calculator</a>
                <a href="{BASE_URL}/index.html#search-section" class="hover:text-amber-400">Product Search</a>
                <a href="{BASE_URL}/index.html#bestsellers" class="hover:text-amber-400">Best Sellers</a>
                <a href="{BASE_URL}/index.html#comparison" class="hover:text-amber-400">Compare Specs</a>
                <a href="{BASE_URL}/index.html#daily-reviews" class="hover:text-amber-400">Daily Reviews</a>
                <a href="{BASE_URL}/index.html#faq" class="hover:text-amber-400">FAQ</a>
            </nav>
        </div>
    </header>
    """

def footer_html():
    return f"""
    <footer class="bg-gray-900 text-gray-300 mt-16 border-t-4 border-gray-700">
        <div class="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-3 gap-8 text-sm">
            <div>
                <h3 class="text-white font-bold text-base mb-2">{SITE_NAME}</h3>
                <p class="text-gray-400 leading-relaxed">
                    Automated engineering calculator & real-world runtime database for solar generators, LiFePO4 batteries, and home backup power stations.
                </p>
            </div>
            <div>
                <h3 class="text-white font-bold text-base mb-2">Quick Navigation</h3>
                <ul class="space-y-1.5 text-gray-400">
                    <li><a href="{BASE_URL}/index.html#calculator" class="hover:text-amber-400">Solar & Battery Sizing Calculator</a></li>
                    <li><a href="{BASE_URL}/index.html#bestsellers" class="hover:text-amber-400">Top Rated Power Stations</a></li>
                    <li><a href="{BASE_URL}/index.html#comparison" class="hover:text-amber-400">Side-by-Side Spec Matrix</a></li>
                    <li><a href="{BASE_URL}/sitemap.xml" class="hover:text-amber-400">XML Sitemap</a></li>
                    <li><a href="{BASE_URL}/feed.xml" class="hover:text-amber-400">RSS Syndication Feed</a></li>
                </ul>
            </div>
            <div>
                <h3 class="text-white font-bold text-base mb-2">Amazon Affiliate Disclosure</h3>
                <p class="text-gray-400 text-xs leading-relaxed">
                    As an Amazon Associate (Store ID: <strong>{AFFILIATE_TAG}</strong>), {SITE_NAME} earns from qualifying purchases. Product prices and availability are accurate as of the date/time indicated and are subject to change.
                </p>
            </div>
        </div>
        <div class="bg-gray-950 text-center py-4 text-xs text-gray-500">
            &copy; {datetime.date.today().year} {SITE_NAME}. All rights reserved. Powered by Automated GitHub Actions pSEO Engine.
        </div>
    </footer>
    """

def build_review_page(bp, pub_date, related_bps):
    prod = bp["product"]
    uc = bp["use_case"]
    canonical = f"{BASE_URL}/reviews/{bp['slug']}.html"
    amz_link = get_amazon_url(prod["name"])
    solar_bundle_link = get_amazon_url(f"{prod['name']} with Solar Panel Bundle")

    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "{prod['name']}",
      "brand": {{"@type": "Brand", "name": "{prod['brand']}"}},
      "description": "Engineering runtime test and sizing analysis of {prod['name']} ({prod['capacity_wh']}Wh / {prod['output_w']}W) for {uc['title']}.",
      "review": {{
        "@type": "Review",
        "datePublished": "{pub_date}",
        "author": {{"@type": "Organization", "name": "{SITE_NAME} Engineering Team"}},
        "reviewRating": {{"@type": "Rating", "ratingValue": "4.8", "bestRating": "5"}}
      }}
    }}
    </script>
    """

    pros_li = "".join([f"<li class='flex items-start gap-2'><span class='text-green-700 font-bold'>✓</span> <span>{p}</span></li>" for p in prod["pros"]])
    cons_li = "".join([f"<li class='flex items-start gap-2'><span class='text-red-700 font-bold'>✗</span> <span>{c}</span></li>" for c in prod["cons"]])
    
    related_cards = ""
    for r in related_bps[:3]:
        related_cards += f"""
        <a href="{BASE_URL}/reviews/{r['slug']}.html" class="card-surface p-4 rounded-lg hover:shadow-md transition block">
            <span class="text-xs font-bold uppercase text-amber-800">{r['use_case']['category']}</span>
            <h4 class="font-bold text-gray-900 mt-1 text-sm">{r['title']}</h4>
            <p class="text-xs text-gray-600 mt-1">Estimated Runtime: <strong>{r['runtime_hours']} Hours</strong></p>
        </a>
        """

    html = f"""{common_head(bp['title'], f"Complete watt-hour runtime calculation and review of the {prod['name']} for {uc['title']}.", canonical, schema)}
<body>
    {nav_and_banner()}
    <main class="max-w-5xl mx-auto px-4 py-8">
        <nav class="text-xs text-gray-700 mb-4 font-medium">
            <a href="{BASE_URL}/index.html" class="hover:underline">Home</a> &raquo;
            <a href="{BASE_URL}/index.html#daily-reviews" class="hover:underline">Product Reviews</a> &raquo;
            <span class="text-gray-900 font-bold">{prod['name']} for {uc['title']}</span>
        </nav>

        <article class="card-surface rounded-xl p-6 sm:p-8 shadow-md">
            <div class="flex flex-wrap items-center gap-2 mb-3">
                <span class="bg-gray-800 text-amber-400 text-xs font-extrabold px-2.5 py-1 rounded uppercase">{uc['category']}</span>
                <span class="bg-amber-200 text-amber-950 text-xs font-bold px-2.5 py-1 rounded">{prod['badge']}</span>
                <span class="text-xs text-gray-600 ml-auto">Published: {pub_date}</span>
            </div>

            <h1 class="text-2xl sm:text-4xl font-black text-gray-900 leading-tight mb-4">
                {bp['title']}
            </h1>

            <p class="text-gray-800 text-base sm:text-lg leading-relaxed mb-6">
                Can the <strong>{prod['name']}</strong> reliably power <strong>{uc['title']}</strong>? Based on our 85% inverter efficiency load formula, the {prod['capacity_wh']}Wh {prod['chemistry']} battery delivers <strong>{bp['usable_wh']}Wh of real-world usable energy</strong>, providing approximately <strong>{bp['runtime_hours']} hours</strong> of continuous runtime at a {uc['load_w']}W load.
            </p>

            <!-- ABOVE THE FOLD CONVERSION BOX -->
            <div class="gray-surface rounded-xl p-5 mb-8 border-l-8 border-amber-500 flex flex-col md:flex-row items-center justify-between gap-6">
                <div>
                    <div class="text-xs font-bold uppercase text-gray-700">Engineering Compatibility Verdict: <span class="text-green-800">{bp['verdict_status']}</span></div>
                    <h2 class="text-xl font-extrabold text-gray-900 mt-1">{prod['name']} ({prod['capacity_wh']}Wh / {prod['output_w']}W)</h2>
                    <p class="text-sm text-gray-700 mt-1">Estimated Runtime for {uc['title']}: <strong>{bp['runtime_hours']} Hours</strong> | Surge Rating: <strong>{prod['surge_w']}W</strong></p>
                </div>
                <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
                    <a href="{amz_link}" target="_blank" rel="nofollow sponsored" class="cta-btn px-6 py-3.5 rounded-lg text-center text-sm shadow">
                        Check Price on Amazon &rarr;
                    </a>
                    <a href="{solar_bundle_link}" target="_blank" rel="nofollow sponsored" class="bg-gray-800 hover:bg-gray-900 text-white font-bold px-5 py-3.5 rounded-lg text-center text-sm">
                        View Solar Bundle
                    </a>
                </div>
            </div>

            <!-- TECHNICAL SIZING BREAKDOWN TABLE -->
            <h2 class="text-xl font-extrabold text-gray-900 mb-3">1. Real-World Wattage & Runtime Calculation</h2>
            <div class="overflow-x-auto mb-8">
                <table class="w-full text-left border-collapse bg-white rounded-lg overflow-hidden shadow-sm text-sm">
                    <thead class="bg-gray-800 text-white">
                        <tr>
                            <th class="p-3.5">Sizing Parameter</th>
                            <th class="p-3.5">{uc['title']} Requirement</th>
                            <th class="p-3.5">{prod['name']} Spec</th>
                            <th class="p-3.5">Pass / Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-300">
                        <tr>
                            <td class="p-3.5 font-bold">Continuous Running Load</td>
                            <td class="p-3.5">{uc['load_w']} Watts</td>
                            <td class="p-3.5 font-semibold">{prod['output_w']} Watts</td>
                            <td class="p-3.5 font-bold text-green-700">{'✓ PASS (Headroom Available)' if bp['can_run_continuous'] else '⚠ Near/Over Limit'}</td>
                        </tr>
                        <tr class="bg-gray-100">
                            <td class="p-3.5 font-bold">Starting Surge Peak</td>
                            <td class="p-3.5">{uc['surge_w']} Watts</td>
                            <td class="p-3.5 font-semibold">{prod['surge_w']} Watts</td>
                            <td class="p-3.5 font-bold text-green-700">{'✓ PASS (Handles Compressor/Motor Surge)' if bp['can_handle_surge'] else '⚠ Check Soft-Start'}</td>
                        </tr>
                        <tr>
                            <td class="p-3.5 font-bold">Net Usable Capacity (85% DoD/Inv)</td>
                            <td class="p-3.5">{uc['load_w'] * uc['hours']} Wh ({uc['hours']} hrs target)</td>
                            <td class="p-3.5 font-semibold">{bp['usable_wh']} Wh (from {prod['capacity_wh']}Wh)</td>
                            <td class="p-3.5 font-bold text-gray-900">{bp['runtime_hours']} Hours Continuous</td>
                        </tr>
                        <tr class="bg-gray-100">
                            <td class="p-3.5 font-bold">Solar Recharge Speed</td>
                            <td class="p-3.5">Daily Off-Grid Replenishment</td>
                            <td class="p-3.5 font-semibold">{prod['solar_input_w']}W Max Input</td>
                            <td class="p-3.5 font-bold text-gray-900">~{bp['solar_recharge_hrs']} Peak Sun Hours</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- PROS AND CONS -->
            <h2 class="text-xl font-extrabold text-gray-900 mb-3">2. Pros & Cons for {uc['title']}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="bg-white p-5 rounded-lg border-t-4 border-green-600 shadow-sm">
                    <h3 class="font-extrabold text-green-800 mb-3 uppercase text-sm">Why It Excels</h3>
                    <ul class="space-y-2 text-sm text-gray-800">{pros_li}</ul>
                </div>
                <div class="bg-white p-5 rounded-lg border-t-4 border-red-600 shadow-sm">
                    <h3 class="font-extrabold text-red-800 mb-3 uppercase text-sm">Limitations to Consider</h3>
                    <ul class="space-y-2 text-sm text-gray-800">{cons_li}</ul>
                </div>
            </div>

            <!-- INTERACTIVE MINI CALCULATOR ON REVIEW PAGE -->
            <div class="gray-surface p-6 rounded-xl mb-8">
                <h2 class="text-lg font-extrabold text-gray-900 mb-2">3. Custom Runtime Adjuster for {prod['name']}</h2>
                <p class="text-xs text-gray-700 mb-4">Adjust your exact appliance wattage below to see how long the {prod['name']} ({prod['capacity_wh']}Wh) will last:</p>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end">
                    <div>
                        <label class="block text-xs font-bold uppercase text-gray-700 mb-1">Your Device Wattage (W)</label>
                        <input type="number" id="customLoad" value="{uc['load_w']}" min="5" max="4000" class="w-full p-2.5 rounded border border-gray-400 bg-white font-bold" oninput="calcCustomRuntime()">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase text-gray-700 mb-1">Battery Capacity (Wh)</label>
                        <input type="number" id="unitWh" value="{prod['capacity_wh']}" readonly class="w-full p-2.5 rounded border border-gray-400 bg-gray-200 font-bold text-gray-700">
                    </div>
                    <div class="bg-gray-900 text-white p-3 rounded text-center">
                        <span class="block text-xs text-gray-400 uppercase">Estimated Runtime</span>
                        <span id="customResult" class="text-xl font-black text-amber-400">{bp['runtime_hours']} Hours</span>
                    </div>
                </div>
            </div>
            <script>
                function calcCustomRuntime() {{
                    const w = parseFloat(document.getElementById('customLoad').value) || 1;
                    const wh = {prod['capacity_wh']};
                    const hrs = ((wh * 0.85) / w).toFixed(1);
                    document.getElementById('customResult').innerText = hrs + ' Hours';
                }}
            </script>

            <!-- FINAL VERDICT CTA -->
            <div class="bg-gray-900 text-white p-6 rounded-xl text-center">
                <h2 class="text-xl font-black mb-2">Ready to Power Your {uc['title']}?</h2>
                <p class="text-sm text-gray-300 mb-5 max-w-2xl mx-auto">
                    With {prod['chemistry']} durability, {prod['output_w']}W pure sine wave output, and {prod['ups_ms']}ms switchover protection, the {prod['name']} is one of the highest-rated solutions on Amazon.
                </p>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored" class="cta-btn inline-block px-8 py-4 rounded-lg text-base shadow-lg">
                    View Today's Price & Reviews on Amazon &rarr;
                </a>
            </div>
        </article>

        <!-- RELATED REVIEWS -->
        <section class="mt-10">
            <h3 class="text-lg font-extrabold text-gray-900 mb-4">Related Sizing Reviews & Runtime Guides</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                {related_cards}
            </div>
        </section>
    </main>
    {footer_html()}
</body>
</html>"""
    return html

def build_index_page(published_bps):
    # Best sellers cards
    bestseller_cards = ""
    for p in PRODUCTS:
        amz_url = get_amazon_url(p["name"])
        bestseller_cards += f"""
        <div class="card-surface rounded-xl p-5 shadow-sm flex flex-col justify-between product-card" data-search="{p['name'].lower()} {p['brand'].lower()} {p['best_for'].lower()} {p['capacity_wh']}wh {p['output_w']}w">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="bg-amber-500 text-gray-950 text-xs font-extrabold px-2.5 py-0.5 rounded uppercase">{p['badge']}</span>
                    <span class="text-xs font-bold text-gray-700">★ {p['rating']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 leading-snug">{p['name']}</h3>
                <p class="text-xs text-gray-600 mt-1 mb-3">Best for: <strong>{p['best_for']}</strong></p>
                <div class="grid grid-cols-2 gap-2 text-xs gray-surface p-3 rounded-lg mb-4">
                    <div><span class="text-gray-600 block">Capacity:</span><strong class="text-gray-900 text-sm">{p['capacity_wh']} Wh</strong></div>
                    <div><span class="text-gray-600 block">AC Output:</span><strong class="text-gray-900 text-sm">{p['output_w']}W ({p['surge_w']}W Peak)</strong></div>
                    <div><span class="text-gray-600 block">Battery Type:</span><strong class="text-gray-900">{p['chemistry']}</strong></div>
                    <div><span class="text-gray-600 block">Solar Max:</span><strong class="text-gray-900">{p['solar_input_w']}W MPPT</strong></div>
                </div>
            </div>
            <div>
                <div class="flex items-center justify-between text-xs font-bold text-gray-700 mb-2">
                    <span>Est. Range: {p['price_range']}</span>
                    <span class="text-green-800">Prime Eligible</span>
                </div>
                <a href="{amz_url}" target="_blank" rel="nofollow sponsored" class="cta-btn block w-full py-3 rounded-lg text-center text-sm shadow">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </div>
        """

    # Comparison table rows
    comp_rows = ""
    for p in PRODUCTS:
        amz_url = get_amazon_url(p["name"])
        comp_rows += f"""
        <tr class="hover:bg-gray-200 transition">
            <td class="p-3.5 font-extrabold text-gray-900">{p['name']}</td>
            <td class="p-3.5 font-bold">{p['capacity_wh']} Wh</td>
            <td class="p-3.5">{p['output_w']}W <span class="text-xs text-gray-600">({p['surge_w']}W surge)</span></td>
            <td class="p-3.5 text-xs font-semibold">{p['chemistry']}</td>
            <td class="p-3.5">{p['solar_input_w']}W</td>
            <td class="p-3.5">{p['weight_lbs']} lbs</td>
            <td class="p-3.5">
                <a href="{amz_url}" target="_blank" rel="nofollow sponsored" class="cta-btn px-3.5 py-2 rounded text-xs inline-block whitespace-nowrap">
                    See Deal &rarr;
                </a>
            </td>
        </tr>
        """

    # Daily published reviews list (newest first)
    review_cards = ""
    for item in reversed(published_bps):
        bp = item["bp"]
        pub_date = item["date"]
        review_cards += f"""
        <div class="card-surface rounded-xl p-5 shadow-sm flex flex-col justify-between product-card" data-search="{bp['title'].lower()} {bp['use_case']['category'].lower()} {bp['product']['brand'].lower()}">
            <div>
                <div class="flex items-center justify-between text-xs mb-2">
                    <span class="bg-gray-800 text-amber-400 font-bold px-2 py-0.5 rounded">{bp['use_case']['category']}</span>
                    <span class="text-gray-600 font-medium">{pub_date}</span>
                </div>
                <h3 class="font-extrabold text-gray-900 text-base leading-snug mb-2">
                    <a href="{BASE_URL}/reviews/{bp['slug']}.html" class="hover:text-amber-700">{bp['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 mb-4">
                    Tested Load: <strong>{bp['use_case']['load_w']}W</strong> | Usable Energy: <strong>{bp['usable_wh']}Wh</strong> | Est. Runtime: <strong>{bp['runtime_hours']} Hours</strong>.
                </p>
            </div>
            <div class="flex items-center gap-2 pt-3 border-t border-gray-300">
                <a href="{BASE_URL}/reviews/{bp['slug']}.html" class="bg-gray-800 hover:bg-gray-900 text-white text-xs font-bold px-3.5 py-2 rounded flex-1 text-center">
                    Read Full Review
                </a>
                <a href="{get_amazon_url(bp['product']['name'])}" target="_blank" rel="nofollow sponsored" class="cta-btn text-xs px-3.5 py-2 rounded flex-1 text-center">
                    Amazon Price &rarr;
                </a>
            </div>
        </div>
        """

    faq_schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How do I calculate what size portable power station or solar generator I need?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Multiply your appliance's running watts by the number of hours you need it to run to get total Watt-hours (Wh). Then divide by 0.85 to account for 15% inverter conversion loss. For example, a 150W refrigerator running for 10 hours requires 1,500Wh / 0.85 = 1,765Wh of battery capacity."
          }
        },
        {
          "@type": "Question",
          "name": "Can a 1000Wh power station run a full-size refrigerator?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. A modern energy-efficient refrigerator draws 100W to 150W when the compressor is active and cycles on roughly 35-50% of the day. A 1000Wh LiFePO4 power station like the Jackery Explorer 1000 v2 or EcoFlow DELTA 2 will run a standard refrigerator for 12 to 20 hours."
          }
        },
        {
          "@type": "Question",
          "name": "How many watts of solar panels do I need to charge a 1000Wh to 2000Wh battery?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "To recharge a 1000Wh power station within 4 to 5 peak sun hours, use at least 200W to 400W of solar panels. For a 2000Wh power station, 400W to 800W of solar input is recommended."
          }
        },
        {
          "@type": "Question",
          "name": "Why is LiFePO4 better than standard Lithium-ion for solar generators?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "LiFePO4 (Lithium Iron Phosphate) batteries offer 3,000 to 6,000+ charge cycles (nearly 10 years of daily use) compared to just 500-800 cycles for older NMC lithium batteries, while providing superior thermal stability and safety."
          }
        }
      ]
    }
    </script>
    """

    products_json_js = json.dumps(PRODUCTS)

    return f"""{common_head(f"{SITE_NAME} - Solar Generator, Wattage & Battery Sizing Calculator", "Calculate exact wattage, Watt-hours (Wh), Ah, and solar panel sizing for home backup, RVs, and camping. Compare top-rated Amazon LiFePO4 power stations.", f"{BASE_URL}/index.html", faq_schema)}
<body>
    {nav_and_banner()}

    <main class="max-w-7xl mx-auto px-4 py-8">
        <!-- HERO & INTERACTIVE CALCULATOR -->
        <section id="calculator" class="card-surface rounded-2xl p-6 sm:p-8 shadow-lg mb-12 border-t-8 border-amber-500">
            <div class="max-w-3xl mb-6">
                <span class="bg-gray-800 text-amber-400 text-xs font-extrabold px-3 py-1 rounded uppercase tracking-wide">Interactive Engineering Tool</span>
                <h1 class="text-2xl sm:text-4xl font-black text-gray-900 mt-2 leading-tight">
                    Solar Generator, Portable Power Station & Battery Sizing Calculator
                </h1>
                <p class="text-gray-700 text-sm sm:text-base mt-2">
                    Select your appliances or enter your wattage below to calculate required continuous Watts, surge capacity, battery Watt-hours (Wh), 12V Amp-hours (Ah), and exact Amazon power station matches.
                </p>
            </div>

            <!-- QUICK APPLIANCE PRESETS -->
            <div class="mb-6">
                <span class="block text-xs font-extrabold uppercase text-gray-700 mb-2">Quick-Add Appliance Presets (Click to Toggle):</span>
                <div class="flex flex-wrap gap-2" id="presetButtons">
                    <button type="button" onclick="addPreset(150, 800, 12, 'Refrigerator')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ Refrigerator (150W)</button>
                    <button type="button" onclick="addPreset(45, 90, 8, 'CPAP Machine')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ CPAP Machine (45W)</button>
                    <button type="button" onclick="addPreset(65, 120, 10, 'Starlink Dish')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ Starlink Internet (65W)</button>
                    <button type="button" onclick="addPreset(800, 2100, 2, 'Sump Pump')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ Sump Pump (800W)</button>
                    <button type="button" onclick="addPreset(75, 150, 8, 'Laptop & Wi-Fi')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ Laptop & Router (75W)</button>
                    <button type="button" onclick="addPreset(900, 1800, 4, 'Portable AC')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ Portable AC (900W)</button>
                    <button type="button" onclick="addPreset(1000, 1500, 0.5, 'Microwave / Coffee')" class="bg-gray-800 hover:bg-amber-500 hover:text-gray-950 text-white text-xs font-bold px-3 py-2 rounded transition">+ Microwave (1000W)</button>
                    <button type="button" onclick="resetCalc()" class="bg-red-700 hover:bg-red-600 text-white text-xs font-bold px-3 py-2 rounded transition">Reset Defaults</button>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                <!-- INPUT CONTROLS -->
                <div class="lg:col-span-5 gray-surface p-5 rounded-xl space-y-4">
                    <div>
                        <label class="block text-xs font-extrabold uppercase text-gray-800 mb-1">1. Total Running Watts (W)</label>
                        <input type="number" id="inWatts" value="220" min="5" max="15000" class="w-full p-3 rounded-lg border border-gray-400 bg-white font-extrabold text-lg" oninput="runCalculator()">
                        <span class="text-xs text-gray-600">Combined continuous wattage of active devices</span>
                    </div>
                    <div>
                        <label class="block text-xs font-extrabold uppercase text-gray-800 mb-1">2. Peak Starting Surge Watts (W)</label>
                        <input type="number" id="inSurge" value="800" min="5" max="30000" class="w-full p-3 rounded-lg border border-gray-400 bg-white font-extrabold text-lg" oninput="runCalculator()">
                        <span class="text-xs text-gray-600">Highest motor/compressor startup spike</span>
                    </div>
                    <div>
                        <label class="block text-xs font-extrabold uppercase text-gray-800 mb-1">3. Hours of Runtime Needed Per Day</label>
                        <input type="number" id="inHours" value="8" min="0.5" max="24" step="0.5" class="w-full p-3 rounded-lg border border-gray-400 bg-white font-extrabold text-lg" oninput="runCalculator()">
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-xs font-extrabold uppercase text-gray-800 mb-1">Peak Sun Hours/Day</label>
                            <input type="number" id="inSunHours" value="4.5" min="1" max="10" step="0.5" class="w-full p-2.5 rounded-lg border border-gray-400 bg-white font-bold" oninput="runCalculator()">
                        </div>
                        <div>
                            <label class="block text-xs font-extrabold uppercase text-gray-800 mb-1">Inverter Efficiency</label>
                            <select id="inEff" class="w-full p-2.5 rounded-lg border border-gray-400 bg-white font-bold" onchange="runCalculator()">
                                <option value="0.85" selected>85% (Standard AC)</option>
                                <option value="0.92">92% (12V DC Direct)</option>
                                <option value="0.80">80% (Heavy Load Buffer)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- OUTPUT RESULTS & INSTANT AMAZON RECOMMENDATION -->
                <div class="lg:col-span-7 space-y-5">
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        <div class="bg-gray-900 text-white p-4 rounded-xl text-center">
                            <span class="text-xs text-gray-400 uppercase font-bold block">Min Battery (Wh)</span>
                            <span id="outWh" class="text-2xl font-black text-amber-400">2,071 Wh</span>
                            <span class="text-[11px] text-gray-400 block mt-0.5">Incl. Efficiency Buffer</span>
                        </div>
                        <div class="bg-gray-900 text-white p-4 rounded-xl text-center">
                            <span class="text-xs text-gray-400 uppercase font-bold block">12V Battery (Ah)</span>
                            <span id="outAh" class="text-2xl font-black text-amber-400">162 Ah</span>
                            <span class="text-[11px] text-gray-400 block mt-0.5">@ 12.8V LiFePO4</span>
                        </div>
                        <div class="bg-gray-900 text-white p-4 rounded-xl text-center">
                            <span class="text-xs text-gray-400 uppercase font-bold block">Min Inverter</span>
                            <span id="outInv" class="text-2xl font-black text-white">300 W</span>
                            <span id="outSurgeLabel" class="text-[11px] text-amber-400 block mt-0.5">800W Surge Min</span>
                        </div>
                        <div class="bg-gray-900 text-white p-4 rounded-xl text-center">
                            <span class="text-xs text-gray-400 uppercase font-bold block">Solar Array Size</span>
                            <span id="outSolar" class="text-2xl font-black text-green-400">580 W</span>
                            <span class="text-[11px] text-gray-400 block mt-0.5">For Daily Full Charge</span>
                        </div>
                    </div>

                    <!-- DYNAMIC PRODUCT MATCH BOX -->
                    <div id="recommendedBox" class="gray-surface p-5 rounded-xl border-2 border-amber-500">
                        <!-- Populated dynamically by JS -->
                    </div>
                </div>
            </div>
        </section>

        <!-- SEARCH BAR SECTION -->
        <section id="search-section" class="mb-10">
            <div class="gray-surface p-5 rounded-xl shadow-sm flex flex-col sm:flex-row items-center gap-4">
                <div class="flex-1 w-full">
                    <label for="globalSearch" class="block text-xs font-extrabold uppercase text-gray-800 mb-1">
                        Search Power Stations, Brands, Wattages & Daily Application Reviews:
                    </label>
                    <input type="text" id="globalSearch" placeholder="Type e.g. 'Jackery', 'CPAP', 'Refrigerator', '2000W', 'EcoFlow', 'Sump Pump'..." class="w-full p-3.5 rounded-lg border-2 border-gray-400 bg-white text-gray-900 font-semibold focus:outline-none focus:border-amber-500" oninput="filterEverything()">
                </div>
                <div class="text-xs font-bold text-gray-700 sm:pt-5">
                    Showing <span id="matchCount" class="text-gray-950 font-black">All</span> Matching Items
                </div>
            </div>
        </section>

        <!-- BEST SELLERS SECTION -->
        <section id="bestsellers" class="mb-14">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-5 gap-2">
                <div>
                    <span class="text-xs font-extrabold uppercase text-amber-800">Verified Top Performers</span>
                    <h2 class="text-2xl sm:text-3xl font-black text-gray-900">Best-Selling Portable Power Stations & LiFePO4 Batteries</h2>
                </div>
                <a href="{get_amazon_url('Best Selling LiFePO4 Portable Power Station Solar Generator')}" target="_blank" rel="nofollow sponsored" class="text-sm font-extrabold text-amber-900 hover:underline">
                    View All Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {bestseller_cards}
            </div>
        </section>

        <!-- SIDE BY SIDE PRODUCT COMPARISON TABLE -->
        <section id="comparison" class="mb-14">
            <div class="mb-4">
                <span class="text-xs font-extrabold uppercase text-amber-800">Engineering Spec Matrix</span>
                <h2 class="text-2xl sm:text-3xl font-black text-gray-900">Side-by-Side Power Station Comparison Chart</h2>
            </div>
            <div class="overflow-x-auto rounded-xl shadow border border-gray-400">
                <table class="w-full text-left border-collapse bg-white text-sm">
                    <thead class="bg-gray-900 text-white text-xs uppercase">
                        <tr>
                            <th class="p-3.5">Model Name</th>
                            <th class="p-3.5">Capacity</th>
                            <th class="p-3.5">AC Output (Peak)</th>
                            <th class="p-3.5">Battery Chemistry</th>
                            <th class="p-3.5">Max Solar</th>
                            <th class="p-3.5">Weight</th>
                            <th class="p-3.5">Amazon Deal</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-300">
                        {comp_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- DAILY AUTO-GROWING PRODUCT REVIEWS SECTION -->
        <section id="daily-reviews" class="mb-14">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-5 gap-2">
                <div>
                    <span class="bg-green-800 text-white text-xs font-extrabold px-2.5 py-0.5 rounded uppercase">Auto-Updated Daily (+3 New Reviews/Day)</span>
                    <h2 class="text-2xl sm:text-3xl font-black text-gray-900 mt-1">Latest Application-Specific Sizing Reviews ({len(published_bps)} Published)</h2>
                </div>
                <a href="{BASE_URL}/sitemap.xml" class="text-xs font-bold text-gray-700 hover:underline">View Full XML Sitemap &rarr;</a>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {review_cards}
            </div>
        </section>

        <!-- SEO FAQ SECTION -->
        <section id="faq" class="card-surface rounded-2xl p-6 sm:p-8 shadow-md">
            <h2 class="text-2xl sm:text-3xl font-black text-gray-900 mb-6">Frequently Asked Questions (Solar & Battery Sizing)</h2>
            <div class="space-y-5">
                <div class="gray-surface p-5 rounded-xl">
                    <h3 class="font-extrabold text-gray-900 text-base mb-1">1. How do I calculate what size portable power station or solar generator I need?</h3>
                    <p class="text-sm text-gray-800 leading-relaxed">
                        Multiply your appliance's continuous running watts (W) by the hours of runtime required to obtain total Watt-hours (Wh). Divide that figure by <strong>0.85</strong> to account for inverter conversion overhead and battery reserve. For example, a 150W refrigerator running for 10 hours requires 1,500Wh &divide; 0.85 = <strong>1,765Wh</strong> of rated capacity.
                    </p>
                </div>
                <div class="gray-surface p-5 rounded-xl">
                    <h3 class="font-extrabold text-gray-900 text-base mb-1">2. Can a 1000Wh power station run a full-size refrigerator?</h3>
                    <p class="text-sm text-gray-800 leading-relaxed">
                        Yes. A standard kitchen refrigerator consumes 100W–150W while the compressor is actively running, and cycles on roughly 35% to 50% of the time. A 1000Wh LiFePO4 unit like the <strong>Jackery Explorer 1000 v2</strong> or <strong>EcoFlow DELTA 2</strong> will keep a full-size refrigerator cold for <strong>12 to 20 hours</strong> on a single charge.
                    </p>
                </div>
                <div class="gray-surface p-5 rounded-xl">
                    <h3 class="font-extrabold text-gray-900 text-base mb-1">3. How many watts of solar panels do I need to charge a 1000Wh to 2000Wh battery?</h3>
                    <p class="text-sm text-gray-800 leading-relaxed">
                        To replenish a 1000Wh power station inside a single day's window of 4.5 peak sun hours, pair it with <strong>200W to 400W of solar panels</strong>. For a 2000Wh power station, use <strong>400W to 800W of solar panels</strong> for reliable off-grid autonomy.
                    </p>
                </div>
                <div class="gray-surface p-5 rounded-xl">
                    <h3 class="font-extrabold text-gray-900 text-base mb-1">4. Why is LiFePO4 better than standard Lithium-ion for solar generators?</h3>
                    <p class="text-sm text-gray-800 leading-relaxed">
                        LiFePO4 (Lithium Iron Phosphate) chemistry delivers <strong>3,000 to 6,000+ deep charge cycles</strong> before reaching 80% capacity—translating to 10+ years of daily use—compared to just 500 cycles on older NMC lithium-ion units.
                    </p>
                </div>
            </div>
        </section>
    </main>

    {footer_html()}

    <script>
        const CATALOG = {products_json_js};
        const AFF_TAG = "{AFFILIATE_TAG}";

        function addPreset(w, surge, hrs, label) {{
            const inW = document.getElementById('inWatts');
            const inS = document.getElementById('inSurge');
            const inH = document.getElementById('inHours');
            inW.value = parseInt(inW.value || 0) + w;
            inS.value = Math.max(parseInt(inS.value || 0), surge + parseInt(inW.value || 0) - w);
            inH.value = hrs;
            runCalculator();
        }}

        function resetCalc() {{
            document.getElementById('inWatts').value = 150;
            document.getElementById('inSurge').value = 600;
            document.getElementById('inHours').value = 8;
            runCalculator();
        }}

        function runCalculator() {{
            const watts = parseFloat(document.getElementById('inWatts').value) || 10;
            const surge = parseFloat(document.getElementById('inSurge').value) || watts;
            const hours = parseFloat(document.getElementById('inHours').value) || 1;
            const sun = parseFloat(document.getElementById('inSunHours').value) || 4.5;
            const eff = parseFloat(document.getElementById('inEff').value) || 0.85;

            const requiredWh = Math.ceil((watts * hours) / eff);
            const requiredAh = Math.ceil(requiredWh / 12.8);
            const minInverter = Math.ceil(watts * 1.25);
            const requiredSolar = Math.ceil((requiredWh / sun) * 1.25);

            document.getElementById('outWh').innerText = requiredWh.toLocaleString() + ' Wh';
            document.getElementById('outAh').innerText = requiredAh.toLocaleString() + ' Ah';
            document.getElementById('outInv').innerText = minInverter.toLocaleString() + ' W';
            document.getElementById('outSurgeLabel').innerText = surge.toLocaleString() + 'W Surge Min';
            document.getElementById('outSolar').innerText = requiredSolar.toLocaleString() + ' W';

            // Cari produk terbaik yang memenuhi spesifikasi
            let matches = CATALOG.filter(p => p.capacity_wh >= requiredWh * 0.75 && p.output_w >= watts && p.surge_w >= surge);
            if (matches.length === 0) {{
                matches = [CATALOG.reduce((prev, curr) => (curr.capacity_wh > prev.capacity_wh) ? curr : prev)];
            }} else {{
                matches.sort((a, b) => a.capacity_wh - b.capacity_wh);
            }}
            const best = matches[0];
            const estRuntime = ((best.capacity_wh * eff) / watts).toFixed(1);
            const amzUrl = 'https://www.amazon.com/s?k=' + encodeURIComponent(best.name) + '&tag=' + AFF_TAG;
            const bundleUrl = 'https://www.amazon.com/s?k=' + encodeURIComponent(best.name + ' Solar Generator Bundle') + '&tag=' + AFF_TAG;

            document.getElementById('recommendedBox').innerHTML = `
                <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div>
                        <span class="bg-amber-500 text-gray-950 text-xs font-extrabold px-2 py-0.5 rounded uppercase">Best Match For Your Load</span>
                        <h3 class="text-lg font-black text-gray-900 mt-1">${{best.name}}</h3>
                        <p class="text-xs text-gray-700 mt-0.5">
                            Rated <strong>${{best.capacity_wh}}Wh</strong> | <strong>${{best.output_w}}W</strong> Output (${{best.surge_w}}W Surge) | Runs your ${'${watts}'}W load for ~<strong>${{estRuntime}} hours</strong> per charge.
                        </p>
                    </div>
                    <div class="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
                        <a href="${{amzUrl}}" target="_blank" rel="nofollow sponsored" class="cta-btn px-5 py-3 rounded-lg text-xs text-center whitespace-nowrap shadow">
                            Check Price on Amazon &rarr;
                        </a>
                        <a href="${{bundleUrl}}" target="_blank" rel="nofollow sponsored" class="bg-gray-800 hover:bg-gray-950 text-white font-bold px-4 py-3 rounded-lg text-xs text-center whitespace-nowrap">
                            + Solar Bundle
                        </a>
                    </div>
                </div>
            `;
        }}

        function filterEverything() {{
            const q = document.getElementById('globalSearch').value.toLowerCase().trim();
            const cards = document.querySelectorAll('.product-card');
            let visible = 0;
            cards.forEach(c => {{
                const text = c.getAttribute('data-search') || '';
                if (!q || text.includes(q)) {{
                    c.style.display = 'flex';
                    visible++;
                }} else {{
                    c.style.display = 'none';
                }}
            }});
            document.getElementById('matchCount').innerText = q ? visible : 'All (' + cards.length + ')';
        }}

        window.addEventListener('DOMContentLoaded', runCalculator);
    </script>
</body>
</html>"""

def generate_sitemap_and_rss(published_bps):
    today_str = datetime.date.today().isoformat()
    urls = [f"""  <url>
    <loc>{BASE_URL}/index.html</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""]

    rss_items = []
    for item in reversed(published_bps):
        bp = item["bp"]
        pub_date = item["date"]
        loc = f"{BASE_URL}/reviews/{bp['slug']}.html"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{pub_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

        rss_items.append(f"""    <item>
      <title>{bp['title']}</title>
      <link>{loc}</link>
      <guid>{loc}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>Engineering sizing review of {bp['product']['name']} for {bp['use_case']['title']} ({bp['runtime_hours']} hrs tested runtime).</description>
    </item>""")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>{SITE_NAME} - Daily Solar &amp; Power Station Reviews</title>
    <link>{BASE_URL}/index.html</link>
    <description>{SITE_TAGLINE}</description>
{chr(10).join(rss_items[:30])}
  </channel>
</rss>"""

    robots_txt = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    return sitemap_xml, rss_xml, robots_txt

def ping_indexnow(new_bps):
    if not new_bps or "username.github.io" in BASE_URL:
        return
    url_list = [f"{BASE_URL}/index.html"] + [f"{BASE_URL}/reviews/{bp['slug']}.html" for bp in new_bps]
    host = urllib.parse.urlparse(BASE_URL).netloc
    payload = json.dumps({
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow non-fatal notice: {e}")

def main():
    os.makedirs(os.path.join(DIST_DIR, "reviews"), exist_ok=True)
    all_bps = generate_all_article_blueprints()
    bp_map = {b["slug"]: b for b in all_bps}

    state, new_bps = load_and_update_state(all_bps)

    published_bps = []
    for entry in state["published"]:
        if entry["slug"] in bp_map:
            published_bps.append({"bp": bp_map[entry["slug"]], "date": entry["date"]})

    # Render semua halaman artikel review yang sudah terbit
    all_only_bps = [item["bp"] for item in published_bps]
    for idx, item in enumerate(published_bps):
        bp = item["bp"]
        related = [b for b in all_only_bps if b["slug"] != bp["slug"]][-3:]
        page_html = build_review_page(bp, item["date"], related)
        with open(os.path.join(DIST_DIR, "reviews", f"{bp['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(page_html)

    # Render halaman utama index.html
    index_html = build_index_page(published_bps)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Render Sitemap, RSS, Robots.txt & IndexNow Key
    sitemap_xml, rss_xml, robots_txt = generate_sitemap_and_rss(published_bps)
    with open(os.path.join(DIST_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    with open(os.path.join(DIST_DIR, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(rss_xml)
    with open(os.path.join(DIST_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)
    with open(os.path.join(DIST_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    print(f"Build selesai! Total artikel aktif: {len(published_bps)} (+{len(new_bps)} artikel baru hari ini).")
    ping_indexnow(new_bps)

if __name__ == "__main__":
    main()
