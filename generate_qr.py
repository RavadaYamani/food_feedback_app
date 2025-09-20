import qrcode

# Customer feedback page URL
feedback_url = "https://myfoodfeedback.railway.app/feedback"

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)
qr.add_data(feedback_url)
qr.make(fit=True)

img = qr.make_image(fill='black', back_color='white')

# Save QR image inside static folder
img.save("static/feedback_qr.png")
print("QR Code generated at static/feedback_qr.png")
