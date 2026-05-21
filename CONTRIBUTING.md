# 贡献指南

感谢你对 QiPing AI 漫剧智能体项目的贡献！

## 📋 行为准则

我们的社区致力于为所有人提供一个尊重和包容的环境。请阅读并遵守我们的 [行为准则](./CODE_OF_CONDUCT.md)。

## 🚀 开始贡献

### 1. Fork 项目

点击 GitHub 页面右上角的 Fork 按钮，将项目复制到你的账户。

### 2. 克隆你的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/qiping.git
cd qiping
git remote add upstream https://github.com/tiankeshan/qiping.git
```

### 3. 创建特性分支

```bash
git checkout -b feature/your-feature-name
# 或者修复 Bug
git checkout -b bugfix/issue-description
```

### 4. 开发和测试

```bash
# 安装依赖
pip install -r backend/requirements.txt
npm install  # 前端

# 运行测试
pytest backend/tests/
npm test     # 前端

# 启动开发环境
docker-compose up -d
```

### 5. 提交改动

```bash
# 遵循 Conventional Commits 规范
git add .
git commit -m "feat: add new AI agent feature"
# 或
git commit -m "fix: resolve issue with script generation"
```

**提交信息格式:**
- `feat:` 新功能
- `fix:` 修复 Bug
- `docs:` 文档更新
- `style:` 代码风格改进
- `refactor:` 代码重构
- `test:` 添加或改进测试
- `chore:` 构建、依赖等杂项

### 6. 推送到你的 Fork

```bash
git push origin feature/your-feature-name
```

### 7. 创建 Pull Request

1. 访问原始仓库
2. 点击 "New Pull Request" 按钮
3. 选择你的分支和目标分支
4. 填写 PR 描述，说明你的改动内容
5. 点击 "Create Pull Request"

## 📝 PR 描述模板

```markdown
## 描述
简要描述你的改动内容。

## 相关问题
关闭 #123

## 改动类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 性能改进

## 测试
描述你测试了什么以及如何测试。

- [ ] 在本地测试通过
- [ ] 添加了单元测试
- [ ] 添加了集成测试

## 检查清单
- [ ] 代码遵循项目风格指南
- [ ] 自审查了代码
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 改动没有产生新的警告
```

## 🏗️ 项目结构

```
qiping/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── agents/         # AI 智能体实现
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   ├── db/             # 数据库操作
│   │   ├── core/           # 核心配置
│   │   └── tasks/          # Celery 任务
│   ├── tests/              # 测试文件
│   ├── main.py            # 应用入口
│   └── requirements.txt    # Python 依赖
├── frontend/               # React 前端
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   └── hooks/
│   ├── tests/
│   └── package.json
├── docs/                   # 文档
├── nginx/                  # Nginx 配置
└── docker-compose.yml      # Docker 编排
```

## 📚 开发指南

### 后端开发

**代码风格:**
- 遵循 PEP 8 规范
- 使用类型提示
- 添加 docstring

```python
def generate_script(title: str, genre: str) -> ScriptResponse:
    """
    生成漫剧脚本。
    
    Args:
        title: 剧集标题
        genre: 剧集类型
    
    Returns:
        ScriptResponse: 生成的脚本响应
    
    Raises:
        ValueError: 如果输入无效
    """
    pass
```

**测试:**
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest backend/tests/test_agents.py

# 显示覆盖率
pytest --cov=app
```

### 前端开发

**代码风格:**
- 使用 ESLint 检查
- 遵循 Prettier 格式
- 添加 JSDoc 注释

```javascript
/**
 * 生成漫剧脚本
 * @param {string} title - 剧集标题
 * @param {string} genre - 剧集类型
 * @returns {Promise<ScriptResponse>} 生成的脚本
 */
async function generateScript(title, genre) {
  // 实现
}
```

## 🐛 报告 Bug

1. 检查是否已存在相同的 Issue
2. 创建新的 Issue，包含以下信息：
   - 清晰的标题和描述
   - 复现步骤
   - 期望的行为
   - 实际行为
   - 截图或日志

## 💡 建议新功能

1. 开启讨论或 Issue
2. 解释为什么这个功能有用
3. 列出可能的实现方案

## 📖 文档

- 使用 Markdown 格式
- 添加代码示例
- 保持更新

## 🔍 代码审查

所有提交都需要经过代码审查。审查者会检查：

- ✅ 代码质量和风格
- ✅ 功能是否正确
- ✅ 是否有充分的测试
- ✅ 文档是否完整
- ✅ 性能影响

## 📝 其他资源

- [完整文档](./docs/)
- [API 文档](./docs/api.md)
- [架构设计](./docs/architecture.md)
- [部署指南](./docs/deployment.md)

## 🙏 感谢

感谢你的贡献！你的努力使这个项目变得更好。

---

**需要帮助？** 
- 在 Issues 中提问
- 参与 Discussions
- 联系维护者

Happy coding! 🎉
