import os
from datetime import date, timedelta
from dotenv import load_dotenv

# 동일 디렉토리의 .env 파일 자동 로드
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from google.adk.agents import LlmAgent
#remote a2a agent to use sub agent, agentcard well known path
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH, RemoteA2aAgent

#expense agent default path
EXPENSE_A2A_BASE = os.getenv("EXPENSE_A2A_BASE", "http://localhost:8001")

#ga local tool, trip checklist
def make_trip_checklist(city: str, depart: str, nights: int, purpose: str) -> dict:
    """출장준비 체크리스트와 일정 생성. 일정 양식은 YYYY-MM-DD."""
    start = date.fromisoformat(depart)
    back = start + timedelta(days=nights)
    overseas = city not in ("부산", "대전", "광주", "대구", "제주")
    #trip prepare items
    items = ["출장 품의서 제출", "교통편 예약", "숙소 예약(규정 한도 내)", f"방문 목적 자료 준비: {purpose}"]

    if overseas:
        items += ["여권 유효기간 확인", "해외출장 보험 가입", "법인카드 해외 사용 등록"]

    return {"city": city, "depart": depart, "return": back.isoformat(), "checklist": items}

#expense agent remote sub agent apply
expense_agent = RemoteA2aAgent(
    name="expense_policy_agent",
    description="재무팀 에이전트. 출장비 한도, 일당, 출장 예싼 계싼, 경비 규정 질문 담당",
    #agent card (default paht + /.well-know/agent-card.json)
    agent_card=f"{EXPENSE_A2A_BASE}{AGENT_CARD_WELL_KNOWN_PATH}",
)

#ga trip root agent
root_agent = LlmAgent(
    name="trip_coordinator",
    model=os.environ["GEMINI_MODEL"],
    description="출장 일정, 체크리스트를 만들고 경비 한도는 재무팀 에이전트에 확인하는 총무 코디네이터",
    instruction=(
        "너는 총무팀 출장 준비 코디네이터로서, 일정과 체크리스트는 make_trip_checklist 로 만든다."
        "출장비 한도, 예산, 경비 규정은 직접 답하지 말고 반드시 expense_policy_agent 에 넘긴다."
        "최종 답변은 일정, 체크리스트, 예싼 한도를 한 번에 정리한다."
    ),
    tools=[make_trip_checklist],
    #delegationable sub agent
    sub_agents=[expense_agent],
)
