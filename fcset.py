import urllib, json
from PyQt4.QtCore import QRectF, Qt
from PyQt4.Qt import QPrinter, QPainter, QFont, QBrush, QColor, QPen, QImage
from PyQt4.QtGui import QApplication


# bkgimg = QImage()
# bkgimg.load("KosyMost.jpg", format = "jpg")
#  
# print bkgimg
# exit()

def background(painter, bkgimg):
    maxx = painter.device().width()
    maxy = painter.device().height()
    
    
    rimg = QRectF(0,0,maxx,maxy*.9)
#     
    painter.fillRect(0,0,maxx, maxy, QBrush(Qt.red, Qt.SolidPattern))
    painter.drawImage(rimg, bkgimg)
    
    wwh = QColor(255,255,255,128)
    
    painter.fillRect(0,2*maxy/10,maxx, 4*maxy/10, QBrush(wwh, Qt.SolidPattern))
    
    u = QRectF(0,9*maxy/10,maxx,maxy/10)
    penHText = QPen(Qt.white);
    painter.setPen(penHText);
    painter.setFont(QFont("Arial", 16, italic=True));
    painter.drawText(u, Qt.AlignLeft | Qt.TextIncludeTrailingSpaces | Qt.AlignVCenter , " ekskursja.pl/flashcards")
    

    

#     painter.drawLine(0,0,maxx,maxy)
#     painter.drawLine(0,maxy,maxx,0)
    
# proxies = {'http': 'http://126.179.0.206:9090' }
headers = {'User-Agent':'MultiFlashcards/fcset.py 0.1'}

url = 'http://ekskursja.pl/wp-content/plugins/flashcards/flashcards.json.php?name=contigo&id=29072'

print url

# response = urllib.urlopen(url, proxies=proxies)
response = urllib.urlopen(url)

data = json.loads(response.read())


app = QApplication([])

printer = QPrinter(QPrinter.HighResolution);
printer.setOutputFormat(QPrinter.PdfFormat);
printer.setPageSize(QPrinter.A6);
printer.setOrientation(QPrinter.Landscape);
printer.setPageMargins (0,0,0,0, QPrinter.Millimeter);
printer.setFullPage(False);

bkgimg = QImage()
if  not bkgimg.load("KosyMost.png", format = "png"):
    print "Not loaded"


printer.setOutputFileName("contigo.pdf");



painter = QPainter(printer)


maxx = painter.device().width()
maxy = painter.device().height()

print "Wymiary: %d,%d" % (maxx, maxy)

q = QRectF(0,2*maxy/10,maxx,2*maxy/10)
a = QRectF(0,4*maxy/10,maxx,2*maxy/10)




penHText = QPen(QColor("#c60b1e"));


for qa in  data['flashcards']:
    print "%s -> %s" % (qa['q'], qa['a'][0])
#     painter.drawText(painter.device().width()/2, 500, qa['q'])
    background(painter, bkgimg)
    painter.setPen(penHText);
    painter.setFont(QFont("Arial", 24, QFont.Bold));
    painter.drawText(q, Qt.AlignCenter, qa['q'])
    printer.newPage()
    
    background(painter, bkgimg)
    painter.setPen(penHText);
    painter.setFont(QFont("Arial", 24, QFont.Bold));
    painter.drawText(q, Qt.AlignCenter | Qt.TextWordWrap, qa['q'])
    painter.drawText(a, Qt.AlignCenter | Qt.TextWordWrap, qa['a'][0])
    printer.newPage()
    
painter.end()

