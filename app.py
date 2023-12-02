from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import treasure_router

from core.db import Base, engine

huntreasure = FastAPI(title="Huntreasure API", debug=True)

huntreasure.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


huntreasure.include_router(treasure_router.router)

# 실행 명령어 디버깅용
# uvicorn app:huntreasure --reload
# --host 0.0.0.0 --port 80
# 파이썬 코드로 실행시
# if __name__ == "__main__":
#     uvicorn.run(fastapi_app
#                 , host = "0.0.0.0"
#                 , port = 80)