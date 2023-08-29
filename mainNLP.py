from operator import index
from corpus import *
from operating import *
import jieba


class __mainPreProcess:

    def __init__(self, string):
        self.str = string
        self.fileName = ""
        self.info = ""
        self.Prio = ""
        getDesktopPath(self)

    def natureLanguageSplit(self):
        string = self.str
        if string == "":
            string = "你好"
        excludes = {"的", " ", "是", "", "", "", "", "", "", "", "", "", ""}
        stringList = jieba.lcut(string)
        for i in excludes:
            if i in stringList:
                del stringList[stringList.index(i)]
        self.strList = stringList
        print(stringList)


class __mainAnalyze(__mainPreProcess):

    def __init__(self, string):
        super().__init__(string)
        super().natureLanguageSplit()

    def groupAnalyze(self):
        createCount, queryCount, insertCount, deleteCount = 0, 0, 0, 0
        for i in self.strList:
            if i in create_group:
                createCount += 1
            if i in query_Group:
                queryCount += 1
            if i in insert_group:
                insertCount += 1
            if i in delete_group:
                deleteCount += 1
        self.createRate = createCount/len(self.strList)
        self.queryRate = queryCount/len(self.strList)
        self.inserRate = insertCount/len(self.strList)
        self.deleteRate = deleteCount/len(self.strList)
        self.groupRate = (createCount+queryCount+insertCount +
                          deleteCount)/len(self.strList)

    def doAnalyze(self):
        exitCount = 0
        for i in self.strList:
            if i in exit_do:
                exitCount += 1
        self.exitRate = exitCount/len(self.strList)

    def attributionAnalyze(self):
        tableCount, attrCount = 0, 0
        for i in self.strList:
            if i in table_design:
                tableCount += 1
            if i in attr_design:
                attrCount += 1
        self.tableRate = tableCount/len(self.strList)
        self.attrRate = attrCount/len(self.strList)
        self.designRate = (tableCount+attrCount)/len(self.strList)

    def opAnalyze(self):
        todoCount, isCount, andCount, thenCount = 0, 0, 0, 0
        for i in self.strList:
            if i in todo_op:
                todoCount += 1
            if i in is_op:
                isCount += 1
            if i in and_op:
                andCount += 1
            if i in then_op:
                thenCount += 1
        self.todoRate = todoCount/len(self.strList)
        self.isRate = isCount/len(self.strList)
        self.andRate = andCount/len(self.strList)
        self.thenRate = thenCount/len(self.strList)
        self.opRate = (todoCount+isCount+andCount+thenCount)/len(self.strList)

    def actionAnalyze(self):
        userCount, machineCount, wannaCount, greetingCount, sorryCount, modestyAskCount = 0, 0, 0, 0, 0, 0
        for i in self.strList:
            if i in user_action:
                userCount += 1
            if i in machine_action:
                machineCount += 1
            if i in wanna_action:
                wannaCount += 1
            if i in greeting_action:
                greetingCount += 1
            if i in sorry_action:
                sorryCount += 1
            if i in modestyAsk_action:
                modestyAskCount += 1
        self.userRate = userCount/len(self.strList)
        self.machineRate = machineCount/len(self.strList)
        self.wannaRate = wannaCount/len(self.strList)
        self.greetingRate = greetingCount/len(self.strList)
        self.sorryRate = sorryCount/len(self.strList)
        self.modestyAskRate = modestyAskCount/len(self.strList)
        self.actionRate = (userCount+machineCount+wannaCount +
                           greetingCount+sorryCount+modestyAskCount)/len(self.strList)

    def statusAnalyze(self):
        statusCount = 0
        for i in self.strList:
            if i in logic_status:
                statusCount += 1
        self.statusRate = statusCount/len(self.strList)

    def numericAnalyze(self):
        numericCount = 0
        for i in self.strList:
            if i.isdigit():
                numericCount += 1
            if i in numeric_num:
                numericCount += 1
            if i in numeric_kanji:
                numericCount += 1
        self.numericRate = numericCount/len(self.strList)

    def opProbabilityAnalyze(self):
        self.opRate = [False, False, False, False, False]
        if self.createRate > 0:
            self.opRate[0] = True
        if self.queryRate > 0:
            self.opRate[1] = True
        if self.inserRate > 0:
            self.opRate[2] = True
        if self.deleteRate > 0:
            self.opRate[3] = True
        if self.exitRate > 0:
            self.opRate[4] = True


class behaviorProcess(__mainAnalyze):

    def __init__(self, string):
        super().__init__(string)
        super().groupAnalyze()
        super().attributionAnalyze()
        super().opAnalyze()
        super().actionAnalyze()
        super().statusAnalyze()
        super().numericAnalyze()
        super().doAnalyze()
        super().opProbabilityAnalyze()

    def createTableSentence(self):
        for i in self.strList:
            if i in is_op:
                name_index = self.strList.index(i)+1
                name = self.strList[name_index]
                break
            else:
                name = False
        for i in self.strList:
            if i in table_design:
                table_index = self.strList.index(i)
                break
            else:
                table_index = False
        for i in self.strList:
            if i in attr_design:
                attr_index = self.strList.index(i)
                break
            else:
                attr_index = False
        if str(table_index).isdigit() and str(attr_index).isdigit() and table_index < attr_index:
            text = "".join(self.strList[attr_index+1:])
            text.replace(",", "")
            self.fileName = name
            createTable(self, text+"\n")
        elif name == False or table_index == False or attr_index == False:
            self.info = "在解算管线中遇到错误，请更改语法"
            self.Prio = "high"

    def querySentence(self):
        for i in self.strList:
            if i in table_design:
                tableName_index = self.strList.index(i)+1
                self.fileName = self.strList[tableName_index]
                break
            else:
                self.info = "未在语句中检测到文件名，请更改语句"
                self.Prio = "middle"
        getContent(self)
        if self.fileIsExists:
            for i in self.strList:
                if self.strList.index(i)+2 >= len(self.strList):
                    break
                elif i in self.attr_sepe and self.strList[self.strList.index(i)+1] in is_op and self.strList[self.strList.index(i)+2].isdigit():
                    num = self.strList[self.strList.index(i)+2]
                    break
                elif i in self.attr_sepe and self.strList[self.strList.index(i)+1].isdigit():
                    num = self.strList[self.strList.index(i)+1]
                    break
            value = []
            for i in self.strList:
                if i in self.attr_sepe:
                    value.append(i)
            baseAttr = value[0]
            if len(value) > 1:
                wannaAttr = value[1:]
            if len(value) == 1 and baseAttr in self.attr_sepe:
                queryFromid(self, num)
            elif len(value) > 1 and baseAttr in self.attr_sepe and wannaAttr[0] in self.attr_sepe:
                for i in self.strList:
                    if self.strList.index(i)+2 >= len(self.strList):
                        break
                    elif i in self.attr_sepe and self.strList[self.strList.index(i)+1] in is_op:
                        baseValue = self.strList[self.strList.index(i)+2]
                        break
                    elif self.strList.index(i) in self.attr_sepe:
                        baseValue = self.strList[self.strList.index(i)+1]
                        break
                queryIndex = []
                for i in wannaAttr:
                    if i in self.attr_sepe:
                        queryIndex.append(self.attr_sepe.index(i))
                queryFromValue(self, baseValue, queryIndex)
            else:
                self.info = "无法将各属性转换为指定的请求对象，请更改语句"
                self.Prio = "middle"

    def insertRecordSentence(self):
        for i in self.strList:
            if i in table_design:
                tableName_index = self.strList.index(i)+1
                tableName = self.strList[tableName_index]
                self.fileName = tableName
                break
            else:
                self.info = "未在语句中检测到文件名，请更改语句"
                self.Prio = "middle"
        getContent(self)
        if self.fileIsExists:
            if "“" in self.strList and "”" in self.strList:
                leftindex = self.strList.index("“")+1
                rightindex = self.strList.index("”")
                value = self.strList[leftindex:rightindex]
                value = "".join(value).split("，")
            else:
                attrListIndex = []
                value = []
                for i in self.strList:
                    if i in self.readAttr:
                        getIndex = self.strList.index(i)
                        attrListIndex.append(getIndex)
                if len(attrListIndex) >= len(self.attr_sepe) // 2:
                    for index in attrListIndex:
                        if self.strList[index+1] in is_op:
                            value.append(self.strList[int(index)+2])
                        else:
                            value.append(self.strList[int(index)+1])
            if len(value) == len(self.attr_sepe) and value[0].isdigit():
                insertRecord(self, value)
                return
            self.info = "需要插入的值与属性不相配，请检查语句"
            self.Prio = "middle"

    def deleteSentence(self):
        for i in self.strList:
            if i in table_design:
                tableName_index = self.strList.index(i)+1
                tableName = self.strList[tableName_index]
                self.fileName = tableName
                break
            else:
                self.info = "未在语句中检测到文件名，请更改语句"
                self.Prio = "middle"
        getContent(self)
        indexList = []
        if self.fileIsExists:
            for i in self.strList:
                if i in self.attr_sepe:
                    indexList.append(self.attr_sepe.index(i))
            for i in self.strList:
                if i in self.attr_sepe:
                    if self.strList[self.strList.index(i)+1] in is_op and self.strList[self.strList.index(i)+2].isdigit():
                        num = self.strList[self.strList.index(i)+2]
                        break
                    elif self.strList[self.strList.index(i)+1].isdigit():
                        num = self.strList[self.strList.index(i)+1]
                        break
                    else:
                        self.info = "未在语句中找到需要删除的编号，请更改语句"
                        self.Prio = "middle"
                        break
            if indexList[0] == 0 and len(indexList) == 1:
                deleteRecord(self, num)
            elif len(indexList) > 1 and indexList[0] == 0:
                del indexList[0]
                deleteValue(self, num, indexList)
            else:
                self.info = "检测到不合规的删除语法"
                self.Prio = "high"

    def exitOp(self):
        if len(self.strList) == 1:
            self.info = "退出中..."
            self.Prio = "exit"
        else:
            self.info = "如想退出，请输入退出或quit等语句..."
            self.Prio = "warning"

    def processor(self):
        trueNum = self.opRate.count(True)
        if "你好" in self.strList and len(self.strList) == 1:
            self.info = "你好"
            self.Prio = "normal"
        else:
            print(self.opRate)
            if trueNum == 1:
                if self.opRate[0]:
                    self.createTableSentence()
                if self.opRate[1]:
                    self.querySentence()
                if self.opRate[2]:
                    self.insertRecordSentence()
                if self.opRate[3]:
                    self.deleteSentence()
                if self.opRate[4]:
                    self.exitOp()
            elif trueNum > 1:
                self.info = "在语句中检测到多个操作，请调整语法"
                self.Prio = "middle"
            elif trueNum <= 0:
                self.info = "未在语句中检测到操作，请调整语法"
                self.Prio = "middle"

    def getInfo(self):
        return self.info, self.Prio


class NLPCall(behaviorProcess):

    def __init__(self, string):
        super().__init__(string)
        super().processor()


class memory():

    def memory(self):
        self.memList = []


class debug(behaviorProcess):

    def listAll(self):
        print(self.createRate, self.queryRate, self.queryValueRate,
              self.queryNumberRate, self.inserRate, self.deleteRate,
              self.groupRate, self.tableRate, self.attrRate, self.designRate,
              self.todoRate, self.isRate, self.andRate, self.opRate,
              self.userRate, self.machineRate, self.wannaRate, self.greetingRate,
              self.sorryRate, self.modestyAskRate, self.actionRate,
              self.statusRate, self.numericRate)
