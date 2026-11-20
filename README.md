# One image summing up 20 November 2026's world news

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Putra-122/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Putra-122/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A newspaper front page that sums up Friday 20 November 2026 in one
1024x1024 image: GTA VI smashing every sales record, a Houthi strike on
Riyadh's tallest tower, the World Court finding Myanmar guilty of genocide
against the Rohingya, and Asian markets tumbling — plus a ticker of the
day's other big stories.

Built for the [make.fun news-image-20261120 bounty](https://make.fun/bounty/news-image-20261120).

## How it works

`main.py` (Python 3.13, stdlib + PIL only, no network) composes the page
from the four text-free panels in `assets/` and renders every word with
PIL fonts, so nothing on the page can be garbled. It writes `entry.png`
(1024x1024 JPEG, under 1 MiB) to `$MAKEFUN_OUTPUT_DIR/entry.png` and to
this directory. Run it twice and the bytes are identical.

```
python3 main.py
```
