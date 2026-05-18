from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import qrcode

from random import randint
from datetime import datetime

# CONFIG 
data       = "http://192.168.1.138/qrcode.png"   # your callback URL
logo_path  = "logo.png"                           # company logo
output     = "bait_card_final.png"

CARD_W       = 900
BG_COLOR     = (0, 0, 0, 0)                       # ✅ transparent
TEXT_COLOR   = (30, 30, 30)                        # ✅ dark — readable on white Word bg
ACCENT_COLOR = (20, 140, 20)                       # ✅ darker green — visible on white
BORDER_COLOR = (50, 50, 50)
FONT_BOLD    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO    = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
# Windows fallback: "C:/Windows/Fonts/arialbd.ttf" etc.

# Randomizing Reference Number
REF_NUMBER = f"IT-SEC-{datetime.now().year}-{randint(1000, 9999)}"    # ✅ 4-digit always


def generate_bait_card(data, logo_path, output):

    # GENERATE QR
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_w, qr_h = qr_img.size

    # EMBEDDING LOGO IN CENTER
    logo = Image.open(logo_path).convert("RGBA")

    logo_size = int(qr_w * 0.27)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    lx = (qr_w - logo_size) // 2
    ly = (qr_h - logo_size) // 2

    # White circle behind logo
    circle_bg = Image.new("RGBA", qr_img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(circle_bg)
    pad = 14
    cd.ellipse(
        [lx - pad, ly - pad, lx + logo_size + pad, ly + logo_size + pad],
        fill=(255, 255, 255, 255)
    )
    qr_img = Image.alpha_composite(qr_img, circle_bg)
    qr_img.paste(logo, (lx, ly), mask=logo)

    # Sharpen QR modules
    qr_rgb = qr_img.convert("RGB")
    qr_rgb = ImageEnhance.Sharpness(qr_rgb).enhance(2.8)
    qr_rgb = ImageEnhance.Contrast(qr_rgb).enhance(1.4)
    qr_img = qr_rgb.convert("RGBA")

    # RESIZE QR FOR CARD
    QR_DISPLAY = 560
    qr_img = qr_img.resize((QR_DISPLAY, QR_DISPLAY), Image.LANCZOS)

    # BUILD CARD CANVAS — fully transparent  ✅
    CARD_H = QR_DISPLAY + 320
    card = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))          # ✅ transparent

    # ✅ No rounded_rectangle border — looks wrong floating on transparent bg

    bd = ImageDraw.Draw(card)

    # PASTE QR CENTERED
    qr_x = (CARD_W - QR_DISPLAY) // 2
    qr_y = 50
    card.paste(qr_img, (qr_x, qr_y), qr_img)

    # Green separator line
    sep_y = qr_y + QR_DISPLAY + 28
    bd.line([(CARD_W//2 - 160, sep_y), (CARD_W//2 + 160, sep_y)], fill=ACCENT_COLOR, width=2)

    # TEXT
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
        tw = bbox[2] - bbox[0]
        td.text(((CARD_W - tw) // 2, y), text, font=font, fill=color)
        return bbox[3] - bbox[1]

    ty = sep_y + 22
    ty += center_text(ty, "INTERNAL ACCESS ONLY", f_title, ACCENT_COLOR) + 16
    ty += center_text(ty, "Scan with authorized company device", f_sub, TEXT_COLOR) + 14
    ty += center_text(ty, "Restricted : Authorized Personnel Only", f_warn, (80, 80, 80)) + 18  # ✅ darker

    # Reference pill
    ref_text = f"Ref:  {REF_NUMBER}"
    bbox = td.textbbox((0, 0), ref_text, font=f_ref)
    rw = bbox[2] - bbox[0]
    rx = (CARD_W - rw) // 2
    td.rounded_rectangle(
        [rx - 18, ty - 8, rx + rw + 18, ty + 30],
        radius=6, fill=(230, 230, 230), outline=(180, 180, 180), width=1  # ✅ light pill for white bg
    )
    td.text((rx, ty), ref_text, font=f_ref, fill=(20, 100, 20))           # ✅ dark green text

    # ✅ Save as RGBA PNG — preserves transparency (no .convert("RGB"))
    card.save(output, dpi=(300, 300))
    print(f"Saved: {output}  ({CARD_W}x{CARD_H}px)")


generate_bait_card(data=data, logo_path=logo_path, output=output)