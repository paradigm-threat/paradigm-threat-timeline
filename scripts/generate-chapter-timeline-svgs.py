#!/usr/bin/env python3
"""Generate chapter-span and chapter-events SVGs for each chapter (01-15). Overview unchanged."""

import json
import sys
import os

# Chapter bounds: (x_start, x_end) on overview. Year span (yr_start, yr_end) for positioning.
# BCE as negative. yr_end None = use next chapter start.
# Optional subtitle per chapter (None = default "Timeline of events in this chapter")
CHAPTER_SUBTITLES = {
    "02.the-golden-age": "Order: Talbott documentary (youtu.be/oophJNlP-fk)",
}

# Full documentary sequence for chapter-events.svg (golden-age-event-dates.md).
# Even spacing on axis; only Cook-dated anchors shown (4077 crescent / nova; 3147 collapse).
def golden_age_documentary_events_with_positions():
    steps = [
        ("Timeless epoch (diffuse cloud)", "?"),
        ("Cloud dissipates", "?"),
        ("Crescent appears (Cook: Saturn nova)", "4077 BCE"),
        ("Earth rotates — first clock", "?"),
        ("Mars destabilizes", "?"),
        ("Mars oscillates", "?"),
        ("Mars drops below Venus", "?"),
        ("Lateral displacements", "?"),
        ("Band around Venus", "?"),
        ("Mars descents continue", "?"),
        ("Material reaches Earth", "?"),
        ("Recovery — Mars moves away", "?"),
        ("Saturn tumbles (Jupiter appears)", "?"),
        ("Venus displaced", "?"),
        ("Temporary Jupiter renewal", "?"),
        ("Final breakup", "3147 BCE"),
    ]
    n = len(steps)
    out = []
    for i, (title, yl) in enumerate(steps):
        t = i / (n - 1) if n > 1 else 0.5
        out.append(({"title": title, "year_label": yl}, t))
    return out
CHAPTERS = [
    ("01.before-creation", "Before Creation", (20, 100), (None, -4077)),  # pre-creation
    ("02.the-golden-age", "The Golden Age", (100, 230), (-4077, -3147)),
    ("03.the-dark-ages", "The Dark Ages", (230, 515), (-3147, -670)),
    ("04.the-blip", "The Blip", (515, 615), (-670, 1053)),
    ("05.ce-11th-common-era-begins", "11th Century", (615, 675), (1053, 1100)),
    ("06.ce-12th-birth-of-christianity", "12th Century", (675, 735), (1100, 1200)),
    ("07.ce-13th-the-russian-horde-tartarian-empire", "13th Century", (735, 795), (1200, 1300)),
    ("08.ce-14th-great-expansion-of-the-mongol-slav", "14th Century", (795, 855), (1300, 1400)),
    ("09.ce-15th-ottoman-conquest-of-europe", "15th Century", (855, 915), (1400, 1500)),
    ("10.ce-16th-reformation-and-inquisition", "16th Century", (915, 975), (1500, 1600)),
    ("11.ce-17th-romanovs-rise-to-power", "17th Century", (975, 1035), (1600, 1700)),
    ("12.ce-18th-mudflood-and-pugachev", "18th Century", (1035, 1095), (1700, 1800)),
    ("13.ce-19th-rise-of-communism", "19th Century", (1095, 1155), (1800, 1900)),
    ("14.ce-20th-the-1917-revolution", "20th Century", (1155, 1216), (1900, 2000)),
    ("15.ce-21st-the-final-struggle", "21st Century", (1216, 1277), (2000, 2030)),
]

# Overview bands: (x1, x2, label, fill, stroke, text_fill)
BANDS = [
    (20, 100, "Before Creation", "#e8e6e0", "#999", "#333"),
    (100, 230, "Golden Age", "#ddd", "#888", "#222"),
    (230, 515, "Dark Ages (3147-670 BCE)", "#ccc", "#777", "#222"),
    (515, 615, "Blip", "#bbb", "#666", "#111"),
    (615, 675, "11th", "#e8e6e0", "#999", "#333"),
    (675, 735, "12th", "#ddd", "#888", "#222"),
    (735, 795, "13th", "#ccc", "#777", "#222"),
    (795, 855, "14th", "#bbb", "#666", "#111"),
    (855, 915, "15th", "#e8e6e0", "#999", "#333"),
    (915, 975, "16th", "#ddd", "#888", "#222"),
    (975, 1035, "17th", "#ccc", "#777", "#222"),
    (1035, 1095, "18th", "#bbb", "#666", "#111"),
    (1095, 1155, "19th", "#e8e6e0", "#999", "#333"),
    (1155, 1216, "20th", "#ddd", "#888", "#222"),
    (1216, 1277, "21st", "#ccc", "#777", "#222"),
]


def has_positionable_date(dates):
    """True if dates has at least one usable start/end/value for timeline positioning."""
    if not dates:
        return False
    d = dates[0]
    return (
        d.get("start") is not None
        or d.get("end") is not None
        or d.get("value") is not None
    )


def flatten_dated_events(entry, out=None):
    """Collect only entries with explicit dates (events/spans), not undated articles."""
    out = out or []
    dates = entry.get("dates") or []
    if entry.get("title") and has_positionable_date(dates):
        out.append({
            "title": entry["title"],
            "dates": dates,
        })
    for c in entry.get("children", []):
        flatten_dated_events(c, out)
    return out


def year_from_dates(dates):
    """Get (year, calendar) for positioning; prefer start, else end, else value."""
    if not dates:
        return None, None
    d = dates[0]
    cal = d.get("calendar")
    if d.get("start") is not None:
        return d["start"], cal
    if d.get("end") is not None:
        return d["end"], cal
    return d.get("value"), cal


def format_year(yr, calendar=None):
    if yr is None:
        return ""
    if calendar is None:
        calendar = "CE" if (isinstance(yr, (int, float)) and yr >= 0) else "BCE"
    return f"{abs(int(yr))} {calendar}"


def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def write_chapter_span_svg(chapter_id, title, x1, x2, media_dir):
    path = os.path.join(media_dir, chapter_id, "chapter-span.svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    bands_svg = []
    for bx1, bx2, label, fill, stroke, text_fill in BANDS:
        is_highlight = (bx1, bx2) == (x1, x2)
        if is_highlight:
            fill = "#b8c8dc"
            text_fill = "#111"
            opacity = "1"
        else:
            opacity = "0.45"
        rect_w = bx2 - bx1
        cx = bx1 + rect_w / 2
        bands_svg.append(f'  <rect x="{bx1}" y="66" width="{rect_w}" height="20" fill="{fill}" stroke="{stroke}" stroke-width="0.5" opacity="{opacity}"/>')
        bands_svg.append(f'  <text x="{cx}" y="80" text-anchor="middle" font-size="9px" fill="{text_fill}" opacity="{opacity}">{escape(label)}</text>')

    svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1357 138" width="1357" height="138">
  <rect width="1357" height="138" fill="#f5f4f0"/>
  <line x1="100" y1="100" x2="1225" y2="100" stroke="#333" stroke-width="2"/>
{chr(10).join(bands_svg)}
  <line x1="100" y1="96" x2="100" y2="104" stroke="#333" stroke-width="1"/>
  <text x="100" y="118" text-anchor="middle" font-size="10px" fill="#222">4077 BCE</text>
  <line x1="515" y1="96" x2="515" y2="104" stroke="#333" stroke-width="1"/>
  <text x="515" y="118" text-anchor="middle" font-size="9px" fill="#444">670 BCE</text>
  <line x1="615" y1="96" x2="615" y2="104" stroke="#999" stroke-width="1"/>
  <text x="615" y="118" text-anchor="middle" font-size="9px" fill="#555">1053 CE</text>
  <line x1="1225" y1="96" x2="1225" y2="104" stroke="#333" stroke-width="1"/>
  <text x="1225" y="118" text-anchor="middle" font-size="10px" fill="#222">today</text>
  <text x="688" y="24" text-anchor="middle" font-size="16px" font-weight="bold" fill="#111">{escape(title)} — Span</text>
  <text x="688" y="38" text-anchor="middle" font-size="10px" fill="#444">This chapter covers the highlighted period</text>
</svg>'''
    with open(path, "w") as f:
        f.write(svg)
    print(f"Wrote {path}")


# Threshold: events within this fraction of axis length are "flush" with start/end
FLUSH_THRESHOLD = 0.035
# Min x-distance between event ticks (px)
MIN_TICK_SPACING = 28
# Vertical spacing (px) for event labels
TICK_LEN = 24
LABEL_ROW_GAP = 18
AXIS_LABEL_OFFSET = 28
# Single row above/below axis - strict up/down alternation
LABEL_OFFSET_ABOVE = 24   # px from tick end
LABEL_OFFSET_BELOW = 24


def write_chapter_events_svg(chapter_id, title, events_with_pos, yr_start, yr_end, media_dir, subtitle=None):
    path = os.path.join(media_dir, chapter_id, "chapter-events.svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    x_min, x_max = 100, 1200
    axis_y = 140
    width = x_max - x_min

    # Check if first/last events are flush with axis ends (to suppress duplicate axis labels)
    first_t = min((0.5 if t is None else t for _, t in events_with_pos), default=0.5)
    last_t = max((0.5 if t is None else t for _, t in events_with_pos), default=0.5)
    show_left_axis_label = first_t > FLUSH_THRESHOLD
    show_right_axis_label = last_t < (1 - FLUSH_THRESHOLD)

    # Axis labels
    if yr_start is not None and yr_end is not None:
        left_label = format_year(yr_start, "BCE" if yr_start < 0 else "CE")
        right_label = format_year(yr_end, "BCE" if yr_end < 0 else "CE")
    else:
        left_label = "start"
        right_label = "end"

    n = len(events_with_pos)
    if n == 0:
        events_svg = []
    else:
        # Snap flush events to axis ends to avoid redundant ticks
        snapped = []
        for ev, t in events_with_pos:
            tt = 0.5 if t is None else t
            if tt <= FLUSH_THRESHOLD:
                tt = 0.0
            elif tt >= 1 - FLUSH_THRESHOLD:
                tt = 1.0
            snapped.append((ev, tt))

        # Compute x positions; group events within 8px as same tick
        xs = []
        for ev, t in snapped:
            x = x_min + t * width
            xs.append((ev, t, x))
        xs.sort(key=lambda r: r[2])

        # Build groups: events at same x (within 8px) share one tick
        groups = []
        for ev, t, x in xs:
            if groups and abs(x - groups[-1][0]) < 8:
                groups[-1][1].append((ev, t))
            else:
                groups.append((x, [(ev, t)]))

        # Space groups apart if too close
        out = []
        for i, (x, evs) in enumerate(groups):
            if i > 0 and x - out[-1][0] < MIN_TICK_SPACING:
                x = out[-1][0] + MIN_TICK_SPACING
                x = min(x, x_max)
            out.append((x, evs))

        # Strict alternate up/down: event 0 below, 1 above, 2 below, 3 above, ...
        placements = [(x, evs, (i % 2) == 0) for i, (x, evs) in enumerate(out)]  # below=True for even

        events_svg = []
        y_vals = [24, 42, axis_y - 4, axis_y, axis_y + 4]
        for x, evs, below in placements:
            if below:
                tick_y2 = axis_y + TICK_LEN
                base_y = axis_y + TICK_LEN + LABEL_OFFSET_BELOW
                dy = 1
            else:
                tick_y2 = axis_y - TICK_LEN
                base_y = axis_y - TICK_LEN - LABEL_OFFSET_ABOVE
                dy = -1

            events_svg.append(f'  <line x1="{x}" y1="{axis_y}" x2="{x}" y2="{tick_y2}" stroke="#999" stroke-width="1"/>')
            y_vals.extend([tick_y2])

            ev_list = [e for e, _ in evs]
            yr_labels = {ev.get("year_label") for ev in ev_list if ev.get("year_label")}
            yr_label = list(yr_labels)[0] if len(yr_labels) == 1 else (ev_list[0].get("year_label") or "")
            at_start = x - x_min < 25
            at_end = x_max - x < 25
            show_yr = yr_label and not (at_start and show_left_axis_label) and not (at_end and show_right_axis_label)

            row = 0
            if show_yr:
                y_vals.append(base_y + row * dy * LABEL_ROW_GAP)
                events_svg.append(f'  <text x="{x}" y="{base_y + row * dy * LABEL_ROW_GAP}" text-anchor="middle" font-size="11px" fill="#222">{escape(yr_label)}</text>')
                row += 1
            for ev in ev_list:
                yv = base_y + row * dy * LABEL_ROW_GAP
                y_vals.append(yv)
                label = (ev["title"][:46] + "...") if len(ev["title"]) > 46 else ev["title"]
                events_svg.append(f'  <text x="{x}" y="{yv}" text-anchor="middle" font-size="10px" fill="#444">{escape(label)}</text>')
                row += 1

    # Axis ticks and labels (conditional)
    axis_lines = [
        f'  <line x1="{x_min}" y1="{axis_y-4}" x2="{x_min}" y2="{axis_y+4}" stroke="#333" stroke-width="1"/>',
        f'  <line x1="{x_max}" y1="{axis_y-4}" x2="{x_max}" y2="{axis_y+4}" stroke="#333" stroke-width="1"/>',
    ]
    if show_left_axis_label:
        axis_lines.append(f'  <text x="{x_min}" y="{axis_y+AXIS_LABEL_OFFSET}" text-anchor="middle" font-size="10px" fill="#444">{left_label}</text>')
    if show_right_axis_label:
        axis_lines.append(f'  <text x="{x_max}" y="{axis_y+AXIS_LABEL_OFFSET}" text-anchor="middle" font-size="10px" fill="#444">{right_label}</text>')

    # Crop height to content bounds
    if n:
        y_vals.extend([axis_y + AXIS_LABEL_OFFSET])
        svg_height = int(max(y_vals)) + 14
    else:
        svg_height = 100
    svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1357 {svg_height}" width="1357" height="{svg_height}">
  <rect width="1357" height="{svg_height}" fill="#f5f4f0"/>
  <line x1="{x_min}" y1="{axis_y}" x2="{x_max}" y2="{axis_y}" stroke="#333" stroke-width="2"/>
{chr(10).join(axis_lines)}
{chr(10).join(events_svg)}
  <text x="650" y="24" text-anchor="middle" font-size="16px" font-weight="bold" fill="#111">{escape(title)} — Events</text>
  <text x="650" y="42" text-anchor="middle" font-size="10px" fill="#444">{escape(subtitle) if subtitle else "Timeline of events in this chapter"}</text>
</svg>'''
    with open(path, "w") as f:
        f.write(svg)
    print(f"Wrote {path}")


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_dir = os.path.join(base, "media")
    scripts = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, scripts)
    from build_events_from_content import build_events_data

    data, errors = build_events_data()
    if errors or not data:
        raise SystemExit("build_events_data failed:\n  - " + "\n  - ".join(errors or ["unknown"]))

    chapter_by_id = {c[0]: c for c in CHAPTERS}

    for entry in data.get("entries", []):
        md = entry.get("md_path", "")
        if not md.startswith("content/"):
            continue
        parts = md.split("/")
        if len(parts) < 2:
            continue
        chapter_id = parts[1]
        if chapter_id not in chapter_by_id:
            continue

        _, title, (x1, x2), (yr_start, yr_end) = chapter_by_id[chapter_id]
        if chapter_id == "02.the-golden-age":
            events_with_pos = golden_age_documentary_events_with_positions()
            write_chapter_span_svg(chapter_id, title, x1, x2, media_dir)
            write_chapter_events_svg(
                chapter_id,
                title,
                events_with_pos,
                yr_start,
                yr_end,
                media_dir,
                subtitle=CHAPTER_SUBTITLES.get(chapter_id),
            )
            continue

        items = flatten_dated_events(entry)

        # Position events: by year if available, else evenly
        events_with_pos = []
        for ev in items:
            yr, cal = year_from_dates(ev.get("dates"))
            if yr_start is not None and yr_end is not None and yr is not None:
                try:
                    yr_f = float(yr)
                    span = yr_end - yr_start
                    if span > 0:
                        t = (yr_f - yr_start) / span
                        t = max(0, min(1, t))
                    else:
                        t = 0.5
                except (TypeError, ValueError):
                    t = 0.5
            else:
                t = None
            d0 = (ev.get("dates") or [{}])[0] if ev.get("dates") else {}
            if d0.get("display_year") == "?" or (d0.get("note") and "?" in str(d0.get("note", ""))):
                ev["year_label"] = "?"
            else:
                ev["year_label"] = format_year(yr, cal) if yr is not None else ""
            events_with_pos.append((ev, t))

        # If no explicit positions, distribute evenly
        has_pos = any(p[1] is not None for p in events_with_pos)
        if not has_pos and events_with_pos:
            for i, (ev, _) in enumerate(events_with_pos):
                n = len(events_with_pos)
                t = i / (n - 1) if n > 1 else 0.5
                events_with_pos[i] = (ev, t)

        # Sort by position for consistent ordering
        def key(ev_t):
            ev, t = ev_t
            if t is not None:
                return (0, t)
            return (1, 0)
        events_with_pos.sort(key=key)

        # Spread overlapping events: when multiple share same t, offset slightly
        from collections import defaultdict
        pos_groups = defaultdict(list)
        for i, (ev, t) in enumerate(events_with_pos):
            tt = 0.5 if t is None else t
            pos_groups[round(tt, 2)].append((i, ev, t))
        for _, group in pos_groups.items():
            if len(group) > 1:
                n = len(group)
                for j, (idx, ev, t) in enumerate(group):
                    tt = 0.5 if t is None else t
                    offset = (j - (n - 1) / 2) * 0.04
                    new_t = max(0.02, min(0.98, tt + offset))
                    events_with_pos[idx] = (ev, new_t)
        events_with_pos.sort(key=key)

        write_chapter_span_svg(chapter_id, title, x1, x2, media_dir)
        write_chapter_events_svg(chapter_id, title, events_with_pos, yr_start, yr_end, media_dir,
                                 subtitle=CHAPTER_SUBTITLES.get(chapter_id))


if __name__ == "__main__":
    main()
