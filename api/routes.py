import secrets
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from config.settings import settings
from notifications.maintenance import send_maintenance_notification
from notifications.outage import send_outage_notification
from notifications.resolution import send_resolution_notification
from utils.logger import get_logger

router = APIRouter(prefix="/notify", tags=["notifications"])
logger = get_logger("api")

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def _require_api_key(key: str = Security(_api_key_header)) -> None:
    """Reject requests that don't carry the configured API key."""
    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key not configured on server",
        )
    if not secrets.compare_digest(key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )


class OutageRequest(BaseModel):
    incident_id: str
    severity: str
    affected_system: str
    impact: str
    status: str
    start_time: str
    eta: str
    current_status: str
    workaround: str = ""
    incident_commander: str = ""
    recipient_group: Optional[str] = None


class MaintenanceRequest(BaseModel):
    maintenance_id: str
    affected_systems: List[str]
    scheduled_start: str
    scheduled_end: str
    description: str
    impact: str
    lead_engineer: str = ""
    rollback_plan: str = ""
    recipient_group: Optional[str] = None


class ResolutionRequest(BaseModel):
    incident_id: str
    affected_system: str
    resolved_at: str
    duration: str
    root_cause: str
    resolution_summary: str
    severity: str = "P2"
    incident_commander: str = ""
    follow_up_actions: str = ""
    recipient_group: Optional[str] = None


@router.post("/outage", dependencies=[Depends(_require_api_key)])
def notify_outage(req: OutageRequest):
    ok = send_outage_notification(**req.model_dump())
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to send outage notification")
    logger.info(f"API outage notification | {req.incident_id}")
    return {"status": "sent", "incident_id": req.incident_id}


@router.post("/maintenance", dependencies=[Depends(_require_api_key)])
def notify_maintenance(req: MaintenanceRequest):
    ok = send_maintenance_notification(**req.model_dump())
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to send maintenance notification")
    logger.info(f"API maintenance notification | {req.maintenance_id}")
    return {"status": "sent", "maintenance_id": req.maintenance_id}


@router.post("/resolution", dependencies=[Depends(_require_api_key)])
def notify_resolution(req: ResolutionRequest):
    ok = send_resolution_notification(**req.model_dump())
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to send resolution notification")
    logger.info(f"API resolution notification | {req.incident_id}")
    return {"status": "sent", "incident_id": req.incident_id}
