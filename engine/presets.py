"""
High-End Motion Graphics Presets & Procedural Generators
"""

import math
import json
from .vector_engine import VectorScene
from .easings import get_easing, spring, ease_out_cubic, ease_out_back, ease_in_out_quad

def create_kinetic_typography_scene(
    text: str,
    subtitle: str = "",
    style: str = "spring_bounce",
    font_size: int = 72,
    accent_color: str = "#38bdf8",
    text_color: str = "#ffffff",
    bg_color: str = "#0a0e17",
    width: int = 1920,
    height: int = 1080,
    duration: float = 3.5,
    fps: int = 30
) -> VectorScene:
    scene = VectorScene(width=width, height=height, fps=fps, duration=duration, bg_color=bg_color)
    words = text.strip().split()
    total_words = len(words)

    grad_def = (
        f'<linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{text_color}" />'
        f'<stop offset="100%" stop-color="{accent_color}" />'
        f'</linearGradient>'
    )
    scene.add_def(grad_def)

    def render_typography(t, frame, time, width, height):
        parts = []
        center_x = width / 2.0
        center_y = height / 2.0 - (30 if subtitle else 0)

        # Ambient floating particle grid
        for i in range(25):
            px = (i * 137.5) % width
            py = ((i * 219.3) + time * 20.0) % height
            alpha = 0.2 + 0.15 * math.sin(time * 2.0 + i)
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{1.5 + (i%3)}" fill="{accent_color}" opacity="{alpha:.2f}" />')

        word_gap = font_size * 0.65
        approx_word_widths = [len(w) * (font_size * 0.52) for w in words]
        total_text_width = sum(approx_word_widths) + (total_words - 1) * word_gap
        start_x = center_x - total_text_width / 2.0

        current_x = start_x
        for idx, word in enumerate(words):
            w_width = approx_word_widths[idx]
            word_center_x = current_x + w_width / 2.0

            word_start_t = idx * (0.35 / max(1, total_words))
            rel_t = max(0.0, min(1.0, (t - word_start_t) / 0.45))

            if rel_t > 0.0:
                if style == "spring_bounce":
                    scale = spring(rel_t, damping=10.0, frequency=14.0)
                    dy = (1.0 - ease_out_cubic(rel_t)) * 80.0
                    alpha = min(1.0, rel_t * 2.5)
                elif style == "glitch":
                    scale = 1.0 + (1.0 - rel_t) * 0.3 * math.sin(rel_t * 30.0)
                    dy = (1.0 - rel_t) * 40.0
                    alpha = min(1.0, rel_t * 3.0)
                else:
                    scale = 1.0
                    dy = (1.0 - ease_out_cubic(rel_t)) * 60.0
                    alpha = ease_out_cubic(rel_t)

                transform = f'transform="translate({word_center_x:.1f}, {center_y + dy:.1f}) scale({max(0.01, scale):.3f}) translate(-{word_center_x:.1f}, -{center_y + dy:.1f})"'
                parts.append(
                    f'<text x="{word_center_x:.1f}" y="{center_y + dy:.1f}" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="{font_size}" fill="url(#titleGrad)" text-anchor="middle" opacity="{alpha:.2f}" {transform} filter="url(#glow-subtle)">{word}</text>'
                )

            current_x += w_width + word_gap

        if subtitle:
            sub_t = max(0.0, min(1.0, (t - 0.4) / 0.5))
            if sub_t > 0.0:
                sub_y = center_y + font_size * 0.9 + 25.0
                sub_dy = (1.0 - ease_out_cubic(sub_t)) * 30.0
                sub_alpha = ease_out_cubic(sub_t)

                badge_w = len(subtitle) * 16.0 + 40.0
                parts.append(
                    f'<rect x="{center_x - badge_w/2.0:.1f}" y="{sub_y - 24.0 + sub_dy:.1f}" width="{badge_w:.1f}" height="36" rx="18" fill="{accent_color}" fill-opacity="0.15" stroke="{accent_color}" stroke-width="1.5" stroke-opacity="{sub_alpha:.2f}" />'
                )
                parts.append(
                    f'<text x="{center_x:.1f}" y="{sub_y + sub_dy:.1f}" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="20" letter-spacing="3" fill="{accent_color}" text-anchor="middle" opacity="{sub_alpha:.2f}">{subtitle.upper()}</text>'
                )

        return "\n".join(parts)

    scene.elements.append(render_typography)
    return scene


def create_hud_interface_scene(
    title: str = "SYSTEM INITIALIZED",
    accent_color: str = "#00f0ff",
    secondary_color: str = "#ff0055",
    bg_color: str = "#050811",
    width: int = 1920,
    height: int = 1080,
    duration: float = 4.0,
    fps: int = 30
) -> VectorScene:
    scene = VectorScene(width=width, height=height, fps=fps, duration=duration, bg_color=bg_color)

    def render_hud(t, frame, time, width, height):
        parts = []
        cx, cy = width / 2.0, height / 2.0

        # Background grid scanlines
        parts.append(f'<line x1="0" y1="{cy}" x2="{width}" y2="{cy}" stroke="{accent_color}" stroke-width="0.7" stroke-opacity="0.2" stroke-dasharray="4 8" />')
        parts.append(f'<line x1="{cx}" y1="0" x2="{cx}" y2="{height}" stroke="{accent_color}" stroke-width="0.7" stroke-opacity="0.2" stroke-dasharray="4 8" />')

        rot1 = time * 45.0
        rot2 = -time * 60.0
        rot3 = time * 90.0

        radius_outer = 260.0
        circ_outer = 2 * math.pi * radius_outer
        stroke_dash1 = f"{circ_outer * 0.25:.1f} {circ_outer * 0.08:.1f} {circ_outer * 0.12:.1f} {circ_outer * 0.05:.1f}"

        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius_outer}" fill="none" stroke="{accent_color}" stroke-width="2" stroke-opacity="0.7" stroke-dasharray="{stroke_dash1}" transform="rotate({rot1:.1f} {cx} {cy})" filter="url(#glow)" />'
        )

        radius_mid = 210.0
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius_mid}" fill="none" stroke="{secondary_color}" stroke-width="3" stroke-opacity="0.8" stroke-dasharray="30 50 120 40" transform="rotate({rot2:.1f} {cx} {cy})" />'
        )

        radius_inner = 150.0
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius_inner}" fill="none" stroke="{accent_color}" stroke-width="1.5" stroke-dasharray="8 12" transform="rotate({rot3:.1f} {cx} {cy})" />'
        )

        pulse = 0.8 + 0.2 * math.sin(time * 8.0)
        core_r = 75.0 * pulse
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{core_r:.1f}" fill="{accent_color}" fill-opacity="0.15" stroke="{accent_color}" stroke-width="2" filter="url(#glow)" />'
        )

        progress_val = int(min(100.0, ease_in_out_quad(min(1.0, t * 1.3)) * 100.0))
        parts.append(
            f'<text x="{cx}" y="{cy + 10}" font-family="monospace" font-weight="bold" font-size="36" fill="{accent_color}" text-anchor="middle" filter="url(#glow)">{progress_val}%</text>'
        )

        parts.append(
            f'<text x="{cx}" y="{cy + radius_outer + 60}" font-family="monospace" font-weight="700" font-size="24" letter-spacing="6" fill="#ffffff" text-anchor="middle">[ {title} ]</text>'
        )

        telemetry = f"TIME: {time:.2f}s | FPS: {fps} | COORD: ({int(cx + math.sin(time)*50)}, {int(cy + math.cos(time)*50)}) | STATUS: ACTIVE"
        parts.append(
            f'<text x="40" y="60" font-family="monospace" font-size="14" fill="{accent_color}" opacity="0.75">{telemetry}</text>'
        )
        parts.append(
            f'<rect x="30" y="42" width="4" height="24" fill="{accent_color}" />'
        )

        return "\n".join(parts)

    scene.elements.append(render_hud)
    return scene


def create_waveform_visualizer_scene(
    title: str = "AUDIO SPECTRUM VISUALIZER",
    bar_count: int = 48,
    accent_color: str = "#ec4899",
    secondary_color: str = "#8b5cf6",
    bg_color: str = "#09090b",
    width: int = 1920,
    height: int = 1080,
    duration: float = 4.0,
    fps: int = 30
) -> VectorScene:
    scene = VectorScene(width=width, height=height, fps=fps, duration=duration, bg_color=bg_color)

    grad_def = (
        f'<linearGradient id="barGrad" x1="0%" y1="100%" x2="0%" y2="0%">'
        f'<stop offset="0%" stop-color="{secondary_color}" />'
        f'<stop offset="100%" stop-color="{accent_color}" />'
        f'</linearGradient>'
    )
    scene.add_def(grad_def)

    def render_waveform(t, frame, time, width, height):
        parts = []
        cx, cy = width / 2.0, height / 2.0 + 40
        total_width = width * 0.75
        bar_w = (total_width / bar_count) * 0.65
        gap = (total_width / bar_count) * 0.35
        start_x = cx - total_width / 2.0

        parts.append(
            f'<text x="{cx}" y="{cy - 240}" font-family="system-ui, sans-serif" font-weight="800" font-size="32" letter-spacing="4" fill="#ffffff" text-anchor="middle" filter="url(#glow-subtle)">{title}</text>'
        )

        parts.append(
            f'<line x1="{start_x - 40}" y1="{cy}" x2="{start_x + total_width + 40}" y2="{cy}" stroke="{accent_color}" stroke-width="2" stroke-opacity="0.6" filter="url(#glow)" />'
        )

        for i in range(bar_count):
            bx = start_x + i * (bar_w + gap)
            freq1 = math.sin(time * 5.0 + i * 0.25)
            freq2 = math.cos(time * 3.5 + i * 0.4)
            freq3 = math.sin(time * 8.0 + i * 0.15)
            envelope = math.sin((i / float(bar_count)) * math.pi)
            amp = max(8.0, (abs(freq1 * 0.5 + freq2 * 0.3 + freq3 * 0.2) * 180.0 + 20.0) * envelope)

            parts.append(
                f'<rect x="{bx:.1f}" y="{cy - amp:.1f}" width="{bar_w:.1f}" height="{amp:.1f}" rx="{bar_w/2.0:.1f}" fill="url(#barGrad)" filter="url(#glow-subtle)" />'
            )
            parts.append(
                f'<rect x="{bx:.1f}" y="{cy + 4:.1f}" width="{bar_w:.1f}" height="{amp * 0.35:.1f}" rx="{bar_w/2.0:.1f}" fill="url(#barGrad)" opacity="0.25" />'
            )

        return "\n".join(parts)

    scene.elements.append(render_waveform)
    return scene


def create_lottie_spec(preset: str = "checkmark", primary_color: str = "#22c55e") -> dict:
    """Generates valid Bodymovin / Lottie JSON data"""
    lottie_data = {
        "v": "5.7.4",
        "fr": 60,
        "ip": 0,
        "op": 120,
        "w": 512,
        "h": 512,
        "nm": f"Lottie_{preset}",
        "ddd": 0,
        "assets": [],
        "layers": []
    }

    hex_clean = primary_color.lstrip("#")
    if len(hex_clean) == 6:
        r, g, b = [int(hex_clean[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    else:
        r, g, b = 0.13, 0.77, 0.36

    layer = {
        "ddd": 0,
        "ind": 1,
        "ty": 4,
        "nm": "Shape 1",
        "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100},
            "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [256, 256, 0]},
            "a": {"a": 0, "k": [0, 0, 0]},
            "s": {
                "a": 1,
                "k": [
                    {"i": {"x": [0.2, 0.2, 0.2], "y": [1, 1, 1]}, "o": {"x": [0.4, 0.4, 0.4], "y": [0, 0, 0]}, "t": 0, "s": [0, 0, 100]},
                    {"i": {"x": [0.2, 0.2, 0.2], "y": [1, 1, 1]}, "o": {"x": [0.4, 0.4, 0.4], "y": [0, 0, 0]}, "t": 30, "s": [115, 115, 100]},
                    {"t": 45, "s": [100, 100, 100]}
                ]
            }
        },
        "shapes": [
            {
                "ty": "gr",
                "it": [
                    {
                        "ty": "el",
                        "d": 1,
                        "p": {"a": 0, "k": [0, 0]},
                        "s": {"a": 0, "k": [220, 220]}
                    },
                    {
                        "ty": "fl",
                        "c": {"a": 0, "k": [r, g, b, 1]},
                        "o": {"a": 0, "k": 100}
                    },
                    {
                        "ty": "tr",
                        "p": {"a": 0, "k": [0, 0]},
                        "a": {"a": 0, "k": [0, 0]},
                        "s": {"a": 0, "k": [100, 100]},
                        "r": {"a": 0, "k": 0},
                        "o": {"a": 0, "k": 100}
                    }
                ]
            }
        ]
    }
    lottie_data["layers"].append(layer)
    return lottie_data
