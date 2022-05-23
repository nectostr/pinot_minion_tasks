"""
Module that set's up the pcap files data collection
"""
from returns.result import Result, Success, Failure

import subprocess
from typing import Optional


def start_collecting(dump_folder: str, arguments: str) -> str:
    """
    Function that starts data collection
    :param dump_folder: foldr to save data to
    :param arguments: string with additional arguments for colelction
    :return:
    """
    proc = subprocess.Popen(f"tcpdump {arguments} -w {dump_folder}", shell=True)
    return f"tcpdump started to '{dump_folder}' with <{proc.pid}>"

def stop_collecting(pid: Optional[int]=None) -> Result[str, str]:
    """
    Kills either all tcpdump procc, or the one, that mentioned in agrs
    :param pid: process id
    :return:
    """
    if pid is None:
        proc = subprocess.Popen("killall tcpdump", shell=True)
    else:
        proc = subprocess.Popen(f"kill -9 {pid}", shell=True)
    out, err = proc.communicate()
    if not (out is None) or not (err is None):
        return Failure(str(out) + str(err))
    else:
        return Success("Done stopping tcpdump")




