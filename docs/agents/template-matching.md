# Template Matching

> <- Back to [AGENTS.md](../../AGENTS.md)

## Overview

The project uses **OpenCV template matching** (`cv2.matchTemplate` with `TM_CCOEFF_NORMED`) to detect game UI elements in screenshots. No OCR is used.

## Matching Strategies

### 1. HSV Matching (Default)

Used by `is_image_template_matching()` at `adb_autoplay.py:222`.

```python
hsv_sc = self.current_cv2_sc_bgr2hsv
hsv_template = template_cv_imgs['bgr2hsv']
matched_coordinates = self.find_template(hsv_sc, hsv_template, threshold=threshold)
```

- Converts both screenshot and template to HSV color space
- More robust to lighting variations in the game

### 2. Grayscale Matching

Used by `is_bnw_image_template_matching()` at `adb_autoplay.py:231`.

- Used for small investor icon detection
- Less affected by color shifts

### 3. Color-Masked Matching

Used for investor and box detection:

- `apply_investor_mask()` at `adb_autoplay.py:249` -- isolates specific HSV colors (#696548, #776F4B, etc.)
- `apply_box_mask()` at `adb_autoplay.py:267` -- isolates box-specific gold/brown colors

### 4. Raw BGR Matching

Used by `get_all_boxes_locations()` at `adb_autoplay.py:398`.

- Direct matching without color space conversion
- Fallback when masked matching fails on different devices

## Multi-Match Detection with DBSCAN

`find_all_templates()` at `adb_autoplay.py:181` finds **all** locations where a template matches above threshold, then uses **DBSCAN clustering** to deduplicate:

```python
dbscan = DBSCAN(eps=self.sc.dbscan_eps, min_samples=5)
dbscan.fit(coord_array)
```

- `eps` = 10 pixels (from `coords.py:150`) -- max distance between points in same cluster
- `min_samples` = 5 -- minimum points to form a cluster
- Returns cluster centroids as final match positions

## Template Images

All templates are in `matching_screenshots/`:

| Template | Purpose | Matching Strategy |
|----------|---------|-------------------|
| `notification.png` | Notification dialog | HSV |
| `settings.png` | Settings icon (game loaded check) | HSV |
| `offline_earnings.png` | Offline earnings popup | HSV |
| `upgrade_button.png` | Upgrade button (threshold 0.97) | HSV |
| `buy_better_food_icon.png` | Food upgrade icon (multi-match) | Grayscale |
| `buy_better_food_button.png` | Buy button in upgrade menu | HSV |
| `box.png`, `box2.png` | Collectible boxes (multi-match) | Raw BGR |
| `go_next_level_icon.png` | Next level indicator (threshold 0.95) | HSV |
| `fly_next_city_icon.png` | Fly to next city (threshold 0.95) | HSV |
| `small_investor_icon.png` | Small investor icon | Grayscale |
| `investor.png` | Large investor (threshold 0.65) | Color-masked |
| `chest_icon.png` | Chest icon | HSV |
| `no_boost_indicator_2x.png` | No-boost check | HSV |
| `ads_crosses/cross1.png` | Ad close button | Grayscale |

## Template Scaling

Templates are resized at load time to match the actual device resolution:

```python
def _resize_template(self, template):
    target_w = max(1, round(w * self.template_x_scale))
    target_h = max(1, round(h * self.template_y_scale))
    interpolation = cv2.INTER_AREA if shrinking else cv2.INTER_LINEAR
    return cv2.resize(template, (target_w, target_h), interpolation=interpolation)
```

Scale factors are computed from `actual_resolution / reference_resolution` (1220x2712).

Can be overridden with `TEMPLATE_SCALE_OVERRIDE` env var.

## Thresholds

Default threshold is `0.8`. Custom thresholds per element:

- `upgrade_button`: 0.97 (very strict -- avoid false positives)
- `go_next_level`: 0.95
- `fly_next_city`: 0.95
- `no_boost_indicator_2x`: 0.92
- `investor` (color-masked): 0.65 (lenient due to mask reducing information)
- `box` / `box2` (multi-match): 0.7

## Debug Mode

Set `DEBUG_TEMPLATE_MATCHING="1"` in `.env` to print raw `cv2.minMaxLoc` values for every template check. Very noisy -- only use when tuning thresholds.
