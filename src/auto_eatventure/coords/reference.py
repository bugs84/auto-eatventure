"""Screen positions at the reference resolution (1220x2712).

ScaledCoords scales them to the phone's resolution: Point, Region and
Swipe values in both directions, numbers ending in _x horizontally and
numbers ending in _y vertically. Other values are not scaled.
"""

# Lowercase names: they are positions, read through ScaledCoords
# pylint: disable=invalid-name

from auto_eatventure.coords.geometry import Point, Region, Swipe

REFERENCE_WIDTH = 1220
REFERENCE_HEIGHT = 2712

# ── Restaurant screen ─────────────────────────────────────────────────

# White settings gear (top right). A dialog dims it, so it tells
# whether a dialog covers the screen (station popups don't dim it).
settings = Point(1134, 161)
settings_roi = Region.around(settings, 30, 30)

# Empty spot (restaurant just below the top bar) tapped to close
# station popups. y is only a fallback: the status bar height differs
# between phones, so at start the spot is placed below the top bar's
# black line (actions/null_spot.py). Too high, the top bar catches the
# tap and the popup stays open (OnePlus Nord 3); too low, it can hit a
# customer bubble, whose Investor dialog starts an ad with Claim
# (Xiaomi at y=340, 301 there).
null_spot_fallback = Point(886, 278)

# The top bar ends with a black line across the screen. Shorter runs of
# black rows are gaps between HUD elements, not the line (Xiaomi: 13
# rows; one row under two dialogs).
top_bar_line_min_rows_y = 5
# The null spot is this far below the line: still on the restaurant
# (the top bar catches taps, popups stay open) but above the tables,
# whose customer bubbles open dialogs (Investor's Claim starts an ad)
null_spot_below_top_bar_y = 22

# ── Start dialogs ─────────────────────────────────────────────────────

close_offline_earnings = Point(974, 1012)

# ── Upgrades dialog ───────────────────────────────────────────────────

upgrade_button = Point(1093, 2524)
# Red badge on the upgrade button (shown while an upgrade can be
# bought). The badge pulses, the area fits its largest size.
upgrade_badge_roi = Region(971, 2407, 1107, 2542)

# Buy button of the first row in the Upgrades dialog
first_upgrade_buy = Point(968, 1115)
first_upgrade_buy_roi = Region.around(first_upgrade_buy, 100, 34)

close_upgrades = Point(1035, 908)
close_upgrades_roi = Region.around(close_upgrades, 40, 40)

# ── Next level / next city ────────────────────────────────────────────

next_level_button = Point(127, 2521)
renovate_button = Point(593, 1912)
fly_next_city_button = Point(593, 1892)
# "Okay" of the "Welcome to <city>" dialog after a flight
welcome_okay_button = Point(618, 1695)
# "Open" of the first stand after a renovation or a flight
first_stand_open_button = Point(604, 1604)

chest = Point(110, 734)
close_chest = Point(1127, 200)

# ── Station upgrade icons ─────────────────────────────────────────────

# Height range of the white arrow in the pulsing red upgrade icon
# (measured on screen 23-39 on Xiaomi, 27-44 on OnePlus Nord 3)
upgrade_arrow_min_height_y = 22
upgrade_arrow_max_height_y = 48

# Icons below this y are ignored: keeps taps off the club button and
# off the red badge of the bottom Upgrades button, which looks like a
# station upgrade icon (~2474)
station_icon_max_y = 2200
# Icons below this y AND within the left side button zone are ignored
# (their station box may overlap the club button in the bottom-left
# corner)
club_button_zone_top_y = 2029
# Icons above this y are too close to the top of the viewport and
# trigger a swipe up
station_icon_min_y = 1100
# Icons above this y need a special tap to avoid the tooltip
station_icon_tooltip_y = 1240

# Y offset when tapping a station icon to open its upgrade menu
station_tap_offset_y = 22
# Small shift of the station icon tap to avoid tapping an adjacent
# station when two stations are close together
station_tap_shift_x = 2
station_tap_shift_y = 2
# Click-and-hold gesture that opens the "buy better food" menu,
# relative to the station icon (right of it, above it)
better_food_hold_offset_x = 20
better_food_hold_offset_y = 130
# Tap on the "buy better food" button, left of the station icon
better_food_tap_offset_x = 110

# Width of the side UI buttons (restaurant race, food boxes, etc.)
# pinned to the left/right screen edges. Station taps are kept at least
# this far from either edge to avoid triggering them.
side_button_zone_width_x = 180

# ── Restaurant scrolling ──────────────────────────────────────────────
# Distance kept to 650px: the usable playfield height (excluding side
# buttons/ad banner zones) is only ~820px, so a swipe close to that
# length would risk jumping straight over a row of stations. 650px
# leaves ~170px (~20%) overlap between consecutive swipes.

swipe_down = Swipe(Point(646, 1889), Point(646, 1239))
swipe_up = Swipe(Point(646, 604), Point(646, 1254))
swipe_little_up = Swipe(Point(646, 604), Point(646, 1133))

# ── Left button column ────────────────────────────────────────────────
# Taps on the left button column (helper, Food Delivery truck) use this
# x, right of the buttons' center (~75). Not side_button_zone_width_x,
# which keeps station taps away from the side buttons. On some phones
# (OnePlus Nord 3) the column is partly hidden behind the screen edge
# and taps on the buttons' left part (< ~90) are ignored.
side_button_tap_x = 120

# ── Active Skills / Popular Dish ──────────────────────────────────────
# Black skill circle at the top center opens the Active Skills dialog.
# Single circle while all skills are ready (cooldown resets on every
# renovation / fly to a new city); it splits into two circles while
# Popular Dish is active or cooling down.
skills_circle = Point(610, 325)

# Select / Start / Stop button of the Popular Dish row (same position).
# Its search area keeps the Sold Out row's own Select button (~305px
# lower) out of the match.
popular_dish_button = Point(942, 1385)
popular_dish_button_roi = Region.around(popular_dish_button, 175, 90)

# First (leftmost) tile in the "Select a dish" dialog. The grid has up
# to 3 tiles per row and is centered, so the first tile moves with the
# number of dishes: 3+ dishes / 2 dishes / 1 dish. Tapping a gap or a
# grey (unavailable) tile does nothing, so they are tried in order.
first_dish_candidates = (
  Point(360, 1304), Point(486, 1304), Point(610, 1304))

# ── Food Delivery ─────────────────────────────────────────────────────
# Truck button in the left button column. It moves up when the button
# above it is missing, so it is searched in this area.
food_delivery_roi = Region(0, 283, 226, 960)

# Accept button of the first order in the "Food Delivery" dialog
food_delivery_accept = Point(610, 1166)
food_delivery_accept_roi = Region.around(food_delivery_accept, 147, 79)

# ── Invite a Helper ───────────────────────────────────────────────────
# Helper (person) button, the top one in the left button column
helper_button = Point(side_button_tap_x, 434)
# Search area of the "available" template (lower part of the button:
# person's body + the empty line where a countdown / ad icon would be)
helper_roi = Region(0, 400, 170, 560)

# Search area of the first helper's Invite button in the "Invite a
# helper" dialog. The dialog is centered, so on a shorter screen it is
# higher than the scaling says (LG G6 2:1: ~90 px). The area covers the
# first row on both, but not the second row (~230 px lower).
helper_invite_roi = Region(657, 840, 951, 1130)

# ── Adventures ────────────────────────────────────────────────────────
# Party popper, the first white button in the right column; it opens
# the "Events" dialog with the Adventures at the bottom
events_button = Point(1141, 429)

# Red X of the "Events" dialog and of an adventure's level dialog
# (e.g. "Feast on Olympus"); the red share around it tells which one
# is open
events_close = Point(1056, 797)
events_close_roi = Region.around(events_close, 34, 34)
adventure_level_close = Point(971, 734)
adventure_level_close_roi = Region.around(adventure_level_close, 34, 34)

# Swipe inside the "Events" dialog to its bottom (Adventures are last)
events_scroll = Swipe(Point(610, 1717), Point(610, 859))

# Search area of the adventures' key icons in the "Events" dialog;
# the Events section above them varies, so they are searched for
events_list_roi = Region(68, 791, 1152, 2181)
# An adventure's Enter button relative to the center of its key icon
adventure_enter_offset_x = 70
adventure_enter_offset_y = 118

# Level dialog: right arrow (shown when the last level is not
# selected), keys counter icon (key or ad) and "Complete last level"
adventure_right_arrow = Point(898, 1045)
adventure_right_arrow_roi = Region.around(adventure_right_arrow, 73, 96)
adventure_counter_roi = Region(474, 1751, 723, 1876)
adventure_complete_last = Point(412, 1949)

# Full screen reward cards: taps reveal them one by one, then the
# summary shows a red X in the top right corner. An empty area of the
# screen's background tells the reward screen.
adventure_reward_bg_roi = Region(0, 395, 181, 621)
adventure_reveal_tap = Point(610, 1356)
adventure_summary_close_roi = Region.around(Point(1118, 186), 56, 56)

# ── Potion Shop event ─────────────────────────────────────────────────
# The event's cauldron button in the right column (main screen: 3rd
# white button, inside the event: 2nd); its place depends on the
# buttons above it, so it is searched in the column
potion_shop_button_roi = Region(1080, 280, 1220, 1250)
# Enter (main screen) and Exit (inside the event) of the "Potion Shop"
# dialog, at the same place
potion_shop_enter_exit = Point(610, 2054)
potion_shop_enter_exit_roi = Region.around(potion_shop_enter_exit, 180, 80)
# Red X of the "Potion Shop" dialog
potion_shop_dialog_close = Point(1057, 660)
# Its list of rewards, scrolled to the bottom by a few swipes: the last
# reward (all stations level 1000) gets a green check when done
potion_shop_rewards_swipe = Swipe(Point(452, 1808), Point(452, 1017))
potion_shop_last_reward_roi = Region.around(Point(810, 1836), 90, 79)
# Green event coin left of the coin counter: shown only inside
potion_shop_coin_roi = Region(100, 60, 300, 260)

# Cauldron button (2nd from the right in the bottom bar, after a
# Potion Kettle was bought) and its red "!" badge (a potion can be
# brewed); the badge area mirrors upgrade_badge_roi
potion_shop_cauldron_button = Point(915, 2556)
potion_shop_cauldron_badge_roi = Region(793, 2439, 929, 2574)
# Cauldron dialog: Brew tab, the list of potions (icons on the left,
# Brew / Claim buttons on the right, level with the icon) and the red X
potion_shop_brew_tab = Point(184, 625)
potion_shop_brew_list_roi = Region(900, 900, 1190, 2600)
potion_shop_potion_icons_roi = Region(30, 900, 260, 2600)
# A potion's level label ("Lvl 3") relative to its icon's center; in
# the Brew list it shows the level the next brew makes
potion_shop_level_label = Region(-82, 76, 87, 132)
# The Brew list is longer than the screen (Divine, Golden, ... below)
potion_shop_brew_list_swipe = Swipe(Point(610, 2260), Point(610, 1017))
# Active Potions tab: the active potions, each with a Bottle button
# (relative to its icon's center like the level label)
potion_shop_active_tab = Point(429, 633)
potion_shop_bottle_row = Region(731, -20, 1013, 115)
potion_shop_cauldron_close = Point(1130, 249)
potion_shop_cauldron_close_roi = Region.around(
  potion_shop_cauldron_close, 40, 40)

# The event's map is taller than the screen. The shop with all its
# stations fits on it when its landmarks are at their _y: the ink, quill
# and books on the counter's right part (hidden by the customers' prices
# when the counter is full), the barrel in the bottom left corner and
# the skull on the wall above the counter (shown only when the map is
# scrolled too far up). Each is searched in its column and moved there
# by swipes on the floor right of the kettle (no station there).
potion_shop_landmark_roi = Region(780, 230, 1050, 2450)
potion_shop_landmark_y = 548
potion_shop_barrel_roi = Region(80, 230, 400, 2450)
potion_shop_barrel_y = 2133
potion_shop_skull_roi = Region(400, 230, 820, 2450)
potion_shop_skull_y = 6
# Below the shop the cellar ("Dig a Cellar" upgrade) has more stations:
# its landmark is the barrel with a candle at its entrance (_y on the
# shop view like the others); the cellar view is the map scrolled to
# potion_shop_cellar_view_y (offset from the shop view).
potion_shop_cellar_roi = Region(150, 230, 700, 2450)
potion_shop_cellar_y = 2754
potion_shop_cellar_view_y = -1970
# Stations by their upgrade arrow: Beetle Juice on the shop view, the
# cellar's best ones on the cellar view. Tapped like an arrow, a station
# shows a popup above it (up to _popup_y), "MAX" at level 1000.
potion_shop_beetle_station = Point(959, 2122)
potion_shop_spider_station = Point(848, 852)
potion_shop_frog_station = Point(738, 1716)
potion_shop_mushrooms_station = Point(1071, 1236)
potion_shop_station_arrow_x = 113
# Icons of the Upgrades dialog's rows (potion_shop_upgrade_* templates)
potion_shop_upgrades_roi = Region(60, 980, 420, 2000)
potion_shop_station_popup_y = 508
potion_shop_aligned_y = 25
potion_shop_max_swipe_y = 1000
potion_shop_swipe_x = 830
potion_shop_swipe_from_y = 1469
