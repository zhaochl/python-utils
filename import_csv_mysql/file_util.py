#!/bin/python

def writefile(destfileName,data2w):
    wordF= file( destfileName,'w')
    wordF.write('%s' %(data2w))
    wordF.close()

def appendfile(destfileName,data2w):
    wordF= file( destfileName,'a')
    wordF.write('%s' %(data2w))
    wordF.close()

def writefile4int(destfileName,iValue):
    wordF= file( destfileName,'w')
    wordF.write('%d' %(iValue))
    wordF.close()

def readfile(destfileName):
    if not os.path.exists(destfileName):
        return ""
    singleFile= file( destfileName,'r')
    singleFile.seek(0)
    fContent = singleFile.read()
    singleFile.close()
    return fContent


