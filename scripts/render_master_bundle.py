import os
from PIL import Image, ImageDraw, ImageFilter

def render_master_bundle():
    cw, ch = 1200, 720
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    
    # Load individual PNGs
    emerg = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-emergenza.png")
    antib = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antibiotici.png")
    antinf = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antinfiammatori.png")
    psico = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-psicofarmaci.png")
    lab = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-laboratorio.png")
    
    def scale_im(im, factor):
        return im.resize((int(im.width * factor), int(im.height * factor)), Image.Resampling.LANCZOS)
    
    # Scale layers
    b_antinf = scale_im(antinf, 0.58)
    b_psico = scale_im(psico, 0.64)
    b_antib = scale_im(antib, 0.64)
    b_emerg = scale_im(emerg, 0.72)
    b_lab = scale_im(lab, 0.60)
    
    # Add subtle individual drop shadow before pasting each
    def paste_with_shadow(layer, pos, shadow_strength=0.35, blur_r=14):
        # Create shadow mask
        alpha = layer.split()[-1]
        shadow = Image.new("RGBA", layer.size, (15, 23, 42, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.bitmap((0, 0), alpha, fill=(15, 23, 42, int(255 * shadow_strength)))
        shadow_blur = shadow.filter(ImageFilter.GaussianBlur(blur_r))
        
        # Paste shadow offset
        canvas.paste(shadow_blur, (pos[0] + 8, pos[1] + 12), shadow_blur)
        canvas.paste(layer, pos, layer)

    # 1. Background layer: Antinfiammatori (left) and Antibiotici (right)
    paste_with_shadow(b_antinf, (60, 130), 0.3, 16)
    paste_with_shadow(b_antib, (690, 110), 0.35, 16)
    
    # 2. Mid layer: Psicofarmaci (mid left)
    paste_with_shadow(b_psico, (220, 80), 0.4, 18)
    
    # 3. Main center: Emergenza
    paste_with_shadow(b_emerg, (370, 30), 0.5, 22)
    
    # 4. Foreground: Laboratorio (landscape book resting in front right)
    paste_with_shadow(b_lab, (610, 240), 0.45, 20)
    
    out_webp = r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-bundle-prontuari.webp"
    canvas.save(out_webp, "WEBP", quality=95)
    print("Master bundle created successfully:", out_webp)

if __name__ == "__main__":
    render_master_bundle()
