import os
import io
from tempfile import Tempfile


class GlueResult:
    def __init__(self, scale, fmt):
        if scale not in ["up", "down"]:
            raise ValueError("...")
        if fmt not in ["pdf", "jpg", "png"]:
            raise ValueError("...")
        self.scale = scale
        self.fmt = fmt
        self.width = 0
        self.tmpfile = Tempfile()
        self.files = []

    def __add__(self, f):
        if not isinstance(f, io.IOBase):
            raise TypeError("...")
        self.files.append(f)
        # if it is an image, update dimensins
        # update dimensions
    
    @property
    def display_name(self):
        return f"glued.{self.fmt}"

    @property
    def memtype(self):
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
        self.tmpfile.seek(0, os.SEEK_SET)
        return self.tmpfile


def glue(files, scale, fmt):
    result = GluerResult(scale, fmt)
    return sum([result] + files)
