from flask import Flask, send_file, render_template, request
from gluer import glue


ALLOWED_MIMETYPES = [
    'application/pdf',
    'image/jpeg',
    'image/png',
]

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=["GET"])
def home():
    """Render a demopage with form for the service"""
    return render_template('index.html', name="Come Together")

@app.route("/cat", methods=["POST"])
def concatenate():
    """Concatenate several images / pdf documents into one"""
    scale = request.values.get('scale', 'up')
    fmt = request.values.get('format', 'pdf')
    files = request.files.getlist("file[]")
    for f in files:
        if f.mimetype not in ALLOWED_MIMETYPES:
            return f"Недопустимый тип файла: {f.mimetype}", 400
    if not files:
        return "Необходимо предоставить как миниум один файл", 400
    try:
        result = glue(files, scale=scale, fmt=fmt)
    except (ValueError, TypeError) as e:
        return str(e), 400
    return send_file(result.file,
                     attachment_filename=result.display_name,
                     mimetype=result.mimetype)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
