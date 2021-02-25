import pyexiv2
import webbrowser
import re

class Img:

    @staticmethod
    def metadata(fileimg):
        P = pyexiv2.Image(fileimg)
        return P.read_exif()

    @staticmethod
    def showImages(response):
        res = response[1]
        path = 'files/template.html'
        pathCache = 'files/cache_index.html';
        _file = open(path,'r')
        html = _file.read()
        _file.close()
        txt = ''
        for r in res:
            txt += '<img src="{}"/>'.format(r)
        htmlContent= re.sub(r'\$1', txt, html)
        _file = open(pathCache,'+w')
        _file.write(htmlContent)
        _file.close()
        webbrowser.open(pathCache)
        ##os.remove(pathCache)

