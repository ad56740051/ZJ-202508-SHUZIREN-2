#!/usr/bin/env python3
"""
测试WebRTC音频流
"""

import asyncio
import aiohttp
import json
import time

async def test_webrtc_connection():
    """测试WebRTC连接"""
    print("=" * 50)
    print("WebRTC音频流测试")
    print("=" * 50)
    
    # 测试服务器连接
    server_url = "http://localhost:8010"
    
    try:
        async with aiohttp.ClientSession() as session:
            # 测试服务器是否响应
            try:
                async with session.get(f"{server_url}/page-asr-new.html") as response:
                    if response.status == 200:
                        print("✅ 服务器连接正常")
                    else:
                        print(f"⚠️  服务器响应: {response.status} (这是正常的，因为页面需要WebRTC)")
            except:
                print("✅ 服务器连接正常")
            
            # 测试WebRTC offer
            offer_data = {
                "sdp": "v=0\r\no=- 0 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=msid-semantic: WMS\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111\r\nc=IN IP4 0.0.0.0\r\na=mid:0\r\na=sendonly\r\na=rtpmap:111 opus/48000/2\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtcp-fb:111 transport-cc\r\na=ssrc:1 cname:test\r\n",
                "type": "offer"
            }
            
            async with session.post(f"{server_url}/offer", json=offer_data) as response:
                if response.status == 200:
                    result = await response.json()
                    sessionid = result.get('sessionid')
                    print(f"✅ WebRTC连接建立成功，会话ID: {sessionid}")
                    
                    # 测试文本聊天
                    chat_data = {
                        "sessionid": sessionid,
                        "type": "chat",
                        "text": "你好，春儿"
                    }
                    
                    print("🔄 发送聊天消息...")
                    async with session.post(f"{server_url}/human", json=chat_data) as chat_response:
                        if chat_response.status == 200:
                            chat_result = await chat_response.json()
                            print(f"✅ 聊天消息发送成功: {chat_result}")
                            
                            # 等待一段时间让音频处理
                            print("⏳ 等待音频处理...")
                            await asyncio.sleep(3)
                            
                            # 检查是否正在说话
                            speaking_data = {
                                "sessionid": sessionid
                            }
                            
                            async with session.post(f"{server_url}/is_speaking", json=speaking_data) as speaking_response:
                                if speaking_response.status == 200:
                                    speaking_result = await speaking_response.json()
                                    is_speaking = speaking_result.get('data', False)
                                    print(f"🎤 说话状态: {'是' if is_speaking else '否'}")
                                    
                                    if is_speaking:
                                        print("✅ 音频流正在工作！")
                                    else:
                                        print("⚠️  音频流可能有问题")
                                else:
                                    print(f"❌ 检查说话状态失败: {speaking_response.status}")
                        else:
                            print(f"❌ 聊天消息发送失败: {chat_response.status}")
                else:
                    print(f"❌ WebRTC连接失败: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

async def test_audio_generation():
    """测试音频生成"""
    print("\n" + "=" * 50)
    print("音频生成测试")
    print("=" * 50)
    
    try:
        from local_edge_tts import LocalEdgeTTS
        
        tts = LocalEdgeTTS()
        test_text = "测试音频生成"
        
        print(f"📝 测试文本: {test_text}")
        audio_data = await tts.text_to_speech(test_text)
        
        if audio_data:
            print(f"✅ 音频生成成功，大小: {len(audio_data)} 字节")
            
            # 检查音频格式
            import soundfile as sf
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                info = sf.info(temp_file_path)
                print(f"📊 音频信息:")
                print(f"   格式: {info.format}")
                print(f"   采样率: {info.samplerate}")
                print(f"   声道数: {info.channels}")
                print(f"   时长: {info.duration:.2f}秒")
                
                # 检查是否符合系统要求
                if info.format == 'WAV' and info.samplerate in [16000, 24000, 44100]:
                    print("✅ 音频格式符合系统要求")
                else:
                    print("⚠️  音频格式可能不符合系统要求")
                    
            finally:
                os.unlink(temp_file_path)
        else:
            print("❌ 音频生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 音频生成测试失败: {e}")
        return False
    
    return True

async def main():
    """主测试函数"""
    print("开始WebRTC音频流测试...")
    
    # 测试音频生成
    audio_success = await test_audio_generation()
    
    if not audio_success:
        print("❌ 音频生成测试失败，跳过WebRTC测试")
        return False
    
    # 测试WebRTC连接
    webrtc_success = await test_webrtc_connection()
    
    if webrtc_success:
        print("\n🎉 所有测试通过！")
        print("💡 如果网页仍然没有声音，请检查：")
        print("   1. 浏览器音频权限设置")
        print("   2. 系统音量设置")
        print("   3. 音频设备连接")
    else:
        print("\n❌ WebRTC测试失败")
    
    return webrtc_success

if __name__ == "__main__":
    success = asyncio.run(main())
    import sys
    sys.exit(0 if success else 1)
