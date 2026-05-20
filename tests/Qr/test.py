import qrcode
from PIL import Image

# 1. Load the logo image
logo_path = 'conf.jpg'  # Replace with your image file path
logo = Image.open(logo_path)

# 2. Set the base width for the logo
basewidth = 100
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

# 3. Create the QR code with high error correction
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

# 4. Add data to the QR code
data = 'https://example.com'
QRcode.add_data(data)
QRcode.make()

# 5. Create the QR image and convert to RGB
QRimg = QRcode.make_image(
    fill_color="black", back_color="white"
).convert('RGB')

# 6. Calculate position to center the logo
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)

# 7. Paste the logo onto the QR code
QRimg.paste(logo, pos)

# 8. Save the final image
QRimg.save('qr_with_logo.png')
print('QR code with logo generated successfully!')
