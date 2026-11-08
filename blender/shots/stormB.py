r"""
stormB.py - 3D-B：紅楓漫天（s46，nb(207.82) -> B(92)，約 7.7 s，末副歌第一句）。

全彩紅楓第一次出現：鏡頭在密集落下的楓葉裡往前穿過紅楓林，每個小節頭加速一下；
「楓」(214.91 s) 那一拍颳起一陣風，葉子朝鏡頭撲來、鏡頭仰起看向樹冠。
字（キメ「楓」）由 engine 的 JIZURA 層打，3D 不放字。

Full 30 fps (fast camera):
  blender -b --factory-startup -P blender/shots/stormB.py -- --mode stills --frames 1,80,160,212,232 --res 50
  blender -b --factory-startup -P blender/shots/stormB.py -- --mode full --res 50
"""
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as sh
import ak_common as ak
bc, bpy = sh.bc, sh.bpy
from mathutils import Vector
import bmesh

A = bc.parse_args({"mode": "stills", "res": 50, "start": 1, "end": 0, "frames": "1,80,160,212,232",
                   "out": "blender/renders/stormB", "samples": 16, "save_blend": 0, "lines": 1, "skip": 0}, doc=__doc__)

AUD = sh.load_audio()
BAR = {b["index"]: b["start"] for b in AUD["bars"]}
T0 = min(AUD["beats"], key=lambda b: abs(b - 207.82))
T1 = BAR[92]
T_KAEDE = 214.91
NF = int(math.ceil((T1 - T0) * sh.FPS - 1e-6))
DOWN = sh.beats_in(T0 + 0.05, T1 - 0.05, "downbeats")

HAZE = "#F7E4CF"
LINE = "#5A2E2A"
bc.reset_scene()
bc.setup_render("EEVEE", res=(1920, 1080), percent=A["res"], fps=30, samples=A["samples"], view="Standard")
bc.world_sky(stops=((0.0, "#FBEBD8"), (0.45, "#F7DCC4"), (1.0, "#F2CDB4")), z_lo=-0.05, z_hi=0.7, sun_dir=None,
             ambient="#C9A898", ambient_strength=0.25, below="#F3D9C2")
SUN = (0.3, 0.75, 0.6)          # backlight from up ahead: lit rims toward the camera, shadows fall at us
bc.sun("Sun", direction=SUN, color="#ffffff", strength=math.pi)
bc.sun("Fill", direction=(-0.3, -0.8, 0.5), color="#ffffff", strength=math.pi * 0.13, shadow=False)


def toon(name, lit, shade, hz=(8.0, 55.0)):
    return bc.toon_material(name, lit=lit, shade=shade, haze=HAZE, haze_range=hz, haze_max=0.88)


M_BARK = toon("Bark", "#8E5F52", "#5E3A35")
M_EARTH = toon("Earth", "#C98E78", "#9C6556")
LEAF_MATS = [ak.leaf_material(f"Leaf_{k}", ak.leaf_png("red", k), tint="#FFFFFF", jitter=(0.85, 1.08), haze=HAZE,
                              haze_range=(8.0, 50.0), haze_max=0.75) for k in "abc"]
FALL_MATS = [ak.leaf_material(f"Fall_{k}", ak.leaf_png("red", k), tint="#FFFFFF", jitter=(0.9, 1.1), haze=HAZE,
                              haze_range=(7.0, 45.0), haze_max=0.7) for k in "abc"]
C_GEO = bc.collection("Geo")
C_LEAF = bc.collection("Leaves")
C_LEAF.lineart_usage = "EXCLUDE"
C_SRC = bc.collection("LeafSrc")
C_SRC.lineart_usage = "EXCLUDE"
CARDS = [ak.leaf_card(f"Card_{k}", m, C_SRC) for k, m in zip("abc", LEAF_MATS)]
FCARDS = [ak.leaf_card(f"FCard_{k}", m, C_SRC) for k, m in zip("abc", FALL_MATS)]
R = ak.rng(46)

# ---------------------------------------------------------------------------------------- camera line
# the camera flies along +Y, weaving through x = cam_x(y); trees keep clear of that line
Y0, Y_LEN = 0.0, 46.0


def cam_x(y):
    return 1.2 * math.sin(y / 9.0) + 0.5 * math.sin(y / 4.3 + 1.0)


# ---------------------------------------------------------------------------------------- forest
GROUND = bc.plane("Ground", size=(300, 300), loc=(0, 60, 0), coll=C_GEO, mat=M_EARTH)
bc.lineart_usage(GROUND, "OCCLUSION_ONLY")
LEAF_PTS = [[], [], []]


def cluster(c, rad, n, scale):
    for _ in range(n):
        while True:
            u, v, w = R.uniform(-1, 1), R.uniform(-1, 1), R.uniform(-1, 1)
            if u * u + v * v + w * w <= 1:
                break
        LEAF_PTS[R.randrange(3)].append(((c[0] + u * rad[0], c[1] + v * rad[1], c[2] + w * rad[2]),
                                         (R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)), R.uniform(*scale)))


bm = bmesh.new()
y = -6.0
while y < Y_LEN + 40:
    for lane in (-1, 1):
        for depth in range(3):
            if R.random() < 0.25:
                continue
            gap = 1.9 + depth * 3.2 + R.uniform(0, 2.0)
            x = cam_x(y) + lane * gap
            yy = y + R.uniform(-1.2, 1.2)
            h = R.uniform(5.5, 8.0)
            base = Vector((x, yy, -0.2))
            top = base + Vector((R.uniform(-0.8, 0.8), R.uniform(-0.8, 0.8), h))
            r0 = R.uniform(0.18, 0.32)
            trunk = ak.bezier(base, base.lerp(top, 0.5) + Vector((R.uniform(-0.4, 0.4), 0, 0)), top, n=8)
            ak.tube(bm, trunk, r0, r0 * 0.4, sides=8)
            for _ in range(R.choice((2, 3))):
                root = trunk[R.randrange(4, 7)]
                tip = root + Vector((R.uniform(-2.5, 2.5), R.uniform(-2.5, 2.5), R.uniform(0.8, 2.0)))
                ak.tube(bm, ak.bezier(root, root.lerp(tip, 0.5) + Vector((0, 0, 0.6)), tip, n=5), r0 * 0.4, 0.03, sides=6)
                cluster(tip, (2.2, 2.2, 1.1), 170, (0.2, 0.34))
            cluster(top + Vector((0, 0, 0.4)), (2.6, 2.6, 1.3), 230, (0.2, 0.34))
    y += R.uniform(3.0, 4.2)
TREES = ak.bm_object("Trees", bm, [M_BARK], C_GEO)
for k in range(3):
    p = LEAF_PTS[k]
    bc.instance_on_points(f"Canopy_{k}", CARDS[k], [q[0] for q in p], [q[1] for q in p], [q[2] for q in p], coll=C_LEAF)

# ground litter, dense
LIT = [[], [], []]
for _ in range(7000):
    yy = R.uniform(-4, Y_LEN + 30)
    xx = cam_x(yy) + R.uniform(-14, 14)
    LIT[R.randrange(3)].append(((xx, yy, 0.02), (R.uniform(-0.3, 0.3), R.uniform(-0.3, 0.3), R.uniform(0, 6.28)), R.uniform(0.13, 0.22)))
for k in range(3):
    p = LIT[k]
    bc.instance_on_points(f"Litter_{k}", CARDS[k], [q[0] for q in p], [q[1] for q in p], [q[2] for q in p], coll=C_LEAF)

# falling leaves: dense near the flight line, wrapping in z
Z_RANGE = (-0.3, 9.0)
FALL = [[], [], []]
for _ in range(9000):
    yy = R.uniform(-2, Y_LEN + 22)
    xx = cam_x(yy) + R.gauss(0, 3.2)
    FALL[R.randrange(3)].append({"co": (xx, yy, R.uniform(*Z_RANGE)), "fall": R.uniform(0.7, 1.4), "sway": R.uniform(0.15, 0.5),
                                 "phase": R.uniform(0, 6.28), "rot0": (R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
                                 "spin": (R.uniform(-2.5, 2.5), R.uniform(-2.5, 2.5), R.uniform(-1.5, 1.5)), "scale": R.uniform(0.13, 0.22)})
GUSTS = []
for k in range(3):
    ob, g = ak.falling_leaves(f"Fall_{k}", FCARDS[k], FALL[k], Z_RANGE, wind=(-0.35, -0.6, 0.0), coll=C_LEAF, gust_dir=(-0.35, -1.0, 0.45))
    GUSTS.append(g)

# gust on 楓: displacement (m) eases out after the hit
F_KAEDE = sh.frame_of(T_KAEDE, T0)
for g in GUSTS:
    keys = [(1, 0.0), (F_KAEDE - 2, 0.0)]
    for d in range(0, NF - F_KAEDE + 3, 2):
        keys.append((F_KAEDE + d, 7.0 * (1 - math.exp(-d / 7.0))))
    sh.key_socket(g, keys)
for ng in bpy.data.node_groups:
    sh.set_id_interp(ng)

# ---------------------------------------------------------------------------------------- camera
F_DOWN = [sh.frame_of(t, T0) for t in DOWN]


def speed(f):
    v = 4.6
    for h in F_DOWN:
        if f >= h:
            v += 2.4 * math.exp(-(f - h) / 9.0)
        v -= 0.9 * math.exp(-((f - (h - 5)) / 3.0) ** 2)
    if f >= F_KAEDE:
        v *= 1.0 - 0.55 * sh.smooth(F_KAEDE, F_KAEDE + 10, f)
    return v


cam = bc.camera("Cam", loc=(0, 0, 1.6), target=(0, 10, 1.8), lens=24)
frames = []
y = Y0
prev_vx = 0.0
for f in range(1, NF + 1):
    if f > 1:
        y += speed(f) / sh.FPS
    x = cam_x(y)
    vx = (cam_x(y + 0.3) - cam_x(y - 0.3)) / 0.6
    ax = vx - prev_vx
    prev_vx = vx
    up = sh.smooth(F_KAEDE - 6, F_KAEDE + 14, f)
    z = 1.7 + 0.25 * math.sin(f / 23.0) + 0.9 * up
    look = Vector((cam_x(y + 6), y + 6, z + 0.15 + 4.5 * up))
    loc = Vector((x, y, z))
    roll = max(-0.2, min(0.2, -0.35 * vx)) + 0.03 * math.sin(f / 7.0)
    lens = 24.0
    for h in F_DOWN:
        if f >= h:
            lens -= 2.2 * math.exp(-(f - h) / 6.0)
    frames.append({"f": f, "loc": tuple(loc), "fwd": tuple(look - loc), "roll": roll, "lens": lens})
sh.key_camera_frames(cam, frames)
print("camera y: 0 -> %.1f m, frames %d, downbeat frames %s, kaede frame %d" % (y, NF, F_DOWN, F_KAEDE), flush=True)

if A["lines"]:
    bc.gp_lineart("LineArt", radius=0.0055, color=LINE, crease_deg=140, noise=0.004, noise_step=2, opacity=0.9)

out_dir = os.path.join(sh.ROOT, A["out"])
os.makedirs(out_dir, exist_ok=True)
sh.set_jpeg_output(os.path.join(out_dir, "f_####"), quality=95)
if A["save_blend"]:
    bc.save_blend(os.path.join(out_dir, "stormB.blend"))

if A["mode"] == "stills":
    fl = [int(v) for v in str(A["frames"]).split(",") if v.strip()]
    print("STILLS", fl, sh.render_frames(os.path.join(out_dir, "still_####.jpg"), fl), flush=True)
elif A["mode"] == "full":
    import time
    sc = bpy.context.scene
    end = A["end"] or NF
    for f in range(A["start"], end + 1):
        dst = os.path.join(out_dir, "f_%04d.jpg" % f)
        if A["skip"] and os.path.exists(dst):
            continue
        sc.frame_set(f)
        sc.render.filepath = dst
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        print("FRAME %d %.2fs" % (f, time.perf_counter() - t0), flush=True)
    print("DONE frames=%d" % NF, flush=True)
