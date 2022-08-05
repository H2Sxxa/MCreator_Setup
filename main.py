from platform import platform
from json import loads
from tarfile import TarFile
from os import listdir, rename,system,startfile
from shutil import move
from tkinter.filedialog import askdirectory
import sys
import traceback
import LiteLog
Logger=LiteLog.LiteLog(__name__)
Logger.info("手动配置教程位于https://zekerzhayard.gitbook.io/minecraft-forge-gou-jian-kai-fa-huan-jing-wang-luo-dai-li-pei-zhi-jiao-cheng ")
Logger.info("如果此程序出错请尝试手动配置")
class Utils():
    @staticmethod
    def make_choice():
        while True:
            Logger.info("是否确定(Y/N)")
            choice=input().upper()
            if choice == "Y":
                return True
            if choice == "N":
                return False
    @staticmethod
    def chose_jdk():
        while True:
            Logger.info("从中选择一个JDK版本")
            Logger.info(Utils.getDownloadUri("jdk"))
            choice = input().lower()
            if choice in Utils.getDownloadUri("jdk"):
                return Utils.getDownloadUri(choice)
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
    Logger.info("您是否为MCreator用户")
    LocationFile=listdir()
    task_setup_pro=False
    task_setup_ssr=False
    use_mcr=False
    if Utils.make_choice():
        use_mcr=True
        Logger.info("选择jdk版本")
        Logger.info("jdk8 适用于 Minecraft 1.16.5 或更旧版本")
        Logger.info("jdk16 适用于 Minecraft 1.17.x")
        Logger.info("jdk17 适用于 Minecraft 1.18 或更新版本")
        Ijdk=Utils.chose_jdk()
        if Ijdk == Utils.getDownloadUri("jdk8"):
            usejdk=8
            if "OpenJDK8U-jdk_x64_windows_hotspot_8u312b07.zip" not in LocationFile:
                DownloadList.write(Ijdk+"\n")
                
        if Ijdk == Utils.getDownloadUri("jdk16"):
            usejdk=16
            if "OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip" not in LocationFile:
                DownloadList.write(Ijdk+"\n")
                
        if Ijdk == Utils.getDownloadUri("jdk17"):
            usejdk=17
            if "OpenJDK17U-jdk_x64_windows_hotspot_17.0.1_12.zip" not in LocationFile:
                DownloadList.write(Ijdk+"\n")
    if "ProxifierSetup.tar" not in LocationFile:
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
    else:
        task_setup_dnf=False
Utils.Download()
if use_mcr:
    Logger.info(r"请手动选择C:\Users\<你的用户名>\.mcreator\gradle\jdks目录")
    Logger.info("没有这个目录手动创建,有此目录建议清空")
    if usejdk == 8:
        rename("OpenJDK8U-jdk_x64_windows_hotspot_8u312b07.zip","adoptopenjdk-8-x64-windows.zip")
        move("adoptopenjdk-8-x64-windows.zip",askdirectory())
    if usejdk == 16:
        rename("OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip","adoptopenjdk-16-x64-windows.zip")
        move("adoptopenjdk-16-x64-windows.zip",askdirectory())
    if usejdk == 17:
        rename("OpenJDK17U-jdk_x64_windows_hotspot_17.0.1_12.zip","adoptopenjdk-17-x64-windows.zip")
        move("adoptopenjdk-17-x64-windows.zip",askdirectory())
        
if task_setup_dnf:
    system(r".\ndp48-x86-x64-allos-enu.exe")

if task_setup_ssr:
    with TarFile("Shadowsockes.tar") as archive:
        archive.extractall()
else:
    Logger.info("是否已经解压Shadowsockes.tar")
    if Utils.make_choice():
        pass
    else:
        with TarFile("Shadowsockes.tar") as archive:
            archive.extractall()

if task_setup_pro:
    with TarFile("ProxifierSetup.tar") as archive:
        archive.extractall()
    startfile(r".\ProxifierSetup.exe")
    Logger.warn("请勿修改软件安装位置")
    Logger.info("如果提示需要注册秘钥")
    Logger.info("第一个文本框随便写，第二个文本框输入「5EZ8G-C3WL5-B56YG-SCXM9-6QZAP」，然后选择「All users on this computer (require administrator)」单选框，最后单击「OK」按钮")
    Logger.info("全部安装完成后回车")
    input()
else:
    Logger.info("是否已经安装Proxifier")
    if Utils.make_choice():
        pass
    else:
        with TarFile("ProxifierSetup.tar") as archive:
            archive.extractall()
        startfile(r".\ProxifierSetup.exe")
        Logger.warn("请勿修改软件安装位置")
        Logger.info("如果提示需要注册秘钥")
        Logger.info("第一个文本框随便写，第二个文本框输入「5EZ8G-C3WL5-B56YG-SCXM9-6QZAP」，然后选择「All users on this computer (require administrator)」单选框，最后单击「OK」按钮")
        Logger.info("全部安装完成后回车")
        input()
try:
    startfile("\"C:\Program Files (x86)\Proxifier\Proxifier.exe\"")
except:
    Logger.error("自动启动Proxifier失败,尝试手动启动Proxifier")

try:
    startfile(r".\Shadowsockes\Shadowsocks.exe")
except:
    Logger.error("自动启动Shadowsocks失败,尝试手动启动Shadowsocks")
try:
    startfile(r".\Minecraft.ppx")
    Logger.info("自动导入成功,如果遇到提示点击确定/continue")
except:
    Logger.error("自动导入配置失败,尝试手动将程序目录下Minecraft.ppx导入Proxifier")
Logger.info("如果Proxifier配置文件没有导入成功,尝试以下步骤")
Logger.info("依次选择左上角「File」—「Import Profile...」")
Logger.info("选择程序下Minecraft.ppx导入")
Logger.info("至此已经完成所有步骤,重新启动MCreator,等待构建成功!")
input()