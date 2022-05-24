"""
Module that filters the youtube traffic flow and saves multiple pcaps
"""
import os

import pyshark
from returns.result import Result, Success


def ends_with(text: str, end: str) -> bool:
    if len(end) > len(text):
        return False
    return text[-len(end):] == end


def f(filepath: str, dump_path: str = ".") -> Result[list, str]:
    capture = pyshark.FileCapture(filepath, display_filter='tls.handshake.extension.type == 0')

    starts = []
    for packet in capture:
        if "TLS" in packet and hasattr(packet.tls, "handshake_extensions_server_name"):
            sni = packet.tls.handshake_extensions_server_name
            if ends_with(sni, ".googlevideo.com"):
                starts.append((packet.ip.src, packet.tcp.srcport,
                               packet.ip.dst, packet.tcp.dstport))
    capture.close()
    filenames = []
    for src, srcport, dst, dstport in starts:
        tshark_filter = f"(ip.src == {src} && tcp.srcport == {srcport} && " \
                        f"ip.dst == {dst} && tcp.dstport == {dstport}) || " \
                        f"(ip.src == {dst} && tcp.srcport == {dstport} && " \
                        f"ip.dst == {src} && tcp.dstport == {srcport})"
        filename = os.path.join(dump_path, f"{src}_{srcport}_{dst}_{dstport}.pcap")
        filenames.append(filename)
        capture = pyshark.FileCapture(filepath, display_filter=tshark_filter, output_file=filename)
        capture.load_packets()
        capture.close()

    return Success(filenames)


if __name__ == '__main__':
    f(r"p.cap")
