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

    app = QApplication(sys.argv)
    
    fcs = FlashCardSet()
    fcs.getFromEkskursja('the-hitchhikers-guide-to-the-galaxy-part-1')
    
    fcs.test()
    
    logger.info('Finished')

if __name__ == '__main__':
    main()


# print fcs.cards[0]