# ベースイメージの指定
FROM python:3.9-slim

# 必要なシステムパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 必要なライブラリのインストール
RUN pip install --upgrade pip

# requirements.txt をコンテナにコピーし、依存関係をインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# gunicornをインストール
RUN pip install gunicorn

# アプリケーションのコードをコンテナにコピー
COPY . .

# blackで整形
RUN black .

# wait-for-it.shスクリプトをコンテナにコピー
COPY wait-for-it.sh /wait-for-it.sh

# コンテナの起動コマンド
# アプリケーションのエントリーポイントを指定
CMD ["/wait-for-it.sh", "db:5432", "--timeout=60", "--", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]