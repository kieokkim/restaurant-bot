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

과제2.
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

과제3.
    Restaurant Bot을 Streamlit Cloud에 배포하여 누구나 사용할 수 있게 만드세요.

배포 가이드
    Step 1: 리포지터리 준비
        코드가 GitHub 리포지터리에 있는지 확인하세요.
        모든 의존성이 포함된 requirements.txt 파일을 만드세요.
        API 키를 위한 .streamlit/secrets.toml을 만드세요 (커밋하지 마세요!)
    Step 2: Streamlit Cloud에 배포
        share.streamlit.io에 접속하세요.
        GitHub으로 로그인하세요.
        "New app"을 클릭하세요.
        리포지터리와 메인 파일을 선택하세요.
        Streamlit Cloud 대시보드에서 시크릿(OPENAI_API_KEY)을 추가하세요.
        배포하세요!
    Step 3: 배포된 앱 테스트
        디스코드 일상방에 링크를 공유하고, 다른 멤버 분들에게 테스트를 요청하세요.
        서로가 서로의 테스트를 도와주는 센스! 기대할게요 :)
        모든 에이전트와 handoff가 올바르게 작동하는지 확인하세요.
        가드레일이 정상적으로 동작하는지 확인하세요.

요구사항
    Restaurant Bot이 공개 URL로 배포 및 접속 가능해야 합니다.
    모든 기능이 작동해야 합니다:
        Triage → Menu/Order/Reservation/Complaints Handoff
        Input 및 Output Guardrails
        세션 내 메모리
    어떤 에이전트가 응답하고 있는지 명확히 표시하는 깔끔한 UI가 구현되어 있어야 합니다.