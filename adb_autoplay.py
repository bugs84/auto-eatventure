"""
adb_autoplay.py - Main entry point and game loop

This file contains only the high-level game loop logic.
Device interaction, template matching, and game actions
are in their respective modules.
"""

import time
import random

from dotenv import load_dotenv

from constants import Constants
from device import Device
from template_matcher import TemplateMatcher
from game_actions import GameActions

load_dotenv()


class Timer:
  def __init__(self, name=""):
    self.name = name

  def __enter__(self):
    self.start_time = time.time()

  def __exit__(self, exc_type, exc_val, exc_tb):
    elapsed_time = time.time() - self.start_time
    print(f"{self.name} elapsed time: {elapsed_time} seconds\n")


class AutoEatventure:
  """Main bot orchestrator. Runs the game loop."""

  def __init__(self):
    self.device = Device()
    self.matcher = TemplateMatcher(self.device.sc)
    self.loc = Constants(self.device.sc)
    self.actions = GameActions(
      self.device, self.matcher, self.loc)

  def start_playing_game(self):
    """Main game loop — runs indefinitely."""
    count = 0
    new_level_first_food_icon_swipe = False
    new_level_started = True
    swipe_pattern = [
      self.loc.swipe_layout_down_coords,
      self.loc.swipe_layout_down_coords,
      self.loc.swipe_layout_down_coords,
      self.loc.swipe_layout_up_coords,
      self.loc.swipe_layout_up_coords,
      self.loc.swipe_layout_up_coords,
    ]
    swipe_count = 0
    nothing_to_update_count = 0

    while True:
      count += 1

      # ── Stale state: force restart ──────────────────────
      if nothing_to_update_count > 50:
        print('Nothing to update — restarting app.')
        self.device.start_app()
        time.sleep(1)
        self.device.click(self.loc.null_click_coords)
        time.sleep(1)

      # ── Stale state: swipe to reveal hidden elements ────
      print('nothing_to_update_count',
            nothing_to_update_count)
      if (nothing_to_update_count >= 15
          and nothing_to_update_count % 5 == 0):
        coords = swipe_pattern[
          swipe_count % len(swipe_pattern)]
        self.device.swipe(**coords)
        time.sleep(3)
        swipe_count += 1

      # ── Capture screenshot ──────────────────────────────
      with Timer("Capturing screenshot"):
        self.device.capture_screenshot()

      # ── Close accidental popups (~every 5 min) ──────────
      if count % 150 == 0:
        self.actions.close_accidental_popups()

      # ── Upgrade items (every 5th iteration) ─────────────
      with Timer("Upgrading items"):
        if count % 5 == 0 and self.actions.is_having_upgrade():
          print('Upgrading items')
          if new_level_started:
            self.actions.do_upgrades(upgrade_count=50)
            new_level_started = False
          else:
            self.actions.do_upgrades()
          self.device.capture_screenshot()

      # ── Find and open boxes (every 2nd iteration) ───────
      if count == 1 or count % 2 == 0:
        with Timer("Finding boxes"):
          print('finding boxes')
          self.actions.open_boxes()

      # ── Find food icons ─────────────────────────────────
      with Timer("Finding food icons"):
        print('finding food icons')
        food_icon_locations = \
          self.actions.get_food_icon_locations()

      # ── First food icon after new level: reposition ─────
      if (len(food_icon_locations) > 0
          and not new_level_first_food_icon_swipe):
        y_coords = [c[1] for c in food_icon_locations]
        min_y_idx = y_coords.index(min(y_coords))
        swipe_x = food_icon_locations[min_y_idx][0]
        self.device.swipe(
          start={'y': min(y_coords), 'x': swipe_x},
          end={
            'x': swipe_x,
            'y': self.device.sc.food_icon_tooltip_boundary_y
          })
        new_level_first_food_icon_swipe = True
        time.sleep(3)
        self.device.start_app()
        time.sleep(3)
        self.device.capture_screenshot()
        continue

      # ── Adjust layout if food icon too close to top ─────
      if len(food_icon_locations) > 0:
        nothing_to_update_count = 0
        is_danger = False
        for c in food_icon_locations:
          if c[1] <= self.device.sc.food_icon_top_boundary_y:
            is_danger = True
            self.device.swipe(
              **self.loc.swipe_layout_little_up_coords)
            time.sleep(3)
            self.device.start_app()
            time.sleep(1)
            break
        if is_danger:
          self.device.capture_screenshot()
          continue

      # ── Update nothing_to_update counter ────────────────
      if len(food_icon_locations) == 0:
        nothing_to_update_count += 1
      else:
        nothing_to_update_count = 0

      # ── Click food icons to upgrade ─────────────────────
      if len(food_icon_locations) != 0:
        with Timer("Clicking food icons"):
          random.shuffle(food_icon_locations)
          self.actions.upgrade_food_items(
            food_icon_locations)
      else:
        # ── Check next level (every 10th, no food) ────────
        if count % 10 == 0:
          print('next level check')
          gone = self.actions.check_to_go_next_level()
          if gone:
            swipe_count = 0
            nothing_to_update_count = 0
            new_level_first_food_icon_swipe = False
            new_level_started = True


# ── Entry point ───────────────────────────────────────────────

bot = AutoEatventure()
bot.device.start_app()
bot.actions.init_game()
bot.start_playing_game()
