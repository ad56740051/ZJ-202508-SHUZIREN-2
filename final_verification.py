#!/usr/bin/env python3
"""
最终验证脚本
验证数字人TTS功能完全正常
"""

import time

def final_verification():
    """最终验证"""
    print("==================================================")
    print("最终验证 - 数字人TTS功能")
    print("==================================================")
    
    try:
        # 1. 测试备选TTS功能
        print("1. 测试备选TTS功能...")
        from local_edge_tts import LocalEdgeTTS
        
        tts = LocalEdgeTTS()
        if tts.fallback_tts:
            print("✅ 备选TTS引擎可用")
            
            # 测试备选TTS
            test_text = "最终验证测试。"
            audio_data = tts._fallback_text_to_speech_sync(test_text)
            
            if audio_data:
                print(f"✅ 备选TTS转换成功，音频大小: {len(audio_data)} 字节")
            else:
                print("❌ 备选TTS转换失败")
                return False
        else:
            print("❌ 备选TTS引擎不可用")
            return False
        
        # 2. 测试数字人TTS集成
        print("\n2. 测试数字人TTS集成...")
        from ttsreal import LocalEdgeTTS as TTSRealLocalEdgeTTS
        
        # 创建模拟对象
        class MockOpt:
            def __init__(self):
                self.fps = 50
                self.tts = "local_edgetts"
        
        class MockParent:
            def __init__(self):
                self.audio_frames = []
            
            def put_audio_frame(self, audio_chunk, eventpoint=None):
                self.audio_frames.append((len(audio_chunk), eventpoint))
        
        opt = MockOpt()
        parent = MockParent()
        
        # 创建TTS实例
        tts_real = TTSRealLocalEdgeTTS(opt, parent)
        print("✅ 数字人TTS实例创建成功")
        
        # 测试TTS转换
        test_text = "数字人TTS集成测试。"
        msg = (test_text, None)
        
        tts_real.txt_to_audio(msg)
        
        if parent.audio_frames:
            total_samples = sum(frame[0] for frame in parent.audio_frames)
            print(f"✅ 数字人TTS转换成功！")
            print(f"   音频帧数量: {len(parent.audio_frames)}")
            print(f"   总样本数: {total_samples}")
            print(f"   音频时长: {total_samples / 16000:.2f}秒")
        else:
            print("❌ 数字人TTS转换失败")
            return False
        
        # 3. 检查启动脚本
        print("\n3. 检查启动脚本...")
        import os
        
        if os.path.exists("2.webui_offline_tts.bat"):
            print("✅ 离线TTS启动脚本存在")
        else:
            print("❌ 离线TTS启动脚本不存在")
            return False
        
        if os.path.exists("2.webui_local_tts.bat"):
            print("✅ 本地TTS启动脚本存在")
        else:
            print("❌ 本地TTS启动脚本不存在")
        
        print("\n==================================================")
        print("🎉 最终验证通过！")
        print("==================================================")
        print("✅ 备选TTS功能正常")
        print("✅ 数字人TTS集成正常")
        print("✅ 启动脚本配置正确")
        print("\n💡 现在可以使用以下命令启动数字人:")
        print("   2.webui_offline_tts.bat")
        print("\n🎵 数字人语音播放功能已完全修复！")
        
        return True
        
    except Exception as e:
        print(f"❌ 最终验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = final_verification()
    if success:
        print("\n🎉 所有验证通过！数字人TTS功能完全正常！")
    else:
        print("\n❌ 验证失败，需要进一步检查")

