"""
Motion Design Templates for Blender, Manim, FFmpeg, and Web/Canvas
"""

BLENDER_3D_LOGO_ORBIT = """import bpy
import math

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 90

# Dark World
world = bpy.data.worlds.new("DarkWorld")
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.02, 0.03, 0.06, 1.0)
scene.world = world

# Create 3D Text
bpy.ops.object.text_add(location=(0, 0, 0))
text_obj = bpy.context.active_object
text_obj.data.body = "ANTIGRAVITY"
text_obj.data.extrude = 0.15
text_obj.data.bevel_depth = 0.02
text_obj.data.align_x = 'CENTER'
text_obj.data.align_y = 'CENTER'

# Glowing Neon Material
mat = bpy.data.materials.new(name="NeonCyan")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

emission = nodes.new(type='ShaderNodeEmission')
emission.inputs['Color'].default_value = (0.0, 0.85, 1.0, 1.0)
emission.inputs['Strength'].default_value = 8.0

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(emission.outputs['Emission'], output.inputs['Surface'])
text_obj.data.materials.append(mat)

# Camera Rig with Orbit Animation
bpy.ops.object.camera_add(location=(0, -6, 2))
cam = bpy.context.active_object
scene.camera = cam

track_constraint = cam.constraints.new(type='TRACK_TO')
track_constraint.target = text_obj
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis = 'UP_Y'

# Keyframe camera
cam.keyframe_insert(data_path="location", frame=1)
cam.location = (4.5 * math.sin(math.pi), -4.5 * math.cos(math.pi), 2.5)
cam.keyframe_insert(data_path="location", frame=90)

# Light
bpy.ops.object.light_add(type='POINT', radius=1.0, location=(2, -2, 4))
light = bpy.context.active_object
light.data.energy = 500.0
light.data.color = (0.2, 0.7, 1.0)
"""

MANIM_VECTOR_SCENE = """from manim import *

class ModernMotionGraphic(Scene):
    def construct(self):
        self.camera.background_color = "#0a0e17"
        
        title = Text("MOTION STUDIO", font="sans-serif", weight=BOLD, font_size=54)
        title.set_color_by_gradient("#38bdf8", "#818cf8")
        
        subtitle = Text("PROCEDURAL ANIMATION ENGINE", font="sans-serif", font_size=20, color="#94a3b8")
        subtitle.next_to(title, DOWN, buff=0.4)
        
        ring = Circle(radius=3.2, color="#38bdf8", stroke_width=3)
        ring.set_stroke(opacity=0.7)
        
        inner_dots = VGroup(*[
            Dot(point=ring.point_from_proportion(i/12.0), radius=0.08, color="#ec4899")
            for i in range(12)
        ])
        
        self.play(Create(ring), run_time=1.5, rate_func=smooth)
        self.play(FadeIn(inner_dots, lag_ratio=0.1), run_time=1.0)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.play(
            Rotate(ring, angle=PI, run_time=2.0),
            Rotate(inner_dots, angle=-PI, run_time=2.0)
        )
        self.wait(1)
"""

HTML5_CANVAS_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { margin: 0; background: #0b0f19; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; }
    canvas { box-shadow: 0 20px 50px rgba(0,0,0,0.8); border-radius: 12px; }
  </style>
</head>
<body>
  <canvas id="canvas" width="1280" height="720"></canvas>
  <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let t = 0;
    
    function draw() {
      t += 0.02;
      ctx.fillStyle = '#0b0f19';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      
      for (let i = 0; i < 5; i++) {
        ctx.beginPath();
        const r = 80 + i * 35 + Math.sin(t * 2 + i) * 10;
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.strokeStyle = `hsla(${200 + i * 25}, 90%, 60%, ${0.3 + 0.15 * Math.sin(t + i)})`;
        ctx.lineWidth = 2 + (i % 2);
        ctx.stroke();
      }
      
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 42px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.shadowColor = '#38bdf8';
      ctx.shadowBlur = 20;
      ctx.fillText('MOTION STUDIO', cx, cy);
      
      requestAnimationFrame(draw);
    }
    draw();
  </script>
</body>
</html>"""

TEMPLATES = {
    "blender_3d_orbit": BLENDER_3D_LOGO_ORBIT,
    "manim_vector_graphic": MANIM_VECTOR_SCENE,
    "html5_canvas_interactive": HTML5_CANVAS_TEMPLATE
}
