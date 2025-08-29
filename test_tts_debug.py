#!/usr/bin/env python3
"""
调试本地EdgeTTS音频输出问题
"""

import asyncio
import sys
import os
import time
import tempfile
import subprocess

def test_audio_playback(audio_file):
    """测试音频播放"""
    print(f"测试播放音频文件: {audio_file}")
    
    # 检查文件是否存在
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在: {audio_file}")
        return False
    
    # 获取文件大小
    file_size = os.path.getsize(audio_file)
    print(f"音频文件大小: {file_size} 字节")
    
    if file_size == 0:
        print("❌ 音频文件为空")
        return False
    
    # 尝试播放音频
    try:
        # 使用系统默认播放器播放
        if sys.platform == "win32":
            os.startfile(audio_file)
        else:
            subprocess.run(["xdg-open", audio_file])
        print("✅ 已尝试播放音频文件")
        return True
    except Exception as e:
        print(f"❌ 播放失败: {e}")
        return False

async def test_tts_with_audio():
    """测试TTS并播放音频"""
    print("=" * 50)
    print("本地EdgeTTS音频输出测试")
    print("=" * 50)
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 测试文本
        test_text = "你好，我是春儿，这是本地语音测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 生成音频
        print("🔄 正在生成音频...")
        start_time = time.time()
        audio_data = await tts.text_to_speech(test_text)
        elapsed_time = time.time() - start_time
        
        if not audio_data:
            print("❌ 音频生成失败")
            return False
        
        print(f"✅ 音频生成成功，耗时: {elapsed_time:.2f}秒")
        print(f"📊 音频数据大小: {len(audio_data)} 字节")
        
        # 保存音频文件
        audio_file = "debug_test_audio.wav"
        with open(audio_file, "wb") as f:
            f.write(audio_data)
        print(f"💾 音频已保存为: {audio_file}")
        
        # 测试播放
        success = test_audio_playback(audio_file)
        
        if success:
            print("\n🎉 测试完成！请检查是否有声音输出")
            print("💡 如果没有声音，请检查：")
            print("   1. 系统音量设置")
            print("   2. 音频设备连接")
            print("   3. 浏览器音频权限")
        else:
            print("\n❌ 音频播放测试失败")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_system_audio():
    """测试系统音频"""
    print("\n" + "=" * 50)
    print("系统音频测试")
    print("=" * 50)
    
    # 检查音频设备
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print(f"✅ 发现 {len(devices)} 个音频设备")
        
        # 显示默认输出设备
        default_output = sd.query_devices(kind='output')
        print(f"📢 默认输出设备: {default_output['name']}")
        
        # 测试音频输出
        print("🔊 正在测试音频输出...")
        duration = 1.0  # 1秒
        sample_rate = 44100
        frequency = 440.0  # A4音符
        
        # 生成测试音频
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # 播放音频
        sd.play(audio, sample_rate)
        sd.wait()
        print("✅ 系统音频测试完成")
        return True
        
    except ImportError:
        print("⚠️  sounddevice 未安装，跳过系统音频测试")
        return True
    except Exception as e:
        print(f"❌ 系统音频测试失败: {e}")
        return False

if __name__ == "__main__":
    # 导入numpy用于音频生成
    try:
        import numpy as np
    except ImportError:
        print("❌ 需要安装 numpy: pip install numpy")
        sys.exit(1)
    
    # 运行测试
    success = asyncio.run(test_tts_with_audio())
    
    if success:
        print("\n🎯 建议：")
        print("1. 如果TTS测试成功但网页没有声音，检查浏览器设置")
        print("2. 确保浏览器允许音频播放")
        print("3. 检查WebRTC音频流设置")
    else:
        print("\n🔧 需要进一步调试TTS功能")
    
    sys.exit(0 if success else 1)

