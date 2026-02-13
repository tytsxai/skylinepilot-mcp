#!/usr/bin/env python3
"""
Web 管理后台
FastAPI + WebSocket 实现实时状态推送
"""
import asyncio
import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

# 导入管理模块
from account_manager import account_manager
from proxy_manager import proxy_manager
from health_monitor import health_monitor
from stats_tracker import stats_tracker
from template_manager import template_manager
from scheduler import task_scheduler
from src.skylinepilot.interfaces.web_api.response import ok_response
from src.skylinepilot.interfaces.web_api.routes.marketing import router as marketing_router
from src.skylinepilot.interfaces.web_api.routes.accounts_read import router as accounts_read_router
from src.skylinepilot.interfaces.web_api.routes.accounts_write import router as accounts_write_router
from src.skylinepilot.interfaces.web_api.routes.templates import router as templates_router
from src.skylinepilot.interfaces.web_api.routes.proxies import router as proxies_router
from src.skylinepilot.interfaces.web_api.routes.health import router as health_router
from src.skylinepilot.interfaces.web_api.routes.stats import router as stats_router
from src.skylinepilot.interfaces.web_api.routes.logs import router as logs_router
from src.skylinepilot.interfaces.web_api.routes.schedules import router as schedules_router
from src.skylinepilot.interfaces.web_api.routes.batch import router as batch_router


# ============ FastAPI 应用 ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    # 初始化默认模板（如果没有模板）
    if not template_manager.list_templates():
        template_manager.add_template(
            "greeting",
            "问候消息",
            "你好 {name}，现在是 {time}，祝你今天愉快！",
            "general",
            ["name", "time"]
        )
        template_manager.add_template(
            "notification",
            "通知消息",
            "通知：{content}\n发送时间：{date} {time}",
            "general",
            ["content", "date", "time"]
        )
        print("✅ 已初始化默认消息模板")

    # 启动定时任务调度器
    scheduler_task = asyncio.create_task(task_scheduler.start())
    print("✅ 定时任务调度器已启动")

    # 启动健康监控
    await health_monitor.start_monitoring(interval=300)  # 每5分钟检查一次
    print("✅ 健康监控已启动")

    yield

    # 关闭时执行
    scheduler_task.cancel()
    health_monitor.stop_monitoring()
    print("🛴 定时任务调度器和健康监控已停止")


app = FastAPI(title="SkylinePilot MCP 增长控制台", lifespan=lifespan)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载前端控制台
app.mount("/console", StaticFiles(directory="console_ui"), name="console")
app.include_router(marketing_router)
app.include_router(accounts_read_router)
app.include_router(accounts_write_router)
app.include_router(templates_router)
app.include_router(proxies_router)
app.include_router(health_router)
app.include_router(stats_router)
app.include_router(logs_router)
app.include_router(schedules_router)
app.include_router(batch_router)


# ============ API 端点 ============

@app.get("/")
async def root():
    """重定向到管理页面"""
    return JSONResponse(content=ok_response({
        "message": "SkylinePilot MCP 控制台运行中",
        "url": "/console/dashboard.html"
    }))


# ============ WebSocket 实时推送 ============

class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """广播消息到所有连接"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 实时推送"""
    await manager.connect(websocket)

    try:
        # 启动后台任务，定期推送状态更新
        stop_event = asyncio.Event()

        async def broadcast_status():
            """定期广播状态"""
            while not stop_event.is_set():
                try:
                    # 获取账号列表
                    accounts = account_manager.list_accounts()

                    # 获取健康报告
                    health_report = health_monitor.get_health_report()

                    # 获取统计摘要
                    stats_summary = stats_tracker.get_summary()

                    # 广播状态
                    await manager.broadcast({
                        "type": "status_update",
                        "timestamp": datetime.now().isoformat(),
                        "accounts": accounts,
                        "health": health_report,
                        "stats": stats_summary
                    })

                    await asyncio.sleep(5)  # 每5秒更新一次
                except Exception as e:
                    print(f"广播错误: {e}")
                    await asyncio.sleep(5)

        # 启动广播任务
        broadcast_task = asyncio.create_task(broadcast_status())

        # 处理客户端消息
        while True:
            data = await websocket.receive_json()

            # 处理客户端请求
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        stop_event.set()
    except Exception as e:
        print(f"WebSocket 错误: {e}")
        manager.disconnect(websocket)
        stop_event.set()


# ============ 启动入口 ============

if __name__ == "__main__":
    # 确保目录存在
    os.makedirs("./runtime_data", exist_ok=True)
    os.makedirs("./console_ui", exist_ok=True)

    print("=" * 60)
    print("🚀 SkylinePilot MCP 增长控制台")
    print("=" * 60)
    print(f"📱 账号数量: {len(account_manager.accounts)}")
    print(f"🌐 全局代理: {'已设置' if proxy_manager.global_proxy else '未设置'}")
    print(f"🔧 独立代理: {len(proxy_manager.proxies)} 个")
    print("")
    print("🌐 管理界面: http://localhost:8080/console/dashboard.html")
    print("📡 API 文档: http://localhost:8080/docs")
    print("🔌 WebSocket: ws://localhost:8080/ws")
    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
