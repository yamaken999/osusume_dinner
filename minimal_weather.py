import os
from dotenv import load_dotenv

load_dotenv()  # ここが重要！

print("OPENWEATHER_API_KEY:", os.getenv("OPENWEATHER_API_KEY"))
