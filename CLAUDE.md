# 番茄钟 Pomodoro Timer

桌面番茄钟应用，Python + pywebview + HTML/CSS/JS。

## 运行

```bash
python pomodoro.py            # 开发模式
dist/番茄钟.exe               # 打包好的可执行文件
```

## 依赖

- `pywebview` — 系统 WebView 桌面容器
- `winsound` — 系统提示音（Windows 自带）
- `Pillow` — 托盘图标生成

## 结构

| 文件 | 作用 |
|------|------|
| `pomodoro.py` | Python 入口，webview 窗口 + JS 桥接 |
| `app.html` | 前端 UI（HTML + CSS + JS，单文件） |
| `icon.png` | 托盘图标（自动生成） |
| `dist/番茄钟.exe` | PyInstaller 打包产物 |

## 前端架构

HTML/CSS/JS 单文件，通过 `window.pywebview.api` 调用 Python：

- **毛玻璃效果** — `backdrop-filter: blur(40px) saturate(180%)` + 半透明白色面板
- **SVG 环形进度** — `stroke-dasharray` 动画驱动
- **计时逻辑** — `setInterval` 200ms 基于时间戳差值（比计次更准确）
- **数据持久化** — `localStorage` 存储任务、历史、设置
- **API 桥接** — `Api.notify()` 系统提示音，`Api.minimize_to_tray()` 最小化

## 配置

| 默认值 | 可调范围 |
|--------|----------|
| 专注 25 分钟 | 5-60 分钟 |
| 短休息 5 分钟 | 1-15 分钟 |
| 长休息 15 分钟 | 5-30 分钟 |
| 每 4 个番茄一次长休息 | |

## 设计决策

- webview 窗口 340×600，无滚动，所有内容固定布局
- 日期全部用 `localDate()` 本地时间（非 UTC），避免时区偏移
- 环形进度用 SVG `stroke-dashoffset`，比 Canvas 更平滑
- PyInstaller 打包时 `--add-data` 内嵌 `app.html` 和 `icon.png`
