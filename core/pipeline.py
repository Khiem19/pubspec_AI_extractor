import json
import time
import hashlib
from typing import Any, Dict

from core.prompts import EXTRACT_PROMPT
from core.llm_client import llm_chat


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _extract_json_slice(text: str) -> str:
    """
    AI-only helper:
    - strips markdown code fences if present
    - returns the first JSON object slice if braces exist
    """
    t = text.strip()

    # strip markdown code fences
    if t.startswith("```"):
        lines = t.splitlines()
        if len(lines) >= 2:
            # drop first fence line (``` or ```json)
            lines = lines[1:]
            # drop last fence line if present
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
        t = "\n".join(lines).strip()

    # extract JSON object if present
    s = t.find("{")
    e = t.rfind("}")
    if s != -1 and e != -1 and e > s:
        return t[s:e + 1].strip()

    # otherwise return as-is (let json.loads fail and we report it)
    return t


def run_extraction(pubspec_text: str) -> Dict[str, Any]:
    """
    Fully AI test mode:
    - One LLM call
    - Expect valid JSON
    - No repair, no regex salvage, no schema validation
    """
    t0 = time.time()
    input_hash = _hash_text(pubspec_text)

    raw = llm_chat(EXTRACT_PROMPT.replace("{PUBSPEC_TEXT}", pubspec_text))
    raw_json = _extract_json_slice(raw)

    try:
        obj = json.loads(raw_json)
        return {
            "status": "ok",
            "input_hash": input_hash,
            "latency_sec": round(time.time() - t0, 3),
            "data": obj,
        }
    except json.JSONDecodeError as e:
        # AI-only: report failure and show model output for analysis
        return {
            "status": "failed",
            "input_hash": input_hash,
            "latency_sec": round(time.time() - t0, 3),
            "error": str(e),
            "raw_output": raw[:4000],  # keep bounded to avoid huge responses
        }
