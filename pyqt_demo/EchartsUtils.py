from PyQt5.QtWidgets import  QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import  QUrl

offset = 20

class Line(object):
    '''
    @param: basehtml: absolute path of html file
    @param: qtcontainer: container to visualize html, only test on QScrollArea now
    @param: legends: list of str for legends
    '''
    def __init__(self, basehtml: str, qtcontainer: QScrollArea, \
                 legends: list, title="") -> None:
        super().__init__()

        self.myHtml = QWebEngineView()
        self.myHtml.loadFinished.connect(self.slotHtmlLoadFinished)

        self.container = qtcontainer
        self.container.setWidget(self.myHtml)

        self.htmlLoadFinished = False
    
        htmlFilename = "file:///{}".format(basehtml)
        self.myHtml.load(QUrl(htmlFilename))

        self.legends = legends
        self.title = title

    def slotHtmlLoadFinished(self):
        self.htmlLoadFinished = True
        self.setTitle(self.title)
        self.build()
    
    def update(self, xAxisData: any, yAxisData: list):
        assert len(self.legends) == len(yAxisData)
        yAxisData = [str(i) for i in yAxisData]
        xAxisData = str(xAxisData)
        jscode = '''update({}, {});'''.format(xAxisData, yAxisData)
        self.myHtml.page().runJavaScript(jscode)   

    def setTitle(self, title: str):
        jscode = '''setTitle('{}');'''.format(title)
        self.myHtml.page().runJavaScript(jscode)      

    def build(self):
        self.myHtml.page().runJavaScript("build('{}', '{}', {}); ".format(int(self.container.width()-offset), 
                                                                    int(self.container.height()-offset), 
                                                                    self.legends))

class Bar(object):
    '''
    @param: basehtml: absolute path of html file
    @param: qtcontainer: container to visualize html, only test on QScrollArea now
    @param: legends: list of str for legends
    '''
    def __init__(self, basehtml: str, qtcontainer: QScrollArea, \
                 xAxis: list, legends: list, title="") -> None:
        super().__init__()

        self.myHtml = QWebEngineView()
        self.myHtml.loadFinished.connect(self.slotHtmlLoadFinished)

        self.container = qtcontainer
        self.container.setWidget(self.myHtml)

        self.htmlLoadFinished = False
    
        htmlFilename = "file:///{}".format(basehtml)
        self.myHtml.load(QUrl(htmlFilename))

        self.legends = legends
        self.series_num = len(self.legends)
        self.xAxis = xAxis
        self.title = title

    def slotHtmlLoadFinished(self):
        self.htmlLoadFinished = True
        self.setTitle(self.title)
        self.build()
    
    def update(self, yAxisData: list):
        yAxisData = [str(i) for i in yAxisData]
        jscode = '''update({})'''.format(yAxisData)
        self.myHtml.page().runJavaScript(jscode)   
    
    def setTitle(self, title: str):
        jscode = '''setTitle('{}')'''.format(title)
        self.myHtml.page().runJavaScript(jscode)      

    def build(self):
        self.myHtml.page().runJavaScript("build('{}', '{}', {}, {}); ".format(int(self.container.width()-offset), 
                                                                    int(self.container.height()-offset), 
                                                                    self.xAxis, self.legends))

class Pie(object):
    '''
    @param: basehtml: absolute path of html file
    @param: qtcontainer: container to visualize html, only test on QScrollArea now
    '''
    def __init__(self, basehtml: str, qtcontainer: QScrollArea, title="") -> None:
        super().__init__()

        self.myHtml = QWebEngineView()
        self.myHtml.loadFinished.connect(self.slotHtmlLoadFinished)

        self.container = qtcontainer
        self.container.setWidget(self.myHtml)

        self.htmlLoadFinished = False
    
        htmlFilename = "file:///{}".format(basehtml)
        self.myHtml.load(QUrl(htmlFilename))

        # self.legend = legend
        self.title = title

    def slotHtmlLoadFinished(self):
        self.htmlLoadFinished = True
        self.build()
        self.setTitle(self.title)
    
    def update(self, data: dict):
        keys = [str(i) for i in data.keys()]
        values = [str(i) for i in data.values()]

        jscode = '''update({},{})'''.format(keys, values)
        self.myHtml.page().runJavaScript(jscode)
    
    def setTitle(self, title: str):
        jscode = '''setTitle('{}')'''.format(title)
        self.myHtml.page().runJavaScript(jscode)      

    def build(self):
        self.myHtml.page().runJavaScript("build('{}', '{}'); ".format(int(self.container.width()-offset), 
                                                                    int(self.container.height()-offset)))
