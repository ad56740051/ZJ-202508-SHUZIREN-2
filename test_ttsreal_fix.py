#!/usr/bin/env python3
"""
测试ttsreal.py修复
"""

import time

def test_ttsreal_fix():
    """测试ttsreal.py修复"""
    print("测试ttsreal.py修复...")
    
    try:
        from ttsreal import LocalEdgeTTS
        
        # 创建一个模拟的opt对象
        class MockOpt:
            def __init__(self):
                self.fps = 50
                self.tts = "local_edgetts"
        
        opt = MockOpt()
        
        # 创建一个模拟的parent对象
        class MockParent:
            def __init__(self):
                self.audio_frames = []
            
            def put_audio_frame(self, audio_chunk, eventpoint=None):
                self.audio_frames.append((len(audio_chunk), eventpoint))
                print(f"📊 接收到音频帧: {len(audio_chunk)} 样本")
        
        parent = MockParent()
        
        # 创建LocalEdgeTTS实例
        print("🔧 创建LocalEdgeTTS实例...")
        tts = LocalEdgeTTS(opt, parent)
        print("✅ LocalEdgeTTS实例创建成功")
        
        # 检查备选TTS
        if hasattr(tts.local_tts, 'fallback_tts') and tts.local_tts.fallback_tts:
            print("✅ 备选TTS引擎可用")
        else:
            print("❌ 备选TTS引擎不可用")
            return False
        
        # 测试文本转语音
        test_text = "测试ttsreal修复。"
        print(f"📝 测试文本: {test_text}")
        
        # 模拟数字人的消息处理
        msg = (test_text, None)
        
        print("🎵 开始TTS转换...")
        start_time = time.time()
        
        # 调用txt_to_audio方法
        tts.txt_to_audio(msg)
        
        end_time = time.time()
        print(f"⏱️ TTS转换耗时: {end_time - start_time:.2f}秒")
        
        # 检查结果
        if parent.audio_frames:
            total_samples = sum(frame[0] for frame in parent.audio_frames)
            print(f"✅ TTS转换成功！")
            print(f"   音频帧数量: {len(parent.audio_frames)}")
            print(f"   总样本数: {total_samples}")
            print(f"   音频时长: {total_samples / 16000:.2f}秒")
            return True
        else:
            print("❌ TTS转换失败，未接收到音频帧")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_ttsreal_fix()
    if result:
        print("\n🎉 ttsreal.py修复成功！")
    else:
        print("\n❌ ttsreal.py修复失败！")

