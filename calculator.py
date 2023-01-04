#using PyQt5 to create a calculator
#importing the necessary modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication,QLineEdit,QGridLayout,QPushButton,QVBoxLayout
import sys
from functools import partial
error='Error'
#class for setting up the application.
class Pycal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(240,240)
        self.setWindowTitle('calculator by zack')
        self._centralWidget=QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout=QVBoxLayout()
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()
    def _createDisplay(self):
        self.display=QLineEdit()
        self.display.setFixedHeight(40)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
    def _createButtons(self):
        self.buttons={}
        self.buttonsLayout=QGridLayout()
        buttons={'7':(0,0),'8':(0,1),'9':(0,2),'/':(0,3),'C':(0,4),'4':(1,0),'5':(1,1),'6':(1,2),'*':(1,3),'(':(1,4),'1':(2,0),'2':(2,1),'3':(2,2),'-':(2,3),')':(2,4),'0':(3,0),'00':(3,1),'.':(3,2),'+':(3,3),'=':(3,4),}
        for txt,pos in buttons.items():
            self.buttons[txt]=QPushButton(txt)
            self.buttons[txt].setFixedSize(40,35)
            self.buttonsLayout.addWidget(self.buttons[txt],pos[0],pos[1])
        self.generalLayout.addLayout(self.buttonsLayout)
    def setDisplayText(self,text):
        self.display.setText(text)
        self.display.setFocus()
    def displayText(self):
        return self.display.text()
    def clearDisplay(self):
        self.setDisplayText('')

#handling errors        
def evaluateExpression(expression):
    try:
        result=str(eval(expression,{},{}))
    except Exception:
        result=error
    return result

#controlling key clicks and screen results
class Control:
    def __init__(self,model,view):
        self._evaluate=model
        self._view=view
        self._connection()
    def _calculateResult(self):
        result=self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)
    def _buildExpression(self,sub_exp):
        if self._view.displayText()==error:
            self._view.clearDisplay()
        expression=self._view.displayText()+sub_exp
        self._view.setDisplayText(expression)
    def _connection(self):
        for txt,btn in self._view.buttons.items():
            if txt not in {'C','='}:
                btn.clicked.connect(partial(self._buildExpression,txt))
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)

        
def zack():
    app=QApplication(sys.argv)
    view=Pycal()
    view.show()
    model=evaluateExpression
    Control(model=model,view=view)
    sys.exit(app.exec_())

    
if __name__=='__main__':
    zack()

    
