from PIL import Image, ImageDraw, ImageFont
import qrcode
import qrcode.image.styledpil
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from random import randint
from datetime import datetime
import sys


#CONFIG
DATA      = "http://192.168.100.10/callback"
LOGO_PATH = "default.jpg"          # set to None for logoless QR static/baits/qr
DOWNLOADS_DIR = Path("static/downloads")
OUTPUT    = "bait_card.png"


CARD_W      = 900
FONT_BOLD   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG    = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

ACC_COL     = (34, 180, 34)
TXT_COL     = (220, 220, 220)
WARN_COL    = (140, 140, 140)
REF_FILL    = (30, 30, 30)
REF_OUT     = (60, 60, 60)
REF_TXT     = (140, 200, 140)

REF_NUMBER  = f"IT-SEC-{datetime.now().year }-{randint(1000, 9999)}"

# GENERATE CIRCULAR ORG LOGO 
def make_circle_logo(path, size):
    logo = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    logo.putalpha(mask)
    return logo

def generate_bait_card(data=DATA, logo_path=LOGO_PATH, output=OUTPUT):
    # QR with rounded modules
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3,
        image_factory=qrcode.image.styledpil.StyledPilImage
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(
        module_drawer=RoundedModuleDrawer(),
        fill_color="black",
        back_color=(0, 0, 0, 0)   # transparent background
    ).convert("RGBA")

    qr_w, qr_h = qr_img.size

    # Embeding logo if provided
    if logo_path:
        LOGO_SIZE  = int(qr_w * 0.22)
        logo       = make_circle_logo(logo_path, LOGO_SIZE)
        pad        = 12
        circle_bg  = Image.new("RGBA", qr_img.size, (0, 0, 0, 0))
        cd         = ImageDraw.Draw(circle_bg)
        lx         = (qr_w - LOGO_SIZE) // 2
        ly         = (qr_h - LOGO_SIZE) // 2
        cd.ellipse([lx-pad, ly-pad, lx+LOGO_SIZE+pad, ly+LOGO_SIZE+pad], fill=(255,255,255,255))
        qr_img     = Image.alpha_composite(qr_img, circle_bg)
        qr_img.paste(logo, (lx, ly), mask=logo)

    # Resize QR for card
    QR_DISPLAY = 500
    qr_img = qr_img.resize((QR_DISPLAY, QR_DISPLAY), Image.LANCZOS)

    # Round the QR white background corners
    radius = 32
    rounded_mask = Image.new("L", (QR_DISPLAY, QR_DISPLAY), 0)
    ImageDraw.Draw(rounded_mask).rounded_rectangle(
        [0, 0, QR_DISPLAY, QR_DISPLAY], radius=radius, fill=255
    )
    qr_img.putalpha(rounded_mask)

    # Build canvas
    CARD_H = QR_DISPLAY + 300
    card   = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 255))
    bd     = ImageDraw.Draw(card)
    bd.rounded_rectangle([0, 0, CARD_W-1, CARD_H-1], radius=28, outline=(50,50,50), width=2)

    # Paste QR (transparent bg blends onto dark card)
    qr_x = (CARD_W - QR_DISPLAY) // 2
    qr_y = 50
    card.paste(qr_img, (qr_x, qr_y), qr_img)

    # Separator
    sep_y = qr_y + QR_DISPLAY + 28
    bd.line([(CARD_W//2 - 160, sep_y), (CARD_W//2 + 160, sep_y)], fill=ACC_COL, width=2)

    # Fonts
    try:
        f_title = ImageFont.truetype(FONT_BOLD, 44)
        f_sub   = ImageFont.truetype(FONT_REG,  28)
        f_warn  = ImageFont.truetype(FONT_REG,  22)
        f_ref   = ImageFont.truetype(FONT_MONO, 22)
    except Exception:
        f_title = f_sub = f_warn = f_ref = ImageFont.load_default()

    td = ImageDraw.Draw(card)

    def center_text(y, text, font, color):
        bbox = td.textbbox((0, 0), text, font=font)
        tw   = bbox[2] - bbox[0]
        th   = bbox[3] - bbox[1]
        td.text(((CARD_W - tw) // 2, y), text, font=font, fill=color)
        return th

    ty = sep_y + 22
    ty += center_text(ty, "INTERNAL ACCESS ONLY",               f_title, ACC_COL)  + 16
    ty += center_text(ty, "Scan with authorized company device", f_sub,  TXT_COL)  + 14
    ty += center_text(ty, "Restricted : Authorized Personnel Only", f_warn, WARN_COL) + 22

    # Ref pill
    ref_text = f"Ref:  {REF_NUMBER}"
    bbox = td.textbbox((0, 0), ref_text, font=f_ref)
    rw   = bbox[2] - bbox[0]
    rx   = (CARD_W - rw) // 2
    td.rounded_rectangle([rx-18, ty-8, rx+rw+18, ty+30], radius=6, fill=REF_FILL, outline=REF_OUT, width=1)
    td.text((rx, ty), ref_text, font=f_ref, fill=REF_TXT)

    card.save(output, dpi=(300, 300)) # Saving to specified path
    print(f"Saved: {output}  Ref: {REF_NUMBER}")

def pdf_bait(data=DATA, logo_path=LOGO_PATH, token=None): # CALLBACK_URL, ORG_LOGO, TOKEN
	output_path = DOWNLOADS_DIR / f"{token}.png"
	print("OUTPUT: ", output_path)
	
	generate_bait_card(data=DATA, logo_path=logo_path, output=output_path) # CALLBACK_URL, ORG_LOGO, DOWNLOAD_PATH
	
	
if __name__ == "__main__":
	#generate_bait_card()
	pdf_bait()	