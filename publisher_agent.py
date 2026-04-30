from .base_agent import BaseAgent
import json


PUBLISHER_SYSTEM = """你是一名资深游戏发行商和文案专家，专门撰写Steam/TapTap等平台的游戏页面文案。
你深知如何用文字打动玩家，提升转化率。

输出必须是严格的JSON格式：
{
  "steam_page": {
    "short_description": "Steam简短描述（375字符以内）",
    "long_description": "Steam详细描述（Markdown格式，800-1200字）",
    "tags": ["标签1", "标签2", "标签3", "标签4", "标签5"],
    "features": ["特色功能1", "特色功能2", "特色功能3", "特色功能4", "特色功能5"],
    "system_requirements": {
      "minimum": {"os": "Windows 10", "cpu": "...", "memory": "...", "storage": "..."},
      "recommended": {"os": "Windows 11", "cpu": "...", "memory": "...", "storage": "..."}
    }
  },
  "taptap_page": {
    "intro": "TapTap简介（200字以内，吸引手游玩家）",
    "highlights": ["亮点1", "亮点2", "亮点3"]
  },
  "press_kit": {
    "press_release": "新闻稿（300字，英文）",
    "key_facts": ["事实1", "事实2", "事实3"],
    "contact_email": "press@yourstudio.com"
  },
  "social_media": {
    "twitter_post": "Twitter发布推文（280字符，英文）",
    "weibo_post": "微博发布内容（140字，中文，含话题标签）",
    "discord_announcement": "Discord公告（英文，含emoji）"
  }
}"""


class PublisherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PublisherAgent",
            system_prompt=PUBLISHER_SYSTEM,
        )

    def generate(self, game_concept: dict) -> dict:
        """Generate all publishing materials."""
        prompt = f"""根据以下游戏信息，生成完整的发行文案套件：

{json.dumps(game_concept, ensure_ascii=False, indent=2)}

请确保文案：
1. 突出核心卖点：{game_concept.get('unique_selling_point', '')}
2. 针对目标群体：{game_concept.get('target_audience', '')}
3. 风格与游戏氛围一致
4. 激发玩家购买欲望"""

        return self.run_json(prompt)
