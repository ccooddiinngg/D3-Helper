# Diablo III 自动启动器

一个用于自动启动和管理 Diablo III 游戏的 Windows 应用程序。

## 功能特性

- ✅ 自动监控 Diablo III 进程
- ✅ 自动启动 Battle.net 和游戏
- ✅ Windows 桌面管理窗口
- ✅ 完整的日志记录系统
- ✅ 后台运行支持
- ✅ 管理员权限自动请求

## 项目结构

```
.
├── main.py                 # 主程序入口
├── config.py              # 配置管理模块
├── utils.py               # 工具函数模块
├── logger_config.py       # 日志配置模块
├── process_manager.py     # 进程管理模块
├── image_finder.py        # 图片查找模块
├── game_launcher.py       # 游戏启动器模块
├── window_manager.py      # 窗口管理模块
├── stop_service.py        # 停止服务脚本
├── run_as_admin.bat       # 以管理员权限运行脚本
├── logs/                  # 日志文件目录
└── README.md             # 项目说明文档
```

## 模块说明

### 核心模块

- **main.py**: 主程序，负责初始化和协调各个模块
- **config.py**: 集中管理所有配置项，便于修改和维护
- **utils.py**: 提供通用的工具函数（权限检查、控制台操作等）

### 功能模块

- **process_manager.py**: 进程检测和窗口查找功能
- **image_finder.py**: 图片识别和点击功能
- **game_launcher.py**: 游戏启动逻辑
- **window_manager.py**: GUI 窗口管理
- **logger_config.py**: 日志系统配置

## 安装依赖

```bash
pip install psutil pyautogui pywin32
```

## 使用方法

### 方法一：直接运行

```bash
python main.py
```

### 方法二：以管理员权限运行

双击 `run_as_admin.bat` 文件，或在命令行中：

```bash
run_as_admin.bat
```

### 停止程序

1. 通过管理窗口点击"退出程序"按钮
2. 运行 `stop_service.py` 脚本
3. 在程序目录创建 `stop_service.txt` 文件

## 配置说明

所有配置项都在 `config.py` 文件中，可以根据需要修改：

- **进程名称**: 游戏和 Battle.net 的进程名称
- **图片文件**: 需要识别的按钮图片路径
- **监控间隔**: 检查游戏进程的时间间隔
- **日志配置**: 日志文件保存位置和格式

## 日志文件

程序只使用一个日志文件 `logs/diablo3_launcher.log`，每次启动都会清空旧内容，方便快速查看本次运行的完整记录。

## 注意事项

1. 程序需要管理员权限才能正常运行
2. 需要准备相应的按钮图片文件（play.png 等）
3. 确保 Battle.net 安装路径正确
4. 程序会在后台运行，可通过管理窗口进行控制

## 开发说明

### 代码结构优化

- ✅ 模块化设计，职责分离
- ✅ 配置集中管理
- ✅ 完善的错误处理
- ✅ 详细的日志记录
- ✅ 代码注释完善

### 性能优化

- ✅ 使用事件等待替代固定延迟
- ✅ 优化进程检查逻辑
- ✅ 减少不必要的文件操作

## 许可证

本项目仅供学习和个人使用。

