#!/usr/bin/env python3
"""
Post-processing script for OrcaSlicer.
1. Moves ; MINX / MINY / MAXX / MAXY lines to right after HEADER_BLOCK_END
   so Creality prtouch can find them.
2. Moves M140 (bed temp) to before M191 (chamber wait) so bed starts
   heating in parallel with chamber.
3. Removes the second T[n] command that Orca inserts before ;filament start gcode
"""
import sys, re
path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()
# ── 1. Move MINX/MINY/MAXX/MAXY after HEADER_BLOCK_END ──────────────────────
tags = {}
tag_indices = []
pat = re.compile(r"^;\s*(MINX|MINY|MAXX|MAXY)\s*=\s*(.+)$")
for i, line in enumerate(lines):
    m = pat.match(line.strip())
    if m:
        tags[m.group(1)] = m.group(2).strip()
        tag_indices.append(i)
if len(tags) == 4:
    for i in sorted(tag_indices, reverse=True):
        del lines[i]
    insert_lines = [f"; {k} = {tags[k]}\n" for k in ("MINX", "MINY", "MAXX", "MAXY")]
    inserted = False
    for i, line in enumerate(lines):
        if "; HEADER_BLOCK_END" in line:
            for j, il in enumerate(insert_lines):
                lines.insert(i + 1 + j, il)
            inserted = True
            break
    if not inserted:
        for j, il in enumerate(insert_lines):
            lines.insert(1 + j, il)
# ── 2. Move M140 before M191 ─────────────────────────────────────────────────
m191_pat = re.compile(r"^\s*M191\b")
m140_pat = re.compile(r"^\s*M140\b")
m191_idx = None
for i, line in enumerate(lines):
    if m191_pat.match(line):
        m191_idx = i
        break
if m191_idx is not None:
    m140_idx = None
    for i in range(m191_idx + 1, len(lines)):
        if m140_pat.match(lines[i]):
            m140_idx = i
            break
    if m140_idx is not None:
        m140_line = lines[m140_idx]
        lines.insert(m191_idx, m140_line)
# ── 3. Remove second T[n] before ;filament start gcode ───────────────────────
t_pat = re.compile(r"^\s*T\d+\s*$")
filament_start_pat = re.compile(r"^;filament start gcode")
first_t_seen = False
for i, line in enumerate(lines):
    if t_pat.match(line):
        if not first_t_seen:
            first_t_seen = True
        else:
            # Check if this T[n] is followed by ;filament start gcode
            # (possibly with blank/comment lines in between)
            for j in range(i + 1, min(i + 5, len(lines))):
                if filament_start_pat.match(lines[j]):
                    lines[i] = ""
                    break
with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)