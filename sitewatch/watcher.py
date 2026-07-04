"""
Проверяет список URL на изменения и шлёт уведомление в Discord через webhook,
когда содержимое страницы поменялось с прошлой проверки.

Использование:
    python -m sitewatch.watcher --urls sites.txt --webhook $DISCORD_WEBHOOK_URL
    python -m sitewatch.watcher --urls sites.txt --webhook $DISCORD_WEBHOOK_URL --interval 300 --loop
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import requests

from sitewatch.diffing import content_hash
from sitewatch.storage import HashStore

USER_AGENT = "site-watch/1.0 (+https://github.com/FreeSX-dev/site-watch)"


def fetch(url: str, timeout: float = 15.0) -> str:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()
    return response.text


def notify_discord(webhook_url: str, message: str) -> None:
    requests.post(webhook_url, json={"content": message}, timeout=10.0)


def check_once(urls: list[str], store: HashStore, webhook_url: str | None) -> list[str]:
    changed: list[str] = []
    for url in urls:
        try:
            html = fetch(url)
        except requests.RequestException as exc:
            print(f"[skip] {url}: {exc}")
            continue

        new_hash = content_hash(html)
        old_hash = store.get(url)

        if old_hash is None:
            print(f"[init] {url}: запомнил текущее состояние")
        elif old_hash != new_hash:
            print(f"[changed] {url}")
            changed.append(url)
            if webhook_url:
                notify_discord(webhook_url, f"Страница изменилась: {url}")

        store.set(url, new_hash)
    return changed


def read_urls(path: str) -> list[str]:
    lines = Path(path).read_text().splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def main() -> None:
    parser = argparse.ArgumentParser(description="Следит за изменениями на веб-страницах.")
    parser.add_argument("--urls", required=True, help="Файл со списком URL, по одному на строку")
    parser.add_argument("--webhook", default=None, help="Discord webhook URL для уведомлений")
    parser.add_argument("--store", default="hashes.json", help="Файл для хранения хэшей страниц")
    parser.add_argument("--interval", type=int, default=300, help="Интервал между проверками, сек")
    parser.add_argument("--loop", action="store_true", help="Проверять непрерывно вместо одного прогона")
    args = parser.parse_args()

    urls = read_urls(args.urls)
    store = HashStore(args.store)

    if not args.loop:
        check_once(urls, store, args.webhook)
        return

    print(f"Слежу за {len(urls)} страницами, проверка каждые {args.interval} сек. Ctrl+C для выхода.")
    while True:
        check_once(urls, store, args.webhook)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
