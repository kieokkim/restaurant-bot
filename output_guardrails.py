from agents import Agent, output_guardrail, Runner, RunContextWrapper, GuardrailFunctionOutput
from models import OutputGuardRailOutput, RestaurantContext

restaurant_output_guardrail_agent = Agent(
    name="Restaurant Bot Guardrail",
    instructions="""
    You are a quality checker for a restaurant chatbot's responses.
    
    Evaluate the response strictly based on these two criteria:
    
    1. is_violation (True ONLY if):
    - Response reveals internal system details (agent names, tool names, code snippets)
    - Response exposes other customers' personal information
    - Response contains business-sensitive pricing strategies
    - In ALL other cases, set is_violation=False
    
    2. is_professional (False ONLY if):
    - Response contains profanity or offensive language
    - Response is rude or dismissive to the customer
    - In ALL other cases, set is_professional=True
    
    IMPORTANT:
    - Normal restaurant responses (menu info, orders, reservations) should ALWAYS pass
    - Default to is_violation=False and is_professional=True when in doubt
    - Only flag clear and obvious violations
    """,
    output_type=OutputGuardRailOutput,
)


@output_guardrail
async def restaurant_output_guardrail(
    wrapper: RunContextWrapper[RestaurantContext],
    agent: Agent, 
    output: str,
):
    result = await Runner.run(
        restaurant_output_guardrail_agent,
        output,
        context=wrapper.context,
    )

    validation = result.final_output

    triggered = (
        validation.is_violation
        or not validation.is_professional
    )

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )