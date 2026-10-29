# 模块化路由
from fastapi import APIRouter

# 创建APIRouter实例
router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0,limit: int = 100):
    return {
        "code":200,
        "message":"success",
        "data":"新闻分类列表"
    }