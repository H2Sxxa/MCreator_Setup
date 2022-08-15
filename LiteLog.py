from abc import ABC, abstractmethod
import sys
from colorama import Fore,Style,init
from time import strftime,localtime
import platform

class __LiteLog(ABC):
    @abstractmethod
    def __init__(self) -> None:
        '''
        Logger = LiteLog(__name__)
        '''
    @abstractmethod
    def setColor(self,loglevel:str,color:Fore) -> Fore:
        '''
        if success , it will return the color of the loglevel\n
        Logger.setColor("INFO",Fore.GREEN)
        '''
    @abstractmethod
    def setTimeFormat(self,timeformat:str) -> str:
        '''
        if success , it will return the format of the time\n
        Logger.info(1)\n
        Logger.setTimeFormat("%H_%M_%S")\n
        Logger.info(1)\n
        >>>[ INFO | __main__ | 12:34:56 ] 1\n
        >>>[ INFO | __main__ | 12_34_56 ] 1
        '''
    @abstractmethod
    def setLogFormat(self,logformat:str) -> str:
        '''
        if success , it will return the format of the log\n
        Logger.info(1)\n
        Logger.setLogFormat("( $infolevel$ | $name$ | $time$ ) $msg$")\n
        Logger.info(1)\n
        >>>[ INFO | __main__ | 12:34:56 ] 1\n
        >>>( INFO | __main__ | 12_34_56 ) 1
        '''
        
    @abstractmethod
    def info(self,msg:any) -> None:
        pass
    
    @abstractmethod
    def warn(self,msg:any) -> None:
        pass
    
    @abstractmethod
    def error(self,msg:any) -> None:
        pass
    
    @abstractmethod
    def debug(self,msg:any) -> None:
        pass
    
    @abstractmethod
    def stdout(*values: object,sep,end,file,flush) -> None:
        '''
        just a print method\n
        print=Logger.stdout
        '''
    
    @abstractmethod
    def getCustomLastlog(self,key:str) -> str:
        '''
        if you want to print it in function, use *lastCustomlog in function args
        '''
    
    @abstractmethod
    def openDebug(self,key:str) -> None:
        '''
        key:stdout,write
        '''

    @abstractmethod
    def closeDebug(self,key:str) -> None:
        '''
        key:stdout,write
        '''
    @abstractmethod
    def debughere(self,keylist):
        '''
        a decorator for easy debug
        '''
    @abstractmethod
    def writeAllLog(self,logpath:str) -> None:
        '''
        write all the log in logpath
        '''
                
    @abstractmethod
    def openWriteStream(self,logpath:str) -> None:
        '''
        keep writing the log in info/warn/error\n
        use closeWriteStream to stop it
        '''
    @abstractmethod
    def closeWriteStream(self,logpath="") -> None:
        '''
        close the write stream
        '''
    
    @abstractmethod
    def apply_logtype(self,key) -> None:
        '''
        append it to __log
        '''
    
    @abstractmethod 
    def apply_logfunc(self,key:str,scope:str,func,*args,**kwargs)-> None:
        '''
        use apply_logtype first\n
        "key":"",\n
        "scope":"", stdout\n
        "func":None,\n
        "args":None,\n
        "kwargs":None
        '''
    
    @abstractmethod 
    def apply_logformat(self,key,color,log) -> None:
        '''
        use apply_logtype first\n
        "key":"",\n
        "color":{\n
            "INFO":Fore.GREEN,\n
            "WARN":Fore.YELLOW,\n
            "ERROR":Fore.RED,\n
            "DEBUG":Fore.CYAN,\n
            "TEXT":Style.RESET_ALL\n
        },
        "log":"[ $infolevel$ | $name$ | $time$ ] $msg$",
        '''
    
    
class LiteLog(__LiteLog):
    def __init__(self,name=__name__) -> None:
        super().__init__()
        self.Oriprint = print
        if platform.system() == "Windows":
            init(True)
            
        self.__log={
            "plainlog":[],
            "forelog":[]
                    }
        self.__debug={
            "stdout":False,
            "write":False
        }
        self.__name=name
        self.__writeStreamList=[]
        self.__format={
            "log":"[ $infolevel$ | $name$ | $time$ ] $msg$",
            "time":"%H:%M:%S"
            }
        self.__color={
            "INFO":Fore.GREEN,
            "STDOUT":Fore.GREEN,
            "WARN":Fore.YELLOW,
            "ERROR":Fore.RED,
            "DEBUG":Fore.CYAN,
            "TEXT":Style.RESET_ALL
        }

        self.__customfunc=[]
        
        self.__customformat=[]
        
        
    def setColor(self,loglevel,color):
        super().setColor()
        loglevel=loglevel.upper()
        self.__color[loglevel]=color
        return self.__color[loglevel]

    def setTimeFormat(self,timeformat):
        super().setTimeFormat()
        self.__format["time"]=timeformat
        return self.__format["time"]

    def setLogFormat(self,logformat):
        super().setLogFormat()
        self.__format["log"]=logformat
        return self.__format["log"]

    def __stdoutHandle(func):
        def stdout_warpper(self,*values: object,**kwargs):
            fore_stdout=(
                self.__color[func.__name__.upper()]
                +self.__format["log"]
                .replace("$infolevel$",func.__name__.upper())
                .replace("$time$",self.getTime)
                .replace("$name$",self.__name)
                .replace("$msg$",self.__color["TEXT"])
                )
            plain_stdout=(
                self.__format["log"]
                .replace("$infolevel$",func.__name__.upper())
                .replace("$time$",self.getTime)
                .replace("$name$",self.__name)
                .replace("$msg$","")
                )
            self.Oriprint(fore_stdout,*values,**kwargs)
            values=map(str,values)
            self.plainlog.append(plain_stdout+"".join(values))
            self.forelog.append(fore_stdout+"".join(values))
            self.__writeStream()
        def common_warpper(self,msg):
            fore_stdout=(
                self.__color[func.__name__.upper()]
                +self.__format["log"]
                .replace("$infolevel$",func.__name__.upper())
                .replace("$time$",self.getTime)
                .replace("$name$",self.__name)
                .replace("$msg$",self.__color["TEXT"]+"%s" % msg)
                )
            plain_stdout=(
                self.__format["log"]
                .replace("$infolevel$",func.__name__.upper())
                .replace("$time$",self.getTime)
                .replace("$name$",self.__name)
                .replace("$msg$","%s" % msg)
                )
            
            if func.__name__.upper() != "DEBUG":
                self.Oriprint(fore_stdout)
                self.plainlog.append(plain_stdout)
                self.forelog.append(fore_stdout)
                self.__writeStream()
                
            elif self.__debug["stdout"] == True:
                self.Oriprint(fore_stdout)
                
            if self.__debug["write"] == True:
                self.plainlog.append(plain_stdout)
                self.forelog.append(fore_stdout)
                self.__writeStream()

            for csmlogshandle in self.__customformat:
                self.__log[csmlogshandle["key"]].append(
                    csmlogshandle["color"][func.__name__.upper()]+
                    csmlogshandle["log"]
                    .replace("$infolevel$",func.__name__.upper())
                    .replace("$time$",self.getTime)
                    .replace("$name$",self.__name)
                    .replace("$msg$",csmlogshandle["color"]["TEXT"]+"%s" % msg)
                )

            for csmfunchandle in self.__customfunc:
                if csmfunchandle["scope"] == "stdout":
                    finargs=[]
                    for arg in csmfunchandle["args"]:
                        if type(arg) == str:
                            if "*lastCustomlog" in arg:
                                arg=arg.replace("*lastCustomlog",self.getCustomLastlog(csmfunchandle["key"]))
                        finargs.append(arg)
                    csmfunchandle["func"](*tuple(finargs),**csmfunchandle["kwargs"])
            return func
        if func.__name__ != "stdout":
            return common_warpper
        else:
            return stdout_warpper

    @__stdoutHandle
    def info(self,msg):
        super().info(msg)
    
    @__stdoutHandle
    def warn(self,msg):
        super().warn(msg)

    @__stdoutHandle
    def error(self,msg):
        super().error(msg)
        
    @__stdoutHandle
    def debug(self,msg):
        super().debug(msg)
    
    @__stdoutHandle
    def stdout(*values: object,sep=' ',end='\n',file=sys.stdout,flush=False):
        super().stdout(*values,sep=' ',end='\n',file=sys.stdout,flush=False)
    
    def openDebug(self,key):
        super().openDebug(key)
        self.__debug[key]=True
        
    def closeDebug(self,key):
        super().closeDebug(key)
        self.__debug[key]=False
    
    def debughere(self,keylist):
        def outter(func):
            def warpper(*args,**kwargs):
                for key in keylist:
                    self.openDebug(key)
                func(*args,**kwargs)
                for key in keylist:
                    self.closeDebug(key)
            return warpper
        return outter
    @property
    def plainlog(self):
        return self.__log["plainlog"]
    
    @property
    def forelog(self):
        return self.__log["forelog"]
    
    @property
    def lastplainlog(self):
        if len(self.__log["plainlog"]) == 0:
            return
        return self.__log["plainlog"][-1]
    
    @property
    def lastforelog(self):
        if len(self.__log["forelog"]) == 0:
            return
        return self.__log["forelog"][-1]

    @property
    def getTime(self):
        return strftime(self.__format["time"], localtime())
    
    @property
    def autoLogName(self):
        return "%s.log" % strftime("%Y%m%d%H%M%S")

    def getCustomLastlog(self,key):
        super().getCustomLastlog(key)
        try:
            return self.__log[key][-1]
        except Exception as e:
            return str(e)
    
    def writeAllLog(self,logpath=""):
        if logpath == "":
            logpath = self.autoLogName
        with open(logpath,"w",encoding="utf-8") as f:
            for log in self.__log["plainlog"]:
                f.write(log+"\n")

    def openWriteStream(self,logpath=""):
        try:
            open(logpath,"w",encoding="utf-8")
        except Exception as e:
            self.error(e)
            return
        self.__writeStreamList.append(logpath)
        
    def closeWriteStream(self,logpath=""):
        try:
            self.__writeStreamList.remove(logpath)
        except Exception as e:
            self.error(e)
            return
    
    def __writeStream(self):
        if self.__writeStreamList == []:
            pass
        else:
            for writein in self.__writeStreamList:
                with open(writein,"a",encoding="utf-8") as f:
                    f.write(self.lastplainlog+"\n")
                f.close()

    def apply_logtype(self,key):
        super().apply_logtype(key)
        self.__log.update({key:[]})

    def apply_logfunc(self,key,scope,func,*args,**kwargs):
        super().apply_logfunc(key,scope,func,*args,**kwargs)
        self.__customfunc.append({"key":key,"scope":scope,"func":func,"args":args,"kwargs":kwargs})
        
    def apply_logformat(self,key,color,log):
        super().apply_logformat(key,color,log)
        self.__customformat.append({"key":key,"color":color,"log":log})