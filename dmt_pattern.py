"""
DMT-inspired recursive nested square tunnels with 4-fold symmetry.
Matches the reference: bold lines, gradient depth shading, glossy center spheres.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

WIDTH, HEIGHT = 2400, 2400
STEPS = 100
ROTATION_DEG = 3.5
SHRINK = 0.965


def draw_vortex(draw, cx, cy, size, rot_dir=1):
    """Nested rotated squares with depth shading from line density + fills."""
    angle = 0.0
    s = size

    # First pass: filled polygons for gradient shading (light outside, dark inside)
    angle_tmp = 0.0
    s_tmp = size
    for i in range(STEPS):
        t = i / STEPS
        # Gradient: white at edge, dark gray at center
        gray = int(245 - 220 * (t ** 1.2))
        half_diag = s_tmp * 0.5
        corners = []
        for k in range(4):
            theta = math.radians(angle_tmp + 45 + 90 * k)
            x = cx + half_diag * math.cos(theta)
            y = cy + half_diag * math.sin(theta)
            corners.append((x, y))
        draw.polygon(corners, fill=(gray, gray, gray))
        angle_tmp += ROTATION_DEG * rot_dir
        s_tmp *= SHRINK

    # Second pass: crisp dark outlines on top
    for i in range(STEPS):
        t = i / STEPS
        # Outer lines bold, inner lines thin
        lw = max(1, int(2.5 * (1 - t * 0.5)))
        # Lines darken toward center
        line_gray = int(60 * (1 - t * 0.3))
        color = (line_gray, line_gray, line_gray)

        half_diag = s * 0.5
        corners = []
        for k in range(4):
            theta = math.radians(angle + 45 + 90 * k)
            x = cx + half_diag * math.cos(theta)
            y = cy + half_diag * math.sin(theta)
            corners.append((x, y))
        corners.append(corners[0])
        draw.line(corners, fill=color, width=lw)

        angle += ROTATION_DEG * rot_dir
        s *= SHRINK

    # Glossy dark sphere at center
    r = max(s * 1.2, 18)
    # Dark base
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(8, 8, 8))
    # Mid reflection
    rm = r * 0.7
    draw.ellipse([cx - rm * 0.8, cy - rm * 1.2, cx + rm * 0.4, cy - rm * 0.1],
                 fill=(60, 60, 60))
    # Specular highlight
    rh = r * 0.3
    draw.ellipse([cx - rh * 0.3, cy - rh * 2.2, cx + rh * 0.8, cy - rh * 0.8],
                 fill=(160, 160, 160))


def main():
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    half = WIDTH // 2
    q = WIDTH // 4
    vortex_size = half * 1.42  # sqrt(2) * half so square edges reach quadrant borders

    configs = [
        (q, q, 1),
        (q * 3, q, -1),
        (q, q * 3, -1),
        (q * 3, q * 3, 1),
    ]

    for cx, cy, rot_dir in configs:
        draw_vortex(draw, cx, cy, vortex_size, rot_dir)

    # Subtle center dividers
    draw.line([(half, 0), (half, HEIGHT)], fill=(210, 210, 210), width=3)
    draw.line([(0, half), (WIDTH, half)], fill=(210, 210, 210), width=3)

    out = '/Users/robin/Desktop/dmt_pattern.png'
    img.save(out, quality=95)
    print(f"Saved {WIDTH}x{HEIGHT} to {out}")


if __name__ == '__main__':
    main()
