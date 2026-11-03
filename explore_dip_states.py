#!/usr/bin/env python3
"""Count distinct `beratungsstand` and `vorgangstyp` values in the DIP API.

Purpose: derive the raw-status -> internal-state mapping from real data
instead of assumptions (see "Legislative State Model" in PROJECT_BRIEF.md).

Usage:
    export DIP_API_KEY=...        # public key from https://dip.bundestag.de/über-dip/hilfe/api
    python explore_dip_states.py --wahlperiode 21 --out dip_states.json
    python explore_dip_states.py --wahlperiode 21 --vorgangstyp Gesetzgebung

Notes:
- Standard library only, no dependencies.
- Parameter names (f.wahlperiode, f.vorgangstyp, cursor) and the auth header
  follow the DIP API documentation as I know it. Confirm them against
  https://search.dip.bundestag.de/api/v1/openapi.yaml before relying on results.
- Be polite: small delay between requests. Rate limits are not published.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

BASE_URL = "https://search.dip.bundestag.de/api/v1"


def fetch_page(api_key: str, params: dict) -> dict:
    url = f"{BASE_URL}/vorgang?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"ApiKey {api_key}",
            "Accept": "application/json",
            "User-Agent": "dip-state-explorer/0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--wahlperiode", type=int, default=21, help="legislative term (default: 21)")
    parser.add_argument("--vorgangstyp", default=None, help='optional filter, e.g. "Gesetzgebung"')
    parser.add_argument("--max-pages", type=int, default=200, help="safety limit on pagination")
    parser.add_argument("--delay", type=float, default=0.3, help="seconds between requests")
    parser.add_argument("--out", default=None, help="write full result as JSON to this path")
    args = parser.parse_args()

    api_key = os.environ.get("DIP_API_KEY")
    if not api_key:
        print("Set DIP_API_KEY (public key is listed on the DIP API help page).", file=sys.stderr)
        return 2

    params = {"format": "json", "f.wahlperiode": args.wahlperiode}
    if args.vorgangstyp:
        params["f.vorgangstyp"] = args.vorgangstyp

    by_status = Counter()
    by_type = Counter()
    by_pair = Counter()  # (vorgangstyp, beratungsstand)
    examples: dict[str, str] = {}
    total = 0
    last_cursor = None

    for page in range(1, args.max_pages + 1):
        try:
            data = fetch_page(api_key, params)
        except urllib.error.HTTPError as error:
            print(f"HTTP {error.code} on page {page}: {error.reason}", file=sys.stderr)
            return 1
        except urllib.error.URLError as error:
            print(f"Network error on page {page}: {error.reason}", file=sys.stderr)
            return 1

        documents = data.get("documents", [])
        if not documents:
            break

        for doc in documents:
            status = doc.get("beratungsstand") or "<none>"
            vtype = doc.get("vorgangstyp") or "<none>"
            by_status[status] += 1
            by_type[vtype] += 1
            by_pair[(vtype, status)] += 1
            examples.setdefault(status, doc.get("titel", ""))
            total += 1

        cursor = data.get("cursor")
        print(f"page {page}: {len(documents)} documents (total {total} of {data.get('numFound', '?')})", file=sys.stderr)
        if not cursor or cursor == last_cursor:
            break
        last_cursor = cursor
        params["cursor"] = cursor
        time.sleep(args.delay)

    print(f"\n{total} Vorgänge, Wahlperiode {args.wahlperiode}"
          + (f", Typ {args.vorgangstyp}" if args.vorgangstyp else ""))

    print("\n== vorgangstyp ==")
    for value, count in by_type.most_common():
        print(f"{count:6d}  {value}")

    print("\n== beratungsstand ==")
    for value, count in by_status.most_common():
        print(f"{count:6d}  {value}")

    if args.out:
        result = {
            "wahlperiode": args.wahlperiode,
            "vorgangstyp_filter": args.vorgangstyp,
            "total": total,
            "vorgangstyp": dict(by_type.most_common()),
            "beratungsstand": dict(by_status.most_common()),
            "beratungsstand_by_vorgangstyp": [
                {"vorgangstyp": t, "beratungsstand": s, "count": c}
                for (t, s), c in by_pair.most_common()
            ],
            "example_title_per_beratungsstand": examples,
        }
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
        print(f"\nFull result written to {args.out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
