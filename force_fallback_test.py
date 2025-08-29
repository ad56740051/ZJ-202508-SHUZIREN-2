#!/usr/bin/env python3
"""
强制使用备选TTS测试
"""

import time

def force_fallback_test():
    print("强制使用备选TTS测试...")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 检查备选TTS是否可用
        if not tts.fallback_tts:
            print("❌ 备选TTS不可用")
            return False
        
        print("✅ 备选TTS可用")
        
        # 测试文本
        test_text = "强制使用备选TTS测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 直接使用备选TTS
        start_time = time.time()
        audio_data = tts._fallback_text_to_speech_sync(test_text)
        end_time = time.time()
        
        if audio_data:
            print(f"✅ 备选TTS转换成功，耗时: {end_time - start_time:.2f}秒")
            print(f"   音频大小: {len(audio_data)} 字节")
            
            # 保存音频
            with open("force_fallback_test.wav", "wb") as f:
                f.write(audio_data)
            print("💾 音频已保存为 force_fallback_test.wav")
            
            return True
        else:
            print("❌ 备选TTS转换失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    force_fallback_test()


