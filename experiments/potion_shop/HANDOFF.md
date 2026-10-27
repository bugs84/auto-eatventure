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

## State (2026-10-27 ~00:00): resumed, new strategy

- 2026-10-26 23:10 the user asked to continue: play the event on the LG
  with a real strategy (which upgrades exist and are bought, which
  station to upgrade, a list of where the stations are, less
  scrolling). LG `.env` has `POTION_SHOP_ENABLED="1"` again.
- New: `STATIONS_UPGRADES.md` (stations + positions, all 131 upgrade
  rows with prices, the level rules, the strategy). Code:
  `potion_shop_planner.py` (the choice: payback time),
  `potion_shop_upgrades.py` (catalog), `StationPlan` in
  `potion_shop_loop.py` (replaced StationFocus and EndGame),
  `vision/station_popup.py` reads the coin counter, the popup's level
  and the dialog's prices too. Offline test of the planner:
  `$S/tools/plantest.py`; live tests `$S/tools/plan_lg.py [steps]`,
  `stations_lg.py`, `upg_lg.py`, `levelup_lg.py`, `enter_lg.py`.
- First live run 23:52: Bat and Dragon MAX (cheap levels), Djinn x75
  bought by the planner, then Unicorn/Djinn/Mermaid levels.
- Night 2026-10-27 (the user asleep, "do it as well as you can"):
  levels per open popup while nearly the best, the button held for 5+
  levels (the user's wish), coin counter p/q samples, other view
  scrolled to when unread. 01:33 the whole shop MAX; the cellar left.
  Live log of it: `STATIONS_UPGRADES.md` (Live LG 2026-10-27).
- 2026-10-27 07:40 the LG was unplugged (bot stopped). State: whole
  shop and Water MAX, Mushrooms 832, Frog 803, Spider (level unread);
  rows bought after 04:00: Mushrooms x50, Frog x50. 08:12 the user
  asked to stop the event: LG `.env` `POTION_SHOP_ENABLED="0"`, normal
  levels after it is plugged in again.
- Battery of the LG logged every 5 min (`battery_lg.sh` in the dev kit
  dir, log `battery_lg.log`): the user moved the LG to a USB hub at
  ~23:00 and wants a comparison of the drain in the morning (before:
  see the watchdog log's pause/resume times).

## Open points

- Below level 300 the level rules are not measured (next event).
- "Faster" rows are counted like a profit x2 (effect unknown).
- Popups covered: Bat's profit (only cheap levels then), Spider's
  level; Mushrooms/Dragon sometimes (read again after 10 min).
- Coin counter on the Xiaomi: no sample of "T" yet (reads None).

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
