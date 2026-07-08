#!/usr/bin/env python3
r"""
Googleの更新を監視し、変化があればメールで通知する一体型プログラム。

使い方:
  1. 下の「設定」欄を書き換える
  2. PowerShellで outputs フォルダへ移動する
  3. py .\google_change_mail_watcher.py を実行する
"""

from __future__ import annotations

import difflib
import email.message
import hashlib
import re
import smtplib
import time
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


# =========================
# 設定
# =========================

WATCH_URL = "https://www.google.com/"
WATCH_NAME = "Google"
CHECK_INTERVAL_SECONDS = 300

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "basawaworks@gmail.com"
SMTP_PASSWORD = "gfmf qaks cwnw efaw"
MAIL_FROM = SMTP_USER
MAIL_TO = "basawaworks@gmail.com"

STATE_DIR = Path(".google_change_mail_watcher_state")
DIFF_LINE_LIMIT = 80
TIMEOUT_SECONDS = 20


# =========================
# プログラム本体
# =========================

USER_AGENT = "google-change-mail-watcher/1.0"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.parts.append(text)

    def text(self) -> str:
        return "\n".join(self.parts)


def state_file() -> Path:
    key = hashlib.sha256(WATCH_URL.encode("utf-8")).hexdigest()[:16]
    return STATE_DIR / f"{key}.txt"


def fetch_page() -> tuple[str, str]:
    request = urllib.request.Request(WATCH_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        content_type = response.headers.get("Content-Type", "")
        body = response.read()

    charset = "utf-8"
    match = re.search(r"charset=([\w.-]+)", content_type, re.I)
    if match:
        charset = match.group(1)

    return content_type, body.decode(charset, errors="replace")


def normalize_page(content_type: str, body: str) -> str:
    target = body
    if "html" in content_type.lower() or "<html" in body.lower():
        parser = TextExtractor()
        parser.feed(body)
        target = parser.text()

    lines = [" ".join(line.split()) for line in target.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def read_previous() -> str | None:
    path = state_file()
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def save_current(content: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file().write_text(content, encoding="utf-8")


def make_diff(previous: str, current: str) -> str:
    diff_lines = list(
        difflib.unified_diff(
            previous.splitlines(),
            current.splitlines(),
            fromfile="前回",
            tofile="今回",
            lineterm="",
        )
    )
    if len(diff_lines) > DIFF_LINE_LIMIT:
        omitted = len(diff_lines) - DIFF_LINE_LIMIT
        diff_lines = diff_lines[:DIFF_LINE_LIMIT] + [f"... 省略: 残り{omitted}行"]
    return "\n".join(diff_lines)


def send_mail(diff: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = email.message.EmailMessage()
    message["Subject"] = f"サイト変更通知: {WATCH_NAME}"
    message["From"] = MAIL_FROM
    message["To"] = MAIL_TO
    message.set_content(
        f"{WATCH_NAME} の変化を検知しました。\n"
        f"日時: {now}\n"
        f"URL: {WATCH_URL}\n\n"
        f"{diff}"
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(message)


def check_once() -> None:
    content_type, body = fetch_page()
    current = normalize_page(content_type, body)
    previous = read_previous()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if previous is None:
        save_current(current)
        print(f"[{now}] 初回保存しました: {WATCH_NAME}")
        return

    if current == previous:
        print(f"[{now}] 変化なし: {WATCH_NAME}")
        return

    diff = make_diff(previous, current)
    send_mail(diff)
    save_current(current)
    print(f"[{now}] 変更を検知し、メールを送信しました: {WATCH_NAME}")


def validate_settings() -> None:
    placeholders = [
        SMTP_USER == "your-email@gmail.com",
        SMTP_PASSWORD == "your-app-password",
        MAIL_TO == "notify-to@example.com",
    ]
    if any(placeholders):
        raise SystemExit(
            "メール設定が未入力です。ファイル上部の SMTP_USER、SMTP_PASSWORD、MAIL_TO を書き換えてください。"
        )


def main() -> None:
    validate_settings()
    print(f"監視を開始します: {WATCH_NAME} ({WATCH_URL})")
    print(f"確認間隔: {CHECK_INTERVAL_SECONDS}秒 / 停止: Ctrl + C")

    while True:
        try:
            check_once()
        except KeyboardInterrupt:
            print("\n監視を停止しました。")
            return
        except Exception as exc:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] エラー: {exc}")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
