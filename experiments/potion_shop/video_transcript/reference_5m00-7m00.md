# Reference transcript: video 5:00-7:00 (Sonnet test, 1 fps sheets only)

Made by a Sonnet subagent from 15 contact sheets (1 fps) + 8 single
frames, before the dialog sheets existed (~108k tokens, 2.5 min). Use it
to check a cheaper model or a changed prompt on the same 2 minutes
(`--download-sections "*300-420"`, burnt-in times then start at 0).

Times are m:ss of the video. Prices in parentheses.

```
5:00 | OTHER | Cauldron red (Sizzle brewing). Dragon Scale Dust popup Level 819 (43.8aj)
5:01 | STATION_UNLOCK | Mermaid Tears: dashed tile, "Unlock 2.05T"
5:02 | TASK | Banner "Unlock Mermaid Tears", rewards 5 + 10
5:02-5:14 | STATION_LEVEL | Mermaid Tears hold burst 4 -> 644 (1 frame/s: 4, 17, 44, 104, 163, 223, 285, 344, 404, 464, 525, 585, 644)
5:12-5:14 | TASK | "Upgrade Mermaid Tears to level 500" done
5:17-5:20 | STATION_LEVEL | Bat Wing Extract 867 -> 903
5:21 | BREW_DONE | Sizzle Serum Lvl 4 (Claim)
5:22 | BREW_LIST | Swift Lvl5 (60 Bat + 30 Dragon); Sizzle Lvl5 (60 Dragon + 30 Unicorn); Perfect Lvl1 (21 Bat + 9 Unicorn); Double Lvl1 (12 Mermaid + 9 Dragon)
5:23 | BREW_START | Double Draught
5:24-5:25 | UPGRADE_BOUGHT | Speedy spooling technique (Spider Silk regenerates faster, 11.3aj), Double distilled (Mermaid x25, 61.5aj), Apply distortion (Frog x3, 68.5aj)
5:26-5:36 | UPGRADE_BOUGHT | Mix with glitter (Unicorn x50, 640aj), Anti-stick coating (Spider Silk x5, 1.11ak), Crystal clear (Purified Water x10, 1.58ak)
5:27-5:34 | STATION_LEVEL | Unicorn Horn Shavings 636 -> 806 (button grey = not affordable)
5:36-5:53 | UPGRADE_BOUGHT | Use Transilvanian Bats (Bat Wing x75, 75.1ak)
5:38 | BREW_DONE | Double Draught Lvl 1
5:39 | BREW_START | Double Draught
5:40-5:49 | STATION_LEVEL | Bat Wing Extract 908 -> 992
5:53-5:54 | UPGRADE_BOUGHT | Rare species blend (Beetle x25), Lure talent from rivals (+1 Alchemist, 130ak), Remake with popular Djinn (Djinn x50)
5:54-5:55 | UPGRADE_BOUGHT | Poke gently (Frogs recover faster, 30.9al), Add rubies for color (Dragon Scale x75, 60al)
5:58-6:15 | STATION_LEVEL | Dragon Scale Dust 819 -> 986; Unicorn 806 -> 819; Bat Wing 993
6:17-6:18 | UPGRADE_BOUGHT | Enhanced mineral content (Purified Water x25, 315al), Discard first runnings (Mermaid x50, 410al), Layer with tritone (Frog x5, 3.02am)
6:18-6:51 | UPGRADE_BOUGHT | Glow-in-the-Dark Formula (Beetle x50, 328am)
6:19 | BREW_DONE | Double Draught Lvl 3 (no Lvl 2 dialog seen: missed between frames)
6:20 | BREW_START | Double Draught
6:21-6:27 | STATION_LEVEL | Unicorn 822 -> 948
6:28-6:33 | STATION_LEVEL | Mermaid Tears 652 -> 846
6:34-6:35 | STATION_LEVEL | Dragon Scale Dust 989 -> 997
6:38-6:51 | STATION_LEVEL | Unicorn 948 -> 985 (about 1 level/s)
6:48 | BREW_DONE | Double Draught Lvl 4
6:49 | BREW_START | Swift Serum (60 Bat + 30 Dragon)
6:51-6:52 | UPGRADE_BOUGHT | Discard weak strands (Spider Silk x25), Post job notices (+1 Alchemist, 4.15an), Send through amplifier (Frog x10, 15.1an)
5:24-6:53 | UPGRADE_SEEN_SKIPPED | all customer rows: Host an alchemy workshop +2 (12.5M), Put up a sign +1 (15T), Advertise in 'Wizard Monthly' +2 (2.25ac), Get a guild endorsement +1 (4af), Guarantee efficacy +1 (3ai), Sponsor a local festival +1 (6.4al) - never bought although affordable
6:55-6:56 | STATION_LEVEL | Unicorn 991 -> 1000 (MAX)
6:56 | TASK | "Upgrade Unicorn Horn Shavings to level 1000", 200 gems
6:57 | STATION_UNLOCK | Djinn's Breath (Level 1, 1.54B), 6:59 Level 28
OTHER | Boost x12 "+40 min" unchanged the whole time (countdown 5h15m12s -> 5h13m13s); no bottling seen
```

Reader's notes: hard to read were the ingredient counts above the
cauldron (small, often covered), the order of purchases within one
second, and star counts. Suggestions it made: closer frames at each
BREW_START, more frames per second while a dialog is open (-> dialog
sheets), state clearly that burnt-in times are the video time.
