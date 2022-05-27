"""
Example of youtube data collection
"""
import multiprocessing
import os
import sys

from returns.result import Result, Success, Failure

import QoE_youtube.fastapicollector as fastapic
import QoE_youtube.watcher as watcher
import extractor.youtube_flow_extractor as utubee
import pcap.pcapcollector as pcapc


def run(video: str, duration: int, data_dump: str, pcap_name: str) -> Result[str, str]:
    """
    Example youtube traffic collection run
    :param video:
    :param duration:
    :param data_dump:
    :param pcap_name:
    :return:
    """
    fa_c = multiprocessing.Process(target=fastapic.run)
    fa_c.start()

    result = pcapc.start_collecting(pcap_name)
    if isinstance(result, Failure):
        fa_c.terminate()
        return result

    pid = result.unwrap()
    pid = pid[pid.find("<") + 1:pid.find(">")]
    pid = int(pid)

    result = watcher.watch(video, duration)
    if isinstance(result, Failure):
        fa_c.terminate()
        pcapc.stop_collecting()
        return result

    result = pcapc.stop_collecting(pid)
    if isinstance(result, Failure):
        fa_c.terminate()
        return result

    result = utubee.extract(pcap_name, data_dump)
    if isinstance(result, Failure):
        fa_c.terminate()
        return result

    fa_c.terminate()

    return Success("All done")


if __name__ == '__main__':
    video = sys.argv[1]
    duration = sys.argv[2]
    data_dump = sys.argv[3]
    pcap_name = os.path.join(data_dump, "test.pcap")
    result = run(video, duration, data_dump, pcap_name)
    print(result)
