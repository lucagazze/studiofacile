import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

os.makedirs(r"c:\Users\lucag\Desktop\studiofacile\mockups\books", exist_ok=True)

def render_photorealistic_book(cover_path, out_path, spine_color=(38, 69, 160), angle=12, is_landscape=False):
    # Load original cover
    orig = Image.open(cover_path).convert("RGBA")
    
    if is_landscape:
        # Standard landscape book
        bw, bh = 560, 395
    else:
        # Standard portrait book
        bw, bh = 430, 610
        
    front = orig.resize((bw, bh), Image.Resampling.LANCZOS)
    
    canvas_w = 800
    canvas_h = 750 if is_landscape else 880
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    # 1. Ground Shadow (multi-layer realistic shadow)
    shadow_img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    
    cx = canvas_w // 2 + 10
    cy = (canvas_h - bh) // 2 + bh
    
    # Ambient diffuse shadow
    sdraw.ellipse([cx - bw//2 - 40, cy - 35, cx + bw//2 + 50, cy + 55], fill=(15, 23, 42, 70))
    # Contact core shadow
    sdraw.ellipse([cx - bw//2 - 10, cy - 20, cx + bw//2 + 20, cy + 25], fill=(15, 23, 42, 130))
    # Directional cast shadow
    cast_poly = [
        (cx - bw//2, cy - 10),
        (cx + bw//2 + 15, cy - 8),
        (cx + bw//2 + 65, cy + 45),
        (cx - bw//2 - 20, cy + 40)
    ]
    sdraw.polygon(cast_poly, fill=(15, 23, 42, 90))
    
    shadow_blurred = shadow_img.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(shadow_blurred, (0, 0), shadow_blurred)
    
    # 2. Book Spine
    spine_w = 32
    ox = (canvas_w - (bw + spine_w)) // 2
    oy = (canvas_h - bh) // 2 - 10
    
    # Create spine gradient with authentic 3D curve
    spine = Image.new("RGBA", (spine_w, bh), (0, 0, 0, 0))
    spine_draw = ImageDraw.Draw(spine)
    
    edge_sample = front.crop((0, 0, 15, bh)).resize((spine_w, bh))
    # Darken and add cylinder lighting
    enhancer = ImageEnhance.Brightness(edge_sample)
    spine_base = enhancer.enhance(0.75)
    
    spine_grad = Image.new("RGBA", (spine_w, bh), (0, 0, 0, 0))
    for x in range(spine_w):
        # Cylinder shading curve
        factor = math.sin((x / spine_w) * math.pi * 0.85)
        alpha_dark = int(140 * (1.0 - factor * 0.8))
        for y in range(bh):
            spine_grad.putpixel((x, y), (0, 0, 0, alpha_dark))
            
    spine.paste(spine_base, (0, 0))
    spine.alpha_composite(spine_grad)
    
    # Paste Spine
    canvas.paste(spine, (ox, oy))
    
    # 3. Pages Top & Bottom block (realistic paper edge)
    top_poly = [
        (ox, oy),
        (ox + spine_w, oy),
        (ox + spine_w + 10, oy - 10),
        (ox + 10, oy - 10)
    ]
    top_paper = ImageDraw.Draw(canvas)
    top_paper.polygon(top_poly, fill=(238, 240, 246, 255), outline=(190, 198, 214, 200))
    
    # Paper lines on top edge
    for i in range(1, 4):
        shift = i * 2.5
        top_paper.line([
            (ox + shift, oy - shift),
            (ox + spine_w + shift, oy - shift)
        ], fill=(210, 216, 230, 180), width=1)
        
    # 4. Front Cover with Sheen and Crease
    front_mod = front.copy()
    sheen = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen)
    
    # Left hinge crease
    for x in range(24):
        a = int(110 * (1.0 - (x / 24.0)))
        sheen_draw.line([(x, 0), (x, bh)], fill=(0, 0, 0, a))
        
    # Specular light gleam
    for x in range(20, 48):
        dist = abs(x - 34)
        a = int(55 * max(0, 1.0 - (dist / 14.0)))
        sheen_draw.line([(x, 0), (x, bh)], fill=(255, 255, 255, a))
        
    front_mod.alpha_composite(sheen)
    
    # Add subtle border to front
    border_draw = ImageDraw.Draw(front_mod)
    border_draw.rectangle([0, 0, bw - 1, bh - 1], outline=(0, 0, 0, 45), width=1)
    
    canvas.paste(front_mod, (ox + spine_w, oy))
    
    # Save optimized WebP and PNG
    canvas.save(out_path, "WEBP", quality=95)
    png_path = out_path.replace(".webp", ".png")
    canvas.save(png_path, "PNG")
    print(f"Photorealistic render: {out_path}")

# Run renders
books_data = [
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\emergenza_cover.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-emergenza.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\antibiotici_page0.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antibiotici.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\antinfiammatori_cover.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antinfiammatori.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\psicofarmaci_cover.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-psicofarmaci.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\laboratorio_page0.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-laboratorio.webp", True),
]

for src, out, land in books_data:
    render_photorealistic_book(src, out, is_landscape=land)

print("Individual renders completed.")
