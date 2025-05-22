import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyAfabpB2r9Q3mVH9c7I0dJeRebzkRVEvb8"
genai.configure(api_key=GEMINI_API_KEY)

for m in genai.list_models():
    print(m.name)
