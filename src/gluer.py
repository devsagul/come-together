import os
import PyPDF2
import io
from fpdf import FPDF
from werkzeug.datastructures import FileStorage
from PIL import Image
from tempfile import TemporaryFile, NamedTemporaryFile


class GlueResult:
    def __init__(self, scale, fmt):
        if scale not in ["up", "down"]:
            raise ValueError("...")
        if fmt not in ["pdf", "jpg", "png"]:
            raise ValueError("...")
        self.scale = scale
        self.fmt = fmt
        self.width = None
        self.tmpfile = TemporaryFile()
        self.files = []

    def __add__(self, f):
        if not isinstance(f, FileStorage):
            raise TypeError("...")
        self.files.append(f)
        if f.mimetype.startswith('image'):
            width = Image.open(f).size[0]
            func = min if self.scale == 'down' else max
            if self.width is not None: self.width = func(self.width, width)
            else: self.width = width
        return self
    
    @property
    def display_name(self):
        return f"glued.{self.fmt}"

    @property
    def mimetype(self):
        types = {
            'pdf' : 'application/pdf',
            'jpg' : 'image/jpg',
            'png' : 'image/png',
        }
        return types[self.fmt]

    @property
    def file(self):
        
        # write all the files
        # converting and scaling them
        if self.fmt == 'pdf':
            image_sources = [self.convert_to_pdf(item) for item in self.files]
        else: image_sources = [self.convert_to_image(item) for item in self.files]
        self._concat(image_sources)
        self.tmpfile.seek(0, os.SEEK_SET)
        return self.tmpfile

    def _concat(self, sources):
        if self.fmt == 'pdf':
            merger = PyPDF2.PdfFileMerger()
            for item in sources:
                reader = PyPDF2.PdfFileReader(item)
                merger.append(item)
            merger.write(self.tmpfile)
            merger.close()
        else:
            ...

    @staticmethod
    def concat_images(images):
        shapes = (item.shape[:2] for item in images)
        hs, ws = zip(*shapes)
        ws = list(ws)
        w = max(ws)
        ratios = (w / item for item in ws)
        h = int(max(hs) * max(ratios) * len(images))
        res = np.zeros((h, w, 3), np.uint8)
        s = 0
        for img in images:
            cur_h, cur_w = img.shape[:2]
            ratio = w / cur_w
            resized = cv2.resize(img, None, fx=ratio, fy=ratio)
            res[s:s+resized.shape[0], :w, :3] = resized
            s += resized.shape[0]
        return res[:s]

    @staticmethod
    def convert_to_pdf(fp):
        if not isinstance(fp, FileStorage):
            raise TypeError('...')
        if (fp.mimetype.endswith('pdf')):
            return fp
        if (fp.mimetype.startswith('image')):
            pdf = FPDF()
            pdf.add_page()    def convert_to_pdf(fp):
        if not isinstance(fp, FileStorage):
            raise TypeError('...')
        if (fp.mimetype.endswith('pdf')):
            return fp
        if (fp.mimetype.startswith('image')):
            pdf = FPDF()
            pdf.add_page()
            image = Image.open(fp)
            tmp = NamedTemporaryFile(suffix='.png')
            w, h = image.size
            image.save(tmp)
            if w / h > 190 / 257:
                pdf.image(tmp.name, w = 190)
            else:
                pdf.image(tmp.name, h = 257)
            return io.BytesIO(pdf.outpu
            image = Image.open(fp)
            tmp = NamedTemporaryFile(suffix='.png')
            w, h = image.size
            image.save(tmp)
            if w / h > 190 / 257:
                pdf.image(tmp.name, w = 190)
            else:
                pdf.image(tmp.name, h = 257)
            return io.BytesIO(pdf.output(dest='S').encode('latin-1'))
        raise ValueError('...')

    @staticmethod
    def convert_to_image(fp):
        if not isinstance(fp, FileStorage):
            raise TypeError('...')
        if (fp.mimetype.startswith('image')):
            return Image.open(fp)
        if (fp.mimetype.endswith('pdf')):
            ...
        raise ValueError('...')


def glue(files, scale, fmt):
    return sum(files, start=GlueResult(scale, fmt))
