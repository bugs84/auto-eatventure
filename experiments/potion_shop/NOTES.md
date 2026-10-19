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
