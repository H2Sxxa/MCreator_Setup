from json import loads
from tarfile import TarFile
from os import getcwd, listdir, makedirs, remove, rename,system,startfile,environ
from os.path import isdir,exists
from shutil import move
from requests import get
from requests import packages
import sys
import winreg
import traceback
import LiteLog
from colorama import Fore,Style
Logger=LiteLog.LiteLog(__name__)
Logger.info("手动配置教程位于https://zekerzhayard.gitbook.io/minecraft-forge-gou-jian-kai-fa-huan-jing-wang-luo-dai-li-pei-zhi-jiao-cheng ")
Logger.info("如果此程序出错请尝试手动配置")
Logger.info("如果你不知道干什么请优先观看控制台出现的日志,而不是前往提问")
Logger.warn("注意,运行此程序时请检查Shadowsockes,Proxifier以及MCreator是否关闭,以免带来一些不必要的麻烦")

class Utils():
    @staticmethod
    def get_release():
        packages.urllib3.disable_warnings()
        Logger.warn("连接api.github.com可能会出错如果遇到错误可稍后访问,也可以自行下载")
        Logger.info("snp代表快照(snapshot)版本,stb代表稳定(stable)版本")
        try:
            stable=[]
            snapshot=[]
            choicelist={}
            choice=""
            for i in map(Utils.extractsort,loads(get(Utils.getUri("github_mcrapi")+"/latest",verify=False).text)["assets"]):
                stable.append(i)
            for i in map(Utils.extractsort,loads(get(Utils.getUri("github_mcrapi"),verify=False).text)[0]["assets"]):
                snapshot.append(i)
            for i,j in zip(stable,range(len(stable))):
                print(Fore.LIGHTRED_EX+"stb%s"%j+" "+Fore.LIGHTGREEN_EX+i["name"]+Style.RESET_ALL)
                choicelist.update({"stb%s"%j:i["download"]})
            for i,j in zip(snapshot,range(len(snapshot))):
                print(Fore.LIGHTRED_EX+"snp%s"%j+" "+Fore.LIGHTGREEN_EX+i["name"]+Style.RESET_ALL)
                choicelist.update({"snp%s"%j:i["download"]})
            while choice not in choicelist:
                Logger.info("选择你需要的版本,然后输入前面的序号,例如stb1")
                Logger.info("如果你不知道下载哪个,请选择.exe结尾的版本")
                choice=input()
            return Utils.getUri("github_proxy")+choicelist[choice]
        except Exception as e:
            Logger.error(e)
            return ""
        
    @staticmethod
    def extractsort(jsonf:dict):
        return {"name":jsonf["name"],"download":jsonf["browser_download_url"]}
    
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
            Logger.info(Utils.getUri("jdk"))
            choice = input().lower()
            if choice in Utils.getUri("jdk"):
                return Utils.getUri(choice)
            
    @staticmethod
    def getUri(key):
        with open("download.json","r",encoding="utf-8") as f:
            return loads(f.read())[key]

    @staticmethod
    def Download():
        system(r".\aria2c.exe -x16 -s4 -iDownloadList.txt")

    @staticmethod
    def check_jdkpath(jdkpath,name):
        if name in listdir(jdkpath):
            remove(jdkpath+"/"+name)
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
        Logger.error("错误日志已保存到crashreport.log")
        Logger.info("如果你看不懂这个崩溃报告可以前往 https://github.com/IAXRetailer/MCreator_Setup/issues 点击「New issue」")
        input()
        exit()

class PlatformCheck():
    def __init__(self) -> None:
        Logger.info("检查注册表中...")
    def need_netframework(self):
        try:
            if "4.8" in winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full"),"Version")[0]:
                return False
        except:
            return True
ErrorHooker()
with open("DownloadList.txt","w",encoding="utf-8") as DownloadList:
    Logger.info("您是否为MCreator用户")
    Logger.info("如果已经下好JDK并且下好MCreator可以输入N跳过此步")
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
        if Ijdk == Utils.getUri("jdk8"):
            usejdk=8
            if "OpenJDK8U-jdk_x64_windows_hotspot_8u312b07.zip" not in LocationFile:
                DownloadList.write(Ijdk+"\n")
                
        if Ijdk == Utils.getUri("jdk16"):
            usejdk=16
            if "OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip" not in LocationFile:
                DownloadList.write(Ijdk+"\n")
                
        if Ijdk == Utils.getUri("jdk17"):
            usejdk=17
            if "OpenJDK17U-jdk_x64_windows_hotspot_17.0.1_12.zip" not in LocationFile:
                DownloadList.write(Ijdk+"\n")
                
        Logger.info("是否需要同时下载MCreator")
        Logger.info("已安装或者下载好了可以输入N跳过此步")
        if Utils.make_choice():
            DownloadList.write(Utils.get_release()+"\n")
            Logger.info("MCreator下载后会存放到%s,请自行安装" % getcwd())
            
    if "ProxifierSetup.tar" not in LocationFile:
        task_setup_pro=True
        DownloadList.write(Utils.getUri("proxifier")+"\n")
        
    if "Shadowsockes.tar" not in LocationFile:
        task_setup_ssr=True
        DownloadList.write(Utils.getUri("shadowsocketes")+"\n")
        
    Platformck=PlatformCheck()
    if Platformck.need_netframework():
        task_setup_dnf=False
        Logger.info("注册表内没有发现.NET 4.8")
        Logger.info("已将.NET Framework 4.8加入下载列表")
        task_setup_dnf=True
        DownloadList.write(Utils.getUri("dnf")+"\n")
    else:
        task_setup_dnf=False
Utils.Download()

if use_mcr:
    jdkpath=environ["USERPROFILE"]+"\.mcreator\gradle\jdks"
    if not exists(environ["USERPROFILE"]+"\.mcreator\gradle\jdks"):
        makedirs(environ["USERPROFILE"]+"\.mcreator\gradle\jdks")
    Logger.info("移动jdk中...")
    if usejdk == 8:
        rename("OpenJDK8U-jdk_x64_windows_hotspot_8u312b07.zip","adoptopenjdk-8-x64-windows.zip")
        Utils.check_jdkpath(jdkpath,"adoptopenjdk-8-x64-windows.zip")
        move("adoptopenjdk-8-x64-windows.zip",jdkpath)
    if usejdk == 16:
        rename("OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip","adoptopenjdk-16-x64-windows.zip")
        Utils.check_jdkpath(jdkpath,"adoptopenjdk-16-x64-windows.zip")
        move("adoptopenjdk-16-x64-windows.zip",jdkpath)
    if usejdk == 17:
        rename("OpenJDK17U-jdk_x64_windows_hotspot_17.0.1_12.zip","adoptopenjdk-17-x64-windows.zip")
        Utils.check_jdkpath(jdkpath,"adoptopenjdk-17-x64-windows.zip")
        move("adoptopenjdk-17-x64-windows.zip",jdkpath)

if task_setup_dnf:
    system(r".\ndp48-x86-x64-allos-enu.exe /q /norestart")

if task_setup_ssr:
    Logger.info("安装SSR...")
    with TarFile("Shadowsockes.tar") as archive:
        archive.extractall()
else:
    if exists("Shadowsockes") and isdir("Shadowsockes"):
        pass
    else:
        with TarFile("Shadowsockes.tar") as archive:
            archive.extractall()
if exists("C:/Program Files (x86)/Proxifier/Proxifier.exe"):
    task_setup_pro=False
else:
    task_setup_pro=True
if task_setup_pro:
    Logger.info("安装Proxifier...")
    with TarFile("ProxifierSetup.tar") as archive:
        archive.extractall()
    system(r"start .\ProxifierSetup.exe /silent")
    key=winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Initex\Proxifier\License")
    winreg.SetValueEx(key,"Owner",0,winreg.REG_SZ,"H2Sxxa")
    winreg.SetValueEx(key,"Key",0,winreg.REG_SZ,"5EZ8G-C3WL5-B56YG-SCXM9-6QZAP")
Logger.info("启动Proxifier...")
system("start \"C:/Program Files (x86)/Proxifier/Proxifier.exe\" ./Minecraft.ppx silent-load")
Logger.info("启动SSR...")
startfile(r".\Shadowsockes\Shadowsocks.exe")

Logger.info("至此已经完成所有步骤,如果你是MCreator用户,请重新启动MCreator,等待构建成功...如果失败,点击re-setup多试几遍,期间不要关闭Shadowsockes和proxifier")
input()