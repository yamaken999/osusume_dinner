# 献立提案Webアプリ

## 必要要件
- Python 3.9以上
- Flask
- google-generativeai

## セットアップ
1. 必要なパッケージをインストール
   ```
   pip install -r requirements.txt
   ```
2. Google Gemini APIキーを環境変数に設定
   - Windowsの場合:
     ```
     set GEMINI_API_KEY=あなたのAPIキー
     ```
   - Linux/Macの場合:
     ```
     export GEMINI_API_KEY=あなたのAPIキー
     ```
3. アプリを起動
   ```
   python app.py
   ```
4. ブラウザで http://localhost:5000 にアクセス

## プロンプト編集
- prompt_template.txt を編集することで、AIへの指示内容を変更できます。 