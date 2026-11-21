import json
import requests
import streamlit as st

API_URL = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="ModeusAristo", page_icon="🧭", layout="wide")
st.title("ModeusAristo")
st.caption("Исследование профессий · факты · синтетическая персона · интервью")


def api(method, path, **kwargs):
    try:
        response = requests.request(method, f"{API_URL.rstrip('/')}{path}", timeout=130, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Ошибка API: {exc}")
        return None


tabs = st.tabs(["Факты", "Персона", "Интервью", "AI Expert"])

with tabs[0]:
    st.subheader("Факты для исследования")
    profession = st.text_input("Профессия", "Python Developer", key="profession")
    current = api("GET", "/facts", params={"profession": profession})
    facts = current.get("facts", []) if current else []
    st.write(f"Сохранено фактов: {len(facts)}")
    st.json(facts)
    facts_json = st.text_area("Добавить/заменить facts (JSON-массив)", value="[]", height=180)
    if st.button("Сохранить facts", key="save_facts"):
        try:
            parsed = json.loads(facts_json)
            if not isinstance(parsed, list):
                st.error("Нужно передать JSON-массив")
            else:
                result = api("POST", "/facts", json={"facts": parsed, "profession": profession})
                if result:
                    st.success(f"Сохранено: {result.get('count', 0)} фактов")
        except json.JSONDecodeError as exc:
            st.error(f"Некорректный JSON: {exc}")

with tabs[1]:
    st.subheader("Создание синтетической персоны")
    if st.button("Создать персону", type="primary"):
        result = api("POST", "/persona/build", params={"profession": profession})
        if result:
            st.session_state.persona = result.get("persona")
            st.success("Персона создана")
    saved = api("GET", "/persona")
    persona = st.session_state.get("persona") or (saved.get("persona") if saved else None)
    if persona:
        st.json(persona)

with tabs[2]:
    st.subheader("AI Interviewer")
    history_result = api("GET", "/interview/history")
    history = history_result.get("history", []) if history_result else []
    for item in history:
        with st.chat_message("user" if item.get("role") == "user" else "assistant"):
            st.write(item.get("content", ""))
    message = st.chat_input("Ответ или старт интервью…", key="interview_input")
    if message:
        result = api("POST", "/interview", json={"message": message})
        if result:
            st.rerun()
    if st.button("Очистить интервью"):
        api("DELETE", "/interview/history")
        st.rerun()

with tabs[3]:
    st.subheader("AI Expert")
    history_result = api("GET", "/expert/history")
    history = history_result.get("history", []) if history_result else []
    for item in history:
        with st.chat_message("user" if item.get("role") == "user" else "assistant"):
            st.write(item.get("content", ""))
    question = st.chat_input("Задайте вопрос синтетическому эксперту…", key="expert_input")
    if question:
        result = api("POST", "/expert", json={"question": question})
        if result:
            st.rerun()
    if st.button("Очистить диалог эксперта"):
        api("DELETE", "/expert/history")
        st.rerun()
