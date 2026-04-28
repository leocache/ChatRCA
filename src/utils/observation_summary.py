from typing import Any, Dict, List


def summarize_log_output(log_text: str) -> List[Dict[str, Any]]:
    if not log_text or not log_text.strip():
        return []

    return [{
        "source_type": "log",
        "source_name": "processed_log",
        "abnormal_field": "ERROR rows",
        "abnormal_value": "non-empty",
        "reason": "Filtered log contains error records"
    }]


def summarize_trace_output(trace_text: str) -> List[Dict[str, Any]]:
    if not trace_text or not trace_text.strip():
        return []

    return [{
        "source_type": "trace",
        "source_name": "processed_trace",
        "abnormal_field": "duration",
        "abnormal_value": "threshold exceeded",
        "reason": "Filtered trace contains slow spans"
    }]


def summarize_metric_output(metric_data: Any) -> List[Dict[str, Any]]:
    result = []

    if isinstance(metric_data, dict):
        for name, content in metric_data.items():
            if content and content.strip():
                result.append({
                    "source_type": "metric",
                    "source_name": name,
                    "abnormal_field": "metric rows",
                    "abnormal_value": "non-empty",
                    "reason": f"Metric file {name} contains candidate abnormal rows"
                })
    elif isinstance(metric_data, str) and metric_data.strip():
        result.append({
            "source_type": "metric",
            "source_name": "processed_metric",
            "abnormal_field": "metric rows",
            "abnormal_value": "non-empty",
            "reason": "Filtered metric contains candidate abnormal rows"
        })

    return result