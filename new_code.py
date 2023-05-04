import pyqrcode
import subprocess
import base64
import os
import sys
import qrcode
import svgwrite
import io
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderSVG
import xml.etree.ElementTree as ET

def create_laisee_qrcode(lnurl: str, idnumber: str, expires: str, sats: str, template_file: str):

    try:
        output_svg = 'images/output_' + idnumber + '.svg'
        output_png = 'images/output_' + idnumber + '.png'

        # Generate the QR code
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(lnurl)
        qr.make(fit=True)

        # Create an SVG container
        dwg = svgwrite.Drawing(output_svg, profile='full', size=('1500px', '1500px'))

        # Load the background image and add it as an SVG element
        template_drawing = svg2rlg(template_file)
        template_svg = renderSVG.drawToString(template_drawing)
        template_element = ET.fromstring(template_svg)
        bg_element = svgwrite.container.Group()
        bg_element.add(svgwrite.container.SVG(element=template_element))
        dwg.add(bg_element)

        # Draw the QR code onto the SVG canvas
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_width, qr_height = qr_image.size
        qr_canvas = dwg.add(dwg.g())

        # Add annotations to the SVG canvas
        qr_canvas.add(dwg.text(idnumber, insert=(105.30424, 337.77887), font_size="50"))
        qr_canvas.add(dwg.text(expires, insert=(105.30424, 337.77887 + 50), font_size="50"))
        qr_canvas.add(dwg.text(sats, insert=(105.30424, 337.77887 + 100), font_size="50"))

        for row in range(qr_width):
            for col in range(qr_height):
                if qr_image.getpixel((row, col)):
                    x = 105.30424 + row
                    y = 337.77887 + col
                    qr_canvas.add(dwg.rect(insert=(x, y), size=(1, 1), fill='black', opacity=1.0))

        # Save the SVG image
        dwg.save()

        # Convert SVG to PNG
        subprocess.run(['rsvg-convert', output_svg, '-o', output_png, '-w' , '600'], cwd=".")
        return output_png
    except Exception as e:
        return str(e)


if __name__ == "__main__":

    template_file = 'templates/rabbit_crop_final.svg'
    lnurl = "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AKXUATJD3CZ7CTSDYHHVVF0D3H82UNV9UUNWVCE4EM6P"
    idnumber = "f7bsdfs"
    expires = "2023-05-15"
    sats = "2500"

    output_png = create_laisee_qrcode(lnurl, idnumber, expires, sats, template_file)

    print(f'Output PNG created: {output_png}')

    # open the output file using the default program for its file type
    if sys.platform.startswith('darwin'):  # macOS
        subprocess.run(['open', output_png])
    elif os.name == 'nt':  # Windows
        os.startfile(output_png)
    elif os.name == 'posix':  # Linux/Unix
        subprocess.run(['xdg-open', output_png])