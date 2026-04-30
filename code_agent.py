from .base_agent import BaseAgent


CODE_SYSTEM = """你是一名专业的HTML5游戏开发工程师，擅长用纯JavaScript/Canvas制作可玩的独立游戏原型。

你的任务是根据游戏概念文档，生成一个完整可运行的HTML5游戏原型。

要求：
1. 单文件HTML，包含所有CSS和JavaScript
2. 使用Canvas API实现游戏渲染
3. 包含：主菜单、游戏主体、游戏结束界面
4. 实现核心玩法机制（简化版）
5. 键盘/鼠标操控
6. 粒子效果和简单动画
7. 分数系统
8. 代码注释清晰，结构良好

输出格式：只输出完整的HTML代码，不要任何解释文字。
代码必须以 <!DOCTYPE html> 开头，以 </html> 结尾。"""


class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CodeAgent",
            system_prompt=CODE_SYSTEM,
        )

    def generate(self, game_concept: dict) -> str:
        """Generate HTML5 game code from game concept."""
        import json

        prompt = f"""根据以下游戏概念文档，生成完整的HTML5游戏原型代码：

{json.dumps(game_concept, ensure_ascii=False, indent=2)}

重点实现：
- 游戏标题：{game_concept.get('title', '未命名游戏')}
- 核心玩法：{game_concept.get('core_mechanic', '')}
- 美术风格：{game_concept.get('art_style', '')}
- 主色调：{', '.join(game_concept.get('color_palette', []))}

请生成完整可运行的HTML5游戏，包含美观的UI和流畅的游戏体验。"""

        result = self.run(prompt)
        # Extract HTML from response
        if "<!DOCTYPE html>" in result:
            start = result.index("<!DOCTYPE html>")
            end = result.rindex("</html>") + 7
            return result[start:end]
        return result
