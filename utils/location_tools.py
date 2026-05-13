import re
from typing import Any, Dict, Optional


def normalize_service_location(
    dataset: str,
    service: Optional[str] = None,
    pod: Optional[str] = None,
    container: Optional[str] = None,
    node: Optional[str] = None,
    ip: Optional[str] = None,
    trace_service: Optional[str] = None,
    trace_span: Optional[str] = None,
    namespace: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "dataset": dataset,
        "namespace": namespace,
        "service": service,
        "pod": pod,
        "container": container,
        "node": node,
        "ip": ip,
        "trace_service": trace_service,
        "trace_span": trace_span,
    }


def infer_service_from_pod(pod_name: Optional[str]) -> Optional[str]:
    if not pod_name:
        return None

    service = pod_name.strip()
    # 去掉典型 deployment / rs 后缀
    service = re.sub(r"-[a-z0-9]{9,10}-[a-z0-9]{5}$", "", service)
    service = re.sub(r"-[a-z0-9]{5}$", "", service)
    return service


def remove_last_suffix(text: str) -> str:
    return re.sub(r"-[^-]*$", "", text)


def normalize_trainticket_pod_to_service(pod_name: Optional[str]) -> Optional[str]:
    if not pod_name:
        return None
    s = remove_last_suffix(remove_last_suffix(pod_name))
    return s


def build_observation_ticket(
    dataset: str,
    incident_id: str,
    fault_time: Optional[str] = None,
    fault_start_time: Optional[str] = None,
    fault_end_time: Optional[str] = None,
    fault_service: Optional[str] = None,
    fault_pod: Optional[str] = None,
    fault_message: Optional[str] = None,
):
    if dataset == "TrainTicket":
        normalized_service = fault_service or normalize_trainticket_pod_to_service(fault_pod)
    else:
        normalized_service = fault_service or infer_service_from_pod(fault_pod)

    return {
        "incident_id": incident_id,
        "dataset": dataset,
        "fault_time": fault_time,
        "fault_start_time": fault_start_time,
        "fault_end_time": fault_end_time,
        "fault_message": fault_message,
        "suspected_service_location": normalize_service_location(
            dataset=dataset,
            service=normalized_service,
            pod=fault_pod,
        ),
    }