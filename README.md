# FlightSearch

Streamlit を使った JAL 国際線 LSP 検索ツールです。最安日検索や複数クラス検索、CSV 出力に対応しています。

## セットアップ
1. Python 3.8 以上を用意します。
2. 依存ライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
3. Amadeus の API キーを環境変数に設定します。
   ```bash
   export AMADEUS_API_KEY=あなたのキー
   export AMADEUS_API_SECRET=あなたのシークレット
   ```

## 実行方法
```bash
streamlit run app.py
```
ブラウザが開くので、フォームに入力して検索します。結果はテーブルで表示され、CSV ダウンロードもできます。

## テスト (任意)
pytest をインストール済みの場合は次のコマンドでテストできます。
```bash
pytest
```
