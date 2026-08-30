import fitz
import os
from PIL import Image
import io

sample_dir = r"c:\Users\lucag\Desktop\studiofacile\amostras\ebooks"
os.makedirs(sample_dir, exist_ok=True)

pdf_dir = r"C:\Users\lucag\Desktop\CLAUDE\Infoproductos\Farmacologia\Ebooks Italiano"

book_samples = {
    "emergenza": ("Farmaci d'Emergenza Illustrati.pdf", [4, 10, 22]),
    "antibiotici": ("Prontuario Illustrato - Antibiotici.pdf", [4, 12, 28]),
    "antinfiammatori": ("Prontuario Illustrato - Antinfiammatori.pdf", [4, 10, 18]),
    "psicofarmaci": ("Prontuario Illustrato - Psicofarmaci.pdf", [4, 15, 30]),
    "laboratorio": ("Esami di Laboratorio Illustrati.pdf", [4, 16, 32]),
}

for book_id, (filename, pages) in book_samples.items():
    pdf_path = os.path.join(pdf_dir, filename)
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        for idx, pno in enumerate(pages):
            if pno < len(doc):
                page = doc[pno]
                pix = page.get_pixmap(dpi=150)
                png_bytes = pix.tobytes("png")
                im = Image.open(io.BytesIO(png_bytes))
                out_path = os.path.join(sample_dir, f"{book_id}_sample_{idx+1}.webp")
                im.save(out_path, "WEBP", quality=88)
                print(f"Saved sample {out_path} ({im.size[0]}x{im.size[1]})")

print("Sample extraction complete.")
