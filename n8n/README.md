# n8n workflows

Импортируйте workflows из вашей локальной n8n-инстанции и настройте credentials Ollama.

## Webhook contract

### Persona Builder
`POST /webhook/persona`
```json
{"facts": []}
```
Ожидаемый ответ:
```json
{"ok":true,"mode":"live","data":{"persona":{}},"usage":{"calls_used":1},"error":null}
```

### AI Interviewer
`POST /webhook/633fd7b3-de53-4967-a744-a2c4c202a99b`
```json
{"message":"Начни интервью","history":[]}
```
Ожидаемый ответ: `data.question`.

### AI Expert
`POST /webhook/persona/respond`
```json
{"question":"...","persona":{},"facts":[],"history":[]}
```
Ожидаемый ответ: `data.answer`.

## Настройка
- Chat Model: Ollama, модель `qwen2.5:3b` (или другая доступная локальная модель).
- Webhook: POST, Respond = Using Respond to Webhook Node.
- Respond to Webhook: Respond With = JSON. Передавайте объект, а не `JSON.stringify()`.
- Для тестирования используйте Test URL и включите Listen for Test Event. Для Production URL workflow должен быть опубликован/активирован.

В репозитории пока лежат контракты и настройки интеграции. Экспортированные workflow JSON нужно добавлять сюда после проверки, чтобы не публиковать локальные credential IDs.