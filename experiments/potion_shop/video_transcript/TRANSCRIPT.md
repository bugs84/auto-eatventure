# Transcript: Rosix, "Eatventure Potion Event 21m 03s (without buying cash)"

Source: https://www.youtube.com/watch?v=OQozLoAeDZU (21:16, 886x1920, no
commentary). Made 2026-10-23 by the plan in `PLAN.md`: 1 fps contact
sheets + 4 fps sheets of every detected dialog (50 windows), read by 8
Sonnet subagents (160 s each, ~1.44M tokens), merged and checked by Opus.

- Times are video time m:ss (+-0.5 s; decimals = from the 4 fps dialog
  sheets). The event clock starts at ~0:07 (the leaderboard's 21m 3s =
  video 21:10).
- Station levels are exact where a popup was read; levels between two
  popups were passed unseen. "?" = unreadable, "(inferred)" = not seen
  directly.
- The account: income x480, gems 1.68M, Boost x12 "+40 min" running the
  whole video (only its countdown changes; never tapped). The Pass is not
  bought (only free rewards). One offer popup (EUR 14.99) was closed
  twice (1:03, 16:33). Money is never short for long: the plateaus where
  a button is grey last seconds, not minutes, until the end game.
- The counter next to the chest icon at the top left (33385 -> 33398)
  counts a reward item (task rewards +4, +2, +6, +1), it is NOT the event
  reward counter (that one is "Rewards N/15" in the event dialog).

## 1. Phases

| Video time | Phase | Stations | Brews |
|---|---|---|---|
| 0:00-0:58 | Bat Wing only | Bat Wing 1 -> 347; Kettle (cauldron) bought 0:17 in the Upgrades dialog | - (cauldron empty, one ingredient only) |
| 0:58-3:43 | Dragon + Swift | Dragon Scale 0:58; Bat Wing -> 638; cellar dug 1:45 (upgrade) | Swift 1-4 |
| 3:14-5:21 | Unicorn + Sizzle | Unicorn 3:15 (-> 630); Bat Wing -> 892; Dragon -> 819 | Sizzle 1-4 |
| 5:01-6:48 | Mermaid + Double | Mermaid 5:01 (-> 650 in 13 s); Unicorn -> 985; Dragon -> 998; Bat Wing -> 994 | Double 1-4 |
| 6:48-8:10 | Djinn + Swift | Unicorn MAX 6:56 -> Djinn 6:57, MAX 7:56 | Swift 5-7 |
| 8:10-9:28 | Beetle + Double | Mermaid MAX 8:53; Beetle 8:25, MAX 9:17 | Double 5-6 |
| 9:26-12:27 | Cellar + Instant | Purified Water 9:26 (MAX 13:10); Spider Silk 11:35 (-> 867); Mushrooms 11:59 (-> 810) | Instant 1-6 |
| 12:28-14:58 | Divine | Spider Silk 868 -> 952 (slow, money) | Divine 1-4; Sizzle bottled 14:46 |
| 14:59-18:06 | Golden | Spider Silk -> 982 | Golden 1-5 |
| 18:06-21:10 | End: stations only | 5 customer upgrades 18:07; Mushrooms 872 -> 1000; Frog 19:48 -> 1000; Spider Silk 1000 | none (cauldron empty) |

Order of the potions (bot notation, each brew +1 level):
`('swift', 4), ('sizzle', 4), ('double', 4), ('swift', 7), ('double', 6),
('instant', 6), ('divine', 4), bottle sizzle, ('golden', 5)` - 32 brews,
then no more brewing. Perfect Potion, Telepathic Tincture and Greedy Gulp
were never brewed.

## 2. Stations

| Station | Unlocked | Price | Levels seen (time) | 1000 |
|---|---|---|---|---|
| Bat Wing Extract | at the start | - | 166 (0:16), 347 (0:58), 545 (2:39), 638 (3:14), 707 (3:50), 801 (4:32), 892 (5:19), 994 (6:12) | not seen (before 21:10) |
| Potion Kettle (cauldron) | 0:17.4 | 2.5M | upgrade "Buy a Potion Kettle" | - |
| Dragon Scale Dust | 0:58.5 | ~2.1ab (inferred) | 240 (1:15), 342 (1:52), 514 (2:38), 550 (2:56), 680 (4:02), 819 (5:00), 959 (6:03), 998 (6:37) | not seen (before 21:10) |
| Cellar | 1:45.1 | 133aa | upgrade "Dig a Cellar" (affordable from 0:51, bought later) | - |
| Unicorn Horn Shavings | 3:14.7 | ? | 548 (3:27), 630 (4:17), 806 (5:34), 948 (6:27), 985 (6:50) | 6:56 |
| Mermaid Tears | 5:01 | ? | 650 (5:14), 846 (6:33), 943 (8:03), 992 (8:20) | 8:53 |
| Djinn's Breath | 6:57 | ? (no visible drop) | 501 (7:07), 963 (7:24), 993 (7:41) | ~7:56 |
| Beetle Juice | 8:25 | 1.64aa | 113 (8:29), 916 (8:43), 983 (9:03), 999 (9:15) | 9:17 |
| Purified Water | 9:26.5 | ? (no visible drop) | 403 (9:39), 936 (9:55), 967 (10:36), 984 (11:54), 996 (13:01) | 13:10 |
| Spider Silk | 11:35 | ? | 483 (11:45), 867 (11:52), 937 (13:28), 952 (14:51), 966 (15:59), 982 (17:51) | ~20:25 (task) |
| Mystic Mushrooms | 11:59 | ? | 810 (12:15), 872 (18:27), 884 (19:09), 950 (19:33), 977 (19:44), 993 (20:33) | ~20:34 (inferred) |
| Frog Screams | 19:48 | 13.5ae | 862 (20:06), 923 (20:16), 962 (20:31), 984 (20:47), 993 (21:04) | 21:10 |

How the stations were played:
- A new station is held right away to ~500-650 (one popup per second,
  ~60 levels/s; Mermaid 4 -> 644 in 12 s, Beetle 113 -> 916 in 14 s),
  which does the "level 500" tasks.
- Then the stations are raised in short bursts until the price turns
  grey, switching between the stations; nothing is saved up for.
- Unicorn MAX (6:56) -> Djinn unlocked the next second; Beetle MAX (9:17)
  -> Purified Water 9:26. Djinn, Purified Water and Frog cost almost
  nothing when bought (no visible coin drop / 13.5ae at 29at coins).
- Bonus tags "+1 Machine" (~L25, ~L110) and "x2 Profit" (every ~50
  levels) are passed during the bursts.
- Times per item seen: Bat Wing 5s -> 2.5s (Bigger ladle) -> 1.3s (Chop
  wings) -> 0.8s (Use stronger solvent); Dragon 5.5s -> 2.8s -> 1.8s (Cut
  before grinding); Unicorn 4s -> 2.7s (Coarser grind); Mermaid 5.3s;
  Djinn 4s; Beetle 6.7s; Purified Water 8s; Spider Silk 9.3s; Mushrooms
  10.7s; Frog 12s.

## 3. Potions

Brews (start -> claim, duration; costs = ingredients delivered by the
alchemists):

| # | Potion | Lvl | Start | Claim | ~s | Costs |
|---|---|---|---|---|---|---|
| 1 | Swift Serum | 1 | 0:59.5 | 1:42.9 | 43 | 12 Bat + 6 Dragon |
| 2 | Swift | 2 | 1:43 | ~2:20 (inferred) | 37 | 18 + 9 |
| 3 | Swift | 3 | ~2:21 | 2:52.5 | 32 | 27 + 13 |
| 4 | Swift | 4 | 2:53 | 3:42.7 | 50 | 40 + 20 |
| 5 | Sizzle Serum | 1 | 3:43.2 | 4:02.6 | 19 | 12 Dragon + 6 Unicorn |
| 6 | Sizzle | 2 | 4:03 | 4:23 | 20 | 18 + 9 |
| 7 | Sizzle | 3 | 4:23.7 | 4:49 | 25 | 27 + 13 |
| 8 | Sizzle | 4 | 4:49.6 | 5:21.4 | 32 | 40 + 20 |
| 9 | Double Draught | 1 | 5:22.4 | 5:38.4 | 16 | 12 Mermaid + 9 Dragon |
| 10 | Double | 2 | 5:39.1 | ~5:56 (inferred) | 17 | ~16-18 + 13 |
| 11 | Double | 3 | ~5:56.5 (inferred) | 6:19.4 | 23 | 27 + 20 |
| 12 | Double | 4 | 6:19.6 | 6:48.2 | 29 | 40 + 30 |
| 13 | Swift | 5 | 6:48.6 | 7:10.4 | 22 | 60 + 30 |
| 14 | Swift | 6 | 7:10.75 | ~7:36.2 | 25 | 91 + 45 |
| 15 | Swift | 7 | 7:36.4 | ~8:10 (inferred) | 34 | 136 + 68 |
| 16 | Double | 5 | ~8:10.5 | ~8:43.5 (inferred) | 33 | 60 + 45 |
| 17 | Double | 6 | ~8:44.5 | 9:28.9 | 44 | 91 + 68 |
| 18 | Instant Infusion | 1 | 9:29.6 | 9:41.4 | 12 | 21 Djinn + 12 Unicorn |
| 19 | Instant | 2 | 9:42 | ~9:56.5 | 14 | 31 + 18 |
| 20 | Instant | 3 | 9:57.5 | 10:20.0 | 22 | 47 + 27 |
| 21 | Instant | 4 | 10:20.8 | 10:50.4 | 30 | 70 + 40 |
| 22 | Instant | 5 | 10:50.9 | 11:31.4 | 40 | 106 + 60 |
| 23 | Instant | 6 | 11:31.9 | 12:27.6 | 56 | 159 + 91 |
| 24 | Divine Decoction | 1 | 12:28.6 | 12:47.6 | 19 | 15 Spider Silk + 6 Mushrooms |
| 25 | Divine | 2 | 12:48.4 | ~13:16.5 | 28 | 22 + 9 |
| 26 | Divine | 3 | 13:18 | 13:51.8 | 34 | 33 + 13 |
| 27 | Divine | 4 | 13:52.4 | 14:58.5 | 66 | 50 + 20 |
| 28 | Golden Gulp | 1 | 14:59.3 | ~15:20 (inferred) | 21 | 12 Beetle + 9 Mushrooms |
| 29 | Golden | 2 | ~15:21 | 15:50.0 | 29 | 18 + 13 |
| 30 | Golden | 3 | 15:50.6 | 16:20.5 | 30 | 27 + 20 |
| 31 | Golden | 4 | 16:21.1 | ~17:03 (inferred) | 41 | 40 + 30 |
| 32 | Golden | 5 | ~17:03.5 | 18:06.2 | 62 | 60 + 45 |

- The cauldron was never idle between 0:59 and 18:06 (claim + new brew
  within ~1 s); idle 0:17-0:59 (no second ingredient yet) and from 18:06
  to the end (Golden Lvl 6, 91 + 68, was offered and not brewed).
- Bottled: only Sizzle Serum Lvl 4 at 14:46 (Active tab, 1 cork; corks
  1.01K; "Bottled Potion Duration 20m, Effect x0.5"). It freed the 5th
  slot for Golden Gulp (Perfect showed "Slots Full!" from 12:47).
- Active at 14:45: Swift 7, Sizzle 4, Double 6, Instant 6, Divine 3. At
  the end (5 slots): Swift 7, Double 6, Instant 6, Divine 4, Golden 5.
- The costs grow x1.5 per level (12, 18, 27, 40, 60, 91, 136, 205, ...);
  a brew's duration follows the costs and how fast the alchemists carry
  the two ingredients (later brews of the same size are faster: more
  alchemists and faster stations).
- Twice a new brew of the same potion started without a captured dialog
  (Swift 2 at 1:43, Double 3 at 5:56): the Brew tap fell between frames,
  or the game re-brews by itself (open question).

All potions seen in the Brew list (9; "Addictive" was not seen):

| Potion | Ingredients (Lvl 1) | Effect (Lvl -> value) | In the list from |
|---|---|---|---|
| Swift Serum | Bat Wing 12 + Dragon 6 | workers walk faster: 1 50%, 3 85%, 4 115%, 5 150%, 6 185%, 7 215% | 0:59 |
| Sizzle Serum | Dragon 12 + Unicorn 6 | workers make food faster: 1 50%, 3 135%, 4 215% | 3:43 |
| Perfect Potion | Bat Wing 21 + Unicorn 9 | 5% chance to make perfect food | 3:43 |
| Double Draught | Mermaid 12 + Dragon 9 | chance of double (5: 40%) | 5:22 |
| Instant Infusion | Djinn 21 + Unicorn 12 | chance to make food instantly: 1 5%, 4 25%, 5 35%, 6 45% | 7:36 |
| Telepathic Tincture | Djinn 15 + Dragon 9 | 10% chance customers order instantly | 7:36 |
| Divine Decoction | Spider Silk 15 + Mushrooms 6 | chance ... (4: 15%, 5: 25%) | 12:27 |
| Greedy Gulp | Purified Water 12 + Spider Silk 9 | 5% chance for a greedy customer | 12:27 |
| Golden Gulp | Beetle 12 + Mushrooms 9 | chance for a golden customer: 1 5%, 3 9%, 4 13%, 5 17%, 6 21% | 12:27 |

## 4. Upgrades

The Upgrades dialog was opened ~45 times, mostly for 1-2 s right when
something became affordable (the red badge). Rules seen:
- Every affordable row was bought except the "+N Customer(s)" rows:
  alchemists, "<station> profit xN", "... faster", also for stations not
  unlocked yet (Djinn, Mermaid, Beetle, cellar ones bought in advance).
- Customer rows: only the first two (Opening discount +1, 23; Free
  samples +2, 3.75K at 0:16) were bought; the others (Host an alchemy
  workshop +2 12.5M, Put up a sign +1 15T, Advertise in 'Wizard Monthly'
  +2 2.25ac, Get a guild endorsement +1 4af, Guarantee efficacy +1 3ai,
  Sponsor a local festival +1 6.4al) stayed blue for 17 minutes and were
  bought all at once at 18:07, one second after the last brew was claimed.
- "Dig a Cellar" (133aa) was affordable from 0:51 but bought at 1:45.

11 alchemists: Hire a potion-mixer 135 (0:16.75), Hire Aurelius 15K
(0:17), Recruit from the forest 20M (0:19.6), Hire another worker 50B
(0:35), Hire Martin the Alchemist 500T (0:42.9), Hire Briar from the
guild 100ab (1:26), Bring on Jax 600ad (2:29.6), Expand to new towns
1.55ag (3:32.4), Hire Jax's mentor 15.5ai (4:54.4), Lure talent from
rivals 130ak (5:53.3), Post job notices 4.15an (6:51.3).

All purchases by dialog (time: rows in order; profit xN = that station's
profit, "fast" = made/collected faster):

| Time | Bought |
|---|---|
| 0:16-0:17 | Opening discount (+1 Customer, 23), Hire a potion-mixer (+1 Alch, 135), Free samples (+2 Customers, 3.75K), Hire Aurelius (+1 Alch, 15K), Buy a Potion Kettle (cauldron, 2.5M) |
| 0:19.6 | Recruit from the forest (+1 Alch, 20M) |
| 0:34-0:35 | Aged wings (Bat x2, 850B), Hire another worker (+1 Alch, 50B) |
| 0:41-0:43 | Bigger ladle (Bat fast, 34.9T), Double concentrated (Bat x3, 3.4aa), Hire Martin (+1 Alch, 500T) |
| 0:51 | Freshly ground (Dragon x2, 680T), Grind harder (Dragon fast, 27.9aa) - before Dragon was unlocked |
| 1:24 | Finely powdered (Dragon x3, 2.72ab) |
| 1:26 | Filtered through Vampire ash (Bat x4, 33.1ab), Hire Briar (+1 Alch, 100ab) |
| 1:34.6 | Chop wings (Bat fast, 1.54ac) |
| 1:45-1:46 | Dig a Cellar (133aa), Paint before shaving (Unicorn x2, 544aa), Precision shaver (Unicorn fast, 22.3ab), Make Djinn brush his teeth (Djinn x2, 436ab), Include certificate (Unicorn x3, 2.18ac), Sourced from Elder Dragons (Dragon x4, 26.5ac), Use Transilvanian Bats (Bat x5, 150ac) |
| 2:02 | Rub clockwise (Djinn fast, 17.9ac), Genuine tears (Mermaid x2, 349ac) |
| 2:25 | Sell as limited edition (Djinn x3, 1.75ad), Fan the flames (Mermaid fast, 14.3ad), Mix with glitter (Unicorn x4, 21.2ad) |
| 2:28-2:29 | Add rubys for color (Dragon x5, 120ad), Aged wings (Bat x10, 750ad), Bring on Jax (+1 Alch, 600ad) |
| 2:44 | Remove shell fragments (Beetle x2, 279ad), Soak to soften (Unicorn fast, 981ad), Double distilled (Mermaid x3, 1.4ae) |
| 2:48-2:49 | Freshly ground (Dragon x10, 600ae), Use stronger solvent (Bat fast, 1.51af) |
| 3:11.9 | Double concentrated (Bat x25, 150af) |
| 3:30-3:33 | Squeeze harder (Beetle fast, 11.5ae), Remake with popular Djinn (Djinn x4, 17ae), Harvest under a double rainbow (Unicorn x5, 96ae), Rub counterclockwise (Djinn fast, 785ae), Rare species blend (Beetle x3, 1.12af), Crystal clear (Water x2, 1.79af), Discard first runnings (Mermaid x4, 13.6af), Bigger buckets (Water fast, 73.1af), Wish customers would pay more (Djinn x5, 76.8af), Paint before shaving (Unicorn x10, 480af), Preheat (Mermaid fast, 628af), Cut before grinding (Dragon fast, 1.21ag), Expand to new towns (+1 Alch, 1.55ag), Use venomous spiders (Spider x2, 6.24ag), Enhanced mineral content (Water x3, 7.14ag), Glow-in-the-Dark Formula (Beetle x4, 10.9ag), Use tears of joy (Mermaid x5, 61.5ag) |
| 3:54-3:55 | Finely powdered (Dragon x25, 121ag), Feed the spiders (Spider fast, 256ag), Make Djinn brush his teeth (Djinn x10, 384ag), Soften carapace (Beetle fast, 503ag), Coarser grind (Unicorn fast, 961ag), Remove dirt (Mushrooms x2, 11.5ah) |
| 4:07-4:08 | Discard weak strands (Spider x3, 25ah), Use golden Beetles (Beetle x5, 49.2ah), Filter out dust (Water x4, 69.3ah), Include certificate (Unicorn x25, 96ah), Genuine tears (Mermaid x10, 308ah) |
| 4:25 | Enhance the substrate (Mushrooms fast, 468ah), Don't rub, just knock (Djinn fast, 769ah), Filtered through Vampire ash (Bat x50, 1ai) |
| 4:54-4:56 | Drill into ceiling (Water fast, 3.22ai), Hire Jax's mentor (+1 Alch, 15.5ai), Send through amplifier (Frog x2, 17.2ai), Hand-picked selection (Mushrooms x3, 45.7ai), Sell as limited edition (Djinn x25, 76.9ai), Higher thread count (Spider x4, 243ai), Remove shell fragments (Beetle x10, 246ai), Label as 'Gravity Perfected' (Water x5, 315ai), Pull a vacuum (Mermaid fast, 615ai), Warm-up ribbits (Frog fast, 702ai), Sourced from Elder Dragons (Dragon x50, 800ai) |
| 5:24-5:26 | Speedy spooling technique (Spider fast, 11.3aj), Double distilled (Mermaid x25, 61.5aj), Apply distortion (Frog x3, 68.5aj), Label as 'Wizard's Choice' (Mushrooms x4, 444aj), Macerate before pressing (Beetle fast, 492aj), Mix with glitter (Unicorn x50, 640aj), Anti-stick coating (Spider x5, 1.11ak), Crystal clear (Water x10, 1.58ak), Dry with hot air (Mushrooms fast, 20.6ak) |
| 5:36 | Use Transilvanian Bats (Bat x75, 75.1ak) |
| 5:53-5:55 | Rare species blend (Beetle x25, 49.2ak), Lure talent from rivals (+1 Alch, 130ak), Remake with popular Djinn (Djinn x50, 512ak), Shift one octave up (Frog x4, 665ak), Sell as 'Elixir-Grade' (Mushrooms x5, 2.02al), Loosen the soil (Water fast, 3.15al), Use venomous spiders (Spider x10, 5.51al), Poke gently (Frog fast, 30.9al), Add rubys for color (Dragon x75, 60al) |
| 6:17-6:18 | Enhanced mineral content (Water x25, 315al), Discard first runnings (Mermaid x50, 410al), Layer with tritone (Frog x5, 3.02am), Remove dirt (Mushrooms x10, 10.1am), Selective spider breeding (Spider fast, 11.1am), Harvest under a double rainbow (Unicorn x75, 48am) |
| 6:51-6:52 | Glow-in-the-Dark Formula (Beetle x50, 328am), Discard weak strands (Spider x25, 1.11an), Post job notices (+1 Alch, 4.15an), Send through amplifier (Frog x10, 15.1an), Control air humidity (Mushrooms fast, 20.2an), Wish customers would pay more (Djinn x75, 38.4an) |
| 7:51 | Hand-picked selection (Mushrooms x25, 2.02ao), Filter out dust (Water x50, 2.1ao), Honey & lemon soak (Frog fast, 30.3ao) |
| 7:58.5 | Use tears of joy (Mermaid x75, 30.8ao) |
| 8:23.9 | Use golden Beetles (Beetle x75, 24.6ap) |
| 9:23 | Apply distortion (Frog x25, 3.02ap), Higher thread count (Spider x50, 7.35ap), Label as 'Wizard's Choice' (Mushrooms x50, 13.5aq), Label as 'Gravity Perfected' (Water x75, 158aq) |
| 13:23 | Anti-stick coating (Spider x75, 551ar), Shift one octave up (Frog x50, 20.2ar) |
| 18:07-18:08 | Host an alchemy workshop (+2 Customers, 12.5M), Advertise in 'Wizard Monthly' (+2, 2.25ac), Get a guild endorsement (+1, 4af), Guarantee efficacy (+1, 3ai), Sponsor a local festival (+1, 6.4al) |
| 19:06.1 | Sell as 'Elixir-Grade' (Mushrooms x100, 1.01at) - checked in an extra 4 fps cut (the dialog detector missed it) |
| 20:08 | Layer with tritone (Frog x175, 1.51au) - the last row (after Frog 6 -> 862) |

Sell as 'Elixir-Grade' (Mushrooms x100, 1.01at) was bought at 19:06.1
(coins 1.01at -> 7.64as; checked in an extra cut), right before
Mushrooms was raised 872 -> 1000. Upgrades from 9:24 to 13:22: none (no
dialog opened; the next rows cost ar-au).

## 5. Event tasks (15, free rewards only)

| Time | Task | Free reward |
|---|---|---|
| 1:00 | Unlock Dragon Scale Dust | 10 gems |
| 2:38 | Upgrade Dragon Scale Dust to level 500 | 4 (box) |
| 3:15 | Unlock Unicorn Horn Shavings | 20 gems |
| 5:02 | Unlock Mermaid Tears | 5 |
| 5:13 | Upgrade Mermaid Tears to level 500 | 25 |
| 6:58 | Upgrade Unicorn Horn Shavings to level 1000 | 200 gems |
| 7:09 | Upgrade Djinn's Breath to level 500 | 10 (scroll) |
| 8:27 | Unlock Beetle Juice | 2 (chest) |
| 9:19 | Upgrade Beetle Juice to level 1000 | 35 (scroll) |
| 9:29 | Unlock Purified Water | 15 (scroll) |
| 9:50 | Upgrade Purified Water to level 500 | 100 gems |
| 11:37 | Unlock Spider Silk | 50 gems |
| 11:47 | Upgrade Spider Silk to level 500 | 6 (chest) |
| 20:26 | Upgrade Spider Silk to level 1000 | 1 |
| 21:10 | Upgrade all stations to level 1000 | 15 (medal) |

No task needs a potion: brewing only speeds the stations' income up. At
21:13 the event dialog shows Rewards 15/15; the leaderboard: rank 1,
21m 3s (2nd 42m 48s).

## 6. Open questions

- Bat Wing and Dragon Scale 1000: never seen in a popup (last 994 at
  6:12, 998 at 6:37); they were 1000 by 21:10 (last task).
- Why were the customer upgrades skipped until the last brew? Likely:
  more customers keep the alchemists busy serving, so they bring the
  ingredients to the cauldron more slowly; after 18:06 only money
  matters. Not proven by the video.
- Why did brewing stop at 18:06 (Golden 6 offered)? Probably the last
  stations (Mushrooms, Frog) need money only, and a new 3-4 min brew
  would not pay off before the end.
- Why Frog only at 19:48 (13.5ae at 29at coins) and Beetle only at 8:25
  (a dashed tile at the lower right from 7:08)? A tile may show up only
  after a milestone of the previous station; not visible.
- Does the cauldron re-brew the same potion by itself (Swift 2 at 1:43,
  Double 3 at 5:56 started with no captured dialog)?
- Unlock prices of Unicorn, Mermaid, Djinn, Purified Water, Spider Silk
  and Mushrooms (bought between two frames).
- Effects of Double Draught and Divine Decoction (text cut).

## 7. Full timeline

The merged event lists of the 8 readers (chunk borders checked: the
continuity lines at the start of a chunk repeat the previous chunk's
end). Format `m:ss | TYPE | details`.

### Chunk 1 (video 0:00 .. 2:39)

```
Notes: times are +-0.5 s. Base-sheet frames are not exactly on the integer
second (the frame labelled 15s is really ~15.4 s per the dialog sheets), so
dialog-sheet times (decimals) are the better ones. Coin letters: K, M, B, T,
aa(1e15), ab, ac, ad, ae (each x1000). Stations seen: only Bat Wing Extract
and Dragon Scale Dust (shop floor). No cellar visit, no Brew list.
0:00 | OTHER | Event dialog "Potion Shop" (Rewards 0/15, Free / Pass columns, Pass "Activate" not used). Task rows visible: Unlock Unicorn Horn Shavings (20 / 360), Unlock Mermaid Tears (5 / 10), Unlock Beetle Juice (2 / 36), Unlock Purified Water (15 / 15), a row above (Dragon Scale) Dust (10 / 180). "Enter" tapped (0:00-0:01). Event ends in 1d 7h. Coins 3.64B, gems 1.68M, x480.
0:01-0:05 | OTHER | Loading screen "Get ready to stir up some trouble!" (cauldron on fire).
0:06 | OTHER | "Welcome to the Potion Shop!" dialog with "Open". Open tapped ~0:06.5.
0:07-0:10 | OTHER | Shop floor with confetti; nothing built yet visible (no dashed tiles yet); Boost x12 +40 min button, countdown 5h 20m 4s at 0:08 (just counts down, never used in this chunk). No view change.
0:11 | VIEW | Shop (top-down, bar at top, cauldron spot middle). Dashed buy tiles + red arrows appear on the left/right side. Whole chunk stays on the shop floor.
0:11 | STATION_LEVEL | FIRST ACTION: tap on the Bat Wing Extract station (already present at the left, a worker + cloud appears): popup "Level 1, Bat Wing Extract, 6 / 5s, price 3". Bat Wing is never "unlocked" in this chunk, it exists from the start.
0:11-0:16 | STATION_LEVEL | Bat Wing Extract 1 -> 166 in one held burst (1:  L1 price 3 at 11s; L9 price 8 at 12s; L26 price 52 at ~13s [tags +1 Machine and x2 Profit shown]; L69 price 6.67K at 14s; L106 517K at 15.0; L121 2.42M at 15.25; L136 13.3M at 15.5; L153 90.9M at 15.75; L166 at 16.0). Coins 3.64B -> 336M. Stopped at L166: price 397M GREY (coins 336M). Time per item 5s.
0:16-0:18 | UPGRADE_BOUGHT | Upgrades dialog #1 opened ~16.1 (button bottom right blue arrow). In order (disappearing rows): "Opening discount" +1 Customer 23 (gone at 16.5); "Hire a potion-mixer" +1 Alchemist 135 (gone at 16.75); "Free samples" +2 Customers 3.75K and "Hire Aurelius" +1 Alchemist 15K (both gone at 17.0); "Buy a Potion Kettle" Unlock Brew Kettle 2.5M (gone between 17.25 and 17.5; coins 336M -> 334M). The Kettle = the cauldron.
0:16-0:18 | UPGRADE_SKIPPED | Dialog #1 left visible (coins 334M): "Host an alchemy workshop" +2 Customers 12.5M (BLUE, affordable); "Recruit from the forest" +1 Alchemist 20M (BLUE, affordable at that moment); "Hire another worker" +1 Alchemist 50B (grey); "Aged wings" Bat Wing profit x2 850B (grey); "Put up a sign" +1 Customer 15T (grey).
0:18 | OTHER | Dialog closed ~18.1. Cauldron is now visible in the shop middle (BLACK, EMPTY), crates at the bat wing station, a cauldron button appears at the bottom bar next to the Upgrade arrow. Cauldron bought at ~0:17.4.
0:18 | IDLE | Cauldron empty from ~0:17.4 to ~0:59.5 (no brew possible: only one ingredient station exists).
0:19-0:20 | UPGRADE_BOUGHT | Upgrades dialog #2 (19.4-20.0): "Recruit from the forest" +1 Alchemist 20M bought at ~19.6 (coins 334M -> 314M).
0:19-0:20 | UPGRADE_SKIPPED | Dialog #2: Host an alchemy workshop 12.5M (BLUE), Hire another worker 50B (grey), Aged wings 850B (grey), Put up a sign 15T (grey), Bigger ladle (Bat Wing made faster) 34.9T (grey, partly seen).
0:20 | OTHER | Coins 50.5B at 20s (income), more bat wing machines/workers visible at the left (4 slots after the +1 Machine tag).
0:20-0:24 | STATION_LEVEL | Bat Wing 166 -> 211 (L166 price 397M blue at 21s, L177 at 22s, L197 price 13.4B at 23s, L211 at 24.0). Stopped at L211: price 65B GREY (coins 14.9B). Tag x2 Profit at L211.
0:25-0:26 | UPGRADE_SKIPPED | Upgrades dialog #3 (25.0-25.9), nothing bought, closed ~26.0 (coins 14.9B): Host an alchemy workshop 12.5M (BLUE), Hire another worker 50B (grey), Aged wings 850B (grey), Put up a sign 15T (grey), Bigger ladle 34.9T (grey).
0:26-0:29 | OTHER | Waiting, bat wing popup L211 grey (65B, coins 14.9B) shown 26.75-29. Coins 14.9B.
0:29-0:31 | STATION_LEVEL | Bat Wing 211 -> 233 (L233 price 787B grey at 30s, coins 421B).
0:31-0:32 | STATION_LEVEL | Bat Wing 233 -> 236 (L236 price 1.11T GREY at 32s, coins 976B).
0:34-0:35 | UPGRADE_BOUGHT | Upgrades dialog #4 (34.1-35.4), coins 976B: "Aged wings" Bat Wing profit x2 850B bought ~34.8 (coins 976B -> 126B); "Hire another worker" +1 Alchemist 50B bought ~35.1 (126B -> 76.3B).
0:34-0:35 | UPGRADE_SKIPPED | Dialog #4 left: Host an alchemy workshop 12.5M (BLUE), Put up a sign 15T (grey), Bigger ladle 34.9T (grey), Hire Martin the Alchemist +1 Alchemist 500T (grey), Freshly ground (Dragon Scale Dust profit x2) 680T (grey).
0:35-0:39 | STATION_LEVEL | Bat Wing 236 -> 255 (L236 1.11T blue at 36.0, L238 1.39T at 36.5, L241 1.95T at 36.75, L246 3.44T GREY at 37-38 (coins 2.66T), L255 at 39.0 price 9.52T blue). Tag x2 Profit at L255.
0:41-0:43 | UPGRADE_BOUGHT | Upgrades dialog #5 (41.4-43.4), coins 4.88aa: "Bigger ladle" Bat Wing made faster 34.9T bought ~41.9 (4.88aa -> 4.84aa); "Double concentrated" Bat Wing profit x3 3.4aa bought ~42.6 (4.84aa -> 1.44aa); "Hire Martin the Alchemist" +1 Alchemist 500T bought ~42.9 (1.44aa -> 947T).
0:41-0:43 | UPGRADE_SKIPPED | Dialog #5 left (coins 947T): Host an alchemy workshop 12.5M (BLUE), Put up a sign 15T (BLUE), Freshly ground (Dragon profit x2) 680T (BLUE, affordable, not bought), Grind harder (Dragon Scale Dust made faster) 27.9aa (grey), Dig a Cellar (Unlock Cellar) 133aa (grey), Paint before shaving (Unicorn Horn Shavings profit x2) 544aa (grey).
0:43-0:48 | STATION_LEVEL | Bat Wing 255 -> 294: time per item now 2.5s (after Bigger ladle): L259 price 15T blue at 44s, L272 65.4T at 45s, L289 449T GREY at 46-47 (coins 187T), L294 791T grey at 48 (coins 203T).
0:49-0:50 | STATION_LEVEL | Bat Wing L303 (2.2aa blue) -> L304 (2.46aa GREY, coins 1.91aa) at 49.25; tag x2 Profit at L304.
0:50-0:51 | UPGRADE_BOUGHT | Upgrades dialog #6 (50.4-51.6), coins 409aa: "Freshly ground" Dragon profit x2 680T and "Grind harder" Dragon Scale Dust made faster 27.9aa bought together ~51.1 (409aa -> 381aa). (Dragon station not unlocked yet, upgrades bought in advance.)
0:50-0:51 | UPGRADE_SKIPPED | Dialog #6 left (coins 381aa): Host 12.5M (BLUE), Put up a sign 15T (BLUE), Dig a Cellar 133aa (BLUE, affordable, not bought), Paint before shaving 544aa (grey), Finely powdered (Dragon profit x3) 2.72ab (grey).
0:52-0:58 | STATION_LEVEL | Bat Wing 304 -> 347: L304 2.46aa blue at 52s, L306 at 52.5, L309 4.33aa at 52.75, L318 12.1aa at 53s, L332 58.7aa GREY at 54s (coins 11.6aa), L332 blue at 55s (1.09ab), L342 183aa GREY at 56s (coins 69.8aa), L347 322aa blue at 58s (coins 8.29ab, 5 stars filled soon).
0:58-0:59 | STATION_UNLOCK | Dragon Scale Dust: new station appears on the right side (coin pile on the right station tile) between 58.0 and 59.0. Price not readable (the buy popup not seen; coins fell 8.29ab -> 6.18ab, so roughly 2.1ab, inferred). Frame at 59: banner at the cauldron.
0:59 | TASK | "Unlock Dragon Scale Dust" (rewards 10 gems Free / 180 Pass, locked) shown at ~59-62; gem effect flying to the top at 60 (reward 10 claimed), check/greyed at 62. Event reward counter (chest 33385 top left) unchanged.
0:59-1:00 | BREW_START | Cauldron turns from black to dark blue with ingredient counts "12" (Bat Wing) and "6" (Dragon Scale) above it at 60s (frame 00061): Swift Serum (dark blue; bat 12 + dragon 6) started between 59.0 and 60.0, no cauldron dialog opened (inferred automatic brew once Dragon unlocked; cauldron button had a red "!" at 59-60).
1:01 | OTHER | "Select a dish" dialog (icons: Bat Wing and Dragon Scale coloured, Unicorn/Djinn lamp/Mermaid/Beetle/Water/Spider/Mushrooms greyed) over a dimmed dialog; opened ~60.5, closed via X before 62 (no purchase seen, no new station appeared). Coins 8.89ab.
1:02 | OTHER | Cauldron on fire (flames), Swift Serum bat 12 / dragon 6 still; coins 18.9ab. Banner "Unlock Dragon Scale Dust" greyed (done).
1:03-1:08 | OTHER | "Big Potion Shop Offer" popup (-92 %, 1d 7h, 30 + 120 + 7.2K items, EUR 14.99) open ~62.7-68.5, closed with the X without buying. Coins 18.9ab -> 38.9ab meanwhile.
1:09 | OTHER | Shop view again; cauldron counts "10" bat / "6" dragon (Swift Serum, counting down as ingredients arrive). A Bat Wing (hat) icon appears at the top middle (round icon at the roof, new from 61s: Swift Serum active indicator, inferred).
1:10-1:14 | STATION_LEVEL | Bat Wing 355 -> 377: L355 795aa blue at 70s (coins 57.3ab), L359 1.26ab at 71s, L372 5.46ab at 72s (coins 18.4ab), L377 9.62ab at 74s (coins 83.9ab). Time per item 2.5s. (The Dragon station popup is not shown between 59 and 74, Dragon climb from L1 to L240 not visible.)
1:15-1:18 | STATION_LEVEL | Dragon Scale Dust: first seen L240 (1.4aa blue, 99.6T, 5.5s) at 75s; L247 (3.08aa) 76s; L263 (18.9aa) 77s with tag x2 Profit; L280 (130aa) at 78.0; L293 (565aa) 78.25; L295 price 709aa GREY at 78.5 (coins 23.1aa).
1:18-1:20 | UPGRADE_SKIPPED | Upgrades dialog #7 (78.9-80.1), nothing bought (coins 23.1aa): Host an alchemy workshop 12.5M (BLUE), Put up a sign 15T (BLUE), Dig a Cellar 133aa (grey), Paint before shaving 544aa (grey), Finely powdered (Dragon profit x3) 2.72ab (grey).
1:20-1:23 | OTHER | Waiting (coins 23.1aa, cauldron counts about 10/5). Dragon L295 grey.
1:23-1:24 | OTHER | Coins 900ab at 83.0-83.75 (payment burst, coins 6.61ab -> 900ab).
1:23-1:25 | UPGRADE_BOUGHT | Upgrades dialog #8 (83.6-84.7), coins 900ab: "Finely powdered" Dragon Scale Dust profit x3 2.72ab bought ~84.4 (900ab -> 897ab).
1:23-1:25 | UPGRADE_SKIPPED | Dialog #8 left visible (all BLUE, affordable): Host an alchemy workshop 12.5M, Put up a sign 15T, Dig a Cellar 133aa, Paint before shaving 544aa, Precision shaver (Unicorn Horn shaved faster) 22.3ab, Filtered through Vampire ash (Bat Wing profit x4) 33.1ab.
1:25-1:27 | UPGRADE_BOUGHT | Upgrades dialog #9 (85.1-86.6), coins 897ab: "Filtered through Vampire ash" Bat Wing profit x4 33.1ab bought ~85.9 (897ab -> 864ab); "Hire Briar from the guild" +1 Alchemist 100ab bought ~86.3 (864ab -> 764ab).
1:25-1:27 | UPGRADE_SKIPPED | Dialog #9 left (coins 764ab): Host 12.5M (BLUE), Put up a sign 15T (BLUE), Dig a Cellar 133aa (BLUE), Paint before shaving 544aa (BLUE), Precision shaver 22.3ab (BLUE), Make Djinn brush his teeth (Djinn's Breath profit x2) 436ab (BLUE), Chop wings (Bat Wing made faster) 1.54ac (grey).
1:27-1:29 | STATION_LEVEL | Bat Wing 383 -> 399: L383 19ab blue (87.25-87.5), L386 26.7ab (87.75), L393 59ab (88s), L399 117ab GREY at 89-91 (coins 39.6ab). 5 stars, 2.5s.
1:29-1:30 | UPGRADE_SKIPPED | Upgrades dialog #10 (89.4-90.4), nothing bought (coins 39.6ab): Host 12.5M (BLUE), Put up a sign 15T (BLUE), Dig a Cellar 133aa (BLUE), Paint before shaving 544aa (BLUE), Precision shaver 22.3ab (BLUE), Make Djinn brush his teeth 436ab (grey), Chop wings 1.54ac (grey), Include certificate (Unicorn profit x3) (partly seen).
1:33-1:35 | UPGRADE_BOUGHT | Upgrades dialog #11 (93.9-95.1): "Chop wings" Bat Wing is made faster 1.54ac bought ~94.6 (coins 2.4ac -> 875ab). Bat Wing time per item 2.5s -> 1.3s (seen at 95.75).
1:33-1:35 | UPGRADE_SKIPPED | Dialog #11 left (coins 875ab): Host 12.5M (BLUE), Put up a sign 15T (BLUE), Dig a Cellar 133aa (BLUE), Paint before shaving 544aa (BLUE), Precision shaver 22.3ab (BLUE), Make Djinn brush his teeth 436ab (BLUE), Include certificate 2.18ac (grey), Advertise in 'Wizard Monthly' +2 Customers 2.25ac (grey).
1:36-1:42 | STATION_LEVEL | Bat Wing 399 -> 427 (stars reset after L400; tag x2 Profit at L403-L409): L403 184ab blue (96s), L409 362ab GREY (97s, coins 16.8ab), L411 454ab blue (99s), L414 638ab grey (100s, coins 88.6ab), L418 1.01ac at 101.0, L420 1.26ac at 101.25, L424 1.98ac GREY at 101.5-101.75 (coins 836ab), L427 2.78ac GREY at 102.0-102.25 (coins 1.67ac). Time 1.3s.
1:42-1:43 | OTHER | Dragon L? counts: cauldron shows only the Dragon icon "1" at 99s (bat wing ingredients all delivered, 1 dragon left).
1:42-1:43 | BREW_DONE | Cauldron dialog opened ~102.2 (Cauldron, tabs: brew / bottle / third), "Brewing..." Swift Serum Lvl 1 ("All workers walk 50% faster", dragon icon with 1 left) at 102.0-102.5; at ~102.7 turns "Brew Complete!" Swift Serum Lvl 1 with a Claim button; Claim tapped ~102.9. Brew took about 43 s (59.5 -> 102.7). The Brew list (potion rows) was NOT shown, no other potion seen.
1:43-1:44 | BREW_START | Right after the claim (dialog fading at 103.0) the cauldron shows a new brew: counts "18" bat wing / "9" dragon at 103-104 (frame 00104), dark blue liquid = Swift Serum again (probably Lvl 2, counts about 1.5x the first; the potion not re-chosen in a dialog: automatic restart, inferred). Red "!" on the cauldron button from ~103.7 to the end of chunk.
1:44-1:47 | UPGRADE_BOUGHT | Upgrades dialog #12 (104.4-107.1), coins 163ac -> 25.7ac, bought in this order (row order top to bottom, each gone in the next frames): "Dig a Cellar" Unlock Cellar 133aa (~105.1); "Paint before shaving" Unicorn Horn Shavings profit x2 544aa and "Precision shaver" Unicorn Horn shaved faster 22.3ab (~105.4); "Make Djinn brush his teeth" Djinn's Breath profit x2 436ab (~105.6); "Include certificate" Unicorn Horn Shavings profit x3 2.18ac (~105.9); "Sourced from Elder Dragons" Dragon Scale Dust profit x4 26.5ac (~106.4, coins 181ac -> 155ac); "Use Transilvanian Bats" Bat Wing profit x5 150ac (~106.6, coins 155ac -> 5.32ac). The cellar is dug (view not moved to it in this chunk).
1:44-1:47 | UPGRADE_SKIPPED | Dialog #12 left at ~107.0 (coins 25.7ac): Put up a sign 15T and Host (partly seen above), Advertise in 'Wizard Monthly' +2 Customers 2.25ac (BLUE), Rub clockwise (Djinn's Breath collected faster) 17.9ac (BLUE; grey at 106.75 when coins 5.32ac), Genuine tears (Mermaid Tears profit x2) 349ac (grey), Grind fewer at once (Dragon Scale Dust made faster) 1.23ad (grey).
1:47-1:52 | STATION_LEVEL | Dragon Scale Dust 299 -> 342 with 5.5s: L299 price 1.12ab blue at 110s (coins 5.13ac), L314 6.11ab at 111s (tag x2 Profit), L342 146ab at 112s (coins 4ac). Bat Wing: L429 3.49ac blue at 108s (coins 40.3ac), L436 7.71ac grey at 109s (coins 5.13ac), L437 8.64ac blue at 114s (coins 2.03ad), L450 37.7ac at 115s (coins 1.79ad; tag x2 Profit fading), L467 259ac GREY at 116-117s (coins 172ac; tag x2 Profit), L477 804ac grey at 118s (coins 71.7ac), L477 blue at 119s (coins 4.51ad). (Coins jump 4ac -> 2.04ad at 112-113: big customer payment.)
2:00-2:03 | STATION_LEVEL | Bat Wing L480 1.13ad blue (120.0), L481 1.27ad GREY at 120.25-120.5 (coins 670ac).
2:00-2:03 | UPGRADE_BOUGHT | Upgrades dialog #13 (120.6-122.6), coins 670ac: "Rub clockwise" Djinn's Breath collected faster 17.9ac bought ~122.1 (670ac -> 652ac); "Genuine tears" Mermaid Tears profit x2 349ac bought ~122.4 (652ac -> 304ac).
2:00-2:03 | UPGRADE_SKIPPED | Dialog #13 left (coins 304ac): Host 12.5M (BLUE), Put up a sign 15T (BLUE), Advertise in 'Wizard Monthly' +2 Customers 2.25ac (BLUE), Grind fewer at once (Dragon made faster) 1.23ad (grey), Sell as limited edition (Djinn's Breath profit x3) 1.75ad (grey), Fan the flames (Mermaid Tears distilled faster) 14.3ad (grey).
2:03-2:08 | STATION_LEVEL | Bat Wing 481 -> 488: L481 blue at 123.25 (coins 13.3ad), L482 1.42ad (123.5), L485 1.99ad (123.75), L488 2.8ad GREY at 124 (coins 588ac); Dragon Scale Dust L358 894ab (84.1ab, time now 2.8s) at 127s (5 stars, coins 34.7ad), L372 4.37ac at 128s, L401 117ac at 129s (1 star, tag x2 Profit), L432 3.92ad GREY at 130s (coins 2.08ad, tag x2 Profit). Dragon time per item went from 5.5s (L342, 112s) to 2.8s (L358, 127s): no dialog purchase seen in between, cause unknown (milestone?).
2:08-2:14 | STATION_LEVEL | Bat Wing L488 2.8ad GREY (coins 2.08ad) at 131-133, L494 5.52ad GREY at 134 (coins 1.75ad), L501 12.2ad GREY at 135 (coins 5.57ad, tag x2 Profit), L507 24.1ad blue at 138 (coins 63.5ad), L512 42.5ad GREY at 139-140 (coins 32.2ad), L513 47.6ad blue at 142 (coins 3.1ae), L526 208ad blue at 143 (coins 2.62ae), L534 514ad GREY at 144 (coins 76.7ad).
2:19-2:21 | BREW_DONE | (inferred) second Swift Serum brew finished: cauldron counts down to only dragon "2" at 138s (bat wing delivered); at 141s counts reset to "27" bat wing / "13" dragon (third brew, dark blue = Swift Serum, probably Lvl 3, started ~139-141 without any dialog).
2:19-2:21 | BREW_START | (inferred) Swift Serum 27 bat wing / 13 dragon at 141s; counts 22/12 at 147s; bat 13 at 158s.
2:24-2:26 | UPGRADE_BOUGHT | Upgrades dialog #14 (144.4-146.6), coins 76.7ad -> 39.6ad: "Sell as limited edition" Djinn's Breath profit x3 1.75ad (~145.2, 76.7ad -> 75ad); "Fan the flames" Mermaid Tears distilled faster 14.3ad (~145.4, 75ad -> 60.7ad); "Mix with glitter" Unicorn Horn Shavings profit x4 21.2ad (~145.7, 60.7ad -> 39.6ad).
2:24-2:26 | UPGRADE_SKIPPED | Dialog #14 left (coins 39.6ad): Put up a sign 15T (BLUE), Advertise in 'Wizard Monthly' 2.25ac (BLUE), Add rubys for color (Dragon Scale Dust profit x5) 120ad (grey), Remove shell fragments (Beetle Juice profit x2) 279ad (grey), Bring on Jax +1 Alchemist 600ad (grey), Aged wings (Bat Wing profit x10) 750ad (grey), Soak to soften (Unicorn Horn shaved faster) 981ad (grey, partly seen). Dialog stayed open till ~146.6 with nothing more bought.
2:27-2:30 | UPGRADE_BOUGHT | Upgrades dialog #15 (147.9-149.9), coins 13.4ae -> 12ae: "Add rubys for color" Dragon profit x5 120ad (~148.4); "Aged wings" Bat Wing profit x10 750ad (~149.4, 13.3ae -> 12.6ae); "Bring on Jax" +1 Alchemist 600ad (~149.6, 12.6ae -> 12ae).
2:27-2:30 | UPGRADE_SKIPPED | Dialog #15 left (coins 12ae): Host 12.5M (BLUE), Put up a sign 15T (BLUE), Advertise in 'Wizard Monthly' 2.25ac (BLUE), Remove shell fragments (Beetle Juice profit x2) 279ad (BLUE, affordable, not bought), Soak to soften (Unicorn Horn faster) 981ad (BLUE, not bought), Double distilled (Mermaid Tears profit x3) 1.4ae (BLUE, not bought), Squeeze harder (Beetle Juice pressed faster) 11.5ae (BLUE/affordable, not bought, last row).
2:30-2:33 | STATION_LEVEL | Bat Wing L534 514ad blue at 150.5 (coins 12ae), L535 575ad at 150.75, L543 1.43ae at 151s (coins 4.53ae). Dragon Scale Dust: L432 3.92ad blue at 152s (coins 1.52ae), L442 12.2ad at 153s, L461 105ad at 154s (coins 799ad, tag x2 Profit), L471 326ad at 156s, L486 1.79ae at 157s (2 stars).
2:37-2:39 | STATION_LEVEL | Dragon Scale Dust L514 price 42.6ae GREY at 158s (coins 11.2ae), tag x2 Profit. Bat Wing L545 1.79ae at 159s (74.8ad, 1.3s).
2:38 | TASK | Banner "Upgrade Dragon Scale Dust to level 500" (rewards: teal chest-like box x4 Free, 72 Pass locked) at 158-159 (reached L500 at ~157.5).
2:38 | REWARD | Event reward counter (chest icon top left) 33385 -> 33389 at 158 (+4 free reward, first of the 15 event rewards claimed in this chunk; the gem 10 reward of Unlock Dragon Scale Dust at 60s did not change the gem counter 1.68M).
0:08-2:39 | OTHER | Boost x12 +40 min never tapped; countdown 5h 20m 4s -> 5h 17m 33s. Gems constant 1.68M. Offers on the right (1d 7h) not used except the popup at 1:03.
```

### Chunk 2 of 8: video 2:40 .. 5:19 (seconds 160..319)

```
Notes on reading: station popup values are "Level N", profit per item, time per item, price. Prices in letters (M, B, T, aa, ab ... aj, ak). Times with decimals come from the 4 fps dialog sheets (+-0.25 s). Coins = top bar; gems stay 1.68M the whole chunk. View is the shop floor the whole chunk (no cellar scroll seen).
2:40 | OTHER | State at chunk start: shop view, cauldron dark blue (Swift Serum brewing, counts above cauldron 10 / 7 = Bat Wing / Dragon Scale, still counting down), coins 32.6ae, Boost x12 +40 min button with countdown 5h17m32s (only runs down in the whole chunk, 5h14m53s at 5:19; no click on Boost seen). Counter at the top-left chest 33389 (constant).
2:40 | TASK | "Upgrade Dragon Scale Dust to level 500", rewards "4" (box with green check = done) and "72" (yellow box, locked). Banner seen 2:38-2:40 (continuity: Dragon Scale 486 at 2:37 -> 514 at 2:38).
2:40-2:41 | STATION_LEVEL | Bat Wing Extract 545 (2:39) -> 551 (2:40) -> 557 (2:41), time 1.3s; GREY at 557 (price 6.96ae, coins 4.06ae) = stopped for money
2:41-2:43 | OTHER | No popup; cauldron dark blue (Swift Serum), counts above cauldron fall; coins stay 4.06ae
2:43.8 | OTHER | Upgrades dialog #1 opened (coins 4.06ae). Rows seen at top: Host an alchemy workshop (+2 Customers, 12.5M), Put up a sign (+1 Customer, 15T), Advertise in 'Wizard Monthly' (+2 Customers, 2.25ac), Remove shell fragments (Beetle juice profit x2, 279ad), Soak to soften (Unicorn Horn is shaved faster, 981ad), Double distilled (Mermaid Tears profit x3, 1.4ae), Squeeze harder (Beetle juice is pressed faster, 11.5ae), Remake with popular Djinn (Djinn's Breath profit x4, 17ae), Harvest under a double rainbow (Unicorn Horn Shavings profit x5, 96ae), Freshly ground (Dragon Scale Dust profit x10, 600ae)
2:44.4 | UPGRADE_BOUGHT | Remove shell fragments - Beetle juice profit x2 - 279ad (coins 4.06ae -> 3.78ae)
2:44.6 | UPGRADE_BOUGHT | Soak to soften - Unicorn Horn is shaved faster - 981ad
2:44.6 | UPGRADE_BOUGHT | Double distilled - Mermaid Tears profit x3 - 1.4ae (coins now 1.41ae)
2:44.8 | UPGRADE_SKIPPED | Squeeze harder (Beetle juice is pressed faster) 11.5ae, Remake with popular Djinn (Djinn's Breath profit x4) 17ae, Harvest under a double rainbow (Unicorn profit x5) 96ae, Freshly ground (Dragon Scale Dust profit x10) 600ae - all GREY (not affordable at 1.41ae)
2:44.8 | UPGRADE_SKIPPED | Host an alchemy workshop (+2 Customers) 12.5M, Put up a sign (+1 Customer) 15T, Advertise in 'Wizard Monthly' (+2 Customers) 2.25ac - buttons BLUE (looked affordable) but never bought (same in every dialog of this chunk)
2:45.1 | OTHER | Upgrades dialog #1 closed (coins 1.41ae)
2:45-2:46 | OTHER | No popup; coins 1.41ae -> 182ae (income); cauldron Swift Serum
2:46.9 | OTHER | Upgrades dialog #2 opened (coins 2.28af). Rows: Host/Put up a sign/Advertise (blue, as above), Squeeze harder 11.5ae (blue), Remake with popular Djinn 17ae (blue), Harvest under a double rainbow 96ae (blue), Freshly ground 600ae, then Rub counterclockwise (Djinn's Breath is collected faster, 785ae), Rare species blend (Beetle juice profit x3, 1.12af), Use stronger solvent (Bat Wing Extract is made faster, 1.51af), Crystal clear (Purified Water profit x2, 1.79af), Get a guild endorsement (+1 Customer, 4af), Discard first runnings (Mermaid Tears profit x4, 13.6af)
2:47.9 | UPGRADE_BOUGHT | Freshly ground - Dragon Scale Dust profit x10 - 600ae (coins 2.28af -> 1.68af)
2:49.1 | UPGRADE_BOUGHT | Use stronger solvent - Bat Wing Extract is made faster - 1.51af (coins -> ~170ae; Bat Wing time later 0.8s instead of 1.3s)
2:49.2 | UPGRADE_SKIPPED | affordable (blue) at the time but not bought: Squeeze harder 11.5ae, Remake with popular Djinn 17ae, Harvest under a double rainbow 96ae, Rub counterclockwise 785ae, Rare species blend 1.12af; grey: Crystal clear 1.79af, Get a guild endorsement 4af, Discard first runnings 13.6af
2:49.4 | OTHER | Upgrades dialog #2 closed (coins 187ae)
2:49.8-2:51.0 | STATION_LEVEL | Bat Wing Extract 557 -> 561 (2:50) -> 568 (2:51.0), time now 0.8s; blue at 568 (24.2ae, coins 44.2ae) when popup switched to Dragon Scale
2:51.2-2:52.3 | STATION_LEVEL | Dragon Scale Dust 514 (2:51.25, blue 42.6ae, 2.8s) -> 515 (2:51.75); GREY at 515 (47.7ae, coins 1.65ae)
2:52.4 | OTHER | Cauldron dialog opened (cauldron button, red "!" badge)
2:52.5 | BREW_DONE | Swift Serum Lvl 3 ("All workers walk 85% faster +30%"), Claim tapped
2:52.8 | BREW_LIST | only one row rendered (frame during open animation): Swift Serum Lvl 4 (costs 40 / 20) with Brew button; other rows not visible
2:53 | BREW_START | Swift Serum Lvl 4 (cauldron dark blue, counts above cauldron 40 Bat Wing / 20 Dragon Scale, frame 00174). Idle gap under 1 s.
2:54-2:55 | STATION_LEVEL | Dragon Scale Dust 517 (2:54, blue 59.9ae, coins 18.4af) -> 530 (2:55, price 261ae blue)
2:56 | STATION_LEVEL | Dragon Scale Dust 550 (coins 1.48af); GREY at 550 (price 2.52af, 87.9ae/item)
2:57 | OTHER | No popup; coins 73.6af
2:58-3:00 | STATION_LEVEL | Bat Wing Extract 570 (2:58, 30.4ae) -> 584 (2:59) -> 608 (3:00); bonus tag "x2 Profit" shown at 3:00 (price 2.26af blue)
3:01-3:02 | OTHER | No popup; coins 1.57af -> 24.6af
3:03 | STATION_LEVEL | Bat Wing Extract 622; GREY (price 11.1af, coins 6.05af)
3:05 | STATION_LEVEL | Bat Wing Extract 624; GREY (13.9af, coins 5.8af)
3:07-3:08 | STATION_LEVEL | Bat Wing Extract 624 (3:07, blue, popup fading, coins 37.1af) -> 626 (3:08, GREY 17.4af, coins 7.93af)
3:09 | OTHER | No popup; coins 44.5af, then 602af at 3:09.5
3:09.7 | OTHER | Upgrades dialog #3 opened (coins 602af). Rows seen: Host/Put up a sign/Advertise (blue), Squeeze harder 11.5ae, Remake with popular Djinn 17ae, Harvest under a double rainbow 96ae, Rub counterclockwise 785ae, Rare species blend 1.12af, Crystal clear 1.79af, Get a guild endorsement 4af, Discard first runnings 13.6af, Bigger buckets (Purified Water is collected faster, 73.1af), Wish customers would pay more (Djinn's Breath profit x5, 76.8af), Double concentrated (Bat Wing Extract profit x25, 150af), Paint before shaving (Unicorn Horn Shavings profit x10, 480af), Preheat (Mermaid Tears are distilled faster, 628af)
3:11.9 | UPGRADE_BOUGHT | Double concentrated - Bat Wing Extract profit x25 - 150af (coins 602af -> 452af)
3:12.0 | UPGRADE_SKIPPED | after the purchase GREY: Paint before shaving 480af, Preheat 628af; BLUE (affordable, not bought): Squeeze harder 11.5ae, Remake 17ae, Harvest 96ae, Rub counterclockwise 785ae, Rare species blend 1.12af, Crystal clear 1.79af, Discard first runnings 13.6af, Bigger buckets 73.1af, Wish customers would pay more 76.8af
3:12.1 | OTHER | Upgrades dialog #3 closed (coins 452af)
3:13 | STATION_LEVEL | Bat Wing Extract 626 (blue 17.4af, 1.9af/item, coins 452af)
3:14 | STATION_LEVEL | Bat Wing Extract 638; GREY (67.5af, coins 34.7af). (Level 638 was the last seen; see 3:47 for the gap.)
3:14.7 | STATION_UNLOCK | Unicorn Horn Shavings - price not seen (unlock happened between two frames; coins 34.7af at 3:14 -> 2.46ag at 3:15)
3:15 | TASK | "Unlock Unicorn Horn Shavings": rewards 20 gems (purple gem) and 360 gems (yellow tile, locked)
3:15 | OTHER | Unicorn station appears at lower left: crate and coin pile, faded Unlock/level popup fading out at the bottom left (coins 2.46ag)
3:16-3:19 | STATION_LEVEL | Unicorn Horn Shavings level ? (banner covers the level) -> 108 (3:19, 9.26T/item, price 355B, 4s); popup prices 3.03M (3:16) -> 14.8M (3:17) -> 395M (3:18) -> 355B (3:19); tags "+1 Machine" and "x2 Profit" shown 3:17-3:20
3:16-3:17 | OTHER | Purple gems fly up toward the top bar (task reward 20 gems; gem counter stays 1.68M at this display resolution, so claim not confirmable)
3:20-3:27 | STATION_LEVEL | Unicorn Horn Shavings 168 (3:20, 319T) -> 227 (3:21, 256aa) -> 290 (3:22, 322ab) -> 349 (3:23, 258ac) -> 409 (3:24, 232ad) -> 468 (3:25, 186ae) -> 531 (3:26, 234af) -> 548 (3:27); GREY at 548 (1.61ag, coins 1.26ag); tags "x2 Profit" and "+1 Machine"
3:27-3:28 | OTHER | White smoke puff at lower left beside the Unicorn station (new machine / building effect, inferred)
3:28.5 | OTHER | No popup; coins 1.26ag -> 69.3ag -> 138ag (income burst)
3:29.4 | OTHER | Upgrades dialog #4 opened (coins 138ag). Rows from the top: Host an alchemy workshop 12.5M, Put up a sign 15T, Advertise 2.25ac, Get a guild endorsement 4af (all +customers, blue), Squeeze harder 11.5ae, Remake with popular Djinn 17ae, Harvest under a double rainbow 96ae, Rub counterclockwise 785ae, Rare species blend 1.12af, Crystal clear 1.79af, Discard first runnings 13.6af, Bigger buckets 73.1af, Wish customers would pay more 76.8af, Paint before shaving 480af, Preheat 628af, Cut before grinding (Dragon Scale Dust is made faster, 1.21ag), Expand to new towns (+1 Alchemist, 1.55ag), Use venomous spiders (Spider Silk profit x2, 6.24ag), Enhanced mineral content (Purified Water profit x3, 7.14ag), Glow-in-the-Dark Formula (Beetle juice profit x4, 10.9ag), Use tears of joy (Mermaid Tears profit x5, 61.5ag), Finely powdered (Dragon Scale Dust profit x25, 121ag), Feed the spiders (Spider Silk regenerates faster, 256ag), Make Djinn brush his teeth (Djinn's Breath profit x10, 384ag)
3:30.1 | UPGRADE_BOUGHT | Squeeze harder - Beetle juice is pressed faster - 11.5ae
3:30.4 | UPGRADE_BOUGHT | Remake with popular Djinn - Djinn's Breath profit x4 - 17ae
3:30.4 | UPGRADE_BOUGHT | Harvest under a double rainbow - Unicorn Horn Shavings profit x5 - 96ae
3:30.6 | UPGRADE_BOUGHT | Rub counterclockwise - Djinn's Breath is collected faster - 785ae
3:30.6 | UPGRADE_BOUGHT | Rare species blend - Beetle juice profit x3 - 1.12af
3:31.1 | UPGRADE_BOUGHT | Crystal clear - Purified Water profit x2 - 1.79af
3:31.4 | UPGRADE_BOUGHT | Discard first runnings - Mermaid Tears profit x4 - 13.6af
3:31.6 | UPGRADE_BOUGHT | Bigger buckets - Purified Water is collected faster - 73.1af
3:31.6 | UPGRADE_BOUGHT | Wish customers would pay more - Djinn's Breath profit x5 - 76.8af
3:31.9 | UPGRADE_BOUGHT | Paint before shaving - Unicorn Horn Shavings profit x10 - 480af
3:31.9 | UPGRADE_BOUGHT | Preheat - Mermaid Tears are distilled faster - 628af
3:32.1 | UPGRADE_BOUGHT | Cut before grinding - Dragon Scale Dust is made faster - 1.21ag (Dragon time 2.8s -> 1.8s later)
3:32.4 | UPGRADE_BOUGHT | Expand to new towns - +1 Alchemist - 1.55ag
3:32.4 | UPGRADE_BOUGHT | Use venomous spiders - Spider Silk profit x2 - 6.24ag
3:32.6 | UPGRADE_BOUGHT | Enhanced mineral content - Purified Water profit x3 - 7.14ag
3:32.6 | UPGRADE_BOUGHT | Glow-in-the-Dark Formula - Beetle juice profit x4 - 10.9ag
3:32.9 | UPGRADE_BOUGHT | Use tears of joy - Mermaid Tears profit x5 - 61.5ag (coins 116ag -> 55ag)
3:33.0 | UPGRADE_SKIPPED | GREY: Finely powdered (Dragon Scale Dust profit x25) 121ag, Feed the spiders (Spider Silk regenerates faster) 256ag, Make Djinn brush his teeth (Djinn's Breath profit x10) 384ag (coins 55ag). BLUE and not bought: Host an alchemy workshop 12.5M, Put up a sign 15T, Advertise in 'Wizard Monthly' 2.25ac, Get a guild endorsement 4af
3:33.4 | OTHER | Upgrades dialog #4 closed (coins 61.9ag)
3:33.8-3:34.0 | OTHER | White smoke puff over a figure next to the cauldron (new alchemist from "Expand to new towns", inferred); coins 105ag
3:34.8 | OTHER | Upgrades dialog #5 opened (coins 105ag): list top Host/Put up a sign/Advertise/Get a guild endorsement (blue), Finely powdered 121ag, Feed the spiders 256ag, Make Djinn brush his teeth 384ag (the last three GREY)
3:35.4 | UPGRADE_SKIPPED | nothing bought in dialog #5: Finely powdered (Dragon Scale Dust profit x25) 121ag, Feed the spiders (Spider Silk regenerates faster) 256ag, Make Djinn brush his teeth (Djinn's Breath profit x10) 384ag, all GREY at 105ag; dialog closed ~3:35.4
3:35.8-3:39 | STATION_LEVEL | Dragon Scale Dust 550 (3:36.0, blue 2.52af, coins 111ag) -> 551 (3:36.25) -> 554 (3:36.5) -> 557 (3:36.75) -> 567 (3:37) -> 592 (3:38) -> 626 (3:39; bonus "x2 Profit"; price 13.9ag blue; coins 35.5ag), time per item 1.8s
3:41.0-3:42.3 | STATION_LEVEL | Unicorn Horn Shavings 548 (3:41.0, blue 1.61ag) -> 550 -> 553 -> 556 -> 560 (3:42.0) -> 561 (3:42.25, blue 7.01ag, coins 253ag); popup closed when cauldron dialog opened
3:42.4 | OTHER | Cauldron dialog opened while "Brewing... Swift Serum Lvl 4" ("All workers walk 115% faster +35%")
3:42.7 | BREW_DONE | Swift Serum Lvl 4 (Brew Complete, Claim)
3:43.0 | BREW_LIST | Swift Serum Lvl 5 (Bat 60 / Dragon 30, "walk 150% faster +35%", Brew), Sizzle Serum Lvl 1 (Dragon 12 / Unicorn 6, "make food 50% faster", Brew), Perfect Potion Lvl 1 (Bat 21 / Unicorn 9, "5% chance to make perfect food", Brew); no "Slots Full"
3:43.2 | BREW_START | Sizzle Serum Lvl 1 (red cauldron, counts above cauldron 12 Dragon Scale / 6 Unicorn Horn, frame 00224); first Sizzle Serum. Idle gap under 1 s.
3:44-3:46 | STATION_LEVEL | Unicorn Horn Shavings 561 (3:44, blue 7.01ag, coins 524ag) -> 574 (3:45, 30.6ag) -> 581 (3:46); GREY at 581 (67.6ag, coins 30.1ag); time 4s
3:47-3:50 | STATION_LEVEL | Bat Wing Extract 644 (3:47, blue 134af, 0.8s) -> 656 (3:48) -> 679 (3:49) -> 707 (3:50, bonus "x2 Profit", GREY 168ag, coins 154ag). Levels 638 (3:14) -> 644 (3:47) changed between frames without a popup seen (inferred from continued purchases).
3:53.2 | OTHER | Upgrades dialog #6 opened (coins 13.7ah). Rows seen: Host/Put up a sign/Advertise/Get a guild endorsement (blue), Finely powdered 121ag, Feed the spiders 256ag, Make Djinn brush his teeth 384ag, Soften carapace (Beetle juice is pressed faster, 503ag), Coarser grind (Unicorn Horn is shaved faster, 961ag), Remove dirt (Mystic Mushrooms profit x2, 11.5ah), Discard weak strands (Spider Silk profit x3, 25ah), Use golden Beetles (Beetle juice profit x5, 49.2ah), Filter out dust (Purified Water profit x4, 69.3ah)
3:54.1 | UPGRADE_BOUGHT | Finely powdered - Dragon Scale Dust profit x25 - 121ag
3:54.4 | UPGRADE_BOUGHT | Feed the spiders - Spider Silk regenerates faster - 256ag
3:54.4 | UPGRADE_BOUGHT | Make Djinn brush his teeth - Djinn's Breath profit x10 - 384ag
3:54.6 | UPGRADE_BOUGHT | Soften carapace - Beetle juice is pressed faster - 503ag
3:54.9 | UPGRADE_BOUGHT | Coarser grind - Unicorn Horn is shaved faster - 961ag (Unicorn time 4s -> 2.7s later)
3:54.9 | UPGRADE_BOUGHT | Remove dirt - Mystic Mushrooms profit x2 - 11.5ah (coins 13.6ah -> 1.24ah)
3:55.0 | UPGRADE_SKIPPED | GREY: Discard weak strands (Spider Silk profit x3) 25ah, Use golden Beetles (Beetle juice profit x5) 49.2ah, Filter out dust (Purified Water profit x4) 69.3ah; BLUE and not bought: Host/Put up a sign/Advertise/Get a guild endorsement (+customers)
3:55.3 | OTHER | Upgrades dialog #6 closed (coins 2.33ah)
3:55.8-4:02.3 | STATION_LEVEL | Dragon Scale Dust 626 (3:55.75, blue 13.9ag, coins 2.33ah) -> 631 (3:56) -> 646 (3:57) -> 656 (3:58; grey 415ag at coins 77.8ag) -> 658 (3:59 grey 521ag; blue at 4:00, coins 46.9ah) -> 665 (4:01.0) -> 669 -> 673 -> 677 (4:01.75) -> 680 (4:02.0); GREY at 680 (6.3ah, coins 3.1ah), time 1.8s
4:02.4 | OTHER | Cauldron dialog opened; top-center round icon above the shop door turns grey at 4:02 (green before; meaning unknown, stays grey to 5:19)
4:02.6 | BREW_DONE | Sizzle Serum Lvl 1 ("All workers make food 50% faster"), Claim tapped
4:02.8 | BREW_LIST | Swift Serum Lvl 5 (60 / 30), Sizzle Serum Lvl 2 (Dragon 18 / Unicorn 9, "make food 50% faster +85%"), Perfect Potion Lvl 1 (21 / 9); no "Slots Full"
4:03.0 | BREW_START | Sizzle Serum Lvl 2 (red, counts 18 Dragon Scale / 9 Unicorn Horn, frame 00244); dialog shows "Brewing... Sizzle Serum Lvl 2" while closing
4:04-4:06 | STATION_LEVEL | Bat Wing Extract 709 (4:04, blue 211ag, coins 662ah) -> 716 (4:05.0) -> 720 -> 723 -> 728 -> 732 (4:06.0) -> 733 (4:06.25, blue 3.2ah, coins 638ah); popup left open while Upgrades opens
4:06.4 | OTHER | Upgrades dialog #7 opened (coins 638ah). Rows: Host/Put up a sign/Advertise/Get a guild endorsement (blue), Discard weak strands 25ah, Use golden Beetles 49.2ah, Filter out dust 69.3ah, Include certificate (Unicorn Horn Shavings profit x25, 96ah), Genuine tears (Mermaid Tears profit x10, 308ah), Enhance the substrate (Mystic Mushrooms grow faster, 468ah), Don't rub, just knock (Djinn's Breath is collected faster, 769ah), Filtered through Vampire ash (Bat Wing Extract profit x50, 1ai), Guarantee efficacy (+1 Customer, 3ai)
4:07.4 | UPGRADE_BOUGHT | Discard weak strands - Spider Silk profit x3 - 25ah
4:07.6 | UPGRADE_BOUGHT | Use golden Beetles - Beetle juice profit x5 - 49.2ah
4:07.6 | UPGRADE_BOUGHT | Filter out dust - Purified Water profit x4 - 69.3ah
4:07.9 | UPGRADE_BOUGHT | Include certificate - Unicorn Horn Shavings profit x25 - 96ah
4:08.1 | UPGRADE_BOUGHT | Genuine tears - Mermaid Tears profit x10 - 308ah (coins 638ah -> 91.4ah)
4:08.3 | UPGRADE_SKIPPED | GREY (not affordable at ~91ah): Enhance the substrate (Mystic Mushrooms grow faster) 468ah, Don't rub, just knock (Djinn's Breath is collected faster) 769ah, Filtered through Vampire ash (Bat Wing Extract profit x50) 1ai, Guarantee efficacy (+1 Customer) 3ai; BLUE not bought: Host/Put up a sign/Advertise/Get a guild endorsement
4:08.6 | OTHER | Upgrades dialog #7 closed; Bat Wing popup (Level 733, 3.2ah blue) still shown at 4:08.75, gone by 4:09.25
4:09-4:12 | STATION_LEVEL | Unicorn Horn Shavings 581 (4:09.25, blue 67.6ag, 2.7s, coins 91.8ah) -> 582 (4:09.5) -> 585 (4:09.75) -> 593 (4:10) -> 613 (4:11, bonus "x2 Profit", 2.54ah blue) -> 626 (4:12, GREY 11.1ah, coins 9.25ah)
4:13-4:14 | OTHER | No popup; coins 16.1ah
4:15 | STATION_LEVEL | Unicorn Horn Shavings 626 (blue 11.1ah, coins 16.1ah)
4:16-4:17 | STATION_LEVEL | Unicorn Horn Shavings 627 (4:16, GREY 12.5ah, coins 5.08ah) -> 630 (4:17, GREY 17.5ah, coins 9.93ah) = stopped for money
4:19-4:21 | STATION_LEVEL | Bat Wing Extract 733 (4:19, blue 3.2ah, coins 652ah) -> 746 (4:20, 14ah) -> 761 (4:21, GREY 76.4ah, coins 49.6ah)
4:22 | OTHER | Coins 852ah -> 4.66ai at 4:22.25 (income burst); no popup
4:22.8 | OTHER | Cauldron dialog opened (Brew Complete shown from 4:23.0)
4:23.0 | BREW_DONE | Sizzle Serum Lvl 2 (Brew Complete, Claim)
4:23.5 | BREW_LIST | Swift Serum Lvl 5 (60 / 30), Sizzle Serum Lvl 3 (Dragon 27 / Unicorn 13, "make food 135% faster +80%"), Perfect Potion Lvl 1 (21 / 9); no "Slots Full"
4:23.7 | BREW_START | Sizzle Serum Lvl 3 (red, counts 27 Dragon Scale / 13 Unicorn Horn, frame 00267)
4:24.2 | OTHER | Upgrades dialog #8 opened (coins 4.75ai). Rows: Host/Put up a sign/Advertise/Get a guild endorsement (blue), Enhance the substrate 468ah, Don't rub, just knock 769ah, Filtered through Vampire ash 1ai, Guarantee efficacy 3ai, Drill into ceiling (Purified Water is collected faster, 3.22ai), Hire Jax's mentor (+1 Alchemist, 15.5ai), Send through amplifier (Frog Scream profit x2, 17.2ai)
4:24.9 | UPGRADE_BOUGHT | Enhance the substrate - Mystic Mushrooms grow faster - 468ah
4:24.9 | UPGRADE_BOUGHT | Don't rub, just knock - Djinn's Breath is collected faster - 769ah
4:25.1 | UPGRADE_BOUGHT | Filtered through Vampire ash - Bat Wing Extract profit x50 - 1ai (coins 4.75ai -> 2.52ai)
4:25.5 | UPGRADE_SKIPPED | Guarantee efficacy (+1 Customer) 3ai and Drill into ceiling (Purified Water is collected faster) 3.22ai were BLUE at coins 3.45ai and not bought; Hire Jax's mentor (+1 Alchemist) 15.5ai and Send through amplifier (Frog Scream profit x2) 17.2ai GREY
4:26.1 | OTHER | Upgrades dialog #8 closed (coins 3.45ai)
4:27-4:29 | STATION_LEVEL | Bat Wing Extract 766 (4:27, 135ah, coins 11.3ai) -> 779 (4:28, 588ah) -> 789 (4:29; GREY 1.83ai, coins 740ah)
4:31 | STATION_LEVEL | Bat Wing Extract 793 (blue 2.87ai, coins 35.6ai)
4:32 | STATION_LEVEL | Bat Wing Extract 801 (bonus "x2 Profit", 1 star again; GREY 7.11ai, coins 355ah)
4:33-4:36 | OTHER | No popup; cauldron red (Sizzle Serum Lvl 3, counts fall); coins 355ah -> 448ah
4:37-4:40 | STATION_LEVEL | Dragon Scale Dust 680 (4:37, blue 6.3ah, coins 1.29aj) -> 692 (4:38, 24.6ah) -> 712 (4:39, bonus "x2 Profit", 237ah) -> 763 (4:40, 5 stars, price 76.7ai blue, coins 789ai)
4:41-4:48 | STATION_LEVEL | Bat Wing Extract 801 (4:41, blue 7.11ai, coins 1.31aj) -> 809 (4:42) -> 825 (4:43) -> 834 (4:44, GREY 300ai, coins 206ai) -> 835 (4:45, 335ai) -> 836 (4:47, 376ai) -> 843 (4:48.0, 830ai) -> 847 (4:48.25) -> 851 (4:48.5) -> 853 (4:48.75, blue 2.58aj, coins 2.98aj)
4:49.0 | OTHER | Cauldron dialog opened
4:49.0 | BREW_DONE | Sizzle Serum Lvl 3 ("All workers make food 135% faster +80%"), Claim
4:49.3 | BREW_LIST | Swift Serum Lvl 5 (60 / 30), Sizzle Serum Lvl 4 (Dragon 40 / Unicorn 20, "make food 215% faster +85%"), Perfect Potion Lvl 1 (21 / 9); no "Slots Full"
4:49.6 | BREW_START | Sizzle Serum Lvl 4 (red, counts 40 Dragon Scale / 20 Unicorn Horn, frame 00291)
4:51-4:52 | STATION_LEVEL | Bat Wing Extract 853 (4:51, blue 2.58aj, coins 81.4ai) -> 857 (4:52.0, 4.06aj) -> 861 (4:52.25) -> 865 (4:52.5) -> 867 (4:52.75; GREY 12.6aj, coins 12.1aj); popup stays until the Upgrades dialog opens
4:53.4 | OTHER | Upgrades dialog #9 opened (coins 12.1aj). Rows: Host/Put up a sign/Advertise/Get a guild endorsement (blue), Guarantee efficacy (+1 Customer, 3ai), Drill into ceiling 3.22ai, Hire Jax's mentor 15.5ai, Send through amplifier 17.2ai, Hand-picked selection (Mystic Mushrooms profit x3, 45.7ai), Sell as limited edition (Djinn's Breath profit x25, 76.9ai), Higher thread count (Spider Silk profit x4, 243ai), Remove shell fragments (Beetle juice profit x10, 246ai), Label as 'Gravity Perfected' (Purified Water profit x5, 315ai), Pull a vacuum (Mermaid Tears are distilled faster, 615ai), Warm-up ribbits (Frogs recover faster, 702ai), Sourced from Elder Dragons (Dragon Scale Dust profit x50, 800ai), Speedy spooling technique (Spider Silk regenerates faster, 11.3aj), Double distilled (Mermaid Tears profit x25, 61.5aj), Apply distortion (Frog Scream profit x3, 68.5aj), Label as 'Wizard's Choice' (price partly hidden, about 444aj)
4:54.1 | UPGRADE_BOUGHT | Drill into ceiling - Purified Water is collected faster - 3.22ai
4:54.4 | UPGRADE_BOUGHT | Hire Jax's mentor - +1 Alchemist - 15.5ai
4:54.4 | UPGRADE_BOUGHT | Send through amplifier - Frog Scream profit x2 - 17.2ai
4:54.6 | UPGRADE_BOUGHT | Hand-picked selection - Mystic Mushrooms profit x3 - 45.7ai
4:54.6 | UPGRADE_BOUGHT | Sell as limited edition - Djinn's Breath profit x25 - 76.9ai
4:54.9 | UPGRADE_BOUGHT | Higher thread count - Spider Silk profit x4 - 243ai
4:54.9 | UPGRADE_BOUGHT | Remove shell fragments - Beetle juice profit x10 - 246ai
4:55.1 | UPGRADE_BOUGHT | Label as 'Gravity Perfected' - Purified Water profit x5 - 315ai
4:55.4 | UPGRADE_BOUGHT | Pull a vacuum - Mermaid Tears are distilled faster - 615ai
4:55.4 | UPGRADE_BOUGHT | Warm-up ribbits - Frogs recover faster - 702ai
4:55.6 | UPGRADE_BOUGHT | Sourced from Elder Dragons - Dragon Scale Dust profit x50 - 800ai (coins 12.1aj -> 9.1aj)
4:55.8 | UPGRADE_SKIPPED | GREY: Speedy spooling technique (Spider Silk regenerates faster) 11.3aj, Double distilled (Mermaid Tears profit x25) 61.5aj, Apply distortion (Frog Scream profit x3) 68.5aj, Label as 'Wizard's Choice' about 444aj (?); BLUE not bought: Guarantee efficacy (+1 Customer) 3ai and the four other +customer rows
4:56.0 | OTHER | Upgrades dialog #9 closed (coins 9.1aj); Bat Wing popup (867, grey 12.6aj) fades at 4:56.0-4:56.25
4:56.5 | OTHER | White smoke puff above the cauldron area (new alchemist from "Hire Jax's mentor", inferred)
4:57-5:00 | STATION_LEVEL | Dragon Scale Dust 770 (4:57, 170ai, coins 330aj) -> 781 (4:58, 590ai) -> 800 (4:59, 1 star, 5.08aj blue) -> 819 (5:00, bonus "x2 Profit", GREY 43.8aj, coins 30.4aj). Levels 763 (4:40) -> 770 (4:57) changed without a popup seen.
5:01 | STATION_UNLOCK | Mermaid Tears - price not seen (bought between 5:00 and 5:01; coins 30.4aj at both). First popup at 5:01 (faded): Level 1, price 1.22T, time 5.3s; banner "Unlock Mermaid Tears" slides in from the right.
5:01-5:02 | TASK | "Unlock Mermaid Tears": rewards "5" and "10" (brown vial/cup icons, "10" yellow and locked); green check shown 5:03; banner fades ~5:04
5:02-5:14 | STATION_LEVEL | Mermaid Tears 5 (5:02, 1.94T, coins 51.2aj) -> 20 (5:03, 10.6T, "x2 Profit") -> 52 (5:04, 398T) -> 111 (5:05, 319aa; "+1 Machine" + "x2 Profit") -> 171 (5:06, 287ab) -> 230 (5:07, 230ac) -> 292 (5:08, 259ad) -> 352 (5:09, 232ae) -> 411 (5:10, 186af) -> 471 (5:11, 167ag) -> 533 (5:12, 188ah) -> 593 (5:13, 169ai) -> 650 (5:14, GREY 108aj, coins 106aj); time 5.3s per item
5:12-5:14 | TASK | "Upgrade Mermaid Tears to level 500": rewards "25" and "25" (second locked); banner appears 5:12, green check on the first reward from 5:13
5:15 | OTHER | Station popup gone; white smoke cloud and a crate at the bottom center of the floor (Mermaid station machines being built, inferred); coins 126aj
5:16-5:19 | OTHER | Mermaid station now shows several small machines/workers at the bottom center (6 small units at 5:19); coins 4.19ak (5:16) -> 6.3ak -> 4.62ak (5:19)
5:17-5:19 | STATION_LEVEL | Bat Wing Extract 867 (5:17, blue 12.6aj, coins 6.3ak) -> 875 (5:18, 31.2aj) -> 892 (5:19, blue 214aj, coins 4.62ak); still climbing at chunk end
5:19 | OTHER | Cauldron red, Sizzle Serum Lvl 4 brewing: Unicorn count above cauldron 2 (Dragon count hidden by the popup); no potion bottled, no Boost click, no offers used
```

### Chunk 3 of 8: video 5:20 .. 7:59 (seconds 320..479)

```
Notes on reading: base sheets are 1 fps, so station levels are samples
(levels in between were passed). Times with decimals come from the dialog
sheets (4 fps, +-0.25 s). "grey" = price button grey (not affordable).
Coins are in letters (aj < ak < al < am < an < ao < ap).
5:20.0 | STATION_LEVEL | Bat Wing 903 (continues 867 -> 892 of the previous chunk); Bonus x2 Profit tag; price 745aj grey (coins 204aj) = stopped for money
5:20.5 | OTHER | Coins jump 204aj -> 868aj (coin shower), no purchase
5:21.0 | OTHER | Cauldron button tapped; Cauldron dialog opens at ~5:21.2 (cauldron was red = Sizzle Serum)
5:21.25-5:21.5 | BREW_DONE | Sizzle Serum Lvl 4 ("Brew Complete!", Claim tapped ~5:21.6)
5:21.75-5:22.25 | BREW_LIST | Swift Serum Lvl 5 (Bat Wing 60 + Dragon Scale 30); Sizzle Serum Lvl 5 (Dragon Scale 60 + Unicorn 30); Perfect Potion Lvl 1 (Bat Wing 21 + Unicorn 9); Double Draught Lvl 1 (Mermaid 12 + Dragon Scale 9); all Brew buttons blue, no "Slots Full". Only these 4 potions listed.
5:22.4 | BREW_START | Double Draught (pink) Lvl 1, costs from list Mermaid 12 + Dragon 9 (tapped Brew on the 4th row); cauldron pink from 5:22.5, counts above cauldron "12" + one more icon (unreadable)
5:22.5 | OTHER | Dialog closes; coins 1.07ak
5:23.75 | OTHER | Upgrades dialog opened (1st of 7 in this chunk)
5:24.0-5:26.0 | UPGRADE_BOUGHT | Order inferred from rows disappearing (the same quarter-second frame for pairs); coins 30.5ak -> 5.63ak
5:24.5-5:24.75 | UPGRADE_BOUGHT | Speedy spooling technique (Spider Silk regenerates faster) 11.3aj
5:24.75-5:25.0 | UPGRADE_BOUGHT | Double distilled (Mermaid Tears profit x25) 61.5aj
5:24.75-5:25.0 | UPGRADE_BOUGHT | Apply distortion (Frog Scream profit x3) 68.5aj
5:25.0-5:25.25 | UPGRADE_BOUGHT | Label as 'Wizard's Choice' (Mystic Mushrooms profit x4) 444aj
5:25.0-5:25.25 | UPGRADE_BOUGHT | Macerate before pressing (Beetle Juice is pressed faster) 492aj
5:25.25-5:25.5 | UPGRADE_BOUGHT | Mix with glitter (Unicorn Horn Shavings profit x50) 640aj
5:25.5-5:25.75 | UPGRADE_BOUGHT | Anti-stick coating (Spider Silk profit x5) 1.11ak
5:25.5-5:25.75 | UPGRADE_BOUGHT | Crystal clear (Purified Water profit x10) 1.58ak
5:25.75-5:26.0 | UPGRADE_BOUGHT | Dry with hot air (Mystic Mushrooms grow faster) 20.6ak
5:24.0-5:26.0 | UPGRADE_SKIPPED | "+1 Customer" rows, all blue (affordable) but never bought in the whole chunk: Guarantee efficacy +1 Customer 3ai; Get a guild endorsement +1 Customer 4af; Host an alchemy workshop +2 Customers 12.5M; Put up a sign +1 Customer 15T; Advertise in 'Wizard Monthly' +2 Customers 2.25ac (the same rows are seen blue in every Upgrades dialog; coins were always far above these prices)
5:25.75-5:26.0 | UPGRADE_SKIPPED | Rare species blend (Beetle Juice profit x25) 49.2ak grey; Use Transilvanian Bats (Bat Wing Extract profit x75) 75.1ak grey; Lure talent from rivals (+1 Alchemist) 130ak grey (coins 26.2ak)
5:26.0-5:26.25 | OTHER | Upgrades dialog closes; coins 5.63ak
5:26.5-5:27 | STATION_LEVEL | Unicorn Horn 632 (21.9ah, blue)
5:27-5:34 | STATION_LEVEL | Unicorn Horn 638 (5:27) -> 654 (5:28) -> 690 (5:29) -> 749 (5:30, Bonus x2 Profit tag) -> 786 (5:31-5:32, tag; price 831aj grey at 5:31 then blue at 5:32) -> 797 (5:33) -> 806 (5:34, grey 8.02ak, tag x2 Profit, 1-star bar) = stopped for money (coins 4.8ak)
5:35.0 | OTHER | Coins 87.2ak
5:35.4 | OTHER | Upgrades dialog opened (2nd)
5:35.75-5:36.25 | UPGRADE_SKIPPED | Visible rows at 5:35.75 (blue unless noted): Rare species blend (Beetle profit x25) 49.2ak blue (coins 87.2ak); Use Transilvanian Bats (Bat Wing profit x75) 75.1ak blue; Lure talent from rivals (+1 Alchemist) 130ak grey; Remake with popular Djinn (Djinn's Breath profit x50) 512ak grey; Shift one octave up (Frog Scream profit x4) 665ak grey
5:36.25-5:36.5 | UPGRADE_BOUGHT | Use Transilvanian Bats (Bat Wing Extract profit x75) 75.1ak (coins 87.2ak -> 12.2ak). Rare species blend 49.2ak (affordable before) was NOT bought; the most expensive affordable row was taken.
5:36.5-5:36.75 | OTHER | Upgrades dialog closes (fading), coins 12.2ak
5:37.0-5:37.75 | STATION_LEVEL | Bat Wing 903 (745aj blue) -> 905 (934aj) -> 908 (1.32ak); base frame 5:37 shows 904 (834aj)
5:38.0-5:38.5 | BREW_DONE | Double Draught Lvl 1 (Claim tapped ~5:38.6)
5:38.75-5:39.0 | BREW_LIST | Swift Serum Lvl 5 (Bat Wing 60 + Dragon 30); Sizzle Serum Lvl 5 (Dragon 60 + Unicorn 30); Double Draught Lvl 2 (Mermaid ~16 + Dragon 13); Perfect Potion Lvl 1 (Bat Wing 21 + Unicorn 9). No "Slots Full". Order of rows changed: Double Draught moved to the 3rd row.
5:39.1 | BREW_START | Double Draught Lvl 2 (pink), counts above the cauldron ~16 / 13 at 5:39.25-5:40 (decreasing: 13 / 10 at 5:45)
5:39.25 | OTHER | Dialog closed; coins 237ak
5:40-5:49 | STATION_LEVEL | Bat Wing 909 (5:40, 1.47ak blue) -> 921 (5:41) -> 943 (5:42, 69.3ak) -> 960 (5:43, 476ak grey) -> 974 (5:44, 2.33al grey) -> 980 (5:46, 4.59al grey) -> 984 (5:48, 7.22al blue) -> 992 (5:49, 17.9al grey, coins 9.91al). Stopped for money at grey prices several times
5:52.1 | OTHER | Upgrades dialog opened (3rd); coins 57al
5:53.0-5:55.0 | UPGRADE_BOUGHT | Order inferred; coins 150al -> 48.1al
5:53.25-5:53.5 | UPGRADE_BOUGHT | Rare species blend (Beetle Juice profit x25) 49.2ak
5:53.25-5:53.5 | UPGRADE_BOUGHT | Lure talent from rivals (+1 Alchemist) 130ak
5:53.5-5:53.75 | UPGRADE_BOUGHT | Remake with popular Djinn (Djinn's Breath profit x50) 512ak
5:53.5-5:53.75 | UPGRADE_BOUGHT | Shift one octave up (Frog Scream profit x4) 665ak
5:53.75-5:54.0 | UPGRADE_BOUGHT | Sell as 'Elixir-Grade' (Mystic Mushrooms profit x5) 2.02al
5:54.0-5:54.25 | UPGRADE_BOUGHT | Loosen the soil (Purified Water is collected faster) 3.15al
5:54.0-5:54.25 | UPGRADE_BOUGHT | Use venomous spiders (Spider Silk profit x10) 5.51al
5:54.5-5:54.75 | UPGRADE_BOUGHT | Poke gently (Frogs recover faster) 30.9al
5:54.75-5:55.0 | UPGRADE_BOUGHT | Add rubys for color (Dragon Scale Dust profit x75) 60al
5:52.1-5:55.4 | UPGRADE_SKIPPED | +1 Customer rows blue, not bought: Get a guild endorsement 4af; Guarantee efficacy 3ai; Sponsor a local festival 6.4al (also blue, affordable)
5:54.75-5:55.25 | UPGRADE_SKIPPED | Enhanced mineral content (Purified Water profit x25) 315al grey (coins 108al->48.1al); Discard first runnings (Mermaid Tears profit x50) 410al grey
5:55.4 | OTHER | Upgrades dialog closes; coins 48.1al; white smoke around the cauldron at 5:55.75 and a crate above it
5:55.75-5:56 | BREW_DONE | Double Draught Lvl 2 (inferred: smoke, counts above cauldron disappear at 5:56; no Cauldron dialog was captured)
5:56-5:57 | BREW_START | Double Draught Lvl 3 (inferred; counts 27 + 20 above the cauldron at 5:57-5:58, cauldron pink). No Cauldron dialog was seen, so the cauldron seems to restart the same potion by itself here
5:58-6:06 | STATION_LEVEL | Dragon Scale Dust 819 (5:58, 43.8aj) -> 829 (5:59) -> 849 (6:00, 1.31ak) -> 896 (6:01, 270ak) -> 956 (6:02, 242al, Bonus x2 Profit tag) -> 959 (6:03-6:06, grey 340al, tag shown 6:03-6:04) = stopped for money
6:07-6:08 | STATION_LEVEL | Unicorn Horn 807 (6:07, 8.98ak) -> 819 (6:08, 35ak)
6:09-6:15 | STATION_LEVEL | Dragon Scale 962 (6:09, 478al blue) -> 974 (6:10-6:11, grey 1.86am) -> 976 (6:14, 2.34am blue) -> 986 (6:15, grey 7.25am)
6:12 | STATION_LEVEL | Bat Wing 994 (22.5al blue; coins 1.65am), 114ak ingredient column
6:16.4 | OTHER | Upgrades dialog opened (4th); coins 89.5am
6:17.25-6:18.25 | UPGRADE_BOUGHT | Order inferred; coins 89.5am -> 16.7am
6:17.25-6:17.5 | UPGRADE_BOUGHT | Enhanced mineral content (Purified Water profit x25) 315al
6:17.5-6:17.75 | UPGRADE_BOUGHT | Discard first runnings (Mermaid Tears profit x50) 410al
6:17.5-6:17.75 | UPGRADE_BOUGHT | Layer with tritone (Frog Scream profit x5) 3.02am
6:17.75-6:18.0 | UPGRADE_BOUGHT | Remove dirt (Mystic Mushrooms profit x10) 10.1am
6:17.75-6:18.0 | UPGRADE_BOUGHT | Selective spider breeding (Spider Silk regenerates faster) 11.1am
6:18.0-6:18.25 | UPGRADE_BOUGHT | Harvest under a double rainbow (Unicorn Horn Shavings profit x75) 48am
6:18.25-6:18.5 | UPGRADE_SKIPPED | Glow-in-the-Dark Formula (Beetle Juice profit x50) 328am grey; Discard weak strands (Spider Silk profit x25) 1.11an grey; Post job notices (+1 Alchemist) 4.15an grey; and +1 Customer rows Guarantee efficacy 3ai, Sponsor a local festival 6.4al blue (not bought)
6:18.75 | OTHER | Upgrades dialog closed
6:19.25-6:19.5 | BREW_DONE | Double Draught Lvl 3 ("Brew Complete!", Claim at ~6:19.5)
6:19.5 | BREW_LIST | Swift Serum Lvl 5 (60/30); Sizzle Serum Lvl 5 (60/30); Double Draught Lvl 4 (Mermaid 40 + Dragon 30); Perfect Potion Lvl 1 (21/9). Row order: Swift, Sizzle, Double Draught, Perfect.
6:19.6 | BREW_START | Double Draught Lvl 4 (Mermaid 40 + Dragon 30; counts "40 / 30" above the cauldron from 6:20)
6:20-6:21 | OTHER | Coins 368am -> 392am; Unicorn popup 6:20.75 L819 (51.6ak 2.7s, 35ak blue)
6:21-6:27 | STATION_LEVEL | Unicorn Horn 823 (6:21, 55.1ak) -> 839 (6:22, 338ak) -> 870 (6:23, 11.4al) -> 932 (6:24, 12.8am, Bonus x2 Profit tag) -> 943 (6:26, 44.4am) -> 948 (6:27, grey 78.2am) = stopped for money
6:28-6:33 | STATION_LEVEL | Mermaid Tears 654 (6:28, 170aj) -> 667 (6:29, 740aj) -> 692 (6:30, 12.6ak) -> 751 (6:31, 10.1al, Bonus x2 Profit tag) -> 810 (6:32, 8.07am blue, tag) -> 846 (6:33, grey 478am, tag) = stopped for money
6:34-6:37 | STATION_LEVEL | Dragon Scale 991 (6:34, 12.8am) -> 997 (6:35, grey 25.2am) -> 998 (6:37, 28.3am blue)
6:38-6:45 | STATION_LEVEL | Unicorn Horn 949 (6:38, 87.5am blue) -> 962 (6:39, 382am) -> 969 (6:40, grey 845am) -> 972 (6:41, 1.19an blue) -> 976 (6:42, grey 1.87an) -> 982 (6:45, 3.69an blue)
6:47.75 | OTHER | Cauldron dialog open: "Brewing..." Double Draught Lvl 4 (1 icon left)
6:48.0-6:48.25 | BREW_DONE | Double Draught Lvl 4 (Claim at ~6:48.4)
6:48.5 | BREW_LIST | Swift Serum Lvl 5 (Bat Wing 60 + Dragon 30); Sizzle Serum Lvl 5 (60/30); Double Draught Lvl 5 (Mermaid 60 + Dragon 45, "40% chance +10%"); Perfect Potion Lvl 1 (Bat Wing 21 + Unicorn 9). Coins 21.4an.
6:48.6 | BREW_START | Swift Serum (dark blue) Lvl 5, counts "60 / 30" (Bat Wing / Dragon Scale) above cauldron from 6:49. Potion switched from Double Draught to Swift Serum.
6:49.25 | OTHER | Coins 137an -> 254an (coin shower)
6:50-6:51 | STATION_LEVEL | Unicorn Horn 985 (6:50-6:52 popup, 5.18an blue, coins 254an)
6:50.4 | OTHER | Upgrades dialog opened (5th)
6:50.75-6:52.0 | UPGRADE_BOUGHT | Order inferred; coins 254an -> 174an
6:51.0-6:51.25 | UPGRADE_BOUGHT | Glow-in-the-Dark Formula (Beetle Juice profit x50) 328am
6:51.0-6:51.25 | UPGRADE_BOUGHT | Discard weak strands (Spider Silk profit x25) 1.11an
6:51.25-6:51.5 | UPGRADE_BOUGHT | Post job notices (+1 Alchemist) 4.15an
6:51.25-6:51.5 | UPGRADE_BOUGHT | Send through amplifier (Frog Scream profit x10) 15.1an
6:51.5-6:51.75 | UPGRADE_BOUGHT | Control air humidity (Mystic Mushrooms grow faster) 20.2an
6:51.75-6:52.0 | UPGRADE_BOUGHT | Wish customers would pay more (Djinn's Breath profit x75) 38.4an
6:52.0-6:52.25 | UPGRADE_SKIPPED | Hand-picked selection (Mystic Mushrooms profit x25) 2.02ao grey; Filter out dust (Purified Water profit x50) 2.1ao grey; Honey & lemon soak (Frogs recover faster) 30.3ao grey; +1 Customer rows Guarantee efficacy 3ai and Sponsor a local festival 6.4al blue, not bought
6:52.4 | OTHER | Upgrades dialog closes
6:52.7-6:53.5 | OTHER | Upgrades dialog opened again (6:52.75) and closed (~6:53.5) with nothing bought: only the top rows were shown (Host an alchemy workshop 12.5M, Put up a sign 15T, Advertise in 'Wizard Monthly' 2.25ac, Get a guild endorsement 4af, Guarantee efficacy 3ai, Sponsor a local festival 6.4al, all blue); coins 174an
6:54-6:55 | STATION_LEVEL | Unicorn Horn 985 (6:53.75-6:54.75 popup, 5.18an blue) -> 992 (6:55, 62.6am, 11.5an blue)
6:56 | STATION_LEVEL | Unicorn Horn 1000 = MAX (popup "MAX" grey, Bonus x2 Profit tag); coins 75.1an
6:56-6:58 | TASK | "Upgrade Unicorn Horn Shavings to level 1000": reward 200 gems (second reward 3.6K gems with a lock, not claimable); done (green check at ~6:58); purple gem shower 6:56.5-6:57.5; gems display stays 1.68M
6:56.8 | STATION_UNLOCK | Djinn's Breath (6th shop station; the dashed tile at right, shown at 6:56, became a lamp station at 6:57). Unlock popup / price NOT captured; coins show no drop (75.1an at 6:56 -> 158an at 6:57)
6:57-7:09 | STATION_LEVEL | Djinn's Breath 1 (6:57, 1.54B blue) -> 11 (6:58, 4.78B) -> 31 (6:59, 46.1B, tags +1 Machine and x2 Profit) -> 80 (7:00, 11.9T) -> 139 (7:01, 9.52aa) -> 199 (7:02, 8.55ab) -> 261 (7:03, 9.62ac) -> 320 (7:04, 7.71ad) -> 382 (7:05, 8.68ae) -> 439 (7:06, 5.55af) -> 501 (7:07, 6.25ag); +1 Machine / x2 Profit tags seen 6:58-7:07; time per item 4s
7:07-7:09 | TASK | "Upgrade Djinn's Breath to level 500": reward 10 (parchment/scroll-like icon; second reward 20 locked); done (green check at 7:09)
7:10-7:11 | VIEW | Camera slightly scrolled down (shop floor, bottom crates and barrel visible) from about 7:10.5; still the shop, cellar never shown
7:10.0-7:10.5 | BREW_DONE | Swift Serum Lvl 5 (Cauldron dialog opened 7:10.2, Claim at ~7:10.5)
7:10.75 | BREW_START | (inferred) Swift Serum again; the dialog closes with "Brewing..." (the list was not captured in the 0.25 s gap); cauldron dark blue with counts 91 + 45 (Bat Wing / Dragon Scale) at 7:11.25-7:11.75, i.e. Swift Serum Lvl 6
7:12-7:19 | STATION_LEVEL | Djinn's Breath 527 (7:12, 119ag) -> 535 (7:13) -> 552 (7:14, 2.03ah) -> 596 (7:15, 296ah) -> 656 (7:16, 266ai, Bonus x2 Profit tag) -> 716 (7:17, 239aj) -> 775 (7:18, 192ak) -> 839 (7:19, 241al, tag)
7:20-7:24 | STATION_LEVEL | Djinn's Breath 897 (7:20, 194am, tag) -> 956 (7:21, 155an) -> 960 (7:23, 244an blue) -> 963 (7:24, grey 343an)
7:28-7:30 | STATION_LEVEL | Djinn's Breath 964 (grey 384an, shown 7:28, 7:29, 7:30; coins 199an-203an) = stopped for money
7:34.0-7:34.5 | STATION_LEVEL | Djinn's Breath 966 (7:34.0, 481an) -> 969 (7:34.25, 676an) -> 972 (7:34.5, 949an) blue (base frame shows 970 / 757an)
7:35.0 | OTHER | Cauldron dialog opens (fading in), "Brewing..." Swift Serum Lvl 6 (185% faster +30%), 1 Bat Wing left; shown 7:35.0-7:36.0
7:36.25 | BREW_DONE | (inferred) Swift Serum Lvl 6 completed; no "Brew Complete" frame in 7:36.0-7:36.25 (claimed in under 0.25 s)
7:36.25 | BREW_LIST | Swift Serum Lvl 7 (Bat Wing 136 + Dragon Scale 68, "215% faster +35%"); Sizzle Serum Lvl 5 (Dragon 60 + Unicorn 30); Double Draught Lvl 5 (Mermaid 60 + Dragon 45); Perfect Potion Lvl 1 (Bat Wing 21 + Unicorn 9); NEW Instant Infusion Lvl 1 (cyan; Djinn's Breath 21 + Unicorn 12; "5% chance to make food instantly"); NEW Telepathic Tincture Lvl 1 (violet; Djinn's Breath 15 + Dragon Scale 9; "10% chance customers order instantly"). 6 rows, no Slots Full. The two new potions appeared after Djinn's Breath was unlocked.
7:36.4 | BREW_START | Swift Serum Lvl 7 (Bat Wing 136 + Dragon Scale 68; card in the faded dialog at 7:36.5 shows "1 / 136 / 68"); cauldron dark blue
7:38-7:42 | STATION_LEVEL | Djinn's Breath 977 (7:38, 1.68ao blue) -> 986 (7:39, 4.64ao grey) -> 986 (7:40, blue) -> 993 (7:41, 10.3ao grey; also grey at 7:42 coins 10ao) = stopped for money
7:45-7:49 | STATION_LEVEL | Djinn's Breath 993 (7:45, 10.3ao blue, coins 10.3ao; bought: coins drop to 87.7an at 7:46) -> 994 (7:49.0, 11.5ao) -> 996 (7:49.25, 14.4ao) -> 998 (7:49.5, grey 18.1ao)
7:49.9 | OTHER | Upgrades dialog opened (6th); coins 60.1ao
7:51.0-7:51.25 | UPGRADE_BOUGHT | Order inferred; coins 60.1ao -> 25.8ao
7:50.75-7:51.0 | UPGRADE_BOUGHT | Hand-picked selection (Mystic Mushrooms profit x25) 2.02ao
7:51.0-7:51.25 | UPGRADE_BOUGHT | Filter out dust (Purified Water profit x50) 2.1ao
7:51.0-7:51.25 | UPGRADE_BOUGHT | Honey & lemon soak (Frogs recover faster) 30.3ao
7:51.25-7:51.75 | UPGRADE_SKIPPED | Use tears of joy (Mermaid Tears profit x75) 30.8ao grey (coins 25.8ao); Apply distortion (Frog Scream profit x25) 3.02ap grey; Higher thread count (Spider Silk profit x50) 7.35ap grey; Use golden Beetles (Beetle Juice profit x75) 24.6ap grey; +1 Customer rows Sponsor a local festival 6.4al blue (and others) not bought
7:51.7 | OTHER | Upgrades dialog closes (fading)
7:54 | STATION_LEVEL | Djinn's Breath 999 (20.3ao grey, coins 7.74ao)
7:57.0 | STATION_LEVEL | Djinn's Breath 1000 = MAX (faded popup "Level 1000 ... MAX, x2 Profit tag" fading out at 7:57.0, i.e. reached ~7:56)
7:57.9 | OTHER | Upgrades dialog opened (7th); coins 294ao
7:58.25-7:58.75 | UPGRADE_BOUGHT | Use tears of joy (Mermaid Tears profit x75) 30.8ao (coins 294ao -> 263ao; row gone at 7:58.75)
7:58.75-7:59.0 | UPGRADE_SKIPPED | Apply distortion (Frog Scream profit x25) 3.02ap grey; Higher thread count (Spider Silk profit x50) 7.35ap grey; Use golden Beetles (Beetle Juice profit x75) 24.6ap grey; Guarantee efficacy 3ai and Sponsor a local festival 6.4al blue, not bought
7:59.0 | OTHER | Upgrades dialog closes; coins 263ao
7:59.25-7:59.75 | STATION_LEVEL | Mermaid Tears 846 (7:59.25-7:59.5, 478am blue, 264am ingredient column, 5.3s) -> 848 (7:59.75, 599am)
7:59.75 | BREW_START | (state, not an event) Swift Serum Lvl 7 still brewing, counts above cauldron ~37 + 20 left (47 + 23 at 7:57.75)
whole chunk | IDLE | none: the cauldron was never empty (claim and rebrew gaps under 1 s)
whole chunk | OTHER | Boost x12 +40 min button unchanged (countdown 5h14m52s -> 5h12m13s); gems 1.68M constant; offer icons "1d 7h" unchanged; no bottling; Active tab never opened; trophy / chest 33389 unchanged; no cellar view
```

### Chunk 4 of 8: video 8:00 - 10:39 (seconds 480..639)

```
Notation: price in the station popup; "blue" = affordable button, "grey" = stopped for money. Coins are the top-bar value. Gems stay 1.68M the whole chunk. Boost x12 +40 min never changes (countdown only: 5h 12m 12s at 8:00 -> 5h 9m 33s at 10:39).
8:00-8:22 | STATION_LEVEL | Mermaid Tears 855 -> 992 (one popup per second): 8:00 855 (1.33an), 8:01 873 (2.11an cost, 10.2an), 8:02 917 (+ "Bonus x2 Profit" tag, 1.5ao), 8:03 943 (grey, 28.4ao), 8:04 945 (35.6ao blue), 8:05 952 (grey 78.7ao), 8:06 no popup, 8:07 957 (139ao blue), 8:08 961 (grey 219ao), 8:09 961 (blue 219ao), 8:10 968 (483ao), 8:12 968, 8:13 978 (1.5ap), 8:14 982 (2.36ap), 8:15 988 (grey 4.66ap, coins 3.46ap), 8:16-8:17 988 grey, 8:19 988 (blue 4.66ap, coins 25.7ap), 8:20 992 (grey 7.33ap, coins 3.5ap), 8:21-8:22 992 grey (popup fading at 8:22)
8:08-8:10 | BREW_DONE (inferred) | Swift Serum (dark blue cauldron; it was already brewing at 7:52; ingredient icons above the cauldron go from bat+dragon (8:00-8:07) to dragon only (8:08-8:09) to none at 8:10). Level not seen; the Brew list at 8:44 offers Swift Lvl 8 so the claimed one was Lvl 7 (inferred).
8:10 | IDLE (inferred) | cauldron dark blue without icons = brew finished, waiting for Claim, ~8:09.5 .. ~8:10.5 (the cauldron dialog itself was not visible in the 1 fps frames).
8:10-8:11 | BREW_START | Double Draught Lvl 5 (pink liquid). Seen only in the fading dialog at 8:11 ("Brewing ... Double Dr..., Lvl 5"). Counts above the cauldron at 8:11: Mermaid 60 + Dragon Scale 45. Brew list rows at that moment not seen. Tapped potion inferred from the Brewing row + pink cauldron.
8:12-8:14 | OTHER | pink cauldron icons (Mermaid + Dragon) count down (e.g. 8:13 "60 45", later 8:16 "37 .."); no other change.
8:22 | OTHER | coins jump 3.59ap -> 33.8ap (income burst while the station popup is grey).
8:23 | OTHER | Upgrades dialog opens (red "!" badge). Fade-in at 8:23.5.
8:23-8:24 | UPGRADE_BOUGHT | 1) Use golden Beetles (Beetle Juice profit x75) 24.6ap, bought at ~8:23.9 (row vanishes between 504.0 and 504.25 in the dialog sheet; coins 33.8ap -> 9.27ap). Only one purchase in this visit.
8:23-8:24 | UPGRADE_SKIPPED | rows seen when dialog closed (~8:24.4), all with BLUE (affordable at 9.27ap) buttons: Host an alchemy workshop +2 Customers 12.5M; Advertise in 'Wizard Monthly' +2 Customers 2.25ac; Get a guild endorsement +1 Customer 4af; Guarantee efficacy +1 Customer 3ai; Sponsor a local festival +1 Customer 6.4al; Apply distortion (Frog Scream profit x25) 3.02ap; Higher thread count (Spider Silk profit x50) 7.35ap. Not affordable (grey): Label as 'Wizard's Choice' (Mystic Mushrooms profit x50) 13.5aq; Label as 'Gravity Perfected' (Purified Water profit x75) 158aq. NOTE: none of the +Customer rows are ever bought in this chunk although the buttons are blue.
8:24 | OTHER | Upgrades dialog closed at ~8:24.4; top-left counter next to the chest icon reads 33389 (changes to 33391 at ~8:25-8:26, see below).
8:24-8:25 | VIEW | camera scrolls down from the cauldron view to the lower shop floor (right side, dashed tile).
8:25 | STATION_UNLOCK | Beetle Juice, price 1.64aa ("Unlock" popup over the dashed tile at ~8:25.2; coins show 9.27ap, not visibly reduced).
8:25 | TASK | banner "Unlock Beetle Juice" with two rewards (blue chest icon "2", yellow locked chest icon "36"); appears ~8:25.5. First reward looks greyed/checked at 8:27 (done). Counter at top-left changes 33389 -> 33391 at ~8:26 (= the "2" reward, inferred).
8:25-8:26 | STATION_LEVEL | Beetle Juice Level 1 (faded popup at 8:25.75: 184ac per item, 6.7s, price 984T) -> next second 8:26 popup 270ac / 1.74aa blue (level number is cut off by the right screen edge, unreadable 8:26-8:28; stars 0)
8:27 | OTHER | Beetle Juice popup shows tags "Bonus +1 Machine" and "Bonus x2 Profit" (price 9.49aa, cost 1.71ad); level still cut off.
8:26-8:28 | STATION_LEVEL | Beetle Juice ? -> ? (level hidden at the screen edge; tags +1 Machine, x2 Profit visible at 8:27-8:29; 8:28 cost 87.1ad, price 400aa)
8:29-8:43 | STATION_LEVEL | Beetle Juice 113 -> 916, about 60 levels per second: 8:29 113 (320ab), 8:30 175 (361ac), 8:31 235 (324ad), 8:32 294 (260ae), 8:33 354 (233af), 8:34 416 (262ag), 8:35 472 (150ah), 8:36 531 (120ai), 8:37 591 (108aj), 8:38 652 (109ak), 8:39 713 (109al), 8:40 772 (87.1am), 8:41 832 (78.2an), 8:42 894 (88ao), 8:43 916 (grey, 1.07ap, coins 848ao). Tag "+1 Machine" visible until 8:36, "x2 Profit" until 8:47.
8:40-8:43 | BREW_DONE (inferred) | Double Draught Lvl 5: only the Mermaid icon left over the cauldron at 8:42, none at ~8:43.5; Claim happened in the cauldron dialog (not captured).
8:44 | BREW_LIST | Cauldron dialog (first visible frame 8:44-8:45, Brew tab): Swift Serum Lvl 8 (Bat Wing 205, Dragon Scale 102); Double Draught Lvl 6 (Mermaid 91, Dragon Scale 68); Sizzle Serum Lvl 5 (Dragon Scale 60, Unicorn 30); Perfect Potion Lvl 1 (Bat Wing 21, Unicorn 9); Instant Infusion Lvl 1 (Djinn 21, Unicorn 12); Telepathic Tincture Lvl 1 (Djinn 15, Dragon Scale 9). No "Slots Full".
8:44-8:45 | BREW_START | Double Draught Lvl 6 (cauldron pink; counts at 8:46: Mermaid 91, Dragon Scale 66 (the 68 at start)). Tapped Brew on the 2nd row (inferred from pink cauldron).
8:44 | OTHER | Telepathic Tincture is a new potion (purple swirl, "10% chance customers order instantly"), Lvl 1.
8:45-8:46 | VIEW | camera at the upper shop (customers/cauldron view), customers counters above.
8:47-8:49 | STATION_LEVEL | Beetle Juice 916 -> 942 : 8:47 916 (blue 1.07ap), 8:48 925 (2.96ap), 8:49 942 (20.3ap)
8:50-8:51 | STATION_LEVEL | Mermaid Tears 992 -> 998 : 8:50 992 (blue 7.33ap), 8:51 998 (grey 14.5ap, coins 3.47ap)
8:53 | STATION_LEVEL | Mermaid Tears MAX (Level 1000, "x2 Profit" tag, grey MAX button; seen as a fading popup at 8:53).
8:54-9:05 | STATION_LEVEL | Beetle Juice 951 -> 983 with stops: 8:54 951 (56.2ap blue), 8:55 963 (grey 219ap), 8:56 963 grey, 8:58 965 (275ap), 8:59 970 (484ap), 9:00 975 (853ap), 9:01 978 (grey 1.2aq), 9:02 978 (blue 1.2aq), 9:03 983 (grey 2.12aq), 9:04-9:08 983 grey 2.12aq (coins 64.1ap -> 64.2ap, waiting for money)
9:09-9:15 | STATION_LEVEL | Beetle Juice 988 -> 999 : 9:09 988 (faded, grey 3.73aq), 9:10 990 (grey 4.67aq), 9:12 993 (blue 6.56aq), 9:13 995 (grey 8.23aq), 9:14 995 (blue 8.23aq), 9:15 999 (grey 13aq)
9:17 | STATION_LEVEL | Beetle Juice MAX (Level 1000, x2 Profit tag, grey "MAX" button)
9:17-9:19 | TASK | banner "Upgrade Beetle Juice to level 1000", rewards: red scroll "35" + yellow locked scroll "35". Done at ~9:19 (first reward shows a green check, greyed). Counter at top-left stays 33391.
9:22-9:24 | OTHER | Upgrades dialog opens at ~9:22.5 (coins 234aq).
9:23-9:24 | UPGRADE_BOUGHT | in this order (rows seen vanishing between 563.25 and 563.75 in the dialog sheet; coins 234aq -> 64aq, sum 171.5aq matches): 1) Apply distortion (Frog Scream profit x25) 3.02ap, 2) Higher thread count (Spider Silk profit x50) 7.35ap [1+2 vanish together between 9:23.25 and 9:23.5; order inferred from list order], 3) Label as 'Wizard's Choice' (Mystic Mushrooms profit x50) 13.5aq, 4) Label as 'Gravity Perfected' (Purified Water profit x75) 158aq [3+4 vanish together between 9:23.5 and 9:23.75; order inferred]. Rows 3 and 4 had been grey at 8:24; blue at 9:23 (coins 234aq).
9:23-9:24 | UPGRADE_SKIPPED | affordable (blue) but not bought: Host an alchemy workshop +2 Customers 12.5M; Advertise in 'Wizard Monthly' +2 Customers 2.25ac; Get a guild endorsement +1 Customer 4af; Guarantee efficacy +1 Customer 3ai; Sponsor a local festival +1 Customer 6.4al. Not affordable (grey), seen after the purchases at 9:23.75-9:24: Shift one octave up (Frog Scream profit x50) 20.2ar; Anti-stick coating (Spider Silk profit x75) 551ar (small text, "551lar" possible); Sell as 'Elixir-Grade' (Mystic Mushrooms profit x100) 1.01at. More rows below the visible area unknown.
9:24 | OTHER | Upgrades dialog closed at ~9:24.2. Coins 64aq -> 121aq -> 192aq (growing).
9:26 | VIEW | camera scrolls down to the cellar (two dashed unlock tiles visible: bottom-left and right; the scroll goes back up at 9:27).
9:26-9:27 | STATION_UNLOCK | Purified Water (cellar, bottom-left tile): bought between 9:26.0 and 9:27.0 (smoke effect at the tile at 9:27, popup "Level 1 Purified Water" fading in at 9:27). Price NOT seen (no "Unlock" popup frame). Coins 320aq before and after (price negligible).
9:27-9:29 | TASK | banner "Unlock Purified Water", rewards: red scroll "15" + yellow locked scroll "15"; first reward turns green check at ~9:29.7 (done).
9:27 | VIEW | camera moves back from the cellar to the cauldron view (shop) after the unlock.
9:28 | OTHER | Cauldron dialog opens (9:28.25) showing "Brewing ... Double Draught Lvl 6".
9:28 | BREW_DONE | Double Draught Lvl 6 ("Brew Complete!" with Claim at 9:28.75-9:29.0).
9:29 | BREW_LIST | (after Claim, ~9:29.1) Swift Serum Lvl 8 (Bat Wing 205, Dragon Scale 102); Double Draught Lvl 7 (Mermaid 136, Dragon Scale 102); Sizzle Serum Lvl 5 (Dragon Scale 60, Unicorn 30); Perfect Potion Lvl 1 (Bat 21, Unicorn 9); Instant Infusion Lvl 1 (Djinn 21, Unicorn 12); Telepathic Tincture Lvl 1 (Djinn 15, Dragon Scale 9). No "Slots Full". (Double Draught Lvl 6 claimed => Lvl 7 next; potion tapped at ~9:29.6.)
9:29 | BREW_START | Instant Infusion Lvl 1 (cyan cauldron from 9:29.75; counts Djinn 21 + Unicorn 12 from list; icons above cauldron not readable at start). Tapped via the 5th row (inferred from the cyan color + Djinn/Unicorn icons).
9:29 | VIEW | camera scrolls down to the cellar (9:29.7-9:30).
9:30-9:39 | STATION_LEVEL | Purified Water 1 -> 403 : 9:30 Level 1 (faded popup; cost 147ad, price 6.3ab grey), 9:31 8 (252ad, 14ab), 9:32 25 (3.74ae, 95.5ab, tag +1 Machine), 9:33 66 (175ae, 9.96ac, tags +1 Machine, x2 Profit), 9:34 126 (71af, 8.94ad), 9:35 186 (14.3ag, 8.02ae), 9:36 245 (2.69ah, 6.43af), 9:37 307 (1.27ai, 7.24ag), 9:38 366 (239ai, 5.8ah), 9:39 403 (8.24aj, 385ah). Coins 320aq -> 377aq.
9:39 | VIEW | camera goes up to the cauldron (shop) view (~9:39.25).
9:39-9:41 | OTHER | Cauldron dialog opened at ~9:39.7: "Brewing ... Instant Infusion Lvl 1".
9:41 | BREW_DONE | Instant Infusion Lvl 1 ("Brew Complete! Claim" at 9:41.25-9:41.5).
9:41 | BREW_LIST | (after Claim, 9:41.75) Swift Serum Lvl 8; Double Draught Lvl 7; Sizzle Serum Lvl 5; Instant Infusion Lvl 2 (Djinn 31, Unicorn 18); Perfect Potion Lvl 1; Telepathic Tincture Lvl 1. Instant Infusion moved up in the list. (Costs of the other rows as at 9:29.) No "Slots Full".
9:41-9:42 | BREW_START | Instant Infusion Lvl 2 (fading dialog at 9:42.0 shows "Brewing ... Lvl 2" with 3 ingredient icons; cauldron cyan at 9:42.25; icons not readable). Djinn 31 + Unicorn 18 from the list. Coins 434aq -> 706aq at 9:42.75.
9:43 | VIEW | camera scrolls down to the cellar (coins 848aq).
9:45-9:47 | STATION_LEVEL | Purified Water 408 -> 455 : 9:45 408 (12.1aj, 677ah blue), 9:46 423 (38.4aj, 3.71ai), 9:47 455 (902aj, 140ai; tag x2 Profit)
9:48-9:51 | STATION_LEVEL | Purified Water ? -> ? (level text hidden behind the task banner; cost per item 169ak at 9:48, 21.5al at 9:49, 4.04am at 9:50, 409am at 9:51; prices 112aj, 141ak, 113al, 102am. Stars 3 -> 4 -> 4 -> 4 and progress bar rising).
9:48-9:50 | TASK | banner "Upgrade Purified Water to level 500", rewards: purple gem "100" + yellow locked gem "1.8K". Gems fly toward the top bar at 9:48-9:49 (visible purple gems), at 9:50 the first reward shows a green check (done). Top-bar gems still show 1.68M (rounded).
9:52-9:55 | STATION_LEVEL | Purified Water 755 -> 936 : 9:52 755 (76.8an, 81.2an, tag x2 Profit), 9:53 817 (18.1ao, 91.4ao), 9:54 877 (1.83ap, 82ap), 9:55 936 (344ap, 65.8aq). Coins 848aq -> 415aq (spent).
9:56 | VIEW | camera goes up to the cauldron view (9:56).
9:56 | BREW_DONE (inferred) | Instant Infusion Lvl 2: cauldron cyan, no icons at 9:56; the dialog is open at 9:57.
9:57 | BREW_LIST | Cauldron dialog Brew tab (9:57, single frame, coins 55aq): Swift Serum Lvl 8 (205, 102); Double Draught Lvl 7 (136, 102); Sizzle Serum Lvl 5 (60, 30); Instant Infusion Lvl 3 (Djinn 47, Unicorn 27); Perfect Potion Lvl 1 (Bat 21, Unicorn 9); Telepathic Tincture Lvl 1 (15, 9). No "Slots Full". (Lvl 2 claimed before this frame.)
9:57-9:58 | BREW_START | Instant Infusion Lvl 3 (cyan cauldron with Djinn + Unicorn icons from 9:58; Brew button of the 4th row).
9:58-9:59 | OTHER | coins 55aq -> 970aq at 9:59.
10:00-10:04 | STATION_LEVEL | Purified Water 947 -> 949 (cellar view): 10:01 947 (grey 229aq, coins 31aq), 10:02-10:03 947 grey, 10:04 949 (grey 287aq, coins 32.6aq; waiting for money). Level at 10:00 not readable (popup not yet shown).
10:05-10:07 | VIEW | back at the cauldron view (customers counters, no popup).
10:08 | STATION_LEVEL | Purified Water 951 (blue 360aq; cost 1.09aq; coins 618aq)
10:09-10:11 | VIEW | cauldron view (scroll transition at 10:09).
10:12-10:13 | STATION_LEVEL | Purified Water 956 (10:13, grey 634aq, cost 1.6aq; coins 197aq)
10:14-10:18 | VIEW | cauldron view; coins 1.99ar -> 2.92ar -> 2.98ar.
10:18-10:19 | OTHER | Cauldron dialog opens at ~10:18.9 ("Brewing ... Instant Infusion Lvl 3"). Over the cauldron at 10:18 only the Djinn icon remained.
10:20 | BREW_DONE | Instant Infusion Lvl 3 ("Brew Complete! Claim" at 10:20.0).
10:20 | BREW_LIST | (after Claim, 10:20.25-10:20.5) Swift Serum Lvl 8 (205, 102); Double Draught Lvl 7 (136, 102); Sizzle Serum Lvl 5 (60, 30); Instant Infusion Lvl 4 (Djinn 70, Unicorn 40); Perfect Potion Lvl 1 (21, 9); Telepathic Tincture Lvl 1 (15, 9). No "Slots Full".
10:20-10:21 | BREW_START | Instant Infusion Lvl 4 (dialog closes at 10:20.75; cyan cauldron with Djinn + Unicorn icons at 10:21). Counts at start not readable.
10:22-10:23 | STATION_LEVEL | Purified Water 957 -> 962 : 10:22 957 (blue 710aq, cost 1.73aq, coins 4.09ar), 10:23 962 (grey 1.26ar, cost 2.54aq, coins 1.12ar)
10:24-10:28 | VIEW | cauldron view, coins 2.67ar -> 4.01ar (waiting).
10:29-10:30 | STATION_LEVEL | Purified Water 964 (10:30, grey 1.57ar, cost 2.97aq, coins 1.36ar)
10:31-10:34 | VIEW | cauldron view (cyan cauldron brewing).
10:35-10:36 | STATION_LEVEL | Purified Water 967 (10:36, blue 2.21ar, cost 3.74aq, coins 3.5ar)
10:37-10:39 | VIEW | back at the cauldron view; cyan cauldron still brewing Instant Infusion Lvl 4 (icons Djinn + Unicorn, counts not readable). End of chunk.
```

### Chunk 5: video seconds 640..799 (10:40 .. 13:19)

```
Notes: prices/coins are as burnt in the popups ("ar", "aq", "ad", ... letters).
Coins are compared with the button price to tell grey (not affordable)
from blue (affordable). Gems stay 1.68M the whole chunk. The counter
under the chest icon (top left) is 33391 until 11:45 and 33397 from 11:46.
Only Purified Water, Spider Silk and Mystic Mushrooms popups appear in this
chunk (all in the cellar). No shop-floor station popup, no Upgrades dialog,
no Active tab, no bottling. Cauldron dialogs: 10:49-10:51, 11:30-11:32,
12:25-12:28, 12:47-12:48, 13:17-13:18.
10:40 | VIEW | shop floor, cauldron brewing Instant Infusion (cyan, djinn lamp + unicorn icons above it), coins 3.39ar
10:40 | BREW_START | (continues from before) Instant Infusion Lvl 4 brewing, cyan cauldron, djinn + unicorn icons
10:42-10:43 | VIEW | scroll down to the cellar
10:43 | STATION_LEVEL | Purified Water 970 (price 3.1ar GREY, coins 2.35ar); previous seen level 967 at 10:36 (blue 2.21ar)
10:44 | VIEW | back to shop floor (coins 4.6ar)
10:49 | OTHER | cauldron button tapped, Cauldron dialog opens (10:49.25), tab Brew shows "Brewing..."
10:49 | BREW_LIST | not a list yet: "Brewing..." Instant Infusion Lvl 4 (25% chance to make food instantly +10%), 1-2 djinn icon in row
10:50 | BREW_DONE | Instant Infusion Lvl 4 ("Brew Complete!" at 10:50.0), coins 7.2ar -> 11.7ar
10:50 | OTHER | Claim tapped at ~10:50.4 (dialog goes from Claim to Brew list)
10:50 | BREW_LIST | (10:50.5) Swift Serum Lvl 8 (205 Bat Wing, 102 Dragon Scale); Double Draught Lvl 7 (136 Mermaid, 102 Dragon Scale); Sizzle Serum Lvl 5 (60 Dragon Scale, 30 Unicorn); Instant Infusion Lvl 5 (106 Djinn, 60 Unicorn); Perfect Potion Lvl 1 (21 Bat Wing, 9 Unicorn); Telepathic Tincture Lvl 1 (15 Djinn, 9 Dragon Scale). No "Slots Full!" visible. Cellar potions (Divine, Greedy, Golden) not yet in the list.
10:50 | BREW_START | Instant Infusion Lvl 5 at ~10:50.9 (inferred: the Brew tap is between dialog frames; cauldron at 10:51 is cyan with djinn + unicorn icons again, and the dialog at 11:30 shows Instant Infusion Lvl 5 brewing); counts 106 / 60 (from the list)
10:51 | VIEW | shop floor, dialog closed (10:51.0), coins 11.7ar
10:52-10:53 | VIEW | cellar (scroll down)
10:52 | STATION_LEVEL | Purified Water 970 (price 3.1ar BLUE, coins 14.1ar) -> 973 at 10:53 (popup only partly visible, price unreadable; coins fell 14.1ar -> 3.71ar)
10:54 | VIEW | shop floor
10:55-10:56 | VIEW | cellar
10:56 | STATION_LEVEL | Purified Water 974 (price 4.88ar GREY, coins 2.4ar)
10:57 | VIEW | shop floor
11:00-11:03 | VIEW | cellar (scroll starts at 11:00)
11:01 | STATION_LEVEL | Purified Water 975 (price 5.46ar GREY, coins 986aq); coins were 5.8ar at 11:00 so 974 -> 975 was bought at ~11:00 for ~4.88ar
11:02 | STATION_LEVEL | Purified Water 975 (price 5.46ar GREY, coins 986aq) still waiting
11:03 | STATION_LEVEL | Purified Water 976 (price 6.12ar GREY, coins 4.77ar)
11:04 | VIEW | shop floor
11:08 | OTHER | shop floor, coins 4.77ar -> 8.3ar (10 s later 15.9ar at 11:08)
11:09-11:10 | VIEW | cellar
11:09 | STATION_LEVEL | Purified Water 976 (price 6.12ar BLUE, coins 15.9ar)
11:10 | STATION_LEVEL | Purified Water 978 (price ? hidden at bottom, profit 8.73aq; coins 2.97ar)
11:11 | VIEW | shop floor
11:14-11:16 | VIEW | cellar
11:16 | STATION_LEVEL | Purified Water 979 (price 8.59ar GREY, coins 4.24ar)
11:17 | VIEW | shop floor
11:21-11:24 | VIEW | cellar (scroll 11:22, popup at 11:22)
11:22 | STATION_LEVEL | Purified Water 980 (price 9.63ar GREY, coins 9.49ar)
11:23 | VIEW | shop floor (camera between at 11:23)
11:24 | STATION_LEVEL | Purified Water 981 (price 10.8ar GREY, coins 102aq)
11:25 | VIEW | shop floor
11:30 | OTHER | cauldron button tapped (Cauldron dialog opens at 11:29.75)
11:30 | BREW_LIST | not a list: "Brewing..." Instant Infusion Lvl 5 (35% chance to make food instantly +10%)
11:31 | BREW_DONE | Instant Infusion Lvl 5 ("Brew Complete!" at 11:31.25), coins 10.4ar
11:31 | OTHER | Claim tapped at ~11:31.4
11:31 | BREW_LIST | (11:31.5) Swift Serum Lvl 8 (205 Bat Wing, 102 Dragon Scale); Double Draught Lvl 7 (136 Mermaid, 102 Dragon Scale); Instant Infusion Lvl 6 (159 Djinn, 91 Unicorn); Sizzle Serum Lvl 5 (60 / 30); Perfect Potion Lvl 1 (21 / 9); Telepathic Tincture Lvl 1 (15 / 9). No "Slots Full!".
11:32 | BREW_START | Instant Infusion Lvl 6 at ~11:31.9 (inferred: the Brew tap is not on a frame; list at 11:32.0 still open, cauldron at 11:32.25 cyan with djinn 159 / unicorn 91 icons (counts read in the 11:32 close-up), dialog at 12:25 shows Lvl 6 brewing). Counts 159 / 91.
11:32 | VIEW | shop floor, dialog closed (11:32.25), coins 20.9ar
11:33-11:34 | VIEW | scroll to the cellar (11:33 scrolling, 11:34 popup)
11:34 | STATION_LEVEL | Purified Water 983 (price 13.6ar BLUE, coins 25.3ar)
11:35 | STATION_UNLOCK | Spider Silk (inferred: at 11:34 the cellar shows a dashed tile where Spider Silk appears; at 11:35 the Spider Silk popup is shown with banner "Unlock Spider Silk"; price not readable, coins about unchanged at the "ar" scale, 11.9ar before and after; the 25.3ar -> 11.9ar drop is the Purified Water 983 -> 984 purchase)
11:35 | TASK | banner "Unlock Spider Silk": rewards 50 gems + 900 gems (gem animation at 11:35-11:36, gems total stays 1.68M); done (green check at 11:37)
11:35 | STATION_LEVEL | Spider Silk popup first seen: price 22.1ac (faded in), level hidden behind the banner
11:36 | STATION_LEVEL | Spider Silk (level hidden) price 48.7ac, profit 2.69ae, time 9.3 s
11:37 | STATION_LEVEL | Spider Silk (level hidden) price 375ac, profit 43ae
11:38-11:45 | STATION_LEVEL | Spider Silk 65 (11:38, price 31.2ad) -> 124 (25ae) -> 186 (28.1af) -> 245 (22.5ag) -> 306 (22.7ah) -> 365 (18.2ai) -> 427 (20.5aj) -> 483 (11.7ak at 11:45); about +60 levels/s, all BLUE (holding the button). Bonus tags "+1 Machine" and "x2 Profit" shown at 11:37 (faded) and stacked at 11:38-11:45
11:46 | TASK | banner "Upgrade Spider Silk to level 500": rewards a chest "6" + a second reward tile "108" (chest, locked tile); done at ~11:46-11:47 (green check on 11:47)
11:46 | REWARD | top-left counter next to the chest icon 33391 -> 33397 (+6) at 11:46 (inferred: reward of the task above, not clearly seen as a popup)
11:46-11:48 | STATION_LEVEL | Spider Silk level hidden behind the banner (price 6.64al at 11:46, 5.33am at 11:47, 6.71an at 11:48), level about 540-660; "+1 Machine" bonus tag fading out at 11:46, "x2 Profit" tag stays
11:49-11:52 | STATION_LEVEL | Spider Silk 720 (11:49, price 5.38ao) -> 782 (6.06ap) -> 842 (5.44aq) -> 867 (11:52, price 92.4aq BLUE, coins 37.9ar), still blue when the burst ended; last seen level 867 (faded popup of 867 again at 12:22)
11:53 | VIEW | cellar camera moves (11:53 view shows the cellar, stations further down)
11:54 | STATION_LEVEL | Purified Water 984 (price 15.2ar BLUE, coins 37.9ar)
11:55 | OTHER | shop floor view, coins 5.89ar (dropped from 37.9ar: about 2 levels of Purified Water bought, ~15.2 + 17ar, inferred)
11:56 | VIEW | shop floor
11:57 | VIEW | cellar (scroll), coins 31.7ar
11:58-11:59 | STATION_LEVEL | Purified Water 987 (price 21.3ar GREY, coins 12.7ar); bought about 984 -> 987 in 11:54-11:58 (coins 31.7ar -> 12.7ar)
11:59 | STATION_UNLOCK | Mystic Mushrooms (inferred: dashed tile at the lower right of the cellar until 11:58; at 11:59 the Mystic Mushrooms popup is shown at Level 1 with banner-less popup; price not readable, coins 12.7ar -> 12.8ar so negligible at "ar" scale)
11:59 | STATION_LEVEL | Mystic Mushrooms 1 (price 40.3ad BLUE, profit 1.25af, time 10.7 s)
12:00-12:15 | STATION_LEVEL | Mystic Mushrooms 10 (12:00, 112ad) -> 27 (767ad) -> 71 (113ae) -> 133 (127af) -> 193 (114ag) -> 252 (91ah) -> 312 (81.7ai) -> 374 (91.9aj) -> 433 (73.7ak) -> 493 (66.1al) -> 552 (53am) -> 613 (53.3an) -> 673 (47.9ao) -> 730 (30.6ap) -> 790 (27.5aq, 12:14) -> 810 (265aq, 12:15, 1 star, BLUE). All BLUE (coins 12.8ar held), about 60 levels/s. Bonus tags: "+1 Machine" and "x2 Profit" at 12:01-12:09 ("+1 Machine" gone from 12:10 at level 552), "x2 Profit" until 12:15. Last seen level 810 (burst may have continued, popup not seen again).
12:16-12:17 | VIEW | shop floor (cauldron visible), coins 10.8ar -> 28.4ar
12:18-12:19 | VIEW | cellar (scroll)
12:19 | STATION_LEVEL | Purified Water 989 (price 26.7ar GREY, coins 979aq)
12:20-12:21 | VIEW | shop floor
12:22-12:23 | VIEW | cellar; at 12:22 a faded Spider Silk popup (867, price 92.4aq) fading out
12:23 | STATION_LEVEL | Purified Water 990 (price 29.9ar GREY, coins 17.7ar)
12:24 | VIEW | shop floor (coins 17.7ar)
12:25 | OTHER | cauldron button tapped, dialog opens at 12:24.75
12:25 | BREW_LIST | not a list: "Brewing..." Instant Infusion Lvl 6 (45% chance to make food instantly +15%)
12:27 | BREW_DONE | Instant Infusion Lvl 6 ("Brew Complete!" at 12:27.5), coins 40ar
12:27 | OTHER | Claim tapped at ~12:27.6
12:27 | BREW_LIST | (12:27.75) Swift Serum Lvl 8 (205 Bat Wing, 102 Dragon Scale); Double Draught Lvl 7 (136 / 102); Instant Infusion Lvl 7 (239 Djinn, 136 Unicorn); Sizzle Serum Lvl 5 (60 / 30); Perfect Potion Lvl 1 (21 / 9, Brew button blue); Telepathic Tincture Lvl 1 (15 Djinn, 9 Dragon Scale); Divine Decoction Lvl 1 (15 Spider Silk, 6 Mystic Mushrooms); Greedy Gulp Lvl 1 (12 Purified Water, 9 Spider Silk); Golden Gulp Lvl 1 (12 Beetle, 9 Mystic Mushrooms). No "Slots Full!". The list scrolls down to the cellar potions by 12:28.0 (a drag).
12:28 | BREW_START | Divine Decoction Lvl 1 (white liquid; counts above the cauldron 15 Spider Silk + 6 Mystic Mushrooms). Brew tap at ~12:28.6 between the 12:28.5 list frame and the 12:28.75 closed dialog. Not Instant Infusion Lvl 7 although its row was visible at the top first.
12:29 | VIEW | shop floor, dialog closed (12:28.75), coins 40ar; cauldron white with spider/mushroom icons
12:30 | VIEW | cellar (scroll), coins 51.2ar
12:31 | STATION_LEVEL | Purified Water 991 (price 33.5ar GREY, coins 21.4ar; coins dropped 51.2ar -> 21.4ar at 12:31, so 990 -> 991 bought at 12:30.x for ~29.9ar)
12:32-12:36 | VIEW | shop floor
12:37 | VIEW | cellar (scrolling), coins 67.7ar
12:38 | STATION_LEVEL | Purified Water 992 (price 37.5ar GREY, coins 34.2ar)
12:39 | VIEW | shop floor
12:40-12:41 | VIEW | cellar; Purified Water 993 at 12:41 (price 42ar GREY, coins 8.75ar)
12:42-12:44 | VIEW | shop floor
12:45 | VIEW | cellar
12:45 | STATION_LEVEL | Purified Water 993 (price 42ar BLUE, coins 50.6ar)
12:46 | STATION_LEVEL | Purified Water 994 (price 47.1ar GREY, coins 8.65ar); camera back to shop right after (12:46.25)
12:46 | VIEW | shop floor
12:47 | BREW_DONE | Divine Decoction Lvl 1 ("Brew Complete!" at 12:47.5; cauldron dialog opened at ~12:47.3); coins 8.7ar
12:47 | OTHER | Claim tapped at ~12:47.6 (not on a frame)
12:47 | BREW_LIST | (12:47.75) Swift Serum Lvl 8; Instant Infusion Lvl 7; Double Draught Lvl 7; Sizzle Serum Lvl 5; Divine Decoction Lvl 2 (22 Spider Silk, 9 Mystic Mushrooms); Perfect Potion Lvl 1 with "Slots Full!" (greyed Brew; inferred: it shares a slot with the Divine Decoction just claimed, not proven). Rows below Perfect Potion not seen (list not scrolled).
12:48 | BREW_START | Divine Decoction Lvl 2 (white, counts 22 Spider Silk + 9 Mystic Mushrooms; Brew tapped at ~12:48.4 between the 12:48.25 list frame and the 12:48.5 closed dialog); coins 8.83ar
12:49 | VIEW | shop floor, dialog closed (12:48.5)
12:52-12:53 | VIEW | cellar
12:52 | STATION_LEVEL | Purified Water 994 (price 47.1ar BLUE, coins 82.7ar) -> 995 at 12:53 (popup partly visible, price unreadable; coins 35.7ar)
12:54-12:56 | VIEW | shop floor
12:57 | STATION_LEVEL | Purified Water 995 (price 52.7ar GREY, coins 52.1ar, cellar view)
12:58-12:59 | VIEW | shop floor
13:00-13:01 | VIEW | cellar
13:01 | STATION_LEVEL | Purified Water 996 (price 59ar GREY, coins 15.7ar)
13:02-13:05 | VIEW | shop floor
13:06 | VIEW | cellar (no popup)
13:07-13:08 | VIEW | shop floor
13:09 | STATION_LEVEL | Purified Water 996 (popup fading in, price 59ar BLUE, coins 521ar)
13:10 | STATION_LEVEL | Purified Water 996 -> 1000 = MAX (burst of ~4 levels in ~1 s: coins 521ar -> 239ar); popup "Level 1000", 3 stars, MAX grey, bonus tag "x2 Profit" shown, profit 94.9aq, time 8 s
13:10 | OTHER | Purified Water reached MAX at 13:10 (790 s)
13:11-13:16 | VIEW | shop floor (cellar left); coins 239ar -> 336ar
13:17 | OTHER | cauldron dialog opens at ~13:16.7 (frame 13:17 shows the Brew list), coins 336ar
13:17 | BREW_DONE | Divine Decoction Lvl 2 (inferred: the dialog goes straight to the Brew list, no Complete frame; Claim tap happened between 13:16.0 and 13:16.9)
13:17 | BREW_LIST | Swift Serum Lvl 8 (205 Bat Wing, 102 Dragon Scale); Instant Infusion Lvl 7 (239 Djinn, 136 Unicorn); Double Draught Lvl 7 (136 Mermaid, 102 Dragon Scale); Sizzle Serum Lvl 5 (60 Dragon Scale, 30 Unicorn); Divine Decoction Lvl 3 (33 Spider Silk, 13 Mystic Mushrooms); Perfect Potion Lvl 1 "Slots Full!" (21 Bat Wing, 9 Unicorn). Rows below not seen. All Brew buttons blue except Perfect Potion (coins 336ar).
13:18 | BREW_START | Divine Decoction Lvl 3 (white; counts above the cauldron 33 Spider Silk + 13 Mystic Mushrooms; cauldron frame at 13:19)
13:18 | VIEW | shop floor, dialog closed, coins 383ar
13:19 | OTHER | end of chunk: coins 383ar, gems 1.68M, Boost x12 +40 min button with countdown 5h 6m 53s (only the countdown changed in the whole chunk, 5h 9m 40s -> 5h 6m 53s)
```

### Chunk 6 (video 13:20 .. 15:59, seconds 800..959)

```
Format: m:ss | TYPE | details. Coins in the top bar are shown as read (units aq < ar < as < at < au). Gems stay 1.68M, the "x480" income multiplier stays x480 and the Boost x12 button only counts down (5h6m52s -> 5h4m13s), nothing is used or bought for gems in the whole chunk.
Continuity (from the previous chunk, 792-799): a Cauldron dialog was open at 13:17 (797) and Divine Decoction Lvl 3 is brewing at the chunk start (white cauldron, counts above it spider 33 / mushroom 13 at 13:20 = ingredients still to deliver).
== 13:20 - 13:31 Divine Lvl 3 brewing, Upgrades dialog, first Spider Silk burst ==
13:20-13:21 | OTHER | Shop view. Cauldron white, counts spider 33 / mushroom 13 (Divine Decoction Lvl 3 brewing, started before this chunk). Coins 475ar.
13:22 | OTHER | Upgrades dialog opens (fade-in at 13:22.25), coins 2.84as. No station popup before it.
13:22-13:24 | UPGRADE_SKIPPED | "Host an alchemy workshop" (+2 Customers) 12.5M - button blue (affordable), not bought
13:22-13:24 | UPGRADE_SKIPPED | "Advertise in 'Wizard Monthly'" (+2 Customers) 2.25ac - blue (affordable), not bought
13:22-13:24 | UPGRADE_SKIPPED | "Get a guild endorsement" (+1 Customer) 4af - blue (affordable), not bought
13:22-13:24 | UPGRADE_SKIPPED | "Guarantee efficacy" (+1 Customer) 3ai - blue (affordable), not bought (these four customer rows are at the top of the list and stay in the list the whole time; the prices are tiny against coins 2.84as, unclear why the player ignores them)
13:22-13:24 | UPGRADE_SKIPPED | "Sponsor a local festival" (+1 Customer) 6.4al - blue (affordable), not bought
13:23 | UPGRADE_BOUGHT | "Anti-stick coating" (Spider Silk profit x75) 551ar - row visible at 803.0, gone at 803.25; coins 2.84as -> 2.29as (consistent with the price). 1st purchase.
13:23 | UPGRADE_BOUGHT | "Shift one octave up" (Frog Scream profit x50) 20.2ar - row visible at 803.5, gone at 803.75; coins 2.29as -> 2.27as (consistent). 2nd purchase.
13:23-13:24 | UPGRADE_SKIPPED | "Sell as 'Elixir-Grade'" (Mystic Mushrooms profit x100) 1.01at - GREY (not affordable)
13:23-13:24 | UPGRADE_SKIPPED | "Layer with tritone" (Frog Scream profit x175) 1.51au - GREY (not affordable). It is the last row of the list.
13:24 | OTHER | Upgrades dialog closed (at 804.0 shop view again), coins 2.27as.
13:24 | VIEW | Scrolls down to the cellar (804 transition, cellar visible from 805).
13:25 | STATION_LEVEL | Spider Silk Lv 868, 1 star, 735ap per item, 9.3s, price 104aq, button BLUE. (start of burst)
13:26 | STATION_LEVEL | Spider Silk Lv 882, 1 star, price 506aq, blue
13:27 | STATION_LEVEL | Spider Silk Lv 904, now 2 stars, tag "Bonus x2 Profit", price 6.12ar, blue
13:25-13:28 | STATION_LEVEL | Spider Silk 868 -> 937 (burst of holding, 4 s). At 13:28 popup Lv 937 (2 stars, tag "Bonus x2 Profit" still shown), price 258ar GREY; coins fell 2.27as -> 129ar = stopped for money.
13:29 | VIEW | Back to the shop view (scrolled up). Coins 224ar.
13:30-13:31 | VIEW | Cellar again (13:30 no popup), 13:31 popup Spider Silk Lv 938, 2 stars, 321aq, price 289ar GREY (coins 15.2ar).
== 13:32 - 13:51 Divine Lvl 3 brewing, waiting, small Spider Silk steps ==
13:32 | VIEW | Shop view. Coins 15.2ar.
13:33 | VIEW | Cellar (scrolled down, no popup visible), coins 365ar.
13:34 | VIEW | Shop view, coins 77.1ar.
13:36 | VIEW | Cellar, no popup (coins 459ar).
13:37 | STATION_LEVEL | Spider Silk Lv 940 (popup mostly cut off at the bottom, price unreadable); coins 135ar.
13:37-13:43 | OTHER | Shop view, cauldron white, counts falling: 13:34 spider 2?/ mushroom 6, 13:35 20/4 ... (spider silk count falls slowly, mushrooms 13 -> ~1). Coins 135ar -> 435ar.
13:44 | STATION_LEVEL | Spider Silk Lv 941, 2 stars, 405aq, price 406ar GREY (coins 73.5ar) - cellar view.
13:45-13:50 | VIEW | Shop view, coins 73.5ar -> 594ar. Cauldron white, spider count only (mushroom icon gone at 13:50).
13:50 | OTHER | A mushroom icon "2" and spider icon still over the cauldron/"Cauldron" button area; Cauldron dialog opened at 13:51.
== 13:51 - 13:53 Divine Lvl 3 done, new brew Divine Lvl 4 ==
13:51 | OTHER | Cauldron dialog opens (dialog sheet 830.0-832.75), tab Brew-state "Brewing... Divine Decoction Lvl 3" (white potion, spider icon "1").
13:51 | BREW_DONE | Divine Decoction Lvl 3 ("Brew Complete!" with Claim at 831.75). 
13:52 | BREW_LIST | (video 832.0 - 832.25, claim done) Brew tab, "Pick a potion to brew!", rows in order:
13:52 | BREW_LIST | Swift Serum Lvl 8 - 205 Bat Wing, 102 Dragon Scale - Brew (blue)
13:52 | BREW_LIST | Instant Infusion Lvl 7 - 239 Djinn, 136 Unicorn - Brew (blue)
13:52 | BREW_LIST | Double Draught Lvl 7 - 136 Mermaid, 102 Dragon Scale - Brew (blue)
13:52 | BREW_LIST | Sizzle Serum Lvl 5 - 60 Dragon Scale, 30 Unicorn - Brew (blue)
13:52 | BREW_LIST | Divine Decoction Lvl 4 - 50 Spider Silk, 20 Mushrooms ("15% chance ... +10%") - Brew (blue)
13:52 | BREW_LIST | Perfect Potion Lvl 1 - 21 Bat Wing, 9 Unicorn - "Slots Full!" (grey)
13:52 | BREW_LIST | (one more row below Perfect Potion cut off, not scrolled to in this dialog)
13:52 | BREW_START | Divine Decoction Lvl 4 (white), tapped Brew at ~832.4; dialog closes at 832.5. Cauldron counts at 13:53: spider 50 / mushroom 20 (frame 834).
13:53 | OTHER | Coins 1.25as (up from 594ar), shop view; no other purchase.
== 13:54 - 14:54 Divine Lvl 4 brewing, Spider Silk climbing ==
13:54 | STATION_LEVEL | Spider Silk Lv 943, 2 stars, 472aq, price 509ar GREY (coins 399ar) - cellar
14:00 | STATION_LEVEL | Spider Silk Lv 943, price 509ar now BLUE (coins 899ar)
14:01 | STATION_LEVEL | Spider Silk Lv 944 (bought 943 -> 944 for 509ar, coins 899ar -> 390ar) (inferred from popup + coins)
14:08 | STATION_LEVEL | Spider Silk Lv 945, 551aq, price 638ar GREY (coins 357ar)
14:12 | STATION_LEVEL | Spider Silk Lv 946, 595aq, price 715ar GREY (coins 360ar)
14:26 | STATION_LEVEL | Spider Silk Lv 947, 642aq, price 800ar GREY (coins 647ar)
14:27-14:28 | STATION_LEVEL | Spider Silk 947 -> 949 (popup Lv 947 at 14:27 coins 1.92as; popup Lv 949, 749aq, price 1.01as grey at 14:28, coins 227ar) (two steps bought, inferred from coin drop)
14:33-14:34 | STATION_LEVEL | Spider Silk 949 -> 950 (inferred: coins 1.26as at 14:33 -> 265ar at 14:34); popup Lv 950, 809aq, price 1.13as GREY
14:42-14:43 | STATION_LEVEL | Spider Silk Lv 951 (popup cut at 14:43, price unreadable)
14:50 | STATION_LEVEL | Spider Silk Lv 951, 874aq, price 1.26as BLUE (coins 1.68as)
14:51 | STATION_LEVEL | Spider Silk 951 -> 952 (inferred: coins 1.68as -> 425ar)
13:54-14:54 | VIEW | Cellar visits (each ~1-3 s, the bot scrolls down, taps the Spider Silk station and scrolls back; times seen): 13:54, 14:00-14:01, 14:03 (no popup), 14:08, 14:11-14:12, 14:25-14:28, 14:33-14:34, 14:42-14:43, 14:50, 14:54 (cellar, no popup).
13:55-14:44 | OTHER | Shop view in between. Cauldron white, counts: 13:55-13:58 spider 50 / mushroom 20, 14:01 4?/16, 14:03 ?/14, 14:06 ?/13, 14:09 ?/10, 14:13 ?/6, 14:16 3?/6, 14:20 3?/2, 14:24 2?/-, mushrooms done by ~14:27, then spider only (14:28 "2?" -> 14:36 "1?" -> 14:42 "1"), coins 129ar-1.68as. 
== 14:45 - 14:46 Active tab: Sizzle Serum bottled ==
14:45 | OTHER | Cauldron dialog open on the Active tab (bottle icon) at 885 (no Brew tab frame seen before it; dialog opened at ~884.5). Header corks 1.01K, "Bottled Potion Duration 20m", "Bottled Potion Effect x0.5", coins 838ar.
14:45 | OTHER | Active list: Swift Serum Lvl 7 (bottled effect 125%), Sizzle Serum Lvl 4 (150%), Double Draught Lvl 6 (30%), Instant Infusion Lvl 6 (30%), Divine Decoction Lvl 3 (8%, Bottle button GREY); each Bottle costs 1 cork.
14:46 | BOTTLE | Sizzle Serum Lvl 4 (red potion flying away with a "1" cork at 886; the row is gone, list now Swift Lvl 7, Double Lvl 6, Instant Lvl 6, Divine Lvl 3, 1 slot "Empty"). Resets Sizzle to Lvl 1 (Brew tab later shows Sizzle Lvl 1).
14:47 | OTHER | Dialog closed (887). Coins 1.68as. Cauldron still white (Divine Lvl 4 brewing).
== 14:55 - 14:59 Divine Lvl 4 done, Golden Gulp Lvl 1 started ==
14:55 | OTHER | Cauldron dialog opens (fade-in at 895.5), "Brewing... Divine Decoction Lvl 4" with spider count 2 -> 1 (frames 895.5-898.0). The player waits with the dialog open. Coins 1.37as.
14:58 | BREW_DONE | Divine Decoction Lvl 4 ("Brew Complete!" + Claim at 898.25). Claim tapped ~898.5-898.7.
14:58-14:59 | BREW_LIST | (898.75 and 899.0-899.25 scrolled) rows:
14:58 | BREW_LIST | Swift Serum Lvl 8 - 205 Bat Wing, 102 Dragon Scale - Brew
14:58 | BREW_LIST | Instant Infusion Lvl 7 - 239 Djinn, 136 Unicorn - Brew
14:58 | BREW_LIST | Double Draught Lvl 7 - 136 Mermaid, 102 Dragon Scale - Brew
14:58 | BREW_LIST | Divine Decoction Lvl 5 - 76 Spider Silk, 30 Mushrooms ("25% chance ... +5%") - Brew
14:59 | BREW_LIST | Sizzle Serum Lvl 1 - 12 Dragon Scale, 6 Unicorn ("50% faster") - Brew (a slot was free after the bottling)
14:59 | BREW_LIST | Perfect Potion Lvl 1 - 21 Bat Wing, 9 Unicorn - Brew
14:59 | BREW_LIST | Telepathic Tincture Lvl 1 (NEW, light blue/violet swirl bottle, "10% chance customers order instantly") - 15 Djinn, 9 Dragon Scale - Brew
14:59 | BREW_LIST | Greedy Gulp Lvl 1 (NEW, green bottle with a belt, "5% chance for a greedy customer") - 12 Purified Water, 9 Spider Silk - Brew
14:59 | BREW_LIST | Golden Gulp Lvl 1 (NEW, orange bottle, "5% chance for a golden customer") - 12 Beetle Juice, 9 Mystic Mushrooms - Brew
14:59 | BREW_START | Golden Gulp Lvl 1 (orange), counts at 15:00: beetle 12 / mushroom 9 (frame 901). Tapped at ~899.3, dialog closed at 899.5.
15:00 | OTHER | Coins 1.82as at 15:00 -> 418ar at 15:01 (cellar upgrade, see below). Cauldron orange.
== 15:01 - 15:20 Golden Gulp Lvl 1 brewing ==
15:01 | STATION_LEVEL | Spider Silk Lv 953, 2 stars, 1.02ar, price 1.58as GREY (coins 418ar) - cellar
15:10 | STATION_LEVEL | Spider Silk Lv 953, price 1.58as now BLUE (coins 3.72as)
15:11 | STATION_LEVEL | Spider Silk Lv 955, 1.18ar, price 1.99as GREY (coins 469ar) (two steps bought 953 -> 955, inferred)
15:15-15:16 | STATION_LEVEL | Spider Silk Lv 955, price 1.99as GREY (coins 1.44as)
15:18 | STATION_LEVEL | Spider Silk Lv 956, 1.28ar, price 2.22as GREY (coins 583ar)
15:01-15:19 | VIEW | Cellar visits: 15:01, 15:06-15:11 (long visit, cellar view 15:06-15:11), 15:15-15:16, 15:18. Shop view otherwise.
15:00-15:19 | OTHER | Cauldron orange, counts beetle 12 -> 10 (15:03) -> ~9 (15:14) -> beetle only, mushroom icon gone (15:15-15:18, "1" left).
15:20 | BREW_DONE | Golden Gulp Lvl 1 (inferred: at 15:19 only the beetle icon is left, at 15:20 the cauldron has NO count icons; the dialog for the claim was not caught). Cauldron IDLE about 15:20-15:21 (inferred, ~1 s).
== 15:21 - 15:49 Golden Gulp Lvl 2 ==
15:21 | OTHER | Cauldron dialog fading (frame 921, semi-transparent), shows "Brewing... Golden Gulp Lvl 2", 18 Beetle / 13 Mushrooms.
15:21 | BREW_START | Golden Gulp Lvl 2 (orange), 18 Beetle / 13 Mushrooms (inferred: Claim of Lvl 1 + Brew tapped between 920.3 and 921.0; the Brew list of this moment was not seen). Counts at 15:22 "18/13".
15:23 | VIEW | Cellar visit (15:23-15:24), no popup readable; shop view from 15:25 (coins 1.18as).
15:21-15:49 | OTHER | Shop view, cauldron orange, counts at 15:25-15:27 beetle 10 / mushroom 13 -> 15:30 ?/9 -> 15:31 ?/7 -> 15:36 ?/7 -> 15:37 ?/ (mushroom icon gone at 15:39), later beetle only. Coins 1.18as -> 5.43as (15:32) -> 735ar (15:34, after cellar buy) -> 3.44as (15:45).
15:34-15:35 | STATION_LEVEL | Spider Silk Lv 958, 1.49ar, price 2.79as GREY (coins 735ar)
15:43 | STATION_LEVEL | Spider Silk Lv 959, 1.61ar, price 3.12as GREY (coins 2.7as)
15:21-15:49 | VIEW | Cellar visits: 15:23-15:24, 15:33-15:35, 15:43. Shop view otherwise.
15:45-15:49 | OTHER | Cauldron dialog open (dialog sheets 945-949.75): "Brewing... Golden Gulp Lvl 2" with beetle icon count 1, 5% chance +4%. Opens at ~945.6, waits for the end. Coins 3.44as.
15:49 | BREW_DONE | Golden Gulp Lvl 2 ("Brew Complete!" + Claim at 949.75; Claim tapped ~950.0).
== 15:50 - 15:59 Golden Gulp Lvl 3 ==
15:50 | BREW_LIST | (950.25-950.5, coins 4.72as) rows:
15:50 | BREW_LIST | Swift Serum Lvl 8 - 205 Bat Wing, 102 Dragon Scale - Brew
15:50 | BREW_LIST | Instant Infusion Lvl 7 - 239 Djinn, 136 Unicorn - Brew
15:50 | BREW_LIST | Double Draught Lvl 7 - 136 Mermaid, 102 Dragon Scale - Brew
15:50 | BREW_LIST | Divine Decoction Lvl 5 - 76 Spider Silk, 30 Mushrooms - Brew
15:50 | BREW_LIST | Golden Gulp Lvl 3 - 27 Beetle, 20 Mushrooms ("9% chance for a golden customer +4%") - Brew
15:50 | BREW_LIST | Sizzle Serum Lvl 1 - 12 Dragon Scale, 6 Unicorn - "Slots Full!" (grey; 5 slots now: Swift, Double, Instant, Divine, Golden Gulp)
15:50 | BREW_LIST | Perfect Potion below (cut off, presumably also Slots Full)
15:51 | BREW_START | Golden Gulp Lvl 3 (orange), tapped at ~950.5-950.7; cauldron counts 27 Beetle / 20 Mushrooms at 15:51-15:52 (frame 952). Dialog closed at 950.75.
15:51 | OTHER | Coins 7.75as (up from 4.72as). 
15:52 | VIEW | Cellar (no popup yet), coins 7.75as.
15:53 | STATION_LEVEL | Spider Silk Lv 962, 2 stars, 2.03ar, price 4.38as BLUE (coins 17.4as)
15:54 | STATION_LEVEL | Spider Silk Lv 965, 2.56ar, price 6.16as GREY (coins 2.7as) = burst 962 -> 965 (3 levels, coins 17.4as -> 2.7as, inferred)
15:55-15:58 | OTHER | Shop view, coins 2.7as -> 6.15as. Cauldron orange, counts beetle 22 / mushroom 20 (15:55) -> 20/20 (15:58).
15:59 | STATION_LEVEL | Spider Silk Lv 966, 2 stars, 2.77ar, price 6.89as GREY (coins 880aq) - cellar visit at the end of the chunk (inferred 965 -> 966 bought between 15:58 and 15:59).
== Not seen in this chunk ==
No TASK banners, no REWARD claims, no STATION_UNLOCK, no station popups other than Spider Silk, no other brews than Divine / Golden Gulp, no Boost use, no offer taps.
```

### Chunk 7 of 8: video seconds 960..1119 (16:00 .. 18:39)

```
Format: m:ss | TYPE | details (video time). Coins are shown as "880aq", "5.99as" etc. (magnitude letters ar < as < at < au). Gems stay 1.68M the whole chunk.
16:00-16:19 | BREW (cont.) | Golden Gulp (orange liquid) is still brewing from the previous chunk; it is the only potion in this whole chunk. Above the cauldron the remaining counts fall: mushroom 14 at 16:02, about 10 at 16:08, 6 at 16:12, 3 at 16:15; the beetle icon is gone from 16:16 on (beetle done first), only the mushroom icon "3" remains until the end of the brew (counts read from the base sheets, small digits, approximate)
16:00 | OTHER | coins 880aq. Boost x12 "+40 min" button: only the countdown ticks (5h 4m 12s at 16:00, 5h 1m 33s at 18:39), nothing else changes
16:00-16:08 | VIEW | shop floor (ingredient stations at the left/right, cauldron in the middle); no taps on stations seen, only worker traffic
16:09-16:10 | VIEW | camera scrolls down towards the cellar (frame 16:09 = cellar, no station popup shown)
16:10 | VIEW | back to the shop floor
16:17-16:18 | VIEW | scroll down to the cellar (16:18 Spider Silk popup visible), then back to the shop at 16:19
16:18 | STATION_LEVEL | 16:18 Spider Silk Level 967, 2 stars, price 7.72as grey (not affordable, coins 903ar), time 9.3 s
16:20 | BREW_DONE | Golden Gulp Lvl 3 ("9% chance for a golden customer +4%"); Cauldron dialog opened at ~16:20.3, shows "Brew Complete!" + Claim (Cauldron dialog sheet w0979); red "!" badge on the Cauldron button beforehand
16:20.9 | BREW_LIST | after Claim the Brew tab opens: Swift Serum Lvl 8 (205 bat wing? / 102 dragon scale?, Brew blue), Instant Infusion Lvl 7 (239 / 136, Brew), Double Draught Lvl 7 (136 / 102, Brew), Divine Decoction Lvl 5 (76 spider silk / 30 mushroom, Brew), Golden Gulp Lvl 4 (40 beetle / 30 mushroom, "13% chance for a golden customer +4%", Brew), Sizzle Serum Lvl 1 (12 / 6, "Slots Full!" greyed), Perfect Potion (cut off at the bottom of the frame). All Brew buttons except Sizzle blue. Costs read from small digits; the 3-digit ones are approximate
16:21 | BREW_START | Golden Gulp Lvl 4 tapped at about 16:21.1 in the list; dialog then shows "Brewing... Golden Gulp Lvl 4" and fades out; cauldron shows beetle 40 / mushroom 30 above it
16:21 | OTHER | Brew Complete -> Claim -> Brew list -> Brew took about 1 s (one Cauldron visit 16:20.3 - 16:21.4)
16:21-16:24 | BREW | Golden Gulp Lvl 4 brewing, counts 40/30 at 16:21-16:24 (beetle part stays 40 for a few s)
16:25 | VIEW | scroll to cellar
16:25-16:26 | STATION_LEVEL | 16:25 Spider Silk Level 967 price 7.72as BLUE (affordable now); 16:26 Level 971, price 12.2as grey (burst 967 -> 971, stopped for money; coins 4.19as)
16:27 | VIEW | back to shop floor
16:33 | OTHER | at 16:33.0 a popup "-92% Big Potion Shop Offer" (1d 7h, 30 / 120 / 7.2K gems items, price EUR 14.99) is opened from the small offer icon at the right and is closed within 0.25 s; nothing bought (dialog sheet w0993)
16:34 | OTHER | Cauldron dialog opened at ~16:34.2 and closed at ~16:35.0: only looking, "Brewing... Golden Gulp Lvl 4", remaining counts 28 beetle / 23 mushroom (zoom 16:34). Nothing tapped
16:34-16:42 | BREW | Golden Gulp Lvl 4 still brewing (counts ~25/25 above the cauldron at 16:33-16:36, mushroom 22 at 16:39, 22/22 at 16:39; digits small)
16:40-16:41 | VIEW | scroll to cellar and back: 16:40 Spider Silk Level 972 grey (price 13.6as, coins 1.35as), shop again from 16:42
17:01 | OTHER | only the mushroom icon "1" left above the cauldron; at 17:02 no counts, orange liquid still bubbling
17:02 | BREW_DONE | Golden Gulp Lvl 4 ends at about 17:02 (counts gone, "!" badge on the Cauldron button) (inferred; no Brew Complete frame seen)
17:03 | BREW_LIST | Cauldron dialog at 17:03 (single frame, no dialog sheet) already shows the Brew list, i.e. the Lvl 4 potion was claimed in the moment before (inferred): Swift Serum Lvl 8 (205 / 102), Instant Infusion Lvl 7 (239 / 136), Double Draught Lvl 7 (136 / 102), Divine Decoction Lvl 5 (76 / 30), Golden Gulp Lvl 5 (17% chance for a golden customer +4%, 60 beetle / 45 mushroom, zoom 17:03), Sizzle Serum Lvl 1 (12 / 6, Slots Full! grey), Perfect Potion (cut off). Coins 13.1as
17:03 | BREW_START | Golden Gulp Lvl 5 (60 beetle / 45 mushroom) started at ~17:03.5 (inferred: dialog closed at 17:04 and the cauldron shows 60/45 at 17:06; the Brew tap itself was not seen)
17:03-18:05 | BREW | Golden Gulp Lvl 5 brewing; counts: 60/45 at 17:06, beetle 51?/39 at 17:12-17:19 (digits unclear), mushroom 32 at 17:24-17:27, 22/22?; mushroom only "13" at 17:52, "9" at 17:56, "7" at 17:57-17:58, "6" at 17:59, "3" at 18:02, "2" at 18:04 (digits small, partly approximate)
17:04-17:05 | VIEW | scroll to cellar
17:04-17:05 | STATION_LEVEL | 17:04 Spider Silk Level 972 BLUE (price 13.6as, coins 68as); 17:05 Level 976, price 21.4as grey. (burst 972 -> 976)
17:06 | VIEW | back to shop floor
17:08-17:09 | VIEW+STATION_LEVEL | cellar visit: 17:08 Spider Silk Level 977 BLUE (price 24as, coins 96.1as); 17:09 Level 980, price 33.7as grey (burst 977 -> 980, stopped for money, coins 15.2as). Back in shop at 17:10
17:26-17:27 | VIEW+STATION_LEVEL | cellar visit; 17:27 Spider Silk Level 981, price 37.8as grey (coins 5.95as). Back in shop at 17:28
17:35-17:36 | VIEW | cellar visit (no station popup seen), shop again at 17:37
17:50-17:51 | VIEW+STATION_LEVEL | cellar visit; 17:51 Spider Silk Level 982, price 42.3as grey (coins 3.92as). Shop again at 17:52
18:03-18:04 | VIEW | cellar visit, no popup seen, shop again at 18:05
18:05 | BREW_DONE | Golden Gulp Lvl 5 finished (no counts above the cauldron at 18:05, "!" badge on the Cauldron button at 18:06) (inferred); actual Brew Complete screen opened at about 18:06.0 by the bot (dialog sheet w1086)
18:06 | BREW_DONE | Cauldron dialog: "Brew Complete!" Golden Gulp Lvl 5 ("17% chance for a golden customer +4%") + Claim. Claimed at ~18:06.2
18:06 | BOTTLE | none (Active tab not opened)
18:06 | BREW_LIST | after Claim: Swift Serum Lvl 8 (205 / 102), Instant Infusion Lvl 7 (239 / 136), Double Draught Lvl 7 (136 / 102), Golden Gulp Lvl 6 (21% chance for a golden customer +3%, 91? beetle / 68 mushroom), Divine Decoction Lvl 5 (76 / 30), Sizzle Serum Lvl 1 (12 / 6, Slots Full!), Perfect Potion (cut off). All Brew buttons blue (except Sizzle). Coins 162as
18:06.5-18:07 | OTHER | NO Brew button was tapped: the dialog was closed (fade-out at 18:06.75, list unchanged) -> cauldron stays EMPTY
18:06 | IDLE | cauldron black and empty from about 18:06 (frame 18:09 = black cauldron) until the end of the chunk at 18:39 (still empty); no brew started in the following 33 s
18:07 | OTHER | at 18:07.0 the bot taps the Upgrades button (up arrow at the bottom right with red badge); the Upgrades dialog opens at ~18:07.2
18:07 | UPGRADE_BOUGHT | in order (rows disappear from the top; 18:07.5 -> 18:07.75 the first two rows are bought within 0.25 s):
18:07 | UPGRADE_BOUGHT | 1. "Host an alchemy workshop" +2 Customers, 12.5M
18:07 | UPGRADE_BOUGHT | 2. "Advertise in 'Wizard Monthly'" +2 Customers, 2.25ac
18:07-18:08 | UPGRADE_BOUGHT | 3. "Get a guild endorsement" +1 Customer, 4af
18:08 | UPGRADE_BOUGHT | 4. "Guarantee efficacy" +1 Customer, 3ai
18:08 | UPGRADE_BOUGHT | 5. "Sponsor a local festival" +1 Customer, 6.4al (gone at 18:08.25)
18:08 | UPGRADE_SKIPPED | "Sell as 'Elixir-Grade'" Mystic Mushrooms profit x100, 1.01at, button grey (not affordable; coins 235as)
18:08 | UPGRADE_SKIPPED | "Layer with tritone" Frog Scream profit x175, 1.51au, button grey (not affordable)
18:08 | OTHER | no "+1 Alchemist" / "Unlock Cellar" row visible in the dialog; the five bought rows give +7 customers in total. Dialog closed at ~18:08.5 (the dialog is only opened once, 18:07.2 - 18:08.4). Coins 235as (unchanged by the purchases, prices are tiny)
18:09-18:24 | OTHER | cauldron EMPTY (black), customers queue growing at the top of the shop (many order bubbles; more customers visible than before the upgrades); coins rise 235as -> 243as (18:14) -> 370as (18:19) -> 400as (18:23)
18:24-18:27 | VIEW | scroll to the cellar (18:24-18:25 cellar shown)
18:25 | STATION_LEVEL | Mystic Mushrooms Level 816, 1 star, time 10.7 s, price 522aq BLUE (zoom 18:26; first Mushrooms popup in this chunk)
18:26 | STATION_LEVEL | Mystic Mushrooms Level 832, price 3.2ar BLUE (burst, button held)
18:27 | STATION_LEVEL | Mystic Mushrooms Level 872, price 298ar BLUE, 1 star (zoom 18:27); coins 397as. Burst 816 -> 872+ (button still blue, i.e. not stopped for money; end of the burst not seen)
18:28 | VIEW | back to shop floor; cauldron still empty (black)
18:28-18:39 | OTHER | cauldron EMPTY, no cellar visit, no dialog; many customers waiting; coins 397as -> 660as (18:31) -> 689as (18:39)
18:39 | OTHER | end of the chunk: cauldron still black/empty (zoom 18:39 = frame 01120); Boost countdown 5h 1m 33s; no banner/task/reward seen in the whole chunk
```

### Chunk 8 of 8: video 18:40 (1120 s) .. 21:15 (1275 s, end of video)

```
Times are video times (m:ss). Coins are as shown in the top bar. Gems 1.68M the whole chunk (unchanged).
18:32-19:03 | VIEW | (continuity) shop floor view, no popups, no purchases; coins grow 665as (1112 s) -> 999as (1144 s)
18:32-19:05 | IDLE | cauldron is black/empty in every frame where it is visible (1112..1186 s; it is not visible again later, cellar view); cauldron button at the bottom has a red "!" badge all the time, the Cauldron dialog is never opened in this chunk
18:40-19:05 | OTHER | Boost button "Boost x12 +40 min" never tapped, only the countdown runs: 5h 1m 32s (1120 s) -> 4h 58m 57s (1275 s)
19:05 | OTHER | (1145 s) a small red dot appears on the bottom-right "up arrow" (Upgrades) button, gone again at 1147 s; the Upgrades dialog is not opened
19:06 | OTHER | (1146 s) coins drop 1.01at -> 7.64as: money was spent on Mystic Mushrooms levels (see next lines)
19:07 | VIEW | (1147 s) camera moves down from the shop to the cellar; first cellar frame shows the Mystic Mushrooms popup (tap on the station)
19:07-19:09 | STATION_LEVEL | Mystic Mushrooms 872 -> 884 (1147 s L872 298ar blue; 1148 s L882 925ar blue; 1149 s L884 1.16as grey, coins 457ar)
19:09-19:12 | STATION_LEVEL | Mystic Mushrooms 884 stopped for money, grey (1.16as, coins 457ar) 1149-1152 s
19:13 | STATION_LEVEL | Mystic Mushrooms L911 (24.8as blue, coins 43.6as); bonus tag "x2 Profit" shown, 2 stars (884 -> 911 happened between 1152 and 1153 s, coins 457ar -> 43.6as)
19:14-19:16 | VIEW | (1154-1156 s) back to the shop floor, coins 18.8as -> 114as (stations leveled, not seen)
19:17-19:18 | STATION_LEVEL | Mystic Mushrooms 912 (27.8as, popup just fading in, 1157 s) -> 916 (1158 s, 43.6as grey, coins 3.98as)
19:19-19:25 | VIEW | (1159-1165 s) shop floor; coins 3.98as -> 278as
19:26-19:27 | STATION_LEVEL | Mystic Mushrooms L916 (43.6as blue, coins 278as, 1166 s) -> L921 (76.9as grey, coins 1.2as, 1167 s); cellar view
19:27-19:32 | STATION_LEVEL | Mystic Mushrooms 921 stopped for money, grey 76.9as (coins 1.2as) 1167-1172 s
19:33 | STATION_LEVEL | Mystic Mushrooms L950 (2.06at, blue, coins 3.45at); 921 -> 950 between 1172 and 1173 s
19:34-19:36 | VIEW | (1174-1177 s) shop floor again; coins 1.39at -> 1.79at
19:38 | VIEW | (1178 s) camera scrolls down to the cellar
19:39-19:43 | STATION_LEVEL | Mystic Mushrooms L951 (2.31at grey, coins 1.79-1.81at) stopped for money 1179-1183 s
19:44 | STATION_LEVEL | Mystic Mushrooms L977 (43.9at grey, coins 28.3at); 951 -> 977 between 1183 and 1184 s
19:45-19:46 | VIEW | (1185-1186 s) shop floor briefly, coins 28.3at -> 29at
19:47 | VIEW | (1187 s) scrolling down in the cellar to the bottom
19:48 | STATION_UNLOCK | Frog Screams (the last station): dashed tile with "Unlock" + blue button 13.5ae (1188 s, coins 29at); next frame (1189 s) the station exists (frog + crate at the bottom). The coin drop of 13.5ae is invisible at 29at (inferred bought at ~1188.5 s)
19:50 | STATION_LEVEL | Frog Screams L6 (107ae blue, 1190 s)
19:51 | STATION_LEVEL | Frog Screams L21 (583ae blue) with bonus tags "+1 Machine" and "x2 Profit" (1191 s)
19:52-20:05 | STATION_LEVEL | Frog Screams burst, one level-up step per second (holding the button): 1192 L54 (24.6af) -> 1193 L114 (22.1ag) -> 1194 L176 (24.8ah) -> 1195 L235 (19.9ai) -> 1196 L295 (17.9aj) -> 1197 L355 (16.1ak) -> 1198 L417 (18.1al) -> 1199 L476 (14.5am) -> 1200 L536 (13an) -> 1201 L595 (10.4ao) -> 1202 L657 (11.7ap) -> 1203 L716 (9.38aq) -> 1204 L776 (8.42ar) -> 1205 L836 (7.56as) -> 1206 L862 (144as, coins 2.79au, blue). Ingredient 12 s per item. Bonus tags seen: "+1 Machine" and "x2 Profit" above the popup from 1191 to 1200 s ("x2 Profit" tag only from 1201 s, +1 Machine tag gone at 1201 s); the star colour turns blue/green/purple/red along the way
20:06 | STATION_LEVEL | Frog Screams stops at L862 (price 144as blue, coins 2.79au): not stopped for money, the bot leaves it (1206-1207 s popup still shown, view scrolls up)
20:06 | OTHER | (1206 s) big red badge on the bottom-right up-arrow (Upgrades) button
20:07-20:08 | VIEW | (1207-1208 s) camera scrolls up toward the shop, Upgrades dialog opens (~1207.5 s)
20:08 | UPGRADE_BOUGHT | "Layer with tritone" - Frog Scream profit x175, 1.51au (1208.0 s: only this one row in the dialog, button blue; closes right after; coins 2.79au -> 1.28au = exactly the price). It is the only row of the dialog, nothing skipped
20:09 | OTHER | (1208.75 s) Active Skills dialog opens (the bot tapped the Popular Dish skill button): "Popular Dish 3m - Selected dish is more likely to be ordered - Select"
20:09-20:10 | OTHER | (1209.5-1210 s) "Select a dish" grid (bat, dragon, unicorn, lamp, mermaid, beetle, drops, spider, mushroom, frog); frog = Frog Screams picked
20:10 | OTHER | (1210.5 s) Active Skills: Popular Dish, 'Frog Screams' is more likely to be ordered, button "Start" tapped; 1210.75 s it shows "2m 59s ACTIVE" + Stop. Dialog closed at ~1211 s (Popular Dish ON for Frog Screams, 3 min)
20:11 | VIEW | (1211 s) cellar bottom, Frog Screams station with crates; popup shows at 1212-1213 s
20:12-20:15 | STATION_LEVEL | Frog Screams 862 -> 902 (1208 s L862 692ar/144as blue; 1213 s L864 181as; 1214 s L878 882as; 1215 s L902 13.4at blue; "x2 Profit" bonus tag at 1215 s, 2 stars)
20:16-20:22 | STATION_LEVEL | Frog Screams L923 (145at grey, coins 77.3at - 87.5at) stopped for money 1216-1221 s
20:22 | STATION_LEVEL | Frog Screams L930 (320at, grey; coins 82.5at, 1222 s)
20:23 | VIEW | (1223 s) camera pans up to Spider Silk (popup near the top of the screen)
20:23-20:25 | STATION_LEVEL | Spider Silk L982 (42.3as blue, 1223 s) -> L984 (53as, 1224 s) -> L998 (259as, 1225 s); coins 1.24au; bonus 2 stars
20:26 | TASK | banner "Upgrade Spider Silk to level 1000" - done (green check at 1226-1228 s), rewards "1" (free, check) and "18" (pass, locked). The top-left reward icon changes and its counter goes 33397 -> 33398 at 1226 s. Spider Silk therefore reached L1000 at ~1225.5-1226 s (MAX level itself not seen in a popup)
20:26 | VIEW | (1226 s) camera back down to Frog Screams: L930 320at blue (coins 1.24au)
20:27 | STATION_LEVEL | Frog Screams L933 (449at, grey, coins 164at); banner still visible
20:28 | VIEW | (1228 s) camera pans up to Mystic Mushrooms; L977 43.9at blue (coins 105au); banner of the Spider Silk task still fading out
20:29-20:31 | STATION_LEVEL | Frog Screams L935 (564at blue, 1229 s) -> L948 (2.46au, 1230 s) -> L962 (12.1au grey, coins 9.64au, 1231 s)
20:32-20:33 | STATION_LEVEL | Mystic Mushrooms L979 (55at blue, 1232 s) -> L993 (269at blue, 1233 s, coins 7.81au)
20:33-20:34 | STATION_LEVEL | Mystic Mushrooms 993 -> 1000 (inferred): coins drop 7.81au -> 5.1au between 1233 and 1234 s, the view is back on Frog Screams at 1234 s (MAX not seen in a popup)
20:34-20:44 | STATION_LEVEL | Frog Screams L962 (12.1au grey, coins 5.1au -> 11.1au) stopped for money 1234-1240 s (shop floor view in between at 1241-1244 s)
20:41-20:43 | VIEW | (1241-1243 s) shop floor view (customers queue, icons with counts above the counter), coins 6.66au -> 11.1au; no purchases; back in the cellar at 1244 s
20:45 | STATION_LEVEL | Frog Screams L962 (12.1au, now blue, coins 12.6au)
20:46 | STATION_LEVEL | Frog Screams L978 (73.7au blue, coins 721au)
20:47-20:50 | STATION_LEVEL | Frog Screams L984 (146au grey, coins 123au) stopped for money 1247-1250 s
20:51-20:54 | STATION_LEVEL | Frog Screams L985 (163au grey, coins 130au -> 146au) stopped for money 1251-1254 s
20:55-20:57 | STATION_LEVEL | Frog Screams L986 (183au grey, coins 17.5au, 1255-1256 s) -> L988 (229au grey, coins 94.5au, 1257 s)
20:58-21:01 | STATION_LEVEL | Frog Screams L990 (287au grey, coins 56au) stopped for money 1258-1261 s
21:02-21:03 | STATION_LEVEL | Frog Screams L992 (360au grey, coins 31.8au) 1262-1263 s
21:04-21:08 | STATION_LEVEL | Frog Screams L993 (403au grey, coins 75.5au -> 292au) stopped for money 1264-1268 s
21:09 | STATION_LEVEL | Frog Screams L998 (711au blue, coins 10.9av); last burst
21:10 | STATION_LEVEL | Frog Screams L1000 reached (1270 s): popup "Level 1000", 3 stars, bonus tag "x2 Profit" (grey), price hidden behind the banner; coins 9.46av
21:10 | TASK | banner "Upgrade all stations to level 1000" with a medal icon; rewards "15" (free) and "30" (pass, locked); appears at 1270 s, green check on the free reward at 1271 s (done, the last of 15 event tasks)
21:13 | STATION_LEVEL | Frog Screams "Level 1000, MAX" (button grey with text MAX, 3 stars) at 1272-1273 s; coins 9.5av
21:12-21:13 | OTHER | (1271-1273 s) a small avatar/person bubble appears above the cellar (visitor icon), unrelated
21:13 | OTHER | (1273.25-1273.5 s) the Potion Shop event dialog opens (tapped the event/trophy icon): title "Potion Shop - Take off your gear and brew fantastic potions!", "Rewards 15/15", tabs Free / Pass, buttons "Activate" (top right) and "Exit". Visible rows: Unlock Dragon Scale Dust (free 10, check; pass 180 locked), Unlock Unicorn Horn Shavings (20 check; pass 360 locked), Unlock Mermaid Tears (5 check; pass 10 locked), Unlock Beetle Juice (2 check; pass 36 locked). All free rewards have green checks. Footer: "Event ends in: 1d 7h"
21:13-21:14 | REWARD | all 15/15 event rewards claimed (free track); "Pass" track rewards locked (not purchased), none claimed
21:14 | OTHER | (1274.0 s) Leaderboard dialog opens (left tab icon), first empty (loading, 1274.25-1274.5 s)
21:14-21:15 | OTHER | (1274.75-1276 s) Leaderboard "Normal Division GYRvQ_a07a" "Complete the Potion Shop event as fast as possible!": rank 1 "x" (green, the player) 100 % 21m 3s; 2 Eloki 100 % 42m 48s; 3 Kleincool 100 % 48m 29s; 4 Globi91 100 % 2h 9m 46s; 5 Player6049 100 % 2h 30m 33s; 6 Felsar 100 % 3h 20m 48s; 7 Kenster 100 % 4h 26m 31s; 8 Gamer67 100 % 4h 57m ?s (cut off). "Division closes in: 1d 7h". The video ends on this screen at 1276 s. The leaderboard time 21m 3s = event completed at video ~21:10 minus ~7 s offset (the task says ~21:03; the Level 1000 banner is seen at 1270 s)
```
