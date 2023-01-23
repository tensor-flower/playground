import os
import ffmpeg
from typing import Tuple, List
from pathlib import Path


def trim(dir: str, in_file: str, inputs: List[Tuple]):
    in_file = os.path.join(
        os.path.dirname(dir),
        in_file)
    out_file = os.path.join(
        os.path.dirname(dir),
        Path(in_file).stem+'_output'+Path(in_file).suffix)
    if os.path.exists(out_file):
        os.remove(out_file)

    input_stream = ffmpeg.input(in_file)
    pts = "PTS-STARTPTS"
    streams = []
    for input in inputs:
        start: int = input[0]
        end: int = input[1]
        video = input_stream.trim(start=start, end=end).setpts(pts)
        audio = (input_stream
                 .filter_("atrim", start=start, end=end)
                 .filter_("asetpts", pts))
        streams = [*streams, video, audio]

    out_stream = ffmpeg.concat(*streams, v=1, a=1)
    output = ffmpeg.output(out_stream, out_file, format="mp4")
    output.run()


def prob(file: str):
    file_probe_result = ffmpeg.probe(file)
    file_duration = file_probe_result.get(
        "format", {}).get("duration", None)
    print(file_duration)


dir: str = '/Users/guowanqi/playground/ffmpeg-trim/assets/'
filename: str = "thimble.mov"
ts: List[Tuple] = [(3, 10), (31, 37)]
trim(dir, filename, ts)
