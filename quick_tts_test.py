#!/usr/bin/env python3
"""
快速TTS测试
"""

import time

def quick_test():
    print("快速TTS测试...")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 测试文本
        test_text = "快速测试。"
        print(f"📝 测试文本: {test_text}")
        
        # 测试转换
        start_time = time.time()
        audio_data = tts.text_to_speech_sync(test_text)
        end_time = time.time()
        
        if audio_data:
            print(f"✅ TTS转换成功，耗时: {end_time - start_time:.2f}秒")
            print(f"   音频大小: {len(audio_data)} 字节")
            
            # 保存音频
            with open("quick_test.wav", "wb") as f:
                f.write(audio_data)
            print("💾 音频已保存为 quick_test.wav")
            
            return True
        else:
            print("❌ TTS转换失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    quick_test()


