# Plan: transcript of a Potion Shop speedrun video -> step-by-step guide

Task for a new Claude Code session (repo auto-eatventure, branch
`potion-shop`). Written 2026-10-23 after a pilot on 2 minutes of the
video; the scripts here are tested.

## Goal

Video: https://www.youtube.com/watch?v=OQozLoAeDZU - "Eatventure Potion
Event 21m 03s (without buying cash)" by Rosix, 21:16 long, portrait
886x1920, no commentary, captions or description: everything must be
read from the frames.

Deliverables (in this folder, committed and pushed to `potion-shop`):
1. `TRANSCRIPT.md` - detailed chronological transcript of the run: when
   each station was unlocked and upgraded to which level, every brew
   (potion, level, start/end), every upgrade bought (and the ones skipped),
   bottling, event tasks/rewards.
2. `GUIDE.md` - a step-by-step ("polopatický") guide in Czech derived
   from the transcript: in which order to unlock and upgrade stations,
   which potions to brew to which level and when, which upgrades to buy
   and skip, so the run can be replayed the same way in a similar time.
3. A short reply to the user (in Czech) with the main findings and the
   open questions. Do NOT change the bot's code (`BREW_PLAN` etc.) in
   this task; propose changes and ask.

What matters most (user's words, 2026-10-23): the order of the steps;
when each station opened and roughly (better exactly) to which level it
was upgraded when; when each potion could be brewed and to which level;
when each upgrade was bought.

## Rules for the session

- Video, frames and sheets go to the session's scratchpad directory
  (called `$OUT` below), never into the repo. Commit only the .md files
  and scripts of this folder, push after each commit
  (`git -c user.name=Claude -c user.email=noreply@anthropic.com commit`,
  trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
- Don't touch the phone or the running bot (dad's phone, Xiaomi
  e0cb42c1; the LG bot in auto-eatventurelg neither).
- The user allowed installing/updating tools (2026-10-23).
- Write "?" for anything unreadable; never invent values.

## Tools (all checked 2026-10-23)

- `~/.local/bin/yt-dlp` (official release 2026.10.21; NOT in PATH; update
  with `~/.local/bin/yt-dlp -U`). Warnings "Python 3.10 deprecated" and
  "No supported JavaScript runtime" are harmless for now; if formats go
  missing, install deno (https://deno.land, user-level) and retry.
- ffmpeg 4.4 in /usr/bin (vp9, av1, h264 decoders).
- OpenCV in the project's `.venv` (`.venv/bin/python`).
- No tesseract/OCR: the text is read by the (sub)agents from images.
- 4 CPUs, 7 GB RAM, >100 GB free disk.

## Step 1 - download and cut (~5 min, no tokens)

From the repo root (`OUT` = an absolute path in the scratchpad):

```bash
experiments/potion_shop/video_transcript/make_sheets.sh "https://www.youtube.com/watch?v=OQozLoAeDZU" "$OUT"
.venv/bin/python experiments/potion_shop/video_transcript/dialog_sheets.py "$OUT"
```

- `make_sheets.sh` downloads format 248 (1080p vp9, video only, ~215 MB)
  and writes:
  - `$OUT/sheets/NNNN.jpg` - contact sheets, 4x2 frames, 1 frame/s, 296
    px wide, video second burnt in (yellow, top-left). Sheet N = seconds
    8*(N-1) .. 8*N-1; ~160 sheets. Readable: station popups (Level,
    name, price), Brew list, Upgrades rows, task banners.
  - `$OUT/frames/NNNNN.jpg` - 443 px single frames, frame NNNNN = second
    NNNNN-1 (for a closer look).
- `dialog_sheets.py` finds the seconds with an open Cauldron dialog
  (teal background) or Upgrades dialog (dimmed screen + white card),
  writes `$OUT/dialogs.csv` and cuts each dialog window (+-1 s) at 4 fps
  into `$OUT/dialog_sheets/w<SSSS>_<n>.jpg` (SSSS = the window's first
  second; 4x2 frames = 2 s; video time with decimals burnt in). Dialogs
  are open only 1-3 s and the player buys several upgrades a second, so
  these sheets give the order of purchases and the Brew Complete levels.
  Pilot (5:00-7:00): 16 dialog seconds, 5 windows, 17 dialog sheets;
  expect ~150-200 for the whole video.
- For an exact full-resolution frame at time T:
  `ffmpeg -v error -ss T -i $OUT/video.webm -frames:v 1 $OUT/t_T.png`.

Check: count of sheets ~160; open one sheet and one dialog sheet.

## Step 2 - transcribe in parallel (subagents)

Split the video into 8 chunks of 160 s (sheets 1-20, 21-40, ..., 141-160;
chunk k = seconds 160*(k-1) .. 160*k-1). Each chunk gets its base sheets,
plus the dialog sheets whose window start SSSS lies in the chunk, plus
(for continuity only) the last base sheet of the previous chunk.

Model: **sonnet** for the chunk agents (pilot: 2 min of video = ~108k
tokens with 1 fps sheets only; very good detail, it read hold bursts
4 -> 644 second by second, Brew lists and upgrade rows correctly). Expect
~150k per 160 s chunk with the dialog sheets, ~1.2-1.5M in total. Haiku
is not recommended (small numbers like "Lvl 5", ingredient counts and
prices); if you want to try it, run it first on 5:00-7:00 and compare
with `reference_5m00-7m00.md`. The main session (Opus) does the merge,
the checks and the guide.

Start the 8 agents in ONE message (Agent tool, `model: "sonnet"`, run in
background), each writing its result to `$OUT/chunks/chunk_K.md` and
returning only a 5-line summary (keeps the main context small).

Prompt template (fill in K, the time range, the file lists, `$OUT`):

```
You transcribe part of a gameplay video of the mobile game Eatventure,
the "Potion Shop" event (a speedrun, 21 min), from contact sheets. Your
part: video seconds A..B (m:ss .. m:ss), chunk K of 8.

Files (read EVERY one with the Read tool, in this order):
- Base sheets (4x2 frames, 1 frame per second, the video second burnt in
  yellow at each frame's top-left; read row 1 left to right, then row 2):
  $OUT/sheets/NNNN.jpg .. NNNN.jpg
- Continuity only (already covered by chunk K-1, don't report its events
  unless they continue into your part): $OUT/sheets/NNNN.jpg
- Dialog sheets (4 frames per second while a dialog was open, the video
  time with decimals burnt in): $OUT/dialog_sheets/w....jpg ...
  Use them for the exact order of purchases in the Upgrades dialog and for
  the Cauldron dialog (Brew Complete level, Brew list, which Brew was
  tapped).
- Closer look at second S: $OUT/frames/<S+1 zero-padded to 5>.jpg (443 px).
  Use it sparingly (unclear numbers, the ingredient counts above the
  cauldron at a new brew).

Game knowledge:
- Stations (ingredients): Bat Wing Extract, Dragon Scale Dust, Unicorn
  Horn Shavings, Mermaid Tears, Djinn's Breath, Beetle Juice (shop floor);
  Purified Water, Spider Silk, Mystic Mushrooms, Frog Screams (cellar
  below; the view scrolls down to it). A station popup shows "Level N",
  the station name, stars, the time per item and the upgrade price
  (grey = not affordable); holding the button raises the level fast.
  "Unlock" + price over a dashed tile = buying a new station. Bonus tags
  "+1 Machine" / "x2 Profit" appear at level milestones.
- Banners "Unlock X" / "Upgrade X to level N" with rewards = event tasks
  (a green check = done). There are 15 event rewards in total.
- Cauldron in the middle: liquid color + the two ingredient icons with
  counts above it = the potion being brewed. Swift Serum (dark blue; Bat
  Wing + Dragon Scale), Sizzle Serum (red; Dragon Scale + Unicorn),
  Perfect Potion (yellow; Bat Wing + Unicorn), Instant Infusion (cyan;
  Djinn + Unicorn), Double Draught (pink; Mermaid + Dragon Scale), Divine
  Decoction (white; Spider Silk + Mushrooms), Golden Gulp (orange; Beetle
  + Mushrooms); others may exist (Telepathic, Greedy, Addictive, ...):
  report any unknown potion with its color and ingredients. Black, empty
  cauldron = nothing brewing.
- Cauldron dialog: Brew tab lists potions with "Lvl N" (= the level the
  NEXT brew gives) and Brew buttons ("Slots Full!" = all slots used);
  "Brewing..." shows the potion in progress; "Brew Complete!" + Claim
  shows the finished potion with its level. The Active tab (bottle icon)
  lists active potions with Bottle buttons (1 cork; resets the potion).
- Upgrades dialog (title "Upgrades"): rows like "+1 Customer", "+2
  Customers", "+1 Alchemist", "<Station> profit xN", "... is collected /
  made faster". A row that disappears between two frames was bought.
  Report the bought rows in order, and the rows visible but not bought.
- Top bar: coins (letters = magnitude: K, M, B, T, aa, ab, ...) and gems.
  Bottom: "Boost x12 +40 min" button with a countdown; report any change.

Output: write to $OUT/chunks/chunk_K.md (Write tool) a chronological
event list, one line per event, format `m:ss | TYPE | details`:
- STATION_UNLOCK (station, price)
- STATION_LEVEL (station: first -> last level of each burst with the
  times; plus single levels seen; "MAX" at 1000; note grey = stopped
  for money)
- BREW_START (potion, ingredient counts if readable), BREW_DONE (potion,
  level), BREW_LIST (every row: potion + Lvl, Slots Full), BOTTLE (potion,
  level), IDLE (cauldron empty from .. to ..)
- UPGRADE_BOUGHT (name, effect, price, in order), UPGRADE_SKIPPED (name,
  effect, price, affordable?)
- TASK (banner text, reward, done), REWARD (event reward claimed)
- VIEW (camera moves: shop / cellar), OTHER (boost, offers, anything
  unusual)
Use "?" for unreadable values, never guess; mark inferred events
"(inferred)". At the end add: a 5-line summary of the chunk (what was
unlocked, brewed and bought), what was hard to read, and the frames you
looked at closely. Your final answer: only the 5-line summary.
```

## Step 3 - merge and check (main session)

1. Read all `chunks/chunk_*.md`; fix the chunk borders (an event cut in
   two, duplicates from the continuity sheet).
2. Consistency checks: station levels never go down; each potion's
   BREW_DONE levels go up by 1 (a jump = a missed brew: look for it in
   the frames); each upgrade bought once; the potion colors match the
   Brew list; 15 rewards in total. For each "?" or conflict, look at the
   single frames or extract a full-res frame (step 1).
3. If a chunk is clearly bad, re-run it (same prompt, maybe with a
   note what to look at).

## Step 4 - write TRANSCRIPT.md

Sections:
1. Header: source, method (1 fps + 4 fps dialogs, sonnet readers), the
   account (profit x480, Boost x12 the whole run, 1.68M gems - money is
   never the limit there), accuracy (+-1 s; levels exact where a popup
   was read).
2. Phase overview (5-8 phases with time ranges, e.g. "Bat Wing only",
   "Swift + Sizzle", "Mermaid/Double", "Djinn/Instant", "Beetle",
   "cellar", "Divine + Golden", "end: stations only").
3. Full chronological timeline (merged events, `m:ss | ...`).
4. Tables:
   - Stations: unlock time + price; level milestones with times (first
     seen, every burst end, 1000/MAX); bonus milestones if seen.
   - Potions: each brew with start time, level, duration; the Brew list
     snapshots; bottling; when the cauldron was idle.
   - Upgrades: all bought in order (time, name, effect, price); skipped
     rows (esp. customers) with when they were first affordable.
   - Event tasks and rewards (time, text, reward).
5. Open questions / unreadable spots.

## Step 5 - write GUIDE.md (Czech)

A step-by-step guide anyone (and later the bot) can follow:
- numbered steps per phase: "1. Upgraduj Bat Wing (držet) na ~360. 2.
  Kup kotel. 3. ..." with target levels and the trigger for the next
  step ("až je Bat Wing 1000 / až je dost peněz na Unlock").
- a brew plan table: order of potions with target levels (in the bot's
  format too: `('swift', 4), ('sizzle', 4), ...`).
- upgrades: what to buy (alchemists, profit xN, faster), what to skip
  (customers) and why (as far as the video shows).
- the end game: when brewing stopped and what was upgraded last.
- a section "Rozdíly pro slabší účet / pro bota": the run used Boost x12
  (our bot never uses boosts, ads or the Pass - user rule) and a very
  strong account; say which steps depend on money and how to adapt
  (e.g. targets lower, the same order).
- a comparison with the bot's current logic (src/auto_eatventure/actions/
  potion_shop.py: BREW_PLAN, LATE_PLAN, BOTTLE_ORDER, FOCUS_STATIONS,
  LAST_UPGRADES; potion_shop_loop.py) as proposals only.

## Step 6 - finish

- Commit TRANSCRIPT.md, GUIDE.md (and any script fixes) to `potion-shop`,
  push.
- Add a short pointer to experiments/potion_shop/NOTES.md (section
  "Video analysis") and update the memory note potion-shop-automation
  (one line).
- Reply to the user in Czech: what was found (main order, surprises),
  the token cost, open questions, the proposed bot changes (ask before
  implementing).

## Known so far (rough pass 2026-10-23, every 8-20 s - check it)

Bat Wing only to ~365 (0:00-1:10), cauldron ~0:20; Dragon Scale ~1:05,
first brew Swift 1:12; Unicorn ~3:20, Sizzle 3:45-4:50 (Swift and Sizzle
at level 4 at 5:22); Mermaid 5:01 (before the Djinn), Double 5:23-6:48
(levels 1, ?, 3, 4), Swift again 6:49; Djinn 6:57 (after Unicorn MAX);
Beetle ~8:30 (to 1000 by ~9:20); cellar Purified Water ~9:35; Instant
9:20-12:20 (level 3 done 10:20); Spider Silk ~11:40, Mushrooms ~12:00;
Divine 12:30-14:35; Golden 15:00-18:20; cauldron idle from ~18:40; Frog
~20:00 to 1000 -> 15/15 at 21:03. Perfect never brewed. Customer
upgrades never bought; alchemists and profit upgrades bought as soon as
affordable. Details of 5:00-7:00 in `reference_5m00-7m00.md`.
