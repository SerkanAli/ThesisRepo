from hashlib import new
import sys
import json
import os
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QTextBrowser, QTreeWidget, QTreeWidgetItem, QMessageBox)
from elg import (Service, Authentication)
from elg.model import (AnnotationsResponse, TextsResponseObject)

m_ServiceID = 478
m_Annotation = ""
m_Features = ""
m_bAutoContent = False

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        label = QLabel("Write the ID of the service")
        self.edit = QLineEdit("")
        self.button = QPushButton("Check Service")
        self.tb = QTextBrowser()
        self.btnClose= QPushButton("...")
        self.btnClose.setDisabled(True)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layout.addWidget(self.tb)
        layout.addWidget(self.btnClose)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.CheckService)
        self.btnClose.clicked.connect(self.close)

    def CheckService(self):
        global m_ServiceID
        if self.edit.text().isdecimal() == False:
            self.edit.setText("Write here only a valid integer!!!")
            return

        m_ServiceID = self.edit.text()
        auth = Authentication.from_json('authJSONFile')
        service = Service.from_id(self.edit.text(), auth)
        self.tb.setText("Service ID:" + self.edit.text() + 
        "\nService Name:" + service.resource_name +
        "\nService Type:" + service.resource_type +
        "\nDescription:" + service.description)
        self.btnClose.setEnabled(True)
        self.btnClose.setText("Get Service:" + str(m_ServiceID))


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name", "Type", "Btn"])
        self.tree.itemClicked.connect(self.OnItemClicked)
        self.button = QPushButton("Check Service")
        self.label = QLabel("Select one item from the list as output \nCurrent item:")
        self.acceptbtn = QPushButton("Generate Output")
        self.acceptbtn.setDisabled(True)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.tree)
        layout.addWidget(self.label)
        layout.addWidget(self.acceptbtn)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.CheckService)
        self.acceptbtn.clicked.connect(self.OnGenerateOutput)

    # Greets the user
    def CheckService(self):
        form = Form()
        form.exec()
        auth = Authentication.from_json('authJSONFile')
        service = Service.from_id(m_ServiceID, auth)
        #plainText = 'Meistens ist der Stoff eine grünlich glasige Masse aus geschmolzenem Quarz und Feldspat. Hallo, nebensatz!. Teile der Schmelzmassen allerdings enthalten große Mengen Metalle, die aus der verdampften Infrastruktur stammen'
        plainText = 'Hallo!'
        result = service(plainText)
        if result.type =="annotations":
            self.ShowAnnotation(result)
        elif result.type == "texts":
            self.ShowText(result)
        return

    def ShowAnnotation(self, input: AnnotationsResponse):
        global m_bAutoContent
        items = []
        
        typeItem = QTreeWidgetItem(["Service Info"])
        typechild = QTreeWidgetItem(["Type", input.type])
        typeItem.addChild(typechild)
        feauterchild = QTreeWidgetItem(["Feauteres", json.dumps(input.features)])
        typeItem.addChild(feauterchild)
        items.append(typeItem)

        self.FillAnnotation(input.annotations, items)
        m_bAutoContent= False
        return
    
    def ShowText(self, input: TextsResponseObject):
        global m_bAutoContent
        items = []

        typeItem = QTreeWidgetItem(["Service Info"])
        typechild = QTreeWidgetItem(["Type", input.type])
        typeItem.addChild(typechild)
        #feauterchild = QTreeWidgetItem(["Feauteres", json.dumps(input.features)])
        #typeItem.addChild(feauterchild)
        items.append(typeItem)
        contentItem = QTreeWidgetItem(["Content"])
        for text in input.texts:
            contentChild = QTreeWidgetItem(["content", text.content])
            contentItem.addChild(contentChild)
            contentChild = QTreeWidgetItem(["features", text.features])
            contentItem.addChild(contentChild)
            contentChild = QTreeWidgetItem(["score", text.score])
            contentItem.addChild(contentChild)
            items.append(contentItem)
            self.FillAnnotation(text.annotations, items)
        
        m_bAutoContent = True
        return

    def FillAnnotation(self, data, items):
        self.btn = QPushButton("Press")  
        if data is not None:
            for key, values in data.items():
                item = QTreeWidgetItem([key])
                for value in values:
                    for bla in value.features:            
                        child = QTreeWidgetItem([bla, value.features[bla]])
                        self.tree.setItemWidget(child, 0, self.btn)
                        item.addChild(child)
                    break
                items.append(item)

        self.tree.insertTopLevelItems(0, items)

    def OnItemClicked(self):
        global m_Annotation, m_Features
        self.label.setText("Select one item from the list as output \nCurrent item:" + self.tree.currentItem().text(0))
        self.acceptbtn.setEnabled(True)
        m_Features = self.tree.currentItem().text(0)
        if self.tree.itemAbove(self.tree.currentItem()) is not None:
            m_Annotation = self.tree.itemAbove(self.tree.currentItem()).text(0)
        return

    def OnGenerateOutput(self):
        outstr = ""
        if m_bAutoContent:
            f = open("UI/tempAuto.txt", "r")
            outstr = f.read()
            outstr = outstr.replace("*ID*", str(m_ServiceID))
        else:
            f = open("UI/temp.txt", "r")
            outstr = f.read()
            outstr = outstr.replace("*ID*", str(m_ServiceID))
            outstr = outstr.replace("*annotations*", str(m_Annotation))
            outstr = outstr.replace("*features*", str(m_Features))
        print(outstr)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Would you like to update the Mapper?")
        msg.setWindowTitle("Update Mapper")
        msg.setDetailedText(outstr)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if  msg.exec() == QMessageBox.Ok:
            self.UpdateMapper(outstr)
           
        return
    
    def UpdateMapper(self, outstr):
        f = open("Service/resolver.py", "r+")
        code = f.read()
        f.seek(0)
        checkLine = "_" + str(m_ServiceID) +"(self"
        newCode = ""
        if checkLine in code:
            lines = code.splitlines()
            bAdd = True
            for line in lines:
                if checkLine in line:
                    bAdd = False
                if bAdd:
                    newCode = newCode + line + "\n"
                if "return" in line:
                    bAdd = True
        else:
            newCode = code
    
        f.write(newCode + "\n    "+ outstr)
        f.close()

        os.system('docker build -t serkanali/elgservicetexttotext:texttottext ./Service')
        os.system('docker push serkanali/elgservicetexttotext:texttottext')

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MainForm()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())