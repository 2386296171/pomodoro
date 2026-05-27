# 🍅 番茄钟

苹果风格桌面番茄钟，毛玻璃质感，支持任务清单、历史统计、自定义时长。

![screenshot](screenshot.png)

## 功能

- **番茄计时** — 25 分钟专注 + 5 分钟短休息，每 4 轮一次 15 分钟长休息
- **任务清单** — 给每个番茄关联待办任务，完成打勾
- **历史统计** — 今日/本周/总计番茄数，7 天柱状图
- **自定义时长** — 专注、短休息、长休息时长均可调节
- **窗口置顶** — 始终在最前，不被打断
- **数据持久化** — 关闭重开自动恢复任务和统计

## 快速开始

### 直接运行（无需安装）

下载 `dist/番茄钟.exe`，双击运行。

### 开发模式

```bash
pip install pywebview pillow
python pomodoro.py
```

## 项目结构

```
├── pomodoro.py      # Python 入口，webview 窗口
├── app.html         # 前端 UI（HTML + CSS + JS）
├── icon.png         # 托盘图标
├── dist/            # 打包产物
│   └── 番茄钟.exe
└── README.md
```

## 技术栈

- **桌面容器**：pywebview（调用系统 Edge WebView2）
- **前端**：原生 HTML/CSS/JS，毛玻璃 `backdrop-filter: blur()`
- **持久化**：localStorage
- **打包**：PyInstaller

## 许可证

MIT
