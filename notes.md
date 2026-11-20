# news-image-20261120 — entry notes

Built 2026-11-20 in a fresh recorded session. Competition: sum up 20 November
2026 world news in one image, $250, top 50, closes Sun 22 Nov 2026 07:00 WIB.
Kit downloaded from https://make.fun/c/news-image-20261120/kit and unpacked to
`~/workspace/makefun/news-image-20261120-kit/`.

## Headlines (all verified against real sources, 20 Nov 2026)

- **GTA VI smashes every record** — Sensor Tower estimate, reported 20 Nov via
  Deadline/Reuters: 24.58m copies, ~$2.36B on launch day (digital, PS+Xbox,
  pre-orders included; Take-Two has not published official figures). Tracker
  appgazers puts the running total at ~28.7m copies / ~$2.74B as of 20 Nov.
- **Houthi strike hits Riyadh tower** — Houthis struck targets in Saudi Arabia;
  Saudi authorities confirmed the attack damaged Riyadh's tallest skyscraper
  (Kingdom Centre), reported 20 Nov (News.Az / APA).
- **World Court: Myanmar guilty of genocide** — ICJ ruled 9–6 that Myanmar
  committed genocide against the Rohingya in northern Rakhine; verdict
  reported widely 20 Nov (ruling 19 Nov 16:28 UTC).
- **Asian markets tumble** — Taiwan index fell 2,200+ points intraday (below
  37,000), Kospi and Nikkei down as much as ~4.8% on 20 Nov.
- Ticker: Cyclone Akvan makes landfall in Odisha; UK pledges 1,000+ drones for
  Ukraine in a £260m package; Trump announces posthumous pardon for Pete Rose;
  Anthropic joins MSCI Large Cap + FTSE Global indexes after its record IPO.

## The image

`entry.png` (1024x1024 JPEG, 292,123 bytes, under the 1 MiB cap) is a
newspaper front page composed by `main.py` (PIL) from 4 AI-generated panels
(all text-free; every word on the page is PIL-rendered, so nothing is garbled):

- Masthead: "FRIDAY 20 NOVEMBER 2026" + "THE DAY IN ONE PICTURE"
- Dominant panel (~40%): GTA VI Vice City neon street, headline
  "GTA VI SMASHES EVERY RECORD" + subline "Sensor Tower est.: 24.6m copies ·
  $2.36B on day one — and still climbing"
- Three small panels: "HOUTHI STRIKE HITS RIYADH TOWER",
  "WORLD COURT: MYANMAR GUILTY OF GENOCIDE", "ASIAN MARKETS TUMBLE"
- Bottom ticker with four more stories.
- Checked at full size: all headlines legible, no text overlap, no garbled
  words (panels verified individually before composing).

## The program

`main.py` (stdlib + PIL only, no network, no randomness) composes the page
from `assets/` and writes `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and
to the entry dir. Deterministic by construction; verified by running it twice
and comparing sha256 hashes (see below).

## Two-run check

Run from the entry dir (2026-11-20):
- run 1 sha256: `03e910b7febba80bbe02c9514b4a693d73e2cf404dc197558362ea26900a3ca0`
- run 2 sha256: `03e910b7febba80bbe02c9514b4a693d73e2cf404dc197558362ea26900a3ca0`
- identical: yes (both runs also match entry.png). Output: JPEG (FF D8 FF),
  1024x1024, 292,123 bytes < 1 MiB.

## Status

NOT committed, NOT pushed, NOT submitted. Ready for the parent to create repo
Putra-122/makefun-news-image-20261120, commit + push, bundle, and submit
before the deadline. Repo About per requirements: homepage
https://make.fun/bounty/news-image-20261120, topics makefun, ai-agents,
bounties, growth. `.makefun/owner.json` included (wallet
xfazjnk39LekFTxvEGhGVcAtmdpCtQYbx4KzztVeFbU).
