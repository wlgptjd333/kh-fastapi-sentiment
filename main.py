from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sentiment.router import router as sentiment_router
from sentiment.db import Base, engine
from sentiment import models  # Base에 TextItem 테이블 등록
from sentiment.migrate_06 import upgrade_schema

app = FastAPI(title="FastAPI Sentiment CRUD")
upgrade_schema()  # 04 DB에 신규 필드 추가도 지원 (교육용)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(sentiment_router)

@app.get("/health", name="health")
def health():
    return {"status": "ok"}
