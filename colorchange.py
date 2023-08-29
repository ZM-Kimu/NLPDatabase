class animationObj:

    def __init__(self, colorOri, colorWanna,*args):
        self.Ori = colorOri
        self.middle = args
        self.Wanna = colorWanna
        self.alphaList = "0123456789ABCDEF"
        self.FinalOutputList = []

    def __getColorList(self):
        colorList1, colorList2 = [], []
        for i in self.Ori:
            if i != "#":
                colorList1.append(i)
        for i in self.Wanna:
            if i != "#":
                colorList2.append(i)
        self.colorList1 = colorList1
        self.colorList2 = colorList2

    def __colorCompare(self):
        self.__getColorList()
        is_1_BiggerThan_2 = []
        for i in range(0, 6):
            if self.colorList1[i] > self.colorList2[i]:
                is_1_BiggerThan_2.append(True)
            elif self.colorList1[i] < self.colorList2[i]:
                is_1_BiggerThan_2.append(False)
            else:
                is_1_BiggerThan_2.append(0)
        self.bigger = is_1_BiggerThan_2

    def __loopGet(self):
        self.__colorCompare()
        tick = 0
        after = ""
        while True:
            after = "#"
            for i in range(6):
                if self.bigger[i]:
                    after += str(
                        self.alphaList[self.alphaList.index(self.colorList1[i])-1])
                if self.bigger[i] is False:
                    after += str(
                        self.alphaList[self.alphaList.index(self.colorList1[i])+1])
                elif self.bigger[i] == 0:
                    after += str(self.colorList1[i])
                tick += 1
            self.Ori = after
            self.FinalOutputList.append(self.Ori)
            self.__colorCompare()
            if after == self.Wanna:
                break

    def gradient(self):
        self.__loopGet()
        return self.FinalOutputList

    def basicTransaction(self):
        transactionList = []
        transactionList.append(self.Ori)
        for i in self.middle:
            transactionList.append(i)
        transactionList.append(self.Wanna)
        return transactionList
