# srapply-next

申荣留学全新官网项目（Python + Vue3），包含：

- 品牌展示官网（Home）
- 管理后台（线索列表 + 跟进状态更新）
- 智能客服聊天组件（网站内实时对话）
- 微信客服通知（访客发言后可推送到企业微信机器人）
- SQLite 线索入库（自动沉淀访客咨询）

## 项目结构

```text
srapply-next/
  backend/   # FastAPI
  frontend/  # Vue3 + Vite
```

## 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

`backend/.env` 可配置：

```env
WECHAT_WEBHOOK_URL=
LLM_API_URL=
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini
JWT_SECRET=srapply-dev-secret
JWT_EXPIRE_SECONDS=28800
```

- 若配置 `LLM_API_URL + LLM_API_KEY`，聊天将调用真实模型接口。
- 若未配置，自动回退到本地规则客服回复。

## 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问：

- 官网: `http://127.0.0.1:5173`
- 管理页: `http://127.0.0.1:5173/admin`
- 后端文档: `http://127.0.0.1:8000/docs`

## 核心接口

- `POST /api/chat/visitor` 访客聊天 + 自动线索入库 + 微信通知
- `POST /api/auth/login` 管理后台登录（JWT）
- `GET /api/admin/leads` 获取线索列表
- `PATCH /api/admin/leads/{lead_id}/status` 更新线索跟进状态
- `PATCH /api/admin/leads/{lead_id}/assign` 分配客服
- `GET /api/admin/leads/{lead_id}/messages` 聊天明细
- `GET/POST /api/cms/cases` 留学案例 CMS
- `GET/POST /api/cms/advisors` 顾问团队 CMS
- `POST /api/analytics/track` 埋点上报
- `GET /api/analytics/summary` 转化率/页面热区

## 管理员默认账号（首次启动自动写入）

- `admin / admin123`（admin）
- `consultant / consult123`（consultant）
- `operator / oper123`（operator）
