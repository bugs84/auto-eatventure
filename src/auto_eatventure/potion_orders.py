"""potion_orders.txt: the Potion Shop bottles still wanted after the
event's rewards ("potion: count" lines, see potion_orders-sample.txt).
Read before each order (edits apply without a restart); the bot lowers
a count after each bottle."""

import logging
import os
import re

from auto_eatventure.actions import potion_shop_cauldron

log = logging.getLogger(__name__)

ORDERS_FILE = 'potion_orders.txt'
ORDER_LINE = re.compile(r'^(\s*([A-Za-z]+)\s*:\s*)([^\s#]*)(.*)$')


def parse_orders(text):
  """{potion: count} of the "potion: count" lines (file order; a "#"
  comment may follow). Lines starting with "#" and empty lines are
  skipped; unknown potions, bad counts and repeated potions with a
  warning."""
  orders = {}
  for line in text.splitlines():
    if not line.strip() or line.lstrip().startswith('#'):
      continue
    match = ORDER_LINE.match(line)
    name = match.group(2).lower() if match else ''
    count = match.group(3) if match else ''
    if (name not in potion_shop_cauldron.POTIONS or name in orders
        or not count.isdigit()
        or match.group(4).strip()[:1] not in ('', '#')):
      log.warning('%s: %r ignored', ORDERS_FILE, line.strip())
      continue
    orders[name] = int(count)
  return orders


def read_text():
  """The text of ORDERS_FILE; '' when it is missing."""
  try:
    with open(ORDERS_FILE, encoding='utf-8') as file:
      return file.read()
  except OSError:
    return ''


def read_orders():
  """{potion: count > 0} of ORDERS_FILE."""
  return {name: count for name, count in parse_orders(read_text()).items()
          if count > 0}


def lower_order(name):
  """Lower the count of the potion in ORDERS_FILE by 1 (only the
  number of its line changes). Returns the new count, None when the
  potion has no count above 0 there."""
  try:
    with open(ORDERS_FILE, encoding='utf-8') as file:
      lines = file.read().splitlines(keepends=True)
  except OSError:
    return None
  for index, line in enumerate(lines):
    match = ORDER_LINE.match(line.rstrip('\r\n'))
    if (line.lstrip().startswith('#') or not match
        or match.group(2).lower() != name or not match.group(3).isdigit()):
      continue
    count = int(match.group(3))
    if count < 1:
      return None
    ending = line[len(line.rstrip('\r\n')):]
    lines[index] = (f'{match.group(1)}{count - 1}{match.group(4)}'
                    f'{ending}')
    # Written aside and moved over: a crash never leaves half a file
    with open(f'{ORDERS_FILE}.tmp', 'w', encoding='utf-8',
              newline='') as file:
      file.writelines(lines)
    os.replace(f'{ORDERS_FILE}.tmp', ORDERS_FILE)
    return count - 1
  return None
