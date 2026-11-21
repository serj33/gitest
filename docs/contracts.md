# Data contracts

## Fact
Facts are stored as JSON objects. Recommended structure:
```json
{
  "id": "fact-001",
  "type": "task",
  "task": "Confirmed activity from source text",
  "tool": ["Python"],
  "error": [],
  "quality_check": [],
  "discussion": [],
  "evidence_ids": ["source-001"],
  "sources": [{"id":"source-001","type":"vacancy","title":"Source title","url":"https://example.org"}]
}
```
Use only fields supported by actual evidence. `evidence_ids` should reference source identifiers.

## Persona
```json
{
  "persona_id": "generated",
  "role": "",
  "specialization": "",
  "main_tasks": [{"task":"", "tools":[], "evidence_ids":[]}],
  "tools": [],
  "evidence_ids": [],
  "limitations": [],
  "mode": "synthetic"
}
```

## API envelope
Current endpoints return direct JSON objects. The n8n workflows may use `{ok, mode, data, usage, error}` envelopes. The API client unwraps both forms.