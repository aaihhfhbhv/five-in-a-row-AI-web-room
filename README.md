# 🎮 五子棋AI联机对战平台（MCTS强化学习 \+ 多人房间联机）

**基于 PyTorch \+ Flask \+ Vue3 开发的完整五子棋AI联机项目**

🔥 原项目AI算法基础上二次开发，新增：**多人联机房间、AI自动托管、规范悔棋、认输、8×8/15×15双棋盘适配**

⭐ 适合毕业设计、课程设计、后端实战、AI博弈学习

---

## 📌 项目介绍

本项目基于开源AlphaGo式五子棋AI算法（MCTS蒙特卡洛树搜索\+策略价值网络）进行二次开发，从单纯的**本地人机Demo**升级为**完整Web联机对战平台**。

支持：人机对战、多人建房联机、AI自动落子托管、悔棋、认输、自动判胜负、房间超时回收等完整业务逻辑。

## ✨ 项目亮点

- **🤖 AI强化学习博弈**：MCTS树搜索 \+ PyTorch策略价值网络，棋力强劲

- **🏠 多人联机房间系统**：随机房间ID、建房/加房/超时自动销毁

- **🎯 双棋盘尺寸适配**：完美支持 8×8 / 15×15 两种棋盘

- **🤝 完善联机功能**：AI托管、规范悔棋、认输、回合锁定、防作弊

- **⚡ 高性能后端**：模型全局预加载、AI计算锁、防并发卡顿

- **💖 前端动态效果**：Vue3 \+ Live2D看板娘 \+ 动态棋盘

---

## 🏗 项目架构

```Plain Text
five-in-a-row-AI-web-room
├── ai/                # AI训练核心、MCTS、神经网络
├── back-end/          # Flask后端接口、房间管理、对局逻辑
├── front-end/         # Vue3+TS前端页面、棋盘渲染、Live2D
├── .gitignore         # 仓库忽略配置
├── requirements.txt   # Python依赖
└── README.md          # 项目说明

```

### 技术栈

- **后端**：Python / Flask / Flask\-RESTful

- **AI算法**：PyTorch / MCTS蒙特卡洛树搜索 / 强化学习

- **前端**：Vue3 / TypeScript / Canvas / Live2D

---

## 🎮 功能介绍

### 1\. 联机房间系统

- 创建房间、随机6位房间ID

- 加入房间、双人匹配对战

- 5分钟无人匹配自动回收房间，节省资源

### 2\. AI自动托管对战

- 玩家开启托管后AI自动思考落子

- 8×8棋盘：深度MCTS模型推演

- 15×15棋盘：高性能启发式AI

### 3\. 规范悔棋机制（联机核心）

- 仅上一手落子玩家可申请悔棋

- 同意悔棋后锁定，必须再次落子才能解锁

- 拒绝悔棋不锁定，可继续申请

### 4\. 完整对局控制

- 自动识别横竖斜五连子、判定胜负

- 玩家认输功能

- 对局结束锁定所有操作

---

## 🚀 快速部署

### 1\. 克隆项目

```Plain Text
git clone https://github.com/aaihhfhbhv/five-in-a-row-AI-web-room.git
cd five-in-a-row-AI-web-room
```

### 2\. 安装依赖

```Plain Text
pip install -r requirements.txt
```

### 3\. 启动后端服务

```Plain Text
cd back-end
python main.py
```

默认运行地址：`http://127.0.0.1:5001`

---

## 💡 项目优化点（本人二次开发新增）

- 修复原版8×8棋盘AI落子错乱BUG

- 全局模型预加载，解决重复加载卡顿

- 新增独立AI计算棋盘，不污染对局状态

- 完整联机房间逻辑、状态锁、权限校验

- 规范可商用的悔棋、认输、回合机制

---

## 📄 开源说明

本项目基于开源项目二次开发，完全开源免费，仅供学习与交流。

欢迎 Star ⭐、Fork、一起学习进步！

**GitHub地址：**[https://github\.com/aaihhfhbhv/five\-in\-a\-row\-AI\-web\-room](https://github.com/aaihhfhbhv/five-in-a-row-AI-web-room)

> （注：部分内容可能由 AI 生成）