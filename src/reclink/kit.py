"""Publish the parts of the design kit (tasteskill) that the two redesigned pages use.

The kit lives in the skill folder (KIT_SRC, override with the TASTE_KIT env var). Only the files listed here
are copied into RecLink/assets/kit/, so the site ships nothing it does not load. The copy is committed;
when the skill folder is not on the machine the build keeps the committed copy.
"""
import os
import shutil

KIT_SRC = os.environ.get("TASTE_KIT") or os.path.expanduser("~/.claude/skills/design-taste-frontend/assets")

# files and folders (relative to the kit root) that the pages load
KIT_FILES = [
    "system.css", "system.js",
    "ui/ui.js", "ui/base.css", "ui/cards.css",
    "motion/motion.css", "motion/motion.js",
    "backgrounds/backgrounds.css", "backgrounds/backgrounds.js",
    "layout/layout.css", "layout/layout.js",
    "icons/icon.css",
    "diagrams/diagram.css", "diagrams/diagram.js", "diagrams/mount.js", "diagrams/presets.json",
    "moments/moments.js", "moments/lib.js",
    "moments/liquid-type/moment.js", "moments/liquid-type/moment.css",
    "moments/line-carries-colour/moment.js", "moments/line-carries-colour/moment.css",
    "moments/counter-rolls/moment.js", "moments/counter-rolls/moment.css",
    "effects/fx.js", "effects/grain-gradient/effect.js",
]


def publish(dest):
    if not os.path.isdir(KIT_SRC):
        print("kit: skill folder not found, keeping the committed copy in", dest)
        return
    for rel in KIT_FILES:
        src = os.path.join(KIT_SRC, rel)
        if not os.path.exists(src):
            print("kit: missing", rel)
            continue
        out = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(src, out)
