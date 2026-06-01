from PIL import Image, ImageDraw, ImageFont
import qrcode
import qrcode.image.styledpil
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from random import randint
from datetime import datetime
from pathlib import Path

# CONFIG
DATA          = "http://192.168.100.10/callback"
LOGO_PATH     = "default.jpg"          # set to None for logoless QR
DOWNLOADS_DIR = Path("static/downloads")
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT        = "bait_card.png"

CARD_W    = 900
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

ACC_COL  = (20, 140, 20)      # dark green — visible on white
TXT_COL  = (30, 30, 30)       # near-black
WARN_COL = (80, 80, 80)       # dark grey
REF_FILL = (230, 230, 230)    # light pill bg
REF_OUT  = (180, 180, 180)    # light pill border
REF_TXT  = (20, 100, 20)      # dark green text

REF_NUMBER = f"IT-SEC-{datetime.now().year}-{randint(1000, 9999)}"


# GENERATE CIRCULAR ORG LOGO
def make_circle_logo(path, size):
    logo = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    logo.putalpha(mask)
    return logo


def generate_bait_card(data=DATA, logo_path=LOGO_PATH, output=OUTPUT):
    # QR with rounded modules, transparent background
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
        back_color=(0, 0, 0, 0)
    ).convert("RGBA")

    qr_w, qr_h = qr_img.size

    # Embeding logo in QR if given
    if logo_path:
        LOGO_SIZE = int(qr_w * 0.22)
        logo      = make_circle_logo(logo_path, LOGO_SIZE)
        pad       = 12
        circle_bg = Image.new("RGBA", qr_img.size, (0, 0, 0, 0))
        cd        = ImageDraw.Draw(circle_bg)
        lx        = (qr_w - LOGO_SIZE) // 2
        ly        = (qr_h - LOGO_SIZE) // 2
        cd.ellipse([lx-pad, ly-pad, lx+LOGO_SIZE+pad, ly+LOGO_SIZE+pad], fill=(255, 255, 255, 255))
        qr_img    = Image.alpha_composite(qr_img, circle_bg)
        qr_img.paste(logo, (lx, ly), mask=logo)

    # Resize QR for card
    QR_DISPLAY = 500
    qr_img = qr_img.resize((QR_DISPLAY, QR_DISPLAY), Image.LANCZOS)

    # Round the QR corners
    rounded_mask = Image.new("L", (QR_DISPLAY, QR_DISPLAY), 0)
    ImageDraw.Draw(rounded_mask).rounded_rectangle(
        [0, 0, QR_DISPLAY, QR_DISPLAY], radius=32, fill=255
    )
    qr_img.putalpha(rounded_mask)

    # Fully transparent canvas — no black bg, no border
    CARD_H = QR_DISPLAY + 300
    card   = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))

    # Paste QR centered
    qr_x = (CARD_W - QR_DISPLAY) // 2
    qr_y = 50
    card.paste(qr_img, (qr_x, qr_y), qr_img)

    # Separator
    bd    = ImageDraw.Draw(card)
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

    ty  = sep_y + 22
    ty += center_text(ty, "INTERNAL ACCESS ONLY",                f_title, ACC_COL)  + 16
    ty += center_text(ty, "Scan with authorized company device",  f_sub,  TXT_COL)  + 14
    ty += center_text(ty, "Restricted : Authorized Personnel Only", f_warn, WARN_COL) + 22

    # Ref pill
    ref_text = f"Ref:  {REF_NUMBER}"
    bbox = td.textbbox((0, 0), ref_text, font=f_ref)
    rw   = bbox[2] - bbox[0]
    rx   = (CARD_W - rw) // 2
    td.rounded_rectangle([rx-18, ty-8, rx+rw+18, ty+30], radius=6, fill=REF_FILL, outline=REF_OUT, width=1)
    td.text((rx, ty), ref_text, font=f_ref, fill=REF_TXT)

    card.save(output, dpi=(300, 300))

    # print(f"Saved: {output}  Ref: {REF_NUMBER}")
    return str(Path(output).name)   # filename only Postfix avoids JSON serialization issues


def qr_bait(data=DATA, logo_path=None, token=None):
    if logo_path is None:
        logo_path = "static/baits/qr/default_icon.jpg" # Default Image
    
    output_path = DOWNLOADS_DIR / f"{token}.png"
    
    # print("OUTPUT: ", output_path, 'DATA: ', data, 'TOKEN: ', token)

    return generate_bait_card(data=data, logo_path=logo_path, output=output_path)


if __name__ == "__main__":
    path = qr_bait()
    print("QR saved to:", path)