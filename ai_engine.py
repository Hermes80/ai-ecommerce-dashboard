import time
from ebay_api import get_active_listings, get_orders

def ai_main_loop():
    print("🤖 Hermes08 AI Engine is now running.")
    while True:
        try:
            listings = get_active_listings()
            orders = get_orders()

            print(f"📦 Active Listings: {len(listings)} | Orders: {len(orders)}")

            # Example AI logic placeholder
            for listing in listings:
                # Future: apply AI optimization
                pass

            time.sleep(300)  # wait 5 minutes before next sync

        except Exception as e:
            print("❌ AI Engine Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    ai_main_loop()
