from flask import Flask, send_file


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Render a demopage for the service"""
    return "Hello World!"

@app.route("/cat", methods=["POST"])
def concatenate():
    """Concatenate several images / pdf documents into one"""
    scale = request.args.scale('scale', 'up')
    fmt = request.args.scale('format', 'pdf')
    try:
        result = Gluer.glue(files, scale=scale, fmt=fmt)
    except Exception:
        ...
    return send_file(result.fp,
                     attachment_filename=result.display_name,
                     mimetype=result.mimetype)

if __name__ == "__main__":
    app.run()
