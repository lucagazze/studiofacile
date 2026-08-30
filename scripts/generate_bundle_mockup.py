import os
from PIL import Image, ImageDraw, ImageFilter

def create_bundle_mockup():
    width = 1200
    height = 700
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Load individual mockups
    emergenza = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-emergenza.png")
    antibiotici = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antibiotici.png")
    antinfiammatori = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-antinfiammatori.png")
    psicofarmaci = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-psicofarmaci.png")
    laboratorio = Image.open(r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-laboratorio.png")
    
    # Composite them in an overlapping fan layout
    # Resize slightly
    scale = 0.65
    def res(im, s=scale):
        return im.resize((int(im.width * s), int(im.height * s)), Image.Resampling.LANCZOS)
    
    m_anti = res(antinfiammatori)
    m_psico = res(psicofarmaci)
    m_biot = res(antibiotici)
    m_emerg = res(emergenza, 0.72)
    m_lab = res(laboratorio, 0.62)
    
    # Positions
    canvas.paste(m_anti, (60, 110), m_anti)
    canvas.paste(m_psico, (240, 90), m_psico)
    canvas.paste(m_biot, (440, 80), m_biot)
    canvas.paste(m_lab, (620, 170), m_lab)
    canvas.paste(m_emerg, (310, 40), m_emerg)
    
    out_webp = r"c:\Users\lucag\Desktop\studiofacile\mockups\books\mockup-bundle-prontuari.webp"
    canvas.save(out_webp, "WEBP", quality=92)
    print("Bundle mockup created:", out_webp)

if __name__ == "__main__":
    create_bundle_mockup()
