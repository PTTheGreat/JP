#!/usr/bin/env python3
"""AI引用監測台(内部ツール・スキャフォールド)。

queries.json の固定クエリ集を主要AI(ChatGPT / Perplexity / Gemini)に投げ、
回答に自サイトのドメインが引用されたかを記録する。

結果は results/YYYY-MM-DD.jsonl に1クエリ1行で追記される:
  {"date", "provider", "query", "cited", "cited_url", "cited_snippet", "raw_answer"}

各プロバイダのAPIキーは環境変数で渡す:
  OPENAI_API_KEY / PERPLEXITY_API_KEY / GEMINI_API_KEY

キー未設定のプロバイダはスキップされる(dry-runで動作確認可能)。
実行: python3 monitor/monitor.py
"""

import json
import os
import re
import datetime
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
CFG = json.loads((HERE / "queries.json").read_text(encoding="utf-8"))
RESULTS = HERE / "results"


def http_json(url, payload, headers):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def ask_chatgpt(query):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    data = http_json(
        "https://api.openai.com/v1/chat/completions",
        {"model": "gpt-4o-search-preview",
         "web_search_options": {},
         "messages": [{"role": "user", "content": query}]},
        {"Authorization": f"Bearer {key}"})
    return data["choices"][0]["message"]["content"]


def ask_perplexity(query):
    key = os.environ.get("PERPLEXITY_API_KEY")
    if not key:
        return None
    data = http_json(
        "https://api.perplexity.ai/chat/completions",
        {"model": "sonar", "messages": [{"role": "user", "content": query}]},
        {"Authorization": f"Bearer {key}"})
    msg = data["choices"][0]["message"]["content"]
    cites = data.get("citations", [])
    return msg + "\n\ncitations: " + json.dumps(cites, ensure_ascii=False)


def ask_gemini(query):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    data = http_json(
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={key}",
        {"contents": [{"parts": [{"text": query}]}],
         "tools": [{"google_search": {}}]},
        {})
    parts = data["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts)


PROVIDERS = {"chatgpt": ask_chatgpt, "perplexity": ask_perplexity, "gemini": ask_gemini}


def check_citation(answer):
    """回答文中に自サイトのドメインが含まれるか判定する。"""
    for domain in CFG["site_domains"]:
        m = re.search(re.escape(domain), answer)
        if m:
            start = max(0, m.start() - 100)
            return True, domain, answer[start:m.end() + 100]
    return False, None, None


def main():
    RESULTS.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    out = RESULTS / f"{today}.jsonl"
    n_ok, n_cited = 0, 0
    with out.open("a", encoding="utf-8") as f:
        for provider in CFG["providers"]:
            ask = PROVIDERS[provider]
            for query in CFG["queries"]:
                try:
                    answer = ask(query)
                except Exception as e:
                    answer = None
                    print(f"[{provider}] error on {query!r}: {e}")
                if answer is None:
                    continue
                cited, url, snippet = check_citation(answer)
                n_ok += 1
                n_cited += cited
                f.write(json.dumps({
                    "date": today, "provider": provider, "query": query,
                    "cited": cited, "cited_url": url,
                    "cited_snippet": snippet, "raw_answer": answer,
                }, ensure_ascii=False) + "\n")
    if n_ok:
        print(f"done: {n_ok} answers, cited {n_cited} ({n_cited / n_ok:.0%}) -> {out}")
    else:
        print("no provider keys set — nothing queried. "
              "Set OPENAI_API_KEY / PERPLEXITY_API_KEY / GEMINI_API_KEY.")


if __name__ == "__main__":
    main()
