# Motion Studio MCP Server 🎬✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![MCP Protocol](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet)](https://modelcontextprotocol.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)

An AI-driven **Model Context Protocol (MCP)** server for programmatic 2D/3D motion design, kinetic typography, Lottie micro-interactions, and FFmpeg video compositing.

Allows LLMs and AI pair programmers to design, keyframe, and render studio-grade motion graphics directly to **MP4 (H.264)**, **GIF (palette-quantized)**, and **WebM (VP9)**.

---

## ⚡ 1-Prompt Standalone Antigravity Setup

You can copy and send the following standalone prompt to **Google Antigravity (AGY)**. It contains the repository link and complete setup instructions so the AI can perform the installation, registration, and verification autonomously in one turn:

```text
Please set up the Motion Studio MCP animation server (https://github.com/swaritsoni6-lgtm/motion-studio-mcp.git) for me:

1. Clone the repository https://github.com/swaritsoni6-lgtm/motion-studio-mcp.git into my Antigravity scratch directory (e.g. ~/.gemini/antigravity/scratch/motion-studio-mcp).
2. Register the MCP server in my ~/.gemini/config/mcp_config.json under the key "motion-studio":
   {
     "mcpServers": {
       "motion-studio": {
         "command": "python3",
         "args": ["<path-to-cloned-repo>/server.py"]
       }
     }
   }
3. Test and verify the installation by calling the `create_motion_graphic` tool to render a 2-second 1080p kinetic typography animation with title "HELLO ANTIGRAVITY" and subtitle "MOTION STUDIO ACTIVE" to an MP4 video.
4. Report back the output video location and confirm the available motion design tools (kinetic typography, HUD interfaces, waveform visualizers, Lottie JSON, video post-FX, and 3D scenes).
```

---

## 💬 Example Prompts to Use Once Installed

Once registered, you can ask your Antigravity agent to create animations with natural language:

* **Kinetic Typography:**
  > *"Render a 3-second kinetic typography MP4 saying 'LAUNCH DAY IS HERE' with glowing cyan and purple gradients, subtitle 'VERSION 2.0 LIVE', at 1080p."*
* **Sci-Fi HUD Hologram:**
  > *"Create a 600x600 looping GIF of a cyberpunk holographic HUD dial with rotating compass brackets and a live 0-100% data telemetry counter."*
* **Audio Waveform Visualizer:**
  > *"Generate an audio spectrum visualizer animation with neon pink and purple oscillating frequency bars and mirrored floor reflections."*
* **Custom Mathematical & 3D Geometry:**
  > *"Render a 3D wireframe dodecahedron rotating on 3 axes with glowing vertices and perspective depth using the programmatic animation engine."*
* **Video Post-Processing & Glitch FX:**
  > *"Take my input video `promo.mp4`, apply a chromatic aberration RGB glitch effect, add a cinematic vignette, and apply a cyberpunk color grading LUT."*
* **Lottie UI Micro-Interactions:**
  > *"Generate a Bodymovin/Lottie JSON animation for a success checkmark badge with emerald green color for my web app."*

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

## 📦 Manual Installation & Configuration

### Prerequisites
* **Python 3.10+**
* **FFmpeg** (with `librsvg` and `libx264` support)

```bash
# Clone the repository
git clone https://github.com/swaritsoni6-lgtm/motion-studio-mcp.git
cd motion-studio-mcp
```

### Configuration (`mcp_config.json`)

Add the server to your `~/.gemini/config/mcp_config.json` (or Claude Desktop `claude_desktop_config.json`):

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

## 🛠️ Tool Schema Reference

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
