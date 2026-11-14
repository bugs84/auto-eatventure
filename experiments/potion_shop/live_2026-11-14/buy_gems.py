"""Buy gem items of the shop under the cart button: "x2 Profit Boost"
(45 gems, +20 min, capped at 2 h) or "Instant Cash" (30 gems).

Usage: .venv/bin/python experiments/potion_shop/live_2026-11-14/buy_gems.py
       xiaomi|lg x2|cash COUNT

Pauses the phone's watchdog and bot, buys up to COUNT, closes the shop
and starts the watchdog again (race_schedule.sh). Every tap is checked
by a template first: only the item card's gem price, its dialog's gem
button and the red X are ever tapped - never an offer for real money.
Each purchase is written to gems.log (its total per phone may not go
over GEM_LIMIT of the phone's .env, default 0: nothing is bought) and
to the phone's logs/autoplay.log; only a reached limit goes to its
logs/key_events.log (key milestones, nothing frequent).
"""
import datetime
import os
import re
import subprocess
import sys
import time

import cv2
import numpy as np
from dotenv import dotenv_values

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, 'gem_templates')
GEMS_LOG = os.path.join(HERE, 'gems.log')
BASE = '~/programs/auto-eatventure'
TEMPLATE_WIDTH = 1440  # the templates are cut on the LG
THRESHOLD = 0.85
# The cards' gem prices look alike (30 / 45: 0.92)
THRESHOLDS = {'card_price': 0.97, 'x2_card_price': 0.97}
PHONES = {
  'xiaomi': ('<serial>', os.path.join(BASE, 'auto-eatventure'),
             'xiaomi_watchdog', 'start-xiaomi'),
  'lg': ('<serial>', os.path.join(BASE, 'auto-eatventurelg'),
         'lg_watchdog.sh', 'start-lg'),
}
# item -> (gems, card price, dialog title, dialog buttons, text)
ITEMS = {
  'cash': (30, 'card_price', 'confirm_title', ('confirm_button',),
           'Instant Cash'),
  'x2': (45, 'x2_card_price', 'x2_title', ('x2_button', 'x2_extend'),
         'x2 Profit Boost +20m'),
}


def log(text):
  print(f'{datetime.datetime.now():%H:%M:%S} {text}', flush=True)


def gem_limit(folder):
  """GEM_LIMIT of the phone's .env (see .env-sample), 0 when unset."""
  value = dotenv_values(os.path.join(folder, '.env')).get('GEM_LIMIT')
  return int(value.strip()) if value and value.strip() else 0


def bot_log(folder, text, key=False):
  """A line in the bot's autoplay.log, with key=True in its
  key_events.log (their formats, see logger.py); the bot is stopped
  meanwhile."""
  now = datetime.datetime.now()
  stamp = f'{now:%Y-%m-%d %H:%M:%S},{now.microsecond // 1000:03d}'
  name, line = (('key_events.log', f'{stamp}  GEMS - {text}') if key
                else ('autoplay.log',
                      f'{stamp} [INFO ] buy_gems: Gems: {text}'))
  with open(os.path.join(folder, 'logs', name), 'a',
            encoding='utf-8') as file:
    file.write(line + '\n')


def spent(name):
  if not os.path.exists(GEMS_LOG):
    return 0
  with open(GEMS_LOG, encoding='utf-8') as file:
    return sum(int(gems) for phone, gems in re.findall(
      r'^\S+ \S+ (\w+): bought .* for (\d+) gems', file.read(), re.M)
      if phone.lower() == name)


class Phone:
  def __init__(self, name, serial):
    self.name = name
    self.serial = serial
    self.templates = {}
    self.scale = None

  def adb(self, *args):
    return subprocess.run(['adb', '-s', self.serial, *args],
                          capture_output=True, check=False).stdout

  def screen(self):
    self.adb('shell', 'input', 'keyevent', '224')
    data = self.adb('exec-out', 'screencap', '-p')
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if self.scale is None:
      self.scale = image.shape[1] / TEMPLATE_WIDTH
    return image

  def template(self, name):
    if name not in self.templates:
      image = cv2.imread(os.path.join(TEMPLATES, name + '.png'))
      if self.scale != 1:
        image = cv2.resize(image, None, fx=self.scale, fy=self.scale,
                           interpolation=cv2.INTER_AREA)
      self.templates[name] = image
    return self.templates[name]

  def find(self, image, name):
    """Center of the template, None below THRESHOLD."""
    template = self.template(name)
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, (x, y) = cv2.minMaxLoc(result)
    h, w = template.shape[:2]
    log(f'  {name}: {score:.3f}')
    if score < THRESHOLDS.get(name, THRESHOLD):
      return None
    return (x + w // 2, y + h // 2)

  def tap(self, point):
    self.adb('shell', 'input', 'tap', str(point[0]), str(point[1]))
    time.sleep(2.5)

  def swipe(self, image, up):
    """Scroll the shop along its right margin (beside the cards)."""
    h, w = image.shape[:2]
    x = str(int(w * 0.99))
    y1, y2 = (int(h * 0.75), int(h * 0.35))
    if not up:
      y1, y2 = y2, y1
    self.adb('shell', 'input', 'swipe', x, str(y1), x, str(y2), '600')
    time.sleep(2)


def find_card(phone, card):
  """Scroll the open shop until the item's card shows (it may open
  scrolled anywhere): down first, then up."""
  for up in [True] * 4 + [False] * 8:
    image = phone.screen()
    if phone.find(image, card) and phone.find(image, 'header'):
      return True
    phone.swipe(image, up)
  return False


def buy(phone, item, count, limit, folder):
  gems, card, title, buttons, text = ITEMS[item]
  image = phone.screen()
  cart = phone.find(image, 'cart')
  if cart is None:
    log('cart button not found (a dialog open?), nothing bought')
    return 0
  phone.tap(cart)
  bought = 0
  if not find_card(phone, card):
    log(f'{text} card not found')
  while bought < count and spent(phone.name) + gems <= limit:
    image = phone.screen()
    if not phone.find(image, title):
      price = phone.find(image, card)
      if price is None or phone.find(image, 'header') is None:
        log(f'{text} card not found')
        break
      phone.tap(price)
      image = phone.screen()
      if not phone.find(image, title):
        log(f'{text} dialog did not open')
        break
    button = next((point for point in (phone.find(image, name)
                                       for name in buttons) if point),
                  None)
    if button is None:
      log(f'{text}: no active gem button (x2 at its 2 h cap?)')
      break
    phone.tap(button)
    if item == 'cash' and phone.find(phone.screen(), title):
      log('the dialog is still open (not enough gems?)')
      break
    bought += 1
    with open(GEMS_LOG, 'a', encoding='utf-8') as file:
      file.write(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S} '
                 f'{phone.name}: bought {text} for {gems} gems\n')
    log(f'bought {text} {bought}x, {phone.name} spent {spent(phone.name)}')
    bot_log(folder, f'Bought {text} for {gems} gems'
                    f' ({spent(phone.name)} of {limit} this event)')
    if spent(phone.name) + gems > limit:
      bot_log(folder, f'Limit reached: {spent(phone.name)} of {limit}'
                      ' gems spent this event', key=True)
  for _ in range(3):  # close the dialog (if left open) and the shop
    image = phone.screen()
    close = phone.find(image, 'close_x')
    if close is None:
      break
    phone.tap(close)
  return bought


def in_race_pause():
  """Tue 21:50 - Wed 07:35: the bots must stay off (race_schedule)."""
  now = datetime.datetime.now()
  minutes = now.hour * 60 + now.minute
  return ((now.weekday() == 1 and minutes >= 21 * 60 + 50)
          or (now.weekday() == 2 and minutes < 7 * 60 + 35))


def pids(pattern, cwd=None):
  out = subprocess.run(['pgrep', '-x', pattern], capture_output=True,
                       text=True, check=False).stdout.split()
  return [p for p in out if cwd is None or _cwd(p) == cwd]


def _cwd(pid):
  try:
    return os.readlink(f'/proc/{pid}/cwd')
  except OSError:  # another user's process
    return None


def main():
  name, item, count = sys.argv[1], sys.argv[2], int(sys.argv[3])
  serial, folder, watchdog, start = PHONES[name]
  if in_race_pause():
    log('race pause, nothing done')
    return
  limit = gem_limit(folder)
  if spent(name) + ITEMS[item][0] > limit:
    log(f'{name}: gem limit reached ({spent(name)} of {limit})')
    bot_log(folder, f'Limit reached, {item} not bought'
                    f' ({spent(name)} of {limit} this event)')
    return
  for pid in pids(watchdog):
    os.kill(int(pid), 15)
  for pid in pids('python3', folder):
    os.kill(int(pid), 15)
  time.sleep(4)
  try:
    bought = buy(Phone(name, serial), item, count, limit, folder)
  finally:
    # Through systemd (the race timers' units): a watchdog started from
    # this process tree could not open a Konsole (00:39, 02:38)
    subprocess.run(['systemctl', '--user', 'start',
                    f'race-{start[len("start-"):]}.service'], check=False,
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
  log(f'{name}: {bought}x {item}, gems spent {spent(name)} of {limit}')
  ensure_bot(name, folder)


def bot_running(folder):
  return any(_cwd(p) == folder for p in subprocess.run(
    ['pgrep', '-f', 'python3 -m auto_eatventure'], capture_output=True,
    text=True, check=False).stdout.split())


def ensure_bot(name, folder):
  """On 2026-11-14 00:39 the watchdog's Konsole did not start the Xiaomi
  bot: wait for the bot, then start a Konsole here, then a bot without
  a window (its logs are files anyway)."""
  launches = [
    'systemd-run --user --collect -p KillMode=process konsole -p'
    f' tabtitle="Auto EatVenture" -e {folder}/run-konsole.sh',
    f'cd {folder} && setsid ./start.sh >/dev/null 2>&1 </dev/null &',
  ]
  for wait_s, launch in zip((150, 60, 60), launches + [None]):
    for _ in range(wait_s // 10):
      if bot_running(folder):
        log(f'{name}: bot running')
        return
      time.sleep(10)
    if launch is None:
      break
    log(f'{name}: bot not running, launching: {launch[:40]}')
    subprocess.run(['bash', '-c', launch], check=False,
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
  log(f'{name}: BOT NOT RUNNING after the purchase')


if __name__ == '__main__':
  main()
