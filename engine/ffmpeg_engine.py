"""
FFmpeg Video Compositing & Post-FX Engine
"""

import os
import subprocess
import tempfile
from typing import Optional, List, Dict, Any

def apply_video_fx(
    input_video: str,
    output_video: str,
    effect: str = "glow",
    vignette: bool = True,
    color_grade: str = "none",
    speed: float = 1.0
) -> Dict[str, Any]:
    """Applies AE-style post effects to a video using FFmpeg filterchains."""
    if not os.path.exists(input_video):
        return {"error": True, "message": f"Input video not found: {input_video}"}

    filters = []

    # Speed ramp / adjustment
    if speed != 1.0 and speed > 0:
        filters.append(f"setpts={1.0/speed}*PTS")

    # Color grading
    if color_grade == "cyberpunk":
        filters.append("curves=r='0/0 0.5/0.3 1/1':b='0/0.15 0.5/0.7 1/1':g='0/0 0.5/0.4 1/0.9'")
    elif color_grade == "teal_orange":
        filters.append("curves=r='0/0.05 0.5/0.65 1/1':b='0/0.1 0.5/0.4 1/0.85'")
    elif color_grade == "vintage":
        filters.append("curves=vintage,colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131")
    elif color_grade == "monochrome_high_contrast":
        filters.append("hue=s=0,eq=contrast=1.4:brightness=0.02")

    # Effect filters
    if effect == "glow":
        filters.append("gblur=sigma=4:steps=2")
    elif effect == "glitch":
        filters.append("rgbashift=rh=8:bh=-8:rv=2:bv=-2")
    elif effect == "motion_blur":
        filters.append("tblend=all_mode=average")

    # Vignette
    if vignette:
        filters.append("vignette=PI/4")

    vf = ",".join(filters) if filters else "null"

    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", input_video,
        "-vf", vf,
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        output_video
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        return {"error": True, "message": res.stderr}

    return {"success": True, "output_path": output_video, "size_bytes": os.path.getsize(output_video)}


def blend_transition(
    video1: str,
    video2: str,
    output_video: str,
    transition: str = "fade",
    duration: float = 1.0,
    offset: float = 2.0
) -> Dict[str, Any]:
    """Applies cross-dissolve, wipe, slide, or zoom transition between two video clips."""
    xfade_trans = {
        "fade": "fade",
        "wipeleft": "wipeleft",
        "wiperight": "wiperight",
        "slideup": "slideup",
        "slidedown": "slidedown",
        "circlecrop": "circlecrop",
        "dissolve": "dissolve",
        "pixelize": "pixelize"
    }.get(transition.lower(), "fade")

    cmd = [
        "ffmpeg", "-y",
        "-i", video1,
        "-i", video2,
        "-filter_complex", f"xfade=transition={xfade_trans}:duration={duration}:offset={offset}",
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        output_video
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        return {"error": True, "message": res.stderr}

    return {"success": True, "output_path": output_video, "size_bytes": os.path.getsize(output_video)}
