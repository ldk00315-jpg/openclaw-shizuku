from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flyer_template import create_flyer, create_template


def komagane_content() -> dict:
    return {
        "title": "駒ヶ根AI実践シェア会（仮）",
        "subtitle": "成果より、まず「やってみた」を持ち寄る会",
        "about_text": "AIに興味のある人が、いま試していること・うまくいったこと・つまずいていることを持ち寄って、互いに補い合う地域の勉強会です。\n初心者歓迎・途中経過歓迎・失敗共有歓迎。\n講師の一方通行ではなく、参加者同士の横のつながりを大切にします。",
        "schedule_steps": [
            "チェックイン（最近試したこと）",
            "ミニ共有（1人3〜5分）",
            "小グループで相談・情報交換",
            "次回までの小さな実験を決める",
        ],
        "goals": [
            "地域内でAI活用の相談相手をつくる",
            "一人で悩まず、実践を継続しやすくする",
            "小さな取り組みを積み上げる",
        ],
        "rules": [
            "売り込み中心にしない（紹介はOK）",
            "相手のレベルを否定しない",
            "機密情報・個人情報は持ち込まない",
            "安心して話せる雰囲気を守る",
        ],
        "organizer": "八木",
        "cooperation": "駒ヶ根商工会議所（予定）",
        "contact": "お問い合わせ：valuegarage@gmail.com",
        "date_location": "日時・場所：初回調整中（駒ヶ根市内予定）",
    }


def main():
    workspace = Path("/home/tomoyuki/.openclaw/workspace")
    template_path = workspace / "templates" / "flyer_a4_portrait.pptx"
    output_dir = workspace / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"komagane_ai_flyer_{ts}.pptx"

    create_template(template_path)
    create_flyer(komagane_content(), output_path)

    print(f"TEMPLATE={template_path}")
    print(f"OUTPUT={output_path}")


if __name__ == "__main__":
    main()
