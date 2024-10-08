from flask import Flask, request, send_file, render_template
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    file = request.files['image']
    img = Image.open(file)

    # 画像のサイズを取得
    img_width, img_height = img.size

    # PDFの設定
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=(img_width, img_height))

    # ImageReaderオブジェクトを作成
    img_reader = ImageReader(img)

    # 画像をPDFに描画
    c.drawImage(img_reader, 0, 0, width=img_width, height=img_height)
    c.showPage()
    c.save()
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name='converted.pdf')

if __name__ == '__main__':
    app.run(debug=True)
