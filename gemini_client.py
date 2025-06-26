import os
import datetime
import logging
import requests
from google.generativeai import GenerativeModel, configure

# 日本の祝日・行事リスト（例示、必要に応じて拡張可能）
JAPANESE_HOLIDAYS = {
    "01-01": "元日",
    "02-11": "建国記念の日",
    "02-23": "天皇誕生日",
    "03-03": "ひな祭り",
    "04-29": "昭和の日",
    "05-03": "憲法記念日",
    "05-04": "みどりの日",
    "05-05": "こどもの日",
    "07-07": "七夕",
    "07-17": "海の日（例年7月第3月曜、簡易化のため日付固定）",
    "08-11": "山の日",
    "09-15": "敬老の日（例年9月第3月曜、簡易化のため日付固定）",
    "09-23": "秋分の日（例年変動、簡易化のため日付固定）",
    "10-10": "体育の日（例年10月第2月曜、簡易化のため日付固定）",
    "11-03": "文化の日",
    "11-23": "勤労感謝の日",
    "12-23": "天皇誕生日（平成時代）",
}

JAPANESE_EVENTS = {
    # 1月
    "01-01": "元日",  # ※祝日だが年始扱いとして残すのが実用的
    "01-07": "七草の節句",
    "01-11": "鏡開き",
    "01-15": "小正月（どんど焼き）",

    # 2月
    "02-03": "節分",
    "02-14": "バレンタインデー",
    "02-19": "雨水（季節の変わり目の目安）",

    # 3月
    "03-03": "ひな祭り",
    "03-14": "ホワイトデー",
    "03-18": "彼岸入り（春）",  # 年によって前後

    # 4月
    "04-01": "エイプリルフール",
    "04-08": "花まつり（灌仏会）",
    "04-15": "入学・新生活シーズン（目安）",

    # 5月
    "05-01": "メーデー",
    "05-05": "端午の節句",  # 祝日と重複するが季節行事として有用
    "05-15": "葵祭（京都）",

    # 6月
    "06-01": "衣替え",
    "06-10": "時の記念日",
    "06-21": "夏至（年により変動）",

    # 7月
    "07-01": "海開き・山開き（目安）",
    "07-07": "七夕",
    "07-15": "お中元のピーク（関東）",

    # 8月
    "08-07": "立秋（目安）",
    "08-13": "お盆入り",
    "08-15": "お盆",
    "08-16": "お盆明け",

    # 9月
    "09-01": "防災の日",
    "09-09": "重陽の節句",
    "09-20": "彼岸入り（秋）",  # 年によって前後

    # 10月
    "10-01": "衣替え（秋）",
    "10-10": "目の愛護デー",
    "10-31": "ハロウィン",

    # 11月
    "11-07": "立冬（季節の節目）",
    "11-15": "七五三",
    "11-22": "いい夫婦の日",

    # 12月
    "12-13": "正月事始め",
    "12-21": "冬至（年によって変動）",
    "12-24": "クリスマスイブ",
    "12-25": "クリスマス",
    "12-31": "大晦日"
}

# 天気情報取得
def get_weather_info():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY", "Tokyo,jp")
    if not api_key:
        return "天気情報取得失敗（APIキー未設定）"
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={api_key}&units=metric&lang=ja"
    )
    try:
        weather_data = requests.get(url, timeout=5).json()
        if "main" in weather_data:
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            desc = weather_data["weather"][0]["description"]
            return f"天気: {desc}、気温: {temp}℃、湿度: {humidity}%"
        else:
            return f"天気情報取得失敗: {weather_data.get('message', '不明なエラー')}"
    except Exception as e:
        logging.error(f"天気情報取得エラー: {e}", exc_info=True)
        return "天気情報取得失敗"

def get_japanese_holiday_and_event():
    today = datetime.datetime.now()
    md = today.strftime("%m-%d")
    holidays = []
    if md in JAPANESE_HOLIDAYS:
        holidays.append(JAPANESE_HOLIDAYS[md])
    if md in JAPANESE_EVENTS:
        holidays.append(JAPANESE_EVENTS[md])
    if holidays:
        return "・".join(holidays)
    else:
        return "特になし"

def load_prompt_template():
    with open("prompt_template.txt", encoding="utf-8") as f:
        return f.read()

def get_menu_suggestions():
    try:
        now = datetime.datetime.now()
        weekday = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"][now.weekday()]
        holiday = get_japanese_holiday_and_event()
        weather = get_weather_info()
        prompt_template = load_prompt_template()
        prompt = prompt_template.format(
            date=now.strftime("%Y-%m-%d"),
            weekday=weekday,
            holiday=holiday,
            weather=weather
        )
        configure(api_key=os.environ["GEMINI_API_KEY"])
        model = GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API呼び出しエラー: {e}", exc_info=True)
        raise 