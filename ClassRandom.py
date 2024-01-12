from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import random
import sqlite3
import re
import math
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QFont

Main_Window=uic.loadUiType("./material/Main_Window_withoutList.ui")[0]
conn1 = sqlite3.connect("Member.db", isolation_level=None)
c = conn1.cursor()

class Home(QMainWindow, Main_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        c.execute("CREATE TABLE IF NOT EXISTS Member(Number text PRIMARY KEY, Name text, Position text DEFAULT 'None')")
        self.ClassWork_Btn.clicked.connect(self.NoList)
        self.PositionSet_Btn.clicked.connect(self.NoList)
        self.RandomGroup_Btn.clicked.connect(self.NoList)
        self.RandomNum_Btn.clicked.connect(self.call_RandomNum)
        self.RegisMember_Btn.clicked.connect(self.call_RegisMember)
        self.Refresh_Btn.clicked.connect(self.show_member)
        self.Exit_Btn.clicked.connect(self.ExitBtn)

    def show_member(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = re.sub(r'[^0-9]', '', str(c.fetchone()))
        if row == '0':

            QMessageBox.warning(self, "데이터 없음", "학급명단을 찾을 수 없습니다.\n\n'학급명단입력' 을 통해 명단을 등록하시기 바랍니다.")
        else:
            self.call_ExistList()
    def call_ExistList(self):
        self.close()
        Main_Window_ExistList(self)
    def call_RegisMember(self):
        RegisMember(self)
    def initUI(self):  # 창크기설정
        self.setGeometry(50, 50, 895, 750)
        self.show()
    def NoList(self):
        QMessageBox.critical(self, "데이터 없음", "학급명단을 불러올 수 없습니다.\n\n본 기능은 학급명단을 등록한 후 이용할 수 있습니다.")
    def call_RandomNum(self):
        RandomNum(self)
    def ExitBtn(self):
        msg = QMessageBox.question(self, "종료", "프로그램을 종료합니다.", QMessageBox.Yes|QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.close()
        else:
            pass
class Main_Window_ExistList(QMainWindow):
    def __init__(self, parent):
        super(Main_Window_ExistList, self).__init__(parent)
        uic.loadUi("./material/Main_Window_ExistList.ui", self)
        self.initUI()
        self.show_member()
        self.ClassWork_Btn.clicked.connect(self.call_ClassWork)
        self.PositionSet_Btn.clicked.connect(self.call_PositionSet)
        self.RandomGroup_Btn.clicked.connect(self.call_RandomGroup)
        self.RandomNum_Btn.clicked.connect(self.call_RandomNum)
        self.RegisMember_Btn.clicked.connect(self.call_RegisMember)
        self.Refresh_Btn.clicked.connect(self.show_member)
        self.Exit_Btn.clicked.connect(self.ExitBtn)
    def initUI(self):  # 창크기설정
        self.setGeometry(50, 50, 895, 750)
        self.show()
    def show_member(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        self.Total_LCD.display(row)
        self.MemList.setRowCount(math.ceil(row/2))
        for i in range(math.ceil(row/2)+1): # 왼쪽 셀 채우기
            c.execute("SELECT Number FROM Member WHERE Number=?", (str(i),))
            Number_Left = re.sub(r'[^0-9]', '     ', str(c.fetchone()))
            c.execute("SELECT Name FROM Member WHERE Number=?", (str(i),))
            Name_Left = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '    ', str(c.fetchone()))
            c.execute("SELECT Number FROM Member WHERE Number=?", (str(i+1+math.ceil(row/2)),))
            Number_Right = re.sub(r'[^0-9]', '     ', str(c.fetchone()))
            c.execute("SELECT Name FROM Member WHERE Number=?", (str(i+1+math.ceil(row/2)),))
            Name_Right = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '   ', str(c.fetchone()))
            self.MemList.setItem(i-1, 0, QTableWidgetItem(Number_Left))
            self.MemList.setItem(i-1, 1, QTableWidgetItem(Name_Left))
            self.MemList.setItem(i, 2, QTableWidgetItem(Number_Right))
            if Name_Right == 'None':
                self.MemList.setItem(i, 3, QTableWidgetItem('    '))
            else:
                self.MemList.setItem(i, 3, QTableWidgetItem(Name_Right))
    def call_ClassWork(self):
        ClassWork(self)
    def call_PositionSet(self):
        PositionSet(self)
    def call_RegisMember(self):
        RegisMember(self)
    def call_RandomNum(self):
        RandomNum(self)
    def call_RandomGroup(self):
        RandomGroup(self)
    def ExitBtn(self):
        msg = QMessageBox.question(self, "종료", "프로그램을 종료합니다.", QMessageBox.Yes|QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.close()
        else:
            pass
class ClassWork(QMainWindow):
    def __init__(self, parent):
        super(ClassWork, self).__init__(parent)
        uic.loadUi("./material/ClassWork.ui", self)
        self.initUI()
        self.Add_Btn.clicked.connect(self.AddBtn)
        self.Exit_Btn.clicked.connect(self.ExitBtn)
        self.Del_Btn.clicked.connect(self.DelBtn)
        self.ManualWrite_Btn.clicked.connect(self.call_Manual)
        self.Reset_Btn.clicked.connect(self.ResetBtn)
        self.Save_Btn.clicked.connect(self.SaveBtn)
        self.Random_Btn.clicked.connect(self.RandomBtn)
        self.Position_Status_Btn.clicked.connect(self.call_StatusView)
        self.Refresh_Btn.clicked.connect(self.Refresh)
        self.Refresh()
    def call_Manual(self):
        ClassWork_Manual(self)
    def Refresh(self):
        c.execute("SELECT COUNT(*) FROM Member WHERE Position LIKE '%None%'")
        NonSet = int(re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone())))
        self.None_LCD.display(NonSet)
    def call_StatusView(self):
        ClassWork_StatusView(self)
    def SaveBtn(self):
        for i in range (self.Member_Table.rowCount()):
            text = self.Member_Table.item(i, 2)
            if not text:
                QMessageBox.warning(self, "데이터 없음", "배정내역이 존재하지 않습니다.")
            else:
                num = re.findall("\d+", text.text()) #배정결과에서 번호만 num List 에 입력
                cycle = len(num)
                for j in range(cycle):
                    Position = self.Member_Table.item(i, 0)
                    NumValue = num[j]
                    c.execute("UPDATE Member SET Position = ? WHERE Number = ?", (Position.text(), NumValue))
                c.execute("SELECT COUNT(*) FROM Member WHERE Position LIKE '%None%'")
                NonSet = int(re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone())))
                self.None_LCD.display(NonSet)
        QMessageBox.information(self, "데이터 저장됨", "배정내역이 성공적으로 저장되었습니다.")
        return 0
    def RandomBtn(self):
        sum=0
        for i in range (self.Member_Table.rowCount()):
            temp = self.Member_Table.item(i, 0)
            temp2 = self.Member_Table.item(i, 1)
            if not temp:
                QMessageBox.warning(self, "역할 미입력", str(i+1)+"번째 행의 역할을 입력하십시오.")
                return 0
            elif not temp2:
                QMessageBox.warning(self, "인원 수 미입력", str(i+1)+"번째 행의 인원 수를 입력하십시오.")
                return 0
            elif temp2.text().isdecimal() == False or temp2.text() == '0':
                QMessageBox.critical(self, "입력 오류", "인원 수는 자연수로 입력되어야 합니다.\n\n문제가 있는 행은 "+str(i+1)+"번째 행 입니다.")
                return 0
            else:
                sum = sum + int(temp2.text())
        c.execute("SELECT COUNT(*) FROM Member WHERE Position LIKE '%None%'")
        NonSet = int(re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone())))
        if sum > NonSet:
            QMessageBox.critical(self, "인원 수 초과", "배정하려는 인원이 미배정 인원보다 많습니다.\n\n미배정 인원은 "+str(NonSet)+"명 입니다. 입력된 인원의 총합은 "+str(sum)+"명 입니다.")
            return 0
        else:
            c.execute("SELECT COUNT(*) FROM Member")
            row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
            TotalPersonNum = [] # 전체 배열; 뽑히지 않은 학생의 번호 배열
            for h in range(row):
                c.execute("SELECT Position FROM Member WHERE Number = ?", (str(h+1),))
                Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                if Value == 'None':
                    TotalPersonNum.append(h+1) # 안뽑힌 학생을 배열에 입력
                else:
                    pass
            TheNumberPosition = self.Member_Table.rowCount() # 역할 수
            for i in range(TheNumberPosition):
                TheNumberPerson = self.Member_Table.item(i, 1) # 역할당 지정한 인원 수
                TheNumberPerson = int(TheNumberPerson.text())
                SelectedPerson = []  # 뽑힌 학생 번호와 이름을 저장하는 배열
                for j in range(TheNumberPerson):
                    SelectedPersonNum = random.choice(TotalPersonNum) # 전체 배열에서 랜덤으로 1회 추출
                    del TotalPersonNum[TotalPersonNum.index(SelectedPersonNum)] # 추출된 번호 전체 배열에서 삭제
                    if TheNumberPerson <= 6:  # 6개까지 이름, 그 이상은 번호만.
                        c.execute("SELECT Name FROM Member WHERE Number=?", (str(SelectedPersonNum),))
                        Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                        SelectedPerson.append(str(SelectedPersonNum)+"번 "+ Value +"  ")
                        SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                    else:
                        SelectedPerson.append(str(SelectedPersonNum) + "번 ")
                        SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                    self.Member_Table.setItem(i, 2, QTableWidgetItem(" "+SelectedPersonText))
            SelectedPerson = [] # 남은사람의 번호와 이름을 저장하는 배열
            for j in TotalPersonNum:
                if len(TotalPersonNum) <= 8:  # 6개까지 이름, 그 이상은 번호만.
                    c.execute("SELECT Name FROM Member WHERE Number=?", (str(j),))
                    Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                    SelectedPerson.append(str(j)+"번 "+ Value +"  ")
                    SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                else:
                    SelectedPerson.append(str(j) + "번 ")
                    SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
            if not SelectedPerson:
                self.Left_Table.setItem(0, 1, QTableWidgetItem("  "))
            else:
                self.Left_Table.setItem(0, 1, QTableWidgetItem(" "+SelectedPersonText))
    def AddBtn(self):
        self.Member_Table.insertRow(self.Member_Table.rowCount())
    def DelBtn(self):
        if self.Member_Table.rowCount()==1:
            QMessageBox.warning(self, "경고", "첫 행은 삭제할 수 없습니다.")
        else:
            self.Member_Table.removeRow(self.Member_Table.rowCount()-1)
    def ResetBtn(self):
        msg = QMessageBox.warning(self, "데이터 삭제 주의", "입력한 내용을 모두 삭제하시겠습니까?", QMessageBox.Yes|QMessageBox.No)
        if msg==QMessageBox.Yes:
            while (self.Member_Table.rowCount()>0):
                self.Member_Table.removeRow(self.Member_Table.rowCount()-1)
            self.Member_Table.insertRow(self.Member_Table.rowCount())
            self.Left_Table.setItem(0, 1, QTableWidgetItem(" "))
            QMessageBox.information(self, "데이터 삭제됨", "입력한 내용 모두 정상적으로 삭제되었습니다.")
        else:
            QMessageBox.information(self, "데이터 삭제되지 않음", "입력한 내용이 삭제되지 않았습니다.")
    def ExitBtn(self):
            self.close()
    def initUI(self):  # 창크기설정
        self.setGeometry(100, 100, 1200, 750)
        self.show()
class ClassWork_Manual(QMainWindow):
    def __init__(self, parent):
        super(ClassWork_Manual, self).__init__(parent)
        uic.loadUi("./material/ClassWork_Manual.ui", self)
        self.initUI()
        self.Cancel_Btn.clicked.connect(self.CancelBtn)
        self.Edit_Reset_Btn.clicked.connect(self.EditResetBtn)
        self.Save_Btn.clicked.connect(self.SaveBtn)
        self.All_Reset_Btn.clicked.connect(self.AllResetBtn)
        self.LoadUser()
    def AllResetBtn(self):
        msg = QMessageBox.question(self, "데이터 삭제 주의", "배정한 내용을 모두 초기화시킵니까?\n\n초기화 후에는 되돌릴 수 없습니다. (자동 저장됩니다.)")
        if msg==QMessageBox.Yes:
            for i in range(self.Member_Table.rowCount()):
                self.Member_Table.setItem(i, 1, QTableWidgetItem("None"))
                c.execute("UPDATE Member SET Position = 'None'")
            QMessageBox.information(self, "데이터 삭제됨", "모든 배정사항이 초기상태로 되돌려졌습니다.")
            self.close()
        else:
            QMessageBox.information(self, "데이터 삭제되지 않음", "모든 배정사항이 보존됩니다.")
    def EditResetBtn(self):
        msg = QMessageBox.warning(self, "데이터 삭제 주의", "입력한 내용을 되돌리겠습니까?", QMessageBox.Yes|QMessageBox.No)
        if msg==QMessageBox.Yes:
            while (self.Member_Table.rowCount()>0):
                self.Member_Table.removeRow(self.Member_Table.rowCount()-1)
            self.Member_Table.insertRow(self.Member_Table.rowCount())
            self.LoadUser()
            QMessageBox.information(self, "데이터 삭제됨", "입력내용이 정상적으로 되돌려졌습니다.")
        else:
            QMessageBox.information(self, "데이터 삭제되지 않음", "입력한 내용이 초기화되지 않았습니다.")
    def CancelBtn(self):
        msg = QMessageBox.question(self, "경고", "취소하시겠습니까?", QMessageBox.Yes|QMessageBox.No)
        if msg==QMessageBox.Yes:
            self.close()
        else:
            pass    
    def LoadUser(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        self.Member_Table.setRowCount(row)
        for i in range(row+1):
            c.execute("SELECT Name FROM Member WHERE Number=?", (str(i),))
            Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
            self.Member_Table.setItem(i-1, 0, QTableWidgetItem(Value))
            c.execute("SELECT Position FROM Member WHERE Number=?", (str(i),))
            Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
            self.Member_Table.setItem(i-1, 1, QTableWidgetItem(Value))
        return 0
    def SaveBtn(self):
        msg = QMessageBox.question(self, "역할수동저장", "저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            for i in range(self.Member_Table.rowCount()):
                #TableName = self.Member_Table.item(i, 0)
                #TableName = TableName.text()
                position = self.Member_Table.item(i ,1)
                position = position.text()
                if not position: #not TableName or not position:
                    QMessageBox.critical(self, "데이터 입력 오류", "입력되지 않은 행이 있습니다. 확인하십시오.\n\n문제가 있는 행은 "+str(i + 1)+"번째 행 입니다.")
                    return
                if position == 'None':
                    pass
                else:
                    c.execute("UPDATE Member SET Position = ? WHERE Number = ?", (position, str(i+1)))
            QMessageBox.information(self, "데이터 저장됨", "입력한 내용이 정상적으로 저장되었습니다.")
            self.close()
            
        else:
            QMessageBox.information(self, "데이터 저장되지 않음", "입력한 내용이 저장되지 않았습니다.")
    def initUI(self):
        self.setGeometry(150, 150, 700, 500)
        self.show()
class ClassWork_StatusView(QMainWindow):
    def __init__(self, parent):
        super(ClassWork_StatusView, self).__init__(parent)
        uic.loadUi("./material/ClassWork_View.ui", self)
        self.initUI()
        self.Close_Btn.clicked.connect(self.Close)
        self.LoadUser()
    def LoadUser(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        self.Member_Table.setRowCount(row)
        for i in range(row+1):
            c.execute("SELECT Name FROM Member WHERE Number=?", (str(i),))
            Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '   ', str(c.fetchone()))
            self.Member_Table.setItem(i-1, 0, QTableWidgetItem(Value))
            c.execute("SELECT Position FROM Member WHERE Number=?", (str(i),))
            Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '   ', str(c.fetchone()))
            self.Member_Table.setItem(i-1, 1, QTableWidgetItem(Value))
    def Close(self):
        self.close()
    def initUI(self):  # 창크기설정
        self.setGeometry(150, 150, 600, 450)
        self.show()
class PositionSet(QMainWindow):
    def __init__(self, parent):
        super(PositionSet, self).__init__(parent)
        uic.loadUi("./material/PositionSet.ui", self)
        self.initUI()
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        self.Total_LCD.display(row)
        self.SetPosition_Btn.clicked.connect(self.SetPosition)
        self.Close_Btn.clicked.connect(self.Close)
    def Close(self):
        self.close()
    def initUI(self):  # 창크기설정
        self.setGeometry(100, 100, 895, 750)
        self.show()
    def SetPosition(self):
        self.Position_display.setColumnCount(self.LineNum.value())
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        if row % self.LineNum.value() == 0:
            self.Position_display.setRowCount(row//self.LineNum.value())
        else:
            self.Position_display.setRowCount(row // self.LineNum.value() +1)
        TotalPersonNum = []  # 뽑히지 않은 학생의 번호
        for i in range(row):
            TotalPersonNum.append(i + 1)
        for j in range(self.Position_display.rowCount()): #열 채우기
            for k in range(self.LineNum.value()): # 행 채우기
                if not TotalPersonNum:
                    return
                else:
                    SelectedPersonNum = random.choice(TotalPersonNum)
                    del TotalPersonNum[TotalPersonNum.index(SelectedPersonNum)]
                    c.execute("SELECT Name FROM Member WHERE Number=?", (str(SelectedPersonNum),))
                    Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                    SelectedPersonText = (str(SelectedPersonNum)+"번 "+ Value +"  ")
                    self.Position_display.setItem(j, k, QTableWidgetItem(" " + SelectedPersonText))
class RegisMember(QMainWindow):
    def __init__(self, parent):
        super(RegisMember, self).__init__(parent)
        uic.loadUi("./material/RegisMember.ui", self)
        self.initUI()
        self.Load_Btn.clicked.connect(self.LoadBtn)
        self.Reset_Btn.clicked.connect(self.ResetBtn)
        self.Add_Btn.clicked.connect(self.AddBtn)
        self.Del_Btn.clicked.connect(self.DelBtn)
        self.Save_Btn.clicked.connect(self.SaveBtn)
        self.Cancel_Btn.clicked.connect(self.CancelBtn)
    def LoadBtn(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        if row == 0:
            QMessageBox.warning(self, "데이터 없음", "불러올 학급명단이 없습니다.")
        else:
            self.Member_Table.setRowCount(row)
            for i in range(row+1):
                c.execute("SELECT Name FROM Member WHERE Number=?", (str(i),))
                Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                self.Member_Table.setItem(i-1, 0, QTableWidgetItem(Value))
    def AddBtn(self):
        self.Member_Table.insertRow(self.Member_Table.rowCount())
    def DelBtn(self):
        if self.Member_Table.rowCount()==1:
            QMessageBox.warning(self, "경고", "첫 행은 삭제할 수 없습니다.")
        else:
            self.Member_Table.removeRow(self.Member_Table.rowCount()-1)
    def ResetBtn(self):
        msg = QMessageBox.warning(self, "데이터 삭제 주의", "입력한 내용을 모두 삭제하시겠습니까?", QMessageBox.Yes|QMessageBox.No)
        if msg==QMessageBox.Yes:
            #self.Member_Table.clear()
            while (self.Member_Table.rowCount()>0):
                self.Member_Table.removeRow(self.Member_Table.rowCount()-1)
            self.Member_Table.insertRow(self.Member_Table.rowCount())
            QMessageBox.information(self, "데이터 삭제됨", "입력한 내용 모두 정상적으로 삭제되었습니다.")
        else:
            QMessageBox.information(self, "데이터 삭제되지 않음", "입력한 내용이 삭제되지 않았습니다.")
    def CancelBtn(self):
        msg = QMessageBox.question(self, "경고", "취소하시겠습니까?", QMessageBox.Yes|QMessageBox.No)
        if msg==QMessageBox.Yes:
            self.close()
        else:
            pass
    def SaveBtn(self):
        msg = QMessageBox.question(self, "학급명단저장", "명단 저장 시 기존 자료는 모두 삭제됩니다.\n\n저장하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        if msg == QMessageBox.Yes:
            c.execute("DELETE FROM Member")
            for i in range(self.Member_Table.rowCount()):
                name = self.Member_Table.item(i, 0)
                i = str(i + 1)
                if not name:
                    QMessageBox.critical(self, "데이터 입력 오류", "작성되지 않은 행이 있습니다. 확인하십시오.\n\n문제가 있는 행은 "+i+"번째 행 입니다.")
                    return
                else:
                    c.execute("INSERT INTO Member(Number, Name) VALUES (?, ?)", (i, name.text()))
            QMessageBox.information(self, "데이터 저장됨", "입력한 내용이 정상적으로 저장되었습니다.")
            self.close()
        else:
            QMessageBox.information(self, "데이터 저장되지 않음", "입력한 내용이 저장되지 않았습니다.")
    def initUI(self):  # 창크기설정
        self.setGeometry(100, 100, 690, 900)
        self.show()
class RandomNum(QMainWindow):
    def __init__(self, parent):
        super(RandomNum, self).__init__(parent)
        uic.loadUi("./material/RandomNum.ui", self)
        self.initUI()
        self.Sel_Btn.clicked.connect(self.Select)
    def Select(self):
        self.RandomSelNum.display(random.randint(1, self.Number.value()))
    def initUI(self):  # 창 크기 설정
        self.setGeometry(100, 100, 600, 450)
        self.show()
class RandomGroup(QMainWindow):
    def __init__(self, parent):
        super(RandomGroup, self).__init__(parent)
        uic.loadUi("./material/RandomGroup.ui", self)
        self.initUI()
        self.TotalNum()
        self.MakeGroup_Btn.clicked.connect(self.MakeGroup)
        self.Close_Btn.clicked.connect(self.Close)
    def Close(self):
        self.close()
    def MakeGroup(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        self.Total_LCD.display(row)
        if row<self.GroupNum.value():
            QMessageBox.critical(self, "조가 너무 많음", "조가 너무 많아 조 편성이 불가능합니다.\n\n개수 조절이 필요합니다...")
            return
        elif self.GroupNum.value()*self.GroupPerson.value() > row:
            QMessageBox.critical(self, "조 편성 불가", str(self.GroupPerson.value())+"명씩 "+str(self.GroupNum.value())+"개의 조를 만들 수 없습니다. 인원이 부족합니다.\n\n인원 및 조 개수 조절이 필요합니다...")
            return
        else:
            TheNumberGroup = self.GroupNum.value() # 만들고자 하는 조 개수
            TheNumberPerson = self.GroupPerson.value() # 한조당 인원 수
            self.Group_Num_display.setRowCount(TheNumberGroup+1)
            self.Group_Person_display.setRowCount(TheNumberGroup + 1)
            c.execute("SELECT COUNT(*) FROM Member")
            row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
            TotalPersonNum = [] #뽑히지 않은 학생의 번호
            for h in range(row):
                TotalPersonNum.append(h+1)
            for i in range(TheNumberGroup): # 조원 추출
                self.Group_Num_display.setItem(i, 0, QTableWidgetItem('     '+str(i+1)+"조"))
                SelectedPerson = []  # 뽑힌 학생
                for j in range(TheNumberPerson):
                    SelectedPersonNum = random.choice(TotalPersonNum)
                    del TotalPersonNum[TotalPersonNum.index(SelectedPersonNum)]
                    if TheNumberPerson <= 7:  # 6개까지 이름, 그 이상은 번호만.
                        c.execute("SELECT Name FROM Member WHERE Number=?", (str(SelectedPersonNum),))
                        Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                        SelectedPerson.append(str(SelectedPersonNum)+"번 "+ Value +"  ")
                        SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                    else:
                        SelectedPerson.append(str(SelectedPersonNum) + "번 ")
                        SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                    self.Group_Person_display.setItem(i, 0, QTableWidgetItem(" "+SelectedPersonText))
            if len(TotalPersonNum) == 0: # 남은 사람이 없다면 "남은사람" 행 출력X
                self.Group_Num_display.setRowCount(TheNumberGroup)
                self.Group_Person_display.setRowCount(TheNumberGroup)
            else: # 남은 사람 존재하는 경우 - "남은사람" 행 출력하기
                self.Group_Num_display.setItem(i+1, 0, QTableWidgetItem('  남은사람'))
                SelectedPerson = []
                for j in TotalPersonNum:
                    if len(TotalPersonNum) <= 6:  # 6개까지 이름, 그 이상은 번호만.
                        c.execute("SELECT Name FROM Member WHERE Number=?", (str(j),))
                        Value = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(c.fetchone()))
                        SelectedPerson.append(str(j)+"번 "+ Value +"  ")
                        SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                    else:
                        SelectedPerson.append(str(j) + "번 ")
                        SelectedPersonText = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', str(SelectedPerson))
                    self.Group_Person_display.setItem(TheNumberGroup, 0, QTableWidgetItem(" "+SelectedPersonText))
    def TotalNum(self):
        c.execute("SELECT COUNT(*) FROM Member")
        row = int(re.sub(r'[^0-9]', '', str(c.fetchone())))
        self.Total_LCD.display(row)
    def initUI(self):
        self.setGeometry(100, 100, 1000, 850)
        self.show()
if __name__=="__main__":
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont("./material/NanumSquareRoundB.ttf")
    app.setFont(QFont("NanumSquareRoundB"))
    fontDB.addApplicationFont("./material/NanumSquareRoundEB.ttf")
    app.setFont(QFont("NanumSquareRoundEB"))
    fontDB.addApplicationFont("./material/NanumSquareRoundL.ttf")
    app.setFont(QFont("NanumSquareRoundL"))
    fontDB.addApplicationFont("./material/NanumSquareRoundR.ttf")
    app.setFont(QFont("NanumSquareRoundR"))
    HomeWindow = Home()
    sys.exit(app.exec_())