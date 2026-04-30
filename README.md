
🎮 Game Art Pipeline — 多Agent游戏创作系统
输入一组主题关键词，自动流水线生成完整独立游戏项目包：世界观、角色设计、游戏原型、宣传海报、发行文案。
架构图
```
[主题关键词]
     ↓
WorldbuildingAgent  →  game_concept.json    (世界观/关卡/角色设定)
     ↓
CharacterAgent      →  character_designs.json (角色外观 + SD/MJ提示词)
     ↓
CodeAgent           →  game.html             (HTML5可玩游戏原型)
     ↓
PosterAgent         →  poster.html           (CSS动画宣传海报)
     ↓
PublisherAgent      →  publish_kit.json      (Steam/TapTap/微博文案)
     ↓
Orchestrator        →  report.html           (项目总览报告)
```
快速开始
1. 安装依赖
```bash
pip install -r requirements.txt
```
2. 配置 API Key
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```
3A. 命令行模式
```bash
python main.py --theme "赛博朋克 孤独 记忆"
python main.py --theme "古风武侠 羁绊 复仇" --output my_game
python main.py --theme "海洋探索 神秘 生存" --skip code poster  # 跳过某些步骤
```
3B. Web UI 模式
```bash
cd web_ui
python app.py
# 打开浏览器访问 http://localhost:5000
```
输出文件说明
文件	内容
`game_concept.json`	游戏世界观、关卡设计、美术方向
`character_designs.json`	角色外观描述 + Stable Diffusion / Midjourney 提示词
`game.html`	HTML5 Canvas 可玩游戏原型（直接在浏览器打开）
`poster.html`	CSS动画游戏宣传海报（1080×1920 竖版）
`publish_kit.json`	Steam详情页、TapTap简介、新闻稿、社交媒体文案
`report.html`	完整项目总结报告
Agent 说明
WorldbuildingAgent
职责：根据关键词生成完整游戏概念
输出：标题、背景、主角/反派、关卡设计、美术风格、色彩方案
CharacterAgent
职责：设计角色外观，生成AI绘图提示词
输出：3个角色（主角/反派/NPC）的详细设计 + SD/MJ提示词
CodeAgent
职责：生成可运行的HTML5游戏原型
输出：单文件HTML，包含主菜单、游戏主体、结算界面、粒子效果
PosterAgent
职责：制作视觉冲击力强的游戏宣传海报
输出：单文件HTML，含CSS动画、精美排版
PublisherAgent
职责：撰写全平台发行文案
输出：Steam详情页（含系统需求）、TapTap简介、新闻稿、Twitter/微博/Discord文案
扩展建议
接入 Stable Diffusion API 自动生成角色立绘
接入 Suno/Udio API 生成游戏配乐
接入 Unity WebGL 生成更完整的游戏原型
添加人工审核节点（Human-in-the-loop）
多语言版本（自动翻译英文发行文案）
技术栈
AI框架：Anthropic Claude API（claude-opus-4-5）
后端：Python 3.10+, Flask
游戏渲染：HTML5 Canvas API
海报：纯 CSS3 动画
