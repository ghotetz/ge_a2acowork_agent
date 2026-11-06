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
gcloud config set project ax-gemini-lab
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
