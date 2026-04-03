# WorldClock

一个桌面世界时钟应用仓库，当前包含两套实现：

- `world_clock.py`
  Python / PyQt5 版本
- `WorldClockWpf/`
  C# / WPF 版本

## 当前推荐

如果你更在意分发体积，推荐使用 `WorldClockWpf`。

## WPF 版本

工程文件：

- `WorldClockWpf/WorldClockWpf.csproj`

已实现的核心功能：

- 多地点时间显示
- 秒数开关
- 置顶
- 主题切换
- 透明度调整
- 配置保存
- 右键删除地点

发布说明：

- 框架依赖发布目录：`WorldClockWpf/publish-fdd/`
- 目标机器需要安装 `.NET Desktop Runtime 8`

## Python 版本

Python 版本保留在仓库中，方便继续参考和迁移已有交互细节。
