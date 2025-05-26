import os
import requests
from dotenv import load_dotenv

# .envファイルからAPIキーなどを読み込み
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Tokyo,jp")

weather_url = (
    f"https://api.openweathermap.org/data/2.5/weather?q={CITY}"
    f"&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
)
weather_data = requests.get(weather_url).json()

print("APIレスポンス内容:", weather_data)

if "main" in weather_data:
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    weather_desc = weather_data["weather"][0]["description"]
    print(f"都市: {CITY}")
    print(f"天気: {weather_desc}")
    print(f"気温: {temperature} ℃")
    print(f"湿度: {humidity} %")
else:
    print("天気情報の取得に失敗しました。")
    print("エラーメッセージ:", weather_data.get("message", "不明なエラー"))
