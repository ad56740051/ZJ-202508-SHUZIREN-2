#!/usr/bin/env python3
"""
真正的离线TTS测试
通过修改网络请求来模拟网络断开，测试备选TTS是否正常工作
"""

import asyncio
import sys
import os
import time
import tempfile

def test_offline_tts():
    """测试真正的离线TTS功能"""
    print("==================================================")
    print("真正的离线TTS测试")
    print("==================================================")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 测试文本
        test_text = "你好，我是春儿，这是真正的离线TTS测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 模拟网络断开 - 通过修改edge_tts的Communicate类
        print("🌐 模拟网络断开情况...")
        
        # 保存原始的edge_tts.Communicate
        import edge_tts
        original_communicate = edge_tts.Communicate
        
        # 创建一个会抛出网络错误的Communicate类
        class MockCommunicate:
            def __init__(self, text, voice):
                self.text = text
                self.voice = voice
                raise Exception("模拟网络连接失败")
            
            async def stream(self):
                raise Exception("模拟网络连接失败")
        
        # 替换edge_tts.Communicate
        edge_tts.Communicate = MockCommunicate
        
        try:
            # 现在尝试转换，应该会使用备选TTS
            audio_data = tts.text_to_speech_sync(test_text)
            if audio_data:
                print(f"✅ 离线TTS转换成功，音频大小: {len(audio_data)} 字节")
                
                # 保存测试音频
                with open("test_offline_tts.wav", "wb") as f:
                    f.write(audio_data)
                print("💾 离线TTS测试音频已保存为 test_offline_tts.wav")
                
                # 获取音频信息
                audio_info = tts.get_audio_info(audio_data)
                if audio_info:
                    print(f"📊 音频信息: {audio_info}")
                
                return True
            else:
                print("❌ 离线TTS转换失败，无音频数据")
                return False
                
        except Exception as e:
            print(f"❌ 离线TTS转换失败: {e}")
            return False
        finally:
            # 恢复原始的edge_tts.Communicate
            edge_tts.Communicate = original_communicate
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_fallback_tts():
    """直接测试备选TTS功能"""
    print("\n==================================================")
    print("直接备选TTS测试")
    print("==================================================")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 测试文本
        test_text = "直接使用备选TTS引擎进行测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 直接调用备选TTS
        if tts.fallback_tts:
            print("✅ 备选TTS引擎可用")
            
            try:
                # 直接使用备选TTS
                audio_data = tts._fallback_text_to_speech_sync(test_text)
                if audio_data:
                    print(f"✅ 直接备选TTS转换成功，音频大小: {len(audio_data)} 字节")
                    
                    # 保存测试音频
                    with open("test_direct_fallback.wav", "wb") as f:
                        f.write(audio_data)
                    print("💾 直接备选TTS测试音频已保存为 test_direct_fallback.wav")
                    
                    return True
                else:
                    print("❌ 直接备选TTS转换失败，无音频数据")
                    return False
                    
            except Exception as e:
                print(f"❌ 直接备选TTS转换失败: {e}")
                return False
        else:
            print("❌ 备选TTS引擎不可用")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始真正的离线TTS功能测试...")
    
    # 测试真正的离线TTS
    result1 = test_offline_tts()
    
    # 测试直接备选TTS
    result2 = test_direct_fallback_tts()
    
    print("\n==================================================")
    print("测试结果汇总")
    print("==================================================")
    print(f"1. 真正的离线TTS测试: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"2. 直接备选TTS测试: {'✅ 通过' if result2 else '❌ 失败'}")
    
    if result1 and result2:
        print("\n🎉 所有测试通过！离线TTS功能正常")
        print("💡 现在即使在网络断开的情况下，数字人也能正常播放语音")
    else:
        print("\n⚠️ 部分测试失败，请检查配置")
    
    print("==================================================")


