import sys
import os

# Configure stdout for emojis and unicode characters
sys.stdout.reconfigure(encoding='utf-8')

from omnimoney.daily_scheduler import DailyScheduler

def main():
    print("=" * 60)
    print(" 🚀 OMNIMONEY OS - DAILY CYCLE AUTOMATION")
    print("=" * 60)
    print("Initializing daily automation sequence...\n")
    
    scheduler = DailyScheduler()
    try:
        summary = scheduler.run_daily_cycle()
        print(f"✅ Daily cycle completed successfully for {summary['date']}")
        print(f"\n📂 Generated Files:")
        print(f"  - Morning Brief: {summary['brief_file']}")
        print(f"  - Prospect Hit List: {summary['hit_list_file']} ({summary['prospects_mined']} prospects)")
        print(f"  - Outreach Scripts: {summary['scripts_file']}")
        print("\nReady for execution. Let's go!")
    except Exception as e:
        print(f"❌ Error during daily cycle: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
