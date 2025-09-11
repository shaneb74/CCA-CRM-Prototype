from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple, List

TZ = timezone.utc

@dataclass(frozen=True)
class SlaRule:
    name: str
    deadline_hours: int
    ref_stage: str
    description: str

STAGES: List[str] = [
    "lead_received",
    "lead_assigned",
    "initial_contact_attempted",
    "initial_contact_made",
    "consultation_scheduled",
    "assessment_started",
    "assessment_completed",
    "qualification_decision"
]

SLA: Dict[str, SlaRule] = {
    "lead_assigned": SlaRule("Assignment", 8, "lead_received",
                             "Assignment within same business day of lead received"),
    "initial_contact_attempted": SlaRule("1st Contact Attempt", 2, "lead_received",
                             "First attempt within 2 business hours of lead received"),
    "initial_contact_made": SlaRule("Initial Contact Made", 48, "lead_received",
                             "Consult scheduled within 2 days of lead creation"),
    "consultation_scheduled": SlaRule("Consult Scheduled", 48, "initial_contact_made",
                             "Consultation scheduled within 2 days of initial contact"),
    "assessment_started": SlaRule("Assessment Started", 72, "initial_contact_made",
                             "Start within 3 business days of initial contact"),
    "assessment_completed": SlaRule("Assessment Completed", 120, "consultation_scheduled",
                             "Complete within 5 business days of consultation"),
    "qualification_decision": SlaRule("Qualification Decision", 24, "assessment_completed",
                             "Decision within 1 business day of assessment completion"),
}

def _now() -> datetime:
    return datetime.now(TZ)

def ensure_intake(lead: dict) -> dict:
    lead.setdefault("intake", {})
    i = lead["intake"]
    i.setdefault("timestamps", {})
    i.setdefault("meta", {})
    i.setdefault("decision", None)
    if "lead_received" not in i["timestamps"]:
        i["timestamps"]["lead_received"] = _now().isoformat()
    return lead

def log_stage(lead: dict, stage: str, when: Optional[datetime] = None, meta: Optional[dict] = None):
    ensure_intake(lead)
    if stage not in STAGES:
        raise ValueError(f"Unknown stage {stage}")
    ts = when or _now()
    lead["intake"]["timestamps"][stage] = ts.isoformat()
    if meta:
        lead["intake"]["meta"].setdefault(stage, {}).update(meta)

def _get_ts(lead: dict, stage: str) -> Optional[datetime]:
    ensure_intake(lead)
    iso = lead["intake"]["timestamps"].get(stage)
    if not iso:
        return None
    try:
        return datetime.fromisoformat(iso)
    except Exception:
        return None

def stage_status(lead: dict, stage: str) -> Tuple[str, Optional[datetime], Optional[datetime]]:
    ensure_intake(lead)
    done_at = _get_ts(lead, stage)
    if done_at:
        return "done", done_at, None
    rule = SLA.get(stage)
    if not rule:
        return "pending", None, None
    ref_ts = _get_ts(lead, rule.ref_stage)
    if not ref_ts:
        return "pending", None, None
    due = ref_ts + timedelta(hours=rule.deadline_hours)
    now = _now()
    return ("due" if now <= due else "late"), None, due

def progress_percent(lead: dict) -> float:
    ensure_intake(lead)
    ts = lead["intake"]["timestamps"]
    done = sum(1 for s in STAGES if s in ts)
    return done / len(STAGES)

def summarize_intake(lead: dict) -> Dict[str, dict]:
    ensure_intake(lead)
    out = {}
    for s in STAGES:
        status, done_at, due_at = stage_status(lead, s)
        out[s] = {
            "status": status,
            "completed_at": done_at,
            "due_at": due_at,
            "sla": SLA[s].description if s in SLA else None,
            "label": stage_label(s),
        }
    return out

def stage_label(stage: str) -> str:
    mapping = {
        "lead_received": "Lead Received",
        "lead_assigned": "Lead Assigned",
        "initial_contact_attempted": "Initial Contact Attempted",
        "initial_contact_made": "Initial Contact Made",
        "consultation_scheduled": "Consultation Scheduled",
        "assessment_started": "Assessment Started",
        "assessment_completed": "Assessment Completed",
        "qualification_decision": "Qualification Decision",
    }
    return mapping.get(stage, stage.replace("_", " ").title())
