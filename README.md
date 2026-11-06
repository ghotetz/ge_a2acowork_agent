# 📌 Google A2A Multi Agent Cowork
> A2A, Multi Agent 간의 협업
> 
> 에이전트 카드를 확인하여 A2A 간 원격 호출 기능 제공

## ⚡ 주요 기능 (Features)
> 재무팀, 총무팀 에이전트 간의 협업으로 출장 경비 정보 확인

## 🛠 기술 스택 (Tech Stack)
- Google ADK, Python, A2A, Multi-Agent, Gemini-Enterprise, AI-Agents

## 💻 시작 가이드 (Getting Started)
- Google Cloud 인증
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project "gcp-project"
```

- Google ADK 설치
```bash
python -m venv .venv && source .venv/bin/activate
pip install "google-adk[gcp]" litellm
```

- Uvicorn a2a_app 구동
```bash
cd a2a_lab
set -a; source expense_agent/.env; set +a
uvicorn expense_agent.agent:a2a_app --host localhost --port 8001

# 다른 터미널에서 에이전트 카드 확인
curl http://localhost:8001/.well-known/agent-card.json
```

- ADK 검증 (Uvicorn a2a_app 구동 후 별도의 터미널에서 확인)
```bash
adk web --port 8000
```

- Agent 동작 확인
```bash
경비 에이전트(8001) 구동 상태에서 trip_coordinator 선택 후 확인
3박4일 도쿄 출장 준비해줘 > 체크리스트 로컬 도구, 예산 A2A 호출 확인
도쿄 호텔 1박 30만원인데 괜찮아? > 한도 초과와 사전 승인 안내
```

- 검증 완료 후 Gemini Enterprise 에 에이전트로 등록
```bash
adk deploy agent_engine \
  --project="프로젝트명" \
  --region="리전명" \
  --display_name="에이전트명" \
  "에이전트 프로젝트 경로"
```
# 📌 A2A Multi-Agent Cowork (Google ADK)

> Collaboration between multiple agents over the A2A (Agent2Agent) protocol.
>
> A local agent discovers a remote agent through its **agent card** and calls it over A2A.

## ⚡ Features

- A trip-planning agent (General Affairs) works with an expense agent (Finance) to prepare business trips
- Combines a local tool (trip checklist) with a remote A2A call (budget and expense-policy check)
- Flags over-limit expenses and explains when pre-approval is required

## 🛠 Tech Stack

- Google ADK, A2A protocol, Uvicorn, Python, Gemini Enterprise

## 💻 Getting Started

### 1. Authenticate to Google Cloud

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project "gcp-project"
```

### 2. Install Google ADK

```bash
python -m venv .venv && source .venv/bin/activate
pip install "google-adk[gcp]" litellm
```

### 3. Start the remote expense agent as an A2A server

```bash
cd a2a_lab
set -a; source expense_agent/.env; set +a
uvicorn expense_agent.agent:a2a_app --host localhost --port 8001

# In another terminal, check the agent card
curl http://localhost:8001/.well-known/agent-card.json
```

### 4. Run the trip agent locally (with the expense agent still running, in a separate terminal)

```bash
adk web --port 8000
```

### 5. Try it

With the expense agent running on port 8001, select `trip_coordinator` in the ADK web UI.

| Prompt | Expected behavior |
| --- | --- |
| Prepare a 4-day, 3-night business trip to Tokyo | Builds the checklist with a local tool and checks the budget via an A2A call |
| A Tokyo hotel is ₩300,000 per night — is that OK? | Flags that it exceeds the limit and explains the pre-approval process |

### 6. Deploy and register in Gemini Enterprise

```bash
adk deploy agent_engine \
  --project="<project-id>" \
  --region="<region>" \
  --display_name="<agent-name>" \
  "<path-to-agent-project>"
```

Once deployed to Vertex AI Agent Engine, register the agent in Gemini Enterprise.
