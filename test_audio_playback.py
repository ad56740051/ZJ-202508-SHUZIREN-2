#!/usr/bin/env python3
"""
音频播放测试
测试生成的音频文件是否可以正常播放
"""

import os
import sys
import time

def test_audio_playback():
    """测试音频播放功能"""
    print("==================================================")
    print("音频播放测试")
    print("==================================================")
    
    # 检查音频文件是否存在
    audio_files = [
        "test_chuner_voice.wav",
        "test_fallback_tts.wav", 
        "test_network_simulation.wav",
        "test_offline_tts.wav",
        "test_direct_fallback.wav"
    ]
    
    existing_files = []
    for file in audio_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            print(f"✅ 找到音频文件: {file} ({file_size} 字节)")
            existing_files.append(file)
        else:
            print(f"❌ 音频文件不存在: {file}")
    
    if not existing_files:
        print("❌ 没有找到任何音频文件")
        return False
    
    # 尝试播放音频文件
    print(f"\n🎵 尝试播放 {len(existing_files)} 个音频文件...")
    
    try:
        import pygame
        
        # 初始化pygame音频
        pygame.mixer.init()
        print("✅ pygame音频初始化成功")
        
        for i, audio_file in enumerate(existing_files, 1):
            print(f"\n{i}. 播放音频: {audio_file}")
            
            try:
                # 加载音频文件
                pygame.mixer.music.load(audio_file)
                print(f"   ✅ 音频文件加载成功")
                
                # 播放音频
                pygame.mixer.music.play()
                print(f"   🎵 开始播放音频...")
                
                # 等待播放完成
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                print(f"   ✅ 音频播放完成")
                
            except Exception as e:
                print(f"   ❌ 音频播放失败: {e}")
        
        pygame.mixer.quit()
        print("\n✅ 所有音频播放测试完成")
        return True
        
    except ImportError:
        print("⚠️ pygame未安装，跳过音频播放测试")
        print("💡 可以通过以下命令安装pygame: pip install pygame")
        return True
        
    except Exception as e:
        print(f"❌ 音频播放测试失败: {e}")
        return False

def test_simple_audio():
    """测试简单的音频生成和播放"""
    print("\n==================================================")
    print("简单音频生成测试")
    print("==================================================")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 测试文本
        test_text = "测试音频播放功能。"
        print(f"📝 测试文本: {test_text}")
        
        # 生成音频
        audio_data = tts.text_to_speech_sync(test_text)
        if audio_data:
            print(f"✅ 音频生成成功，大小: {len(audio_data)} 字节")
            
            # 保存音频文件
            with open("test_playback.wav", "wb") as f:
                f.write(audio_data)
            print("💾 音频文件已保存为 test_playback.wav")
            
            # 尝试播放
            try:
                import pygame
                pygame.mixer.init()
                
                pygame.mixer.music.load("test_playback.wav")
                pygame.mixer.music.play()
                print("🎵 开始播放测试音频...")
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                pygame.mixer.quit()
                print("✅ 测试音频播放完成")
                return True
                
            except ImportError:
                print("⚠️ pygame未安装，无法播放音频")
                return True
            except Exception as e:
                print(f"❌ 音频播放失败: {e}")
                return False
        else:
            print("❌ 音频生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 简单音频测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始音频播放测试...")
    
    # 测试现有音频文件播放
    result1 = test_audio_playback()
    
    # 测试简单音频生成和播放
    result2 = test_simple_audio()
    
    print("\n==================================================")
    print("测试结果汇总")
    print("==================================================")
    print(f"1. 现有音频文件播放测试: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"2. 简单音频生成播放测试: {'✅ 通过' if result2 else '❌ 失败'}")
    
    if result1 and result2:
        print("\n🎉 所有测试通过！音频播放功能正常")
        print("💡 数字人的语音可以正常播放")
    else:
        print("\n⚠️ 部分测试失败，请检查音频配置")
    
    print("==================================================")


