import os
from dotenv import load_dotenv
import requests
import google.generativeai as genai
from datetime import datetime

# .envを読み込む
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Tokyo,jp")

# 天気情報の取得
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
weather_data = requests.get(weather_url).json()
print(weather_data)  # デバッグ表示

if "main" in weather_data and "weather" in weather_data:
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    weather_desc = weather_data["weather"][0]["description"]
else:
    weather_desc = weather_data.get("message", "天気情報が取得できませんでした")
    temperature = "-"
    humidity = "-"

# 日付・曜日
today = datetime.now()
weekday = ["月", "火", "水", "木", "金", "土", "日"][today.weekday()]

# プロンプト
prompt = f"""
今日の日付は{today.year}年{today.month}月{today.day}日です。
天気は「{weather_desc}」、気温は{temperature}度、湿度は{humidity}%です。

以下の条件を考慮し、バラエティに富み、毎日違う楽しさや新鮮味がある、今日の夕食プランを提案してください。
・曜日による変化（月曜日はリセット、金曜日はご褒美、週末は特別感など）
・月の初め、中旬、月末で体調や気分が変わること（例：月末は疲れがち、給料日後はちょっと豪華に）
・季節感や旬の食材を意識すること
・最近の日本や世界のイベントや記念日を意識すること（例：祝日、行事、話題のグルメ、トレンド）
・ジャンルが偏らないよう、複数のジャンルで提案すること
・昨日・直近と同じような料理や食材になりすぎないように（マンネリ化防止）
・たまには珍しい料理や話題の料理、季節の限定メニューなども取り入れること
・バランスの良い栄養や、疲れている場合は体調ケアできる要素も考慮すること
・自炊と外食、それぞれ3つずつ具体的なメニューを挙げてください
・各メニューには、理由や一言コメントを添えてください

仕事が終わったあとも、ちょっと楽しみになるような提案を、ユーモアも交えてお願いします。
"""

# Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
response = model.generate_content(prompt)
result = response.text.strip()

# Teams投稿
payload = {"text": result}
if TEAMS_WEBHOOK_URL:
    r = requests.post(TEAMS_WEBHOOK_URL, json=payload)
    if r.status_code == 200:
        print("✅ Teamsに投稿成功！")
    else:
        print(f"❌ 投稿失敗: {r.status_code} {r.text}")
else:
    print("⚠️ Teams Webhook URLが設定されていません。以下が生成結果です：\n")
    print(result)
