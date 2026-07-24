# practice-team6
team6小组实践
# 🎬 观影派对 (Viewing Party)

这是一个专为 Python 初学者设计的结对编程项目。通过为"观影派对"场景构建一套工具函数，你将练习并掌握条件判断、列表、字典、嵌套循环和数据结构等核心编程技能。

**现在，本项目已包含一个完整的 Web 前端界面！** 你可以通过浏览器直观地管理电影、添加好友，并一键获取各种电影推荐。

## 📖 项目背景

你和你的朋友们喜欢一起在线看电影。为了找出"你没看过但朋友看过"或"你看过但朋友没看过"的电影，你们不再需要费力地翻看电子表格，而是用 Python 程序来解决这个问题！

本项目通过测试驱动开发（TDD）的方式，引导你一步步完成一套功能函数，实现电影管理、数据统计和智能推荐。最终，这些核心函数被封装成了一个可直接运行的 Web 应用。

## ✨ 核心技能与特性

通过完成本项目，你将锻炼以下能力：

- 使用条件逻辑处理业务规则
- 操作和遍历列表、字典等数据结构
- 处理嵌套循环和复杂数据结构
- 践行**结对编程 (Pair Programming)** 的最佳实践
- 使用 **Git 和 GitHub** 进行团队协作
- **（新增）** 使用 **Flask** 框架将 Python 函数转化为 Web API
- **（新增）** 使用 **HTML, CSS, JavaScript** 构建交互式前端界面

## 🚀 快速开始（网页版）

这是体验项目功能最直观的方式。

### 前置要求

- Python 3.6+
- `pip` (Python 包管理工具)
- Git

### 安装与运行

1.  **克隆仓库**

    `git clone https://github.com/BISTU-OSSD/practice-team6.git`

    `cd practice-team6/viewing-party`

2.  **创建并激活虚拟环境** (推荐)

    `python3 -m venv venv`

    `source venv/bin/activate`  # Linux/macOS

    或 `.\venv\Scripts\activate`  # Windows

3.  **安装依赖**

    项目依赖已更新，现在包含 `Flask`。

    `pip install -r requirements.txt`

4.  **启动 Flask 应用**

    `python app.py`

    终端会显示以下信息，表示服务已启动：

    `* Running on http://127.0.0.1:5000`

5.  **访问网页**

    打开浏览器，访问 `http://127.0.0.1:5000`。你现在就可以：

    - 输入用户名登录
    - 添加电影（标题、类型、评分）
    - 标记电影为"已看"或加入"想看"
    - 添加好友
    - 点击 **"我的独享电影"**、**"订阅推荐"** 等按钮，体验推荐系统

> **注意**：首次使用时，为了让推荐功能有数据，建议你在普通窗口和一个无痕窗口分别以不同用户名登录，互相添加为好友，并各自添加一些电影。

## 🧪 仅运行核心测试 (无 Web 界面)

如果你只想测试背后的 Python 逻辑，可以忽略 Web 部分。

1.  **安装测试依赖** (如果你还没安装)

    `pip install pytest`

2.  **运行所有测试**

    `pytest`

## 🧑‍🤝‍🧑 团队协作指南

本项目通过 GitHub Issues 和 Pull Requests 进行协作。

### 1. 项目分工 (Issues)

项目按功能划分为 5 个 Wave，并打包成 4 个主要的开发任务（Issues），每个任务都对应一个独立的测试文件：

| Issue | 任务 (Wave) | 核心函数 | 难度 |
| :--- | :--- | :--- | :--- |
| **Issue 1** | **Wave 1: 基础数据操作** | `create_movie`, `add_to_watched`, `add_to_watchlist`, `watch_movie` | ⭐️ |
| **Issue 2** | **Wave 2: 数据统计** | `get_watched_avg_rating`, `get_most_watched_genre` | ⭐️⭐️ |
| **Issue 3** | **Wave 3: 个人与好友对比** | `get_unique_watched`, `get_friends_unique_watched` | ⭐️⭐️⭐️ |
| **Issue 4** | **Wave 4 & 5: 智能推荐系统** | `get_available_recs`, `get_new_rec_by_genre`, `get_rec_from_favorites` | ⭐️⭐️⭐️⭐️ |
| **Issue 5** | **Web 前端与 API 集成** | `app.py`, `templates/`, `static/` | ⭐️⭐️⭐️⭐️ |

每个 Issue 都关联了对应的 `Milestone`，方便追踪项目整体进度。

### 2. 开发流程 (基于 main 分支)

由于核心代码集中在 `party.py` 文件上，为避免代码冲突，请遵循以下工作流：

**第一步：领取任务**

在 GitHub Issues 页面，**Assign** 自己到要负责的 Issue。

**第二步：同步代码**

每次开始编码前，务必先从远程仓库拉取最新代码。

`git pull origin main`

**第三步：分区域开发**

在 `party.py` 文件中，按 Wave 区域编写自己的函数。**只修改自己负责的 Wave 区域**，避免与他人修改同一段代码。

**第四步：测试驱动开发 (TDD)**

- 激活对应的测试文件（如 `tests/test_wave_01.py`），找到对应的 `@pytest.mark.skip()` 并删除它来激活测试。
- 运行测试，观察失败信息。
- 在 `party.py` 中编写最少的代码让测试通过。
- 重复以上"失败-成功-重构"的循环，逐个函数推进。

`pytest tests/test_wave_01.py`

**第五步：提交代码**

完成一个函数或一个小功能后，及时提交，保持提交粒度小而清晰。

`git add party.py`

`git commit -m "[Wave 1] 完成 create_movie 函数"`

`git push origin main`

**第六步：创建 Pull Request 并关闭 Issue**

当你的代码准备好合并时，从你的分支向 `main` 分支发起 Pull Request。在 PR 描述中写 `Closes #Issue编号`，合并后关联的 Issue 会自动关闭。

## 📁 项目结构

```text
practice-team6/
└── viewing-party/                # 项目根目录
    ├── app.py                    # Flask Web 应用主程序
    ├── party.py                  # 核心功能函数库
    ├── requirements.txt          # 项目依赖 (包含 Flask)
    ├── templates/                # HTML 模板目录
    │   └── index.html            # 主页面
    ├── static/                   # 静态资源目录
    │   ├── css/
    │   │   └── style.css         # 样式文件
    │   └── js/
    │       └── main.js           # 前端交互脚本
    ├── tests/                    # 测试文件目录 (如有)
    │   ├── test_wave_01.py
    │   └── ...
    └── README.md                 # 项目说明
