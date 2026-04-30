from .base_agent import BaseAgent
import json


CHARACTER_SYSTEM = """你是一名专业的游戏角色设计师和AI绘图提示词工程师。
你精通Stable Diffusion、Midjourney、DALL-E等AI绘图工具的提示词写作。

你的任务是为游戏角色生成详细的设计描述和AI绘图提示词。

输出必须是严格的JSON格式：
{
  "characters": [
    {
      "role": "角色定位（protagonist/antagonist/npc）",
      "name": "角色名字",
      "visual_description": "详细外观描述（中文，200字）",
      "personality_traits": ["性格特征1", "性格特征2"],
      "sd_prompt": "Stable Diffusion正向提示词（英文）",
      "sd_negative_prompt": "Stable Diffusion反向提示词（英文）",
      "midjourney_prompt": "Midjourney提示词（英文，包含--参数）",
      "color_scheme": ["颜色1", "颜色2"],
      "design_notes": "设计要点说明"
    }
  ],
  "art_direction": {
    "overall_style": "整体美术方向",
    "reference_artists": ["参考画师1", "参考画师2"],
    "mood_board_keywords": ["关键词1", "关键词2", "关键词3"],
    "consistency_guide": "保持一致性的关键要素"
  }
}"""


class CharacterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CharacterAgent",
            system_prompt=CHARACTER_SYSTEM,
        )

    def generate(self, game_concept: dict) -> dict:
        """Generate character designs and art prompts."""
        prompt = f"""根据以下游戏概念，为主要角色生成完整的设计方案和AI绘图提示词：

游戏名称：{game_concept.get('title', '')}
世界背景：{game_concept.get('setting', '')}
美术风格：{game_concept.get('art_style', '')}
色彩方案：{', '.join(game_concept.get('color_palette', []))}

主角信息：{json.dumps(game_concept.get('protagonist', {}), ensure_ascii=False)}
反派信息：{json.dumps(game_concept.get('antagonist', {}), ensure_ascii=False)}

请为主角、反派各生成1个详细角色设计，并额外创建1个NPC角色。
确保三个角色风格统一但各具特色。"""

        return self.run_json(prompt)
