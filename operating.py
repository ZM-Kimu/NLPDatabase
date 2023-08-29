import os
import winreg


def getDesktopPath(self):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    self.desktopPath = winreg.QueryValueEx(key, "Desktop")[0]+"\\"
    print("getdesktop",self.desktopPath)

def createTable(self, attr):
    try:
        self.readAttr = attr
        self.contentList = []
        if os.path.exists(self.desktopPath+self.fileName+".txt"):
            self.info = "文件已存在，进行覆盖"
            self.Prio = "warning"
        else:
            self.info = "创建成功"
            self.Prio = "normal"
        writeContentToText(self)
    except Exception as err:
        print(err)
        self.info = "错误，无法将指定信息写入至指定文件，可能是未拥有权限，或语句错误"
        self.Prio = "high"


def getContent(self):
    try:
        readAllToMem(self)
        self.readJudgement = False
        self.contentList = []
        print(self.fileName, "filenameingetCOnte")
        if os.path.exists(self.desktopPath+self.fileName+".txt"):
            self.readAttr = self.readTable[0]
            attr = self.readAttr.strip("\n")
            print(attr, "in getattr")
            if " " in attr or attr == "":
                self.info = "在文件内检测到不规范的属性名，出现错误，请检查文件"
                self.Prio = "high"
            if "、" in attr:
                self.attr_sepeChar = "、"
                self.attr_sepe = attr.split("、")
            if "，" in attr:
                self.attr_sepeChar = "，"
                self.attr_sepe = attr.split("，")
            if len(self.readTable) > 1:
                content = self.readTable[1:]
                for i in content:
                    i = i.strip("\n").split(" ")
                    self.contentList.append(i)
                self.readJudgement = True
                print(f"this{type(self.contentList)}ingetcontent")
            self.fileIsExists = True
        else:
            self.info = f"文件{self.fileName}不存在，请先创建文件，或更改语句"
            self.Prio = "high"
            self.fileIsExists = False
    except:
        self.info = f"在读文件{self.fileName}时遇到错误，可能是权限不足，或语句错误"
        self.Prio = "high"


def queryFromid(self, num):
    for i in self.contentList:
        if i[0] == num:
            self.info = f"{i}"
            self.Prio = "normal"
            return
    self.info = "无任何结果"
    self.Prio = "middle"


def queryFromValue(self, uniqueValue, queryIndex):
    for content in self.contentList:
        if uniqueValue in content:
            queryList = []
            for index in queryIndex:
                queryList.append(f"{self.attr_sepe[index]}:{content[index]}")
            self.info = f"{queryList}"
            self.Prio = "normal"
            return
    self.info = "无任何结果"
    self.Prio = "middle"


def insertRecord(self, list):
    getContent(self)
    dictLeftIndex, dictRightIndex = 0, len(self.contentList)-1
    if len(self.contentList) > 0 and self.readJudgement:
        while dictLeftIndex <= dictRightIndex:
            middleIndex = (dictLeftIndex + dictRightIndex) // 2
            print(self.contentList[middleIndex], list, len(self.contentList), dictLeftIndex,
                  middleIndex, dictRightIndex)
            if self.contentList[middleIndex][0] == list[0]:
                self.info = "已有存在的编号"
                self.Prio = "middle"
                return
            elif self.contentList[middleIndex][0] > list[0]:
                dictRightIndex = middleIndex - 1
            else:
                dictLeftIndex = middleIndex + 1
        self.contentList.insert(dictLeftIndex, list)
        self.info = f"编号为{list[0]}的信息已存入"
        self.Prio = "normal"
    elif len(self.contentList) == 0 and not self.readJudgement:
        self.contentList.insert(dictLeftIndex, list)
        self.info = f"第一条信息已存入"
        self.Prio = "normal"
    writeContentToText(self)


def deleteRecord(self, num):
    getContent(self)
    if self.readJudgement:
        for i in self.contentList:
            print(i, "i in deler")
            if i[0] == num:
                print(i[0], "inkerdelete")
                del self.contentList[self.contentList.index(i)]
                self.info = f"成功删除编号为{num}的记录"
                self.Prio = "warning"
                break
            else:
                self.info = "删除失败，可能是编号不存在"
                self.Prio = "middle"
    else:
        self.info = "删除失败，文件不存在内容"
        self.Prio = "middle"
    writeContentToText(self)


def deleteValue(self, recordNum, indexList):
    getContent(self)
    print(indexList, "indexlist")
    attrList = []
    for i in indexList:
        attrList.append(self.attr_sepe[i])
    for i in self.contentList:
        if i[0] == recordNum:
            for index in indexList:
                print(i[index], "instand")
                i[index] = "Null"
            self.info = f"成功删除记录{recordNum}中的{attrList}"
            self.Prio = "warning"
            break
        else:
            self.info = f"编号{recordNum}不存在"
            self.Prio = "middle"
    writeContentToText(self)


def getTextFile(self):
    fileList = os.listdir(self.desktopPath)
    self.hasTableNow = []
    for i in fileList:
        if ".txt" in i:
            self.hasTableNow.append(i)


def writeContentToText(self):
    file = open(self.desktopPath+self.fileName+".txt", "wt")
    file.write(self.readAttr)
    for i in self.contentList:
        i = " ".join(i)
        print(f"write{i}intxt")
        file.write(i+"\n")
    file.close()


def readAllToMem(self):
    try:
        file = open(self.desktopPath+self.fileName+".txt", "rt")
        read = file.readlines()
        file.close()
        self.readTable = read
    except:
        self.info = "无法解析源文件，可能是文件不存在，或权限错误"
        self.Prio = "high"
