#!/usr/bin/env python3
"""
Motion Studio Model Context Protocol (MCP) Server
Enables programmatic 2D/3D motion graphics rendering, kinetic typography, Lottie generation, and FFmpeg video compositing.
"""

import sys
import json
import os
import subprocess
import tempfile
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.vector_engine import VectorScene
from engine.easings import get_easing
from engine.presets import (
    create_kinetic_typography_scene,
    create_hud_interface_scene,
    create_waveform_visualizer_scene,
    create_lottie_spec
)
from engine.templates import TEMPLATES
from engine.ffmpeg_engine import apply_video_fx, blend_transition

DEFAULT_OUTPUT_DIR = os.path.expanduser("~/.gemini/antigravity/scratch/renders")

TOOLS = [
    {
        "name": "create_motion_graphic",
        "description": "Generates and renders high-end motion graphics (kinetic typography, sci-fi HUD interfaces, audio spectrum visualizers) directly to MP4 or GIF.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "preset": {
                    "type": "string",
                    "enum": ["kinetic_typography", "hud_interface", "waveform_visualizer"],
                    "description": "The style of motion graphic preset to generate."
                },
                "title": {
                    "type": "string",
                    "description": "Main headline or title text."
                },
                "subtitle": {
                    "type": "string",
                    "description": "Secondary subline / caption text (optional)."
                },
                "accent_color": {
                    "type": "string",
                    "description": "Primary accent hex color (e.g., #38bdf8 or #00f0ff)."
                },
                "secondary_color": {
                    "type": "string",
                    "description": "Secondary accent hex color (e.g., #ff0055 or #8b5cf6)."
                },
                "bg_color": {
                    "type": "string",
                    "description": "Background hex color (e.g., #0a0e17 or #09090b)."
                },
                "output_format": {
                    "type": "string",
                    "enum": ["mp4", "gif", "webm"],
                    "description": "Video/animation format (default: mp4)."
                },
                "output_path": {
                    "type": "string",
                    "description": "Absolute output filepath (optional; default generates in scratch/renders/)."
                },
                "duration": {
                    "type": "number",
                    "description": "Duration in seconds (default: 3.5s)."
                },
                "width": {
                    "type": "integer",
                    "description": "Width in pixels (default: 1920)."
                },
                "height": {
                    "type": "integer",
                    "description": "Height in pixels (default: 1080)."
                },
                "fps": {
                    "type": "integer",
                    "description": "Frames per second (default: 30)."
                }
            },
            "required": ["preset", "title"]
        }
    },
    {
        "name": "render_programmatic_animation",
        "description": "Renders a custom Python code-driven vector animation scene to MP4/GIF using mathematical easing, paths, and gradients.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "python_render_code": {
                    "type": "string",
                    "description": "Python snippet defining a `def render(t, frame, time, width, height):` function that returns an SVG elements string."
                },
                "output_path": {
                    "type": "string",
                    "description": "Target output path for the rendered video/gif."
                },
                "output_format": {
                    "type": "string",
                    "enum": ["mp4", "gif", "webm"],
                    "description": "Format to compile (default: mp4)."
                },
                "duration": {
                    "type": "number",
                    "description": "Duration in seconds (default: 3.0)."
                },
                "fps": {
                    "type": "integer",
                    "description": "Frames per second (default: 30)."
                },
                "width": {
                    "type": "integer",
                    "description": "Width in pixels (default: 1920)."
                },
                "height": {
                    "type": "integer",
                    "description": "Height in pixels (default: 1080)."
                },
                "bg_color": {
                    "type": "string",
                    "description": "Background hex color (default: #0d1117)."
                }
            },
            "required": ["python_render_code"]
        }
    },
    {
        "name": "create_lottie_animation",
        "description": "Generates Bodymovin/Lottie JSON animation specification for web, iOS, and Android vector animations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "preset": {
                    "type": "string",
                    "enum": ["checkmark", "spinner", "pulse_ring"],
                    "description": "Type of UI micro-interaction to generate."
                },
                "primary_color": {
                    "type": "string",
                    "description": "Hex color code for the animated elements."
                },
                "output_path": {
                    "type": "string",
                    "description": "Absolute output path for the .json Lottie file."
                }
            },
            "required": ["preset"]
        }
    },
    {
        "name": "apply_video_composite_fx",
        "description": "Applies After Effects-style post-processing (bloom/glow, chromatic glitch, cyberpunk/vintage color grades, vignette, motion blur, or transitions) to video files via FFmpeg.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_video": {
                    "type": "string",
                    "description": "Path to the source video."
                },
                "output_video": {
                    "type": "string",
                    "description": "Path to save the processed video."
                },
                "effect": {
                    "type": "string",
                    "enum": ["none", "glow", "glitch", "motion_blur"],
                    "description": "Visual effect filter to apply."
                },
                "color_grade": {
                    "type": "string",
                    "enum": ["none", "cyberpunk", "teal_orange", "vintage", "monochrome_high_contrast"],
                    "description": "Color grading LUT preset."
                },
                "vignette": {
                    "type": "boolean",
                    "description": "Whether to apply a cinematic dark edge vignette."
                },
                "speed": {
                    "type": "number",
                    "description": "Speed multiplier (1.0 = normal, 2.0 = 2x fast forward, 0.5 = slow motion)."
                }
            },
            "required": ["input_video", "output_video"]
        }
    },
    {
        "name": "render_blender_scene",
        "description": "Executes or generates a Blender Python (bpy) 3D motion graphics script. If Blender CLI is installed, renders frames to video; otherwise exports a validated .py script and instructions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bpy_script": {
                    "type": "string",
                    "description": "Python bpy script setting up the 3D scene, materials, camera animations, and lighting."
                },
                "output_file": {
                    "type": "string",
                    "description": "Target video output path."
                },
                "engine": {
                    "type": "string",
                    "enum": ["BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "CYCLES"],
                    "description": "Render engine to use in Blender."
                }
            },
            "required": ["bpy_script"]
        }
    },
    {
        "name": "get_animation_templates",
        "description": "Fetches ready-to-use template code for 3D Blender scenes, Manim vector graphics, or interactive HTML5 Canvas animations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_type": {
                    "type": "string",
                    "enum": ["blender_3d_orbit", "manim_vector_graphic", "html5_canvas_interactive", "all"],
                    "description": "The template to retrieve."
                }
            }
        }
    }
]

def handle_create_motion_graphic(args):
    preset = args.get("preset", "kinetic_typography")
    title = args.get("title", "MOTION GRAPHIC")
    subtitle = args.get("subtitle", "")
    accent_color = args.get("accent_color", "#38bdf8")
    secondary_color = args.get("secondary_color", "#ff0055")
    bg_color = args.get("bg_color", "#0a0e17")
    output_format = args.get("output_format", "mp4")
    duration = float(args.get("duration", 3.5))
    width = int(args.get("width", 1920))
    height = int(args.get("height", 1080))
    fps = int(args.get("fps", 30))

    output_path = args.get("output_path")
    if not output_path:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"{preset}_{int(duration)}s.{output_format}")

    if preset == "kinetic_typography":
        scene = create_kinetic_typography_scene(
            text=title,
            subtitle=subtitle,
            accent_color=accent_color,
            bg_color=bg_color,
            width=width,
            height=height,
            duration=duration,
            fps=fps
        )
    elif preset == "hud_interface":
        scene = create_hud_interface_scene(
            title=title,
            accent_color=accent_color,
            secondary_color=secondary_color,
            bg_color=bg_color,
            width=width,
            height=height,
            duration=duration,
            fps=fps
        )
    elif preset == "waveform_visualizer":
        scene = create_waveform_visualizer_scene(
            title=title,
            accent_color=accent_color,
            secondary_color=secondary_color,
            bg_color=bg_color,
            width=width,
            height=height,
            duration=duration,
            fps=fps
        )
    else:
        return {"error": True, "message": f"Unknown preset: {preset}"}

    compiled_file = scene.compile(output_path=output_path, format_type=output_format)
    file_size = os.path.getsize(compiled_file) if os.path.exists(compiled_file) else 0

    return {
        "success": True,
        "preset": preset,
        "output_path": compiled_file,
        "format": output_format,
        "duration": duration,
        "resolution": f"{width}x{height}",
        "fps": fps,
        "file_size_bytes": file_size,
        "message": f"Successfully rendered {preset} animation to {compiled_file} ({file_size / 1024:.1f} KB)"
    }


def handle_render_programmatic_animation(args):
    code = args.get("python_render_code", "")
    output_format = args.get("output_format", "mp4")
    duration = float(args.get("duration", 3.0))
    fps = int(args.get("fps", 30))
    width = int(args.get("width", 1920))
    height = int(args.get("height", 1080))
    bg_color = args.get("bg_color", "#0d1117")

    output_path = args.get("output_path")
    if not output_path:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"custom_anim_{int(duration)}s.{output_format}")

    scene = VectorScene(width=width, height=height, fps=fps, duration=duration, bg_color=bg_color)

    local_env = {
        "scene": scene,
        "math": sys.modules["math"],
        "get_easing": get_easing,
        "VectorScene": VectorScene
    }

    try:
        exec(code, local_env)
        if "render" in local_env and callable(local_env["render"]):
            scene.elements.append(local_env["render"])

        compiled_file = scene.compile(output_path=output_path, format_type=output_format)
        file_size = os.path.getsize(compiled_file) if os.path.exists(compiled_file) else 0
        return {
            "success": True,
            "output_path": compiled_file,
            "size_bytes": file_size,
            "resolution": f"{width}x{height}",
            "frames_rendered": scene.total_frames
        }
    except Exception as e:
        return {"error": True, "message": str(e), "traceback": traceback.format_exc()}


def handle_create_lottie_animation(args):
    preset = args.get("preset", "checkmark")
    primary_color = args.get("primary_color", "#22c55e")
    output_path = args.get("output_path")

    if not output_path:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"lottie_{preset}.json")

    lottie_json = create_lottie_spec(preset=preset, primary_color=primary_color)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(lottie_json, f, indent=2)

    return {
        "success": True,
        "output_path": output_path,
        "preset": preset,
        "data_summary": {
            "version": lottie_json.get("v"),
            "frame_rate": lottie_json.get("fr"),
            "width": lottie_json.get("w"),
            "height": lottie_json.get("h"),
            "total_frames": lottie_json.get("op")
        }
    }


def handle_apply_video_composite_fx(args):
    input_video = args.get("input_video")
    output_video = args.get("output_video")
    effect = args.get("effect", "none")
    color_grade = args.get("color_grade", "none")
    vignette = args.get("vignette", True)
    speed = float(args.get("speed", 1.0))

    return apply_video_fx(
        input_video=input_video,
        output_video=output_video,
        effect=effect,
        vignette=vignette,
        color_grade=color_grade,
        speed=speed
    )


def handle_render_blender_scene(args):
    bpy_script = args.get("bpy_script")
    output_file = args.get("output_file")
    if not output_file:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_file = os.path.join(DEFAULT_OUTPUT_DIR, "blender_render.mp4")

    blender_bin = subprocess.run(["which", "blender"], capture_output=True, text=True).stdout.strip()
    if not blender_bin:
        script_path = os.path.splitext(output_file)[0] + "_script.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(bpy_script)
        return {
            "success": True,
            "blender_installed": False,
            "script_saved_to": script_path,
            "message": "Blender binary not found on local path. Script has been saved and is ready to run with `blender -b -P " + script_path + "`."
        }

    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(bpy_script)
        temp_script = f.name

    try:
        cmd = [blender_bin, "-b", "-P", temp_script, "-o", output_file, "-a"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "success": res.returncode == 0,
            "output_path": output_file,
            "stdout": res.stdout[-500:],
            "stderr": res.stderr[-500:] if res.stderr else ""
        }
    finally:
        if os.path.exists(temp_script):
            os.remove(temp_script)


def handle_get_animation_templates(args):
    template_type = args.get("template_type", "all")
    if template_type in TEMPLATES:
        return {"template_name": template_type, "code": TEMPLATES[template_type]}
    return {"templates": TEMPLATES}


def handle_tool_call(name, args):
    if name == "create_motion_graphic":
        return handle_create_motion_graphic(args)
    elif name == "render_programmatic_animation":
        return handle_render_programmatic_animation(args)
    elif name == "create_lottie_animation":
        return handle_create_lottie_animation(args)
    elif name == "apply_video_composite_fx":
        return handle_apply_video_composite_fx(args)
    elif name == "render_blender_scene":
        return handle_render_blender_scene(args)
    elif name == "get_animation_templates":
        return handle_get_animation_templates(args)
    else:
        return {"error": True, "message": f"Unknown tool: {name}"}


def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "motion-studio-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()

            elif method == "notifications/initialized":
                pass

            elif method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS
                    }
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                tool_res = handle_tool_call(tool_name, tool_args)

                is_error = isinstance(tool_res, dict) and tool_res.get("error", False)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(tool_res, indent=2)
                            }
                        ],
                        "isError": is_error
                    }
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()

            elif method == "ping":
                res = {"jsonrpc": "2.0", "id": req_id, "result": {}}
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()

            else:
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method {method} not found"
                    }
                }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()

        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e),
                    "data": traceback.format_exc()
                }
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
