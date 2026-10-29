from fastapi import FastAPI
from routers import news

app = FastAPI()

@app.get("/")
async def hello():
    return {"msg":"hello"}

# 挂载路由
app.include_router(news.router)

