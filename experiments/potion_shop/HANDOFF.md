# Potion Shop: handoff (state 2026-10-26 12:45)

Read this first when continuing the Potion Shop work, then `NOTES.md`
(history, findings) in this directory.

## Where everything is

| What | Where |
|------|-------|
| This handoff + notes | `experiments/potion_shop/HANDOFF.md`, `NOTES.md` (repo, branch `potion-shop`) |
| Dev branch (all Potion Shop code) | `potion-shop` (pushed to origin), last commit 52d2bda |
| LG branch | `potion-shop-lg` = `potion-shop` + uiScaling (PR #25), last merge 6497faf |
| Xiaomi bot (dad's phone, e0cb42c1, 1080x2400) | main dir `/home/vondr/programs/auto-eatventure/auto-eatventure` |
| LG bot (Jenik's LG G6, LGH87084afac10, 1440x2880) | `/home/vondr/programs/auto-eatventure/auto-eatventurelg` (detached checkout of `origin/potion-shop-lg`), `.venv/bin/python` |
| LG watchdog | `auto-eatventurelg/watchdog/lg_watchdog.sh` (restarts the bot within ~60 s, pauses below 30 % battery, resumes at 70 %: the user's choice, don't change) |
| All dev tools, test screenshots, pylint | `/home/vondr/programs/auto-eatventure/potion-shop-dev/scratchpad/` (copy of the old session scratchpad, paths already rewritten); called `$S` below |

## State when stopped (2026-10-26 ~12:45)

- The user stopped the event work: "the bot drives around and doesn't
  work much". The LG bot was switched to normal restaurants
  (`POTION_SHOP_ENABLED="0"` in `auto-eatventurelg/.env`) after the
  bot left the event by hand (`potion_shop.leave()`).
- The Xiaomi had finished the event 15/15 before (2026-10-25) and plays
  normal cities.
- LG event: Cauldron fine (LG potions max out at level 6; all kept
  potions MAX, "Brewing done, buying customers" reached), customers
  bought. The weak part is the station upgrades (below).

## What works

- Entering/leaving, crates, Upgrades dialog, Cauldron (brewing plan,
  `CauldronWatch` every 5 min, brewing past the plan, done without a
  free slot), bottling orders (Xiaomi), shop/cellar views by landmarks,
  scroll-aware station arrows (`station_place()`).
- Station popup reading (`vision/station_popup.py`): profit, time,
  price by character samples in `matching_screenshots/station_popup_chars/`;
  blue and grey (unaffordable, red price) buttons; columns covered by
  the event's edge buttons are detected and such numbers not read.

## What does not work well (why the user stopped it)

1. **Station focus (`StationFocus` in `potion_shop_loop.py`)** -
   focus = max profit/price of the station popups. In practice:
   - The focus thrashes between stations: each upgrade buys many
     levels (long press) and drops its ratio, so the survey re-reads
     and switches focus every minute, with many shop<->cellar scrolls.
   - Popups are often unreadable: the Bat's profit is always covered by
     the "1485" chest (left), the Dragon's right part by the "1d 11h"
     chest, the Spider's (cellar) top by the round button at the top
     of the screen; alchemists walk over popups.
   - Every new suffix letter needs a sample: "an" was added at 12:37,
     "ao", "ap", ... will be missing. Unreadable popups are saved to
     `logs/station_popup_<station>.png` (cut the sample from there:
     `$S/tools/popsamples.py <img> <profit|-> <time|-> <price>`).
   - Survey taps (open popup, read, close) cost ~5 s per station.
2. The user's idea of the strategy: upgrade the station that gives the
   most (they expected Bat, then Dragon Scale); "Neni upgrade jako
   upgrade" = compare the real profit gained per coin, not the last
   "profit x2" row.

## Ideas for next time

- Read the popups less often and buy fewer levels per focus (short
  taps instead of the long press), or compute the focus once per
  survey and stick to it until the next survey (no re-read after each
  upgrade), to stop the thrash and the scrolling.
- Read covered popups at another scroll position (move the map so the
  station is mid-screen) instead of failing.
- Generate letter samples for all of a-z at once (from the game's font
  or by collecting them over a run) instead of one per new suffix.
- Maybe consider the time (profit per second per coin); customers are
  probably the bottleneck, so profit/price was used.
- Separate strategies: the fastest one vs Jenik's account (fewer
  upgrades, potions max at 6).

## Tools (`$S` = `/home/vondr/programs/auto-eatventure/potion-shop-dev/scratchpad`)

Run from the worktree root with `PYTHONPATH=src` (LG dir: its
`.venv/bin/python`; main dir: `.venv/bin/python`).

- Lint: `PYTHONPATH=src:$S/pylib $S/pylib/bin/pylint src/auto_eatventure`
  (10/10 required; 2-space indent, 79 chars, max-locals 15).
- Regression checks: `timeout 600 bash $S/refactor/check.sh <tag>`,
  then compare `$S/refactor/{regress,regress2,lvl,units}_<tag>.txt`
  with the last tag (`grey`; regress differs from `base` on purpose).
- Station popups: `$S/tools/rp.py <png>...` (read_popup),
  `popread.py` (raw texts), `popdbg.py` (per character: best samples
  and differences), `cover.py` (covered columns), `popsamples.py` (cut
  samples), `readlive.py <cellar|shop> <station>...` (live on the LG:
  scroll, open, save `$S/pop/live_<station>.png`, read; pause the bot
  first).
- Test screenshots: `$S/pop/` (LG popups incl. grey button
  `popup_water_*`, covered `bat.png`, `dragon.png`, `popup_spider_*`),
  `$S/lg/` (LG views: shop, cellar, Cauldron, brew lists).
- `$S/tools/arrows_lg.py <png>` (map offset + each station's arrow),
  `icons_lg.py`, `lgwatch.sh` (anomaly watcher of the LG log).

## Operating the LG bot

- Pause: `kill -STOP <pid>` / resume `kill -CONT` (the watchdog
  restarts the bot after 10 min of a silent log).
- Restart (run from the MAIN dir, never after `cd` into the LG dir:
  pgrep would match the own shell):
  ```
  D=/home/vondr/programs/auto-eatventure/auto-eatventurelg; for p in $(pgrep -f '^python3 -m auto_eatventure'); do [ "$(readlink /proc/$p/cwd)" = "$D" ] && kill -TERM $p && kill -CONT $p; done; K=$(ps -eo pid,cmd | awk '$2=="konsole" && /Auto EatVenture LG/ {print $1}'); [ -n "$K" ] && kill $K
  ```
- Merge into the LG branch after a change on `potion-shop`:
  ```
  L=../auto-eatventurelg; git -C $L fetch -q origin; git -C $L merge --no-edit origin/potion-shop && git -C $L push -q origin HEAD:potion-shop-lg
  ```
  (reference.py conflicts: keep the LG anchors `Center(...)`, `Top(...)`.)
- To play the event again: `POTION_SHOP_ENABLED="1"` in the LG `.env`,
  restart.

## Rules from the user (still valid)

- Never tap ads, Boost, Activate/Pass, Collect x2; spend only in-game
  coins, corks, ingredients (no real money). The user may buy boosts
  themselves.
- `POTION_SHOP_ENABLED` stays off by default in the repo; develop on
  `potion-shop`, push after each change, merge into `potion-shop-lg`;
  master only when asked.
- Don't interfere when someone uses the phone; don't look at personal
  content. Reports to the user in Czech.
