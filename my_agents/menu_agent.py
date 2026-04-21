from agents import Agent, RunContextWrapper
from models import RestaurantContext
from tools import get_menu, get_menu_item_details, check_allergens, AgentToolUsageLoggingHooks
from output_guardrails import restaurant_output_guardrail

def dynamic_menu_agent_instructions(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent[RestaurantContext],
):
    return f"""
    You are a Menu specialist helping {wrapper.context.name}.
    
    YOUR ROLE: Answer questions about the menu, ingredients, and allergens.
    
    MENU SUPPORT PROCESS:
    1. Retrieve the full menu when asked
    2. Provide detailed information about specific items
    3. Check allergen information when requested
    4. Make recommendations based on customer preferences
    
    ALWAYS:
    - Check allergens thoroughly for customers with dietary restrictions
    - Suggest alternatives if a requested item contains allergens
    - Highlight popular or recommended dishes
    - Be transparent about ingredients
    """

menu_agent = Agent(
    name="Menu Agent",
    instructions=dynamic_menu_agent_instructions,
    tools=[get_menu, get_menu_item_details, check_allergens],
    hooks=AgentToolUsageLoggingHooks(),
    output_guardrails=[restaurant_output_guardrail],
)