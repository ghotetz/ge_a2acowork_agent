import os
import sys
from dotenv import load_dotenv

# same dir .env auto load
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from google.adk.agents import LlmAgent
#adk agent to a2a svr app
from google.adk.a2a.utils.agent_to_a2a import to_a2a
#mcp to adk tools
from google.adk.tools.mcp_tool import MCPToolset
#child process run for local mcp
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
#child process parameters
from mcp import StdioServerParameters

RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expense_rules_mcp.py")

#expense agent define
root_agent = LlmAgent(
    name="expense_policy_agent",
    model=os.environ["GEMINI_MODEL"],
    description="출장비,경비 규정 한도를 안내하고 출장 예산을 계산하는 재무팀 에이전트",
    instruction=(
        "너는 재무팀 경비 규정 에이전트로서, 금액은 반드시 도구 결과로만 답하고 원 단위로 표기한다."
        "한도를 넘는 지출은 사전 승인이 필요하다고 알린다."
    ),
    #tool lits
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                #exepense_rules.mcp.py as child process
                server_params=StdioServerParameters(command=sys.executable, args=[RULES]),
                timeout=10,
            )
        )
    ]
)

#a2a svr app, with uvicorn agent card auto generated
#port should be the same with uvicorn
a2a_app = to_a2a(root_agent, port=8001)