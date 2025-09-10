
# communities_store.py
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Set, Dict
import streamlit as st

@dataclass
class Community:
    id: str
    name: str
    type: str
    city: str
    state: str
    license_no: str | None = None
    bed_count: int | None = None
    vacancy: bool = False
    accepts_medicaid: str = "No"
    specialties: Set[str] = field(default_factory=set)
    highest_license: str | None = None
    languages: Set[str] = field(default_factory=set)
    amenities: Set[str] = field(default_factory=set)
    contacts: List[Dict] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict:
        d = asdict(self)
        for k in ("specialties", "languages", "amenities"):
            d[k] = sorted(list(d.get(k, [])))
        return d

def init():
    if "communities" not in st.session_state:
        st.session_state.communities: List[Community] = seed_communities()
    st.session_state.setdefault("community_shortlist", [])

def all() -> List[Community]:
    return st.session_state.get("communities", [])

def get(cid: str) -> Community | None:
    return next((c for c in all() if c.id == cid), None)

def upsert(c: Community):
    items = all()
    for i, x in enumerate(items):
        if x.id == c.id:
            items[i] = c
            break
    else:
        items.append(c)

def remove(cid: str):
    items = all()
    st.session_state.communities = [c for c in items if c.id != cid]

def search(query: str = "", facets: Dict | None = None) -> List[Community]:
    items = list(all())
    q = (query or "").strip().lower()
    if q:
        items = [c for c in items if q in c.name.lower() or q in c.city.lower() or q in c.state.lower()]
    f = facets or {}
    if t := f.get("type"):
        items = [c for c in items if c.type == t]
    if med := f.get("accepts_medicaid"):
        items = [c for c in items if c.accepts_medicaid == med]
    if hl := f.get("highest_license"):
        items = [c for c in items if (c.highest_license or "") == hl]
    return items

def seed_communities() -> List[Community]:
    return [
        Community(id="CM-1001", name="Oak Meadow", type="Assisted Living",
            city="Seattle", state="WA", license_no="AL12345", bed_count=80,
            vacancy=True, accepts_medicaid="0-3 Months",
            specialties={"Dementia"}, highest_license="RN, BSN",
            languages={"English","Spanish"},
            amenities={"Awake staff","Wound care","Insulin"},
            contacts=[{"name":"Jane Admin","role":"Marketing Director","phone":"555-1234","email":"jane@oakmeadow.com"}],
            notes="Pet-friendly; secured memory wing."
        ),
        Community(id="CM-1002", name="Harbor View AFH", type="Adult Family Home",
            city="Tacoma", state="WA", bed_count=6, vacancy=False,
            accepts_medicaid="No", specialties={"Mental Health"},
            highest_license="HCA", languages={"English"}, amenities={"Catheter","Hoyer lift"}
        )
    ]
