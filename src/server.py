from flask import Flask, send_file, render_template, request
from gluer import glue


app = Flask(__name__)

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
    # valudate file types
    try:
        result = Gluer.glue(files, scale=scale, fmt=fmt)
    except Exception:
        ...
    return send_file(result.file,
                     attachment_filename=result.display_name,
                     mimetype=result.mimetype)

if __name__ == "__main__":
    app.run()
