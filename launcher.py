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
import cli_support
from colorama import Fore,Style

packages.urllib3.disable_warnings()
Logger=Remilia.LiteLog.LiteLog("Launcher")
rootFiles=listdir()
Argv=sys.argv

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


if len(Argv) > 1:
    StartFile=Argv[1]
else:
    StartFile="script.py"

def runScript(text):
    try:
        exec(text)
        with open("Cache/cache.py","w") as f:
            f.write(text)
            
    except Exception as e:
        if isinstance(e,ImportError):
            Logger.error(e)
            input("请前往 [ https://github.com/IAXRetailer/MCreator_Setup ] 更新至最新Release版本,脚本所要求的库当前启动器无法提供")
        else:
            Logger.error(e)
            input("")
        if exists("Cache/cache.py"):
            Logger.info("检测到缓存中有能够使用的脚本,尝试重新启动中")
            with open("Cache/cache.py","r") as f:
                exec(f.read())


if "Cache" not in rootFiles:
    mkdir("Cache")
    mkdir("Cache/Logs")
    
if "Data" not in rootFiles:
    mkdir("Data")
    
if exists(StartFile):
    Logger.info("正在启动本地 [ %s ]" % StartFile)
    with open(StartFile,"r",encoding="utf-8") as string:
        scriptText=string.read()
else:
    scriptUri=InfoDict["script"]
    Logger.info("从 [ %s ] 拉取 [ script.py ] 并启动..." % scriptUri)
    Logger.info("如果下载失败可以前往上述网址下载文件,然后移动到本目录下重命名为 [ script.py ] ,最后重启此程序")
    try:
        resp=get(scriptUri,verify=False)
        scriptText=resp.text
    except Exception as e:
        Logger.error(e)
        exit()

runScript(scriptText)
Logger.writeAllLog("Cache/Logs/launcher.log")