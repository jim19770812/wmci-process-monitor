import os
import subprocess
from typing import Dict, Set
import argparse
import time
from datetime import datetime

def run(name:str, f, pids:Set)->Dict[str, str]:
    result={}
    command =f"C:\Windows\System32\wbem\WMIC.exe process where caption='{name}' get processid,caption,commandline /format:CSV"
    #print(command)
    process=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    current_pid:str=str(os.getpid())
    while True:
        line=process.stdout.readline().decode().rstrip()
        if line == '' and process.poll() != None:
            break
        datas=line.split(",")
        if datas[0] in ['','Node'] or datas[3]==current_pid: continue
        if datas[3] not in pids:
            pids.add(datas[3])
            dt=datetime.now().strftime("%H:%M:%S")
            s=f"{dt}\t{datas[3]}\t{datas[2]}"
            print(s)
            if f:
                f.write(f"{s}\n")
                f.flush()
    process.stdout.close()
    process.wait()
    return result


if __name__=="__main__":
    parse=argparse.ArgumentParser("持续进程监控工具")
    parse.add_argument("--caption", type=str, default='', required=True, help="要监控的进程进程的完整映像名")
    parse.add_argument("--output", type=str, default='', required=False, help="输出日志文件，可选")
    args=parse.parse_args()
    pids=set()
    f = open(args.output, 'w') if args.output else None
    try:
        while True:
            run(args.caption, f, pids)
            time.sleep(0.001)
    finally:
        if f: f.close()
