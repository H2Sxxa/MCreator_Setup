from platform import platform
from json import loads
from tarfile import TarFile
from os import listdir,system
import sys
import traceback
import LiteLog
Logger=LiteLog.LiteLog(__name__)
class Utils():
    @staticmethod
    def make_choice():
        while True:
            Logger.info("是否确定(Y/N)")
            choice=input()
            if choice == "Y":
                return True
            if choice == "N":
                return False
    @staticmethod
    def getDownloadUri(key):
        with open("download.json","r",encoding="utf-8") as f:
            return loads(f.read())[key]
    @staticmethod
    def Download():
        system(r".\aria2c.exe -x16 -s4 -iDownloadList.txt")

class ErrorHooker:
    def __init__(self) -> None:
        sys.excepthook = self.Hooker
        
    def Hooker(self,*args):
        exc_type, exc_value, exc_traceback_obj = args
        Logger.error("Got a exception")
        Logger.error(exc_type)
        Logger.error(exc_value)
        Logger.error("Exception location\n"+"".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
        Logger.writeAllLog("crashreport.log")
        input()
        exit()

class PlatformCheck():
    def __init__(self) -> None:
        Logger.info("Check platform now...")
        platforminfo=platform()
        Logger.info(platforminfo)
        self.system,self.version,self.version2,self.serverpack=platform().split("-")
        if self.system != "Windows":
            Logger.info("暂不支持非Windows系统")
            input()
            exit()
    def need_netframework(self):
        if self.version == "7":
            Logger.info("win7需要下载 .NET Framework 4.8 否则Shadowsock无法运行")
            return True
        elif self.version == "10":
            Logger.warn("低于Windows 10 1903需要下载 .NET Framework 4.8 否则Shadowsock无法运行")
            Logger.warn("如果无法使用,自行下载安装 %s"% Utils.getDownloadUri("dnf"))
            return False
        else:
            return False
ErrorHooker()
with open("DownloadList.txt","w",encoding="utf-8") as DownloadList:
    LocationFile=listdir()
    task_setup_pro=False
    task_setup_ssr=False
    if "Proxifier.tar" not in LocationFile:
        task_setup_pro=True
        DownloadList.write(Utils.getDownloadUri("proxifier")+"\n")
    if "Shadowsockes.tar" not in LocationFile:
        task_setup_ssr=True
        DownloadList.write(Utils.getDownloadUri("shadowsocketes")+"\n")
    Platformck=PlatformCheck()
    if Platformck.need_netframework():
        task_setup_dnf=False
        Logger.info("下载 .NET Framework 4.8")
        if Utils.make_choice():
            task_setup_dnf=True
            DownloadList.write(Utils.getDownloadUri("dnf")+"\n")

Utils.Download()
if task_setup_dnf:
    system(r".\ndp48-x86-x64-allos-enu.exe")

if task_setup_pro:
    with TarFile("Proxifier.tar") as archive:
        archive.extractall()
        
if task_setup_ssr:
    with TarFile("Shadowsockes.tar") as archive:
        archive.extractall()