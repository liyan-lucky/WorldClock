# 当前仓库状态

更新时间：2026-07-01

## 定位

`WorldClock` 是本地桌面世界时钟应用仓库，当前包含两套实现：Python / PyQt5 版本和 C# / WPF 版本。

## 当前实现

- `world_clock.py`：Python / PyQt5 实现。
- `requirements.txt`：Python 依赖，当前为 `PyQt5>=5.15.11`。
- `WorldClockWpf/`：C# / WPF 实现。
- `WorldClockWpf/WorldClockWpf.csproj`：目标框架为 `net8.0-windows`，启用 WPF。

## 当前推荐

如果更在意分发体积和 Windows 桌面体验，优先使用 `WorldClockWpf`。Python 版本保留在仓库中，用于继续参考和迁移已有交互细节。

## 当前功能

- 多地点时间显示。
- 秒数开关。
- 置顶。
- 主题切换。
- 透明度调整。
- 配置保存。
- 右键删除地点。

## 当前分支和备份

- `main`：当前主工作分支。
- `backup`：`main` 的快照备份分支。
- `.github/workflows/force-backup-main.yml`：手动输入 `YES` 后，把 `main` 当前提交强制覆盖到 `backup`。

## 本地数据和隐私

- 本项目当前设计为本地桌面应用，正常时钟显示不需要网络访问。
- 当前不包含账号登录、广告 SDK、遥测、分析统计或云同步逻辑。
- 本地配置文件为 `world_clock_config.json`，不应提交到仓库。

## 合规边界

- 仓库采用 MIT License。
- WPF 版本当前未声明第三方 NuGet 包。
- Python 版本使用 PyQt5 / Qt，分发 Python 打包版本前应确认 PyQt5 / Qt 的许可证和再分发要求。
- 不要把本应用作为法律、医疗、航空、交通、金融交易、应急、安全关键或最后期限关键场景的唯一时间依据。

功能、依赖、发布方式或本地配置规则变化时，应同步更新本文件、根 README 和相关合规文档。
