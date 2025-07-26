# FlightSearch

これはANAとJALのエラーフェアを監視するDjangoアプリのひな形です。以下の手順で環境を準備します。

```bash
# 仮想環境の作成と依存パッケージのインストール
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.env` ファイルに環境変数を設定してください。

主な環境変数例:
```
SECRET_KEY=django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost
DATABASE_URL=postgres://user:password@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=your-password
AMADEUS_CLIENT_ID=your-client-id
AMADEUS_CLIENT_SECRET=your-client-secret
```

Celery を起動するには次のコマンドを使用します。
```bash
celery -A flights_project worker -B --loglevel=info
```
