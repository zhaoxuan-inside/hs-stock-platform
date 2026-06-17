# 股票数据平台 - API设计文档

## 1. 通用规范

### 1.1 请求头

| 头名 | 必填 | 类型 | 说明 |
|------|------|------|------|
| Content-Type | 是 | string | application/json |
| Authorization | 否 | string | Bearer {token} |
| X-Trace-ID | 否 | string | 链路追踪ID(UUID) |

### 1.2 响应格式

\\\json
{
  "code": 200,
  "message": "success",
  "trace_id": "string",
  "data": {}
}
\\\

### 1.3 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 2. 认证模块

### 2.1 登录

**POST /api/v1/auth/login**

请求体：
\\\json
{
  "username": "string (必填，3-64字符)",
  "password": "string (必填，6-128字符)"
}
\\\

### 2.2 Token刷新

**POST /api/v1/auth/refresh**

---

## 3. 股票基础信息模块

### 3.1 获取股票列表

**GET /api/v1/stocks**

查询参数：
| 参数 | 类型 | 必填 | 默认值 | 边界 | 说明 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | >=1 | 页码 |
| size | integer | 否 | 20 | 1-100 | 每页数量 |
| keyword | string | 否 | - | <=128字符 | 股票代码或名称 |
| industry_code | string | 否 | - | - | 行业代码 |
| exchange | string | 否 | - | SSE/SZSE | 交易所 |

### 3.2 获取股票详情（融合多对一信息）

**GET /api/v1/stocks/{code}**

---

## 4. K线数据模块

### 4.1 获取K线数据

**GET /api/v1/stocks/{code}/kline**

---

## 5. 财务数据模块（一对多关系）

### 5.1 获取盈利能力数据

**GET /api/v1/stocks/{code}/finance/profit**

### 5.2 获取营运能力数据

**GET /api/v1/stocks/{code}/finance/operation**

### 5.3 获取成长能力数据

**GET /api/v1/stocks/{code}/finance/growth**

### 5.4 获取偿债能力数据

**GET /api/v1/stocks/{code}/finance/balance**

### 5.5 获取现金流量数据

**GET /api/v1/stocks/{code}/finance/cashflow**

### 5.6 获取杜邦分析数据

**GET /api/v1/stocks/{code}/finance/dupont**

---

## 6. 公司报告模块（一对多关系）

### 6.1 获取业绩预告数据

**GET /api/v1/stocks/{code}/reports/forecast**

### 6.2 获取业绩快报数据

**GET /api/v1/stocks/{code}/reports/express**

### 6.3 获取分红数据

**GET /api/v1/stocks/{code}/reports/dividend**

---

## 7. 行业分类模块（多对多关系）

### 7.1 获取行业列表

**GET /api/v1/industries**

### 7.2 获取行业详情及关联股票

**GET /api/v1/industries/{code}**

---

## 8. 指数模块（多对多关系）

### 8.1 获取指数列表

**GET /api/v1/indexes**

### 8.2 获取指数详情及成分股

**GET /api/v1/indexes/{code}**

---

## 9. 任务管理模块

### 9.1 获取任务列表

**GET /api/v1/tasks**

### 9.2 触发任务

**POST /api/v1/tasks/{task_id}/run**

### 9.3 暂停任务

**POST /api/v1/tasks/executions/{execution_id}/pause**

### 9.4 继续任务

**POST /api/v1/tasks/executions/{execution_id}/resume**

---

## 10. 消息模块

### 10.1 获取消息列表

**GET /api/v1/messages**

### 10.2 标记消息已读

**PUT /api/v1/messages/{message_id}/read**

---

## 11. AI问答模块

### 11.1 发送问答请求

**POST /api/v1/chat**

---

## 12. 数据关系展示策略总结

### 12.1 融合展示（多对一关系）

| 数据类型 | 展示位置 | 说明 |
|----------|----------|------|
| 行业信息 | 股票详情页 | 通过industry_code字段关联 |
| 最新价格 | 股票列表/详情 | 从最新K线数据获取 |
| 估值指标 | 股票详情页 | PE/PB等从K线数据获取 |

### 12.2 列表展示（一对多关系）

| 数据类型 | API路径 | 展示方式 |
|----------|----------|----------|
| 盈利能力 | /stocks/{code}/finance/profit | 表格列表 |
| 营运能力 | /stocks/{code}/finance/operation | 表格列表 |
| 成长能力 | /stocks/{code}/finance/growth | 表格列表 |
| 偿债能力 | /stocks/{code}/finance/balance | 表格列表 |
| 现金流量 | /stocks/{code}/finance/cashflow | 表格列表 |
| 杜邦分析 | /stocks/{code}/finance/dupont | 表格列表 |
| 业绩预告 | /stocks/{code}/reports/forecast | 表格列表 |
| 业绩快报 | /stocks/{code}/reports/express | 表格列表 |
| 分红信息 | /stocks/{code}/reports/dividend | 表格列表 |

### 12.3 关联跳转（多对多关系）

| 数据类型 | API路径 | 关联方式 |
|----------|----------|----------|
| 行业-股票 | /industries/{code} | 行业详情页展示关联股票，支持跳转 |
| 指数-成分股 | /indexes/{code} | 指数详情页展示成分股，支持跳转 |
| 股票-指数 | /stocks/{code} | 股票详情页展示所属指数，支持跳转 |

---

## 13. WebSocket接口

### 13.1 消息推送

**连接地址：ws://{host}/ws/messages?token={access_token}&trace_id={trace_id}**

### 13.2 任务进度推送

**连接地址：ws://{host}/ws/tasks/{execution_id}?token={access_token}&trace_id={trace_id}**

### 13.3 股票价格推送

**连接地址：ws://{host}/ws/stocks?token={access_token}&trace_id={trace_id}&codes={stock_codes}**