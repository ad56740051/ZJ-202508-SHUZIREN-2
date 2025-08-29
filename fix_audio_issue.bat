@echo off
chcp 65001
echo ==================================================
echo 数字人语音播放问题修复脚本
echo ==================================================
echo.

echo 1. 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)
echo ✅ Python环境正常
echo.

echo 2. 安装必要的依赖包...
echo 安装pyttsx3...
pip install pyttsx3
if %errorlevel% neq 0 (
    echo ❌ pyttsx3安装失败
    pause
    exit /b 1
)
echo ✅ pyttsx3安装成功
echo.

echo 3. 运行TTS功能测试...
python test_local_tts.py
if %errorlevel% neq 0 (
    echo ❌ TTS功能测试失败
    pause
    exit /b 1
)
echo ✅ TTS功能测试通过
echo.

echo 4. 运行离线TTS测试...
python test_offline_tts.py
if %errorlevel% neq 0 (
    echo ❌ 离线TTS测试失败
    pause
    exit /b 1
)
echo ✅ 离线TTS测试通过
echo.

echo 5. 运行音频播放测试...
python test_audio_playback.py
if %errorlevel% neq 0 (
    echo ❌ 音频播放测试失败
    pause
    exit /b 1
)
echo ✅ 音频播放测试通过
echo.

echo ==================================================
echo 🎉 所有测试通过！语音播放问题已修复
echo ==================================================
echo.
echo 💡 现在请使用以下命令启动数字人：
echo.
echo    2.webui_local_tts.bat
echo.
echo ⚠️  重要：请使用 2.webui_local_tts.bat 而不是 2.webui.bat
echo.
echo 📖 详细说明请查看：语音播放问题修复指南.md
echo.
pause


