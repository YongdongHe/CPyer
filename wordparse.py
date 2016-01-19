#coding=utf8
from config import chars,num,space,sym
code  = open("my.cpp").read()

class wordParse():
    def __init__(self,code):
        self.code = code
        self.index = 0
        self.buff = ""
        self.status = 0
        self.time = 0
    def getCh(self):
        # print '%d====%s'%(len(self.code),self.index)
        if(self.index==len(self.code)):
            self.index += 1
            return self.code[self.index-2]
        if self.index > len(self.code):
            raise EOFError()
        else:
            self.index += 1
            return self.code[self.index-1]

    def recall(self):
        if self.index >= 1 :
            self.index -=1
    def parseSym(self):
        print "<%s,sym>"%(self.buff)
        self.flushBuff()
    def parseNum(self):
        print "<%s,num>"%(self.buff)
        self.flushBuff()
    def parseDef(self):
        print "<%s,def>"%(self.buff)
        self.flushBuff()
    def runError(self):
        print "%s<error"%(self.code[:self.index])
    def flushBuff(self):
        self.buff = ""
    def getWord(self):
        while True:
            try:
                print self.status
                if self.status == 0 :
                    #状态0：缓冲区为空
                    ch = self.getCh()
                    self.buff += ch
                    if ch in num:
                        self.status = 1
                    elif ch in chars :
                        self.status = 2
                    elif ch in sym :
                        self.status = 3
                    elif ch in space:
                        self.status = 4
                    else:
                        self.status =-1
                elif self.status ==1:
                    #状态1：缓冲区内为数字
                    ch = self.getCh()
                    if ch in num :
                        self.buff += ch
                        self.status =1
                    elif(ch in sym)or (ch in space):
                         self.parseNum()
                         self.recall()
                         self.status = 0
                    else:
                        self.status = -1
                elif self.status == 2:
                    #状态2：缓冲区内为标识符或者关键字
                    ch = self.getCh()
                    if (ch in chars)or (ch in num):
                        self.buff += ch
                        self.status = 2
                    elif (ch in sym) or (ch in space):
                        self.parseDef()
                        self.recall()
                        self.status =0
                    else:
                        self.status = -1
                elif self.status == 3:
                    #状态3：缓冲区内为符号
                    ch = self.getCh()
                    if ch in sym:
                        self.buff += ch
                        if self.buff in sym:
                            self.parseSym()
                            self.status = 0
                        else:
                            self.buff = self.buff[:-1]
                            self.recall()
                            self.parseSym()
                            self.status = 0
                    else:
                        self.parseSym()
                        self.recall()
                        self.status = 0
                elif self.status == 4:
                    #状态4：缓冲区内为空格
                    ch = self.getCh()
                    if ch in space:
                        self.status =4
                    else:
                        self.flushBuff()
                        self.recall()
                        self.status =0
                else:
                    self.runError()
                    break
            except EOFError,e :
                break


def main():
    word = wordParse(code)
    word.getWord()
    print code

if __name__ == '__main__':
    main()