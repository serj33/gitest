import requests


class N8NClient:
    """HTTP client for the project's n8n webhooks."""

    def __init__(self, base_url="http://localhost:5678/webhook", timeout=120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.persona_url = f"{self.base_url}/persona"
        self.interviewer_url = f"{self.base_url}/633fd7b3-de53-4967-a744-a2c4c202a99b"
        self.expert_url = f"{self.base_url}/persona/respond"

    def _post(self, url, payload):
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("Превышено время ожидания ответа от n8n") from exc
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError("Не удалось подключиться к n8n. Проверь, запущен ли n8n") from exc
        except requests.exceptions.HTTPError as exc:
            raise RuntimeError(f"HTTP-ошибка n8n: {exc}") from exc
        except ValueError as exc:
            raise RuntimeError("n8n вернул некорректный JSON") from exc

        if isinstance(result, dict) and result.get("ok") is False:
            raise RuntimeError(f"Ошибка n8n: {result.get('error')}")
        return result

    def build_persona(self, facts):
        return self._post(self.persona_url, {"facts": facts})

    def get_question(self, message, history):
        return self._post(self.interviewer_url, {"message": message, "history": history})

    def ask_expert(self, question, persona, facts, history):
        return self._post(self.expert_url, {
            "question": question, "persona": persona, "facts": facts, "history": history
        })

    def get_facts(self, profession=None):
        return build_facts(profession)


n8n_client = N8NClient()
