# Cloud save (Google Play Games): notes for a possible automation

Seen 2026-10-31 on the Xiaomi (dad's phone, e0cb42c1, 1080x2400,
Eatventure 1.54.0, last updated 2026-09-22) after the user had played
the same account on another phone.

## What the game shows at start

1. `cs_01_offline_earnings.png`: the usual "Offline Earnings" dialog
   first (12.4B, "Collect x2" = an ad, never tap it). Closed by its red
   X at (866, 900).
2. `cs_02_cloud_save_found.png`: then "Cloud Save found!" ("It looks
   like you have made progress on another device. Would you like to
   load that progress from the cloud or keep your current
   progress?"). Two cards:
   - **Local** (red title): "3780 - Santiago / Taco Stand / Bugs" and
     8 icons (the city's progress), red button **Use Local** at
     ~(324, 1626).
   - **Cloud** (green title): "3780 - Santiago / Tapas Bar / Bugs"
     (further: the next restaurant of the city). With an older app
     than the one that saved it, instead of a button: red text
     **"Update your game to load this progress!"** - the cloud save
     can't be loaded until Eatventure is updated in Google Play. A
     "use cloud" button was not seen (expected there with the same
     version).
   - Red X top right at ~(910, 780): its effect is unknown (keeps
     local? asks again next start?) - not tapped.

Coordinates are of the 1080x2400 screenshot (reference 1220x2712:
multiply by 1.13).

## Risks for the bot as it is

- `start_dialogs.wait_until_ready()` / `popups.close_popup()` close
  dialogs by their red X: on this dialog that may keep the local
  (older) progress and the cloud save may be overwritten later. The
  dialog should be detected before any X is tapped.
- The bot doesn't update the app: an outdated app blocks the cloud
  save.

## Ideas if automated

- Template of the "Cloud Save found!" title (or of the Local/Cloud
  card titles) in `matching_screenshots/`, checked in
  `wait_until_ready()` before the red-X handling.
- A `.env` switch (e.g. `CLOUD_SAVE=cloud|local|ask`): "cloud" taps the
  cloud card's button when shown; when the "Update your game" text is
  there, log a key event (ERROR - app update needed) and stop instead
  of choosing; "ask" stops the bot and leaves the dialog to the user.
- App version: `adb shell dumpsys package com.hwqgrhhjfd.idlefastfood |
  grep versionName`; an update is in Google Play (user's decision, not
  done by the bot).

## After the update (2026-10-31 08:45)

Updated in Google Play (57.10 MB download) 1.54.0 -> 1.55.5. The game
was then started (monkey launcher intent) and after 30 s it was straight
in the restaurant (tacos, 27.3T coins): no Offline Earnings and no
"Cloud Save found!" dialog - the dialog left open before the update was
not shown again. Whether the local or the cloud save got loaded was not
clear from the screen (`xiaomi_20261031_084528.png` in
`captured_screenshots_on_the_fly/`).

Correction: the dialog came later. At 08:52 (about 7 min after the
start) "Cloud Save found!" was shown over the game, now with both
buttons (`cs_03_cloud_save_after_update.png`): red **Use Local** at
~(324, 1626) and green **Use Cloud** at ~(755, 1626) (1080x2400). No X
on this dialog. So the dialog doesn't come right at start: the bot
would have to watch for it during play too, not only in
`wait_until_ready()`.

## Use Cloud (2026-10-31 09:42)

Tapping **Use Cloud** at (755, 1622) shows at once "Restart required!"
("Your Cloud Save progress has been downloaded. Please restart the app
to continue playing.") with one blue button **Close Game** at
~(540, 1395) (`cs_04_restart_required.png`). No X. The game must then
be started again (automation: tap Close Game, then
`device.start_app()` + `wait_until_ready()`).

After Close Game (540, 1395) the game was closed; started again it
loaded the cloud save: Tapas Bar (shrimp, beer), 564ab coins (local
had 249T), then the usual Offline Earnings (closed by its X).

## Second time (2026-11-06 00:24, the full flow by hand)

The user had played the account on their phone; the Xiaomi's bot and
game had been stopped before (no bot ran during the whole flow, so no
red-X handling could pick Local). Eatventure 1.55.5, no update needed.

1. Game started (monkey launcher intent): Offline Earnings (41.4ab,
   "Collect x2" = ad, not tapped) closed by its red X at (866, 900).
2. **"Cloud Save found!" came ~20 s later**, right after that dialog
   (on 2026-10-31 it took ~7 min; the timing varies)
   (`cs_05_cloud_save_found_2026-11-06.png`, coin animation over it):
   Local "3949 - Madrid / Drive Thru", Cloud "3950 - Amsterdam /
   Lemonade Stand" (the newer one, from the other phone). Found by a
   template of the title cropped from `cs_03` ((280, 735)-(800, 825) of
   the 1080x2400 screenshot), TM_CCOEFF_NORMED > 0.8.
3. **Use Cloud** at (755, 1622) -> "Restart required!" -> **Close
   Game** at (540, 1395): the game process ends (`pidof` empty).
4. Started again: after ~30 s the cloud save was loaded, Amsterdam's
   Lemonade Stand, 3.74B coins, 264K gems, no dialog
   (`cs_06_after_cloud_load_2026-11-06.png`). The bot was started after
   that.

Rule of thumb: before the account is played on another phone, the
Xiaomi's bot (and its watchdog) must be stopped and the game closed;
afterwards the cloud save is loaded as above before the bot starts,
else both phones overwrite each other's save.
