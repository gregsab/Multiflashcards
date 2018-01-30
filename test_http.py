import urllib2, sys
from PyQt4.Qt import QApplication
from PyQt4.Qt import QImage


app = QApplication(sys.argv)

proxy = urllib2.ProxyHandler({'http': 'sabakgrz:2155Sylwia!@126.179.0.206:9090'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
# conn = urllib2.urlopen('http://ekskursja.pl/wp-content/plugins/flashcards/flashcards.json.php?name=animal-idioms&id=3652')

conn = urllib2.urlopen('http://ekskursja.pl/wp-content/uploads/2014/01/maxresdefault.jpg')
data = conn.read()
img = QImage()
img.loadFromData(data)

img.save('test.jpg')

# fcjson = conn.read()
# c = json.loads(fcjson)
# print fc['type']

