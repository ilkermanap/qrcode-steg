from PIL import Image
from karekod import KareKodlar
import math, sys

class Birlestir:
    def __init__(self, resim, veri, parcaBoyu):
        self.resim = Image.open(resim)
        self.veri = veri
        self.qr = KareKodlar(veri, parcaBoyu, 10)
        x,y = self.resim.size
        self.qr.resimYap(x,y)

        
    def birlestir(self):
        x, y = self.resim.size
        for j in range(y):
            for i in range(x):
                r,g,b = self.resim.getpixel((i,j))
                p = self.qr.resim.getpixel((i,j))
                if p == 0:
                    r = r | 1
                    g = g | 1
                    b = b | 1
                elif p == 255:
                    r = r & 254
                    g = g & 254
                    b = b & 254
                self.resim.putpixel((i,j),(r,g,b))

    def ayir(self, fname):
        x, y = self.resim.size
        n = Image.new("1",self.resim.size, color = 0)
        for j in range(y):
            for i in range(x):
                r,g,b = self.resim.getpixel((i,j))
                p = (r & 1) & (g & 1) & (b & 1)
                if p == 1:
                    n.putpixel((i,j), 255 )
                else:
                    n.putpixel((i,j), 0   )

        n.save(fname)


a = Birlestir(sys.argv[1], open(sys.argv[1],"rb").read(4095),512 )
a.birlestir()
a.resim.save("karekod-eklenmis.png")
a.qr.resim.save("eklenen-karekod.png")
a.ayir("ayirilmis-karekod.png")
