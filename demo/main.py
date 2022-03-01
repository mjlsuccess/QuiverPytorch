from cgitb import html
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer

import sys, os
rootpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(rootpath)

from matplotlib.pyplot import title
import numpy as np
from torchvision import  models

from mainwindow_ui import *
import echarts.utils as echarts
from quiver.utils import ModelViewer

from quiver.engine import server
from quiver.engine.model_utils import register_hook

# 主界面
def cvtPath(path):
    return path.replace(os.sep, "/")

class MainWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(MainWindow, self).__init__(parent=parent, flags=flags)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # echarts 图标可视化
        currentfolder = os.path.abspath(os.path.dirname(__file__))
        root = os.path.join(os.path.dirname(currentfolder), "echarts", "html")
        colors = ['#dd6b66', '#759aa0', '#e69d87']

        htmlfile = os.path.join(root, "line.html")
        self.line1 = echarts.Line(cvtPath(htmlfile), self.ui.scrollArea, ["Series1 %", "Series2 %", "Series3 %", "Series4 %"], colors=colors, title="Line test")
        self.line2 = echarts.Line(cvtPath(htmlfile), self.ui.scrollArea_4, ["Series1 %", "Series2 %", "Series3 %", "Series4 %"], colors=colors, title="Line test")

        htmlfile = htmlfile = os.path.join(root, "bar.html")
        
        self.bar1 = echarts.Bar(cvtPath(htmlfile), self.ui.scrollArea_2, xAxis=["123"], legends=["Series1 %", "Series2 %", "Series3 %", "Series4 %"], colors=colors, title="Bar test1") 
        self.bar2 = echarts.Bar(cvtPath(htmlfile), self.ui.scrollArea_5, xAxis=["123"], legends=["Series1 %", "Series2 %", "Series3 %", "Series4 %"], title="Bar test2") 

        htmlfile = os.path.join(root, "pie.html")
        self.pie1 = echarts.Pie(cvtPath(htmlfile), self.ui.scrollArea_3, colors=colors,  title="Pie test1/ms")
        self.pie2 = echarts.Pie(cvtPath(htmlfile), self.ui.scrollArea_7, title="Pie test2/ms")

        # self.ui.tabWidget.tabBarClicked.connect(self.slotTabClicked)

        self.show()

        # 定时器，用于生产echarts可视化所需的数据
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.slotTimeout)
        self.count = 0
        self.timer.start()

        # quiver 模型可视化相关
        self.models = {"vgg":models.vgg19(pretrained=False), "resnet":models.resnet18(pretrained=False)}
        self.model = self.models["vgg"]
        rootpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.datapth = os.path.join(rootpath, "data", "Cat")
        self.modelVis = ModelViewer(self.ui.scrollArea_10)
        
        self.ui.pushButton.clicked.connect(self.slotModelVis)
        self.ui.checkBox_resnet.stateChanged.connect(self.slotModelSelect)
        self.ui.checkBox_vgg.stateChanged.connect(self.slotModelSelect)

        self.clearflag = False

    def slotModelSelect(self, status):
        if self.ui.checkBox_vgg.isChecked():
            self.model = self.models["vgg"]
            currentfolder = os.path.abspath(os.path.dirname(__file__))
            self.datapth = os.path.join(os.path.dirname(currentfolder), "data","Cat")

        if self.ui.checkBox_resnet.isChecked():
            self.model = self.models["resnet"]
            currentfolder = os.path.abspath(os.path.dirname(__file__))
            self.datapth = os.path.join(os.path.dirname(currentfolder), "data","Dog")

    # 模型可视化
    def slotModelVis(self):
        print("load model vis")
        self.modelVis.slotUpdateModel(self.model, self.datapth)

    def slotTimeout(self):
        if self.line1.htmlLoadFinished:
            self.count += 1
            xValue = self.count
            yValue1 = np.random.randint(10,40)
            yValue2 = np.random.randint(20,40)
            yValue3 = np.random.randint(30,40)
            yValue4 = np.random.randint(20,40)            

            # test bar
            if self.count <= 5:
                self.bar1.update([yValue1, yValue2, yValue3, yValue4])
                self.bar2.update([yValue1, yValue2, yValue3, yValue4])
            elif self.count>5 and self.count <10:
                
                self.bar1.clearData()
                self.bar2.clearData()
                    # self.clearflag = True
            else:
                self.bar1.update([yValue1, yValue2, yValue3, yValue4])
                self.bar2.update([yValue1, yValue2, yValue3, yValue4])   

            # test line
            if self.count <= 5:
                self.line1.update(xValue, [yValue1, yValue2, yValue3, yValue4])
                self.line2.update(xValue, [yValue1, yValue2, yValue3, yValue4])
            elif self.count>5 and self.count <10:
                self.line1.clearData()
                self.line2.clearData()
            else:
                self.line1.update(xValue, [yValue1, yValue2, yValue3, yValue4])
                self.line2.update(xValue, [yValue1, yValue2, yValue3, yValue4])      

            # test pie
            if self.count <= 5:
                self.pie1.update({"test1": yValue1,"test2": yValue2,"test3": yValue3,"test4": yValue4})
                self.pie2.update({"test1": yValue1,"test2": yValue2,"test3": yValue3,"test4": yValue4})
            elif self.count>5 and self.count <10:
                self.pie1.clearData()
                self.pie2.clearData()
            else:
                self.pie1.update({"test1": yValue1,"test2": yValue2,"test3": yValue3,"test4": yValue4})
                self.pie2.update({"test1": yValue1,"test2": yValue2,"test3": yValue3,"test4": yValue4})                        
               

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())