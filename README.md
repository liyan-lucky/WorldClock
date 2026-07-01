# WorldClock

一个本地桌面世界时钟应用仓库，当前包含两套实现：

- `world_clock.py`
  Python / PyQt5 版本
- `WorldClockWpf/`
  C# / WPF 版本

## 当前状态

当前事实以 [CURRENT_STATUS.md](docs/CURRENT_STATUS.md) 为准。

## 当前推荐

如果你更在意分发体积和 Windows 桌面体验，推荐使用 `WorldClockWpf`。Python 版本保留在仓库中，方便继续参考和迁移已有交互细节。

## 功能

- 多地点时间显示
- 秒数开关
- 置顶
- 主题切换
- 透明度调整
- 配置保存
- 右键删除地点

## WPF 版本

工程文件：

```text
WorldClockWpf/WorldClockWpf.csproj
```

当前目标框架：

```text
net8.0-windows
```

运行或构建前需要安装 .NET SDK 8。框架依赖发布的目标机器需要安装 `.NET Desktop Runtime 8`。

常用命令：

```bash
dotnet build WorldClockWpf/WorldClockWpf.csproj
```

发布目录说明：

```text
WorldClockWpf/publish-fdd/
```

该目录用于框架依赖发布产物，不建议提交到仓库。

## Python 版本

Python 版本保留在仓库中，方便继续参考和迁移已有交互细节。

依赖文件：

```text
requirements.txt
```

当前依赖：

```text
PyQt5>=5.15.11
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

运行：

```bash
python world_clock.py
```

## 分支和备份

- `main`：当前主工作分支。
- `backup`：`main` 的快照备份分支。
- `.github/workflows/force-backup-main.yml`：手动输入 `YES` 后，把 `main` 当前提交强制覆盖到 `backup`。

## 配置文件

应用会在本地保存配置文件：

```text
world_clock_config.json
```

该文件用于保存城市、主题、窗口大小、窗口位置、透明度、是否显示秒数、是否置顶等本地设置。该文件属于本地用户配置，不应提交到仓库。

## 隐私说明

本项目当前设计为本地桌面应用，正常时钟显示不需要网络访问，不包含账号登录、广告 SDK、遥测、分析统计或云同步逻辑。

如第三方分发版添加网络、自动更新、崩溃上报或云同步功能，应提供单独的隐私说明。

## 合规与许可证

本仓库采用 MIT License。

相关文件：

- `LICENSE`
- `NOTICE.md`
- `THIRD_PARTY_NOTICES.md`
- `DISCLAIMER.md`
- `PRIVACY.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `COMPLIANCE.md`
- `docs/CURRENT_STATUS.md`

## 重要免责声明

WorldClock 是通用桌面世界时钟工具。时区数据、夏令时规则、操作系统 API、运行时库和本地系统时间设置都可能变化或异常。

请不要把本应用作为法律、医疗、航空、交通、金融交易、应急、安全关键或最后期限关键场景的唯一时间依据。关键用途请同时核对权威来源。

## 第三方依赖提示

WPF 版本当前未声明第三方 NuGet 包。

Python 版本使用 PyQt5 / Qt。若要分发 Python 打包版本，请先确认 PyQt5 / Qt 的许可证和再分发要求。
