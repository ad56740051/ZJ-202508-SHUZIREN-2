@echo off
chcp 65001
set PYTHONUSERBASE=.\python\Lib\site-packages
set PYTHONPATH=.\python\Lib\site-packages
set PATH=%PATH%;.\python\Scripts
echo 启动离线TTS数字人系统...
echo 正在使用本地语音合成，无需联网...
echo 强制使用备选TTS引擎...
.\python\python.exe app.py --avatar_id avatar11 --customvideo_config custom_video.json --tts local_edgetts
pause
