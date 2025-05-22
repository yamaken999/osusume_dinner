import requests
import google.generativeai as genai

# APIキーとWebhook URLをセット
GEMINI_API_KEY = "AIzaSyAfabpB2r9Q3mVH9c7I0dJeRebzkRVEvb8"
TEAMS_WEBHOOK_URL = "https://accenture.webhook.office.com/webhookb2/60ad6b03-7f46-46a8-9d83-0d579a4eda48@e0793d39-0939-496d-b129-198edd916feb/IncomingWebhook/f25b751d00a8489ba32552f2c4b045f3/fe097da7-39f5-4835-9095-0a98f716f456/V28DCdRxnpz8ZEUc_9dJG36D2phu3S96Fbbd-0NC3yqT01"

# Gemini APIの設定
genai.configure(api_key=GEMINI_API_KEY)

# モデル呼び出し
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
response = model.generate_content("以下の要素からオススメされる食事を自炊する場合と、外食す場合でそれぞれ3つ挙げよ。- 今日が月の何営業日なのか（月の初めであれば元気、月末に向かうにつれて体が疲れている状態とする）。- 25日は給料日なので25日～月末までは少し豪華な提案をしてもよい。- 今日の気温と湿度（気温や湿度が高い場合はサッパリとしたもの、あっさりとしたものがよい）- 曜日（週の後半は元気が出るものがよい）")
fortune = response.text.strip()
print("生成された占い：", fortune)

# Teamsに投稿
payload = {"text": fortune}
r = requests.post(TEAMS_WEBHOOK_URL, json=payload)
if r.status_code == 200:
    print("✅ Teamsに投稿成功！")
else:
    print(f"❌ 投稿失敗: {r.status_code} {r.text}")
