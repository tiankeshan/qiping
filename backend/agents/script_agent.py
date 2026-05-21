"""
Script Agent - AI 脚本生成智能体

该模块负责：
1. 生成漫剧脚本
2. 管理角色对话
3. 优化场景描述
4. 支持多种类型和风格
"""

import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ScriptAgent:
    """脚本生成智能体"""
    
    def __init__(self, llm_provider: str = "openai", api_key: str = None):
        """
        初始化 Script Agent
        
        Args:
            llm_provider: LLM 提供商 (openai, claude, etc.)
            api_key: API 密钥
        """
        self.llm_provider = llm_provider
        self.api_key = api_key
        self.model_config = self._get_model_config()
    
    def _get_model_config(self) -> Dict:
        """获取模型配置"""
        configs = {
            "openai": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 4000
            },
            "claude": {
                "model": "claude-3-opus-20240229",
                "temperature": 0.7,
                "max_tokens": 4000
            }
        }
        return configs.get(self.llm_provider, configs["openai"])
    
    async def generate_script(
        self,
        title: str,
        genre: str,
        premise: str,
        episodes: int = 1,
        style: str = "vertical_drama",
        characters: Optional[List[Dict]] = None
    ) -> Dict:
        """
        生成漫剧脚本
        
        Args:
            title: 漫剧标题
            genre: 类型 (romance, fantasy, mystery, etc.)
            premise: 剧情前提
            episodes: 剧集数
            style: 风格 (vertical_drama, comic, etc.)
            characters: 预定义的角色列表
        
        Returns:
            生成的脚本数据
        """
        logger.info(f"开始生成脚本: {title}")
        
        try:
            # 构建 prompt
            prompt = self._build_prompt(
                title=title,
                genre=genre,
                premise=premise,
                episodes=episodes,
                style=style,
                characters=characters
            )
            
            # 调用 LLM API（这里用模拟实现示例）
            script_content = await self._call_llm(prompt)
            
            # 解析脚本
            parsed_script = self._parse_script(script_content)
            
            logger.info(f"脚本生成成功: {title}")
            
            return {
                "status": "success",
                "script_id": f"script_{datetime.now().timestamp()}",
                "title": title,
                "genre": genre,
                "episodes": episodes,
                "content": parsed_script,
                "generated_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"脚本生成失败: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _build_prompt(
        self,
        title: str,
        genre: str,
        premise: str,
        episodes: int,
        style: str,
        characters: Optional[List[Dict]]
    ) -> str:
        """构建 LLM prompt"""
        
        character_desc = ""
        if characters:
            character_desc = "\n角色设定:\n"
            for char in characters:
                character_desc += f"- {char.get('name', '未命名')}: {char.get('description', '')}\n"
        
        prompt = f"""
你是一位专业的漫剧编剧。根据以下信息生成一个{episodes}集的{genre}类型漫剧脚本。

标题: {title}
类型: {genre}
风格: {style}
前提: {premise}

{character_desc}

请按以下格式生成脚本:

第N幕
======
场景: [地点]
描述: [场景描述]
人物: [参与人物]

对话:
[人物名称]: [对话内容]
[人物名称]: [对话内容]

请确保：
1. 剧情引人入胜
2. 人物对话自然流畅
3. 符合{genre}类型的特点
4. 适合{style}的呈现方式
5. 总共{episodes}集，每集3-5幕
"""
        return prompt
    
    async def _call_llm(self, prompt: str) -> str:
        """
        调用 LLM API
        
        这里是模拟实现。在实际应用中，应该集成真实的 API 调用
        """
        # 模拟 API 调用延迟
        await asyncio.sleep(0.5)
        
        # 返回示例脚本
        mock_response = """
第一幕
======
场景: 办公室
描述: 豪华的CEO办公室，落地窗外是城市夜景
人物: 林雨欣（CEO女主），快递员（男主）

对话:
林雨欣: 这个快递应该不是给我的...
快递员: 抱歉，这确实是这间办公室的...
林雨欣: 我很忙，直接放在这里吧
快递员: 好的，签名一下就行

第二幕
======
场景: 办公室（稍后）
描述: 林雨欣打开快递，发现是心头所想的设计模型
人物: 林雨欣

对话:
林雨欣: (惊喜) 竟然是这个... 太棒了!
"""
        return mock_response
    
    def _parse_script(self, raw_script: str) -> Dict:
        """
        解析原始脚本文本
        
        将文本解析为结构化的场景和对话数据
        """
        scenes = []
        current_scene = None
        
        lines = raw_script.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('第') and '幕' in line:
                # 新场景
                if current_scene:
                    scenes.append(current_scene)
                current_scene = {
                    "scene_no": len(scenes) + 1,
                    "title": line,
                    "location": "",
                    "description": "",
                    "characters": [],
                    "dialogues": []
                }
            
            elif line.startswith('场景:') and current_scene:
                current_scene["location"] = line.replace('场景:', '').strip()
            
            elif line.startswith('描述:') and current_scene:
                current_scene["description"] = line.replace('描述:', '').strip()
            
            elif line.startswith('人物:') and current_scene:
                chars = line.replace('人物:', '').strip().split('，')
                current_scene["characters"] = chars
            
            elif ':' in line and current_scene and not line.startswith('第'):
                # 对话行
                parts = line.split(':', 1)
                if len(parts) == 2:
                    current_scene["dialogues"].append({
                        "character": parts[0].strip(),
                        "text": parts[1].strip()
                    })
        
        if current_scene:
            scenes.append(current_scene)
        
        return {
            "total_scenes": len(scenes),
            "scenes": scenes
        }
    
    async def optimize_script(self, script: Dict) -> Dict:
        """
        优化脚本质量
        
        包括改进对话、调整节奏等
        """
        logger.info("开始优化脚本...")
        
        # 这里可以添加更多的优化逻辑
        # 比如检查对话长度、节奏等
        
        return script
    
    def get_script_stats(self, script: Dict) -> Dict:
        """获取脚本统计信息"""
        scenes = script.get("scenes", [])
        total_dialogues = sum(len(s.get("dialogues", [])) for s in scenes)
        total_characters = len(set(
            d.get("character") for s in scenes for d in s.get("dialogues", [])
        ))
        
        return {
            "total_scenes": len(scenes),
            "total_dialogues": total_dialogues,
            "unique_characters": total_characters,
            "avg_dialogues_per_scene": total_dialogues / len(scenes) if scenes else 0
        }


# 创建全局 Script Agent 实例
script_agent = ScriptAgent(llm_provider="openai")
