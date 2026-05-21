"""
QiPing 数据库模型

包含以下表结构：
- Users: 用户信息
- Episodes: 漫剧剧集
- Scripts: 脚本内容
- Characters: 角色信息
- Scenes: 场景信息
- ViewHistory: 观看历史
- Comments: 评论
- Likes: 点赞
- AIGenerationJobs: AI 生成任务
- ContentRecommendations: 内容推荐
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, ForeignKey, JSON, Index, UniqueConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

Base = declarative_base()


class UserType(str, enum.Enum):
    """用户类型枚举"""
    VIEWER = "viewer"
    CREATOR = "creator"
    ADMIN = "admin"


class EpisodeStatus(str, enum.Enum):
    """剧集状态枚举"""
    DRAFT = "draft"
    PROCESSING = "processing"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class GenerationStatus(str, enum.Enum):
    """生成任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # 个人信息
    full_name = Column(String(120), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # 用户类型和状态
    user_type = Column(Enum(UserType), default=UserType.VIEWER)
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # 社交数据
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # 关系
    episodes = relationship("Episode", back_populates="creator")
    view_history = relationship("ViewHistory", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Episode(Base):
    """剧集表"""
    __tablename__ = "episodes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # 分类信息
    genre = Column(String(50), nullable=False, index=True)  # romance, fantasy, mystery etc
    style = Column(String(50), default="vertical_drama")  # 视频风格
    language = Column(String(20), default="zh-CN")
    
    # 内容数据
    thumbnail_url = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)  # 秒为单位
    episode_number = Column(Integer, nullable=True)
    season_number = Column(Integer, default=1)
    
    # 状态
    status = Column(Enum(EpisodeStatus), default=EpisodeStatus.DRAFT, index=True)
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # 数据统计
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # AI 生成数据
    ai_model_used = Column(JSON, nullable=True)  # 使用的 AI 模型信息
    ai_quality_score = Column(Float, nullable=True)
    generation_time = Column(Integer, nullable=True)  # 生成耗时（秒）
    
    # 外键
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # 关系
    creator = relationship("User", back_populates="episodes")
    scripts = relationship("Script", back_populates="episode", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="episode", cascade="all, delete-orphan")
    scenes = relationship("Scene", back_populates="episode", cascade="all, delete-orphan")
    view_history = relationship("ViewHistory", back_populates="episode", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="episode", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="episode", cascade="all, delete-orphan")
    ai_jobs = relationship("AIGenerationJob", back_populates="episode", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_creator_created', 'creator_id', 'created_at'),
        Index('idx_genre_published', 'genre', 'is_published'),
    )
    
    def __repr__(self):
        return f"<Episode {self.title}>"


class Script(Base):
    """脚本表"""
    __tablename__ = "scripts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    
    # AI 模型信息
    ai_model = Column(String(50), nullable=False)  # gpt-4, claude-3 etc
    prompt = Column(Text, nullable=True)  # 输入的 prompt
    
    # 质量评分
    quality_score = Column(Float, default=0.0)
    tokens_used = Column(Integer, nullable=True)
    generation_time = Column(Float, nullable=True)  # 秒
    
    # 外键
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    episode = relationship("Episode", back_populates="scripts")
    
    def __repr__(self):
        return f"<Script for {self.episode_id}>"


class Character(Base):
    """角色表"""
    __tablename__ = "characters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    appearance = Column(Text, nullable=True)  # 外观描述
    personality = Column(Text, nullable=True)  # 性格描述
    role = Column(String(50), nullable=True)  # 主角、配角等
    
    # 媒体资源
    avatar_url = Column(String(500), nullable=True)
    voice_sample_url = Column(String(500), nullable=True)
    
    # 外键
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    episode = relationship("Episode", back_populates="characters")
    
    def __repr__(self):
        return f"<Character {self.name}>"


class Scene(Base):
    """场景表"""
    __tablename__ = "scenes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scene_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=True)
    
    # 媒体资源
    image_urls = Column(JSON, default=[])  # 场景图片 URL 列表
    video_url = Column(String(500), nullable=True)  # 场景视频
    audio_url = Column(String(500), nullable=True)  # 配音音频
    
    # 外键
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    episode = relationship("Episode", back_populates="scenes")
    
    def __repr__(self):
        return f"<Scene {self.scene_number}>"


class ViewHistory(Base):
    """观看历史表"""
    __tablename__ = "view_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 观看进度
    watch_time = Column(Integer, default=0)  # 秒
    progress = Column(Float, default=0.0)  # 0-100 百分比
    is_completed = Column(Boolean, default=False)
    
    # 外键
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    watched_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # 关系
    user = relationship("User", back_populates="view_history")
    episode = relationship("Episode", back_populates="view_history")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'episode_id', name='uq_user_episode_view'),
        Index('idx_user_watched', 'user_id', 'watched_at'),
    )
    
    def __repr__(self):
        return f"<ViewHistory user={self.user_id} episode={self.episode_id}>"


class Comment(Base):
    """评论表"""
    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    
    # 评论统计
    likes = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    
    # 外键
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    parent_comment_id = Column(String(36), ForeignKey("comments.id"), nullable=True)  # 回复
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="comments")
    episode = relationship("Episode", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment by {self.user_id}>"


class Like(Base):
    """点赞表"""
    __tablename__ = "likes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 外键
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="likes")
    episode = relationship("Episode", back_populates="likes")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'episode_id', name='uq_user_episode_like'),
    )
    
    def __repr__(self):
        return f"<Like user={self.user_id} episode={self.episode_id}>"


class AIGenerationJob(Base):
    """AI 生成任务表"""
    __tablename__ = "ai_generation_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 任务信息
    agent_type = Column(String(50), nullable=False, index=True)  # script, visual, voice etc
    status = Column(Enum(GenerationStatus), default=GenerationStatus.PENDING, index=True)
    
    # 输入输出
    input_params = Column(JSON, nullable=False)  # 输入参数
    output_result = Column(JSON, nullable=True)  # 输出结果
    error_message = Column(Text, nullable=True)  # 错误信息
    
    # 资源统计
    tokens_used = Column(Integer, nullable=True)  # LLM tokens
    processing_time = Column(Float, nullable=True)  # 秒
    cost = Column(Float, nullable=True)  # 成本
    
    # 外键
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # 关系
    episode = relationship("Episode", back_populates="ai_jobs")
    
    __table_args__ = (
        Index('idx_agent_status', 'agent_type', 'status'),
        Index('idx_episode_agent', 'episode_id', 'agent_type'),
    )
    
    def __repr__(self):
        return f"<AIGenerationJob {self.agent_type} - {self.status}>"


class ContentRecommendation(Base):
    """内容推荐表"""
    __tablename__ = "content_recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 推荐分数
    score = Column(Float, nullable=False)  # 0-1
    algorithm = Column(String(50), nullable=False)  # collaborative, content-based etc
    reason = Column(String(200), nullable=True)  # 推荐理由
    
    # 用户交互
    was_clicked = Column(Boolean, default=False)
    was_watched = Column(Boolean, default=False)
    
    # 外键
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False, index=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    clicked_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('idx_user_recommendation', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Recommendation score={self.score}>"
