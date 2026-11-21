from backend.services.persona_validator import validate_persona


def test_invalid_evidence_is_removed_and_tasks_without_evidence_are_dropped():
    facts = [{"evidence_ids": ["source-1"]}]
    persona = {
        "main_tasks": [
            {"task": "Supported", "tools": ["Python"], "evidence_ids": ["source-1", "fake"]},
            {"task": "Unsupported", "tools": [], "evidence_ids": ["fake"]},
        ],
        "tools": ["Python", "Invented"],
        "evidence_ids": ["source-1", "fake"],
    }
    result = validate_persona(persona, facts)
    assert len(result["main_tasks"]) == 1
    assert result["main_tasks"][0]["evidence_ids"] == ["source-1"]
    assert result["evidence_ids"] == ["source-1"]
    assert result["tools"] == ["Python"]


def test_persona_text_is_parsed():
    facts = [{"evidence_ids": ["e1"]}]
    result = validate_persona({"text": '{"main_tasks": [{"task":"x", "tools":[], "evidence_ids":["e1"]}]}'}, facts)
    assert result["main_tasks"][0]["task"] == "x"
