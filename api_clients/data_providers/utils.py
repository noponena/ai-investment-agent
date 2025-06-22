from typing import Any


def is_alpha_vantage_valid_response(response: Any) -> bool:
    """
    Returns True if the response does not contain Alpha Vantage error/notice keys.
    Deems responses invalid if any entry has 'Information', 'Note', or 'Error Message' in its 'raw' field.
    """
    error_keys = {"Information", "Note", "Error Message"}
    if not isinstance(response, list):
        return False
    for entry in response:
        raw = entry.get("raw", {})
        if not isinstance(raw, dict):
            continue
        if any(k in raw for k in error_keys):
            return False
    return True
