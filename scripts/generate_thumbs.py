import os
from PIL import Image

def generate_toast_thumbs():
    thumbs = [
        ("emergenza", r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\emergenza_cover.png"),
        ("antibiotici", r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\antibiotici_page0.png"),
        ("antinfiammatori", r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\antinfiammatori_cover.png"),
        ("psicofarmaci", r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\psicofarmaci_cover.png"),
        ("laboratorio", r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks\laboratorio_page0.png"),
        ("bundle", r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-bundle-prontuari.webp"),
    ]
    for key, p in thumbs:
        im = Image.open(p).convert("RGB")
        im_thumb = im.resize((120, 80), Image.Resampling.LANCZOS)
        out_p = rf"c:\Users\lucag\Desktop\studiofacile\mockups\books\thumb-{key}.webp"
        im_thumb.save(out_p, "WEBP", quality=90)
        print(f"Generated thumb: {out_p}")

if __name__ == "__main__":
    generate_toast_thumbs()
