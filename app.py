from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        file = request.files['file']
        if file.filename == '':
            return 'no file selected', 400
        if file:
            input_image = Image.open(file)
            output_image = remove(input_image,post_process_mask=True)
            byte_io = BytesIO()
            output_image.save(byte_io, 'PNG')
            byte_io.seek(0)
            return send_file(byte_io, mimetype='image/png', 
                             as_attachment=True, download_name='_rmbg.png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5100)

