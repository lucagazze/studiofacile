import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

os.makedirs(r"c:\Users\lucag\Desktop\studiofacile\mockups\books", exist_ok=True)

def create_3d_book_mockup(front_cover_path, output_path, is_landscape=False, width=700, height=900):
    img = Image.open(front_cover_path).convert("RGBA")
    
    # Target book cover size in canvas
    if is_landscape:
        bw, bh = 540, 380
    else:
        bw, bh = 420, 600
        
    front = img.resize((bw, bh), Image.Resampling.LANCZOS)
    
    # Canvas
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Spine width
    spine_w = 30
    
    # Position
    ox = (width - (bw + spine_w)) // 2 + 10
    oy = (height - bh) // 2
    
    # Draw soft realistic shadow
    shadow_canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_canvas)
    
    # Elliptical contact and diffuse shadow
    shadow_draw.ellipse([ox - 20, oy + bh - 25, ox + bw + spine_w + 30, oy + bh + 45], fill=(16, 24, 40, 110))
    shadow_draw.ellipse([ox + 10, oy + bh - 15, ox + bw + spine_w + 10, oy + bh + 25], fill=(16, 24, 40, 160))
    
    # Skew shadow
    shadow_poly = [
        (ox, oy + bh - 10),
        (ox + spine_w + bw, oy + bh - 5),
        (ox + spine_w + bw + 40, oy + bh + 40),
        (ox - 30, oy + bh + 35)
    ]
    shadow_draw.polygon(shadow_poly, fill=(16, 24, 40, 80))
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(18))
    
    canvas.paste(shadow_canvas, (0, 0), shadow_canvas)
    
    # Draw 3D spine
    spine_img = Image.new("RGBA", (spine_w, bh), (38, 69, 160, 255))
    # Extract edge of front for spine tone
    edge = front.crop((0, 0, 10, bh)).resize((spine_w, bh))
    # Darken spine for 3D depth
    enhancer = ImageEnhance.Brightness(edge)
    spine_dark = enhancer.enhance(0.7)
    
    # Create gradient on spine
    gradient = Image.new('L', (spine_w, 1))
    for x in range(spine_w):
        gradient.putpixel((x, 0), int(255 * (0.5 + 0.5 * (x / spine_w))))
    grad_mask = gradient.resize((spine_w, bh))
    
    # Paste spine
    canvas.paste(spine_dark, (ox, oy))
    
    # Front cover overlay with subtle gloss/sheen
    front_with_sheen = front.copy()
    sheen = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen)
    # Left inner crease shadow
    for x in range(18):
        alpha = int(90 * (1.0 - (x / 18.0)))
        sheen_draw.line([(x, 0), (x, bh)], fill=(0, 0, 0, alpha))
    # Vertical specular highlight
    for x in range(18, 32):
        alpha = int(45 * (1.0 - abs(x - 25) / 7.0))
        sheen_draw.line([(x, 0), (x, bh)], fill=(255, 255, 255, alpha))
        
    front_with_sheen.alpha_composite(sheen)
    
    # Paste front cover
    canvas.paste(front_with_sheen, (ox + spine_w, oy))
    
    # Page thickness on top / bottom
    pages_top = ImageDraw.Draw(canvas)
    pages_top.polygon([
        (ox, oy),
        (ox + spine_w, oy),
        (ox + spine_w + 8, oy - 8),
        (ox + 8, oy - 8)
    ], fill=(230, 235, 245, 230), outline=(180, 190, 210, 180))
    
    # Save optimized WebP and PNG
    canvas.save(output_path, "WEBP", quality=92)
    png_path = output_path.replace(".webp", ".png")
    canvas.save(png_path, "PNG")
    print(f"Generated 3D mockup: {output_path}")

# Run for all books
items = [
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\emergenza_cover.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-emergenza.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\antibiotici_page0.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antibiotici.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\antinfiammatori_cover.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antinfiammatori.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\psicofarmaci_cover.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-psicofarmaci.webp", False),
    (r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\laboratorio_page0.png", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-laboratorio.webp", True),
]

for src, out, land in items:
    create_3d_book_mockup(src, out, land)
