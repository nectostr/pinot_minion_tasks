"""
Module that set's up the pcap files data collection
"""
import subprocess
import time
from typing import Optional

from returns.result import Result, Success, Failure


def start_collecting(dump_file: str, arguments: str) -> Result[str, str]:
    """
    Function that starts data collection
    :param dump_file: foldr to save data to
    :param arguments: string with additional arguments for collecting
    :return: Failure with error or success with pid and filename
    """
    proc = subprocess.Popen(f"sudo tcpdump {arguments} -w {dump_file}",
                            shell=True,
                            universal_newlines=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    time.sleep(1)
    out = next(iter(proc.stdout.readline, b''))
    if out and ("tcpdump: listening" not in out):
        return Failure(f"{out}")
    return Success(f"{out} with <{proc.pid}>")


def stop_collecting(pid: Optional[int] = None) -> Result[str, str]:
    """
    Kills either all tcpdump procc, or the one, that mentioned in agrs
    :param pid: process id
    :return: Success or Failure with relevant info
    """
    if pid is None:
        proc = subprocess.Popen("sudo killall tcpdump",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    else:
        proc = subprocess.Popen(f"kill -9 {pid}",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if out != b"" or err != b"":
        return Failure(f"out: {out}, err: {err}")
    else:
        return Success("Done stopping tcpdump")
