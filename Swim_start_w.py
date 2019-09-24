from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QCheckBox
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import swim_main
import serial.tools.list_ports
import serial_read
import time
import MySQLdb as db
import numpy as np
import webbrowser
import fetchUI
import mysql.connector
from mysql.connector import Error
import itertools
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

#######################################################################################################################
#######################################################################################################################

class UiClass2(QMainWindow,fetchUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(UiClass2, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.switch)
        self.comboBox.addItem("select")
        self.comboBox_2.addItem("select")
        self.comboBox.setCurrentText("select")
        self.comboBox_2.setCurrentText("select")
        self.getNames()

    def getNames(self):

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='lrnDatabase',
                                                 user='root',
                                                 password='imran1996')
            sql_Query = "select Name from page1_pointtable"
            cursor = connection.cursor(buffered=True)
            cursor.execute(sql_Query)
            record = cursor.fetchall()
            self.dbName = list(itertools.chain(*record))
            yar = ['position', 'Required_Time_ms', 'Meter', 'name_id', 'id']
            self.comboBox_2.addItem(yar[0])
            self.comboBox_2.addItem(yar[1])
            self.comboBox_2.addItem(yar[2])
            self.comboBox_2.addItem(yar[3])
            self.comboBox_2.addItem(yar[4])
            xar = []
            for x in range(0,len(self.dbName)):
                if self.dbName[x] not in xar:
                    xar.append(self.dbName[x])
                    self.comboBox.addItem(self.dbName[x])


        except mysql.connector.Error as error:
            print("Failed to get record from database: {}".format(error))
        finally:
            # closing database connection.
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


    def switch(self):

        self.name = self.comboBox.currentText()
        self.filed = self.comboBox_2.currentText()
        print(self.name)
        print(self.filed)
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='lrnDatabase',
                                                 user='root',
                                                 password='imran1996')
            sql_Query = "select %s from page1_pointtable where Name ='%s'" %(self.filed,self.name)
            sql_Query2 = "select %s from page1_pointtable where Name ='%s'" % ("Round", self.name)
            cursor = connection.cursor(buffered=True)
            cursor.execute(sql_Query)
            record = cursor.fetchall()
            cursor.execute(sql_Query2)
            record2 = cursor.fetchall()
            self.mstimes = list(itertools.chain(*record))
            self.rounds = list(itertools.chain(*record2))
            xar = []
            yar = []
            for x in range(0,len(self.mstimes)):
                xar.append(self.rounds[x])
                yar.append((self.mstimes[x]))
            self.ax1.clear()
            self.ax1.stem(xar, yar)
        except mysql.connector.Error as error:
            print("Failed to get record from database: {}".format(error))
        finally:
            # closing database connection.
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        plt.show()

#######################################################################################################################
#######################################################################################################################
class mainUiClass(QMainWindow,swim_main.Ui_MainWindow):
    switch_window = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(mainUiClass, self).__init__(parent)
        self.setupUi(self)
        self.meterSet = 50
        self.threadclass = ThreadClass()
        self.threadclass.start()
        self.threadclass.COMsignal.connect(self.updateCOMports)

        self.reasponseTime = ['','','','','','','','']
        self.finishTime = ['','','','','','','','']
        self.reqTimems = [0,0,0,0,0,0,0,0]
        self.meterCover = [0,0,0,0,0,0,0,0]
        self.timeTaken = [0,0,0,0,0,0,0,0]
        self.position = [0,0,0,0,0,0,0,0]
        self.minIndex = [0, 0, 0, 0, 0, 0, 0, 0]
        self.round = ''

        self.comboBox.addItem("Swimmer 1")
        self.comboBox_2.addItem("Swimmer 2")
        self.comboBox_3.addItem("Swimmer 3")
        self.comboBox_4.addItem("Swimmer 4")
        self.comboBox_5.addItem("Swimmer 5")
        self.comboBox_6.addItem("Swimmer 6")
        self.comboBox_7.addItem("Swimmer 7")
        self.comboBox_8.addItem("Swimmer 8")

        self.comboBox.setCurrentText("Swimmer 1")
        self.comboBox_2.setCurrentText("Swimmer 2")
        self.comboBox_3.setCurrentText("Swimmer 3")
        self.comboBox_4.setCurrentText("Swimmer 4")
        self.comboBox_5.setCurrentText("Swimmer 5")
        self.comboBox_6.setCurrentText("Swimmer 6")
        self.comboBox_7.setCurrentText("Swimmer 7")
        self.comboBox_8.setCurrentText("Swimmer 8")

        self.milliseconds2=0
        self.actionavailable_ports.toggled.connect(self.onStageChange)
        self.actionavailable_ports_2.toggled.connect(self.onStageChange)
        self.actionavailable_ports_3.toggled.connect(self.onStageChange)
        self.actionavailable_ports_4.toggled.connect(self.onStageChange)

        self.action50m.toggled.connect(self.onStageChange_2)
        self.action100m_freestyle.toggled.connect(self.onStageChange_2)
        self.action100m_backstroke.toggled.connect(self.onStageChange_2)
        self.action100m_butterfly.toggled.connect(self.onStageChange_2)
        self.action200m_freestyle.toggled.connect(self.onStageChange_2)
        self.action200m_backstroke.toggled.connect(self.onStageChange_2)
        self.action200m_butterfly.toggled.connect(self.onStageChange_2)

        self.pushButton_3.clicked.connect(self.updateName)
        self.name = ['','','','','','','','']
        self.play = 0
        self.pushButton.clicked.connect(self.startTime)
        self.pushButton_2.clicked.connect(self.endTime)
        self.threadclass.intSignal.connect(self.rcvInt)
        self.inc = 0
        self.pushButton_5.clicked.connect(self.setRound)
        self.pushButton_4.clicked.connect(self.saveInDataBase)
        self.pushButton_6.clicked.connect(self.reset)
        self.strURL = "http://localhost/phpmyadmin/"
        self.actionOpen_Database.triggered.connect(self.openDB)
        self.actionImprovement_Curve.triggered.connect(self.gosecond)
        self.dbName = []
        self.dbID = []
        self.getNames()
    ###################################################################################################################

    def getNames(self):

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='lrnDatabase',
                                                 user='root',
                                                 password='imran1996')
            sql_Query = "select username from auth_user"
            sql_Query2 = "select id from auth_user"
            cursor = connection.cursor(buffered=True)
            cursor.execute(sql_Query)
            record = cursor.fetchall()
            cursor.execute(sql_Query2)
            record2 = cursor.fetchall()
            self.dbName = list(itertools.chain(*record))
            self.dbID = list(itertools.chain(*record2))
            xar = []
            yar = []
            for x in range(0,len(self.dbID)):
                xar.append(self.dbName[x])
                yar.append(self.dbID[x])
                self.comboBox.addItem(self.dbName[x])
                self.comboBox_2.addItem(self.dbName[x])
                self.comboBox_3.addItem(self.dbName[x])
                self.comboBox_4.addItem(self.dbName[x])
                self.comboBox_5.addItem(self.dbName[x])
                self.comboBox_6.addItem(self.dbName[x])
                self.comboBox_7.addItem(self.dbName[x])
                self.comboBox_8.addItem(self.dbName[x])

            print(self.dbName)
            print(self.dbID)

        except mysql.connector.Error as error:
            print("Failed to get record from database: {}".format(error))
        finally:
            # closing database connection.
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")



    ###################################################################################################################
    def gosecond(self):
        self.switch_window.emit("go")
    ###################################################################################################################
    def openDB(self):
        webbrowser.open(self.strURL, new=2)
    ###################################################################################################################
    def reset(self):
        self.reasponseTime = ['', '', '', '', '', '', '', '']
        self.finishTime = ['', '', '', '', '', '', '', '']
        self.meterCover = [0, 0, 0, 0, 0, 0, 0, 0]
        self.timeTaken = [0, 0, 0, 0, 0, 0, 0, 0]
        self.position = [0, 0, 0, 0, 0, 0, 0, 0]
        self.minIndex = [0, 0, 0, 0, 0, 0, 0, 0]
        self.reqTimems = [0, 0, 0, 0, 0, 0, 0, 0]
        self.name = ['', '', '', '', '', '', '', '']
        self.round = ''
        self.inc = 0
        self.play = 0
        self.label_7.setText("status")
        self.lineEdit_9.setText("round")

        self.comboBox.setCurrentText("Swimmer 1")
        self.comboBox_2.setCurrentText("Swimmer 2")
        self.comboBox_3.setCurrentText("Swimmer 3")
        self.comboBox_4.setCurrentText("Swimmer 4")
        self.comboBox_5.setCurrentText("Swimmer 5")
        self.comboBox_6.setCurrentText("Swimmer 6")
        self.comboBox_7.setCurrentText("Swimmer 7")
        self.comboBox_8.setCurrentText("Swimmer 8")

        self.lcdNumber_57.setProperty("value", 0)
        self.lcdNumber_55.setProperty("value", 0)
        self.lcdNumber_48.setProperty("value", 0)
        self.lcdNumber_19.setProperty("value", 0)
        self.lcdNumber_18.setProperty("value", 0)
        self.lcdNumber_16.setProperty("value", 0)
        self.lcdNumber_52.setProperty("value", 0)
        self.lcdNumber_45.setProperty("value", 0)
        self.lcdNumber_50.setProperty("value", 0)
        self.lcdNumber_22.setProperty("value", 0)
        self.lcdNumber_20.setProperty("value", 0)
        self.lcdNumber_21.setProperty("value", 0)
        self.lcdNumber_66.setProperty("value", 0)
        self.lcdNumber_42.setProperty("value", 0)
        self.lcdNumber_70.setProperty("value", 0)
        self.lcdNumber_24.setProperty("value", 0)
        self.lcdNumber_23.setProperty("value", 0)
        self.lcdNumber_25.setProperty("value", 0)
        self.lcdNumber_67.setProperty("value", 0)
        self.lcdNumber_53.setProperty("value", 0)
        self.lcdNumber_49.setProperty("value", 0)
        self.lcdNumber_27.setProperty("value", 0)
        self.lcdNumber_26.setProperty("value", 0)
        self.lcdNumber_28.setProperty("value", 0)
        self.lcdNumber_69.setProperty("value", 0)
        self.lcdNumber_41.setProperty("value", 0)
        self.lcdNumber_71.setProperty("value", 0)
        self.lcdNumber_30.setProperty("value", 0)
        self.lcdNumber_29.setProperty("value", 0)
        self.lcdNumber_31.setProperty("value", 0)
        self.lcdNumber_56.setProperty("value", 0)
        self.lcdNumber_46.setProperty("value", 0)
        self.lcdNumber_43.setProperty("value", 0)
        self.lcdNumber_33.setProperty("value", 0)
        self.lcdNumber_32.setProperty("value", 0)
        self.lcdNumber_34.setProperty("value", 0)
        self.lcdNumber_54.setProperty("value", 0)
        self.lcdNumber_68.setProperty("value", 0)
        self.lcdNumber_58.setProperty("value", 0)
        self.lcdNumber_36.setProperty("value", 0)
        self.lcdNumber_35.setProperty("value", 0)
        self.lcdNumber_37.setProperty("value", 0)
        self.lcdNumber_51.setProperty("value", 0)
        self.lcdNumber_44.setProperty("value", 0)
        self.lcdNumber_47.setProperty("value", 0)
        self.lcdNumber_39.setProperty("value", 0)
        self.lcdNumber_38.setProperty("value", 0)
        self.lcdNumber_40.setProperty("value", 0)
        self.lcdNumber_73.setProperty("value", 0)
        self.lcdNumber_75.setProperty("value", 0)
        self.lcdNumber_74.setProperty("value", 0)
        self.lcdNumber_84.setProperty("value", 0)
        self.lcdNumber_96.setProperty("value", 0)
        self.lcdNumber_99.setProperty("value", 0)
        self.lcdNumber_88.setProperty("value", 0)
        self.lcdNumber_103.setProperty("value", 0)
        self.lcdNumber_105.setProperty("value", 0)
        self.lcdNumber_106.setProperty("value", 0)
        self.lcdNumber_107.setProperty("value", 0)
        self.lcdNumber_108.setProperty("value", 0)
        self.lcdNumber_109.setProperty("value", 0)
        self.lcdNumber_110.setProperty("value", 0)
        self.lcdNumber_111.setProperty("value", 0)




    ###################################################################################################################
    def saveInDataBase(self):
        #try:
        connection = mysql.connector.connect(host='localhost',
                                             database='lrnDatabase',
                                             user='root',
                                             password='imran1996')
        cursor = connection.cursor(buffered=True)
        self.swimmerid = []
        self.arx = []
        for x in range(0,len(self.name)):
            sql_Query = "select id from auth_user where username = '%s'" % (self.name[x])
            cursor.execute(sql_Query)
            record = cursor.fetchone()
            self.arx.append(record)

        self.swimmerid = list(itertools.chain(*self.arx))
        print(self.swimmerid)

        for x in range(0,len(self.name)):
            cursor.execute("INSERT INTO page1_pointtable(Round,Name,Response_Time,Required_Time,Required_Time_ms,Meter,Position,name_id)"
                        "VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (''.join(self.round),
                                                                   ''.join(self.name[x]),
                                                                   ''.join(self.reasponseTime[x]),
                                                                   ''.join(self.finishTime[x]),
                                                                   ''.join("%s"%(self.reqTimems[x])),
                                                                   ''.join("%s"%(self.meterCover[x])),
                                                                   ''.join("%s"%(self.position[x])),
                                                                   ''.join("%s"%(self.swimmerid[x]))))

        self.label_7.setText("Done")
        connection.commit()
        '''        except:
            self.label_7.setText("Fail")
        finally:
            # closing database connection.
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")'''





    ###################################################################################################################
    def setRound(self):
        self.round = self.lineEdit_9.text()
        print(self.round)
    ###################################################################################################################
    def rcvInt(self, inString):
        if chr(inString[0]) == 's' and chr(inString[1]) == 't' and chr(inString[2]) == 'a':
            self.tCount()

        if chr(inString[0]) == 'e' and chr(inString[1]) == 'n' and chr(inString[2]) == 'd':
            self.endTime()

        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '1':
            self.time = serial_read.ston(inString)
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[0] = self.timeToSTR(ms,s,m)
            self.lcdNumber_57.setProperty("value", ms)
            self.lcdNumber_55.setProperty("value", s)
            self.lcdNumber_48.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '1':
            self.time = serial_read.ston(inString)
            self.timeTaken[0] = self.time
            self.inc = self.inc+1
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.finishTime[0] = self.timeToSTR(ms,s,m)
            self.lcdNumber_19.setProperty("value", ms)
            self.lcdNumber_18.setProperty("value", s)
            self.lcdNumber_16.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '2':
            self.time = serial_read.ston(inString)
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[1] = self.timeToSTR(ms, s, m)
            self.lcdNumber_52.setProperty("value", ms)
            self.lcdNumber_45.setProperty("value", s)
            self.lcdNumber_50.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '2':
            self.time = serial_read.ston(inString)
            self.timeTaken[1] = self.time
            self.inc = self.inc + 1
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.finishTime[1] = self.timeToSTR(ms, s, m)
            self.lcdNumber_22.setProperty("value", ms)
            self.lcdNumber_20.setProperty("value", s)
            self.lcdNumber_21.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '3':
            self.time = serial_read.ston(inString)
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[2] = self.timeToSTR(ms, s, m)
            self.lcdNumber_66.setProperty("value", ms)
            self.lcdNumber_42.setProperty("value", s)
            self.lcdNumber_70.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '3':
            self.time = serial_read.ston(inString)
            self.timeTaken[2] = self.time
            self.inc = self.inc + 1
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.finishTime[2] = self.timeToSTR(ms, s, m)
            self.lcdNumber_24.setProperty("value", ms)
            self.lcdNumber_23.setProperty("value", s)
            self.lcdNumber_25.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '4':
            self.time = serial_read.ston(inString)
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[3] = self.timeToSTR(ms, s, m)
            self.lcdNumber_67.setProperty("value", ms)
            self.lcdNumber_53.setProperty("value", s)
            self.lcdNumber_49.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '4':
            self.time = serial_read.ston(inString)
            self.timeTaken[3] = self.time
            self.inc = self.inc + 1
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.finishTime[3] = self.timeToSTR(ms, s, m)
            self.lcdNumber_27.setProperty("value", ms)
            self.lcdNumber_26.setProperty("value", s)
            self.lcdNumber_28.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '5':
            self.time = serial_read.ston(inString)
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[4] = self.timeToSTR(ms, s, m)
            self.lcdNumber_69.setProperty("value", ms)
            self.lcdNumber_41.setProperty("value", s)
            self.lcdNumber_71.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '5':
            self.time = serial_read.ston(inString)
            self.timeTaken[4] = self.time
            self.inc = self.inc + 1
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.finishTime[4] = self.timeToSTR(ms, s, m)
            self.lcdNumber_30.setProperty("value", ms)
            self.lcdNumber_29.setProperty("value", s)
            self.lcdNumber_31.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '6':
            self.time = serial_read.ston(inString)
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[5] = self.timeToSTR(ms, s, m)
            self.lcdNumber_56.setProperty("value", ms)
            self.lcdNumber_46.setProperty("value", s)
            self.lcdNumber_43.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '6':
            self.time = serial_read.ston(inString)
            self.timeTaken[5] = self.time
            self.inc = self.inc + 1
            m,s,ms = self.timeToPrintInLCD(self.time)
            self.finishTime[5] = self.timeToSTR(ms, s, m)
            self.lcdNumber_33.setProperty("value", ms)
            self.lcdNumber_32.setProperty("value", s)
            self.lcdNumber_34.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '7':
            self.time = serial_read.ston(inString)
            m, s, ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[6] = self.timeToSTR(ms, s, m)
            self.lcdNumber_54.setProperty("value", ms)
            self.lcdNumber_68.setProperty("value", s)
            self.lcdNumber_58.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '7':
            self.time = serial_read.ston(inString)
            self.timeTaken[6] = self.time
            self.inc = self.inc + 1
            m, s, ms = self.timeToPrintInLCD(self.time)
            self.finishTime[6] = self.timeToSTR(ms, s, m)
            self.lcdNumber_36.setProperty("value", ms)
            self.lcdNumber_35.setProperty("value", s)
            self.lcdNumber_37.setProperty("value", m)
#
        elif chr(inString[0]) == 'R' and chr(inString[1]) == 'L' and chr(inString[2]) == '8':
            self.time = serial_read.ston(inString)
            m, s, ms = self.timeToPrintInLCD(self.time)
            self.reasponseTime[7] = self.timeToSTR(ms, s, m)
            self.lcdNumber_51.setProperty("value", ms)
            self.lcdNumber_44.setProperty("value", s)
            self.lcdNumber_47.setProperty("value", m)
#
        elif chr(inString[0]) == 'F' and chr(inString[1]) == 'L' and chr(inString[2]) == '8':
            self.time = serial_read.ston(inString)
            self.timeTaken[7] = self.time
            self.inc = self.inc + 1
            m, s, ms = self.timeToPrintInLCD(self.time)
            self.finishTime[7] = self.timeToSTR(ms, s, m)
            self.lcdNumber_39.setProperty("value", ms)
            self.lcdNumber_38.setProperty("value", s)
            self.lcdNumber_40.setProperty("value", m)
#
        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '1':
            self.met = serial_read.ston(inString)
            self.meterCover[0]=self.met
            self.lcdNumber_72.setProperty("value", self.met)
#
        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '2':
            self.met = serial_read.ston(inString)
            self.meterCover[1] = self.met
            self.lcdNumber_73.setProperty("value", self.met)

        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '3':
            self.met = serial_read.ston(inString)
            self.meterCover[2] = self.met
            self.lcdNumber_75.setProperty("value", self.met)

        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '4':
            self.met = serial_read.ston(inString)
            self.meterCover[3] = self.met
            self.lcdNumber_74.setProperty("value", self.met)

        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '5':
            self.met = serial_read.ston(inString)
            self.meterCover[4] = self.met
            self.lcdNumber_84.setProperty("value", self.met)

        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '6':
            self.met = serial_read.ston(inString)
            self.meterCover[5] = self.met
            self.lcdNumber_96.setProperty("value", self.met)

        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '7':
            self.met = serial_read.ston(inString)
            self.meterCover[6] = self.met
            self.lcdNumber_99.setProperty("value", self.met)

        elif chr(inString[0]) == 'M' and chr(inString[1]) == 'L' and chr(inString[2]) == '8':
            self.met = serial_read.ston(inString)
            self.meterCover[7] = self.met
            self.lcdNumber_88.setProperty("value", self.met)

        print(self.timeTaken)

        if self.inc >=8:
            for z in range(0,len(self.timeTaken)):
                self.reqTimems[z] = self.timeTaken[z]

            for x in range(0,len(self.timeTaken)):
                self.minIndex[x] = self.timeTaken.index(min(self.timeTaken))
                self.timeTaken[self.minIndex[x]] = max(self.timeTaken) + 1

            for y in range(0,len(self.timeTaken)):
                self.timeTaken[self.minIndex[y]] = y+1
                self.position[self.minIndex[y]] = y+1

            self.lcdNumber_103.setProperty("value", self.timeTaken[0])
            self.lcdNumber_105.setProperty("value", self.timeTaken[1])
            self.lcdNumber_106.setProperty("value", self.timeTaken[2])
            self.lcdNumber_107.setProperty("value", self.timeTaken[3])
            self.lcdNumber_108.setProperty("value", self.timeTaken[4])
            self.lcdNumber_109.setProperty("value", self.timeTaken[5])
            self.lcdNumber_110.setProperty("value", self.timeTaken[6])
            self.lcdNumber_111.setProperty("value", self.timeTaken[7])

            print(self.reasponseTime)
            print(self.finishTime)

            self.endTime()

        print(self.timeTaken)
    ###################################################################################################################
    def timeToSTR(self,ek,dos,shot):
        out = "%s:%s:%s" % (shot,dos,ek)
        return out
    ###################################################################################################################
    def timeToPrintInLCD(self, val):
        self.ms = 0
        self.s = 0
        self.m = 0
        if val < 1000:
            self.ms = val
        elif val >= 1000:
            self.s = int(val / 1000)
            self.ms = int(val % 1000)

            if self.s >= 60:
                self.m = int(self.s / 60)
                self.s = self.s % 60
        return self.m,self.s,self.ms
    ###################################################################################################################
    def startTime(self):
        serial_read.send_value(b'start')
        print('start')
        #self.tCount()
    ###################################################################################################################
    def tCount(self):
        self.milliseconds2 = int(round(time.time() * 1000))
        self.threadclass.timeSignal.connect(self.runTime)
        self.play = 1
    ###################################################################################################################
    def runTime(self, t):
        if self.play == 1:
            self.timeToPrint = t - self.milliseconds2
            self.ms0 = 0
            self.s0 = 0
            self.m0 = 0
            if self.timeToPrint < 1000:
                self.ms0 = self.timeToPrint
            elif self.timeToPrint >= 1000:
                self.s0 = int(self.timeToPrint / 1000)
                self.ms0 = int(self.timeToPrint % 1000)

                if self.s0 >= 60:
                    self.m0 = int(self.s0 / 60)
                    self.s0 = self.s0 % 60

            self.lcdNumber_2.setProperty("value", self.ms0)
            self.lcdNumber_3.setProperty("value", self.s0)
            self.lcdNumber.setProperty("value", self.m0)
            #print(self.timeToPrint)
    ###################################################################################################################
    def endTime(self):
        serial_read.send_value(b'end')
        self.play = 0
        self.inc = 0
    ###################################################################################################################
    def updateName(self):
        self.name[0] = self.comboBox.currentText()
        self.name[1] = self.comboBox_2.currentText()
        self.name[2] = self.comboBox_3.currentText()
        self.name[3] = self.comboBox_4.currentText()
        self.name[4] = self.comboBox_5.currentText()
        self.name[5] = self.comboBox_6.currentText()
        self.name[6] = self.comboBox_7.currentText()
        self.name[7] = self.comboBox_8.currentText()

        for x in range(0,len(self.name)):
            print(self.name[x])
    ###################################################################################################################
    def onStageChange(self, state):
        if state == True:
            self.ports = serial.tools.list_ports.comports(include_links=False)
            self.ports.reverse()
            if self.sender() == self.actionavailable_ports:
                self.setCOMports1(self.ports)
                self.actionavailable_ports_2.setChecked(False)
                self.actionavailable_ports_3.setChecked(False)
                self.actionavailable_ports_4.setChecked(False)
            elif self.sender() == self.actionavailable_ports_2:
                self.setCOMports2(self.ports)
                self.actionavailable_ports.setChecked(False)
                self.actionavailable_ports_3.setChecked(False)
                self.actionavailable_ports_4.setChecked(False)
            elif self.sender() == self.actionavailable_ports_3:
                self.setCOMports3(self.ports)
                self.actionavailable_ports.setChecked(False)
                self.actionavailable_ports_2.setChecked(False)
                self.actionavailable_ports_4.setChecked(False)
            elif self.sender() == self.actionavailable_ports_4:
                self.setCOMports4(self.ports)
                self.actionavailable_ports.setChecked(False)
                self.actionavailable_ports_2.setChecked(False)
                self.actionavailable_ports_3.setChecked(False)
    ###################################################################################################################
    def onStageChange_2(self, state):
        if state == True:

            if self.sender() == self.action50m:
                serial_read.send_value(b'm50')
                self.meterSet = 50
                self.action100m_freestyle.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action200m_butterfly.setChecked(False)
            elif self.sender() == self.action100m_freestyle:
                serial_read.send_value(b'm100')
                self.meterSet = 100
                self.action50m.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action200m_butterfly.setChecked(False)
            elif self.sender() == self.action100m_backstroke:
                serial_read.send_value(b'm100')
                self.meterSet = 100
                self.action100m_freestyle.setChecked(False)
                self.action50m.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action200m_butterfly.setChecked(False)
            elif self.sender() == self.action100m_butterfly:
                serial_read.send_value(b'm100')
                self.meterSet = 100
                self.action100m_freestyle.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action50m.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action200m_butterfly.setChecked(False)
            elif self.sender() == self.action200m_freestyle:
                serial_read.send_value(b'm200')
                self.meterSet = 200
                self.action100m_freestyle.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action50m.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action200m_butterfly.setChecked(False)
            elif self.sender() == self.action200m_backstroke:
                serial_read.send_value(b'm200')
                self.meterSet = 200
                self.action100m_freestyle.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action50m.setChecked(False)
                self.action200m_butterfly.setChecked(False)
            elif self.sender() == self.action200m_butterfly:
                serial_read.send_value(b'm200')
                self.meterSet = 200
                self.action100m_freestyle.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action50m.setChecked(False)
            else:
                serial_read.send_value(b'm50')
                self.meterSet = 50
                self.action50m.setChecked(False)
                self.action100m_freestyle.setChecked(False)
                self.action100m_backstroke.setChecked(False)
                self.action100m_butterfly.setChecked(False)
                self.action200m_freestyle.setChecked(False)
                self.action200m_backstroke.setChecked(False)
                self.action200m_butterfly.setChecked(False)

        print(self.meterSet)
    ###################################################################################################################
    def setCOMports1(self, ports):
        print(ports[0])
        j=serial_read.set_port(ports[0])
        print(j)
    ###################################################################################################################
    def setCOMports2(self, ports):
        print(ports[1])
        j=serial_read.set_port(ports[1])
        print(j)
    ###################################################################################################################
    def setCOMports3(self, ports):
        print(ports[2])
        j=serial_read.set_port(ports[2])
        print(j)
    ###################################################################################################################
    def setCOMports4(self, ports):
        print(ports[3])
        j=serial_read.set_port(ports[3])
        print(j)
    ###################################################################################################################
    def updateCOMports(self,ports):

        if len(ports)==1 :
            self.actionavailable_ports.setText(str(ports[0]))
            self.actionavailable_ports.setVisible(True)
            self.actionavailable_ports_2.setVisible(False)
            self.actionavailable_ports_3.setVisible(False)
            self.actionavailable_ports_4.setVisible(False)
        if len(ports)==2:
            self.actionavailable_ports.setText(str(ports[0]))
            self.actionavailable_ports.setVisible(True)
            self.actionavailable_ports_2.setText(str(ports[1]))
            self.actionavailable_ports_2.setVisible(True)
            self.actionavailable_ports_3.setVisible(False)
            self.actionavailable_ports_4.setVisible(False)
        if len(ports)==3:
            self.actionavailable_ports.setText(str(ports[0]))
            self.actionavailable_ports.setVisible(True)
            self.actionavailable_ports_2.setText(str(ports[1]))
            self.actionavailable_ports_2.setVisible(True)
            self.actionavailable_ports_3.setText(str(ports[2]))
            self.actionavailable_ports_3.setVisible(True)
            self.actionavailable_ports_4.setVisible(False)
        if len(ports)==4:
            self.actionavailable_ports.setText(str(ports[0]))
            self.actionavailable_ports.setVisible(True)
            self.actionavailable_ports_2.setText(str(ports[1]))
            self.actionavailable_ports_2.setVisible(True)
            self.actionavailable_ports_3.setText(str(ports[2]))
            self.actionavailable_ports_3.setVisible(True)
            self.actionavailable_ports_4.setText(str(ports[3]))
            self.actionavailable_ports_4.setVisible(True)
        elif len(ports)==0:
            self.actionavailable_ports.setVisible(False)
            self.actionavailable_ports_2.setVisible(False)
            self.actionavailable_ports_3.setVisible(False)
            self.actionavailable_ports_4.setVisible(False)
#######################################################################################################################
#######################################################################################################################
class ThreadClass(QtCore.QThread):
    COMsignal = pyqtSignal('PyQt_PyObject')
    timeSignal = pyqtSignal('PyQt_PyObject')
    intSignal = pyqtSignal('PyQt_PyObject')
    #signal_2 = pyqtSignal('PyQt_PyObject')
    def __init__(self, parent = None):
        super(ThreadClass, self).__init__(parent)
    ###################################################################################################################
    def run(self):
        self.len1=0
        self.port = serial.tools.list_ports.comports(include_links=False)

        j = serial_read.set_port('')
        print(j)

        while 1:
            self.ports1 = serial.tools.list_ports.comports(include_links=False)
            self.ports1.reverse()
            #if self.len1 != len(self.ports1):
            self.COMsignal.emit(self.ports1)
            #self.signal_2.emit(value)
            #self.len1 = len(self.ports1)
            self.milliseconds = int(round(time.time() * 1000))
            self.timeSignal.emit(self.milliseconds)
            self.S = serial_read.give_value()
            #print(self.S)
            if len(self.S) > 3:
                self.intSignal.emit(self.S)
                print(self.S)
#######################################################################################################################
#######################################################################################################################
class Controller:

    def __init__(self):
        pass


    def show_main(self):
        self.window = mainUiClass()
        self.window.switch_window.connect(self.show_window_two)
        self.window.show()

    def show_window_two(self):
        self.window_two = UiClass2()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()