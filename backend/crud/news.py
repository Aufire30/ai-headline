from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News

# 分类
async def get_categories(db:AsyncSession,skip:int = 0,limit:int = 100):
    temp = select(Category).offset(skip).limit(limit)
    result = await db.execute(temp)
    return result.scalars().all()

# 列表
async def get_news_list(db:AsyncSession,category_id:int,skip:int = 0,limit:int = 10):
    temp = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(temp)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int): # 查询指定分类下的总数量
    temp = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(temp)
    return result.scalar_one() # 只能有一个结果，否则报错

# 详情
async def get_news_detail(db:AsyncSession,news_id:int):
    temp = select(News).where(News.id == news_id)
    result = await db.execute(temp)
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
    temp = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(temp)
    await db.commit()

    # 检查数据库是否真的命中了数据(即浏览量是否更新成功)，命中则返回True
    return result.rowcount > 0

async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int = 5):
    # 推荐浏览量最高、发布时间最新的前5个新闻
    temp = (select(News).where(News.id != news_id,News.category_id == category_id)
                        .order_by(News.views.desc(),News.publish_time.desc()) # 默认升序，desc表示降序
                        .limit(limit))
    result = await db.execute(temp)

    # return result.scalars().all()

    related_news = result.scalars().all()
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "category": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]