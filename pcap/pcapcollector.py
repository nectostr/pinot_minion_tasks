"""
Module that set's up the pcap files data collection
"""
import subprocess
import time
from typing import Optional, List

from returns.result import Result, Success, Failure


def start_collecting(dump_file: str, arguments: Optional[List[str]] = None) -> Result[str, str]:
    """
    Function that starts data collection
    :param dump_file: foldr to save data to
    :param arguments: string with additional arguments for collecting
    :return: Failure with error or success with pid and filename
    """
    arguments = arguments or []
    proc = subprocess.Popen(["tcpdump"] + arguments + ["-U", "-w", dump_file])
    time.sleep(2)
    if proc.poll() is None:
        return Success(f"Running with <{proc.pid}>")

    return Failure(f"Process terminated with return code {proc.poll()}")


def stop_collecting(pid: Optional[int] = None) -> Result[str, str]:
    """
    Kills either all tcpdump procc, or the one, that mentioned in agrs
    :param pid: process id
    :return: Success or Failure with relevant info
    """
    if pid is None:
        line = ["killall", "tcpdump"]
    else:
        line = ["kill", f"{pid}"]

    proc = subprocess.Popen(line,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    time.sleep(2)  # for tcpdump to finish file

    if out != b"" or err != b"":
        return Failure(f"out: {out}, err: {err}")
    return Success("Done stopping tcpdump")
