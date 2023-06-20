import psutil
import time

def getProcessList():
    list = []
    for process in psutil.process_iter():
        try:
            name = process.name()
            if name == 'svchost.exe':
                pass
            else:
                list.append(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list

def startTime():
    start = time.time()
    return start

def endTime(czas):
    elapsed = (time.strftime('%H:%M:%S', time.gmtime(time.time() - czas)))
    return elapsed

