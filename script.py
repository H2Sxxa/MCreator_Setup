from json import loads
from tarfile import TarFile
from os import getcwd, listdir, makedirs, mkdir, remove, rename,system,startfile,environ
from os.path import isdir,exists
from shutil import move
from urllib import request
from requests import get
from requests import packages
import sys
import winreg
import traceback
import Remilia
from cli_support import prompts,utils
from colorama import Fore,Style

rootFiles=listdir()
Logger=Remilia.LiteLog.LiteLog(__name__)
Logger.info("手动配置教程位于https://zekerzhayard.gitbook.io/minecraft-forge-gou-jian-kai-fa-huan-jing-wang-luo-dai-li-pei-zhi-jiao-cheng ")
Logger.info("如果此程序出错请尝试手动配置")
InfoDict={
    "jdk8":"https://ghproxy.com/https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U-jdk_x64_windows_hotspot_8u312b07.zip",
    "jdk16":"https://ghproxy.com/https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip",
    "jdk17":"https://ghproxy.com/https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U-jdk_x64_windows_hotspot_17.0.1_12.zip",
    "dnf":"https://download.visualstudio.microsoft.com/download/pr/2d6bb6b2-226a-4baa-bdec-798822606ff1/8494001c276a4b96804cde7829c04d7f/ndp48-x86-x64-allos-enu.exe",
    "shadowsocketes":"https://ghproxy.com/https://github.com/IAXRetailer/MCreator_Setup/blob/main/Shadowsockes.tar",
    "proxifier":"https://ghproxy.com/https://github.com/IAXRetailer/MCreator_Setup/blob/main/ProxifierSetup.tar",
    "proxifierConfig":"https://ghproxy.com/https://github.com/IAXRetailer/MCreator_Setup/blob/main/Minecraft.ppx",
    "github_mcrapi":"https://api.github.com/repos/MCreator/MCreator/releases",
    "github_proxy":"https://ghproxy.com/",
    "script":"https://ghproxy.com/https://raw.githubusercontent.com/IAXRetailer/MCreator_Setup/main/script.py"
}



BrightStyle=prompts.Style.from_dict({
        "questionmark": "ansibrightred bold",
        "question": "ansibrightgreen",
        "sign": "",
        "unsign": "",
        "selected": "",
        "pointer": "bold",
        "annotation": "bold",
        "answer": "bold",
})


ListPromptAnce="（使用 ↑ 和 ↓ 选择，ENTER 确认）"
CheckBoxPromptAnce="（使用 ↑ 和 ↓ 选择，SPACE 选中，ENTER 确认）"
downloadUrls=[]

def MakeChoice(question=""):
    global prompts,ListPromptAnce,BrightStyle
    return prompts.ListPrompt(
        question=question,
        choices=[
            prompts.Choice("是",True),
            prompts.Choice("否",False)
                ],
        annotation=ListPromptAnce,
        ).prompt(style=BrightStyle).data

def MakeCheck(question="",choices=[]):
    global prompts,CheckBoxPromptAnce,BrightStyle
    return prompts.CheckboxPrompt(
        question=question,
        choices=choices,
        annotation=CheckBoxPromptAnce,
        ).prompt(style=BrightStyle)

def check_jdkpath(jdkpath,name):
    if name in listdir(jdkpath):
        remove(jdkpath+"/"+name)

def get_release():
    result=[]
    try:
        for i in loads(get(InfoDict["github_mcrapi"]+"/latest",verify=False).text)["assets"]:
            result.append(prompts.Choice(name="%s(稳定版)"%i["name"],data=InfoDict["github_proxy"]+i["browser_download_url"]))
        for i in loads(get(InfoDict["github_mcrapi"],verify=False).text)[0]["assets"]:
            result.append(prompts.Choice(name="%s(快照版)"%i["name"],data=InfoDict["github_proxy"]+i["browser_download_url"]))
        for i in loads(get("https://api.github.com/repos/cdc12345/MCreator-Chinese/releases/latest",verify=False).text)["assets"]:
            result.append(prompts.Choice(name="%s(中文版(cdc12345/MCreator-Chinese))"%i["name"],data=InfoDict["github_proxy"]+i["browser_download_url"]))
        return result
    except Exception as e:
        Logger.error(e)
        if MakeChoice("拉取失败是否重试"):
            return get_release()
        else:
            return [prompts.Choice(name="拉取失败,跳过并自行下载",data="")]
    
class PlatformCheck():
    def __init__(self) -> None:
        Logger.info("检查注册表中...")
    def need_netframework(self):
        try:
            if "4.8" in winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full"),"Version")[0]:
                return False
            else:
                return True
        except:
            return True
        
class ErrorHooker:
    def __init__(self) -> None:
        sys.excepthook = self.Hooker
        
    def Hooker(self,*args):
        exc_type, exc_value, exc_traceback_obj = args
        Logger.error("Got a exception")
        Logger.error(exc_type)
        Logger.error(exc_value)
        Logger.error("Exception location\n"+"".join(traceback.format_exception(exc_type, exc_value, exc_traceback_obj)))
        Logger.writeAllLog("Cache/Logs/script.log")
        Logger.error("错误日志已保存到Cache/Logs/script.log")
        Logger.info("如果你看不懂这个崩溃报告可以前往 https://github.com/IAXRetailer/MCreator_Setup/issues 点击「New issue」提交此日志")
        input()
        exit()
        
if PlatformCheck().need_netframework():
    downloadUrls.append(InfoDict["dnf"])
    needinstalldnf=True
    Logger.info("注册表内没有发现.NET 4.8")
    Logger.info("已将.NET Framework 4.8加入下载列表")
else:
    needinstalldnf=False
    
ErrorHooker()
if MakeChoice("您是否为MCreator用户"):
    usemcr=True
    usejdk=MakeCheck(
        question="使用哪几种JDK",
        choices=[                            
            prompts.Choice("JDK8（适用于 Minecraft 1.16.5 或更旧版本）",InfoDict["jdk8"]),
            prompts.Choice("JDK16（适用于 Minecraft 1.17.x）",InfoDict["jdk16"]),
            prompts.Choice("JDK17（适用于 Minecraft 1.18 或更新版本）",InfoDict["jdk17"])
                ]
        )
    jdks=[_.data for _ in usejdk]
    
    if MakeChoice("是否下载MCreator"):
        downloadUrls.extend([_.data for _ in MakeCheck(question="下载哪几种MCreator(下载到本目录后需自行安装)",choices=get_release())])
    
    downloadUrls.extend(jdks)
else:
    usemcr=False

if "ProxifierSetup.tar" not in rootFiles:
    downloadUrls.append(InfoDict["proxifier"])
    
if "Shadowsockes.tar" not in rootFiles and not exists("Shadowsockes"):
    task_setup_ssr=True
    downloadUrls.append(InfoDict["shadowsocketes"])
else:
    if not exists("Shadowsockes"):
        task_setup_ssr=True
    else:
        task_setup_ssr=False

if "Minecraft.ppx" not in rootFiles:
    downloadUrls.append(InfoDict["proxifierConfig"])

with open("Cache/download.txt","w",encoding="utf-8") as dld:
    dld.write("\n".join(downloadUrls))

system(r".\aria2c.exe -x16 -s4 -iCache/download.txt")

if usemcr:
    jdkpath=environ["USERPROFILE"]+"\.mcreator\gradle\jdks"
    if not exists(environ["USERPROFILE"]+"\.mcreator\gradle\jdks"):
        makedirs(environ["USERPROFILE"]+"\.mcreator\gradle\jdks")
    Logger.info("移动jdk中...")
    if InfoDict["jdk8"] in jdks:
        rename("OpenJDK8U-jdk_x64_windows_hotspot_8u312b07.zip","adoptopenjdk-8-x64-windows.zip")
        check_jdkpath(jdkpath,"adoptopenjdk-8-x64-windows.zip")
        move("adoptopenjdk-8-x64-windows.zip",jdkpath)
    if InfoDict["jdk16"] in jdks:
        rename("OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip","adoptopenjdk-16-x64-windows.zip")
        check_jdkpath(jdkpath,"adoptopenjdk-16-x64-windows.zip")
        move("adoptopenjdk-16-x64-windows.zip",jdkpath)
    if InfoDict["jdk17"] in jdks:
        rename("OpenJDK17U-jdk_x64_windows_hotspot_17.0.1_12.zip","adoptopenjdk-17-x64-windows.zip")
        check_jdkpath(jdkpath,"adoptopenjdk-17-x64-windows.zip")
        move("adoptopenjdk-17-x64-windows.zip",jdkpath)

if needinstalldnf:
    Logger.info("开始安装.NET 4.8...")
    system(r".\ndp48-x86-x64-allos-enu.exe /q /norestart")
    Logger.info("安装完成")

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
    if "ProxifierSetup.exe" not in rootFiles:
        with TarFile("ProxifierSetup.tar") as archive:
            archive.extractall()
    system(r"start .\ProxifierSetup.exe /silent")
    try:
        key=winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Initex\Proxifier\License")
        winreg.SetValueEx(key,"Owner",0,winreg.REG_SZ,"H2Sxxa")
        winreg.SetValueEx(key,"Key",0,winreg.REG_SZ,"5EZ8G-C3WL5-B56YG-SCXM9-6QZAP")
    except Exception as e:
        Logger.error(e)
        Logger.info("尝试仅注册当前用户...")
        try:
            key=winreg.CreateKey(winreg.HKEY_CURRENT_USER,r"Software\Initex\Proxifier\License")
            winreg.SetValueEx(key,"Owner",0,winreg.REG_SZ,"H2Sxxa")
            winreg.SetValueEx(key,"Key",0,winreg.REG_SZ,"5EZ8G-C3WL5-B56YG-SCXM9-6QZAP")
        except Exception as e:
            Logger.error(e)
            Logger.error("自动注册失败,可能需要管理员权限")
            Logger.error("你可以尝试手动注册")
            Logger.error("启动proxifier,如果需要秘钥选择第二个按钮")
            Logger.error("第一个文本框随便写,第二个文本框输入「5EZ8G-C3WL5-B56YG-SCXM9-6QZAP」,然后选择「All users on this computer (require administrator)」单选框,最后单击「OK」按钮")
            Logger.error("完成后回车")
            input()
            
Logger.info("启动Proxifier...")
system("start \"C:/Program Files (x86)/Proxifier/Proxifier.exe\" ./Minecraft.ppx silent-load")
Logger.info("启动SSR...")
startfile(r".\Shadowsockes\Shadowsocks.exe")

Logger.info("至此已经完成所有步骤,如果你是MCreator用户,请重新启动MCreator,等待构建成功...如果失败,点击re-setup多试几遍,期间不要关闭Shadowsockes和proxifier")
input()