#!/usr/bin/env python3
"""
简单的音频测试
"""

import asyncio
import aiohttp
import json

async def test_simple_chat():
    """测试简单的聊天功能"""
    print("=" * 50)
    print("简单聊天测试")
    print("=" * 50)
    
    server_url = "http://localhost:8010"
    
    try:
        async with aiohttp.ClientSession() as session:
            # 创建WebRTC连接
            offer_data = {
                "sdp": "v=0\r\no=- 0 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=msid-semantic: WMS\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111\r\nc=IN IP4 0.0.0.0\r\na=mid:0\r\na=sendonly\r\na=rtpmap:111 opus/48000/2\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtcp-fb:111 transport-cc\r\na=ssrc:1 cname:test\r\n",
                "type": "offer"
            }
            
            print("🔄 建立WebRTC连接...")
            async with session.post(f"{server_url}/offer", json=offer_data) as response:
                if response.status == 200:
                    result = await response.json()
                    sessionid = result.get('sessionid')
                    print(f"✅ WebRTC连接成功，会话ID: {sessionid}")
                    
                    # 发送聊天消息
                    chat_data = {
                        "sessionid": sessionid,
                        "type": "chat",
                        "text": "你好，春儿"
                    }
                    
                    print("🔄 发送聊天消息...")
                    async with session.post(f"{server_url}/human", json=chat_data) as chat_response:
                        if chat_response.status == 200:
                            print("✅ 聊天消息发送成功")
                            
                            # 等待音频处理
                            print("⏳ 等待音频处理...")
                            await asyncio.sleep(2)
                            
                            # 检查说话状态
                            speaking_data = {"sessionid": sessionid}
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
                                    print(f"❌ 检查说话状态失败")
                        else:
                            print(f"❌ 聊天消息发送失败: {chat_response.status}")
                else:
                    print(f"❌ WebRTC连接失败: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_simple_chat())
    if success:
        print("\n🎉 测试完成！")
        print("💡 请在浏览器中访问: http://localhost:8010/page-asr-new.html")
        print("💡 如果仍然没有声音，请检查浏览器音频权限")
    else:
        print("\n❌ 测试失败")
    
    import sys
    sys.exit(0 if success else 1)

