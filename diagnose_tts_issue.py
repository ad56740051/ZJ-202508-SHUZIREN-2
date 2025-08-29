#!/usr/bin/env python3
"""
数字人TTS问题诊断脚本
检查数字人实际使用的TTS引擎和配置
"""

import os
import sys
import json
import argparse

def check_tts_configuration():
    """检查TTS配置"""
    print("==================================================")
    print("TTS配置检查")
    print("==================================================")
    
    # 检查配置文件
    config_file = "local_tts_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ 配置文件存在: {config_file}")
            print(f"   默认语音: {config.get('tts_settings', {}).get('default_voice', '未设置')}")
            print(f"   可用语音数量: {len(config.get('tts_settings', {}).get('available_voices', {}))}")
        except Exception as e:
            print(f"❌ 配置文件读取失败: {e}")
    else:
        print(f"❌ 配置文件不存在: {config_file}")
    
    # 检查依赖包
    print("\n依赖包检查:")
    try:
        import edge_tts
        print("✅ edge-tts 已安装")
    except ImportError:
        print("❌ edge-tts 未安装")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 已安装")
    except ImportError:
        print("❌ pyttsx3 未安装")
    
    try:
        import soundfile as sf
        print("✅ soundfile 已安装")
    except ImportError:
        print("❌ soundfile 未安装")

def test_tts_integration():
    """测试TTS集成"""
    print("\n==================================================")
    print("TTS集成测试")
    print("==================================================")
    
    try:
        # 测试LocalEdgeTTS导入
        from local_edge_tts import LocalEdgeTTS
        print("✅ LocalEdgeTTS 导入成功")
        
        # 创建TTS实例
        tts = LocalEdgeTTS()
        print("✅ TTS实例创建成功")
        
        # 检查备选TTS
        if tts.fallback_tts:
            print("✅ 备选TTS引擎可用")
        else:
            print("❌ 备选TTS引擎不可用")
        
        # 测试文本转语音
        test_text = "测试TTS集成功能。"
        print(f"📝 测试文本: {test_text}")
        
        audio_data = tts.text_to_speech_sync(test_text)
        if audio_data:
            print(f"✅ TTS转换成功，音频大小: {len(audio_data)} 字节")
            
            # 保存测试音频
            with open("diagnose_test.wav", "wb") as f:
                f.write(audio_data)
            print("💾 诊断测试音频已保存为 diagnose_test.wav")
            
            return True
        else:
            print("❌ TTS转换失败，无音频数据")
            return False
            
    except Exception as e:
        print(f"❌ TTS集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_app_configuration():
    """检查应用配置"""
    print("\n==================================================")
    print("应用配置检查")
    print("==================================================")
    
    # 检查app.py中的TTS配置
    try:
        with open("app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找TTS相关配置
        if '--tts' in content:
            print("✅ app.py 包含TTS参数配置")
        else:
            print("❌ app.py 未找到TTS参数配置")
        
        if 'local_edgetts' in content:
            print("✅ app.py 包含本地TTS配置")
        else:
            print("❌ app.py 未找到本地TTS配置")
        
        # 查找默认TTS设置
        import re
        default_tts_match = re.search(r'default\s*=\s*[\'"]([^\'"]*)[\'"]', content)
        if default_tts_match:
            default_tts = default_tts_match.group(1)
            print(f"📋 默认TTS设置: {default_tts}")
        else:
            print("❌ 未找到默认TTS设置")
            
    except Exception as e:
        print(f"❌ 应用配置检查失败: {e}")

def check_basereal_integration():
    """检查basereal.py中的TTS集成"""
    print("\n==================================================")
    print("basereal.py TTS集成检查")
    print("==================================================")
    
    try:
        with open("basereal.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查TTS导入
        if 'from ttsreal import' in content:
            print("✅ basereal.py 导入了TTS模块")
        else:
            print("❌ basereal.py 未导入TTS模块")
        
        # 检查LocalEdgeTTS使用
        if 'LocalEdgeTTS' in content:
            print("✅ basereal.py 包含LocalEdgeTTS")
        else:
            print("❌ basereal.py 未找到LocalEdgeTTS")
        
        # 检查TTS初始化
        if 'opt.tts == "local_edgetts"' in content:
            print("✅ basereal.py 包含本地TTS初始化逻辑")
        else:
            print("❌ basereal.py 未找到本地TTS初始化逻辑")
            
    except Exception as e:
        print(f"❌ basereal.py 检查失败: {e}")

def check_ttsreal_implementation():
    """检查ttsreal.py中的LocalEdgeTTS实现"""
    print("\n==================================================")
    print("ttsreal.py LocalEdgeTTS实现检查")
    print("==================================================")
    
    try:
        with open("ttsreal.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查LocalEdgeTTS类
        if 'class LocalEdgeTTS' in content:
            print("✅ ttsreal.py 包含LocalEdgeTTS类")
        else:
            print("❌ ttsreal.py 未找到LocalEdgeTTS类")
        
        # 检查txt_to_audio方法
        if 'def txt_to_audio' in content:
            print("✅ ttsreal.py 包含txt_to_audio方法")
        else:
            print("❌ ttsreal.py 未找到txt_to_audio方法")
        
        # 检查备选TTS逻辑
        if 'fallback_tts' in content:
            print("✅ ttsreal.py 包含备选TTS逻辑")
        else:
            print("❌ ttsreal.py 未找到备选TTS逻辑")
            
    except Exception as e:
        print(f"❌ ttsreal.py 检查失败: {e}")

def simulate_app_startup():
    """模拟应用启动过程"""
    print("\n==================================================")
    print("应用启动模拟")
    print("==================================================")
    
    try:
        # 模拟命令行参数
        sys.argv = ['app.py', '--avatar_id', 'avatar11', '--customvideo_config', 'custom_video.json', '--tts', 'local_edgetts']
        
        # 导入app模块
        import app
        
        # 检查参数解析
        if hasattr(app, 'parser'):
            args = app.parser.parse_args()
            print(f"✅ 参数解析成功")
            print(f"   TTS类型: {args.tts}")
            print(f"   头像ID: {args.avatar_id}")
            print(f"   自定义视频配置: {args.customvideo_config}")
        else:
            print("❌ 未找到参数解析器")
            
    except Exception as e:
        print(f"❌ 应用启动模拟失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("开始数字人TTS问题诊断...")
    
    # 执行各项检查
    check_tts_configuration()
    tts_integration_result = test_tts_integration()
    check_app_configuration()
    check_basereal_integration()
    check_ttsreal_implementation()
    simulate_app_startup()
    
    print("\n==================================================")
    print("诊断结果汇总")
    print("==================================================")
    print(f"TTS集成测试: {'✅ 通过' if tts_integration_result else '❌ 失败'}")
    
    if tts_integration_result:
        print("\n🎉 TTS功能正常，问题可能在于:")
        print("1. 数字人启动时未使用正确的TTS参数")
        print("2. 应用配置问题")
        print("3. 音频播放管道问题")
        
        print("\n💡 建议解决方案:")
        print("1. 确保使用 2.webui_local_tts.bat 启动")
        print("2. 检查启动参数是否包含 --tts local_edgetts")
        print("3. 查看 wav2lip_realtime.log 中的详细错误信息")
    else:
        print("\n⚠️ TTS功能异常，需要修复TTS集成问题")
    
    print("==================================================")

if __name__ == "__main__":
    main()


