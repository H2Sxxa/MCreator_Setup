
from os import system
from tarfile import TarFile
import winreg


with TarFile("ProxifierSetup.tar") as archive:
    archive.extractall()
system(r"start .\ProxifierSetup.exe /silent")
key=winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Initex\Proxifier\License")
winreg.SetValueEx(key,"Owner",0,winreg.REG_SZ,"H2Sxxa222")
winreg.SetValueEx(key,"Key",0,winreg.REG_SZ,"5EZ8G-C3WL5-B56YG-SCXM9-6QZAP")