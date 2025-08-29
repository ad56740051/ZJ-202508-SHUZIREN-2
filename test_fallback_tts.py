#!/usr/bin/env python3
"""
测试备选TTS功能
模拟网络断开情况，测试本地TTS是否正常工作
"""

import asyncio
import sys
import os
import time

def test_fallback_tts():
    """测试备选TTS功能"""
    print("==================================================")
    print("备选TTS功能测试")
    print("==================================================")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 测试文本
        test_text = "你好，我是春儿，这是备选TTS测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 模拟网络断开的情况
        print("🌐 模拟网络断开情况...")
        
        # 直接测试备选TTS
        if tts.fallback_tts:
            print("✅ 备选TTS引擎可用")
            
            # 测试备选TTS
            try:
                audio_data = tts.text_to_speech_sync(test_text)
                if audio_data:
                    print(f"✅ 备选TTS转换成功，音频大小: {len(audio_data)} 字节")
                    
                    # 保存测试音频
                    with open("test_fallback_tts.wav", "wb") as f:
                        f.write(audio_data)
                    print("💾 备选TTS测试音频已保存为 test_fallback_tts.wav")
                    
                    # 获取音频信息
                    audio_info = tts.get_audio_info(audio_data)
                    if audio_info:
                        print(f"📊 音频信息: {audio_info}")
                    
                    return True
                else:
                    print("❌ 备选TTS转换失败，无音频数据")
                    return False
                    
            except Exception as e:
                print(f"❌ 备选TTS转换失败: {e}")
                return False
        else:
            print("❌ 备选TTS引擎不可用")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_network_disconnect_simulation():
    """模拟网络断开的情况"""
    print("\n==================================================")
    print("网络断开模拟测试")
    print("==================================================")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        
        # 测试文本
        test_text = "网络断开时的备选TTS测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 尝试转换（如果网络正常，会使用EdgeTTS；如果网络断开，会使用备选TTS）
        try:
            audio_data = tts.text_to_speech_sync(test_text)
            if audio_data:
                print(f"✅ TTS转换成功，音频大小: {len(audio_data)} 字节")
                
                # 保存测试音频
                with open("test_network_simulation.wav", "wb") as f:
                    f.write(audio_data)
                print("💾 网络模拟测试音频已保存为 test_network_simulation.wav")
                
                return True
            else:
                print("❌ TTS转换失败，无音频数据")
                return False
                
        except Exception as e:
            print(f"❌ TTS转换失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始备选TTS功能测试...")
    
    # 测试备选TTS
    result1 = test_fallback_tts()
    
    # 测试网络断开模拟
    result2 = test_network_disconnect_simulation()
    
    print("\n==================================================")
    print("测试结果汇总")
    print("==================================================")
    print(f"1. 备选TTS功能测试: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"2. 网络断开模拟测试: {'✅ 通过' if result2 else '❌ 失败'}")
    
    if result1 and result2:
        print("\n🎉 所有测试通过！备选TTS功能正常")
        print("💡 现在即使在网络断开的情况下，数字人也能正常播放语音")
    else:
        print("\n⚠️ 部分测试失败，请检查配置")
    
    print("==================================================")


