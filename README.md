과제1.
    다음 에이전트를 갖춘 Restaurant Bot을 구축하세요:
    Triage Agent - 고객이 무엇을 원하는지 파악
    Menu Agent - 메뉴, 재료, 알레르기 관련 질문에 답변
    Order Agent - 주문을 받고 확인
    Reservation Agent - 테이블 예약 처리
요구사항
    OpenAI Agents SDK의 handoff 기능을 사용하세요.
    Triage 에이전트가 요청에 맞는 전문 에이전트로 라우팅해야 합니다.
    각 에이전트는 역할에 맞는 명확한 지시사항을 가져야 합니다.
    UI에 handoff가 일어나는 것을 표시하세요 ("메뉴 전문가에게 연결합니다...").

예시 상호작용
    User: 예약을 하고 싶어
    Triage: 예약 담당에게 연결해 드릴게요...
    [Reservation Agent로 handoff]
    Reservation: 예약을 도와드리겠습니다! 인원수와 희망 날짜를 알려주세요.
    User: 아, 그전에 채식 메뉴 있는지 알려줘
    [Menu Agent로 handoff]
    Menu: 네! 여러 가지 채식 메뉴가 있습니다...