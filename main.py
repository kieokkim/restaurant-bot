from openai import OpenAI
client = OpenAI(api_key=st.secrets[f"OPENAI_API_KEY"])

import asyncio
import streamlit as st
from agents import Agent, Runner, SQLiteSession, InputGuardrailTripwireTriggered
from models import RestaurantContext
from my_agents.triage_agent import triage_agent

restaurant_ctx = RestaurantContext(
    customer_id=1,
    name="nico",
)

### 한번 생성한 세션은 계속 유지
if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "restaurant-bot-memory.db",
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


### run_agent
async def run_agent(message):
    with st.chat_message("ai"):
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
                        st.write(f"🤖 transfered from {st.session_state['agent'].name} to {event.new_agent.name}")

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
