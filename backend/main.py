import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🎯 导入你刚才写的路由
from router.auth_router import router as auth_router
from router.shop_router import router as shop_router
from router.promotion_router import router as promotion_router
from router.product_router import router as product_router
from router.order_router import router as order_router
from router.system_router import router as system_router
from utils.logger_util import get_logger

# 获取日志记录器
logger = get_logger(__name__)

# 1. 初始化 FastAPI 应用
app = FastAPI(
    title="妙手 TikTok RPA",
    version="1.0.0"
)

# 2. 配置跨域 (非常重要！否则 Tauri/Vue 无法调用接口)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # 在生产环境建议限制为具体的本地地址
    allow_credentials=True,
    allow_methods=["*"],             # 允许所有方法 (GET, POST, etc.)
    allow_headers=["*"],             # 允许所有请求头
)

# 3. 注册路由模块
app.include_router(auth_router)
app.include_router(shop_router)
app.include_router(promotion_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(system_router)

# 启动事件处理
@app.on_event("startup")
async def startup_event():
    logger.info("妙手 TikTok RPA 后端服务启动成功")



# 4. 根路径检查
@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running"}

# 5. 启动入口
if __name__ == "__main__":
    # 配置启动参数
    # reload=True 表示代码修改后自动重启服务 (开发模式必备)
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=5000, 
        reload=False,
        log_level="info",  # 设置uvicorn日志级别为info
        access_log=True,    # 启用访问日志
        use_colors=True,    # 启用彩色日志输出
        log_config=None     # 禁用uvicorn默认日志配置
    )