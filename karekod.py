import qrcode
from PIL import Image

class KareKod:
    """
    veri icinde bulunan bilgi icin karekod uretir
    """
    def __init__(self, veri):
        self.img = qrcode.make(veri)

    def kaydet(self, dosyaAdi):
        self.img.save(dosyaAdi)

    def buyut(self, x, y):
        self.img = self.img.resize((x,y))

class KareKodlar:
    """
    Buyuk veri parcasi icin herbiri parcaBoyu buyuklugunde 
    kucuk karekodlar uretir. karekod resimlerinin boyutlarini da
    zoom ile boler.
    """
    def __init__(self, veri, parcaBoyu, zoom):
        self.resim = 0
        self.zoom = zoom
        veriboyu = len(veri)
        self.kodlar = {}
        if veriboyu < parcaBoyu:
            self.parca = 1
        elif veriboyu % parcaBoyu == 0:
            self.parca = (len(veri) / parcaBoyu)
        else:
            self.parca = (len(veri) / parcaBoyu) + 1

        for i in range(self.parca):
            self.kodlar[i] = KareKod(veri[(i * parcaBoyu):(i + 1) * parcaBoyu])
            xx,yy = self.kodlar[i].img.size
            self.kodlar[i].buyut(xx / zoom, yy/zoom)
            #self.kodlar[i].kaydet("%d.png" % i)

    def resimYap(self, (x,y)):
        """
        x,y buyuklugunde bir resim icine karekodlari yerlestirir.

        """
        self.resim = Image.new("1",(x,y),1)
        self.resim.save("bak.png")
        px, py = self.kodlar[0].img.size
        if x < px:
            return None
        if y < py:
            return None
        maxparca = (x / px) * (y / py)
        if maxparca < len(self.kodlar):
            return None
        rx = 0
        ry = 0
        for i, qr in self.kodlar.items():
            if (rx * px) + px >= x:
                rx = 0
                ry += 1
            self.resim.paste(qr.img, (rx * px, ry * py))
            rx += 1

if __name__ == "__main__":
    veri = open("/bin/bash","rb").read(4512)
    k = KareKodlar(veri,128,4)
    k.resimYap((1000,1000))
    k.resim.save("buyukresim.png")
