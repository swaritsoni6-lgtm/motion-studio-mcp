# Motion Studio MCP Server 🎬✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![MCP Protocol](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet)](https://modelcontextprotocol.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)

An AI-driven **Model Context Protocol (MCP)** server for programmatic 2D/3D motion design, kinetic typography, Lottie micro-interactions, and FFmpeg video compositing.

Allows LLMs and AI pair programmers to design, keyframe, and render studio-grade motion graphics directly to **MP4 (H.264)**, **GIF (palette-quantized)**, and **WebM (VP9)**.

---

## 🚀 Key Capabilities

### 1. 🎨 Parameterized Motion Graphics
* **`create_motion_graphic`**:
  * **`kinetic_typography`**: Multi-word spring-bounce reveals, staggered delays, ambient floating particle fields, glowing gradients, and subtitle badges.
  * **`hud_interface`**: Sci-Fi holographic dials, rotating compass brackets, live telemetry counter ($0\% \to 100\%$), and pulsing core.
  * **`waveform_visualizer`**: Audio spectrum bars with multi-frequency harmonic oscillations and mirrored floor reflections.

### 2. 🧮 Custom Mathematical & Vector Scenes
* **`render_programmatic_animation`**:
  * Full Python animation environment with easing curves (`spring`, `ease_out_cubic`, `ease_out_back`, `ease_in_out_expo`), SVG vector rendering, and 60fps frame compilation via FFmpeg.

### 3. 📱 Bodymovin / Lottie Web Animations
* **`create_lottie_animation`**:
  * Generates clean `.json` animations (checkmarks, loaders, pulse rings) ready for web, iOS, and Android runtimes.

### 4. 🎞️ Post-FX & Video Compositing
* **`apply_video_composite_fx`**:
  * After Effects-style post-processing: Bloom glow, chromatic RGB glitch, cinematic color grades (`cyberpunk`, `teal_orange`, `vintage`), vignettes, speed ramping, and clip transitions (`xfade`).

### 5. 🧊 3D Blender & Manim Integration
* **`render_blender_scene`**:
  * Generates and runs headless Blender Python (`bpy`) scripts (3D text extrusion, camera paths, emission shaders, Cycles/EEVEE).
* **`get_animation_templates`**:
  * Ready-to-use boilerplate for Blender 3D, Manim, and interactive HTML5 Canvas.

---

## 📦 Installation & Setup

### Prerequisites
* **Python 3.10+**
* **FFmpeg** (with `librsvg` and `libx264` support)

```bash
# Clone the repository
git clone https://github.com/swaritsoni6-lgtm/motion-studio-mcp.git
cd motion-studio-mcp
```

### Adding to Antigravity / Claude Desktop / MCP Clients

Add the server entry to your `mcp_config.json`:

```json
{
  "mcpServers": {
    "motion-studio": {
      "command": "python3",
      "args": [
        "/path/to/motion-studio-mcp/server.py"
      ]
    }
  }
}
```

---

## 🛠️ Tool Specifications

### `create_motion_graphic`
```json
{
  "preset": "kinetic_typography",
  "title": "CODE MEETS CREATIVITY",
  "subtitle": "PROGRAMMATIC MOTION REVOLUTION",
  "accent_color": "#38bdf8",
  "output_format": "mp4",
  "duration": 3.0,
  "width": 1920,
  "height": 1080,
  "fps": 30
}
```

### `render_programmatic_animation`
```json
{
  "python_render_code": "def render(t, frame, time, width, height):\n    cx, cy = width / 2.0, height / 2.0\n    return f'<circle cx=\"{cx}\" cy=\"{cy}\" r=\"{100*t}\" fill=\"#38bdf8\" />'",
  "duration": 2.0,
  "output_format": "mp4"
}
```

### `apply_video_composite_fx`
```json
{
  "input_video": "input.mp4",
  "output_video": "output_glitched.mp4",
  "effect": "glitch",
  "color_grade": "cyberpunk",
  "vignette": true
}
```

---

## 🌐 Interactive Web Player
Open [`player.html`](./player.html) in your browser to interactively scrub, inspect, and preview all rendered animation clips in real-time.

---

## 📄 License
This project is licensed under the [MIT License](./LICENSE).
