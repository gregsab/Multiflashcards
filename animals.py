# -*- coding: utf-8 -*-
'''
Created on 31 pa 2016

@author: sabakgrz
'''
import sys, logging

from babel.fcards import FlashCard, FlashCardSet, PdfCard

from PyQt4.Qt import QApplication


def main():
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)

    logger.info('Started on %s' % sys.version)
    logger.info('Using %s' % sys.executable)

    app = QApplication()
    
    langs = ('pl', 'en', 'es', 'it')
    
    fcs = FlashCardSet('OWOCE cz.1', img = 'img/owoce/owoce09.jpg', level="A1")
    fcs.addCard( FlashCard(('jabłko', 'apple', 'manzana', 'mela'), langs, 'img/owoce/owoce01.jpg') )
    fcs.addCard( FlashCard(('gruszka', 'pear', 'pera', 'pera'), langs, 'img/owoce/owoce02.jpg') )
    fcs.addCard( FlashCard(('arbuz', 'water melon', 'sandia', 'cocomero, anguria'), langs, 'img/owoce/owoce03.jpg') )
    fcs.addCard( FlashCard(('banan', 'banana', 'platano', 'banana'), langs, 'img/owoce/owoce04.jpg') )
    fcs.addCard( FlashCard(('wiśnia', 'cherry', 'guindo', 'amarena'), langs, 'img/owoce/owoce05.jpg') )
    fcs.addCard( FlashCard(('śliwka', 'plum', 'ciruela', 'prugna'), langs, 'img/owoce/owoce07.jpg') )
    fcs.addCard( FlashCard(('winogrona', 'grapes', 'uva', 'uva'), langs, 'img/owoce/owoce08.jpg') )
    
    fcs.test()
    
    logger.info('Finished')

if __name__ == '__main__':
    main()


# print fcs.cards[0]