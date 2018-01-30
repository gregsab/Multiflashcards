# -*- coding: utf-8 -*-

'''
Created on 31 paź 2016

@author: sabakgrz
'''

from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys, logging, glob, os, urllib2, json, random

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)    


class FlashCard():
    def __init__(self, words, langs = None, img = None):
        self.words = words
        self.langs = langs
        self.img = img
        pass
    
    def __str__(self):
        return "[%s]" % (self.words,)
    
    
class FlashCardSet():
    LEVEL_COLOR_EASY = "#1e73be"
    LEVEL_COLOR_MEDIUM = "#dd9933"
    LEVEL_COLOR_HARD = "#dd3333"

    def __init__(self, title = "Fiszki", level = 'A1', img = None):
        self.title = title
        self.cards = []
        self.img = img
        self.level = level
        self.from_url = False
        self.size = QSize(480,640)
        
        if (img != None):
            self.bkgimg = QImage()
            if not self.bkgimg.load(img):
                logger.warning("Background image not loaded: %s" % img)
            else:        
                logger.info("Background image loaded: %s" % img)
    
    def recalc_size(self, perc=10, width=720):
        w = self.bkgimg.width()
        h = self.bkgimg.height()
        
        h1 = h * (1+perc/100.0)
        
        r = 1.0*width/w
        h2 = h1 * r
        
        self.size = QSize(width,h2)
        
        logger.info("Output size [%d, %d] to [%d, %d]" % (w, h, width, h2))
        
    
    def __str__(self):
        return self.title
            
    def addCard(self, card):
        self.cards.append(card)
        logger.info("Card %s added" % card)
        
    def getFromEkskursja(self, name):
        self.from_url = True
        base_url = 'http://ekskursja.pl/wp-content/plugins/flashcards/flashcards.json.php?name='
        
        fc_url = base_url + name
        
        logger.info("GET %s" % fc_url)
        conn = urllib2.urlopen(fc_url)
        fcjson = conn.read()
        c = json.loads(fcjson)
        fcset = c['flashcards']
        
        self.level = c['properties']['level']
        self.img = c['properties']['image']
        self.title = c['properties']['title']
        
        for fc in fcset:
            self.addCard( FlashCard((fc['q'], fc['a'][0]), \
                        (c['properties']['language'],c['properties']['language']), \
                         c['properties']['image'])) 
            
        conn = urllib2.urlopen(c['properties']['image'])
        data = conn.read()
       
        self.bkgimg = QImage()
        if  not self.bkgimg.loadFromData(data):
            logger.warning("Background image NOT loaded: %s" % c['properties']['image'])
        else:
            logger.info("Background image loaded: %s" % c['properties']['image'])
            self.recalc_size()
            
            
        logger.info("Flashcard Set [%s] loaded" % self.title)
        
    def saveAsImages(self, size, pathname):
        i = 1
        
        files = glob.glob(pathname + '/*.png')
        
        logger.info("Removing %d .png files from %s" % (len(files), pathname))
        
        for filename in files:
            os.unlink(filename)
            
        
        title_image = self.getTitlePageAsImage()
        fname = pathname+'/img'+ str(i).zfill(3) + '.png'
        logger.info("Saving title page: %s" % fname)
        title_image.save(fname)
        
        i = i+1
        
        for n in range(0, len(self.cards)):
            for k in range(0, len(self.cards[n].words)):
                img = self.getAsImageN(n, k)
                fname = pathname+'/img'+ str(i).zfill(3) + '.png'
                logger.info("Saving flashcard page: %s" % fname)
                img.save(pathname+'/img'+ str(i).zfill(3) + '.png' )
                i = i+1

        fname = pathname+'/img'+ str(i).zfill(3) + '.png'
        logger.info("Saving title page: %s" % fname)
        title_image.save(fname)

    def saveAsImagesQA(self, pathname, lst):
        i = 1
        
        files = glob.glob(pathname + '/*.png')
        
        logger.info("Removing %d .png files from %s" % (len(files), pathname))
        
        for filename in files:
            os.unlink(filename)
            
        
        title_image = self.getTitlePageAsImage()
        fname = pathname+'/img'+ str(i).zfill(3) + '.png'
        logger.info("Saving title page: %s" % fname)
        title_image.save(fname)
        
        i = i+1
        
        for n in lst:
            img = self.getAsImageNQ(n)
            fname = pathname+'/img'+ str(i).zfill(3) + '.png'
            logger.info("Saving flashcard page: %s" % fname)
            img.save(pathname+'/img'+ str(i).zfill(3) + '.png' )
            i = i+1
            img = self.getAsImageNA(n)
            fname = pathname+'/img'+ str(i).zfill(3) + '.png'
            logger.info("Saving flashcard page: %s" % fname)
            img.save(pathname+'/img'+ str(i).zfill(3) + '.png' )
            i = i+1

        fname = pathname+'/img'+ str(i).zfill(3) + '.png'
        logger.info("Saving title page: %s" % fname)
        title_image.save(fname)

        
    def getTitlePageAsImage(self):
        target = QImage(self.size, QImage.Format_RGB32);
        painter = QPainter(target)
        cslb = CardSetLayoutBasic(self, painter)
        
        painter.fillRect(cslb.canvas, QBrush(cslb.level_color, Qt.SolidPattern))
        
        cslb.footer()
        cslb.background(self.bkgimg)
            
        cslb.title(self.title)
        
        cslb.logo()
        return target

        
    def getAsImageN(self, n, k):
        target = QImage(self.size, QImage.Format_RGB32);
        painter = QPainter(target)
        cslb = CardSetLayoutBasic(self, painter)
        
        painter.fillRect(cslb.canvas, QBrush(cslb.level_color, Qt.SolidPattern))
        
        cslb.footer()
        cslb.flag(self.cards[n].langs[k])

        
#         if (self.cards[n].img is None):
#             img = self.bkgimg
#         else:
#             img = self.cards[n].img
            
            
        cslb.background(self.bkgimg)
        cslb.text(self.cards[n].words[k])
        
        cslb.logo()
        return target
    
    def getAsImageNQ(self, n):
        target = QImage(self.size, QImage.Format_RGB32);
        painter = QPainter(target)
        cslb = CardSetLayoutBasic(self, painter)
        
        painter.fillRect(cslb.canvas, QBrush(cslb.level_color, Qt.SolidPattern))
        
        cslb.footer()
        cslb.flag(self.cards[n].langs[0])

        
#         if (self.cards[n].img is None):
#             img = self.bkgimg
#         else:
#             img = self.cards[n].img
            
            
        cslb.background(self.bkgimg)
        cslb.textQ(self.cards[n].words[0])
        
        cslb.logo()
        return target
        
    def getAsImageNA(self, n):
        target = QImage(self.size, QImage.Format_RGB32);
        painter = QPainter(target)
        cslb = CardSetLayoutBasic(self, painter)
        
        painter.fillRect(cslb.canvas, QBrush(cslb.level_color, Qt.SolidPattern))
        
        cslb.footer()
        cslb.flag(self.cards[n].langs[1])

        
#         if (self.cards[n].img is None):
#             img = self.bkgimg
#         else:
#             img = self.cards[n].img
            
            
        cslb.background(self.bkgimg)
        cslb.textQ(self.cards[n].words[0])
        cslb.textA(self.cards[n].words[1])
        
        cslb.logo()
        return target        
        
        
    def test(self):
        self.saveAsImagesQA('movie', random.sample(range(len(self.cards)),10))
          
     
class CardSetLayoutBasic():
    
    def _findFontSizes(self):
        self.title_font_size = 72
        for i in range(1, 100):
            f = QFont("Arial", i)
            fm = QFontMetrics(f)
            if (fm.height()>self.maxy/10):
                self.title_font_size = i;
                break;

        self.word_font_size = 72;
        for i in range(1, 100):
            f = QFont("Arial", i)
            fm = QFontMetrics(f)
            if (fm.height()>self.maxy/10):
                self.word_font_size = i;
                break;

        self.footer_font_size = 72;
        for i in range(11, 100):
            f = QFont("Arial", i)
            fm = QFontMetrics(f)
            if (fm.height()>self.maxy/16):
                self.footer_font_size = i;
                break;

        logger.info("Font sizes (title, word, footer): %d,%d,%d" % (self.title_font_size, self.word_font_size, self.footer_font_size))

    
    def __init__(self, fcset, painter):
        self.painter = painter
        self.maxx = painter.device().width()
        self.maxy = painter.device().height()
        logger.info("Canvas size: %d,%d" % (self.maxx, self.maxy))    
        
        self._findFontSizes()
        
        self.canvas = QRect(0, 0, self.maxx, self.maxy)
        self.bckg_img = QRect(0, 0, self.maxx, self.maxy*.9)
        self.body = QRect(0, 0, self.maxx, self.maxy*.9)
        self.title_area = QRect(0, 2*self.maxy/10, self.maxx, 4*self.maxy/10)
        self.text_area = QRect(0, 7*self.maxy/10, self.maxx, 2*self.maxy/10)
        self.textQ_area = QRect(0, 2*self.maxy/10, self.maxx, 2*self.maxy/10)
        self.textA_area = QRect(0, 4*self.maxy/10, self.maxx, 2*self.maxy/10)
        self.textQA_area = QRect(0, 2*self.maxy/10, self.maxx, 4*self.maxy/10)
        
        self.footer_area = QRect(self.maxy/10, 9*self.maxy/10, self.maxx-self.maxy/10, self.maxy/10)
        
        fx = self.footer_area.x()
        fy = self.footer_area.y()
        fh = self.footer_area.height()
        fw = self.footer_area.width()
        
        self.flag_area = QRect(fx+fw-1.1*fh, fy, fh, fh)
        self.fbook_area = QRect(.1*fh, fy+.1*fh, .8*fh, .8*fh)

        self.fbook_logo = QImage()
        fb_logo_file = "img/FB-fLogo-Blue-broadcast-2.png"
        if not self.fbook_logo.load(fb_logo_file, "PNG"):
            logger.warning("Could not load image: \"%s\"" % fb_logo_file)
        else:
#             logger.info("Logo loaded from: \"%s\" successfully" % fb_logo_file)
            pass

        self.logo_area = QRectF(self.maxx*.925, self.maxx*.025, self.maxx*.05, self.maxx*.05)

        self.logo_img = QImage()
        logo_file = 'img/logo3.png'
        if not self.logo_img.load(logo_file):
            logger.warning("Could not load image: \"%s\"" % logo_file)
        else:
#             logger.info("Logo loaded from: \"%s\" successfully" % logo_file)
            pass

        self.logo_area = QRectF(self.maxx*.925, self.maxx*.025, self.maxx*.05, self.maxx*.05)
        
        self.flags = {   
            'pl' : QImage('img/flags/Poland.png'), 
            'en' : QImage('img/flags/United-Kingdom.png'),
            'es' : QImage('img/flags/Spain.png'),
            'it' : QImage('img/flags/Italy.png')
        }
        
        self.level_color = QColor(FlashCardSet.LEVEL_COLOR_EASY) 
        if fcset.level.startswith("B") :
            self.level_color = QColor(FlashCardSet.LEVEL_COLOR_MEDIUM) 
        elif fcset.level.startswith("C") :
            self.level_color = QColor(FlashCardSet.LEVEL_COLOR_HARD)
            
    def logo(self):
        self.painter.drawImage(self.logo_area, self.logo_img)

        
    def footer(self):    
        self.painter.drawImage(self.fbook_area, self.fbook_logo)

        penHText = QPen(Qt.white);
        self.painter.setPen(penHText);
        self.painter.setFont(QFont("Arial", self.footer_font_size, italic=True));
        
        self.painter.drawText(self.footer_area, Qt.AlignLeft | Qt.TextIncludeTrailingSpaces | Qt.AlignVCenter , "/FiszkaBabel")
        
    def flag(self, lang):    
        self.painter.drawImage(self.flag_area, self.flags[lang])
        
    def background(self, bkgimg): 
        self.painter.drawImage(self.bckg_img, bkgimg)    

    def text(self, text):
        wwh = QColor(0,0,0,192)     
        self.painter.fillRect(self.text_area, QBrush(wwh, Qt.SolidPattern))

        penHText = QPen(Qt.white);
        self.painter.setPen(penHText);
        self.painter.setFont(QFont("Arial", self.word_font_size, QFont.Bold))
        
        self.painter.drawText(self.text_area, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignVCenter, \
             QString.fromUtf8("%s" % text))

    def textQ(self, text):
        wwh = QColor(0,0,0,192)     
        self.painter.fillRect(self.textQA_area, QBrush(wwh, Qt.SolidPattern))

        penHText = QPen(Qt.white);
        self.painter.setPen(penHText);
        self.painter.setFont(QFont("Arial", self.word_font_size, QFont.Bold))
        
        self.painter.drawText(self.textQ_area, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignVCenter, \
             QString.fromUtf8("%s" % text))

    def textA(self, text):
        penHText = QPen(Qt.white);
        self.painter.setPen(penHText);
        self.painter.setFont(QFont("Arial", self.word_font_size-4, italic=True))
        
        self.painter.drawText(self.textA_area, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignVCenter, \
             QString.fromUtf8("%s" % text))



    def title(self, text):
        wwh = QColor(0,0,0,192)     
        self.painter.fillRect(self.title_area, QBrush(wwh, Qt.SolidPattern))

        penHText = QPen(Qt.white);
        self.painter.setPen(penHText);
        self.painter.setFont(QFont("Arial", self.title_font_size, QFont.Bold))
        
        self.painter.drawText(self.title_area, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignVCenter, \
             QString.fromUtf8("%s" % text))

class CardSetLayoutQAOnePicture(CardSetLayoutBasic):
    def __init__(self, name):
        base_url = 'http://localhost/ekskursja/wp-content/plugins/flashcards/flashcards.json.php?name='
        
        fc_url = base_url + name
        
        logger.info("GET %s" % fc_url)
        conn = urllib2.urlopen(fc_url)
        fcjson = conn.read()
        c = json.loads(fcjson)
        
#         data = conn.read()
#         img = QImage()
#         img.loadFromData(data)

class PdfCard():
    def __init__(self, fout):
        printer = QPrinter(QPrinter.HighResolution);
        printer.setOutputFileName(fout);
        
        printer.setOutputFormat(QPrinter.PdfFormat);
        printer.setPageSize(QPrinter.A6);
        printer.setOrientation(QPrinter.Landscape);
        printer.setPageMargins (0,0,0,0, QPrinter.Millimeter);
        printer.setFullPage(False);
        
        self.painter = QPainter(printer)
        
#         self.card = PlainCard(self.painter)
        
        logger.info("Will be writing to PDF: %s" % fout)        


class FlashcardWriter():
    '''
    classdocs
    '''
    
    def init_layout(self, painter, fcset):
        self.level_color = QColor(FlashCardSet.LEVEL_COLOR_EASY)    

    
    def write(self, fcset, fout):
        self.title_page(painter, fcset)

        for fc in fcset.cards:
            self.draw_flashcard(printer, painter, fcset, fc)
        
        printer.newPage()
        
        self.title_page(painter, fcset)
        
        painter.end()
        
    def all_bottom(self, painter, level):
        painter.fillRect(0, 0, self.maxx, self.maxy, QBrush(self.level_color, Qt.SolidPattern))

        painter.drawImage(self.fbook_area, self.fbook_logo)


        penHText = QPen(Qt.white);
        painter.setPen(penHText);
        painter.setFont(QFont("Arial", 16, italic=True));
        
        
        painter.drawText(self.footer, Qt.AlignLeft | Qt.TextIncludeTrailingSpaces | Qt.AlignVCenter , "       /FiszkaBabel")
       
    def title_page(self, painter, fcset):
        logger.info("Printing title page: %s" % fcset.title)
        
        self.all_bottom(painter, fcset.level)
        
        bkgimg = QImage()
        if  not bkgimg.load(fcset.img):
            print "Not loaded"
            
        painter.drawImage(self.body, bkgimg)    
        
        wwh = QColor(0,0,0,64)     
        painter.fillRect(self.title_area, QBrush(wwh, Qt.SolidPattern))

        penHText = QPen(Qt.white);
        painter.setPen(penHText);
        painter.setFont(QFont("Arial", 36, QFont.Bold))
        
        painter.drawText(self.title_area, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignVCenter, fcset.title)
        
        self.all_top(painter)

    def draw_flashcard(self, printer, painter, fcset, fcard):
        
        for i in range(0, len(fcard.words)):
            printer.newPage()
            
            logger.info("Printing card: %s [%s]" % (fcard.words[i], fcard.langs[i]))
            
            self.all_bottom(painter, fcset.level)
    
            if (fcard.img is None):
                img = fcset.img
            else:
                img = fcard.img
    
            bkgimg = QImage()
            if  not bkgimg.load(img):
                print "Not loaded:", img
                
            painter.drawImage(self.bckg_img, bkgimg)    
    
            
            wwh = QColor(0,0,0,64)     
            painter.fillRect(self.active_area, QBrush(wwh, Qt.SolidPattern))
    
            penHText = QPen(Qt.white);
            painter.setPen(penHText);
            painter.setFont(QFont("Arial", 36, QFont.Bold))
    
     
            painter.drawText(self.active_area, Qt.AlignCenter | Qt.TextWordWrap | Qt.AlignVCenter, \
                             QString.fromUtf8("%s" % fcard.words[i]))
            
            painter.drawImage(self.flag_area, self.flags[fcard.langs[i]])
    
            self.all_top(painter)

    def all_top(self, painter):
#         painter.setClipRegion(self.logo_region)
        painter.drawImage(self.logo_area, self.logo_img)
            
        
    def background(self, painter, bkgimg):
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