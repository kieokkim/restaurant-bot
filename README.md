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

과제1.
    Restaurant Bot에 Guardrails와 Complaints Agent를 추가하세요!
    다음 기능을 추가하세요:
    Input Guardrails - 부적절하거나 주제에 벗어난 메시지 필터링
    Output Guardrails - 봇이 부적절한 응답을 하지 않도록 보장
    Complaints Agent - 불만족한 고객을 세심하게 처리하고 해결책 제시
요구사항
    다음을 거부하는 Input Guardrails를 추가하세요:
        주제에 벗어난 질문 (레스토랑과 관련 없는 내용)
        부적절한 언어
    다음을 보장하는 Output Guardrails를 추가하세요:
        전문적이고 정중한 응답
        내부 정보를 노출하지 않음
    다음과 같은 Complaints Agent를 만드세요:
        고객의 불만을 공감하며 인정
        해결책 제시 (환불, 할인, 매니저 콜백)
        심각한 문제를 적절히 에스컬레이션