import logging
from flask import Flask, render_template
from gemini_client import get_menu_suggestions
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    try:
        suggestions = get_menu_suggestions()
        return render_template("index.html", suggestions=suggestions)
    except Exception as e:
        app.logger.error(f"Error: {e}", exc_info=True)
        return render_template("index.html", suggestions=f"エラーが発生しました: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 