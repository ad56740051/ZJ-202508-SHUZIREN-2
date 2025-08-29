#!/usr/bin/env python3
"""
修复TTS问题脚本
确保数字人使用本地TTS而不是在线TTS
"""

import os
import sys
import time

def fix_tts_issue():
    """修复TTS问题"""
    print("==================================================")
    print("修复TTS问题")
    print("==================================================")
    
    # 1. 检查当前配置
    print("1. 检查当前配置...")
    
    # 检查启动脚本
    if os.path.exists("2.webui_local_tts.bat"):
        print("✅ 本地TTS启动脚本存在")
    else:
        print("❌ 本地TTS启动脚本不存在")
    
    # 检查app.py中的默认TTS设置
    try:
        with open("app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'default=\'local_edgetts\'' in content:
            print("✅ app.py 默认使用本地TTS")
        else:
            print("❌ app.py 默认不使用本地TTS")
            
    except Exception as e:
        print(f"❌ 检查app.py失败: {e}")
    
    # 2. 测试备选TTS功能
    print("\n2. 测试备选TTS功能...")
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        tts = LocalEdgeTTS()
        
        if tts.fallback_tts:
            print("✅ 备选TTS引擎可用")
            
            # 测试备选TTS
            test_text = "测试备选TTS功能。"
            audio_data = tts._fallback_text_to_speech_sync(test_text)
            
            if audio_data:
                print(f"✅ 备选TTS转换成功，音频大小: {len(audio_data)} 字节")
                
                # 保存测试音频
                with open("fix_test.wav", "wb") as f:
                    f.write(audio_data)
                print("💾 修复测试音频已保存为 fix_test.wav")
                
                return True
            else:
                print("❌ 备选TTS转换失败")
                return False
        else:
            print("❌ 备选TTS引擎不可用")
            return False
            
    except Exception as e:
        print(f"❌ 备选TTS测试失败: {e}")
        return False

def create_offline_tts_script():
    """创建离线TTS启动脚本"""
    print("\n3. 创建离线TTS启动脚本...")
    
    script_content = '''@echo off
chcp 65001
set PYTHONUSERBASE=.\python\Lib\site-packages
set PYTHONPATH=.\python\Lib\site-packages
set PATH=%PATH%;.\python\Scripts
echo 启动离线TTS数字人系统...
echo 正在使用本地语音合成，无需联网...
echo 强制使用备选TTS引擎...
.\python\python.exe app.py --avatar_id avatar11 --customvideo_config custom_video.json --tts local_edgetts
pause
'''
    
    try:
        with open("2.webui_offline_tts.bat", 'w', encoding='utf-8') as f:
            f.write(script_content)
        print("✅ 离线TTS启动脚本已创建: 2.webui_offline_tts.bat")
        return True
    except Exception as e:
        print(f"❌ 创建启动脚本失败: {e}")
        return False

def modify_local_edge_tts():
    """修改local_edge_tts.py，强制使用备选TTS"""
    print("\n4. 修改local_edge_tts.py...")
    
    try:
        with open("local_edge_tts.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经修改过
        if '# FORCE_FALLBACK_TTS' in content:
            print("✅ local_edge_tts.py 已经修改过")
            return True
        
        # 修改text_to_speech方法，强制使用备选TTS
        old_method = '''    async def text_to_speech(self, text: str, output_path: Optional[str] = None) -> bytes:
        """
        文本转语音
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径，如果为None则返回音频数据
            
        Returns:
            音频数据(bytes)
        """
        try:
            logger.info(f"开始转换文本: {text[:50]}...")
            start_time = time.time()
            
            # 首先尝试使用edge-tts
            try:'''
        
        new_method = '''    async def text_to_speech(self, text: str, output_path: Optional[str] = None) -> bytes:
        """
        文本转语音
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径，如果为None则返回音频数据
            
        Returns:
            音频数据(bytes)
        """
        try:
            logger.info(f"开始转换文本: {text[:50]}...")
            start_time = time.time()
            
            # FORCE_FALLBACK_TTS: 强制使用备选TTS，避免网络问题
            if self.fallback_tts:
                logger.info("强制使用备选TTS引擎...")
                return await self._fallback_text_to_speech(text, output_path)
            
            # 首先尝试使用edge-tts
            try:'''
        
        if old_method in content:
            content = content.replace(old_method, new_method)
            
            with open("local_edge_tts.py", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ local_edge_tts.py 已修改，强制使用备选TTS")
            return True
        else:
            print("❌ 未找到需要修改的方法")
            return False
            
    except Exception as e:
        print(f"❌ 修改local_edge_tts.py失败: {e}")
        return False

def main():
    """主函数"""
    print("开始修复TTS问题...")
    
    # 执行修复步骤
    step1 = fix_tts_issue()
    step2 = create_offline_tts_script()
    step3 = modify_local_edge_tts()
    
    print("\n==================================================")
    print("修复结果汇总")
    print("==================================================")
    print(f"1. TTS功能检查: {'✅ 通过' if step1 else '❌ 失败'}")
    print(f"2. 创建离线启动脚本: {'✅ 成功' if step2 else '❌ 失败'}")
    print(f"3. 修改TTS配置: {'✅ 成功' if step3 else '❌ 失败'}")
    
    if step1 and step2 and step3:
        print("\n🎉 修复完成！")
        print("\n💡 现在请使用以下命令启动数字人:")
        print("   2.webui_offline_tts.bat")
        print("\n⚠️ 重要说明:")
        print("   - 此脚本强制使用本地TTS，无需网络连接")
        print("   - 音质可能比在线TTS稍差，但响应更快")
        print("   - 确保音频设备正常工作")
    else:
        print("\n⚠️ 部分修复失败，请检查错误信息")
    
    print("==================================================")

if __name__ == "__main__":
    main()


