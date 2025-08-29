# 本地EdgeTTS使用说明

## 概述

本项目已集成本地EdgeTTS功能，无需联网即可进行语音合成。本地EdgeTTS基于Microsoft Edge浏览器的TTS引擎，提供高质量的中文语音合成服务。

## 功能特点

- ✅ **完全离线**：无需联网，保护隐私
- ✅ **高质量语音**：支持多种中文语音
- ✅ **低延迟**：本地处理，响应速度快
- ✅ **易于配置**：支持配置文件自定义设置
- ✅ **兼容性好**：与现有数字人系统完美集成

## 支持的语音

| 语音ID | 语音名称 | 性别 | 特点 |
|--------|----------|------|------|
| zh-CN-XiaoxiaoNeural | 中文女声-晓晓 | 女 | 默认语音，清晰自然 |
| zh-CN-YunxiNeural | 中文男声-云希 | 男 | 年轻男声 |
| zh-CN-YunyangNeural | 中文男声-云扬 | 男 | 成熟男声 |
| zh-CN-XiaoyiNeural | 中文女声-晓伊 | 女 | 温柔女声 |
| zh-CN-YunjianNeural | 中文男声-云健 | 男 | 稳重男声 |
| zh-CN-XiaohanNeural | 中文女声-晓涵 | 女 | 活泼女声 |
| zh-CN-YunxiaNeural | 中文女声-云夏 | 女 | 甜美女声 |
| zh-CN-XiaomoNeural | 中文女声-晓墨 | 女 | 知性女声 |
| zh-CN-YunfengNeural | 中文男声-云枫 | 男 | 磁性男声 |
| zh-CN-XiaoxuanNeural | 中文女声-晓萱 | 女 | 优雅女声 |
| zh-CN-YunzeNeural | 中文男声-云泽 | 男 | 深沉男声 |

## 安装步骤

### 1. 安装依赖

运行安装脚本：
```bash
install_local_tts.bat
```

或者手动安装：
```bash
pip install edge-tts soundfile resampy numpy
```

### 2. 测试安装

运行测试脚本：
```bash
python local_edge_tts.py
```

如果看到"测试音频已保存为 test_output.wav"，说明安装成功。

## 使用方法

### 1. 启动本地TTS数字人系统

运行启动脚本：
```bash
2.webui_local_tts.bat
```

### 2. 通过命令行启动

```bash
python app.py --tts local_edgetts --avatar_id avatar11 --customvideo_config custom_video.json
```

### 3. 配置语音

编辑 `local_tts_config.json` 文件来配置语音设置：

```json
{
    "tts_settings": {
        "default_voice": "zh-CN-XiaoxiaoNeural",
        "available_voices": {
            "zh-CN-XiaoxiaoNeural": "中文女声-晓晓",
            "zh-CN-YunxiNeural": "中文男声-云希"
        }
    },
    "character_settings": {
        "chuner_voice": "zh-CN-XiaoxiaoNeural"
    }
}
```

## 配置文件说明

### tts_settings
- `default_voice`: 默认语音ID
- `available_voices`: 可用语音列表
- `audio_settings`: 音频设置
- `performance_settings`: 性能设置

### character_settings
- `chuner_voice`: 春儿角色的语音ID
- `chuner_personality`: 角色性格描述

## 技术实现

### 核心文件
- `local_edge_tts.py`: 本地EdgeTTS核心实现
- `ttsreal.py`: TTS接口集成
- `basereal.py`: 基础功能支持
- `app.py`: 主程序入口

### 工作流程
1. 文本输入 → 本地EdgeTTS处理
2. 音频生成 → 音频流处理
3. 唇同步 → Wav2Lip模型
4. 视频合成 → 实时输出

## 性能优化

### 1. 缓存机制
启用音频缓存可以减少重复文本的处理时间：
```json
{
    "performance_settings": {
        "enable_cache": true,
        "cache_size": 100
    }
}
```

### 2. 流式处理
支持流式音频处理，提高响应速度：
```json
{
    "performance_settings": {
        "enable_streaming": true
    }
}
```

## 故障排除

### 1. 安装失败
- 确保Python版本 >= 3.7
- 检查网络连接（首次安装需要下载模型）
- 尝试使用国内镜像源：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple edge-tts`

### 2. 语音合成失败
- 检查edge-tts是否正确安装
- 确认语音ID是否正确
- 查看日志文件获取详细错误信息

### 3. 音频质量问题
- 调整音频采样率设置
- 检查音频格式配置
- 确保音频设备正常工作

## 与在线版本的区别

| 特性 | 本地EdgeTTS | 在线EdgeTTS |
|------|-------------|-------------|
| 网络依赖 | ❌ 无需联网 | ✅ 需要联网 |
| 隐私保护 | ✅ 完全本地 | ❌ 数据上传 |
| 响应速度 | ✅ 更快 | ❌ 受网络影响 |
| 语音质量 | ✅ 相同 | ✅ 相同 |
| 稳定性 | ✅ 更稳定 | ❌ 受网络影响 |

## 更新日志

### v1.0.0 (2024-01-XX)
- ✅ 实现本地EdgeTTS功能
- ✅ 支持多种中文语音
- ✅ 集成配置文件系统
- ✅ 添加性能优化选项
- ✅ 完善错误处理机制

## 技术支持

如果遇到问题，请：
1. 查看日志文件
2. 检查配置文件
3. 运行测试脚本
4. 提交Issue到项目仓库

## 许可证

本项目基于Apache License 2.0开源协议。

