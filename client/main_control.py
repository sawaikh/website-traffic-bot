import requests
import time

from config import PANEL_IP

BASE_URL = f"http://{PANEL_IP}:8000"

def run_task():
    url = input("🔗 Website URL: ")
    duration = input("⏱️ Time on page (seconds): ")
    click_ad = input("🖱️ Click on Ad? (yes/no): ").lower()

    task_data = {
        "url": url,
        "duration": int(duration),
        "click_ad": click_ad == "yes"
    }

    print("🚀 Sending task to all VPS...")
    try:
        res = requests.post(f"{BASE_URL}/run_task", json=task_data)
        print("✅ Task result:")
        print(res.json())
    except Exception as e:
        print("❌ Error sending task:", e)

def check_status():
    try:
        res = requests.get(f"{BASE_URL}/vps_status")
        data = res.json()
        print(f"🟢 Online: {data['online']} | 🔴 Offline: {data['offline']} | Total: {data['total']}")
    except Exception as e:
        print("❌ Status check error:", e)

def update_script():
    try:
        res = requests.post(f"{BASE_URL}/update_script")
        print("📦 Update started on all VPS.")
    except Exception as e:
        print("❌ Update error:", e)

def main():
    while True:
        print("\n🧠 OPTIONS:")
        print("1️⃣  Run Task")
        print("2️⃣  Show VPS Online Status")
        print("3️⃣  Update All VPS Scripts")
        print("0️⃣  Exit")
        choice = input("👉 Enter choice: ")

        if choice == "1":
            run_task()
        elif choice == "2":
            check_status()
        elif choice == "3":
            update_script()
        elif choice == "0":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
