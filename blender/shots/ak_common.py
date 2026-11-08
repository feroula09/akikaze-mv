r"""
ak_common.py - helpers shared by the two 秋風恋歌 3D shots (pathA.py, stormB.py).

  * leaf cards: the 2D maple sprites (assets/prop/prop_leaf_*.png) on alpha-dithered quads,
    flat watercolour colour + per-instance brightness jitter + distance haze
  * bmesh builders: lumpy rocks / slabs, tapered tubes (trunks, branches)
  * Catmull-Rom centreline sampling for the path
"""
import os
import math
import random

import _shared as sh
bc = sh.bc
bpy = sh.bpy
import bmesh
from mathutils import Vector, Matrix

ROOT = sh.ROOT
PROP = os.path.join(ROOT, "assets", "prop")


def leaf_png(color, k):
    return os.path.join(PROP, f"prop_leaf_{color}_{k}.png")


# ------------------------------------------------------------------------------------ materials
def leaf_material(name, img_path, tint="#ffffff", jitter=(0.8, 1.05), haze=None, haze_range=(8.0, 60.0),
                  haze_max=0.85, strength=1.0):
    """Unlit leaf card: texture colour x tint x per-instance brightness, alpha from the PNG.
    Dithered transparency so cards cast dappled shadows onto the toon surfaces."""
    m, nt, out = bc.new_material(name)
    N, L = nt.nodes, nt.links
    tex = N.new("ShaderNodeTexImage")
    tex.location = (-900, 0)
    tex.image = bpy.data.images.load(img_path, check_existing=True)
    tex.image.alpha_mode = "STRAIGHT"
    oi = N.new("ShaderNodeObjectInfo")
    oi.location = (-900, -300)
    mr = N.new("ShaderNodeMapRange")
    mr.location = (-700, -300)
    mr.inputs["To Min"].default_value = jitter[0]
    mr.inputs["To Max"].default_value = jitter[1]
    L.new(oi.outputs["Random"], mr.inputs["Value"])
    mul = N.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.location = (-500, 0)
    mul.inputs["Factor"].default_value = 1.0
    L.new(tex.outputs["Color"], mul.inputs["A"])
    mul.inputs["B"].default_value = bc.rgb(tint)
    bri = N.new("ShaderNodeMix")
    bri.data_type = "RGBA"
    bri.blend_type = "MULTIPLY"
    bri.location = (-300, 0)
    bri.inputs["Factor"].default_value = 1.0
    L.new(mul.outputs["Result"], bri.inputs["A"])
    cmb = N.new("ShaderNodeCombineColor")
    cmb.location = (-500, -300)
    for i in range(3):
        L.new(mr.outputs[0], cmb.inputs[i])
    L.new(cmb.outputs[0], bri.inputs["B"])
    col = bri.outputs["Result"]
    if haze:
        col = bc._haze(nt, col, haze, haze_range, haze_max)
    em = N.new("ShaderNodeEmission")
    em.location = (100, 0)
    em.inputs["Strength"].default_value = strength
    L.new(col, em.inputs["Color"])
    tr = N.new("ShaderNodeBsdfTransparent")
    tr.location = (100, -200)
    mix = N.new("ShaderNodeMixShader")
    mix.location = (400, 0)
    L.new(tex.outputs["Alpha"], mix.inputs[0])
    L.new(tr.outputs[0], mix.inputs[1])
    L.new(em.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], out.inputs["Surface"])
    for attr, val in (("surface_render_method", "DITHERED"), ("use_transparent_shadow", True)):
        try:
            setattr(m, attr, val)
        except (AttributeError, TypeError):
            pass
    m.use_backface_culling = False
    return m


def leaf_card(name, mat, coll=None):
    """1 x 1 m quad centred on the origin in XY with UVs (the instancing source)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    vs = [bm.verts.new(p) for p in ((-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0))]
    f = bm.faces.new(vs)
    for loop, (u, v) in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        loop[uv].uv = (u, v)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bc.link(ob, coll)
    me.materials.append(mat)
    bc.hide_source(ob)
    return ob


# ------------------------------------------------------------------------------------ geometry
def rock(bm, center, size, rnd, rot_z=0.0, lump=0.18, subdiv=1):
    """Lumpy ellipsoid stone added to bm (smooth shaded). Returns its faces."""
    sx, sy, sz = size
    mat = Matrix.Translation(center) @ Matrix.Rotation(rot_z, 4, "Z") @ Matrix.Diagonal((sx, sy, sz, 1.0))
    res = bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0, matrix=mat)
    vs = res["verts"]
    c = Vector(center)
    for v in vs:
        d = v.co - c
        v.co = c + d * (1.0 + lump * (rnd.random() - 0.5))
    faces = list({f for v in vs for f in v.link_faces})
    for f in faces:
        f.smooth = True
    return faces


def tube(bm, pts, r0, r1, sides=7):
    """Tapered tube along polyline pts (list of Vector), radius r0 -> r1. Capped at the root."""
    n = len(pts)
    rings = []
    prev_side = None
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        side = prev_side if prev_side is not None else (t.orthogonal().normalized())
        side = (side - t * side.dot(t)).normalized()     # keep frame continuous (no twist)
        prev_side = side
        up = t.cross(side).normalized()
        r = r0 + (r1 - r0) * (i / (n - 1))
        ring = [bm.verts.new(p + (side * math.cos(a) + up * math.sin(a)) * r)
                for a in (2 * math.pi * k / sides for k in range(sides))]
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for k in range(sides):
            f = bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]))
            f.smooth = True
    bm.faces.new(list(reversed(rings[0])))
    return rings


def bezier(p0, p1, p2, n=8):
    p0, p1, p2 = Vector(p0), Vector(p1), Vector(p2)
    return [(1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2 for t in (i / (n - 1) for i in range(n))]


def bm_object(name, bm, mats, coll=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    bc.link(ob, coll)
    return ob


# ------------------------------------------------------------------------------------ path
class Centreline:
    """Catmull-Rom through 2D control points, re-sampled by arc length.
    at(s) -> (x, y), tangent(s) -> unit (x, y), normal(s) = tangent rotated +90 deg (to the left)."""

    def __init__(self, ctrl, step=0.05):
        P = [Vector((x, y)) for x, y in ctrl]
        P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
        dense = []
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            for k in range(40):
                t = k / 40
                dense.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        dense.append(P[-2])
        self.pts, self.s = [dense[0]], [0.0]
        for p in dense[1:]:
            self.s.append(self.s[-1] + (p - self.pts[-1]).length)
            self.pts.append(p)
        self.length = self.s[-1]

    def at(self, s):
        s = max(0.0, min(self.length, s))
        lo, hi = 0, len(self.s) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.s[mid] <= s:
                lo = mid
            else:
                hi = mid
        span = self.s[hi] - self.s[lo] or 1.0
        return self.pts[lo].lerp(self.pts[hi], (s - self.s[lo]) / span)

    def tangent(self, s):
        return (self.at(s + 0.2) - self.at(s - 0.2)).normalized()

    def normal(self, s):
        t = self.tangent(s)
        return Vector((-t.y, t.x))

    def point(self, s, lateral=0.0, z=0.0):
        p = self.at(s) + self.normal(s) * lateral
        return Vector((p.x, p.y, z))


def rng(seed):
    return random.Random(seed)


# ------------------------------------------------------------------------------------ falling leaves
def falling_leaves(name, card, pts, z_range, wind=(0.0, 0.0, 0.0), coll=None, gust_dir=(0.0, -1.0, 0.3)):
    """Animated leaf swarm in ONE Geometry Nodes object, driven by Scene Time (deterministic).
    pts: list of dicts {co, fall (m/s), sway (m), phase, rot0 (euler), spin (rad/s xyz), scale}.
    z wraps inside z_range so the fall never runs dry. wind = constant drift (m/s).
    Returns (object, gust_value_socket): key the socket (metres of extra displacement along
    gust_dir, scaled per leaf) for a gust."""
    n = len(pts)
    me = bpy.data.meshes.new(name + "_pts")
    me.vertices.add(n)
    me.vertices.foreach_set("co", [c for p in pts for c in p["co"]])

    def attr(key, kind, vals):
        a = me.attributes.new(key, kind, "POINT")
        a.data.foreach_set("vector" if kind == "FLOAT_VECTOR" else "value", vals)
    attr("fall", "FLOAT", [p["fall"] for p in pts])
    attr("sway", "FLOAT", [p["sway"] for p in pts])
    attr("phase", "FLOAT", [p["phase"] for p in pts])
    attr("rot0", "FLOAT_VECTOR", [c for p in pts for c in p["rot0"]])
    attr("spin", "FLOAT_VECTOR", [c for p in pts for c in p["spin"]])
    attr("scl", "FLOAT", [p["scale"] for p in pts])
    me.update()
    ob = bpy.data.objects.new(name, me)
    bc.link(ob, coll)

    ng = bpy.data.node_groups.new(name + "_GN", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, Lk = ng.nodes, ng.links

    def node(kind, **kw):
        nd = N.new(kind)
        for k, v in kw.items():
            setattr(nd, k, v)
        return nd

    def named(key, vec=False):
        nd = node("GeometryNodeInputNamedAttribute", data_type="FLOAT_VECTOR" if vec else "FLOAT")
        nd.inputs["Name"].default_value = key
        return nd.outputs["Attribute"]

    def math(op, a, b=None, c=None):
        nd = node("ShaderNodeMath", operation=op)
        for i, v in enumerate((a, b, c)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                nd.inputs[i].default_value = v
            else:
                Lk.new(v, nd.inputs[i])
        return nd.outputs[0]

    def vmath(op, a, b):
        nd = node("ShaderNodeVectorMath", operation=op)
        for i, v in enumerate((a, b)):
            if isinstance(v, (tuple, list)):
                nd.inputs[i].default_value = v
            else:
                Lk.new(v, nd.inputs[i])
        return nd.outputs[0]

    gi, go = node("NodeGroupInput"), node("NodeGroupOutput")
    m2p = node("GeometryNodeMeshToPoints")
    Lk.new(gi.outputs[0], m2p.inputs["Mesh"])
    t = node("GeometryNodeInputSceneTime").outputs["Seconds"]
    gust = node("ShaderNodeValue", name="Gust")
    gust.outputs[0].default_value = 0.0
    pos = node("GeometryNodeInputPosition").outputs[0]
    sep = node("ShaderNodeSeparateXYZ")
    Lk.new(pos, sep.inputs[0])
    phase = named("phase")
    z = math("WRAP", math("SUBTRACT", sep.outputs["Z"], math("MULTIPLY", named("fall"), t)), z_range[1], z_range[0])
    swing = math("MULTIPLY", named("sway"), math("SINE", math("ADD", math("MULTIPLY", t, 1.7), phase)))
    swing2 = math("MULTIPLY", named("sway"), math("COSINE", math("ADD", math("MULTIPLY", t, 1.1), math("MULTIPLY", phase, 1.3))))
    x = math("ADD", math("ADD", sep.outputs["X"], swing), math("MULTIPLY", t, wind[0]))
    y = math("ADD", math("ADD", sep.outputs["Y"], math("MULTIPLY", swing2, 0.6)), math("MULTIPLY", t, wind[1]))
    cmb = node("ShaderNodeCombineXYZ")
    Lk.new(x, cmb.inputs[0])
    Lk.new(y, cmb.inputs[1])
    Lk.new(z, cmb.inputs[2])
    def vscale(vec, s):
        nd = node("ShaderNodeVectorMath", operation="SCALE")
        if isinstance(vec, (tuple, list)):
            nd.inputs[0].default_value = vec
        else:
            Lk.new(vec, nd.inputs[0])
        Lk.new(s, nd.inputs["Scale"])
        return nd.outputs[0]

    g_amt = math("MULTIPLY", gust.outputs[0], math("ADD", 0.6, math("MULTIPLY", phase, 0.12)))
    newpos = vmath("ADD", cmb.outputs[0], vscale(gust_dir, g_amt))
    sp = node("GeometryNodeSetPosition")
    Lk.new(m2p.outputs["Points"], sp.inputs["Geometry"])
    Lk.new(newpos, sp.inputs["Position"])
    info = node("GeometryNodeObjectInfo", transform_space="ORIGINAL")
    info.inputs["Object"].default_value = card
    try:
        info.inputs["As Instance"].default_value = True
    except KeyError:
        pass
    iop = node("GeometryNodeInstanceOnPoints")
    Lk.new(sp.outputs[0], iop.inputs["Points"])
    Lk.new(info.outputs["Geometry"], iop.inputs["Instance"])
    rot = vmath("ADD", named("rot0", True), vscale(named("spin", True), math("ADD", t, math("MULTIPLY", gust.outputs[0], 0.35))))
    e2r = node("FunctionNodeEulerToRotation")
    Lk.new(rot, e2r.inputs[0])
    Lk.new(e2r.outputs[0], iop.inputs["Rotation"])
    Lk.new(named("scl"), iop.inputs["Scale"])
    Lk.new(iop.outputs["Instances"], go.inputs[0])
    mod = ob.modifiers.new("Swarm", "NODES")
    mod.node_group = ng
    return ob, gust.outputs[0]
