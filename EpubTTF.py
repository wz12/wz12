#encoding= utf-8

import glob
import os
import sys
import zipfile
import os.path
import shutil

SS_TO="""@font-face {
	font-family:"zw";
    """
SS_TO_2="""
    src:url(res:///opt/sony/ebook/FONT/zw.ttf),
	url(res:///Data/FONT/zw.ttf),
	url(res:///opt/sony/ebook/FONT/tt0011m_.ttf)
	url(res:///fonts/ttf/zw.ttf),
	url(res:///../../media/mmcblk0p1/fonts/zw.ttf),
	url(res:///DK_System/system/font/zw.ttf),
	url(res:///abook/fonts/zw.ttf),
	url(res:///system/fonts/zw.ttf),
	url(res:///system/media/sdcard/fonts/zw.ttf),
	url(res:///media/fonts/zw.ttf),
	url(res:///sdcard/fonts/zw.ttf),
	url(res:///system/fonts/DroidSansFallback.ttf),
	url(res:///mnt/MOVIFAT/font/zw.ttf),
	url(fonts/zw.ttf);
}
"""
SS_TO_BODY = """
body { font-family: 'zw', serif; }
"""

def processCSS(fName):
    f1 = open(fName,"r")
    fName2 = os.path.join(os.path.dirname(fName),"new_"+ os.path.basename(fName) )
    fName2 = os.path.normpath(fName2)
    print u"老的css文件：",fName
    print u"新的css文件",fName2

    f2 = open(fName2,"w")
    contents = f1.read()
    if "@font-face" in contents:
        start = contents.index("src:url")
        end = contents.find("}", start +1 )
        conts = contents[:start]+SS_TO_2 + contents[(end +1):]
        f2.write(conts)
        print "modify font_face successfully"

    else:
        f2.write(SS_TO)
        f2.write(SS_TO_2)
        f2.write(SS_TO_BODY)
        f2.write(contents)
        print "add font_face successfully"
        
    f1.close()
    f2.close()
    os.remove(fName)
    os.rename(fName2, fName)
    print u"离开css文件处理"
    print ""

def processEpub(oldFile):
    z = zipfile.ZipFile(oldFile,'a')
    fileCSS = filter(lambda x:x.endswith("css"), z.namelist())
    print fileCSS

    for fi in  fileCSS:
        if "url(res:///system/fonts/DroidSansFallback.ttf" in z.open(fi).read():
            print "already show Chinese OK"
            return


    workDir = oldFile[:-5] #".epub" 5 char
    z.extractall(workDir) 
    print u"工作目录：",workDir

    CSS2 = map(lambda x:os.path.normpath(os.path.join(workDir, x)), fileCSS)
    map(printIt, CSS2)
    map(processCSS, CSS2)
    newFile = os.path.join( os.path.dirname(oldFile),"nook_" + os.path.basename(oldFile))
    print u"建立目标文件", newFile
    zz = zipfile.ZipFile( newFile,"w",zipfile.ZIP_DEFLATED )

    #write to a new zip
    pwd=os.getcwd()
    os.chdir(workDir)
    print u"当前目录", os.getcwd();
    map(lambda x: zz.write(x),z.namelist() )
    print u"关闭目标文件"
    zz.close()
    os.chdir(pwd)
    shutil.rmtree(workDir)

def printIt(x):
    print x

if __name__ == "__main__":
    print sys.argv[1:]
    list_of_ = [glob.glob(x) for x in sys.argv[1:]] 
    ll = list(set(reduce(lambda m,n:m+n, list_of_)))
    map(processEpub, ll)

