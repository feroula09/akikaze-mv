r"""
pathA.py - 3D-A：石板小徑長鏡頭（s03-s04，B(8) -> B(21)，約 30.6 s）。

現在段：褪色的朽葉紅褐，和紙色霧氣。鏡頭從落葉高度起步、升到眼高，沿石板小徑穿過楓林往前推；
s04（B(17) 起）慢下來，停在小徑前方（小夜的背影由 engine 合成）。

Render on twos: frames 1,3,5... are written as consecutive f_0001, f_0002 ... -> engine `seq` fps 15.

  blender -b --factory-startup -P blender/shots/pathA.py -- --mode stills --frames 1,300,600,918 --res 50
  blender -b --factory-startup -P blender/shots/pathA.py -- --mode full --res 50
"""
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _shared as sh
import ak_common as ak
bc, bpy = sh.bc, sh.bpy
from mathutils import Vector, Matrix
import bmesh

A = bc.parse_args({"mode": "stills", "res": 50, "step": 2, "start": 1, "end": 0, "frames": "1,150,300,450,640,780,918",
                   "out": "blender/renders/pathA", "samples": 16, "save_blend": 0, "lines": 1, "skip": 0}, doc=__doc__)

AUD = sh.load_audio()
BAR = {b["index"]: b["start"] for b in AUD["bars"]}
T0, T_S04, T1 = BAR[8], BAR[17], BAR[21]
NF = int(math.ceil((T1 - T0) * sh.FPS - 1e-6))

# ---------------------------------------------------------------------------------------- palette
HAZE = "#ECE1D1"
LINE = "#5B4A43"
SKY = ((0.0, "#EFE5D6"), (0.5, "#EADCCB"), (1.0, "#E6D5C4"))

bc.reset_scene()
bc.setup_render("EEVEE", res=(1920, 1080), percent=A["res"], fps=30, samples=A["samples"], view="Standard")
bc.world_sky(stops=SKY, z_lo=-0.05, z_hi=0.6, sun_dir=None, ambient="#B8A898", ambient_strength=0.25, below="#E9DCCB")
SUN = (-0.45, 0.35, 0.82)
bc.sun("Sun", direction=SUN, color="#ffffff", strength=math.pi)
bc.sun("Fill", direction=(0.4, -0.6, 0.5), color="#ffffff", strength=math.pi * 0.12, shadow=False)


def toon(name, lit, shade, dark=None, hz=(6.0, 48.0)):
    return bc.toon_material(name, lit=lit, shade=shade, dark=dark, haze=HAZE, haze_range=hz, haze_max=0.9)


M_SLAB = toon("Slab", "#D8CDBF", "#A99D90")
M_ROCK = toon("Rock", "#BEB3A3", "#8C8276")
M_MOSS = toon("Moss", "#B7B18F", "#8A8569")
M_BANK = toon("Bank", "#CDB39A", "#A48B77")
M_EARTH = toon("Earth", "#C2AC98", "#9E8878")
M_BARK = toon("Bark", "#9C8272", "#6F5C52")
M_PLASTER = toon("Plaster", "#ECE2D2", "#C2B5A4")
M_WOOD = toon("Wood", "#927866", "#64534A")
M_ROOF = toon("Roof", "#827874", "#5A5350")
M_SHOJI = toon("Shoji", "#F5EFE4", "#D5CBBB")

LEAF_TINT = "#F6E0D6"          # fades the crimson sprites toward the 現在段 rose-brown
LEAF_MATS = [ak.leaf_material(f"Leaf_{k}", ak.leaf_png("red", k), tint=LEAF_TINT, haze=HAZE, haze_range=(5.0, 42.0),
                              haze_max=0.88) for k in "abc"]
LITTER_MATS = [ak.leaf_material(f"Litter_{k}", ak.leaf_png("red", k), tint="#E9CFC4", jitter=(0.72, 0.95), haze=HAZE,
                                haze_range=(5.0, 42.0), haze_max=0.88) for k in "abc"]

C_GEO = bc.collection("Geo")
C_LEAF = bc.collection("Leaves")
C_LEAF.lineart_usage = "EXCLUDE"
C_SRC = bc.collection("LeafSrc")
C_SRC.lineart_usage = "EXCLUDE"
CARDS = [ak.leaf_card(f"Card_{k}", m, C_SRC) for k, m in zip("abc", LEAF_MATS)]
LCARDS = [ak.leaf_card(f"LCard_{k}", m, C_SRC) for k, m in zip("abc", LITTER_MATS)]

# ---------------------------------------------------------------------------------------- path
PATH = ak.Centreline([(0, -12), (0, 0), (0.8, 12), (2.8, 24), (3.2, 36), (1.0, 48), (-2.2, 60), (-3.5, 75), (-2, 95), (0, 112)])
HALF = 1.3            # half width of the paving
WALL = 1.6            # wall line
BANK_Z = 0.75
S_MAX = PATH.length
R = ak.rng(8)

# paving slabs
bm = bmesh.new()
s = 0.3
while s < S_MAX - 0.5:
    depth = R.uniform(0.38, 0.55)
    n = R.choice((2, 3, 3, 4))
    while True:                                     # no slivers: every slab at least 0.5 m wide
        cuts = sorted(R.uniform(-HALF + 0.5, HALF - 0.5) for _ in range(n - 1))
        edges = [-HALF] + cuts + [HALF]
        if min(b - a for a, b in zip(edges, edges[1:])) >= 0.5:
            break
    t = PATH.tangent(s)
    yaw = math.atan2(t.y, t.x) - math.pi / 2
    for a, b in zip(edges, edges[1:]):
        lat = (a + b) / 2 + R.uniform(-0.03, 0.03)
        w = (b - a) / 2 - 0.035
        c = PATH.point(s + R.uniform(-0.03, 0.03), lat, 0.02)
        ak.rock(bm, c, (w, depth / 2 - 0.03, 0.05), R, rot_z=yaw + R.uniform(-0.05, 0.05), lump=0.06, subdiv=2)
    s += depth
SLABS = ak.bm_object("Slabs", bm, [M_SLAB], C_GEO)

# retaining walls (rocks, moss on upward faces of the top course)
bm = bmesh.new()
for side in (1, -1):
    for course, z in enumerate((0.2, 0.52)):
        s = 0.25 * course
        while s < S_MAX:
            ln = R.uniform(0.38, 0.55)
            t = PATH.tangent(s)
            yaw = math.atan2(t.y, t.x) - math.pi / 2
            c = PATH.point(s, side * (WALL + R.uniform(-0.03, 0.06) + 0.06 * course), z + R.uniform(-0.03, 0.03))
            fs = ak.rock(bm, c, (0.16, ln / 2, 0.19 + 0.03 * course), R, rot_z=yaw + R.uniform(-0.12, 0.12), lump=0.12, subdiv=2)
            if course == 1:
                for f in fs:
                    f.normal_update()
                    if f.normal.z > 0.55:
                        f.material_index = 1
            s += ln * 0.92
WALLS = ak.bm_object("Walls", bm, [M_ROCK, M_MOSS], C_GEO)

# ground under the path + raised banks behind the walls (left bank climbs into a hillside)
GROUND = bc.plane("Ground", size=(400, 400), loc=(0, 40, -0.01), coll=C_GEO, mat=M_EARTH)
bm = bmesh.new()
STEP = 1.0
for side in (1, -1):
    rows = []
    s = 0.0
    while s <= S_MAX + 0.01:
        row = []
        for lat, rise in ((WALL + 0.12, 0.0), (WALL + 0.9, 0.05), (6.0, 0.6), (14.0, 2.4 if side > 0 else 1.0), (40.0, 9.0 if side > 0 else 4.0)):
            row.append(bm.verts.new(PATH.point(s, side * lat, BANK_Z + rise)))
        rows.append(row)
        s += STEP
    # wall backing (vertical) so gaps between rocks never show the void
    back = [(bm.verts.new(PATH.point(sv, side * (WALL + 0.12), 0.0)), r[0]) for sv, r in zip([i * STEP for i in range(len(rows))], rows)]
    for (b0, t0_), (b1, t1_) in zip(back, back[1:]):
        bm.faces.new((b0, b1, t1_, t0_) if side > 0 else (b1, b0, t0_, t1_))
    for r0, r1 in zip(rows, rows[1:]):
        for k in range(len(r0) - 1):
            q = (r0[k], r0[k + 1], r1[k + 1], r1[k])
            bm.faces.new(q if side < 0 else tuple(reversed(q)))
BANKS = ak.bm_object("Banks", bm, [M_BANK], C_GEO)
for ob in (GROUND, BANKS):
    bc.lineart_usage(ob, "OCCLUSION_ONLY")


def bank_z(lat):
    a = abs(lat)
    if a < WALL + 0.9:
        return BANK_Z
    if a < 6.0:
        return BANK_Z + 0.05 + 0.55 * (a - WALL - 0.9) / (6.0 - WALL - 0.9)
    return BANK_Z + 0.6 + 1.8 * (a - 6.0) / 8.0 * (1.0 if lat > 0 else 0.22)


# ---------------------------------------------------------------------------------------- trees
LEAF_PTS = [[], [], []]       # per texture: (loc, rot, scale)


def add_cluster(center, radius, n, scale):
    cx, cy, cz = center
    rx, ry, rz = radius
    for _ in range(n):
        while True:
            u, v, w = R.uniform(-1, 1), R.uniform(-1, 1), R.uniform(-1, 1)
            if u * u + v * v + w * w <= 1:
                break
        LEAF_PTS[R.randrange(3)].append(((cx + u * rx, cy + v * ry, cz + w * rz),
                                         (R.uniform(0, 6.28), R.uniform(0, 6.28), R.uniform(0, 6.28)),
                                         R.uniform(*scale)))


bm = bmesh.new()


def tree(s, lat, height, lean, big=False, far=False):
    side = 1 if lat > 0 else -1
    base = PATH.point(s, lat, bank_z(lat) - 0.2)
    n = PATH.normal(s)
    inward = Vector((-n.x * side, -n.y * side, 0.0))
    t = PATH.tangent(s)
    along = Vector((t.x, t.y, 0.0))
    top = base + Vector((0, 0, height)) + inward * lean + along * R.uniform(-0.6, 0.6)
    mid = base + Vector((0, 0, height * 0.5)) + inward * lean * 0.15
    r0 = R.uniform(0.2, 0.3) * (1.3 if big else 1.0)
    trunk = ak.bezier(base, mid, top, n=9)
    ak.tube(bm, trunk, r0, r0 * 0.45, sides=8)
    leaf_scale = (0.45, 0.75) if far else (0.2, 0.36)
    nb = 2 if far else R.choice((3, 4, 4))
    for k in range(nb):
        root = trunk[R.randrange(5, 8)]
        toward = inward if k < nb - 1 else -inward
        tip = root + toward * R.uniform(2.0, 3.6) + along * R.uniform(-1.8, 1.8) + Vector((0, 0, R.uniform(0.4, 1.6)))
        ctrl = root.lerp(tip, 0.5) + Vector((0, 0, R.uniform(0.5, 1.0)))
        ak.tube(bm, ak.bezier(root, ctrl, tip, n=6), r0 * 0.4, 0.035, sides=6)
        rad = (R.uniform(2.0, 2.8), R.uniform(2.0, 2.8), R.uniform(0.9, 1.3))
        add_cluster(tip + Vector((0, 0, 0.2)), rad, 200 if far else 300, leaf_scale)
        add_cluster(root.lerp(tip, 0.55) + Vector((0, 0, 0.4)), (1.2, 1.2, 0.7), 40 if far else 70, leaf_scale)
    add_cluster(top + Vector((0, 0, 0.5)), (2.4, 2.4, 1.4), 220 if far else 260, leaf_scale)
    if not far:                                     # one long limb arching over the paving -> canopy tunnel
        root = trunk[6]
        tip = PATH.point(s + R.uniform(-1.5, 1.5), side * R.uniform(-0.6, 0.4), R.uniform(5.2, 6.2))
        ak.tube(bm, ak.bezier(root, root.lerp(tip, 0.5) + Vector((0, 0, 1.0)), tip, n=7), r0 * 0.38, 0.03, sides=6)
        add_cluster(tip, (2.6, 2.6, 1.0), 320, leaf_scale)
        add_cluster(root.lerp(tip, 0.5) + Vector((0, 0, 0.9)), (1.8, 1.8, 0.8), 140, leaf_scale)


s = 1.0
k = 0
while s < S_MAX - 6:
    side = 1 if (k % 2 == 0) ^ (R.random() < 0.25) else -1
    tree(s, side * R.uniform(3.0, 4.6), R.uniform(4.0, 5.4), R.uniform(1.2, 2.2), big=R.random() < 0.3)
    s += R.uniform(3.4, 5.0)
    k += 1
s = 0.0
while s < S_MAX:
    for side in (1, -1):
        if R.random() < 0.8:
            tree(s + R.uniform(-1.5, 1.5), side * R.uniform(7.5, 15.0), R.uniform(5.0, 7.0), R.uniform(0.5, 1.5), far=True)
    s += R.uniform(4.5, 7.0)
TREES = ak.bm_object("Trees", bm, [M_BARK], C_GEO)

# low red shrubs behind the walls
s = 2.0
while s < S_MAX - 4:
    side = R.choice((1, -1))
    lat = side * R.uniform(2.2, 3.4)
    add_cluster(PATH.point(s, lat, bank_z(lat) + R.uniform(0.35, 0.6)), (R.uniform(0.6, 1.0), R.uniform(0.6, 1.0), 0.45), 70, (0.16, 0.26))
    s += R.uniform(2.0, 4.5)

for k in range(3):
    pts = LEAF_PTS[k]
    bc.instance_on_points(f"Canopy_{k}", CARDS[k], [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts], coll=C_LEAF)

# fallen leaves: on the banks and a few on the paving
LIT = [[], [], []]
for _ in range(5200):
    s = R.uniform(0, S_MAX)
    lat = R.choice((1, -1)) * R.uniform(WALL + 0.3, 9.0)
    p = PATH.point(s, lat, bank_z(lat) + 0.03)
    LIT[R.randrange(3)].append((tuple(p), (R.uniform(-0.25, 0.25), R.uniform(-0.25, 0.25), R.uniform(0, 6.28)), R.uniform(0.12, 0.2)))
for _ in range(650):
    s = R.uniform(0, S_MAX)
    lat = R.uniform(-HALF, HALF) * (0.75 if R.random() < 0.6 else 1.0)
    p = PATH.point(s, lat, 0.085)
    LIT[R.randrange(3)].append((tuple(p), (R.uniform(-0.12, 0.12), R.uniform(-0.12, 0.12), R.uniform(0, 6.28)), R.uniform(0.11, 0.17)))
for k in range(3):
    pts = LIT[k]
    bc.instance_on_points(f"Litter_{k}", LCARDS[k], [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts], coll=C_LEAF)


# ---------------------------------------------------------------------------------------- houses
def house(s, lat, w, d, h, face_path=True):
    """Small Taisho tea-house: plaster walls, wood posts, shoji on the path side, tiled gable roof."""
    side = 1 if lat > 0 else -1
    t = PATH.tangent(s)
    yaw = math.atan2(t.y, t.x)
    o = PATH.point(s, lat, bank_z(lat) - 0.1)
    Mw = Matrix.Translation(o) @ Matrix.Rotation(yaw, 4, "Z")      # local x along the path, local +y = left of path
    fy = -side * d / 2                                              # path-facing wall in local y
    parts = []

    def bx(name, size, loc, mat, rot=(0, 0, 0)):
        ob = bc.box(name, size=size, coll=C_GEO, mat=mat, origin="CENTER")
        from mathutils import Euler
        ob.matrix_world = Mw @ Matrix.Translation(loc) @ Euler(rot).to_matrix().to_4x4()
        parts.append(ob)
        return ob
    bx("HBase", (w + 0.3, d + 0.3, 0.45), (0, 0, 0.225), M_ROCK)
    bx("HWall", (w, d, h), (0, 0, 0.45 + h / 2), M_PLASTER)
    for x in [-w / 2 + i * w / 4 for i in range(5)]:
        bx("HPost", (0.14, 0.14, h), (x, fy - side * 0.05, 0.45 + h / 2), M_WOOD)
    bx("HBeam", (w + 0.1, 0.16, 0.16), (0, fy - side * 0.06, 0.45 + h - 0.1), M_WOOD)
    bx("HSill", (w + 0.1, 0.12, 0.1), (0, fy - side * 0.06, 0.45 + 0.75), M_WOOD)
    for i in range(4):
        x0 = -w / 2 + i * w / 4 + w / 8
        bx("HShoji", (w / 4 - 0.2, 0.04, h - 1.1), (x0, fy - side * 0.03, 0.45 + 0.8 + (h - 1.1) / 2), M_SHOJI)
        for j in range(1, 4):
            bx("HKumiko", (0.025, 0.06, h - 1.1), (x0 - (w / 4 - 0.2) / 2 + j * (w / 4 - 0.2) / 4, fy - side * 0.05, 0.45 + 0.8 + (h - 1.1) / 2), M_WOOD)
        for j in range(1, 5):
            bx("HKumiko", (w / 4 - 0.2, 0.06, 0.025), (x0, fy - side * 0.05, 0.45 + 0.8 + j * (h - 1.1) / 5), M_WOOD)
    pitch = math.radians(27)
    half = d / 2 + 0.7
    rl = half / math.cos(pitch)
    ridge = 0.45 + h + (d / 2) * math.tan(pitch)
    for sgn in (1, -1):
        bx("HRoof", (w + 1.2, rl, 0.12), (0, sgn * half / 2, ridge - (half / 2) * math.tan(pitch)), M_ROOF, rot=(-sgn * pitch, 0, 0))
    bx("HRidge", (w + 1.3, 0.22, 0.2), (0, 0, ridge + 0.05), M_ROOF)
    return parts


house(60.0, -6.0, 6.0, 4.2, 2.6)
house(86.0, 5.5, 4.2, 3.4, 2.4)

# ---------------------------------------------------------------------------------------- camera
S_CAM0 = 10.0
V = 1.15                      # m/s walking dolly
T_STOP = T_S04 + 6.3
H0, H1 = 0.8, 1.55
T_RISE = BAR[12]              # 4 bars: low -> eye height (the title sits over these bars)


def speed(t):
    if t < T_S04:
        return V * (0.75 + 0.25 * sh.smooth(T0, T0 + 3.0, t))
    return V * (1.0 - sh.smoother(T_S04, T_STOP, t))


cam = bc.camera("Cam", loc=(0, 0, 1), target=(0, 10, 1), lens=28)
frames = []
s_cam = S_CAM0
for f in range(1, NF + 1):
    t = sh.time_of(f, T0)
    if f > 1:
        s_cam += speed(t) / sh.FPS
    k = sh.ease_in_out_sine(sh.clamp((t - T0) / (T_RISE - T0)))
    h = sh.lerp(H0, H1, k)
    sway = 0.22 * math.sin(2 * math.pi * (t - T0) / 11.0)
    loc = PATH.point(s_cam, sway, h)
    look = PATH.point(s_cam + 8.0, sway * 0.4, sh.lerp(0.35, 1.2, k))
    fwd = look - loc
    roll = math.radians(0.5) * math.sin(2 * math.pi * (t - T0) / 13.0)
    frames.append({"f": f, "loc": tuple(loc), "fwd": tuple(fwd), "roll": roll, "lens": 28.0})
sh.key_camera_frames(cam, frames)
print("camera s: %.1f -> %.1f m  (path %.1f m), frames %d" % (S_CAM0, s_cam, S_MAX, NF), flush=True)

# ---------------------------------------------------------------------------------------- lines + output
if A["lines"]:
    bc.gp_lineart("LineArt", radius=0.0055, color=LINE, crease_deg=140, noise=0.004, noise_step=2, opacity=0.9)

out_dir = os.path.join(sh.ROOT, A["out"])
os.makedirs(out_dir, exist_ok=True)
sh.set_jpeg_output(os.path.join(out_dir, "f_####"), quality=95)
if A["save_blend"]:
    bc.save_blend(os.path.join(out_dir, "pathA.blend"))

if A["mode"] == "stills":
    fl = [int(x) for x in str(A["frames"]).split(",") if x.strip()]
    times = sh.render_frames(os.path.join(out_dir, "still_####.jpg"), fl)
    print("STILLS", fl, times, flush=True)
elif A["mode"] == "full":
    src = list(range(1, NF + 1, A["step"]))
    end = A["end"] or len(src)
    import time
    sc = bpy.context.scene
    for k in range(A["start"], end + 1):
        dst = os.path.join(out_dir, "f_%04d.jpg" % k)
        if A["skip"] and os.path.exists(dst):
            continue
        sc.frame_set(src[k - 1])
        sc.render.filepath = dst
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        print("FRAME %d (src %d) %.2fs" % (k, src[k - 1], time.perf_counter() - t0), flush=True)
    print("DONE frames=%d fps=%g" % (len(src), sh.FPS / A["step"]), flush=True)
