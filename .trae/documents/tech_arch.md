## 1. Architecture Design

\\\mermaid
flowchart LR
    A[Frontend] --> B[Backend API]
    B --> C[(PostgreSQL)]
    B --> D[(Redis)]
    B --> E[(MongoDB)]
    B --> F[External APIs]
    
    subgraph Frontend
        A1[Vue 3 + TypeScript]
        A2[Vue Router]
        A3[Pinia]
        A4[Tailwind CSS]
        A5[ECharts]
        A6[Lucide Icons]
    end
    
    subgraph Backend API
        B1[FastAPI]
        B2[SQLAlchemy]
        B3[Authentication]
        B4[Task Scheduler]
    end
\\\

## 2. Technology Description
- Frontend: Vue 3 + TypeScript + Vite
- Routing: Vue Router 4
- State Management: Pinia
- Styling: Tailwind CSS 3
- Charts: ECharts
- Icons: Lucide Vue
- HTTP Client: Axios
- Backend: FastAPI (existing)
- Database: PostgreSQL (existing)

## 3. Route Definitions

| Route | Purpose | Component |
|-------|---------|-----------|
| /login | Login Page | Login.vue |
| /register | Register Page | Register.vue |
| / | Home Page | Home.vue |
| /stocks | Stock List | StockList.vue |
| /stocks/:code | Stock Detail | StockDetail.vue |
| /industries | Industry Analysis | Industry.vue |
| /tasks | Task Management | TaskManager.vue |
| /messages | Messages | Messages.vue |

## 4. API Definitions

### 4.1 Authentication API

POST /auth/register
- Request: { username: string, password: string }
- Response: User object

POST /auth/login
- Request: { username: string, password: string }
- Response: { access_token: string, token_type: string }

GET /auth/me
- Headers: Authorization: Bearer token
- Response: User object

### 4.2 Stock API

GET /stocks
- Query: industry_code?, type?, keyword?, page=1, page_size=20
- Response: Paged stock data

GET /stocks/{code}
- Response: Stock object

GET /stocks/{code}/detail
- Response: Stock detail with industry name

GET /stocks/{code}/kline/day
- Query: start_date?, end_date?, limit=100
- Response: KLine array

### 4.3 Finance API

GET /finance/{stock_code}/summary
- Query: year, quarter
- Response: Finance summary

GET /finance/{stock_code}/profit
- Query: limit=20
- Response: FinanceProfit array

GET /finance/{stock_code}/dividend
- Query: limit=20
- Response: DividendData array

## 5. Data Model

### 5.1 Frontend Data Types

interface Stock {
  code: string
  name: string
  industry_code: string | null
  exchange: string | null
  type: string
}

interface KLine {
  id: number
  stock_code: string
  date: string
  open: number
  close: number
  high: number
  low: number
  volume: number
  pct_chg: number | null
}

interface Task {
  id: string
  name: string
  api_name: string
  status: string
}

interface Message {
  id: string
  user_id: string
  title: string
  content: string
  type: string
  status: string
}

## 6. Project Structure

frontend/
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   ├── Stock/
│   │   ├── Finance/
│   │   ├── Task/
│   │   └── Common/
│   ├── views/
│   │   ├── Login.vue
│   │   ├── Home.vue
│   │   ├── StockList.vue
│   │   ├── StockDetail.vue
│   │   ├── Industry.vue
│   │   ├── TaskManager.vue
│   │   └── Messages.vue
│   ├── stores/
│   ├── composables/
│   ├── utils/
│   ├── router/
│   ├── styles/
│   ├── App.vue
│   └── main.ts
└── package.json
