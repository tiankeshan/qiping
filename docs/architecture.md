# 系统架构设计文档

## 📊 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     React 前端应用                       │
│         (创作者平台 + 观众应用 + 后台管理)               │
└────────────────┬────────────────────────────────────────┘
                 │ REST API / WebSocket
┌─────────────────────────────────────────────────────────┐
│                    FastAPI 后端服务                      │
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
│PostgreSQL │ Redis  │ Celery  │
│(数据库)   │(缓存) │(队列)  │
└───────────┘ └────────┘ └────────┘
```

## 🤖 五大 AI 智能体设计

### 1. Script Agent (脚本生成智能体)

**功能:**
- 基于创意提示自动生成完整脚本
- 支持多种类型和风格
- 角色对话自动生成
- 场景描述智能补充

**技术栈:**
- OpenAI GPT-4 / Claude 3
- Prompt Engineering
- Jinja2 模板引擎

**API 端点:**
```
POST /api/agents/script
{
  "title": "CEO和快递员的爱情故事",
  "genre": "romance",
  "premise": "高冷女CEO与热情快递员相遇后的故事",
  "episodes": 5,
  "style": "vertical_drama"
}
```

**输出:**
```json
{
  "script_id": "script_001",
  "title": "CEO和快递员的爱情故事",
  "scenes": [
    {
      "scene_no": 1,
      "location": "办公室",
      "description": "...",
      "dialogues": [
        {"character": "CEO女主", "text": "..."}
      ]
    }
  ]
}
```

### 2. Visual Agent (漫画绘制智能体)

**功能:**
- 根据脚本自动生成漫画风格的图像
- 支持多种艺术风格 (Anime, Realistic, Watercolor等)
- 角色一致性保证
- 场景美学优化

**技术栈:**
- Midjourney API / Stability AI
- DALL-E 3
- ComfyUI (本地方案)

**API 端点:**
```
POST /api/agents/visual
{
  "script_id": "script_001",
  "character_descriptions": [
    {
      "name": "CEO女主",
      "appearance": "长黑色直发，穿着黑色职业套装",
      "expression": "冷漠沉着"
    }
  ],
  "art_style": "anime",
  "resolution": "1080x1920"
}
```

**输出:**
```json
{
  "visual_id": "visual_001",
  "images": [
    {
      "scene_no": 1,
      "url": "s3://bucket/images/scene_001.jpg",
      "width": 1080,
      "height": 1920
    }
  ]
}
```

### 3. Voice Agent (配音智能体)

**功能:**
- 多语言文本转语音
- 自然语调和情感表达
- 自动字幕生成
- 音频编辑和优化

**技术栈:**
- Google Cloud Text-to-Speech
- Azure Speech Services
- 音频处理 (librosa, pydub)

**API 端点:**
```
POST /api/agents/voice
{
  "episode_id": "ep_001",
  "script_content": "你就是我的快递员...",
  "language": "zh-CN",
  "voice_characteristics": {
    "gender": "female",
    "age": "20-30",
    "emotion": "romantic"
  }
}
```

**输出:**
```json
{
  "audio_id": "audio_001",
  "audio_url": "s3://bucket/audio/ep_001.mp3",
  "subtitles": [
    {
      "start_time": 0.5,
      "end_time": 2.3,
      "text": "你就是我的快递员..."
    }
  ]
}
```

### 4. Recommendation Agent (推荐智能体)

**功能:**
- 个性化内容推荐
- 协同过滤算法
- 基于内容相似度推荐
- 用户行为分析

**技术栈:**
- Collaborative Filtering
- Content-Based Filtering
- Matrix Factorization (Surprise库)
- Redis 缓存

**API 端点:**
```
GET /api/agents/recommendations
  ?user_id=user_123
  &limit=10
  &genre=romance
```

**输出:**
```json
{
  "recommendations": [
    {
      "episode_id": "ep_002",
      "title": "首席医生的爱情故事",
      "score": 0.95,
      "reason": "基于你对言情剧的喜好"
    }
  ]
}
```

### 5. Interactive Agent (实时互动智能体)

**功能:**
- 实时剧情分支选择
- 观众投票影响剧情
- 实时评论和互动
- 剧情动态生成

**技术栈:**
- WebSocket (fastapi-websocket)
- Redis Pub/Sub
- 事件驱动架构

**WebSocket 端点:**
```
WS /api/interactive/ws/{episode_id}

客户端发送:
{
  "type": "choice",
  "path": 1,
  "timestamp": "2024-01-01T00:00:00Z"
}

服务器响应:
{
  "type": "plot_update",
  "new_content": "...",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 💾 数据库设计

### 核心表结构

```sql
-- 剧集表
Episodes
  - id (PK)
  - title
  - genre
  - style
  - script_content
  - visual_urls
  - audio_url
  - status (draft, published, archived)
  - views, likes, rating
  - created_at, updated_at
  - creator_id (FK)

-- 脚本表
Scripts
  - id (PK)
  - episode_id (FK)
  - content
  - ai_model
  - quality_score
  - generation_time

-- 角色表
Characters
  - id (PK)
  - name
  - description
  - avatar_url
  - episode_id (FK)

-- 用户表
Users
  - id (PK)
  - username
  - email
  - password_hash
  - user_type (creator, viewer)
  - is_premium
  - followers, following
  - created_at

-- 观看历史表
ViewHistory
  - id (PK)
  - user_id (FK)
  - episode_id (FK)
  - watch_time
  - progress
  - completed_at

-- AI 生成任务表
AIGenerationJobs
  - id (PK)
  - episode_id (FK)
  - agent_type (script, visual, voice)
  - status (pending, processing, completed)
  - input_params (JSON)
  - output_result (JSON)
  - tokens_used
  - processing_time

-- 推荐表
ContentRecommendations
  - id (PK)
  - user_id (FK)
  - episode_id (FK)
  - score
  - algorithm
  - clicked, watched
```

## 🔄 工作流程

### 漫剧创作工作流

```
1. 创建新漫剧
   └─> Script Agent (生成脚本)
   └─> Visual Agent (生成漫画)
   └─> Voice Agent (生成配音)
   └─> Interactive Agent (设置互动)
   └─> 发布

2. 用户观看
   └─> 推荐系统推荐
   └─> 用户点击观看
   └─> 记录观看历史
   └─> 参与互动投票

3. 数据分析
   └─> 统计观看数据
   └─> 计算推荐分数
   └─> 优化算法
```

### API 调用流程

```
Frontend
  │
  ├─> POST /api/agents/script
  │   ├─> Script Agent (LLM)
  │   └─> Save to DB
  │
  ├─> POST /api/agents/visual
  │   ├─> Visual Agent (Image Generation)
  │   └─> Upload to S3
  │
  ├─> POST /api/agents/voice
  │   ├─> Voice Agent (TTS)
  │   └─> Upload to S3
  │
  ├─> GET /api/agents/recommendations
  │   └─> Redis Cache / Recommendation Agent
  │
  └─> WS /api/interactive/ws/{episode_id}
      └─> Real-time Updates
```

## 📈 扩展性设计

### 水平扩展

- **负载均衡**: Nginx 反向代理
- **数据库副本**: PostgreSQL 主从复制
- **缓存层**: Redis 集群
- **任务队列**: Celery 分布式
- **CDN**: 为媒体文件加速

### 垂直扩展

- **异步处理**: FastAPI + asyncio
- **缓存策略**: 多层缓存
- **数据库优化**: 索引、分片、归档

## 🔐 安全设计

- JWT 认证和授权
- HTTPS / TLS 加密
- SQL 注入防护 (SQLAlchemy ORM)
- XSS 防护 (CORS)
- 速率限制 (Rate Limiting)
- 文件上传验证

## 📊 性能优化

- 查询优化: 数据库索引、连接池
- 缓存策略: Redis 缓存热数据
- CDN: 媒体文件加速
- 异步处理: 后台任务队列
- 数据压缩: 音视频压缩

## 🚀 部署架构

```
Internet
  │
  └─> Nginx (负载均衡/反向代理)
      │
      ├─> FastAPI Backend (多实例)
      ├─> React Frontend
      ├─> PostgreSQL (主)
      ├─> Redis Cluster
      └─> Celery Workers
```

---

**下一步:** 继续实现具体的智能体逻辑和前端界面！🚀
