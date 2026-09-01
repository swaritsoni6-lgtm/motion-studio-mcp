"""
Vector Animation Engine
Renders mathematical SVG scenes and compiles them directly to MP4/GIF/WebM via FFmpeg.
"""

import os
import sys
import math
import subprocess
import tempfile
from typing import List, Dict, Any, Optional, Callable
from .easings import get_easing, ease_out_cubic, spring

class VectorScene:
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30, duration: float = 3.0, bg_color: str = "#0d1117"):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.total_frames = int(fps * duration)
        self.bg_color = bg_color
        self.elements = []
        self.defs = []

    def add_def(self, svg_def_string: str):
        self.defs.append(svg_def_string)

    def render_frame_svg(self, frame_idx: int) -> str:
        t = frame_idx / float(self.total_frames - 1) if self.total_frames > 1 else 0.0
        time_sec = frame_idx / float(self.fps)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            '<defs>',
            '  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">',
            '    <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>',
            '  <filter id="glow-subtle" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur" />',
            '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '  </filter>'
        ]
        svg_parts.extend(self.defs)
        svg_parts.append('</defs>')

        # Background
        if self.bg_color:
            svg_parts.append(f'<rect width="100%" height="100%" fill="{self.bg_color}" />')

        for elem in self.elements:
            if callable(elem):
                res = elem(t=t, frame=frame_idx, time=time_sec, width=self.width, height=self.height)
                if res:
                    svg_parts.append(res)
            elif isinstance(elem, str):
                svg_parts.append(elem)

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def compile(self, output_path: str, format_type: str = "mp4") -> str:
        """Compiles all frames into high quality video / GIF using FFmpeg"""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            frame_pattern = os.path.join(tmpdir, "frame%05d.svg")
            for i in range(self.total_frames):
                frame_svg = self.render_frame_svg(i)
                filepath = os.path.join(tmpdir, f"frame{i:05d}.svg")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(frame_svg)

            if format_type.lower() == "gif":
                palette_path = os.path.join(tmpdir, "palette.png")
                cmd_palette = [
                    "ffmpeg", "-y", "-framerate", str(self.fps),
                    "-i", frame_pattern,
                    "-vf", f"fps={self.fps},scale={self.width}:-1:flags=lanczos,palettegen",
                    palette_path
                ]
                subprocess.run(cmd_palette, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                cmd_gif = [
                    "ffmpeg", "-y", "-framerate", str(self.fps),
                    "-i", frame_pattern,
                    "-i", palette_path,
                    "-lavfi", f"fps={self.fps},scale={self.width}:-1:flags=lanczos [x]; [x][1:v] paletteuse",
                    output_path
                ]
                subprocess.run(cmd_gif, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif format_type.lower() == "webm":
                cmd = [
                    "ffmpeg", "-y", "-framerate", str(self.fps),
                    "-i", frame_pattern,
                    "-c:v", "libvpx-vp9", "-b:v", "2M", "-pix_fmt", "yuva420p",
                    output_path
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else: # mp4
                cmd = [
                    "ffmpeg", "-y", "-framerate", str(self.fps),
                    "-i", frame_pattern,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p",
                    output_path
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output_path
