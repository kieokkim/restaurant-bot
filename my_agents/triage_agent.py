from dis import Instruction
from doctest import OutputChecker
import streamlit as st
from agents import Agent, Runner, handoff, RunContextWrapper, input_guardrail, GuardrailFunctionOutput
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters
from streamlit.cursor import RunningCursor

from models import RestaurantContext, InputGuardRailOutput, HandoffData

from my_agents.menu_agent import menu_agent
from my_agents.order_agent import order_agent
from my_agents.reservation_agent import reservation_agent

input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
    Ensure the user's request specifically pertains to restaurant-related topics such as:
    menu inquiries, ingredients, allergens, food orders, or table reservations.
    
    If the request is off-topic, return a reason for the tripwire.
    You can make small conversation with the user, especially at the beginning of the conversation,
    but don't help with requests that are not related to restaurant services.
    """,
    output_type=InputGuardRailOutput
)

@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
    input: str,
):
    result = await Runner.run(input_guardrail_agent, input, context=wrapper.context,)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_off_topic,
    )


def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
        {RECOMMENDED_PROMPT_PREFIX}

    You are a restaurant assistant. You ONLY help customers with menu inquiries, food orders, and table reservations.
    You call customers by their name.

    The customer's name is {wrapper.context.name}.

    YOUR MAIN JOB: Understand the customer's need and route them to the right specialist.

    ISSUE CLASSIFICATION GUIDE:

    🍽️ MENU - Route here for:
    - Questions about menu items, ingredients, prices
    - Allergen and dietary restriction inquiries
    - Recommendations and popular dishes
    - "What's on the menu?", "Does this contain nuts?", "What do you recommend?"

    📋 ORDER - Route here for:
    - Placing new food orders
    - Checking order status
    - Cancelling or modifying orders
    - "I'd like to order", "Where is my food?", "Cancel my order"

    📅 RESERVATION - Route here for:
    - Making table reservations
    - Checking availability
    - Cancelling or modifying reservations
    - "I'd like to book a table", "Is there availability?", "Cancel my reservation"

    CLASSIFICATION PROCESS:
    1. Greet the customer warmly by name
    2. Listen to the customer's request
    3. Classify into ONE of the three categories above
    4. Explain the routing: "I'll connect you with our [category] specialist"
    5. Route to the appropriate specialist agent

    SPECIAL HANDLING:
    - Multiple requests: Handle the most urgent first
    - Unclear requests: Ask 1 clarifying question before routing
    - Always be friendly and welcoming
    """


def handle_handoff(
    wrapper:RunContextWrapper[RestaurantContext],
    input_data:HandoffData
):
    with st.sidebar:
        st.write(
            f"""Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.issue_type}
            Description: {input_data.issue_description}
        """
        )
    pass

def make_handoff(agent):
    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    input_guardrails=[off_topic_guardrail],
    handoffs=[
        make_handoff(menu_agent),
        make_handoff(order_agent),
        make_handoff(reservation_agent),
    ]
)