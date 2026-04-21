import streamlit as st
from agents import function_tool, AgentHooks, Agent, Tool, RunContextWrapper
from models import RestaurantContext
import random
from datetime import datetime, timedelta

# =============================================================================
# MENU AGENT TOOLS
# =============================================================================

@function_tool
def get_menu(context: RestaurantContext) -> str:
    """Get the full restaurant menu."""
    return """
🍽️ TODAY'S MENU

[파스타]
- 까르보나라 - ₩18,000
- 알리오 올리오 - ₩16,000
- 토마토 파스타 - ₩15,000

[피자]
- 마르게리타 - ₩20,000
- 페퍼로니 - ₩22,000
- 콰트로 포르마지 - ₩24,000

[음료]
- 탄산음료 - ₩3,000
- 주스 - ₩4,000
- 와인 (글라스) - ₩8,000
    """.strip()


@function_tool
def get_menu_item_details(context: RestaurantContext, item_name: str) -> str:
    """
    Get detailed information about a specific menu item.

    Args:
        item_name: Name of the menu item
    """
    menu_details = {
        "까르보나라": {
            "ingredients": "스파게티, 판체타, 달걀, 파르미지아노, 후추",
            "allergens": "글루텐, 달걀, 유제품",
            "calories": "650kcal",
        },
        "마르게리타": {
            "ingredients": "토마토소스, 모짜렐라, 바질",
            "allergens": "글루텐, 유제품",
            "calories": "800kcal",
        },
    }

    item = menu_details.get(item_name, None)
    if not item:
        return f"'{item_name}' 메뉴 정보를 찾을 수 없어요."

    return f"""
🍴 {item_name} 상세정보
재료: {item['ingredients']}
알레르기: {item['allergens']}
칼로리: {item['calories']}
    """.strip()


@function_tool
def check_allergens(context: RestaurantContext, allergen: str) -> str:
    """
    Check which menu items contain a specific allergen.

    Args:
        allergen: Allergen to check (글루텐, 달걀, 유제품, 견과류 등)
    """
    allergen_map = {
        "글루텐": ["까르보나라", "알리오 올리오", "토마토 파스타", "마르게리타", "페퍼로니", "콰트로 포르마지"],
        "달걀": ["까르보나라"],
        "유제품": ["까르보나라", "마르게리타", "페퍼로니", "콰트로 포르마지"],
        "견과류": [],
    }

    items = allergen_map.get(allergen, [])
    if not items:
        return f"✅ '{allergen}' 알레르겐이 포함된 메뉴가 없어요."

    return f"⚠️ '{allergen}' 포함 메뉴:\n" + "\n".join(f"• {item}" for item in items)


# =============================================================================
# ORDER AGENT TOOLS
# =============================================================================

@function_tool
def place_order(context: RestaurantContext, items: str, table_number: int) -> str:
    """
    Place a food order for the customer.

    Args:
        items: Comma-separated list of ordered items
        table_number: Table number
    """
    order_id = f"ORD-{random.randint(10000, 99999)}"
    estimated_time = random.randint(15, 30)

    context.current_order = order_id

    return f"""
✅ 주문이 접수되었습니다!
📋 주문번호: {order_id}
🍽️ 주문 항목: {items}
🪑 테이블: {table_number}번
⏱️ 예상 시간: 약 {estimated_time}분
    """.strip()


@function_tool
def check_order_status(context: RestaurantContext, order_id: str) -> str:
    """
    Check the current status of an order.

    Args:
        order_id: Order ID to check
    """
    statuses = ["접수됨", "조리 중", "서빙 준비 중", "서빙 완료"]
    current_status = random.choice(statuses)

    return f"""
📦 주문 상태: {order_id}
🔄 현재 상태: {current_status}
    """.strip()


@function_tool
def cancel_order(context: RestaurantContext, order_id: str, reason: str) -> str:
    """
    Cancel an existing order.

    Args:
        order_id: Order ID to cancel
        reason: Reason for cancellation
    """
    return f"""
❌ 주문 취소 완료
📋 주문번호: {order_id}
📝 사유: {reason}
💳 결제 취소는 영업일 기준 1-2일 소요됩니다.
    """.strip()


# =============================================================================
# RESERVATION AGENT TOOLS
# =============================================================================

@function_tool
def make_reservation(
    context: RestaurantContext,
    date: str,
    time: str,
    party_size: int,
    name: str,
) -> str:
    """
    Make a table reservation.

    Args:
        date: Reservation date (YYYY-MM-DD)
        time: Reservation time (HH:MM)
        party_size: Number of people
        name: Name for the reservation
    """
    reservation_id = f"RES-{random.randint(10000, 99999)}"

    return f"""
✅ 예약이 완료되었습니다!
🔗 예약번호: {reservation_id}
👤 예약자: {name}
📅 날짜: {date}
🕐 시간: {time}
👥 인원: {party_size}명
📞 변경/취소: 방문 2시간 전까지 가능
    """.strip()


@function_tool
def check_availability(
    context: RestaurantContext, date: str, time: str, party_size: int
) -> str:
    """
    Check table availability for a specific date and time.

    Args:
        date: Date to check (YYYY-MM-DD)
        time: Time to check (HH:MM)
        party_size: Number of people
    """
    available = random.choice([True, True, True, False])

    if available:
        return f"✅ {date} {time}, {party_size}명 예약 가능합니다!"
    else:
        alt_times = ["18:00", "18:30", "20:00", "20:30"]
        return f"""
❌ {date} {time}는 예약이 마감되었습니다.
🕐 대안 시간: {', '.join(alt_times)}
        """.strip()


@function_tool
def cancel_reservation(
    context: RestaurantContext, reservation_id: str
) -> str:
    """
    Cancel an existing reservation.

    Args:
        reservation_id: Reservation ID to cancel
    """
    return f"""
❌ 예약 취소 완료
🔗 예약번호: {reservation_id}
📅 취소 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """.strip()


# =============================================================================
# AGENT HOOKS
# =============================================================================

class AgentToolUsageLoggingHooks(AgentHooks):

    async def on_tool_start(self,
        context: RunContextWrapper[RestaurantContext],
        agent: Agent[RestaurantContext],
        tool: Tool,
    ):
        with st.sidebar:
            st.write(f"⚒️ **{agent.name}** starting tool: `{tool.name}`")

    async def on_tool_end(self,
        context: RunContextWrapper[RestaurantContext],
        agent: Agent[RestaurantContext],
        tool: Tool,
        result: str,
    ):
        with st.sidebar:
            st.write(f"✅ **{agent.name}** used tool: `{tool.name}`")
            st.code(result)

    async def on_handoff(self,
        context: RunContextWrapper[RestaurantContext],
        agent: Agent[RestaurantContext],
        source: Agent[RestaurantContext],
    ):
        with st.sidebar:
            st.write(f"🔄 Handoff: **{source.name}** → **{agent.name}**")

    async def on_start(self,
        context: RunContextWrapper[RestaurantContext],
        agent: Agent[RestaurantContext],
    ):
        with st.sidebar:
            st.write(f"🚀 **{agent.name}** activated")

    async def on_end(self,
        context: RunContextWrapper[RestaurantContext],
        agent: Agent[RestaurantContext],
        output,
    ):
        with st.sidebar:
            st.write(f"🏁 **{agent.name}** completed")

# =============================================================================
# COMPLAINTS AGENT TOOLS
# =============================================================================

@function_tool
def submit_complaint(
    context: RestaurantContext,
    complaint_description: str,
    severity: str,
) -> str:
    """
    Submit and log a customer complaint.

    Args:
        complaint_description: Description of the complaint
        severity: Severity level (minor, serious, critical)
    """
    complaint_id = f"CMP-{random.randint(10000, 99999)}"

    return f"""
📝 Complaint Logged
🔗 Complaint ID: {complaint_id}
👤 Customer: {context.name}
⚠️ Severity: {severity.upper()}
📋 Description: {complaint_description}
⏱️ Our team will review this within 24 hours.
    """.strip()


@function_tool
def process_complaint_refund(
    context: RestaurantContext,
    refund_amount: float,
    reason: str,
) -> str:
    """
    Process a refund as compensation for a complaint.

    Args:
        refund_amount: Amount to refund
        reason: Reason for the refund
    """
    refund_id = f"REF-{random.randint(100000, 999999)}"

    return f"""
✅ Refund Processed
🔗 Refund ID: {refund_id}
👤 Customer: {context.name}
💰 Amount: ₩{refund_amount:,.0f}
📝 Reason: {reason}
⏱️ Processing time: 1-3 business days
    """.strip()


@function_tool
def apply_discount_coupon(
    context: RestaurantContext,
    discount_percentage: int,
    reason: str,
) -> str:
    """
    Apply a discount coupon to compensate for a minor complaint.

    Args:
        discount_percentage: Discount percentage (10, 20, 30, etc.)
        reason: Reason for the discount
    """
    coupon_code = f"SORRY{random.randint(1000, 9999)}"

    return f"""
🎟️ Discount Coupon Issued
👤 Customer: {context.name}
💸 Discount: {discount_percentage}% off next visit
🔑 Coupon Code: {coupon_code}
📝 Reason: {reason}
⏰ Valid for: 30 days
    """.strip()


@function_tool
def schedule_manager_callback(
    context: RestaurantContext,
    preferred_time: str,
    issue_summary: str,
) -> str:
    """
    Schedule a callback from the restaurant manager.

    Args:
        preferred_time: Customer's preferred callback time
        issue_summary: Brief summary of the issue
    """
    callback_id = f"CBK-{random.randint(10000, 99999)}"

    return f"""
📞 Manager Callback Scheduled
🔗 Callback ID: {callback_id}
👤 Customer: {context.name}
🕐 Preferred Time: {preferred_time}
📋 Issue: {issue_summary}
✅ A manager will contact you at your preferred time.
    """.strip()


@function_tool
def escalate_to_manager(
    context: RestaurantContext,
    issue_summary: str,
    severity: str,
) -> str:
    """
    Escalate a critical complaint to the manager immediately.

    Args:
        issue_summary: Summary of the critical issue
        severity: Severity level (serious, critical)
    """
    ticket_id = f"ESC-{random.randint(10000, 99999)}"

    return f"""
🚨 Complaint Escalated to Manager
🔗 Escalation ID: {ticket_id}
👤 Customer: {context.name}
⚡ Severity: {severity.upper()}
📋 Issue: {issue_summary}
⏱️ Expected response: within 1 hour
✅ A manager has been notified immediately.
    """.strip()