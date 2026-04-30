#!/usr/bin/env python3
"""
Game + Art Multi-Agent Pipeline - CLI Entry Point
Usage: python main.py --theme "赛博朋克 孤独 记忆"
"""

import argparse
import sys
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="🎮 Game + Art Multi-Agent Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --theme "赛博朋克 孤独 记忆"
  python main.py --theme "古风武侠 羁绊 复仇" --output my_game
  python main.py --theme "海洋探索 神秘 生存" --skip code poster
        """
    )
    parser.add_argument(
        "--theme",
        type=str,
        required=True,
        help="游戏主题关键词，用空格分隔（如：'赛博朋克 孤独 记忆'）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="输出目录名（默认：output）"
    )
    parser.add_argument(
        "--skip",
        nargs="*",
        choices=["worldbuilding", "character", "code", "poster", "publisher"],
        default=[],
        help="跳过指定步骤（用于测试或断点续传）"
    )

    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ 错误: 请设置环境变量 ANTHROPIC_API_KEY")
        print("   export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    print("=" * 60)
    print("🎮  Game + Art Multi-Agent Pipeline")
    print("=" * 60)
    print(f"📌 主题关键词: {args.theme}")
    print(f"📁 输出目录: {args.output}")
    if args.skip:
        print(f"⏭️  跳过步骤: {', '.join(args.skip)}")
    print("=" * 60)
    print()

    # Import and run orchestrator
    sys.path.insert(0, str(Path(__file__).parent))
    from orchestrator import GameArtOrchestrator

    orchestrator = GameArtOrchestrator(output_dir=args.output)
    
    try:
        result = orchestrator.run(
            theme_keywords=args.theme,
            skip_steps=args.skip
        )
        
        print()
        print("=" * 60)
        print("✅ Pipeline 完成！")
        print("=" * 60)
        print()
        print("生成文件：")
        for key, path in result.items():
            print(f"  📄 {key}: {path}")
        print()
        print(f"💡 打开报告: open {args.output}/report.html")
        print(f"🎮 试玩游戏: open {args.output}/game.html")
        print(f"🖼️  查看海报: open {args.output}/poster.html")
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
