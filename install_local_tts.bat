@echo off
chcp 65001
echo 正在安装本地EdgeTTS依赖...
echo.

set PYTHONUSERBASE=.\python\Lib\site-packages
set PYTHONPATH=.\python\Lib\site-packages
set PATH=%PATH%;.\python\Scripts

echo 安装edge-tts库...
.\python\python.exe -m pip install edge-tts

echo.
echo 安装其他必要依赖...
.\python\python.exe -m pip install soundfile resampy numpy

echo.
echo 测试本地EdgeTTS...
.\python\python.exe test_local_tts.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ 安装和测试完成！本地EdgeTTS功能正常
    echo 💡 现在可以运行 2.webui_local_tts.bat 启动本地语音数字人系统
) else (
    echo ❌ 测试失败，请检查错误信息
    echo 💡 可以手动运行 python test_local_tts.py 查看详细错误
)
pause
