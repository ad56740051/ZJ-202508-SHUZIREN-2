ZJ-SHUZIREN 接口对接文档（含 Python 示例）

版本
- 仓库：ad56740051/ZJ-SHUZIREN
- 主要文件：app.py, webrtc.py, web/*
- 协议/框架：HTTP(aiohttp) + WebRTC(aiortc)，CORS 已开启(*)

概览
- 服务启动参数
  - 监听端口：--listenport（默认 8010）
  - 传输模式：--transport webrtc|rtmp|rtcpush（默认 webrtc）
  - 会话上限：--max_session（默认 1）
- 统一会话管理
  - 通过 POST /offer 进行 WebRTC SDP 协商，成功后返回 sessionid
  - 之后所有控制接口均需携带 sessionid
- 鉴权说明
  - 代码中未实现鉴权/签名校验，默认无鉴权
- 静态页面
  - / 路径下提供 web/ 目录中的演示页面，可参考调用流程

接口清单
1) WebRTC 会话协商：POST /offer
- 用于建立数字人的音视频下行流（人像画面 + 语音）
- 请求体（JSON）
  {
    "sdp": "<client-offer-sdp>",
    "type": "offer"
  }
- 响应体（JSON）
  {
    "sdp": "<server-answer-sdp>",
    "type": "answer",
    "sessionid": 123456
  }
- 特性与限制
  - 服务器端设置视频编解码器优先级：H264/VP8/rtx
  - 当会话数达到 opt.max_session（默认 1）会拒绝新连接
- 可直接调用：是（标准 WebRTC Offer/Answer 流程）

2) 文本驱动说话（联动 LLM+TTS）：POST /human
- 通过文本让数字人说话；type=chat 时会调用内置 LLM 流式生成文本并逐句播报；type=echo 时直接播报 text
- 请求体（JSON）
  {
    "sessionid": 123456,
    "type": "chat" | "echo",
    "text": "你好",
    "interrupt": true
  }
  - sessionid：/offer 返回
  - type：chat 走 LLM；echo 直接播报 text
  - interrupt：true 时先打断当前发声
- 响应体（JSON）
  { "code": 0, "data": "ok" }
- 可直接调用：是

3) 上传音频文件播放/对口型：POST /humanaudio
- 使用已有音频内容驱动（例如对口型）
- 请求体（multipart/form-data）
  - 字段：sessionid: number, file: File（二进制音频）
- 响应体（JSON）
  - 成功：{ "code": 0, "msg": "ok" }
  - 失败：{ "code": -1, "msg": "err", "data": "<异常信息>" }
- 可直接调用：是

4) 切换音/视频状态：POST /set_audiotype
- 控制数字人输出形态，例如动态口播/静态画面/表演视频
- 请求体（JSON）
  {
    "sessionid": 123456,
    "audiotype": 0 | 1 | 2,
    "reinit": true
  }
  - audiotype 参考前端用法：
    - 0：动态视频口播
    - 1：静态视频
    - 2：表演视频
- 响应体（JSON）
  { "code": 0, "data": "ok" }
- 可直接调用：是

5) 查询是否在说话：POST /is_speaking
- 请求体（JSON）
  { "sessionid": 123456 }
- 响应体（JSON）
  - 会话不存在：{ "code": -1, "data": false, "msg": "Session not found" }
  - 正常：{ "code": 0, "data": true|false }
- 可直接调用：是

6) 录制控制：POST /record
- 控制录制当前输出
- 请求体（JSON）
  { "sessionid": 123456, "type": "start_record" | "end_record" }
- 响应体（JSON）
  { "code": 0, "data": "ok" }
- 可直接调用：是

注意事项
- 前端脚本里存在 /get_audiotype 的调用样例，但后端未实现该路由；请使用 /is_speaking 与 /set_audiotype 实现状态感知与切换
- CORS 已全量开启；可跨域直接调用
- LLM 默认对接阿里 DashScope 兼容 OpenAI API（模型 qwen-plus），通过环境变量 DASHSCOPE_API_KEY 配置；仅在 type="chat" 场景生效

典型调用流程
1) 客户端生成 WebRTC offer SDP
2) POST /offer → 获得 answer SDP 与 sessionid
3) 客户端 setRemoteDescription(answer) 完成 WebRTC 连接，开始接收数字人画面与语音
4) 发送文本触发发声：POST /human（type="chat"/"echo"）
5) 或上传音频：POST /humanaudio
6) 可选：POST /set_audiotype 切换状态
7) 可选：轮询 POST /is_speaking 以判断说话状态
8) 可选：POST /record 开始/结束录制

Python 示例代码

依赖安装
- pip install aiortc requests aiohttp

1) WebRTC 协商并接收媒体（aiortc）
import asyncio
import json
import requests
from aiortc import RTCPeerConnection, RTCSessionDescription

BASE_URL = "http://<server-host>:8010"

async def webrtc_connect():
    pc = RTCPeerConnection()

    @pc.on("track")
    def on_track(track):
        print(f"Track received: kind={track.kind}")
        # 在这里可将音频/视频保存或播放（例如保存为文件需要额外处理）

    # 客户端声明只接收音视频
    pc.addTransceiver("video", direction="recvonly")
    pc.addTransceiver("audio", direction="recvonly")

    # 生成本地 offer
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # 请求 /offer，获取 answer 与 sessionid
    r = requests.post(
        f"{BASE_URL}/offer",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}),
        timeout=15,
    )
    r.raise_for_status()
    ans = r.json()
    sessionid = ans["sessionid"]

    # 设置远端描述，完成连接
    await pc.setRemoteDescription(RTCSessionDescription(sdp=ans["sdp"], type=ans["type"]))
    print("WebRTC connected, sessionid =", sessionid)
    return pc, sessionid

if __name__ == "__main__":
    asyncio.run(webrtc_connect())

2) 文本触发发声：/human
import json
import requests

BASE_URL = "http://<server-host>:8010"

def send_text(sessionid: int, text: str, mode="chat", interrupt=True):
    payload = {
        "sessionid": sessionid,
        "type": mode,      # "chat" 走 LLM, "echo" 直接播报 text
        "text": text,
        "interrupt": interrupt
    }
    r = requests.post(f"{BASE_URL}/human", headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=15)
    r.raise_for_status()
    print("human:", r.json())

# 使用示例
# send_text(123456, "你好，今天天气怎么样？", mode="chat")

3) 上传音频：/humanaudio
import requests

BASE_URL = "http://<server-host>:8010"

def upload_audio(sessionid: int, filepath: str):
    files = {
        "file": open(filepath, "rb")
    }
    data = {"sessionid": str(sessionid)}
    r = requests.post(f"{BASE_URL}/humanaudio", files=files, data=data, timeout=60)
    r.raise_for_status()
    print("humanaudio:", r.json())

# 使用示例
# upload_audio(123456, "/path/to/audio.wav")

4) 切换状态：/set_audiotype
import json
import requests

BASE_URL = "http://<server-host>:8010"

def set_audiotype(sessionid: int, audiotype: int, reinit: bool = True):
    payload = {
        "sessionid": sessionid,
        "audiotype": audiotype,  # 0 动态口播; 1 静态视频; 2 表演视频
        "reinit": reinit
    }
    r = requests.post(f"{BASE_URL}/set_audiotype", headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=15)
    r.raise_for_status()
    print("set_audiotype:", r.json())

# 使用示例
# set_audiotype(123456, 2, True)

5) 查询是否在说话：/is_speaking
import json
import requests

BASE_URL = "http://<server-host>:8010"

def is_speaking(sessionid: int) -> bool:
    payload = {"sessionid": sessionid}
    r = requests.post(f"{BASE_URL}/is_speaking", headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=10)
    r.raise_for_status()
    data = r.json()
    if data.get("code") == 0:
        return bool(data.get("data"))
    else:
        return False

# 使用示例
# print(is_speaking(123456))

6) 录制控制：/record
import json
import requests

BASE_URL = "http://<server-host>:8010"

def record_control(sessionid: int, action: str):
    assert action in ("start_record", "end_record")
    payload = {"sessionid": sessionid, "type": action}
    r = requests.post(f"{BASE_URL}/record", headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=15)
    r.raise_for_status()
    print("record:", r.json())

# 使用示例
# record_control(123456, "start_record")
# record_control(123456, "end_record")

错误处理与超时建议
- HTTP 调用建议设置超时并检查返回 JSON 中的 code 字段
- /offer 失败常见原因：超过 max_session、SDP 不兼容、网络不可达
- /humanaudio 建议限制文件大小与类型；异常返回时会在 data 中给出异常信息
- 对于 WebRTC 轨道 track，可根据业务需要落盘（需要额外编码）或实时播放/分析

安全与上线建议
- 建议为所有接口增加鉴权（例如 token、签名、来源校验），并加上限流与会话清理
- 生产环境建议部署在 HTTPS，WebRTC 建议在安全上下文访问
- 达到会话上限时，客户端侧应重试/排队或给出提示

参考代码位置（便于验证）
- 路由注册与 CORS：app.py (474-517)
- /offer: app.py (206-256)
- /human: app.py (258-276)
- /humanaudio: app.py (278-299)
- /set_audiotype: app.py (301-312)
- /is_speaking: app.py (330-346)
- /record: app.py (314-328)
- WebRTC 媒体发送类：webrtc.py（HumanPlayer / PlayerStreamTrack）

如需我提供一个可运行的 Python Demo（整合协商 + 控制 + 简易媒体处理），也可以继续补充。
