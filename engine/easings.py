"""
Animation Easings & Mathematical Interpolation Functions
"""

import math

def linear(t: float) -> float:
    return max(0.0, min(1.0, t))

def ease_in_quad(t: float) -> float:
    t = linear(t)
    return t * t

def ease_out_quad(t: float) -> float:
    t = linear(t)
    return t * (2.0 - t)

def ease_in_out_quad(t: float) -> float:
    t = linear(t)
    return 2.0 * t * t if t < 0.5 else -1.0 + (4.0 - 2.0 * t) * t

def ease_in_cubic(t: float) -> float:
    t = linear(t)
    return t * t * t

def ease_out_cubic(t: float) -> float:
    t = linear(t)
    t -= 1.0
    return t * t * t + 1.0

def ease_in_out_cubic(t: float) -> float:
    t = linear(t)
    return 4.0 * t * t * t if t < 0.5 else (t - 1.0) * (2.0 * t - 2.0) * (2.0 * t - 2.0) + 1.0

def ease_out_expo(t: float) -> float:
    t = linear(t)
    return 1.0 if t == 1.0 else 1.0 - math.pow(2.0, -10.0 * t)

def ease_in_out_expo(t: float) -> float:
    t = linear(t)
    if t == 0.0:
        return 0.0
    if t == 1.0:
        return 1.0
    if t < 0.5:
        return math.pow(2.0, 20.0 * t - 10.0) / 2.0
    return (2.0 - math.pow(2.0, -20.0 * t + 10.0)) / 2.0

def ease_out_elastic(t: float) -> float:
    t = linear(t)
    if t == 0.0:
        return 0.0
    if t == 1.0:
        return 1.0
    p = 0.3
    s = p / 4.0
    return math.pow(2.0, -10.0 * t) * math.sin((t - s) * (2.0 * math.pi) / p) + 1.0

def ease_out_back(t: float, s: float = 1.70158) -> float:
    t = linear(t)
    t -= 1.0
    return t * t * ((s + 1.0) * t + s) + 1.0

def ease_out_bounce(t: float) -> float:
    t = linear(t)
    if t < (1.0 / 2.75):
        return 7.5625 * t * t
    elif t < (2.0 / 2.75):
        t -= (1.5 / 2.75)
        return 7.5625 * t * t + 0.75
    elif t < (2.5 / 2.75):
        t -= (2.25 / 2.75)
        return 7.5625 * t * t + 0.9375
    else:
        t -= (2.625 / 2.75)
        return 7.5625 * t * t + 0.984375

def spring(t: float, damping: float = 12.0, frequency: float = 15.0) -> float:
    """Spring physics easing"""
    t = linear(t)
    return 1.0 - math.exp(-damping * t) * math.cos(frequency * t)

EASING_MAP = {
    "linear": linear,
    "ease_in_quad": ease_in_quad,
    "ease_out_quad": ease_out_quad,
    "ease_in_out_quad": ease_in_out_quad,
    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,
    "ease_out_expo": ease_out_expo,
    "ease_in_out_expo": ease_in_out_expo,
    "ease_out_elastic": ease_out_elastic,
    "ease_out_back": ease_out_back,
    "ease_out_bounce": ease_out_bounce,
    "spring": spring,
}

def get_easing(name: str):
    return EASING_MAP.get(name.lower(), ease_out_cubic)
