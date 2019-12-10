from subprocess import check_output
import time
import os

def checkDiskUtil():
    output = check_output("df -h", shell=True)
    for line in str(output).split("\\n"):
        if line.find("/opt") > 0:
            lineParts = line.split()
    utilPercent = int(lineParts[4].strip("%"))
    return utilPercent
while True:
    inUse = checkDiskUtil()
    if inUse > 95:
        capFile = {}
        for name in os.listdir("/opt"):
            if name.startswith("capture-"):
                st=os.stat('/opt/' + name)    
                mtime=st.st_mtime
                capFile[name] = int(mtime)
        sortedFilesByDate = (sorted(capFile.items(), key = lambda kv:(kv[1], kv[0])))
        for key, val in sortedFilesByDate:
            check_output("rm /opt/" + key, shell=True)
            inUse = checkDiskUtil()
            if inUse <= 95:
                break
    time.sleep(60)
