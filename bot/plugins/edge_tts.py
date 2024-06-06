import datetime
from typing import Dict
import edge_tts
import asyncio
from .plugin import Plugin

class EdgeTTSTextToSpeech(Plugin):
    """
    A plugin to convert text to speech using Microsoft Edge's Text to Speech API
    """

    def get_source_name(self) -> str:
        return "EdgeTTS"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "edge_text_to_speech",
            "description": "Convert text to speech using Microsoft Edge's Text to Speech API",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to convert to speech"},
                    "voice": {"type": "string", "description": "The voice to use for the text to speech conversion"},
                    "lang": {"type": "string", "description": "The language of the text to convert to speech"}
                },
                "required": ["text"],
            }
        }]

    async def text_to_speech(self, text, voice, output_file):
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save(output_file)

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        if function_name == "edge_text_to_speech":
            text = kwargs['text']
            lang = kwargs.get('lang', 'en-US')
            voice = kwargs.get('voice')

            # 如果沒有指定語音，根據語言選擇適當的語音
            if not voice:
                if lang == 'zh-HK':
                    voice = 'zh-HK-WanLungNeural'
                elif lang == 'en-US':
                    voice = 'en-US-GuyNeural'
                
                # 可以根據需要添加更多語言和語音的對應關係
                else:
                    voice = 'zh-HK-WanLungNeural'  # 默認語音

            output = f'edge_tts_{datetime.datetime.now().timestamp()}.mp3'
            await self.text_to_speech(text, voice, output)
            return {
                'direct_result': {
                    'kind': 'file',
                    'format': 'path',
                    'value': output
                }
            }
        else:
            return {
                'status': 'error',
                'message': f'Function {function_name} not found'
            }
