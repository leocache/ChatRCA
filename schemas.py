from typing import List, Optional, Literal
from pydantic import BaseModel, Field

RootCauseCategory = Literal[
    "network",
    "resource",
    "application",
    "database",
    "middleware",
    "dependency",
    "configuration",
    "unknown"
]

class ServiceLocation(BaseModel):
    dataset: Optional[str] = None
    namespace: Optional[str] = None
    service: Optional[str] = None
    pod: Optional[str] = None
    container: Optional[str] = None
    node: Optional[str] = None
    ip: Optional[str] = None
    trace_service: Optional[str] = None
    trace_span: Optional[str] = None

class EvidenceItem(BaseModel):
    source_type: Literal["metric", "log", "trace", "architecture"]
    source_name: str
    abnormal_field: Optional[str] = None
    abnormal_value: Optional[str] = None
    reason: str

class ExpertFinding(BaseModel):
    expert_name: str
    root_cause_category: RootCauseCategory
    service_location: ServiceLocation
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[EvidenceItem] = []

class FinalDiagnosis(BaseModel):
    incident_id: Optional[str] = None
    root_cause_category: RootCauseCategory
    root_cause_detail: str
    service_location: ServiceLocation
    affected_service: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[EvidenceItem] = []
    expert_findings: List[ExpertFinding] = []