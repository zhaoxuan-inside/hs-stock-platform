# 股票数据平台 - 数据库设计文档

## 1. 数据库概述

本系统采用多数据库架构，根据数据特性选择合适的存储方案：

| 数据库类型 | 技术 | 用途 |
|------------|------|------|
| 关系型数据库 | PostgreSQL | 用户信息、股票基础数据、任务配置、消息数据、财务数据、公司报告、行业分类 |
| 文档数据库 | MongoDB | AI问答历史记录、系统日志、用户行为日志 |
| 缓存数据库 | Redis | 股票数据缓存、用户Token、任务进度 |
| 配置存储 | etcd | 系统配置、分布式锁 |

---

## 2. ER图

\\\mermaid
erDiagram
    USER ||--o{ MESSAGE : receives
    USER ||--o{ CHAT_HISTORY : creates
    TASK ||--o{ TASK_EXECUTION : has
    TASK ||--o{ SCHEDULER : schedules
    STOCK ||--o{ KLINE_DAY : has
    STOCK ||--o{ KLINE_WEEK : has
    STOCK ||--o{ KLINE_MONTH : has
    STOCK ||--o{ KLINE_5MIN : has
    STOCK ||--o{ KLINE_15MIN : has
    STOCK ||--o{ KLINE_30MIN : has
    STOCK ||--o{ KLINE_60MIN : has
    STOCK ||--o{ FINANCE_PROFIT : has
    STOCK ||--o{ FINANCE_OPERATION : has
    STOCK ||--o{ FINANCE_GROWTH : has
    STOCK ||--o{ FINANCE_BALANCE : has
    STOCK ||--o{ FINANCE_CASHFLOW : has
    STOCK ||--o{ FINANCE_DUPONT : has
    STOCK ||--o{ REPORT_FORECAST : has
    STOCK ||--o{ REPORT_EXPRESS : has
    STOCK ||--o{ DIVIDEND_DATA : has
    STOCK ||--o{ ADJUST_FACTOR : has
    INDUSTRY ||--o{ STOCK_INDUSTRY : maps
    INDEX ||--o{ INDEX_CONSTITUENT : contains
    
    USER {
        uuid id PK
        varchar username UK
        varchar password_hash
        varchar role
        timestamp created_at
        timestamp updated_at
    }
    
    STOCK {
        varchar code PK
        varchar name
        varchar industry_code FK
        varchar exchange
        varchar type
        timestamp created_at
        timestamp updated_at
    }
    
    INDUSTRY {
        varchar code PK
        varchar name
        varchar parent_code
        timestamp created_at
    }
    
    STOCK_INDUSTRY {
        varchar stock_code PK,FK
        varchar industry_code PK,FK
        timestamp created_at
    }
    
    INDEX {
        varchar code PK
        varchar name
        varchar type
        timestamp created_at
    }
    
    INDEX_CONSTITUENT {
        varchar index_code PK,FK
        varchar stock_code PK,FK
        date entry_date
        date exit_date
        timestamp created_at
    }
    
    TASK {
        uuid id PK
        varchar name
        varchar api_name
        jsonb config_schema
        timestamp created_at
        timestamp updated_at
    }
    
    TASK_EXECUTION {
        uuid id PK
        uuid task_id FK
        varchar status
        int progress
        int completed_count
        int total_count
        text current_item
        timestamp start_time
        timestamp end_time
        text error_message
        jsonb result
        jsonb progress_data
    }
    
    SCHEDULER {
        uuid id PK
        varchar name
        uuid task_id FK
        varchar cron_expression
        jsonb config
        varchar status
        timestamp last_run_time
        timestamp next_run_time
        timestamp created_at
        timestamp updated_at
    }
    
    MESSAGE {
        uuid id PK
        uuid user_id FK
        varchar title
        text content
        varchar type
        uuid related_task_id
        varchar status
        timestamp created_at
    }
    
    FINANCE_PROFIT {
        bigint id PK
        varchar stock_code FK
        int year
        int quarter
        decimal roe
        decimal roa
        decimal gross_profit_rate
        decimal net_profit_rate
        decimal eps
        decimal total_share
        decimal liqa_share
        timestamp created_at
    }
    
    FINANCE_OPERATION {
        bigint id PK
        varchar stock_code FK
        int year
        int quarter
        decimal ar_turnover
        decimal inventory_turnover
        decimal current_asset_turnover
        decimal total_asset_turnover
        timestamp created_at
    }
    
    FINANCE_GROWTH {
        bigint id PK
        varchar stock_code FK
        int year
        int quarter
        decimal revenue_growth_rate
        decimal net_profit_growth_rate
        decimal asset_growth_rate
        decimal eps_growth_rate
        timestamp created_at
    }
    
    FINANCE_BALANCE {
        bigint id PK
        varchar stock_code FK
        int year
        int quarter
        decimal asset_liability_ratio
        decimal current_ratio
        decimal quick_ratio
        decimal interest_coverage_ratio
        timestamp created_at
    }
    
    FINANCE_CASHFLOW {
        bigint id PK
        varchar stock_code FK
        int year
        int quarter
        decimal operating_cash_flow
        decimal investing_cash_flow
        decimal financing_cash_flow
        decimal free_cash_flow
        timestamp created_at
    }
    
    FINANCE_DUPONT {
        bigint id PK
        varchar stock_code FK
        int year
        int quarter
        decimal roe
        decimal net_profit_margin
        decimal asset_turnover
        decimal equity_multiplier
        timestamp created_at
    }
    
    REPORT_FORECAST {
        bigint id PK
        varchar stock_code FK
        date report_date
        int year
        int quarter
        varchar type
        decimal profit_low
        decimal profit_high
        decimal profit_change_low
        decimal profit_change_high
        varchar change_reason
        timestamp created_at
    }
    
    REPORT_EXPRESS {
        bigint id PK
        varchar stock_code FK
        date report_date
        int year
        int quarter
        decimal revenue
        decimal net_profit
        decimal eps
        decimal revenue_change
        decimal net_profit_change
        timestamp created_at
    }
    
    DIVIDEND_DATA {
        bigint id PK
        varchar stock_code FK
        date report_date
        date ex_date
        date pay_date
        decimal dividend_per_share
        decimal bonus_share_ratio
        decimal transfer_share_ratio
        varchar plan_status
        timestamp created_at
    }
    
    ADJUST_FACTOR {
        bigint id PK
        varchar stock_code FK
        date date
        decimal adjust_factor
        timestamp created_at
    }
\\\

---

## 3. 表结构设计

### 3.1 用户表 (users)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 用户唯一标识 |
| username | VARCHAR(64) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(256) | NOT NULL | 密码哈希值(BCrypt) |
| role | VARCHAR(32) | NOT NULL, DEFAULT 'user' | 角色(user/admin) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**DDL:**
`sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
`

### 3.2 股票基础信息表 (stocks)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| code | VARCHAR(16) | PRIMARY KEY | 股票代码 |
| name | VARCHAR(64) | NOT NULL | 股票名称 |
| industry_code | VARCHAR(16) | FOREIGN KEY | 所属行业代码 |
| exchange | VARCHAR(32) | | 交易所(SSE/SZSE) |
| type | VARCHAR(16) | DEFAULT 'stock' | 类型(stock/index) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**DDL:**
`sql
CREATE TABLE stocks (
    code VARCHAR(16) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    industry_code VARCHAR(16) REFERENCES industry(code),
    exchange VARCHAR(32),
    type VARCHAR(16) DEFAULT 'stock',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stocks_name ON stocks(name);
CREATE INDEX idx_stocks_industry_code ON stocks(industry_code);
CREATE INDEX idx_stocks_exchange ON stocks(exchange);
CREATE INDEX idx_stocks_type ON stocks(type);
`

### 3.3 行业分类表 (industry)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| code | VARCHAR(16) | PRIMARY KEY | 行业代码 |
| name | VARCHAR(64) | NOT NULL | 行业名称 |
| parent_code | VARCHAR(16) | | 父级行业代码 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE industry (
    code VARCHAR(16) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    parent_code VARCHAR(16) REFERENCES industry(code),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_industry_parent_code ON industry(parent_code);
`

### 3.4 股票行业关联表 (stock_industry)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| stock_code | VARCHAR(16) | PRIMARY KEY, FOREIGN KEY | 股票代码 |
| industry_code | VARCHAR(16) | PRIMARY KEY, FOREIGN KEY | 行业代码 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE stock_industry (
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    industry_code VARCHAR(16) NOT NULL REFERENCES industry(code),
    PRIMARY KEY (stock_code, industry_code),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stock_industry_industry_code ON stock_industry(industry_code);
`

### 3.5 指数表 (stock_index)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| code | VARCHAR(16) | PRIMARY KEY | 指数代码 |
| name | VARCHAR(64) | NOT NULL | 指数名称 |
| type | VARCHAR(32) | | 指数类型(composite/size/industry) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE stock_index (
    code VARCHAR(16) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    type VARCHAR(32),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stock_index_type ON stock_index(type);
`

### 3.6 指数成分股表 (index_constituent)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| index_code | VARCHAR(16) | PRIMARY KEY, FOREIGN KEY | 指数代码 |
| stock_code | VARCHAR(16) | PRIMARY KEY, FOREIGN KEY | 股票代码 |
| entry_date | DATE | | 纳入日期 |
| exit_date | DATE | | 退出日期 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE index_constituent (
    index_code VARCHAR(16) NOT NULL REFERENCES stock_index(code),
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    entry_date DATE,
    exit_date DATE,
    PRIMARY KEY (index_code, stock_code),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_index_constituent_stock_code ON index_constituent(stock_code);
CREATE INDEX idx_index_constituent_entry_date ON index_constituent(entry_date);
`

### 3.7 采集任务表 (tasks)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 任务唯一标识 |
| name | VARCHAR(128) | NOT NULL | 任务名称 |
| api_name | VARCHAR(128) | NOT NULL | 关联的API名称 |
| config_schema | JSONB | NOT NULL | 配置JSON Schema |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**DDL:**
`sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    api_name VARCHAR(128) NOT NULL,
    config_schema JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_api_name ON tasks(api_name);
`

### 3.8 任务执行记录表 (task_executions)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 执行记录唯一标识 |
| task_id | UUID | FOREIGN KEY | 关联任务ID |
| status | VARCHAR(32) | NOT NULL | 状态(pending/running/paused/failed/success/partial) |
| progress | INTEGER | NOT NULL, DEFAULT 0 | 执行进度(0-100) |
| completed_count | INTEGER | NOT NULL, DEFAULT 0 | 已完成数量 |
| total_count | INTEGER | NOT NULL, DEFAULT 0 | 总数量 |
| current_item | TEXT | | 当前处理项 |
| start_time | TIMESTAMP | NOT NULL | 开始时间 |
| end_time | TIMESTAMP | | 结束时间 |
| error_message | TEXT | | 错误信息 |
| result | JSONB | | 执行结果 |
| progress_data | JSONB | | 进度详情(断点续传数据) |

**DDL:**
`sql
CREATE TABLE task_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(id),
    status VARCHAR(32) NOT NULL,
    progress INTEGER NOT NULL DEFAULT 0,
    completed_count INTEGER NOT NULL DEFAULT 0,
    total_count INTEGER NOT NULL DEFAULT 0,
    current_item TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    error_message TEXT,
    result JSONB,
    progress_data JSONB
);

CREATE INDEX idx_task_executions_task_id ON task_executions(task_id);
CREATE INDEX idx_task_executions_status ON task_executions(status);
CREATE INDEX idx_task_executions_start_time ON task_executions(start_time);
`

### 3.9 定时任务表 (schedulers)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 定时任务唯一标识 |
| name | VARCHAR(128) | NOT NULL | 任务名称 |
| task_id | UUID | FOREIGN KEY | 关联采集任务ID |
| cron_expression | VARCHAR(64) | NOT NULL | CRON表达式 |
| config | JSONB | | 任务配置 |
| status | VARCHAR(32) | NOT NULL, DEFAULT 'active' | 状态(active/inactive) |
| last_run_time | TIMESTAMP | | 最后执行时间 |
| next_run_time | TIMESTAMP | | 下次执行时间 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**DDL:**
`sql
CREATE TABLE schedulers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    task_id UUID NOT NULL REFERENCES tasks(id),
    cron_expression VARCHAR(64) NOT NULL,
    config JSONB,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    last_run_time TIMESTAMP,
    next_run_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_schedulers_task_id ON schedulers(task_id);
CREATE INDEX idx_schedulers_status ON schedulers(status);
`

### 3.10 消息表 (messages)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PRIMARY KEY | 消息唯一标识 |
| user_id | UUID | FOREIGN KEY | 接收用户ID |
| title | VARCHAR(128) | NOT NULL | 消息标题 |
| content | TEXT | NOT NULL | 消息内容 |
| type | VARCHAR(32) | NOT NULL | 消息类型(task_error/task_success/task_progress/system) |
| related_task_id | UUID | | 关联任务ID |
| status | VARCHAR(32) | NOT NULL, DEFAULT 'unread' | 阅读状态(read/unread) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(128) NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR(32) NOT NULL,
    related_task_id UUID,
    status VARCHAR(32) NOT NULL DEFAULT 'unread',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_messages_type ON messages(type);
CREATE INDEX idx_messages_created_at ON messages(created_at);
`

---

## 4. K线数据表设计

### 4.1 分表策略说明

根据数据量评估，采用不同的存储策略：

| K线周期 | 预估数据量(5000支股票) | 存储策略 | 说明 |
|----------|------------------------|----------|------|
| 日K | ~11万条/月，~130万条/年 | 全量表 | 数据量适中，可全量保存 |
| 周K | ~2.3万条/月，~28万条/年 | 全量表 | 数据量小，可全量保存 |
| 月K | ~5000条/月，~6万条/年 | 全量表 | 数据量很小，全量保存 |
| 5分钟K | ~180万条/天，~800万条/月 | 按月分表 | 数据量大，需分表存储 |
| 15分钟K | ~60万条/天，~270万条/月 | 按月分表 | 数据量大，需分表存储 |
| 30分钟K | ~30万条/天，~130万条/月 | 按月分表 | 数据量大，需分表存储 |
| 60分钟K | ~15万条/天，~65万条/月 | 按月分表 | 数据量大，需分表存储 |

### 4.2 日K数据表 (kline_day)

**全量表设计：**

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| date | DATE | NOT NULL | 日期 |
| open | DECIMAL(10,2) | NOT NULL | 开盘价 |
| close | DECIMAL(10,2) | NOT NULL | 收盘价 |
| high | DECIMAL(10,2) | NOT NULL | 最高价 |
| low | DECIMAL(10,2) | NOT NULL | 最低价 |
| volume | BIGINT | NOT NULL | 成交量(股) |
| amount | DECIMAL(18,2) | | 成交额(元) |
| pct_chg | DECIMAL(6,2) | | 涨跌幅(%) |
| pe_ttm | DECIMAL(10,2) | | 滚动市盈率 |
| pb_mrq | DECIMAL(10,2) | | 市净率 |
| is_st | BOOLEAN | DEFAULT false | 是否ST |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE kline_day (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(10,2) NOT NULL,
    close DECIMAL(10,2) NOT NULL,
    high DECIMAL(10,2) NOT NULL,
    low DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    amount DECIMAL(18,2),
    pct_chg DECIMAL(6,2),
    pe_ttm DECIMAL(10,2),
    pb_mrq DECIMAL(10,2),
    is_st BOOLEAN DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_kline_day_stock_date ON kline_day(stock_code, date);
CREATE INDEX idx_kline_day_date ON kline_day(date);
`

### 4.3 周K数据表 (kline_week)

**DDL:**
`sql
CREATE TABLE kline_week (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(10,2) NOT NULL,
    close DECIMAL(10,2) NOT NULL,
    high DECIMAL(10,2) NOT NULL,
    low DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    amount DECIMAL(18,2),
    pct_chg DECIMAL(6,2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_kline_week_stock_date ON kline_week(stock_code, date);
CREATE INDEX idx_kline_week_date ON kline_week(date);
`

### 4.4 月K数据表 (kline_month)

**DDL:**
`sql
CREATE TABLE kline_month (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(10,2) NOT NULL,
    close DECIMAL(10,2) NOT NULL,
    high DECIMAL(10,2) NOT NULL,
    low DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    amount DECIMAL(18,2),
    pct_chg DECIMAL(6,2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_kline_month_stock_date ON kline_month(stock_code, date);
CREATE INDEX idx_kline_month_date ON kline_month(date);
`

### 4.5 分钟K线分表设计

**5分钟K线表格式：kline_5min_YYYYMM**
**15分钟K线表格式：kline_15min_YYYYMM**
**30分钟K线表格式：kline_30min_YYYYMM**
**60分钟K线表格式：kline_60min_YYYYMM**

**DDL模板：**
`sql
CREATE TABLE IF NOT EXISTS kline_5min_202401 (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    open DECIMAL(10,2) NOT NULL,
    close DECIMAL(10,2) NOT NULL,
    high DECIMAL(10,2) NOT NULL,
    low DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    amount DECIMAL(18,2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_kline_5min_202401_stock_datetime ON kline_5min_202401(stock_code, datetime);
`

---

## 5. 财务数据表设计

### 5.1 盈利能力数据表 (finance_profit)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| year | INTEGER | NOT NULL | 年份 |
| quarter | INTEGER | NOT NULL | 季度(1-4) |
| roe | DECIMAL(10,4) | | 净资产收益率(%) |
| roa | DECIMAL(10,4) | | 总资产收益率(%) |
| gross_profit_rate | DECIMAL(10,4) | | 毛利率(%) |
| net_profit_rate | DECIMAL(10,4) | | 净利率(%) |
| eps | DECIMAL(10,4) | | 每股收益(元) |
| total_share | DECIMAL(18,4) | | 总股本(万股) |
| liqa_share | DECIMAL(18,4) | | 流通股本(万股) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE finance_profit (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    roe DECIMAL(10,4),
    roa DECIMAL(10,4),
    gross_profit_rate DECIMAL(10,4),
    net_profit_rate DECIMAL(10,4),
    eps DECIMAL(10,4),
    total_share DECIMAL(18,4),
    liqa_share DECIMAL(18,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_finance_profit_stock_year_quarter ON finance_profit(stock_code, year, quarter);
CREATE INDEX idx_finance_profit_year ON finance_profit(year);
`

### 5.2 营运能力数据表 (finance_operation)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| year | INTEGER | NOT NULL | 年份 |
| quarter | INTEGER | NOT NULL | 季度(1-4) |
| ar_turnover | DECIMAL(10,4) | | 应收账款周转率 |
| inventory_turnover | DECIMAL(10,4) | | 存货周转率 |
| current_asset_turnover | DECIMAL(10,4) | | 流动资产周转率 |
| total_asset_turnover | DECIMAL(10,4) | | 总资产周转率 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE finance_operation (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    ar_turnover DECIMAL(10,4),
    inventory_turnover DECIMAL(10,4),
    current_asset_turnover DECIMAL(10,4),
    total_asset_turnover DECIMAL(10,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_finance_operation_stock_year_quarter ON finance_operation(stock_code, year, quarter);
`

### 5.3 成长能力数据表 (finance_growth)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| year | INTEGER | NOT NULL | 年份 |
| quarter | INTEGER | NOT NULL | 季度(1-4) |
| revenue_growth_rate | DECIMAL(10,4) | | 营业收入增长率(%) |
| net_profit_growth_rate | DECIMAL(10,4) | | 净利润增长率(%) |
| asset_growth_rate | DECIMAL(10,4) | | 总资产增长率(%) |
| eps_growth_rate | DECIMAL(10,4) | | 每股收益增长率(%) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE finance_growth (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    revenue_growth_rate DECIMAL(10,4),
    net_profit_growth_rate DECIMAL(10,4),
    asset_growth_rate DECIMAL(10,4),
    eps_growth_rate DECIMAL(10,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_finance_growth_stock_year_quarter ON finance_growth(stock_code, year, quarter);
`

### 5.4 偿债能力数据表 (finance_balance)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| year | INTEGER | NOT NULL | 年份 |
| quarter | INTEGER | NOT NULL | 季度(1-4) |
| asset_liability_ratio | DECIMAL(10,4) | | 资产负债率(%) |
| current_ratio | DECIMAL(10,4) | | 流动比率 |
| quick_ratio | DECIMAL(10,4) | | 速动比率 |
| interest_coverage_ratio | DECIMAL(10,4) | | 利息保障倍数 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE finance_balance (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    asset_liability_ratio DECIMAL(10,4),
    current_ratio DECIMAL(10,4),
    quick_ratio DECIMAL(10,4),
    interest_coverage_ratio DECIMAL(10,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_finance_balance_stock_year_quarter ON finance_balance(stock_code, year, quarter);
`

### 5.5 现金流量数据表 (finance_cashflow)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| year | INTEGER | NOT NULL | 年份 |
| quarter | INTEGER | NOT NULL | 季度(1-4) |
| operating_cash_flow | DECIMAL(18,4) | | 经营活动现金流(万元) |
| investing_cash_flow | DECIMAL(18,4) | | 投资活动现金流(万元) |
| financing_cash_flow | DECIMAL(18,4) | | 筹资活动现金流(万元) |
| free_cash_flow | DECIMAL(18,4) | | 自由现金流(万元) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE finance_cashflow (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    operating_cash_flow DECIMAL(18,4),
    investing_cash_flow DECIMAL(18,4),
    financing_cash_flow DECIMAL(18,4),
    free_cash_flow DECIMAL(18,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_finance_cashflow_stock_year_quarter ON finance_cashflow(stock_code, year, quarter);
`

### 5.6 杜邦指标数据表 (finance_dupont)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| year | INTEGER | NOT NULL | 年份 |
| quarter | INTEGER | NOT NULL | 季度(1-4) |
| roe | DECIMAL(10,4) | | 净资产收益率(%) |
| net_profit_margin | DECIMAL(10,4) | | 销售净利率(%) |
| asset_turnover | DECIMAL(10,4) | | 总资产周转率 |
| equity_multiplier | DECIMAL(10,4) | | 权益乘数 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE finance_dupont (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    roe DECIMAL(10,4),
    net_profit_margin DECIMAL(10,4),
    asset_turnover DECIMAL(10,4),
    equity_multiplier DECIMAL(10,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_finance_dupont_stock_year_quarter ON finance_dupont(stock_code, year, quarter);
`

---

## 6. 公司报告表设计

### 6.1 业绩预告表 (report_forecast)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| report_date | DATE | NOT NULL | 报告日期 |
| year | INTEGER | NOT NULL | 报告年份 |
| quarter | INTEGER | NOT NULL | 报告季度(1-4) |
| type | VARCHAR(32) | | 预告类型(预增/预减/续盈/续亏/扭亏/首亏) |
| profit_low | DECIMAL(18,4) | | 预计净利润下限(万元) |
| profit_high | DECIMAL(18,4) | | 预计净利润上限(万元) |
| profit_change_low | DECIMAL(10,4) | | 预计变动幅度下限(%) |
| profit_change_high | DECIMAL(10,4) | | 预计变动幅度上限(%) |
| change_reason | TEXT | | 变动原因 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE report_forecast (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    report_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    type VARCHAR(32),
    profit_low DECIMAL(18,4),
    profit_high DECIMAL(18,4),
    profit_change_low DECIMAL(10,4),
    profit_change_high DECIMAL(10,4),
    change_reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_report_forecast_stock_code ON report_forecast(stock_code);
CREATE INDEX idx_report_forecast_report_date ON report_forecast(report_date);
`

### 6.2 业绩快报表 (report_express)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| report_date | DATE | NOT NULL | 报告日期 |
| year | INTEGER | NOT NULL | 报告年份 |
| quarter | INTEGER | NOT NULL | 报告季度(1-4) |
| revenue | DECIMAL(18,4) | | 营业收入(万元) |
| net_profit | DECIMAL(18,4) | | 净利润(万元) |
| eps | DECIMAL(10,4) | | 每股收益(元) |
| revenue_change | DECIMAL(10,4) | | 营收同比变动(%) |
| net_profit_change | DECIMAL(10,4) | | 净利润同比变动(%) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE report_express (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    report_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    revenue DECIMAL(18,4),
    net_profit DECIMAL(18,4),
    eps DECIMAL(10,4),
    revenue_change DECIMAL(10,4),
    net_profit_change DECIMAL(10,4),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_report_express_stock_code ON report_express(stock_code);
CREATE INDEX idx_report_express_report_date ON report_express(report_date);
`

### 6.3 分红信息表 (dividend_data)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| report_date | DATE | NOT NULL | 公告日期 |
| ex_date | DATE | | 除权除息日期 |
| pay_date | DATE | | 派息日期 |
| dividend_per_share | DECIMAL(10,4) | | 每股派息(元) |
| bonus_share_ratio | DECIMAL(10,4) | | 送股比例 |
| transfer_share_ratio | DECIMAL(10,4) | | 转增比例 |
| plan_status | VARCHAR(32) | | 方案状态(预案/实施) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE dividend_data (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    report_date DATE NOT NULL,
    ex_date DATE,
    pay_date DATE,
    dividend_per_share DECIMAL(10,4),
    bonus_share_ratio DECIMAL(10,4),
    transfer_share_ratio DECIMAL(10,4),
    plan_status VARCHAR(32),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dividend_data_stock_code ON dividend_data(stock_code);
CREATE INDEX idx_dividend_data_report_date ON dividend_data(report_date);
`

### 6.4 复权因子表 (adjust_factor)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGSERIAL | PRIMARY KEY | 自增主键 |
| stock_code | VARCHAR(16) | NOT NULL | 股票代码 |
| date | DATE | NOT NULL | 日期 |
| adjust_factor | DECIMAL(18,8) | NOT NULL | 复权因子 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**DDL:**
`sql
CREATE TABLE adjust_factor (
    id BIGSERIAL PRIMARY KEY,
    stock_code VARCHAR(16) NOT NULL REFERENCES stocks(code),
    date DATE NOT NULL,
    adjust_factor DECIMAL(18,8) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_adjust_factor_stock_date ON adjust_factor(stock_code, date);
`

---

## 7. MongoDB集合设计

### 7.1 问答历史集合 (chat_history)

**文档结构：**
`json
{
    "_id": "ObjectId",
    "user_id": "UUID字符串",
    "question": "用户提问内容",
    "reference_content": "引用的股票数据内容",
    "responses": [
        {
            "model": "qwen",
            "model_name": "通义千问",
            "response": "模型响应内容",
            "response_time": 1234
        }
    ],
    "trace_id": "链路追踪ID",
    "created_at": "ISODate"
}
`

**索引：**
`javascript
db.chat_history.createIndex({ user_id: 1, created_at: -1 });
db.chat_history.createIndex({ trace_id: 1 });
`

### 7.2 系统日志集合 (system_logs)

**文档结构：**
`json
{
    "_id": "ObjectId",
    "level": "debug/info/warn/error",
    "module": "模块名称",
    "message": "日志内容",
    "trace_id": "链路追踪ID",
    "context": {
        "request_id": "请求ID",
        "user_id": "用户ID",
        "task_id": "任务ID",
        "stock_code": "股票代码"
    },
    "duration": "响应时间(ms)",
    "created_at": "ISODate"
}
`

**索引：**
`javascript
db.system_logs.createIndex({ level: 1, created_at: -1 });
db.system_logs.createIndex({ module: 1, created_at: -1 });
db.system_logs.createIndex({ trace_id: 1 });
`

### 7.3 用户行为日志集合 (user_behavior)

**文档结构：**
`json
{
    "_id": "ObjectId",
    "user_id": "UUID字符串",
    "action": "操作类型(view/search/click/submit)",
    "target": "操作目标(stocks/stock_detail/tasks/chat)",
    "detail": {
        "stock_code": "股票代码",
        "keyword": "搜索关键词",
        "task_id": "任务ID"
    },
    "trace_id": "链路追踪ID",
    "duration": "停留时间(ms)",
    "created_at": "ISODate"
}
`

**索引：**
`javascript
db.user_behavior.createIndex({ user_id: 1, created_at: -1 });
db.user_behavior.createIndex({ action: 1, created_at: -1 });
db.user_behavior.createIndex({ target: 1, created_at: -1 });
`

---

## 8. Redis键设计

### 8.1 缓存键

| 键名格式 | 说明 | 过期时间 |
|----------|------|----------|
| stock:list | 股票列表缓存 | 5分钟 |
| stock:{code}:latest | 股票最新数据 | 1分钟 |
| stock:{code}:finance | 股票财务数据 | 30分钟 |
| kline:{code}:{period}:{date_range} | K线数据缓存 | 5分钟 |
| industry:list | 行业列表 | 1小时 |
| index:{code}:constituents | 指数成分股 | 1小时 |

### 8.2 Token键

| 键名格式 | 说明 | 过期时间 |
|----------|------|----------|
| token:access:{user_id} | Access Token | 2小时 |
| token:refresh:{user_id} | Refresh Token | 7天 |
| token:blacklist:{token} | Token黑名单 | 剩余有效期 |

### 8.3 任务进度键

| 键名格式 | 说明 | 过期时间 |
|----------|------|----------|
| task:progress:{execution_id} | 任务执行进度 | 24小时 |
| task:lock:{task_id} | 任务分布式锁 | 1小时 |

### 8.4 消息队列键

| 键名格式 | 说明 | 过期时间 |
|----------|------|----------|
| message:queue:{user_id} | 用户消息队列 | - |

---

## 9. etcd键设计

### 9.1 配置键

| 键名 | 说明 |
|------|------|
| /config/app/settings | 应用全局配置 |
| /config/database/postgres | PostgreSQL配置 |
| /config/database/redis | Redis配置 |
| /config/database/mongodb | MongoDB配置 |
| /config/auth/jwt | JWT配置 |
| /config/external/baostock | Baostock API配置 |
| /config/external/qwen | 通义千问配置 |
| /config/external/deepseek | DeepSeek配置 |

### 9.2 分布式锁键

| 键名 | 说明 |
|------|------|
| /lock/task/{task_id} | 任务执行锁 |
| /lock/scheduler/{scheduler_id} | 定时任务锁 |

---

## 10. 数据初始化

### 10.1 初始用户数据

`sql
INSERT INTO users (username, password_hash, role)
VALUES ('admin', '.rK4fl8x2q7Meu6Q6D2V5fF5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q', 'admin');
`

### 10.2 初始任务数据示例

`sql
INSERT INTO tasks (name, api_name, config_schema)
VALUES 
('获取A股日K数据', 'query_history_k_data_plus', '{
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "股票代码"},
        "start_date": {"type": "string", "format": "date", "description": "开始日期"},
        "end_date": {"type": "string", "format": "date", "description": "结束日期"},
        "frequency": {"type": "string", "enum": ["d", "w", "m"], "default": "d"},
        "adjustflag": {"type": "string", "enum": ["1", "2", "3"], "default": "3"}
    },
    "required": ["code", "start_date", "end_date"]
}'),
('获取盈利能力数据', 'query_profit_data', '{
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "股票代码"},
        "year": {"type": "integer", "description": "年份"},
        "quarter": {"type": "integer", "minimum": 1, "maximum": 4, "description": "季度"}
    },
    "required": ["code", "year", "quarter"]
}'),
('获取行业分类数据', 'query_stock_industry', '{
    "type": "object",
    "properties": {}
}'),
('获取上证50成分股', 'query_sz50_stocks', '{
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date", "description": "日期"}
    }
}'),
('获取沪深300成分股', 'query_hs300_stocks', '{
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date", "description": "日期"}
    }
}'),
('获取中证500成分股', 'query_zz500_stocks', '{
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date", "description": "日期"}
    }
}'),
('获取业绩预告数据', 'query_forcast_report', '{
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "股票代码"}
    }
}'),
('获取业绩快报数据', 'query_performance_express_report', '{
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "股票代码"}
    }
}'),
('获取分红数据', 'query_dividend_data', '{
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "股票代码"},
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date"}
    },
    "required": ["code"]
}'),
('获取复权因子数据', 'query_adjust_factor', '{
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": "股票代码"},
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date"}
    },
    "required": ["code"]
}');
`

---

## 11. 数据迁移策略

### 11.1 分表迁移

对于分钟级K线数据，需要定期创建新表：

1. **自动建表**：在应用启动时或数据写入前检查目标表是否存在，不存在则自动创建
2. **数据归档**：对于超过N个月的历史数据，可考虑归档到冷存储
3. **分区查询**：查询时根据日期范围自动路由到对应分表

### 11.2 缓存策略

1. **写穿透**：数据写入数据库后立即更新缓存
2. **读缓存**：查询时优先读取缓存，缓存未命中时查询数据库并更新缓存
3. **缓存失效**：数据更新时主动失效相关缓存

### 11.3 任务进度持久化

任务执行过程中定期将进度保存到：
1. **Redis**：实时进度，用于WebSocket推送
2. **PostgreSQL**：持久化进度，用于任务恢复

---

## 12. 数据关系总结

### 12.1 一对一关系（融合展示）
- stocks ↔ industry（通过industry_code字段）

### 12.2 一对多关系（列表展示）
- stocks ↔ finance_profit（多条年度/季度记录）
- stocks ↔ finance_operation
- stocks ↔ finance_growth
- stocks ↔ finance_balance
- stocks ↔ finance_cashflow
- stocks ↔ finance_dupont
- stocks ↔ report_forecast
- stocks ↔ report_express
- stocks ↔ dividend_data
- stocks ↔ adjust_factor
- stocks ↔ kline_day/kline_week/kline_month
- tasks ↔ task_executions

### 12.3 多对多关系（关联跳转）
- industry ↔ stocks（通过stock_industry关联表）
- stock_index ↔ stocks（通过index_constituent关联表）
