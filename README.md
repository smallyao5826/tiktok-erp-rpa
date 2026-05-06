# 妙手 TikTok RPA

一个基于 FastAPI + Vue 3 + Tauri 构建的 TikTok 店铺自动化管理工具，提供促销活动管理、订单统计、店铺管理等核心功能。

## ✨ 核心功能

### 🔐 认证管理
- **全自动 OCR 登录** - 自动识别验证码完成登录
- **Cookie 持久化** - 登录状态自动保存到本地数据库
- **账户信息查询** - 获取当前登录账户信息

### 🏪 店铺管理
- 获取当前账号绑定的所有店铺列表
- 查询单个店铺的详细信息

### ⚡ 促销活动管理
- **一键分桶创建闪购任务** - 支持按时间槽批量创建闪购活动
- **活动商品管理** - 添加/更新活动商品及策略定价
- **活动复制** - 将现有活动复制到新时段
- **批量停用** - 批量下架/停止促销活动
- **商品追加** - 批量追加商品到活动

### 📊 定价策略系统
- **策略 CRUD** - 创建、查询、更新、删除定价策略
- **SKU 特价覆盖** - 为特定 SKU 设置特价
- **智能定价** - 特价 > 关键词策略 > 默认兜底

### 📦 订单管理
- **仓库订单统计** - 按仓库获取待发货订单数汇总

## 🛠️ 技术栈

### 后端
- Python 3.11+
- FastAPI 0.104+
- SQLite (本地数据库)
- requests (HTTP 请求)
- pytesseract + Pillow + opencv-python (OCR 验证码识别)

### 前端
- Vue 3 + TypeScript
- Vite 6
- Tauri 2 (桌面应用框架)
- TailwindCSS 3

## 📁 项目结构

```
.
├── backend/                    # 后端服务
│   ├── client/                # TikTok API 客户端
│   │   ├── auth_client.py     # 认证接口
│   │   ├── base_client.py     # 基础请求封装
│   │   ├── order_client.py    # 订单接口
│   │   ├── product_client.py  # 商品接口
│   │   ├── promotion_client.py # 促销接口
│   │   └── shop_client.py     # 店铺接口
│   ├── dao/                   # 数据访问层
│   │   ├── auth_dao.py        # 认证数据
│   │   ├── base_dao.py        # 基础 DAO
│   │   ├── price_dao.py       # 定价策略数据
│   │   └── webhook_dao.py     # Webhook 数据
│   ├── router/                # API 路由
│   │   ├── auth_router.py     # 认证路由
│   │   ├── order_router.py    # 订单路由
│   │   ├── product_router.py  # 商品路由
│   │   ├── promotion_router.py # 促销路由
│   │   ├── shop_router.py     # 店铺路由
│   │   └── system_router.py   # 系统路由
│   ├── schemas/               # 数据模型
│   │   ├── auth_schema.py     # 认证模型
│   │   ├── base_response.py   # 统一响应格式
│   │   ├── order_schema.py    # 订单模型
│   │   ├── product_schema.py  # 商品模型
│   │   ├── promotion_schema.py # 促销模型
│   │   └── shop_schema.py     # 店铺模型
│   ├── service/               # 业务逻辑层
│   │   ├── auth_service/      # 认证服务
│   │   ├── order_service/     # 订单服务
│   │   ├── product_service/   # 商品服务
│   │   ├── promotion_service/ # 促销服务
│   │   ├── shop_service/      # 店铺服务
│   │   └── system_service/    # 系统服务
│   ├── utils/                 # 工具函数
│   │   ├── cookie_util.py     # Cookie 工具
│   │   ├── db_util.py         # 数据库工具
│   │   ├── decorators.py      # 装饰器
│   │   ├── logger_util.py     # 日志工具
│   │   ├── ocr_util.py        # OCR 工具
│   │   └── webhook_util.py    # Webhook 工具
│   ├── db/                    # SQLite 数据库文件
│   ├── main.py                # 应用入口
│   └── requirements.txt       # 依赖清单
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── api/               # API 调用封装
│   │   ├── components/        # 公共组件
│   │   ├── views/             # 页面视图
│   │   │   ├── flash/         # 闪购管理
│   │   │   │   ├── Add.vue    # 创建闪购
│   │   │   │   ├── Manage.vue # 活动管理
│   │   │   │   └── Strategy.vue # 定价策略
│   │   │   ├── shipping/      # 发货管理
│   │   │   │   └── PreLaunch.vue # 待发货统计
│   │   │   ├── Login.vue      # 登录页
│   │   │   ├── Shops.vue      # 店铺管理
│   │   │   └── Home.vue       # 首页
│   │   ├── router/            # 路由配置
│   │   └── utils/             # 工具函数
│   ├── src-tauri/             # Tauri 配置
│   └── package.json           # 前端依赖
└── README.md
```

## 📦 安装

### 环境要求
- Python 3.11+
- Node.js 18+
- Rust (用于 Tauri 构建)

### 后端安装

```bash
cd backend
pip install -r requirements.txt
```

### 前端安装

```bash
cd frontend
pnpm install
```

## 🚀 运行

### 开发模式

**启动后端:**
```bash
cd backend
python main.py
```
后端服务默认运行在 `http://127.0.0.1:5000`

**启动前端:**
```bash
cd frontend
pnpm dev
```

### 构建桌面应用

```bash
cd frontend
pnpm tauri build
```

## 🔌 API 接口

### 认证管理
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/auth/login` | POST | OCR 自动登录 |
| `/api/auth/cookie` | GET | 获取有效 Cookie |
| `/api/auth/account/info` | GET | 获取账户信息 |

### 店铺管理
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/shop/list` | GET | 获取店铺列表 |
| `/api/shop/info` | GET | 获取店铺详情 |

### 促销管理
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/promotion/flash-sale/create` | POST | 创建闪购活动 |
| `/api/promotion/product/add-update` | POST | 添加/更新商品 |
| `/api/promotion/copy` | POST | 复制活动 |
| `/api/promotion/deactivate` | POST | 批量停用 |
| `/api/promotion/list` | GET | 查询活动列表 |

### 定价策略
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/promotion/strategy/list` | GET | 获取策略列表 |
| `/api/promotion/strategy/save` | POST | 保存策略 |
| `/api/promotion/strategy/delete` | DELETE | 删除策略 |

### 订单管理
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/order/warehouse-summary` | POST | 仓库订单统计 |

## 📖 API 文档

启动后端服务后访问：
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
