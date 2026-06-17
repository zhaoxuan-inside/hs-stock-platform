# 股票数据平台 - 项目目录结构规划

## 1. 项目根目录结构

`
hs-stock-platform/
├── frontend/           # 前端应用
├── backend/            # 后端应用
├── docker/             # Docker部署配置
├── docs/               # 项目文档
├── configs/            # 配置文件目录(运行时挂载)
├── logs/               # 日志文件目录(运行时挂载)
├── data/               # 数据文件目录(运行时挂载)
├── .gitignore
├── LICENSE
└── README.md
`

---

## 2. 前端项目结构 (frontend/)

`
frontend/
├── src/
│   ├── assets/         # 静态资源(图片、字体等)
│   ├── components/     # 通用组件
│   │   ├── Layout/     # 布局组件
│   │   │   ├── Sidebar.vue
│   │   │   ├── Header.vue
│   │   │   └── MainContent.vue
│   │   ├── Stock/      # 股票相关组件
│   │   │   ├── StockCard.vue
│   │   │   ├── StockSearch.vue
│   │   │   └── KLineChart.vue
│   │   ├── Task/       # 任务相关组件
│   │   │   ├── TaskList.vue
│   │   │   ├── TaskProgress.vue
│   │   │   └── ConfigForm.vue
│   │   ├── Chat/       # AI问答组件
│   │   │   ├── ChatPanel.vue
│   │   │   ├── ModelSelector.vue
│   │   │   └── ReferenceSelector.vue
│   │   ├── Message/    # 消息相关组件
│   │   │   ├── MessageList.vue
│   │   │   ├── MessageCard.vue
│   │   │   └── MessageFilter.vue
│   │   └── Common/     # 通用组件
│   │       ├── Loading.vue
│   │       ├── Empty.vue
│   │       ├── Pagination.vue
│   │       └── Toast.vue
│   ├── views/          # 页面视图
│   │   ├── Login.vue
│   │   ├── Dashboard.vue
│   │   ├── StockList.vue
│   │   ├── StockDetail.vue
│   │   ├── TaskList.vue
│   │   ├── Scheduler.vue
│   │   ├── Chat.vue
│   │   └── Messages.vue
│   ├── stores/         # Pinia状态管理
│   │   ├── auth.ts
│   │   ├── stocks.ts
│   │   ├── tasks.ts
│   │   ├── chat.ts
│   │   └── messages.ts
│   ├── api/            # API接口封装
│   │   ├── auth.ts
│   │   ├── stocks.ts
│   │   ├── tasks.ts
│   │   ├── chat.ts
│   │   └── messages.ts
│   ├── utils/          # 工具函数
│   │   ├── request.ts  # Axios封装(含trace_id)
│   │   ├── websocket.ts# WebSocket封装(含trace_id)
│   │   ├── cache.ts    # 本地缓存
│   │   ├── format.ts   # 格式化工具
│   │   └── logger.ts   # 日志工具(含trace_id)
│   ├── middleware/      # 前端中间件
│   │   └── trace.ts    # Trace ID管理
│   ├── types/          # TypeScript类型定义
│   │   ├── index.ts
│   │   ├── stock.ts
│   │   ├── task.ts
│   │   ├── chat.ts
│   │   └── message.ts
│   ├── router/         # Vue Router配置
│   │   └── index.ts
│   ├── styles/         # 全局样式
│   │   ├── variables.scss
│   │   └── global.scss
│   ├── App.vue
│   └── main.ts
├── public/
│   └── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .env.development
├── .env.production
└── README.md
`

### 2.1 关键文件说明

| 文件 | 说明 |
|------|------|
| src/api/*.ts | 后端API接口封装，统一管理请求方法 |
| src/stores/*.ts | Pinia状态管理，管理各模块状态 |
| src/utils/request.ts | Axios实例封装，统一处理请求拦截、响应拦截(含trace_id) |
| src/utils/websocket.ts | WebSocket封装，处理连接、消息监听、重连(含trace_id) |
| src/utils/cache.ts | 本地缓存工具，使用LocalStorage/SessionStorage |
| src/utils/logger.ts | 前端日志工具，统一日志格式(含trace_id) |
| src/middleware/trace.ts | 前端Trace ID管理，生成和传递trace_id |
| src/router/index.ts | 路由配置，包含路由守卫、权限控制 |

---

## 3. 后端项目结构 (backend/)

采用DDD架构模式：

`
backend/
├── src/
│   ├── stock_platform/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI应用入口
│   │   ├── core/                # 核心模块
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── security.py      # 安全相关(JWT、签名)
│   │   │   ├── logging.py       # 日志配置(结构化日志、trace_id)
│   │   │   ├── dependencies.py  # 依赖注入(含trace_id上下文)
│   │   │   └── trace.py         # Trace ID管理(生成、传递、上下文)
│   │   ├── domain/              # 领域层
│   │   │   ├── __init__.py
│   │   │   ├── models/          # 领域模型
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── stock.py
│   │   │   │   ├── task.py
│   │   │   │   ├── scheduler.py
│   │   │   │   ├── message.py
│   │   │   │   └── chat.py
│   │   │   ├── repositories/    # 仓储接口
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_repository.py
│   │   │   │   ├── stock_repository.py
│   │   │   │   ├── task_repository.py
│   │   │   │   ├── scheduler_repository.py
│   │   │   │   ├── message_repository.py
│   │   │   │   └── chat_repository.py
│   │   │   └── services/        # 领域服务
│   │   │       ├── __init__.py
│   │   │       ├── auth_service.py
│   │   │       ├── stock_service.py
│   │   │       ├── task_service.py
│   │   │       ├── scheduler_service.py
│   │   │       ├── message_service.py
│   │   │       └── chat_service.py
│   │   ├── infrastructure/      # 基础设施层
│   │   │   ├── __init__.py
│   │   │   ├── database/        # 数据库实现
│   │   │   │   ├── __init__.py
│   │   │   │   ├── postgres.py  # PostgreSQL连接
│   │   │   │   ├── mongodb.py   # MongoDB连接
│   │   │   │   ├── redis.py     # Redis连接
│   │   │   │   └── etcd.py      # etcd连接
│   │   │   ├── repositories/    # 仓储实现
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_repository_impl.py
│   │   │   │   ├── stock_repository_impl.py
│   │   │   │   ├── task_repository_impl.py
│   │   │   │   ├── scheduler_repository_impl.py
│   │   │   │   ├── message_repository_impl.py
│   │   │   │   └── chat_repository_impl.py
│   │   │   ├── external/        # 外部API调用
│   │   │   │   ├── __init__.py
│   │   │   │   ├── baostock.py  # Baostock API封装
│   │   │   │   ├── qwen.py      # 通义千问API封装
│   │   │   │   └── deepseek.py  # DeepSeek API封装
│   │   │   └── scheduler/       # 定时任务实现
│   │   │       ├── __init__.py
│   │   │       └── apscheduler.py
│   │   ├── application/         # 应用层
│   │   │   ├── __init__.py
│   │   │   ├── dtos/            # 数据传输对象
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_dto.py
│   │   │   │   ├── stock_dto.py
│   │   │   │   ├── task_dto.py
│   │   │   │   ├── scheduler_dto.py
│   │   │   │   ├── message_dto.py
│   │   │   │   └── chat_dto.py
│   │   │   └── services/        # 应用服务
│   │   │       ├── __init__.py
│   │   │       ├── auth_app_service.py
│   │   │       ├── stock_app_service.py
│   │   │       ├── task_app_service.py
│   │   │       ├── scheduler_app_service.py
│   │   │       ├── message_app_service.py
│   │   │       └── chat_app_service.py
│   │   └── presentation/        # 表现层
│   │       ├── __init__.py
│   │       ├── api/             # API路由
│   │       │   ├── __init__.py
│   │       │   ├── auth.py
│   │       │   ├── stocks.py
│   │       │   ├── tasks.py
│   │       │   ├── scheduler.py
│   │       │   ├── chat.py
│   │       │   ├── messages.py
│   │       │   ├── dashboard.py
│   │       │   └── external.py
│   │       ├── websocket/       # WebSocket路由
│   │       │   ├── __init__.py
│   │       │   ├── messages.py
│   │       │   ├── tasks.py
│   │       │   └── stocks.py
│   │       └── middleware/      # 中间件
│   │           ├── __init__.py
│   │           ├── auth.py      # JWT认证中间件
│   │           ├── signature.py # 签名验证中间件
│   │           ├── cors.py      # CORS中间件
│   │           └── trace.py     # Trace ID中间件(生成、注入上下文、响应头)
│   └── tests/                   # 测试目录
│       ├── __init__.py
│       ├── unit/                # 单元测试
│       ├── integration/         # 集成测试
│       └── fixtures/            # 测试数据
├── requirements.txt             # Python依赖
├── requirements-dev.txt         # 开发依赖
├── .env.example                 # 环境变量示例
├── alembic.ini                  # Alembic配置
├── alembic/                     # 数据库迁移
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
└── README.md
`

### 3.1 DDD分层说明

| 层级 | 职责 | 说明 |
|------|------|------|
| Presentation | 对外接口 | REST API、WebSocket、中间件 |
| Application | 应用服务 | 事务管理、DTO转换、用例编排 |
| Domain | 领域核心 | 实体、值对象、领域服务、仓储接口 |
| Infrastructure | 基础设施 | 数据库实现、外部API调用、配置管理 |

### 3.2 关键文件说明

| 文件 | 说明 |
|------|------|
| src/stock_platform/main.py | FastAPI应用入口，注册路由、中间件 |
| src/stock_platform/core/config.py | 配置管理，从etcd/环境变量读取配置 |
| src/stock_platform/core/security.py | JWT生成验证、密码加密、签名算法 |
| src/stock_platform/core/logging.py | 结构化日志配置，支持JSON格式输出 |
| src/stock_platform/core/trace.py | Trace ID生成、传递、上下文管理 |
| src/stock_platform/core/dependencies.py | 依赖注入(含trace_id上下文) |
| src/stock_platform/domain/models/*.py | 领域实体定义 |
| src/stock_platform/domain/repositories/*.py | 仓储接口定义 |
| src/stock_platform/infrastructure/repositories/*.py | 仓储接口实现 |
| src/stock_platform/infrastructure/external/*.py | 外部API封装 |
| src/stock_platform/presentation/api/*.py | REST API路由定义 |
| src/stock_platform/presentation/middleware/trace.py | Trace ID中间件(生成、注入、响应头) |

---

## 4. Docker部署结构 (docker/)

`
docker/
├── nginx/
│   ├── conf.d/
│   │   └── default.conf        # Nginx配置
│   └── Dockerfile
├── frontend/
│   └── Dockerfile
├── backend/
│   ├── Dockerfile
│   └── entrypoint.sh
└── docker-compose.yml
`

### 4.1 docker-compose.yml 服务说明

| 服务名 | 镜像 | 端口映射 | 数据卷 |
|--------|------|----------|--------|
| nginx | nginx:1.25 | 80:80, 443:443 | ./nginx/conf.d:/etc/nginx/conf.d |
| frontend | hs-stock-fe:latest | - | - |
| backend | hs-stock-be:latest | - | ../configs:/app/configs |
| postgres | postgres:16 | - | ../data/postgres:/var/lib/postgresql/data |
| mongodb | mongo:7.0 | - | ../data/mongodb:/data/db |
| redis | redis:7.2 | - | ../data/redis:/data |
| etcd | etcd:3.5 | - | ../data/etcd:/etcd-data |

---

## 5. 配置文件结构 (configs/)

`
configs/
├── app/
│   ├── settings.yaml        # 应用全局配置
│   └── logging.yaml         # 日志配置
├── database/
│   ├── postgres.yaml        # PostgreSQL配置
│   ├── mongodb.yaml         # MongoDB配置
│   ├── redis.yaml           # Redis配置
│   └── etcd.yaml            # etcd配置
├── auth/
│   └── jwt.yaml             # JWT配置
├── external/
│   ├── baostock.yaml        # Baostock API配置
│   ├── qwen.yaml            # 通义千问配置
│   └── deepseek.yaml        # DeepSeek配置
└── scheduler/
    └── settings.yaml        # 定时任务配置
`

### 5.1 配置文件示例

**settings.yaml:**
`yaml
app:
  name: "hs-stock-platform"
  host: "0.0.0.0"
  port: 8000
  debug: false

cors:
  allowed_origins:
    - "http://localhost:5173"
    - "https://your-domain.com"
`

**postgres.yaml:**
`yaml
host: "postgres"
port: 5432
database: "stock_platform"
username: "stock"
password: "password"
`

**jwt.yaml:**
`yaml
secret_key: "your-secret-key"
access_token_expire_minutes: 120
refresh_token_expire_days: 7
algorithm: "HS256"
`

---

## 6. 日志文件结构 (logs/)

`
logs/
├── frontend/
│   ├── access.log              # 前端访问日志(含trace_id)
│   ├── error.log               # 前端错误日志(含trace_id)
│   └── app.log                 # 前端应用日志(含trace_id)
├── backend/
│   ├── app.log                 # 后端应用日志(JSON格式，含trace_id)
│   ├── access.log              # 后端访问日志(含trace_id)
│   ├── error.log               # 后端错误日志(含trace_id)
│   ├── task.log                # 任务执行日志(含trace_id)
│   └── external.log            # 第三方API调用日志(含trace_id)
└── nginx/
    ├── access.log              # Nginx访问日志(透传X-Trace-ID)
    └── error.log               # Nginx错误日志
`

### 6.1 日志轮转策略

| 日志文件 | 轮转周期 | 保留天数 | 单文件大小限制 |
|----------|----------|----------|----------------|
| app.log | 每日 | 30天 | 100MB |
| access.log | 每日 | 30天 | 100MB |
| error.log | 每日 | 90天 | 100MB |
| task.log | 每日 | 30天 | 200MB |
| external.log | 每日 | 30天 | 200MB |

### 6.2 日志格式

**后端日志格式(JSON):**
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "span_id": "span-001",
  "level": "INFO",
  "logger": "app.middleware.request",
  "message": "Request received",
  "fields": {
    "method": "GET",
    "path": "/api/v1/stocks",
    "client_ip": "192.168.1.100",
    "user_id": "user-001"
  },
  "duration_ms": 156,
  "status_code": 200
}
```

---

## 7. 数据文件结构 (data/)

`
data/
├── postgres/               # PostgreSQL数据目录
├── mongodb/                # MongoDB数据目录
├── redis/                  # Redis数据目录
└── etcd/                   # etcd数据目录
`

---

## 8. 部署用户配置

| 项目 | 值 |
|------|------|
| 用户名 | stock |
| UID | 1001 |
| GID | 100 |
| 宿主机路径 | /home/stock/hs-stock-platform |

**目录权限：**
`
chown -R stock:stock /home/stock/hs-stock-platform
chmod -R 755 /home/stock/hs-stock-platform
chmod -R 777 /home/stock/hs-stock-platform/logs
chmod -R 777 /home/stock/hs-stock-platform/data
`

---

## 9. 文件清单总览

### 9.1 前端文件清单

| 文件路径 | 说明 |
|----------|------|
| frontend/src/main.ts | 入口文件 |
| frontend/src/App.vue | 根组件 |
| frontend/src/router/index.ts | 路由配置 |
| frontend/src/stores/*.ts | 状态管理(5个) |
| frontend/src/api/*.ts | API接口(5个) |
| frontend/src/views/*.vue | 页面视图(8个) |
| frontend/src/components/**/*.vue | 组件(20+) |
| frontend/package.json | 依赖配置 |
| frontend/vite.config.ts | 构建配置 |

### 9.2 后端文件清单

| 文件路径 | 说明 |
|----------|------|
| backend/src/stock_platform/main.py | 应用入口 |
| backend/src/stock_platform/core/*.py | 核心模块(5个) |
| backend/src/stock_platform/core/logging.py | 结构化日志配置 |
| backend/src/stock_platform/core/trace.py | Trace ID管理 |
| backend/src/stock_platform/domain/models/*.py | 领域模型(6个) |
| backend/src/stock_platform/domain/repositories/*.py | 仓储接口(6个) |
| backend/src/stock_platform/domain/services/*.py | 领域服务(6个) |
| backend/src/stock_platform/infrastructure/database/*.py | 数据库连接(4个) |
| backend/src/stock_platform/infrastructure/repositories/*.py | 仓储实现(6个) |
| backend/src/stock_platform/infrastructure/external/*.py | 外部API(3个) |
| backend/src/stock_platform/application/dtos/*.py | DTO(6个) |
| backend/src/stock_platform/application/services/*.py | 应用服务(6个) |
| backend/src/stock_platform/presentation/api/*.py | API路由(8个) |
| backend/src/stock_platform/presentation/websocket/*.py | WebSocket路由(3个) |
| backend/src/stock_platform/presentation/middleware/*.py | 中间件(4个) |
| backend/src/stock_platform/presentation/middleware/trace.py | Trace ID中间件 |
| backend/requirements.txt | 依赖清单 |
| backend/alembic.ini | 迁移配置 |

### 9.3 Docker文件清单

| 文件路径 | 说明 |
|----------|------|
| docker/docker-compose.yml | 编排配置 |
| docker/nginx/conf.d/default.conf | Nginx配置 |
| docker/nginx/Dockerfile | Nginx构建 |
| docker/frontend/Dockerfile | 前端构建 |
| docker/backend/Dockerfile | 后端构建 |
| docker/backend/entrypoint.sh | 后端入口脚本 |
