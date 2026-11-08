"""Write the image-generation job files from docs/CHARACTER.md.

The character sentences, the style block, the background block and the palette words
are read from docs/CHARACTER.md and pasted verbatim, so every batch uses the same text.
Run from the project root:  python assets/make_jobs.py
Then:  python tools/imagegen.py assets/<dir>/<jobs>.jsonl --out-dir assets/<dir>
"""
import json
import re
from pathlib import Path

DOC = Path("docs/CHARACTER.md").read_text(encoding="utf-8")
BLOCKS = re.findall(r"```text\r?\n(.*?)\r?\n```", DOC, re.S)
SAYO, CHIZ, STYLE, BG_STYLE = BLOCKS
assert SAYO.startswith("The same original character") and "Sayo" in SAYO
assert "Chizuru" in CHIZ and STYLE.startswith("Delicate") and "{palette}" in BG_STYLE
PAL = dict(re.findall(r"^\| (\S+) \| ([a-z][^|]+?) \|\s*$", DOC, re.M))
assert set(PAL) == {"現在段", "回憶段", "時雨", "雲開", "紅楓", "風花"}, PAL

GREEN, MAGENTA = "#00FF00", "#FF00FF"
REF_S, REF_C = "assets/char/REF_sayo.png", "assets/char/REF_chizuru.png"
FULL_BLEED = "Full-bleed close-up filling the entire frame edge to edge, 16:9 landscape: "


def char(jid, pose, who, opaque=False):
    sent, ref, key = (SAYO, REF_S, GREEN) if who == "S" else (CHIZ, REF_C, MAGENTA)
    job = {"id": jid, "out": f"{jid}.png", "images": [ref], "prompt": f"{pose} {sent} {STYLE}"}
    job.update({"transparent": False} if opaque else {"transparent": True, "key": key})
    return job


def bg(jid, place, pal, ref=None):
    job = {"id": jid, "out": f"{jid}.png", "transparent": False,
           "prompt": f"{place} {BG_STYLE.replace('{palette}', PAL[pal])}"}
    if ref:
        job["images"] = [ref]
    return job


def prop(jid, what, key=None):
    job = {"id": jid, "out": f"{jid}.png", "prompt": f"{what} {STYLE}"}
    job.update({"transparent": True, "key": key} if key else {"transparent": False})
    return job


SAYO_POSES = [
    ("sayo_walk_back", "Full body seen from behind, walking away along a path with small steps, head slightly bowed, the large crimson ribbon bow at the back of her head clearly visible, its two long tails and her long hair drifting to the left in a gentle breeze, lonely mood."),
    ("sayo_hum", "Bust shot (chest up), front three-quarter view, eyes gently closed, lips slightly parted, softly humming a song, holding the faded temari against her chest with both hands, a few strands of hair moving in the breeze, calm and sad."),
    ("sayo_side_leaf", "Upper body in side profile facing left, head bowed, looking down at a single red maple leaf resting in her open right palm, melancholic, hair falling forward over her shoulder."),
    ("sayo_hand_chest", "Bust shot (chest up), facing the viewer, eyes closed, her right hand pressed flat over her heart, serene and aching expression, hair and ribbon tails moving softly."),
    ("sayo_back_lookup", "Full body seen from behind, standing still on a path, head tilted far back looking up at the sky, arms hanging at her sides with the faded temari in her right hand, the crimson bow, its long tails and her hair drifting in the wind."),
    ("sayo_lookup", "Upper body from a slightly low angle, three-quarter view, looking up at falling leaves above her with lips slightly parted, wonder and longing, one hand lifted a little as if to catch a leaf, hair and ribbon tails lifting in the breeze."),
    ("sayo_wind", "Full body, standing against a strong gust of wind blowing from the right, holding her hair back with her left hand, the faded temari pressed to her chest with the right, eyes narrowed, hakama, sleeves, long hair and the two crimson ribbon tails all whipping violently to the left."),
    ("sayo_smile", "Bust shot (chest up), three-quarter view, a warm gentle open smile, looking to her left at someone beside her with affection, soft summer light, hair moving softly."),
    ("sayo_sit", "Full body, sitting on a low stone step, front three-quarter view with her body turned slightly to her left, knees together, hands folded in her lap, looking down quietly, the hakama spread over the step."),
    ("sayo_sing_rain", "Bust shot (chest up), facing the viewer, singing softly with her mouth slightly open, eyes half closed, standing in the rain: hair and kimono damp, wet strands stuck to her cheeks, raindrops on her shoulders, sorrowful."),
    ("sayo_sleeve", "Upper body, three-quarter view, raising her right kimono sleeve to hide her eyes as she cries, shoulders hunched, rain-wet hair, the purple-and-cream yagasuri sleeve large in the frame with raindrops on it."),
    ("sayo_crouch", "Full body, front three-quarter view, crouching on the ground and hugging her knees, face buried in her arms, the faded temari held against her knees, long rain-wet hair spilling down her back to the ground, the crimson bow drooping, utterly still and lonely."),
    ("sayo_lookup_tears", "Bust shot (chest up) from a slightly low angle, lifting her face toward the sky, tears running down both cheeks, eyes wide open and shining, lips parted in surprise as if hearing a beloved voice, rain-wet hair."),
    ("sayo_reach_up", "Full body seen from a low three-quarter angle, standing and stretching her right arm straight up toward the sky with fingers open, face tilted up, the faded temari clutched to her chest with her left hand, hair and the long crimson ribbon tails streaming upward in a rising wind."),
    ("sayo_sing_power", "Upper body from a slightly low angle, singing with all her heart, mouth open on a long high note, eyes squeezed half shut with emotion, right hand clenched at her chest, left arm flung out to the side, hair and crimson ribbon tails flaring in a strong wind."),
    ("sayo_smile_snow", "Bust shot (chest up), three-quarter view, looking up at gently falling snowflakes with a soft, tearful but peaceful smile, a snowflake on her bangs, quiet cold air."),
]
SAYO_OPAQUE = [
    ("hands_temari_faded", FULL_BLEED + "her two hands gently cupping the small faded temari ball (dull red and cream threads, worn and colour-drained), seen from slightly above, the purple-and-cream yagasuri sleeves and maroon-brown hakama behind, one fallen red maple leaf resting on the hakama, soft overcast daylight."),
    ("sayo_listen", FULL_BLEED + "her face from the chin up in three-quarter view, eyes closed, listening to a distant song, long black bangs and strands of hair crossing the frame, a glimpse of the crimson ribbon, soft overcast daylight on her skin."),
    ("sayo_tear_smile", FULL_BLEED + "her face from the chin up, eyes half open, a single tear on her cheek and a tiny snowflake melting beside it, a small relieved smile, soft white winter light, strands of black hair crossing the frame."),
]
CHIZ_POSES = [
    ("chizuru_sing", "Upper body, three-quarter view, singing a children's song with a bright open mouth, eyes happily curved, bouncing the temari on her right palm, the braid swinging, warm golden summer light."),
    ("chizuru_walk_back", "Full body seen completely from behind (back view): we see her back, the leaf-green obi bow at the back of her waist and the back of her head, her face is NOT visible; she walks away from the viewer at a relaxed pace, the end of her braid showing over her left shoulder, the temari in her left hand at her side, summer light."),
    ("chizuru_bounce", "Full body, front three-quarter view, bouncing the temari off the ground with her right hand, the ball just below her palm, laughing joyfully, braid and sleeves swinging."),
    ("chizuru_sit", "Full body, sitting on a low stone step, front three-quarter view with her body turned slightly to her right, holding the temari in her lap with both hands, smiling and turning her head to her right toward someone beside her."),
    ("chizuru_float", "Full body, floating in the air high in the sky, seen slightly from below, looking downward with a serene loving smile, right hand reaching down with the palm open, the temari held against her hip with her left hand, sleeves, hem and braid drifting upward softly as if weightless, no ground."),
    ("chizuru_smile", "Close-up of her face and shoulders, looking slightly down at the viewer with a gentle, kind smile, eyes a little moist, warm light from behind her."),
    ("chizuru_reach_down", "Full body seen from below, floating in the sky, reaching her right hand straight down toward the viewer with fingers open, looking down with a tender smile, sleeves and braid hanging down toward the hand."),
    ("chizuru_wave", "Upper body, three-quarter view, waving goodbye with her right hand raised beside her face, a warm peaceful smile with closed eyes, the temari in her left hand, braid and sleeves moving softly in the wind."),
]
CHIZ_OPAQUE = [
    ("hands_temari_new", FULL_BLEED + "her two hands holding the bright new temari ball wound with red, green and white thread in a geometric pattern, offering it toward the viewer, the white summer kimono with pale-green maple leaves and the leaf-green obi behind, warm golden summer sunlight."),
]

LEAF = "A single Japanese maple (momiji) leaf with a short stem, flat, centred, generous margin, nothing touches the edges, "
PROPS = [
    prop("prop_leaf_red_a", LEAF + "crimson red with slightly darker veins, seen from directly above.", GREEN),
    prop("prop_leaf_red_b", LEAF + "vermilion red fading to orange at the tips, slightly curled, tilted.", GREEN),
    prop("prop_leaf_red_c", LEAF + "deep crimson, seen at an angle, one lobe gently curled up.", GREEN),
    prop("prop_leaf_green_a", LEAF + "fresh spring-green with lighter veins, seen from directly above. ENTIRELY fresh summer green from tip to stem: no red, orange, yellow, brown or purple anywhere on the leaf.", MAGENTA),
    prop("prop_leaf_green_b", LEAF + "bright leaf-green, slightly curled, tilted. ENTIRELY fresh summer green from tip to stem: no red, orange, yellow, brown or purple anywhere on the leaf.", MAGENTA),
    prop("prop_leaf_green_c", LEAF + "soft leaf-green, seen at an angle, one lobe gently curled up. ENTIRELY fresh summer green from tip to stem: no red, orange, yellow, brown or purple anywhere on the leaf.", MAGENTA),
    prop("prop_temari_faded", "A single small faded temari ball lying on its own, its dull red and cream threads worn and colour-drained, a few loose threads, generous margin, nothing touches the edges.", GREEN),
    prop("prop_temari_new", "A single bright new temari ball wound with red, green and white thread in a crisp geometric star pattern, generous margin, nothing touches the edges.", MAGENTA),
    prop("prop_oshiba", "Full-bleed, filling the entire frame edge to edge, 16:9 landscape: two pressed maple leaves, one crimson and one fresh green, laid side by side and slightly overlapping on a sheet of handmade white washi paper, flattened and slightly translucent like pressed flowers, seen from directly above, placed a little left of centre with lots of empty paper around them; the red leaf is pure crimson, the green leaf pure fresh green; plain paper only, no flowers, no other decorations or objects."),
]

PATH = ("A narrow old stone-slab path (ishidatami) winding gently uphill into a quiet Japanese mountain maple grove in the Taisho era, "
        "low mossy stone walls on both sides, maple trees arching over the path, the path centred and leading to a soft vanishing point "
        "slightly above the centre, empty space in the middle ground for a small figure, light from the upper left.")
STEPS = ("A short flight of old low stone steps on a small village shrine path in the Taisho era, seen from a front three-quarter angle, "
         "the lowest broad step in the lower centre of the frame clear and empty as a place to sit, a small stone lantern on one side, maple trees above.")
BG = [
    bg("bg_washi", "A blank sheet of handmade Japanese washi paper filling the frame edge to edge, warm cream white with visible long kozo fibres and a few faint fibre flecks, very subtle uneven tone, completely empty, flat even lighting, seen straight on.", "現在段"),
    bg("bg_path_present", PATH + " A few fallen leaves scattered on the stones.", "現在段"),
    bg("bg_canopy", "Looking straight up from the ground into the canopy of Japanese maple trees, branches spreading from the edges toward a pale sky in the centre, leaves backlit, a few leaves falling.", "現在段"),
    bg("bg_sky_overcast", "Sky only: a wide soft overcast autumn sky with layered pale clouds, a faint brighter area at the upper left, a thin line of distant maple treetops along the very bottom edge, low horizon.", "現在段"),
    bg("bg_sky_rain", "Sky only: heavy grey rain clouds over a thin line of distant treetops along the bottom edge, curtains of fine rain, one small thin gap in the clouds at the upper right where pale light leaks through, low horizon.", "時雨"),
    bg("bg_sky_open", "Sky only: rain clouds parting widely in the centre, a large opening of soft luminous light, gentle light rays falling diagonally, cloud edges glowing, a thin line of maple treetops along the bottom edge, plenty of empty bright space in the upper centre.", "雲開"),
    bg("bg_steps_summer", STEPS + " Dappled sunlight on the stones.", "回憶段"),
    bg("bg_forest_red", "A Japanese maple grove at the peak of autumn colour with an old stone-slab path leading into it, every tree blazing crimson and vermilion, the air full of falling red leaves, a pale clear sky visible above the canopy in the upper part of the frame.", "紅楓"),
]
SAME = "The same place, path and composition as the reference image, "
BG_VARIANTS = [
    bg("bg_path_summer", SAME + "but in late summer: every maple leaf fresh green, warm golden sunlight from the upper left with dappled shadows on the stones, no fallen leaves.", "回憶段", "assets/bg/bg_path_present.png"),
    bg("bg_path_rain", SAME + "during a cold autumn shower: wet dark stones reflecting the grey sky, fine diagonal rain streaks, mist between the trees, fallen leaves stuck to the wet path.", "時雨", "assets/bg/bg_path_present.png"),
    bg("bg_path_snow", SAME + "in the first light snow: thin white snow on the stones, walls and branches, most leaves gone with only a few faded russet leaves left, soft falling snowflakes.", "風花", "assets/bg/bg_path_present.png"),
    bg("bg_steps_autumn", "The same place, steps and composition as the reference image, but in late autumn: faded russet maple leaves, fallen leaves on the steps, soft overcast daylight.", "現在段", "assets/bg/bg_steps_summer.png"),
]
BOTH = [{
    "id": "hands_two_leaves", "out": "hands_two_leaves.png", "transparent": False, "images": [REF_S, REF_C],
    "prompt": FULL_BLEED + "two girls' hands raised side by side against a bright summer sky; the left hand, in a white kimono sleeve with a pale-green maple pattern (Chizuru), holds a fresh green maple leaf; the right hand, in a purple-and-cream yagasuri sleeve (Sayo), holds a single early-red maple leaf; the two leaves touch at their tips, sunlight shining through them, the veins glowing. " + STYLE,
}]

CHAR = ([char(j, p, "S") for j, p in SAYO_POSES] + [char(j, p, "S", True) for j, p in SAYO_OPAQUE]
        + [char(j, p, "C") for j, p in CHIZ_POSES] + [char(j, p, "C", True) for j, p in CHIZ_OPAQUE] + BOTH)

FILES = {"assets/char/jobs_core.jsonl": CHAR, "assets/prop/jobs_prop.jsonl": PROPS,
         "assets/bg/jobs_bg.jsonl": BG, "assets/bg/jobs_bg_variants.jsonl": BG_VARIANTS}
for path, jobs in FILES.items():
    assert len({j["id"] for j in jobs}) == len(jobs), path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for j in jobs:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    print(f"{path}: {len(jobs)} jobs")
