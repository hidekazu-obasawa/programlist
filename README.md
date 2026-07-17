# サイト変化通知プログラム

指定したWebサイトを取得し、前回保存した内容と比べて変化があれば通知します。
Python標準機能だけで動くので、追加インストールは不要です。

## すぐ試す

```powershell
py .\site_watcher.py --url https://example.com
```

初回は比較用データを保存します。2回目以降に内容が変わると差分が表示されます。

## 5分ごとに監視する

```powershell
py .\site_watcher.py --url https://example.com --interval 300
```

## 複数サイトを監視する

`sites.example.json`をコピーしてURLを書き換えます。

```powershell
py .\site_watcher.py --config .\sites.example.json --interval 300
```

## 特定部分だけ監視する

設定ファイルの`pattern`に正規表現を書きます。

```json
{
  "name": "ニュース欄",
  "url": "https://example.com/news",
  "pattern": "<main.*?</main>"
}
```

## Webhook通知

SlackやDiscordなどのWebhook URLを指定できます。

```powershell
py .\site_watcher.py --url https://example.com --webhook-url "https://example.com/webhook"
```

## メール通知

メール通知は環境変数を設定してから`--email`を付けます。

```powershell
$env:SMTP_HOST="smtp.example.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="your-account@example.com"
$env:SMTP_PASSWORD="your-password"
$env:MAIL_TO="to@example.com"
py .\site_watcher.py --url https://example.com --email
```

`py`が使えない場合は、Pythonをインストールするか、環境にあるPython実行ファイルのパスに置き換えてください。

## 保存されるもの

比較用データは既定で`.site_watcher_state`フォルダに保存されます。
保存先を変えたい場合は`--state-dir`を指定してください。
