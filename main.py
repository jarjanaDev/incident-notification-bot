"""
Incident Notification Bot — Entry Point

Usage:
  python main.py --mode cli          # Interactive CLI demo
  python main.py --mode api          # Start FastAPI server
  python main.py --mode outage       # Send sample outage notification
  python main.py --mode maintenance  # Send sample maintenance notification
  python main.py --mode resolution   # Send sample resolution notification
"""

import argparse
import sys

from utils.logger import get_logger

logger = get_logger("main")


def run_api():
    import uvicorn
    from fastapi import FastAPI
    from api.routes import router
    from config.settings import settings

    app = FastAPI(
        title="Incident Notification Bot",
        description="REST API for triggering IT incident notifications",
        version="1.0.0",
    )
    app.include_router(router)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "incident-notification-bot"}

    logger.info(f"Starting API on {settings.api_host}:{settings.api_port}")
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)


def demo_outage():
    from notifications.outage import send_outage_notification

    logger.info("Sending demo outage notification...")
    result = send_outage_notification(
        incident_id="INC0043821",
        severity="P1",
        affected_system="Payment Processing Service",
        impact="Users unable to complete transactions",
        status="ACTIVE — Under Investigation",
        start_time="13:45 IST",
        eta="14:30 IST",
        current_status="Investigation ongoing. Payment team and infra team engaged.",
        workaround="Manual processing via backup channel.",
        incident_commander="Santosh Dharma",
    )
    print("Outage notification sent." if result else "Send failed — check SMTP config and logs.")


def demo_maintenance():
    from notifications.maintenance import send_maintenance_notification

    logger.info("Sending demo maintenance notification...")
    result = send_maintenance_notification(
        maintenance_id="MNT0001234",
        affected_systems=["Database Cluster", "Auth Service"],
        scheduled_start="2026-06-10 02:00 IST",
        scheduled_end="2026-06-10 04:00 IST",
        description="Database version upgrade and index optimization.",
        impact="Auth service intermittently unavailable during window.",
        lead_engineer="Santosh Dharma",
        rollback_plan="Restore from pre-maintenance snapshot if upgrade fails.",
    )
    print("Maintenance notification sent." if result else "Send failed — check SMTP config and logs.")


def demo_resolution():
    from notifications.resolution import send_resolution_notification

    logger.info("Sending demo resolution notification...")
    result = send_resolution_notification(
        incident_id="INC0043821",
        affected_system="Payment Processing Service",
        resolved_at="14:25 IST",
        duration="40 minutes",
        root_cause="Database connection pool exhaustion due to unoptimized query introduced in v2.3.1.",
        resolution_summary="Rolled back v2.3.1 deployment. Connection pool restored. All transactions processing normally.",
        severity="P1",
        incident_commander="Santosh Dharma",
        follow_up_actions="1. Query optimization by 2026-06-10\n2. Add connection pool monitoring alert\n3. PIR scheduled for 2026-06-09",
    )
    print("Resolution notification sent." if result else "Send failed — check SMTP config and logs.")


def run_cli():
    print("\nIncident Notification Bot")
    print("=" * 40)
    print("1. Send outage notification (demo)")
    print("2. Send maintenance notification (demo)")
    print("3. Send resolution notification (demo)")
    print("4. Start REST API server")
    print("0. Exit")

    choice = input("\nSelect option: ").strip()
    if choice == "1":
        demo_outage()
    elif choice == "2":
        demo_maintenance()
    elif choice == "3":
        demo_resolution()
    elif choice == "4":
        run_api()
    elif choice == "0":
        sys.exit(0)
    else:
        print("Invalid option.")


def main():
    parser = argparse.ArgumentParser(description="Incident Notification Bot")
    parser.add_argument(
        "--mode",
        choices=["cli", "api", "outage", "maintenance", "resolution"],
        default="cli",
        help="Run mode (default: cli)",
    )
    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "outage":
        demo_outage()
    elif args.mode == "maintenance":
        demo_maintenance()
    elif args.mode == "resolution":
        demo_resolution()
    else:
        run_cli()


if __name__ == "__main__":
    main()
