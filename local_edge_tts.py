#!/usr/bin/env python3
"""
本地EdgeTTS服务
基于edge-tts库实现本地语音合成，无需联网
"""

import asyncio
import edge_tts
import tempfile
import os
import json
import time
import logging
from typing import Optional, Dict, Any
import numpy as np
import soundfile as sf
from io import BytesIO

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalEdgeTTS:
    """本地EdgeTTS服务类"""
    
    def __init__(self, voice_name: str = "zh-CN-XiaoxiaoNeural", config_file: str = "local_tts_config.json"):
        """
        初始化本地EdgeTTS
        
        Args:
            voice_name: 语音名称，默认使用中文女声
            config_file: 配置文件路径
        """
        self.voice_name = voice_name
        self.config_file = config_file
        self.available_voices = {}
        self.config = {}
        self._load_config()
        self._load_available_voices()
        self._init_fallback_tts()
    
    def _init_fallback_tts(self):
        """初始化备选TTS引擎"""
        self.fallback_tts = None
        try:
            import pyttsx3
            self.fallback_tts = pyttsx3.init()
            # 设置语音属性
            self.fallback_tts.setProperty('rate', 150)  # 语速
            self.fallback_tts.setProperty('volume', 0.9)  # 音量
            logger.info("备选TTS引擎(pyttsx3)初始化成功")
        except ImportError:
            logger.warning("pyttsx3未安装，备选TTS不可用")
        except Exception as e:
            logger.warning(f"备选TTS引擎初始化失败: {e}")
    
    def _load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"成功加载配置文件: {self.config_file}")
            else:
                logger.warning(f"配置文件不存在: {self.config_file}，使用默认配置")
                self.config = {}
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            self.config = {}
        
    def _load_available_voices(self):
        """加载可用的语音列表"""
        try:
            # 优先从配置文件加载语音列表
            if self.config and 'tts_settings' in self.config and 'available_voices' in self.config['tts_settings']:
                self.available_voices = self.config['tts_settings']['available_voices']
                logger.info(f"从配置文件加载了 {len(self.available_voices)} 个语音")
            else:
                # 预定义一些常用的中文语音
                self.available_voices = {
                    "zh-CN-XiaoxiaoNeural": "中文女声-晓晓",
                    "zh-CN-YunxiNeural": "中文男声-云希", 
                    "zh-CN-YunyangNeural": "中文男声-云扬",
                    "zh-CN-XiaoyiNeural": "中文女声-晓伊",
                    "zh-CN-YunjianNeural": "中文男声-云健",
                    "zh-CN-XiaohanNeural": "中文女声-晓涵",
                    "zh-CN-YunxiaNeural": "中文女声-云夏",
                    "zh-CN-XiaomoNeural": "中文女声-晓墨",
                    "zh-CN-YunfengNeural": "中文男声-云枫",
                    "zh-CN-XiaoxuanNeural": "中文女声-晓萱",
                    "zh-CN-YunzeNeural": "中文男声-云泽"
                }
                logger.info(f"使用默认配置加载了 {len(self.available_voices)} 个中文语音")
        except Exception as e:
            logger.error(f"加载语音列表失败: {e}")
            # 使用默认语音
            self.available_voices = {"zh-CN-XiaoxiaoNeural": "中文女声-晓晓"}
    
    def get_available_voices(self) -> Dict[str, str]:
        """获取可用的语音列表"""
        return self.available_voices
    
    def set_voice(self, voice_name: str):
        """设置语音"""
        if voice_name in self.available_voices:
            self.voice_name = voice_name
            logger.info(f"设置语音为: {voice_name} ({self.available_voices[voice_name]})")
        else:
            logger.warning(f"语音 {voice_name} 不可用，使用默认语音")
            self.voice_name = "zh-CN-XiaoxiaoNeural"
    
    async def text_to_speech(self, text: str, output_path: Optional[str] = None) -> bytes:
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
            try:
                # 创建临时文件用于存储MP3音频
                temp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                temp_mp3.close()
                
                # 使用edge-tts进行转换，生成MP3
                communicate = edge_tts.Communicate(text, self.voice_name)
                
                with open(temp_mp3.name, "wb") as file:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            file.write(chunk["data"])
                
                # 将MP3转换为WAV格式
                if output_path is None:
                    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                    output_path = temp_wav.name
                    temp_wav.close()
                
                # 使用soundfile读取MP3并转换为WAV
                try:
                    # 读取MP3文件
                    audio_data, sample_rate = sf.read(temp_mp3.name)
                    
                    # 保存为WAV格式
                    sf.write(output_path, audio_data, sample_rate, format='WAV')
                    
                    # 读取生成的WAV文件
                    with open(output_path, "rb") as file:
                        wav_audio_data = file.read()
                    
                    # 清理临时文件
                    os.unlink(temp_mp3.name)
                    if output_path != temp_wav.name:
                        os.unlink(output_path)
                    
                    elapsed_time = time.time() - start_time
                    logger.info(f"EdgeTTS文本转语音完成，耗时: {elapsed_time:.2f}秒")
                    
                    return wav_audio_data
                    
                except Exception as e:
                    logger.error(f"音频格式转换失败: {e}")
                    # 如果转换失败，直接返回MP3数据
                    with open(temp_mp3.name, "rb") as file:
                        mp3_audio_data = file.read()
                    os.unlink(temp_mp3.name)
                    return mp3_audio_data
                    
            except Exception as e:
                logger.warning(f"EdgeTTS转换失败，尝试使用备选TTS: {e}")
                
                # 如果edge-tts失败，使用备选TTS
                if self.fallback_tts:
                    return await self._fallback_text_to_speech(text, output_path)
                else:
                    raise Exception("EdgeTTS失败且无备选TTS可用")
            
        except Exception as e:
            logger.error(f"文本转语音失败: {e}")
            raise
    
    async def _fallback_text_to_speech(self, text: str, output_path: Optional[str] = None) -> bytes:
        """使用备选TTS引擎进行文本转语音"""
        try:
            logger.info("使用备选TTS引擎进行转换...")
            
            if output_path is None:
                temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                output_path = temp_wav.name
                temp_wav.close()
            
            # 使用pyttsx3进行转换
            self.fallback_tts.save_to_file(text, output_path)
            self.fallback_tts.runAndWait()
            
            # 读取生成的WAV文件
            with open(output_path, "rb") as file:
                wav_audio_data = file.read()
            
            # 清理临时文件
            if output_path != temp_wav.name:
                os.unlink(output_path)
            
            logger.info("备选TTS转换完成")
            return wav_audio_data
            
        except Exception as e:
            logger.error(f"备选TTS转换失败: {e}")
            raise
    
    def _fallback_text_to_speech_sync(self, text: str, output_path: Optional[str] = None) -> bytes:
        """同步版本的备选TTS引擎进行文本转语音"""
        try:
            logger.info("使用备选TTS引擎进行转换...")
            
            if output_path is None:
                temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                output_path = temp_wav.name
                temp_wav.close()
            
            # 使用pyttsx3进行转换
            self.fallback_tts.save_to_file(text, output_path)
            self.fallback_tts.runAndWait()
            
            # 读取生成的WAV文件
            with open(output_path, "rb") as file:
                wav_audio_data = file.read()
            
            # 清理临时文件
            if output_path != temp_wav.name:
                os.unlink(output_path)
            
            logger.info("备选TTS转换完成")
            return wav_audio_data
            
        except Exception as e:
            logger.error(f"备选TTS转换失败: {e}")
            raise
    
    def text_to_speech_sync(self, text: str, output_path: Optional[str] = None) -> bytes:
        """
        同步版本的文本转语音
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            
        Returns:
            音频数据(bytes)
        """
        return asyncio.run(self.text_to_speech(text, output_path))
    
    async def text_to_speech_stream(self, text: str) -> bytes:
        """
        流式文本转语音（用于实时处理）
        
        Args:
            text: 要转换的文本
            
        Returns:
            音频数据(bytes)
        """
        try:
            audio_data = b""
            communicate = edge_tts.Communicate(text, self.voice_name)
            
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            return audio_data
            
        except Exception as e:
            logger.error(f"流式文本转语音失败: {e}")
            raise
    
    def get_audio_info(self, audio_data: bytes) -> Dict[str, Any]:
        """
        获取音频信息
        
        Args:
            audio_data: 音频数据
            
        Returns:
            音频信息字典
        """
        try:
            # 将音频数据写入临时文件
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # 读取音频信息
            with sf.SoundFile(temp_file_path) as audio_file:
                info = {
                    "sample_rate": audio_file.samplerate,
                    "channels": audio_file.channels,
                    "duration": len(audio_file) / audio_file.samplerate,
                    "format": audio_file.format,
                    "subtype": audio_file.subtype
                }
            
            # 清理临时文件
            os.unlink(temp_file_path)
            
            return info
            
        except Exception as e:
            logger.error(f"获取音频信息失败: {e}")
            return {}

# 测试函数
async def test_local_edge_tts():
    """测试本地EdgeTTS功能"""
    tts = LocalEdgeTTS()
    
    # 显示可用语音
    voices = tts.get_available_voices()
    print("可用语音:")
    for voice_id, voice_name in voices.items():
        print(f"  {voice_id}: {voice_name}")
    
    # 测试文本转语音
    test_text = "你好，我是春儿，很高兴见到你！"
    print(f"\n测试文本: {test_text}")
    
    try:
        audio_data = await tts.text_to_speech(test_text)
        audio_info = tts.get_audio_info(audio_data)
        
        print(f"转换成功！")
        print(f"音频信息: {audio_info}")
        print(f"音频数据大小: {len(audio_data)} 字节")
        
        # 保存测试音频
        with open("test_output.wav", "wb") as f:
            f.write(audio_data)
        print("测试音频已保存为 test_output.wav")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_local_edge_tts())
