#!/usr/bin/env python3
"""
数字人TTS功能测试
模拟数字人实际使用TTS的过程
"""

import sys
import os
import time

def test_digital_human_tts():
    """测试数字人TTS功能"""
    print("==================================================")
    print("数字人TTS功能测试")
    print("==================================================")
    
    try:
        # 模拟数字人的TTS调用过程
        from ttsreal import LocalEdgeTTS
        from basereal import BaseReal
        
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
                print(f"📊 接收到音频帧: {len(audio_chunk)} 样本, 事件: {eventpoint}")
        
        parent = MockParent()
        
        # 创建LocalEdgeTTS实例
        print("🔧 创建LocalEdgeTTS实例...")
        tts = LocalEdgeTTS(opt, parent)
        print("✅ LocalEdgeTTS实例创建成功")
        
        # 测试文本转语音
        test_text = "你好，我是春儿，这是数字人TTS测试。"
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
            
            # 检查事件点
            start_events = [frame[1] for frame in parent.audio_frames if frame[1] and frame[1].get('status') == 'start']
            end_events = [frame[1] for frame in parent.audio_frames if frame[1] and frame[1].get('status') == 'end']
            
            if start_events:
                print(f"   开始事件: {start_events[0]}")
            if end_events:
                print(f"   结束事件: {end_events[0]}")
            
            return True
        else:
            print("❌ TTS转换失败，未接收到音频帧")
            return False
            
    except Exception as e:
        print(f"❌ 数字人TTS测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_network_failure_scenario():
    """测试网络失败场景"""
    print("\n==================================================")
    print("网络失败场景测试")
    print("==================================================")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 模拟网络断开的情况
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
            # 测试文本
            test_text = "网络断开时的TTS测试。"
            print(f"📝 测试文本: {test_text}")
            
            # 尝试转换，应该会使用备选TTS
            audio_data = tts.text_to_speech_sync(test_text)
            
            if audio_data:
                print(f"✅ 备选TTS转换成功，音频大小: {len(audio_data)} 字节")
                
                # 保存测试音频
                with open("network_failure_test.wav", "wb") as f:
                    f.write(audio_data)
                print("💾 网络失败测试音频已保存为 network_failure_test.wav")
                
                return True
            else:
                print("❌ 备选TTS转换失败，无音频数据")
                return False
                
        finally:
            # 恢复原始的edge_tts.Communicate
            edge_tts.Communicate = original_communicate
            
    except Exception as e:
        print(f"❌ 网络失败场景测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始数字人TTS功能测试...")
    
    # 测试数字人TTS功能
    result1 = test_digital_human_tts()
    
    # 测试网络失败场景
    result2 = test_network_failure_scenario()
    
    print("\n==================================================")
    print("测试结果汇总")
    print("==================================================")
    print(f"1. 数字人TTS功能测试: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"2. 网络失败场景测试: {'✅ 通过' if result2 else '❌ 失败'}")
    
    if result1 and result2:
        print("\n🎉 所有测试通过！数字人TTS功能正常")
        print("💡 如果数字人仍然无法播放语音，问题可能在于:")
        print("   1. 音频播放管道配置")
        print("   2. WebRTC音频传输")
        print("   3. 浏览器音频播放")
    else:
        print("\n⚠️ 部分测试失败，需要进一步排查")
    
    print("==================================================")

if __name__ == "__main__":
    main()


