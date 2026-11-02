# FastAPI Sentiment

Hugging Face 감정분석 모델을 FastAPI에 연결하는 교육 실습 (교재 `FastAPI_HuggingFace/LLM` 02 → 04 → 06).

| 태그 | 내용 |
|---|---|
| `step-02` | `/predict/`: 입력 → 모델 추론 → 화면 |
| `step-04` | `/new/`, `/items/`: SQLite 저장, 목록·상세·수정·삭제 |
| `step-06` | Redis·Celery로 `/new/` 분석을 Worker에서 처리, 결과 캐시 |

## 실행 (터미널 3개)

Docker Desktop을 먼저 켠다.
Redis 주소는 `.env`에서 읽는다 (Git에 올리지 않음). 처음이면 `cp .env.example .env` 후 값을 채운다.

```bash
cd ~/fastapi_sentiment && docker compose up -d
```

```bash
cd ~/fastapi_sentiment && source .venv/bin/activate && celery -A sentiment.celery_app:celery_app worker --loglevel=info --pool=solo
```

```bash
cd ~/fastapi_sentiment && source .venv/bin/activate && python -m uvicorn main:app --reload
```

- 동기: http://127.0.0.1:8000/predict/
- 비동기: http://127.0.0.1:8000/new/
- 목록: http://127.0.0.1:8000/items/

## 테스트

```bash
python -m pytest -q
```

테스트는 실제 `sentiment.db`에 테스트 글을 남긴다.

## 측정 결과 (RTX 3060)

| 항목 | 시간 |
|---|---:|
| `POST /new/` 응답 | 0.02초 |
| 첫 분석 완료 (Worker 모델 로딩) | 약 6초 |
| 같은 문장 재분석 (캐시) | 0.02초 |
| `POST /predict/` 첫 요청 / 다음 요청 | 1.4초 / 0.005초 |
