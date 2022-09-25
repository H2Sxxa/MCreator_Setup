from json import loads
from tarfile import TarFile
from os import getcwd, listdir, makedirs, remove, rename,system,startfile,environ
from os.path import isdir,exists
from shutil import move
from urllib import request
from requests import get
from requests import packages
import sys
import winreg
import traceback
import Remilia
from colorama import Fore,Style

def getJsonKV(key):
    with open("download.json","r",encoding="utf-8") as jsontext:
        return loads(jsontext.read())[key]

script=getJsonKV("script")
Logger=Remilia.LiteLog.LiteLog("Launcher")
packages.urllib3.disable_warnings()
if "script.py" in listdir():
    Logger.warn("正在启动本地 [ script.py ] ,如果需要保持程序的持续更新,建议删除此文件")
    with open("script.py","r",encoding="utf-8") as string:
        exec(string.read())
else:
    Logger.info("从 [ %s ] 拉取 [ script.py ] 并启动..."%script)
    Logger.info("如果下载失败可以前往上述网址下载文件,然后移动到本目录下重命名为 [ script.py ] ,最后重启此程序")
    try:
        resp=get(script,verify=False)
    except Exception as e:
        Logger.error(e)
        exit()
    exec(resp.text)
