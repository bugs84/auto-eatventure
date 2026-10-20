# Potion Shop event

Goal: play the Potion Shop event to the end (15/15 rewards), as fast as
possible (the event leaderboard ranks by completion time). Device:
Xiaomi e0cb42c1 (1080x2400). Coordinates are device px unless noted.

## Schedule

Weekly, Saturday to Tuesday (eatventuretools.app). The main screen shows
the event as the 3rd white button in the right column (black cauldron
with green potion, ~1014, 744) with a green "Event ends in" countdown.

## Flow (verified by hand, 2026-10-19)

1. Main screen: tap the cauldron button (1014, 744) -> "Potion Shop"
   dialog (ps_01): Rewards x/15, Free and Pass columns, Enter.
   - Never tap Activate / Pass (the Pass costs real money).
2. Enter (540, 1818) -> green loading screen "Get ready to stir up some
   trouble!" (ps_04), ~8 s.
3. "Welcome to the Potion Shop!" with Open (540, 1422) (ps_05). The bot
   already detects it as `levels.is_open_button_shown()`.
4. Inside: a restaurant-like map, green event coins (top left) instead
   of normal coins. Bottom bar: vault (=Cauldron dialog vault tab),
   Boost x12 (ad, never tap), Cauldron (appears after buying a Potion
   Kettle), Upgrades (bottom right, same place as the main game).
5. Exit: the cauldron button in the right column (1014, 558 inside the
   event) -> the same dialog with an Exit button (540, 1818) (ps_24).

## Inside the event

- Ingredient stations = normal stations: dashed tile + red arrow =
  "Unlock" for coins (ps_07), then the usual station popup with
  level / stars / long-press upgrade (ps_10, ps_11). The bot's
  `stations.find_icons()` finds their arrows (incl. dashed tiles).
- Upgrades dialog = the main game's one: +1 Customer, +1 Alchemist
  (workers), Buy a Potion Kettle, "<ingredient> profit x2", "made
  faster" (ps_12, ps_13). `upgrades._has_badge()` / `_is_dialog_open()`
  work.
- Cauldron dialog (ps_15): tabs Brew / Active Potions / Arcane Vault.
  - Brew: list of potions, each with level, effect, ingredient costs and
    a Brew button (ps_21: Perfect Potion lvl 1 = 21 Bat Wing + 9
    Unicorn Horn, "All workers 5% chance to make perfect food"). Needs
    2+ ingredient stations. After Brew the kettle on the map asks for
    the ingredients like a customer and alchemists carry them (ps_22,
    ps_23); slow with 1 alchemist.
  - Active Potions: bottle potions for use outside the event with corks
    (363 corks, 5 slots, 20 min, effect x0.5) (ps_17).
  - Arcane Vault: permanent artifacts, all MAX on this account (ps_18).
- Red "!" on the Cauldron button = something can be brewed.
- Rewards are claimed automatically when reached (banner with a green
  check, ps_20).
- Leaderboard (bar chart in the event dialog): % completed and "Your
  time" counted from the first Enter (ps_25).
- Map (ps_27): the shop with the stations on top, below it a stone
  tunnel and a second building (probably unlocked later).

## Rewards (15)

1. Unlock Dragon Scale Dust, 2. Unlock Unicorn Horn Shavings,
3. Unlock Mermaid Tears, 4. Unlock Beetle Juice, 5. Unlock Purified
Water, 6. Unlock Spider Silk, 7. Dragon Scale Dust lvl 500, 8. Djinn's
Breath lvl 500, 9. Mermaid Tears lvl 500, 10. Purified Water lvl 500,
11. Spider Silk lvl 500, 12. Unicorn Horn lvl 1000, 13. Beetle Juice
lvl 1000, 14. Spider Silk lvl 1000, 15. All stations lvl 1000.

## Stations (confirmed by the user)

By income, cheapest first; a better station also costs more at the same
level. Ground floor (all level 1000 MAX with 3 stars at 09:00, st_*):
1. Bat Wing Extract 362ak / 0.8 s
2. Dragon Scale Dust 289al
3. Unicorn Horn Shavings 231am / 2.7 s
4. Djinn's Breath 185an / 4 s
5. Mermaid Tears 148ao / 5.3 s
6. Beetle Juice 118ap / 6.7 s
Cellar: 7. Purified Water, 8. Spider Silk, 9. Mystic Mushrooms,
10. Frog Screams (guide lN8mXr71loA: Purified Water x75 158aq ->
Spider x75 551ar -> Mushrooms x75 1at -> Frog x75 1.5au).

## Normal game loop inside the event (test, 5 min)

Unlocked/upgraded stations and bought upgrades, then got stuck: an icon
near the top -> `scroll_if_icons_too_high` swipe started on an open
station popup, so the map never moved (loop of "icons too high").

## Rules from the user

- Never buy anything for real money; never start ads.
- Event coins, ingredients, gems as rewards are fine to spend/use.
- Speed multipliers / boosts: not yet (later, for the fastest route).

## Research (web, 2026-10-19)

Sources: Spectre's Community Handbook sheet
(docs.google.com/spreadsheets/d/1xcVOTizpCp8oQFAalfHUrB91F_Mr-mFZmP1HoHU8xQo,
Potions gid 1452831391, Arcane Vault gid 120729671), eatventuretools.app
/guides/events, YouTube runs (xAryan, Andre V.C., GUNDAM TIME, Johnny
Green). Reddit not reachable.

How it works:
- Gear, pets, helpers don't work inside; the main vault, profit
  multiplier, shop boosts and the ad boost do.
- A potion in a cauldron slot is active 100% of the time inside the
  event until bottled. Each new brew of the same potion = +1 level
  (max level from Crystal Catalyst; MAX here = 10). Costs ~x1.5 per
  level, sweet spot level 6-7.
- Alchemists fill the brew before serving customers (cauldron idle =
  time lost, brewing = fewer served customers).
- Potions: Swift Serum (Bat Wing + Dragon Scale, walk +50%..+350%),
  Sizzle Serum (Dragon Scale + Unicorn, faster food +50%..+800%),
  Perfect Potion (Bat Wing + Unicorn, 5%..100%), Instant Infusion
  (Djinn + Unicorn, 5%..100%), Double Draught (Mermaid + Dragon Scale,
  10%..100%), Divine Decoction (Spider Silk + Mystic Mushrooms,
  5%..60%), Golden Gulp (Beetle Juice + Mushrooms, 5%..40%); others
  (Telepathic, Greedy, Addictive) unused by speedrunners.

Fastest strategy (consensus of the runs):
1. (Boosts x2/x5 for gems at the start - NOT used yet, user rule.)
2. Unlock Bat Wing + Dragon Scale, buy the Potion Kettle and every
   "+1 Alchemist"; only 3-4 customers until late game (more customers
   early clog the alchemists).
3. Brew order (xAryan): Swift to L3-4 -> unlock Unicorn -> Sizzle L4 ->
   Perfect L2-3 -> Djinn -> Instant L4-6 -> Mermaid -> Double. Never
   leave the cauldron idle.
4. Stations: upgrade the best-paying station, aim at its multiplier
   milestones (x10/x50/x75).
5. Late: with Beetle, Spider and Mushrooms open, bottle Perfect and
   Sizzle, brew Divine + Golden. Final set: Swift ~8, Instant ~6,
   Double ~6, Divine 5-6, Golden ~5.
6. Basement: don't open the Frog until its x75 is affordable; Popular
   Dish (10 min cooldown) on Spider / Frog.
7. When potions are done: stop brewing, buy all customers.
Pitfalls: too many customers early, idle cauldron, bottling the core
potions, opening extra stations too early (customers order cheaper
food), leaving the event (reopens station boxes).
Times: casual 2-7.5 h, good runs 27-40 min, best ~13-21 min.

## Automation status (branch potion-shop)

Code: `actions/potion_shop.py` (actions), `potion_shop_loop.py`
(PotionShopLoop), wired in `game_loop.py` (`POTION_SHOP_ENABLED`, off by
default, checked every 30 min). Overnight test runner (not in the repo):
runs PotionShopLoop directly, saves every Cauldron list to
`brew_log/` and the map every 10 min to `progress/`.

Learned while automating (2026-10-19/20, Xiaomi):
- Swipes on the event map are not repeatable (inertia, ~1.1-1.3x the
  swipe length; a swipe starting on a station/tile opens its popup and
  doesn't scroll). So the map is aligned by a landmark (ink, quill and
  books on the counter's right part, `potion_shop_landmark`) measured
  after every swipe; swipes start on the floor right of the kettle.
- At the start the whole shop (counter + 6 stations + 2 tiles) fits on
  one screen; the cellar ("Dig a Cellar" upgrade, 133aa, bought by the
  Upgrades loop) adds 4 station tiles + crates below the shop (ps_51,
  ps_52); the map ends below it with a closed building.
- Landmarks (all measured as the offset from the shop view, device px):
  counter ink/quill (hidden once 9 customers' prices cover the counter,
  00:27 night 2), barrel bottom left, skull above the counter (only
  when scrolled up to the roof, offset ~+1015 = map top), barrel with
  candle at the cellar entrance. Map bottom = offset -2045, cellar view
  -1743 (ref -1970). Without any landmark the fallback swipes alternate
  up/down (one direction only got stuck at the map top).
- Crates (wooden boxes by the stations) = more slots of a station;
  without them ingredients come slowly. Own template (the main game's
  box template scores only ~0.6 there), threshold 0.7 (moving shine).
- Cauldron red badge = a brewed potion is DONE (while brewing the kettle
  shows bubbles with the ingredients it still needs, no badge). The
  badge fades out ~20 s after a new brew; the Claim shows a moment after
  the badge appears. "Brew Complete!" may also open the dialog itself.
- Brew list: rows of potions with icon + "Lvl N" (= level of the next
  brew) + Brew button; while brewing only the brewing row, no button.
  Levels are read by `vision/level_label.py` (digit samples in
  `matching_screenshots/level_digits/`, all 0-9 now). A missing
  sample is dangerous: an 8 was read as 6 -> brewed one level too far;
  MAX_DIFFERENCE is now 0.1 (real matches 0-0.01).
- A swipe that starts on a station opens its popup, which eats the next
  swipes (map stuck at one offset): tap the null spot when the map did
  not move.
- Brew list is longer than the screen: Perfect, Telepathic, Divine
  Decoction (Spider Silk + Mushrooms), Greedy Gulp, Golden Gulp (Beetle
  + Mushrooms), Addictive Aether below (ps_54, ps_55); they show
  "Slots Full!" while 5 potions are active. Read on both pages.
- Bottle (Active Potions tab, ps_56/57): immediate, no confirmation,
  1 cork, frees the slot - and sets the potion's Brew level back to 1
  (the early plan then brewed Perfect again -> LATE_PLAN once Divine is
  in the list: Swift 8, Instant 6, Double 6, Divine 6, Golden 5;
  Perfect then Sizzle bottled when a planned potion needs a slot).
- Cellar stations (01:27): Purified Water, Spider Silk (lvl 132),
  Mystic Mushrooms, Frog - all unlocked by the normal station loop.
- Rewards 8/15 at 02:14 (6 unlocks, Dragon Scale 500, Djinn 500);
  coins ~200-800ah. Station popup: a 3 s hold bought Beetle 361->412,
  a 10 s hold 412->469 and ran out of coins - so coins, not the hold
  time, limit the levels (ps_61-63).
- Rewards 12/15 at 03:55 (Unicorn 1000 done; left: Beetle 1000,
  Spider Silk 1000, all stations 1000); coins ~600ap.
- Stations stop at level 1000 (popup "MAX"); late in the event the
  shop has no icons -> the loop goes to the cellar (coins limit it).
- End game (user's advice 2026-10-20): from Beetle Juice MAX only one
  station gets the coins, the next one by income, until level 1000; a
  station whose last upgrade is still in the Upgrades dialog is not
  worth its levels - coins are saved for that upgrade first (Frog: not
  before "Layer with tritone" x175). Measured at 08:42 (ps_68-72) the
  income per second put Frog before Mushrooms, wrongly: Spider had more
  of its upgrades.
- Upgrades dialog at 10:30 (upg_*): only "Sell as 'Elixir-Grade'"
  Mystic Mushrooms profit x100 1.01at and "Layer with tritone" Frog
  Scream profit x175 1.51au left; Spider Silk 992 (2 stars) 20.5ar/9.3s,
  next level 132as, coins ~136as (+~0.6as/s).
- 12:54 brewed: Swift 9, Instant 8, Double 8, Divine 6, Golden 5
  (list shows the next level). User: Golden at least to 7 ->
  LATE_PLAN golden 7.
- Bug 10:30: in the cellar the Spider Silk popup stayed open - its icon
  is above station_icon_tooltip_y, so stations.upgrade() closes the
  popup by a tap beside the icon, which lands on the station again;
  the null spot is inside that popup too. The open popup hid the
  arrow, so Spider got a level only every few minutes (180as in hand,
  147as the price). A tap on the empty cellar floor
  (potion_shop_cellar_floor) closes it.
- 13:07-13:23 the same with Frog (level 937): the first floor spot was
  inside the Frog popup (middle of the screen); moved left of the
  frogs, outside all three popups.
- Spider MAX 11:09, Mushrooms x100 11:21 and MAX 13:05, Frog x175
  13:06 (user's x2 + Boost x12 ad from 12:50: x52.8, coins ~1au/s).
- 06:32 the phone was taken (Google app in front), the runner stopped
  ("Not inside the event"); not resumed without the user (dad's phone).
- Night 2 state (01:15): Swift 9, Sizzle 8, Instant 8, Double 8,
  Perfect 3 (active levels); Telepathic shows "Slots Full!". No Divine/
  Golden in the list yet (need cellar ingredients).
- Active Potions tab: up to 5 active potions (Bandolier MAX); a brewed
  potion stays active until bottled (1 cork). Divine/Golden (cellar
  ingredients) will need bottling Perfect and Sizzle (TODO).
- Without levels the bot brewed Swift up to level 10 (too much; plan
  says 4 then 8). Now BREW_PLAN with target levels.
- Upgrades badge: a station icon next to the button looks like it ->
  when nothing was bought, the badge is ignored for 60 s.

Next steps (ideas):
1. Cellar: done (every 60 s, 3 loops there). Popular Dish on
   Spider/Frog (guides); don't open the Frog until its x75 (TODO: which
   cellar tile is the Frog).
2. Customers vs alchemists: buy all alchemists, only 3-4 customers
   early (needs reading the Upgrades rows: icon templates).
3. Station targeting: upgrade the best-paying station to its x10/x50/
   x75 milestones instead of every icon.
4. Bottle Perfect + Sizzle when Divine/Golden become available.
5. Leaving the event when 15/15: `leave_if_completed()` looks for the
   green check at the last reward (ps_67; ratio 0.10 with a check, 0
   without) - the Exit path is untested until 15/15.
6. Boosts x2/x5 (gems) for speed - only when the user allows it.
