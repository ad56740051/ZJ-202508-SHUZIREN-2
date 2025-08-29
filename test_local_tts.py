#!/usr/bin/env python3
"""
本地EdgeTTS功能测试脚本
"""

import asyncio
import sys
import os

def test_import():
    """测试模块导入"""
    print("1. 测试模块导入...")
    try:
        import edge_tts
        print("   ✅ edge-tts 导入成功")
    except ImportError as e:
        print(f"   ❌ edge-tts 导入失败: {e}")
        return False
    
    try:
        import soundfile as sf
        print("   ✅ soundfile 导入成功")
    except ImportError as e:
        print(f"   ❌ soundfile 导入失败: {e}")
        return False
    
    try:
        import resampy
        print("   ✅ resampy 导入成功")
    except ImportError as e:
        print(f"   ❌ resampy 导入失败: {e}")
        return False
    
    try:
        from local_edge_tts import LocalEdgeTTS
        print("   ✅ LocalEdgeTTS 导入成功")
    except ImportError as e:
        print(f"   ❌ LocalEdgeTTS 导入失败: {e}")
        return False
    
    return True

async def test_basic_functionality():
    """测试基本功能"""
    print("\n2. 测试基本功能...")
    try:
        from local_edge_tts import LocalEdgeTTS
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("   ✅ TTS实例创建成功")
        
        # 测试语音列表
        voices = tts.get_available_voices()
        print(f"   ✅ 获取到 {len(voices)} 个可用语音")
        
        # 测试文本转语音
        test_text = "你好，我是春儿，很高兴见到你！"
        print(f"   📝 测试文本: {test_text}")
        
        audio_data = await tts.text_to_speech(test_text)
        if audio_data:
            print(f"   ✅ 语音合成成功，音频大小: {len(audio_data)} 字节")
            
            # 保存测试音频
            with open("test_chuner_voice.wav", "wb") as f:
                f.write(audio_data)
            print("   💾 测试音频已保存为 test_chuner_voice.wav")
            
            # 获取音频信息
            audio_info = tts.get_audio_info(audio_data)
            if audio_info:
                print(f"   📊 音频信息: {audio_info}")
            
            return True
        else:
            print("   ❌ 语音合成失败，无音频数据")
            return False
            
    except Exception as e:
        print(f"   ❌ 基本功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_different_voices():
    """测试不同语音"""
    print("\n3. 测试不同语音...")
    try:
        from local_edge_tts import LocalEdgeTTS
        
        test_voices = [
            "zh-CN-XiaoxiaoNeural",  # 晓晓
            "zh-CN-YunxiNeural",     # 云希
            "zh-CN-XiaoyiNeural"     # 晓伊
        ]
        
        test_text = "春儿为您演奏一曲古筝。"
        
        for i, voice_id in enumerate(test_voices):
            print(f"   🎵 测试语音 {i+1}: {voice_id}")
            tts = LocalEdgeTTS(voice_id)
            audio_data = await tts.text_to_speech(test_text)
            if audio_data:
                filename = f"test_voice_{i+1}_{voice_id}.wav"
                with open(filename, "wb") as f:
                    f.write(audio_data)
                print(f"   ✅ 语音 {voice_id} 测试成功，保存为 {filename}")
            else:
                print(f"   ❌ 语音 {voice_id} 测试失败")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 不同语音测试失败: {e}")
        return False

async def test_config_file():
    """测试配置文件"""
    print("\n4. 测试配置文件...")
    try:
        config_file = "local_tts_config.json"
        if os.path.exists(config_file):
            print(f"   ✅ 配置文件存在: {config_file}")
            
            from local_edge_tts import LocalEdgeTTS
            tts = LocalEdgeTTS(config_file=config_file)
            
            # 检查是否从配置文件加载了语音
            voices = tts.get_available_voices()
            print(f"   📋 从配置文件加载了 {len(voices)} 个语音")
            
            return True
        else:
            print(f"   ⚠️  配置文件不存在: {config_file}")
            print("   💡 将使用默认配置")
            return True
            
    except Exception as e:
        print(f"   ❌ 配置文件测试失败: {e}")
        return False

async def test_integration():
    """测试与主系统的集成"""
    print("\n5. 测试系统集成...")
    try:
        # 测试是否可以导入主系统的TTS类
        sys.path.append('.')
        
        # 模拟opt参数
        class MockOpt:
            def __init__(self):
                self.fps = 50
                self.sample_rate = 16000
        
        class MockParent:
            def __init__(self):
                self.sample_rate = 16000
                self.chunk = 320
            
            def put_audio_frame(self, audio_chunk, eventpoint=None):
                pass
        
        opt = MockOpt()
        parent = MockParent()
        
        # 测试LocalEdgeTTS类是否可以正常初始化
        from ttsreal import LocalEdgeTTS
        tts = LocalEdgeTTS(opt, parent)
        print("   ✅ LocalEdgeTTS集成测试成功")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 系统集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("本地EdgeTTS功能测试")
    print("=" * 50)
    
    # 测试导入
    if not test_import():
        print("\n❌ 模块导入失败，请检查依赖安装")
        return False
    
    # 运行异步测试
    async def run_tests():
        results = []
        
        results.append(await test_basic_functionality())
        results.append(await test_different_voices())
        results.append(await test_config_file())
        results.append(await test_integration())
        
        return results
    
    # 运行测试
    test_results = asyncio.run(run_tests())
    
    # 输出结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    test_names = [
        "基本功能测试",
        "不同语音测试", 
        "配置文件测试",
        "系统集成测试"
    ]
    
    all_passed = True
    for i, (name, result) in enumerate(zip(test_names, test_results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{i+1}. {name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！本地EdgeTTS功能正常")
        print("💡 现在可以运行 2.webui_local_tts.bat 启动本地语音数字人系统")
    else:
        print("⚠️  部分测试失败，请检查错误信息并修复问题")
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

