@echo off
chcp 65001
set PYTHONUSERBASE=.\python\Lib\site-packages
set PYTHONPATH=.\python\Lib\site-packages
set PATH=%PATH%;.\python\Scripts
cd wav2lip
..\python\python.exe genavatar.py --video_path ../video/pipa-speak-2.mp4 --img_size 256 --avatar_id avatar13
pause