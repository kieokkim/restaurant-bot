import streamlit as st
from openai import OpenAI
import os

api_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

import asyncio
from agents import Agent, Runner, SQLiteSession, InputGuardrailTripwireTriggered
from models import RestaurantContext
from my_agents.triage_agent import triage_agent

db_path = os.path.join("/tmp", "restaurant-bot-memory.db")

### 한번 생성한 세션은 계속 유지
if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        db_path,
    )
session = st.session_state["session"]

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent

### paint_history
async def paint_history():
    messages = await session.get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"])

asyncio.run(paint_history())


if "restaurant_ctx" not in st.session_state:
    st.session_state["restaurant_ctx"] = RestaurantContext(
        customer_id=1,
        name="guest",
    )

if not asyncio.run(session.get_items()):
    with st.chat_message("ai"):
        st.write("안녕하세요 레스토랑 챗봇입니다. 무엇을 도와드릴까요?")

### run_agent
async def run_agent(message):
    restaurant_ctx = st.session_state["restaurant_ctx"]

    with st.chat_message("ai"):
        status_placeholder = st.empty()
        text_placeholder = st.empty()
        response = ""

        st.session_state["text_placeholder"] = text_placeholder

        try:
            stream = Runner.run_streamed(triage_agent, message, session=session, context=restaurant_ctx)

            async for event in stream.stream_events():
                if event.type == "raw_response_event":
                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response)

                elif event.type == "agent_updated_stream_event":
                    if st.session_state["agent"].name != event.new_agent.name:
                        status_placeholder.info(f"🔄 **{st.session_state['agent'].name}** → **{event.new_agent.name}**")
                        st.session_state["agent"] = event.new_agent
                        text_placeholder = st.empty()
                        response = ""

        except InputGuardrailTripwireTriggered:
            st.write("그 내용은 제가 도와드릴 수 없어요.")

message = st.chat_input("챗봇에게 물어볼 내용을 적어주세요.")


if message:
    if "text_placeholder" in st.session_state:
        st.session_state["text_placeholder"].empty()

    if message:
        with st.chat_message("human"):
            st.write(message)

        asyncio.run(run_agent(message))

with st.sidebar:
    reset = st.button("🔄 Reset Memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))
