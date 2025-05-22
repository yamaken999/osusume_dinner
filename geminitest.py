import google.generativeai as genai

# APIキー
GEMINI_API_KEY = "AIzaSyAfabpB2r9Q3mVH9c7I0dJeRebzkRVEvb8"  # あなたの本物のAPIキー

# 設定
genai.configure(api_key=GEMINI_API_KEY)

# モデル呼び出し（モデル名を正しく修正！）
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# コンテンツ生成
response = model.generate_content("今日の占いを短く面白く作ってください。絵文字も入れて！")

# 出力
print("Geminiからの返答：")
print(response.text.strip())
