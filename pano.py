# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys, logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)    

def init_printer(printer):
    printer.setOutputFormat(QPrinter.PdfFormat);
#     printer.setPageSize(QPrinter.A6);
    printer.setOrientation(QPrinter.Landscape);
    printer.setPageMargins (0,0,0,0, QPrinter.Millimeter);
    printer.setFullPage(False);
    
    logger.info("Printer: %s" % printer)    

def main():  
    app = QApplication(sys.argv)           
    reader = QImageReader("O is for Outlaw.jpg")
    image = QImage()
    
#     url = QUrl("http://http://ekskursja.pl/wp-content/uploads/2016/04/20160316_163843-2.jpg");
        
#     x = reader.size().width()
#     y = reader.size().height()/2
#     
#     reader.setClipRect(QRect(0,0,x,y))    
    
#     printer = QPrinter(QPrinter.HighResolution);
#     init_printer(printer)
#     printer.setOutputFileName("output/pano.pdf");

    
    
    
    image.load("img/talty01.jpg")
    w = image.size().width()
    h = image.size().height()
    
    logger.info("Size: %d,%d" % (w,h))
    
    
    imglogo = QImage('img/ekskursja-profil.png')
    
    r = 9.0/16.0
    w1 = h/r
    
    d = w - w1
    
    dd = d/200.0

    target = QImage(w1,h,QImage.Format_RGB32);
    painter = QPainter(target)

    logger.info("Inne: %d,%d,%d" % (w1,d,dd))
    
    scrw = w1
    scrh = h

    penHText = QPen(Qt.white);
    painter.setPen(penHText);
    painter.setFont(QFont("Arial", 24, QFont.Bold, italic=True));
        
    wwh = QColor(0,0,0,128)     

    for i in range(200):
        image2 = image.copy(QRect(i*dd,0,w1,h))    

        painter.drawImage(QRect(0,0,scrw, scrh), image2)
        painter.drawImage(QRect(scrw - .125*scrh,.025*scrh, .1*scrh, .1*scrh), imglogo)
        painter.fillRect(0, .9*scrh, scrw,.1*scrh, QBrush(wwh, Qt.SolidPattern))
        painter.drawText(0, .9*scrh, scrw,.1*scrh, Qt.AlignLeft | Qt.TextIncludeTrailingSpaces | Qt.AlignVCenter , \
                         QString.fromUtf8("  jez. Tałty"))

        target.save('movie/mv'+ str(i).zfill(3) + '.png' )
        target.save('movie/mv'+ str(400-i-1).zfill(3) + '.png' )
        
    painter.end()
    
if __name__ == '__main__':
    main()