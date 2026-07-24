# 🤝 贡献指南

感谢你对「观影派对」项目的关注！这是一个为 Python 初学者设计的协作学习项目，欢迎任何形式的贡献。

## 📖 项目简介

「观影派对」是一个通过测试驱动开发（TDD）方式学习 Python 的练习项目。项目包含 5 个 Wave 的功能模块，从基础数据操作到智能推荐系统，循序渐进地练习 Python 核心编程技能。

**项目现已包含完整的 Web 前端界面**，你可以通过浏览器直观地管理电影、添加好友并体验推荐系统。

## 🎯 贡献方式

### 1. 💡 通过 Issue 认领任务

本项目已在 GitHub Issues 中按 Wave 划分好开发任务，每个 Issue 对应一个独立的功能模块：

| Issue | 任务 (Wave) | 核心函数 | 难度 |
| :--- | :--- | :--- | :--- |
| **Issue 1** | Wave 1: 基础数据操作 | `create_movie`, `add_to_watched`, `add_to_watchlist`, `watch_movie` | ⭐️ |
| **Issue 2** | Wave 2: 数据统计 | `get_watched_avg_rating`, `get_most_watched_genre` | ⭐️⭐️ |
| **Issue 3** | Wave 3: 个人与好友对比 | `get_unique_watched`, `get_friends_unique_watched` | ⭐️⭐️⭐️ |
| **Issue 4** | Wave 4 & 5: 智能推荐系统 | `get_available_recs`, `get_new_rec_by_genre`, `get_rec_from_favorites` | ⭐️⭐️⭐️⭐️ |
| **Issue 5** | Web 前端与 API 集成 | `app.py`, `templates/`, `static/` | ⭐️⭐️⭐️⭐️ |

**认领方式**：在对应 Issue 下评论 `/assign` 或联系仓库管理员将你 Assign 到该 Issue。

### 2. 🐛 报告 Bug

如果你发现代码中的问题：
1. 先搜索已有 Issues，确认该 Bug 未被报告
2. 使用 **Bug Report** 模板创建新 Issue
3. 提供详细的复现步骤和预期行为

### 3. 💬 参与讨论

- 在现有 Issue 评论区分享你的想法
- 帮助解答其他贡献者的问题
- 提出改进建议


def get_watched_avg_rating(user_data):
    # ...
