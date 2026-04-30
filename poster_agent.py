from .base_agent import BaseAgent
import json


POSTER_SYSTEM = """你是一名顶级游戏营销设计师，专门制作令人过目不忘的游戏宣传海报。
你精通HTML/CSS动画，能够创作视觉冲击力极强的数字海报。

你的任务是生成一个完整的HTML游戏宣传海报，要求：
1. 单文件HTML，包含所有样式和动画
2. 视觉震撼，有强烈的美术风格
3. 包含游戏标题、tagline、核心卖点
4. CSS动画效果（粒子、光效、过渡）
5. 响应式设计，适合1080x1920竖版海报尺寸
6. 使用Google Fonts获取特殊字体

只输出完整HTML代码，不要任何解释。代码必须以 <!DOCTYPE html> 开头。"""


class PosterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PosterAgent",
            system_prompt=POSTER_SYSTEM,
        )

    def generate(self, game_concept: dict, character_designs: dict) -> str:
        """Generate promotional poster HTML."""
        colors = game_concept.get("color_palette", ["#1a1a2e", "#16213e", "#0f3460", "#e94560"])

        prompt = f"""根据以下游戏信息，制作一张震撼的游戏宣传海报：

游戏名称：{game_concept.get('title', '')}
一句话介绍：{game_concept.get('tagline', '')}
游戏类型：{game_concept.get('genre', '')}
美术风格：{game_concept.get('art_style', '')}
核心卖点：{game_concept.get('unique_selling_point', '')}
目标受众：{game_concept.get('target_audience', '')}
色彩方案：{', '.join(colors)}
音乐风格：{game_concept.get('music_vibe', '')}

主角：{game_concept.get('protagonist', {}).get('name', '')} - {game_concept.get('protagonist', {}).get('description', '')}

设计要求：
- 主色调严格使用：{colors[0] if colors else '#1a1a2e'}
- 强调色：{colors[-1] if len(colors) > 1 else '#e94560'}
- 风格参考：{character_designs.get('art_direction', {}).get('overall_style', '')}
- 氛围关键词：{', '.join(character_designs.get('art_direction', {}).get('mood_board_keywords', []))}

请创作一个视觉冲击力极强的竖版游戏海报HTML，包含动态光效和精美排版。"""

        result = self.run(prompt)
        if "<!DOCTYPE html>" in result:
            start = result.index("<!DOCTYPE html>")
            end = result.rindex("</html>") + 7
            return result[start:end]
        return result
