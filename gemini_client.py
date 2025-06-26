import os
import datetime
import logging
from google.generativeai import GenerativeModel, configure

def get_japanese_holiday_and_event():
    # TODO: 祝日・行事判定ロジックを実装（現状はダミー）
    return "こどもの日"

def load_prompt_template():
    with open("prompt_template.txt", encoding="utf-8") as f:
        return f.read()

def get_menu_suggestions():
    try:
        now = datetime.datetime.now()
        weekday = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"][now.weekday()]
        holiday = get_japanese_holiday_and_event()
        prompt_template = load_prompt_template()
        prompt = prompt_template.format(
            date=now.strftime("%Y-%m-%d"),
            weekday=weekday,
            holiday=holiday
        )
        configure(api_key=os.environ["GEMINI_API_KEY"])
        model = GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API呼び出しエラー: {e}", exc_info=True)
        raise 