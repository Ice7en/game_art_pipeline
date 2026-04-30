import os
import json
import time
from pathlib import Path
from agents import (
    WorldbuildingAgent,
    CodeAgent,
    CharacterAgent,
    PosterAgent,
    PublisherAgent,
)


class GameArtOrchestrator:
    """
    Main orchestrator for the Game + Art multi-agent pipeline.
    
    Pipeline flow:
    [Theme Keywords]
         ↓
    WorldbuildingAgent → game_concept.json
         ↓
    CharacterAgent    → character_designs.json
         ↓
    CodeAgent         → game.html
         ↓
    PosterAgent       → poster.html
         ↓
    PublisherAgent    → publish_kit.json
         ↓
    [Output Folder]
    """

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}
        self.log_callback = None  # Optional: set to receive progress logs

    def log(self, message: str, level: str = "info"):
        """Log a message."""
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level.upper()}] {message}"
        print(formatted)
        if self.log_callback:
            self.log_callback(message, level)

    def save_json(self, data: dict, filename: str) -> Path:
        """Save dict to JSON file."""
        path = self.output_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.log(f"Saved: {path}")
        return path

    def save_html(self, html: str, filename: str) -> Path:
        """Save HTML string to file."""
        path = self.output_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        self.log(f"Saved: {path}")
        return path

    def run(self, theme_keywords: str, skip_steps: list = None) -> dict:
        """
        Run the full pipeline.
        
        Args:
            theme_keywords: Theme keywords for the game (e.g. "赛博朋克 孤独 记忆")
            skip_steps: List of step names to skip (for testing)
        
        Returns:
            Dict with all generated content and file paths
        """
        skip_steps = skip_steps or []
        output = {}

        # ── Step 1: Worldbuilding ──────────────────────────────────────────
        self.log("🌍 Step 1/5 - WorldbuildingAgent: 生成游戏世界观...")
        if "worldbuilding" not in skip_steps:
            agent = WorldbuildingAgent()
            game_concept = agent.generate(theme_keywords)
            self.results["game_concept"] = game_concept
            output["game_concept_path"] = str(self.save_json(game_concept, "game_concept.json"))
            self.log(f"✅ 游戏《{game_concept.get('title', '未命名')}》世界观生成完毕")
        else:
            # Load existing if skipping
            with open(self.output_dir / "game_concept.json", encoding="utf-8") as f:
                self.results["game_concept"] = json.load(f)
            self.log("⏭️  跳过 Worldbuilding 步骤")

        game_concept = self.results["game_concept"]

        # ── Step 2: Character Design ───────────────────────────────────────
        self.log("🎨 Step 2/5 - CharacterAgent: 设计角色与AI绘图提示词...")
        if "character" not in skip_steps:
            agent = CharacterAgent()
            character_designs = agent.generate(game_concept)
            self.results["character_designs"] = character_designs
            output["character_designs_path"] = str(
                self.save_json(character_designs, "character_designs.json")
            )
            self.log(f"✅ {len(character_designs.get('characters', []))} 个角色设计完毕")
        else:
            with open(self.output_dir / "character_designs.json", encoding="utf-8") as f:
                self.results["character_designs"] = json.load(f)
            self.log("⏭️  跳过 Character 步骤")

        character_designs = self.results["character_designs"]

        # ── Step 3: Game Code ──────────────────────────────────────────────
        self.log("💻 Step 3/5 - CodeAgent: 生成HTML5游戏原型...")
        if "code" not in skip_steps:
            agent = CodeAgent()
            game_html = agent.generate(game_concept)
            self.results["game_html"] = game_html
            output["game_html_path"] = str(self.save_html(game_html, "game.html"))
            self.log("✅ 游戏原型代码生成完毕")
        else:
            self.log("⏭️  跳过 Code 步骤")

        # ── Step 4: Poster ─────────────────────────────────────────────────
        self.log("🖼️  Step 4/5 - PosterAgent: 制作游戏宣传海报...")
        if "poster" not in skip_steps:
            agent = PosterAgent()
            poster_html = agent.generate(game_concept, character_designs)
            self.results["poster_html"] = poster_html
            output["poster_html_path"] = str(self.save_html(poster_html, "poster.html"))
            self.log("✅ 宣传海报生成完毕")
        else:
            self.log("⏭️  跳过 Poster 步骤")

        # ── Step 5: Publishing Kit ─────────────────────────────────────────
        self.log("📦 Step 5/5 - PublisherAgent: 生成发行文案套件...")
        if "publisher" not in skip_steps:
            agent = PublisherAgent()
            publish_kit = agent.generate(game_concept)
            self.results["publish_kit"] = publish_kit
            output["publish_kit_path"] = str(self.save_json(publish_kit, "publish_kit.json"))
            self.log("✅ 发行文案套件生成完毕")
        else:
            self.log("⏭️  跳过 Publisher 步骤")

        # ── Generate Summary Report ────────────────────────────────────────
        self.log("📋 生成项目总结报告...")
        self._generate_summary_report(game_concept, character_designs, output)
        
        self.log("🎉 全部完成！输出目录：" + str(self.output_dir.resolve()))
        return output

    def _generate_summary_report(self, game_concept: dict, character_designs: dict, output: dict):
        """Generate a human-readable HTML summary report."""
        chars = character_designs.get("characters", [])
        char_rows = ""
        for c in chars:
            char_rows += f"""
            <tr>
                <td>{c.get('name', '')}</td>
                <td>{c.get('role', '')}</td>
                <td style="font-size:11px">{c.get('sd_prompt', '')[:80]}...</td>
            </tr>"""

        levels_html = ""
        for i, lv in enumerate(game_concept.get("levels", []), 1):
            levels_html += f"<li><strong>{lv.get('name', '')}</strong>: {lv.get('description', '')}</li>"

        html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>{game_concept.get('title', '')} - 项目报告</title>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #0d0d0d; color: #e0e0e0; }}
  h1 {{ color: #fff; border-bottom: 3px solid #6c63ff; padding-bottom: 10px; }}
  h2 {{ color: #6c63ff; margin-top: 30px; }}
  .badge {{ display: inline-block; background: #6c63ff; color: white; padding: 4px 12px; border-radius: 20px; font-size: 13px; margin: 4px; }}
  .card {{ background: #1a1a2e; border-radius: 12px; padding: 20px; margin: 15px 0; border: 1px solid #333; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ background: #6c63ff; color: white; padding: 10px; text-align: left; }}
  td {{ padding: 10px; border-bottom: 1px solid #333; }}
  .file-link {{ background: #16213e; padding: 8px 15px; border-radius: 8px; display: inline-block; margin: 5px; color: #6c63ff; text-decoration: none; }}
  ul {{ line-height: 1.8; }}
</style>
</head>
<body>
<h1>🎮 {game_concept.get('title', '未命名游戏')}</h1>
<p style="font-size:18px; color:#aaa; font-style:italic">{game_concept.get('tagline', '')}</p>

<div class="card">
  <strong>类型：</strong>{game_concept.get('genre', '')} &nbsp;|&nbsp;
  <strong>目标受众：</strong>{game_concept.get('target_audience', '')} &nbsp;|&nbsp;
  <strong>音乐风格：</strong>{game_concept.get('music_vibe', '')}
</div>

<h2>🌍 世界观</h2>
<div class="card">{game_concept.get('setting', '')}</div>

<h2>⚔️ 核心玩法</h2>
<div class="card">{game_concept.get('core_mechanic', '')}</div>

<h2>🎯 核心卖点</h2>
<div class="card">{game_concept.get('unique_selling_point', '')}</div>

<h2>🗺️ 关卡设计</h2>
<div class="card"><ul>{levels_html}</ul></div>

<h2>🎨 美术方向</h2>
<div class="card">
  <strong>风格：</strong>{game_concept.get('art_style', '')}<br><br>
  <strong>色彩方案：</strong><br>
  {"".join(f'<span class="badge" style="background:{c}">{c}</span>' for c in game_concept.get("color_palette", []))}
</div>

<h2>👥 角色设计</h2>
<div class="card">
<table>
  <tr><th>角色名</th><th>定位</th><th>SD提示词（预览）</th></tr>
  {char_rows}
</table>
</div>

<h2>📁 生成文件</h2>
<div class="card">
  <a class="file-link" href="game.html">🎮 游戏原型 game.html</a>
  <a class="file-link" href="poster.html">🖼️ 宣传海报 poster.html</a>
  <a class="file-link" href="game_concept.json">📄 游戏概念 game_concept.json</a>
  <a class="file-link" href="character_designs.json">🎨 角色设计 character_designs.json</a>
  <a class="file-link" href="publish_kit.json">📦 发行套件 publish_kit.json</a>
</div>
</body>
</html>"""

        report_path = self.output_dir / "report.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)
        self.log(f"Saved: {report_path}")
