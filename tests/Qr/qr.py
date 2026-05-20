from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import qrcode

from random import randint
from datetime import datetime

from flask import current_app
# CONFIG 

# callback_url = current_app.config['CALLBACK_URL']

data       = "http://192.168.100.10/qrcode.png"   # your callback URL
logo_path  = "logo.png"                           # company logo

CARD_W       = 900
BG_COLOR     = (0, 0, 0, 0)                       # transparent
TEXT_COLOR   = (30, 30, 30)                        # dark — readable on white Word bg
ACCENT_COLOR = (20, 140, 20)                       # darker green — visible on white
BORDER_COLOR = (50, 50, 50)
FONT_BOLD    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO    = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
# Windows fallback: "C:/Windows/Fonts/arialbd.ttf" etc.

# Randomizing Reference Number — shared across both versions
REF_NUMBER = f"IT-SEC-{datetime.now().year-1}-{randint(1000, 9999)}" # 1 YEAR AGO


def generate_bait_card(data, logo_path, output, version="standalone"):

    #ge
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_w, qr_h = qr_img.size

    #EMBED LOGO IN CENTER
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
        fill=(255, 255, 255, 255) # CHANGE SHAPES OF CIRCLE BEHIND LOGO
    )
    qr_img = Image.alpha_composite(qr_img, circle_bg)
    qr_img.paste(logo, (lx, ly), mask=logo)

    # Sharpen QR modules
    qr_rgb = qr_img.convert("RGB")
    qr_rgb = ImageEnhance.Sharpness(qr_rgb).enhance(2.8)
    qr_rgb = ImageEnhance.Contrast(qr_rgb).enhance(1.4)
    qr_img = qr_rgb.convert("RGBA")

    # RESIZE QR FOR CARD
    QR_DISPLAY = 500
    qr_img = qr_img.resize((QR_DISPLAY, QR_DISPLAY), Image.LANCZOS)

    # ── BUILD CANVAS ──────────────────────────────────────────────────────────
    if version == "standalone":
        CARD_H  = QR_DISPLAY + 320
        bg      = (0, 0, 0, 0)#(15, 15, 15, 255)         # dark background
        txt_col = (220, 220, 220)            # light text
        acc_col = (34, 180, 34)             # bright green
        warn_col= (160, 160, 160)
        ref_fill= (30, 30, 30)
        ref_out = (60, 60, 60)
        ref_txt = (140, 200, 140)
    else:  # document
        CARD_H  = QR_DISPLAY + 120          # compact — no big text block
        bg      = (0, 0, 0, 0)              # transparent
        txt_col = TEXT_COLOR
        acc_col = ACCENT_COLOR
        warn_col= (80, 80, 80)
        ref_fill= (230, 230, 230)
        ref_out = (180, 180, 180)
        ref_txt = (20, 100, 20)

    card = Image.new("RGBA", (CARD_W, CARD_H), bg)
    bd   = ImageDraw.Draw(card)

    if version == "standalone":
        bd.rounded_rectangle(
            [0, 0, CARD_W-1, CARD_H-1], radius=28, outline=BORDER_COLOR, width=3
        )

    # ── PASTE QR CENTERED ─────────────────────────────────────────────────────
    qr_x = (CARD_W - QR_DISPLAY) // 2
    qr_y = 50
    card.paste(qr_img, (qr_x, qr_y), qr_img)

    # Green separator line
    sep_y = qr_y + QR_DISPLAY + 28
    bd.line([(CARD_W//2 - 160, sep_y), (CARD_W//2 + 160, sep_y)], fill=acc_col, width=2)

    #FONTS
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
        td.text(((CARD_W - tw) // 2, y), text, font=font, fill=color)
        return bbox[3] - bbox[1]

    ty = sep_y + 22

    # ── TEXT BLOCK (standalone only) ──────────────────────────────────────────
    if version == "standalone":
        ty += center_text(ty, "INTERNAL ACCESS ONLY",              f_title, acc_col)  + 16
        ty += center_text(ty, "Scan with authorized company device", f_sub,  txt_col) + 14
        ty += center_text(ty, "Restricted : Authorized Personnel Only", f_warn, warn_col) + 18

    # ── REF PILL (both versions) ──────────────────────────────────────────────
    ref_text = f"Ref:  {REF_NUMBER}"
    bbox = td.textbbox((0, 0), ref_text, font=f_ref)
    rw   = bbox[2] - bbox[0]
    rx   = (CARD_W - rw) // 2
    td.rounded_rectangle(
        [rx - 18, ty - 8, rx + rw + 18, ty + 30],
        radius=6, fill=ref_fill, outline=ref_out, width=1
    )
    td.text((rx, ty), ref_text, font=f_ref, fill=ref_txt)

    # ── SAVE ──────────────────────────────────────────────────────────────────
    card.save(output, dpi=(300, 300))
    print(f"[{version:>10}] Saved: {output}  ({CARD_W}x{CARD_H}px)  Ref: {REF_NUMBER}")


# ── GENERATE BOTH ─────────────────────────────────────────────────────────────
generate_bait_card(data=data, logo_path='conf.jpg', output="bait_standalone.png", version="standalone")
#generate_bait_card(data=data, logo_path=logo_path, output="bait_document.png",   version="document")