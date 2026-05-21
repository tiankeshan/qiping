# 🎬 QiPing - AI 漫剧智能体平台

基于市场最火爆的 AI 短剧平台（ReelShort、DramaBox、Popshort.ai）的设计理念，打造的开源 **AI 漫剧创作智能体系统**。

## ✨ 核心特性

- 🤖 **5大AI智能体** - 脚本生成、漫画绘制、配音、推荐、互动
- 🎨 **实时生成** - 一行创意提示，秒生成完整漫剧剧集
- 🌍 **多语言支持** - 自动翻译、配音、本地化
- 📱 **垂直视频** - 原生支持TikTok/YouTube Shorts格式
- 🔄 **实时互动** - WebSocket支持观众与剧情实时互动
- 🚀 **完全开源** - MIT License，支持本地部署
- 💾 **云端存储** - 集成多个云存储方案

## 📊 对标分析

| 功能 | ReelShort | DramaBox | 本项目 |
|------|-----------|----------|--------|
| AI脚本生成 | ✅ | ✅ | ✅ |
| AI绘图 | ✅ | ⚠️ | ✅ |
| 多语言配音 | ✅ | ✅ | ✅ |
| **实时互动** | ❌ | ❌ | ✅ |
| **开源可部署** | ❌ | ❌ | ✅ |
| 个性化推荐 | ✅ | ✅ | ✅ |

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     React前端应用                        │
│         (创作者平台 + 观众应用 + 后台管理)               │
└────────────────┬────────────────────────────────────────┘
                 │ REST API / WebSocket
┌─────────────────────────────────────────────────────────┐
│                    FastAPI后端服务                       │
│  ┌──────────┬──────────┬──────────┬──────────────────┐  │
│  │ Script   │ Visual   │ Voice    │ Recommendation   │  │
│  │ Agent    │ Agent    │ Agent    │ Agent            │  │
│  └──────────┴──────────┴──────────┴──────────────────┘  │
│  ┌──────────────────────────────────────────────────┐   │
│  │        Interactive Agent (WebSocket)             │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
┌────▼────┐ ┌────▼────┐ ┌───▼────┐
│ PostgreSQL │ Redis  │ Celery  │
│ (数据库)   │ (缓存) │ (队列)  │
└───────────┘ └────────┘ └────────┘
```

## 🚀 快速开始

### 前置条件
- Docker & Docker Compose
- Python 3.9+
- Node.js 16+
- API密钥：OpenAI, Midjourney (可选)

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/tiankeshan/qiping.git
cd qiping

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入API密钥

# 3. 启动所有服务
docker-compose up -d

# 4. 初始化数据库
docker-compose exec backend python -m alembic upgrade head

# 5. 访问应用
# 后端API文档: http://localhost:8000/docs
# 前端应用: http://localhost:3000
```

## 📚 API 快速参考

### 脚本生成智能体
```bash
POST /api/agents/script
{
  "title": "CEO和快递员的爱情故事",
  "genre": "romance",
  "premise": "高冷女CEO与热情快递员相遇后的故事",
  "episodes": 5,
  "style": "vertical_drama"
}
```

### 漫画绘制智能体
```bash
POST /api/agents/visual
{
  "script": "第一幕：办公室。CEO正在处理文件...",
  "character_descriptions": ["高冷女CEO, 28岁, 黑色职业装"],
  "art_style": "anime"
}
```

### 配音智能体
```bash
POST /api/agents/voice
{
  "episode_id": "ep_001",
  "text": "你就是我的quick delivery...",
  "language": "zh-CN",
  "voice": "female_v1"
}
```

### 推荐智能体
```bash
GET /api/agents/recommendations?user_id=user_123&limit=10
```

### 实时互动
```
WS /api/interactive/ws/{episode_id}
# 实时接收剧情更新和观众互动数据
```

## 📁 项目结构

```
qiping/
├── backend/                    # FastAPI后端
│   ├── app/
│   │   ├── agents/            # 5大AI智能体
│   │   │   ├── script_agent.py
│   │   │   ├── visual_agent.py
│   │   │   ├── voice_agent.py
│   │   │   ├── recommendation_agent.py
│   │   │   └── interactive_agent.py
│   │   ├── api/               # API路由
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 业务逻辑
│   │   └── core/              # 配置和工具
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # React前端
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── services/
│   └── package.json
├── docs/                       # 文档
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
├── docker-compose.yml
└── README.md
```

## 🔧 技术栈

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **任务队列**: Celery
- **缓存**: Redis
- **数据库**: PostgreSQL
- **AI模型**: OpenAI GPT-4, Claude 3, Midjourney, Stability AI

### 前端
- **框架**: React 18
- **UI库**: TailwindCSS, Ant Design
- **状态管理**: Redux Toolkit
- **实时通信**: Socket.io

### 部署
- **容器化**: Docker
- **编排**: Docker Compose / Kubernetes
- **CDN**: 集成多云存储

## 📖 文档

- [完整架构设计](./docs/architecture.md)
- [API文档](./docs/api.md)
- [部署指南](./docs/deployment.md)
- [贡献指南](./CONTRIBUTING.md)

## 🎯 功能路线图

- [x] 项目初始化
- [x] 基础架构搭建
- [ ] Script Agent 完整实现
- [ ] Visual Agent 完整实现
- [ ] Voice Agent 完整实现
- [ ] Recommendation Agent 完整实现
- [ ] Interactive Agent 完整实现
- [ ] 前端UI开发
- [ ] 移动端适配
- [ ] 性能优化
- [ ] 生产环境部署

## 💡 使用场景

1. **内容创作者** - 快速生成高质量漫剧内容
2. **短视频平台** - 自动化内容生成和推荐
3. **广告营销** - 定制化广告漫剧
4. **教育培训** - 个性化学习内容
5. **游戏叙事** - 动态故事生成

## 🤝 贡献

欢迎贡献代码！请参考 [贡献指南](./CONTRIBUTING.md)

```bash
# 1. Fork 项目
# 2. 创建功能分支
git checkout -b feature/amazing-feature
# 3. 提交改动
git commit -m 'Add amazing feature'
# 4. 推送到分支
git push origin feature/amazing-feature
# 5. 打开 Pull Request
```

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

## 📧 联系方式

- Issues: [GitHub Issues](https://github.com/tiankeshan/qiping/issues)
- 讨论: [GitHub Discussions](https://github.com/tiankeshan/qiping/discussions)
- Email: tiankeshan@example.com

---

**⭐ 如果你觉得这个项目有帮助，请给个Star！**
