import fitz
import os
import shutil
from PIL import Image

output_dir = r"c:\Users\lucag\Desktop\studiofacile\mockups\ebooks"
os.makedirs(output_dir, exist_ok=True)

pdf_dir = r"C:\Users\lucag\Desktop\CLAUDE\Infoproductos\Farmacologia\Ebooks Italiano"

# Map of books
books = [
    {
        "id": "emergenza",
        "title": "Farmaci d'Emergenza Illustrati",
        "filename": "Farmaci d'Emergenza Illustrati.pdf",
        "download_cover": r"C:\Users\lucag\Downloads\Farmaci_d_Emergenza_Illustrati_Portada-01.png"
    },
    {
        "id": "antibiotici",
        "title": "Prontuario Illustrato - Antibiotici",
        "filename": "Prontuario Illustrato - Antibiotici.pdf",
        "download_cover": None
    },
    {
        "id": "antinfiammatori",
        "title": "Prontuario Illustrato - Antinfiammatori",
        "filename": "Prontuario Illustrato - Antinfiammatori.pdf",
        "download_cover": r"C:\Users\lucag\Downloads\Prontuario_Illustrato_Antinfiammatori_Portada-01.png"
    },
    {
        "id": "psicofarmaci",
        "title": "Prontuario Illustrato - Psicofarmaci",
        "filename": "Prontuario Illustrato - Psicofarmaci.pdf",
        "download_cover": r"C:\Users\lucag\Downloads\Prontuario_Illustrato_Psicofarmaci_Portada-01.png"
    },
    {
        "id": "laboratorio",
        "title": "Esami di Laboratorio Illustrati",
        "filename": "Esami di Laboratorio Illustrati.pdf",
        "download_cover": None
    }
]

for b in books:
    pdf_path = os.path.join(pdf_dir, b["filename"])
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        page0 = doc[0]
        pix = page0.get_pixmap(dpi=200)
        page0_out = os.path.join(output_dir, f"{b['id']}_page0.png")
        pix.save(page0_out)
        print(f"Rendered page0 for {b['id']} ({pix.width}x{pix.height})")
    
    if b["download_cover"] and os.path.exists(b["download_cover"]):
        dest = os.path.join(output_dir, f"{b['id']}_cover.png")
        shutil.copy(b["download_cover"], dest)
        print(f"Copied user cover for {b['id']} -> {dest}")

print("Done extracting covers.")
