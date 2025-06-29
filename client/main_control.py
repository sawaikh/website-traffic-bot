import requests
import json

from config import PANEL_IP

def run_task():
    url = input("🔗 Enter website URL: ")
    duration = input("⏳ Enter time in seconds to stay on site: ")
    click = input("🖱️ Click on ads? (yes/no): ")

    payload = {
        "url": url,
        "duration": duration,
        "click_ads": click
    }

    try:
        res = requests.post(f"http://{PANEL_IP}:8000/run_task", json=payload)
        if res.status_code == 200:
            print("✅ Task sent to VPS")
        else:
            print("❌ Failed to send task.")
    except Exception as e:
        print("❌ Error:", e)

def show_status():
    try:
        res = requests.get(f"http://{PANEL_IP}:8000/vps_status")
        data = res.json()
        online = len(data)
        print(f"🟢 Online: {online} VPS")
        for ip in data:
            print(" -", ip)
    except Exception as e:
        print("❌ Status check error:", e)

def update_script():
    try:
        res = requests.post(f"http://{PANEL_IP}:8000/update_script")
        print("📦 Update command sent to all VPS")
    except Exception as e:
        print("❌ Update error:", e)

while True:
    print("\n🧠 OPTIONS:")
    print("1️⃣  Run Task")
    print("2️⃣  Show VPS Online Status")
    print("3️⃣  Auto-Update Bot Script")
    print("0️⃣  Exit")

    choice = input("👉 Enter choice: ")
    if choice == "1":
        run_task()
    elif choice == "2":
        show_status()
    elif choice == "3":
        update_script()
    elif choice == "0":
        break
    else:
        print("❌ Invalid choice.")
