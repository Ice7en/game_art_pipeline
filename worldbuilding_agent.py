from .base_agent import BaseAgent


WORLDBUILDING_SYSTEM = """你是一名资深独立游戏策划师，擅长创作引人入胜的游戏世界观。
你的任务是根据用户提供的主题关键词，生成完整的游戏概念文档。

输出必须是严格的JSON格式，包含以下字段：
{
  "title": "游戏名称（中英文）",
  "tagline": "一句话介绍",
  "genre": "游戏类型",
  "setting": "世界背景描述（200字以内）",
  "protagonist": {
    "name": "主角名字",
    "description": "主角描述",
    "abilities": ["能力1", "能力2", "能力3"]
  },
  "antagonist": {
    "name": "反派名字",
    "description": "反派描述"
  },
  "core_mechanic": "核心玩法机制描述",
  "levels": [
    {"name": "关卡名", "description": "关卡描述", "challenge": "主要挑战"}
  ],
  "art_style": "美术风格描述",
  "color_palette": ["主色1", "主色2", "主色3", "强调色"],
  "music_vibe": "音乐风格描述",
  "target_audience": "目标玩家群体",
  "unique_selling_point": "核心差异化卖点"
}

注意：levels 数组至少包含3个关卡。所有字段必须填写，不可为空。"""


class WorldbuildingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="WorldbuildingAgent",
            system_prompt=WORLDBUILDING_SYSTEM,
        )

    def generate(self, theme_keywords: str) -> dict:
        """Generate game concept from theme keywords."""
        prompt = f"""请根据以下主题关键词，设计一款独立游戏的完整世界观：

主题关键词：{theme_keywords}

请确保游戏概念新颖、有深度，美术风格独特，能够吸引独立游戏玩家。
输出完整的JSON文档。"""

        return self.run_json(prompt)
