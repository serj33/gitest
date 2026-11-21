import json


def validate_persona(persona, facts):
    """Remove task evidence references that do not exist in the supplied facts."""
    if isinstance(persona, dict) and "data" in persona:
        data = persona.get("data") or {}
        persona = data.get("persona", persona)
    if isinstance(persona, dict) and isinstance(persona.get("text"), str):
        try:
            persona = json.loads(persona["text"])
        except json.JSONDecodeError as exc:
            raise ValueError("Persona text is not valid JSON") from exc
    if not isinstance(persona, dict):
        raise ValueError("Persona has invalid format")

    valid_ids = set()
    for fact in facts:
        if not isinstance(fact, dict):
            continue
        ids = fact.get("evidence_ids", [])
        if isinstance(ids, list):
            valid_ids.update(ids)
        if fact.get("evidence_id"):
            valid_ids.add(fact["evidence_id"])

    tasks = []
    for task in persona.get("main_tasks", []):
        if not isinstance(task, dict):
            continue
        ids = task.get("evidence_ids", [])
        verified = [item for item in ids if item in valid_ids] if isinstance(ids, list) else []
        if verified:
            task["evidence_ids"] = verified
            tasks.append(task)
    persona["main_tasks"] = tasks
    evidence = sorted({item for task in tasks for item in task.get("evidence_ids", [])})
    persona["evidence_ids"] = evidence
    persona["tools"] = sorted({tool for task in tasks for tool in task.get("tools", [])})
    return persona
