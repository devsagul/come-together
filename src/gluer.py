import os
import PyPDF2
import io
import math
import pdf2image
from fpdf import FPDF
from werkzeug.datastructures import FileStorage
from PIL import Image
from tempfile import NamedTemporaryFile


class GlueResult:
    def __init__(self, scale, fmt):
        if scale not in ["up", "down"]:
            raise ValueError('scale has to be up or down')
        if fmt not in ["pdf", "jpg", "png"]:
            raise ValueError('fmt has to be one of pdf, jpg, png')
        self.scale = scale
        self.fmt = fmt
        self.width = None
        self.tmpfile = NamedTemporaryFile(suffix="."+fmt)
        self.files = []

    def __add__(self, f):
        if not isinstance(f, FileStorage):
            raise TypeError('f has to be an instance of FileStorage')
        self.files.append(f)
        if f.mimetype.startswith('image'):
            width = Image.open(f).size[0]
        else: width = 2200 # TODO remove hardcoded value 
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
        if self.fmt == 'pdf':
            image_sources = [self.convert_to_pdf(item) for item in self.files]
        else: 
            image_sources =[]
            for item in self.files:
                image_sources += self.convert_to_images(item)
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
            dst = Image.new('RGB', (self.width, sum([x.height for x in sources])))
            h = 0
            for image in sources:
                dst.paste(image, (0, h))
                h += image.height
            dst.save(self.tmpfile)

    @staticmethod
    def convert_to_pdf(fp):
        if not isinstance(fp, FileStorage):
            raise TypeError('fp has to be an instance of FileStorage')
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
            return io.BytesIO(pdf.output(dest='S').encode('latin-1'))
        raise ValueError(f'Incopatible mimetype: {fp.mimetype}')

    def convert_to_images(self, fp):
        if not isinstance(fp, FileStorage):
            raise TypeError('fp has to be an instance of FileStorage')
        if (fp.mimetype.startswith('image')):
            image = Image.open(fp)
            return [scale_image(image, self.width)]
        if (fp.mimetype.endswith('pdf')):
            images = pdf2image.convert_from_bytes(fp.read(), dpi=300)
            return [scale_image(image, self.width) for image in images]

        raise ValueError(f'Incopatible mimetype: {fp.mimetype}')


def scale_image(image, width):
    scale = width / image.width
    i = image.resize((math.ceil(scale * image.width),
                        math.ceil(scale * image.height)),
                        Image.ANTIALIAS)
    return i

def glue(files, scale, fmt):
    return sum(files, start=GlueResult(scale, fmt))
