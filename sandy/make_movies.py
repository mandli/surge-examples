#!/usr/bin/env python

"""
ffmpeg, convert png to mpg

ffmpeg -r FRAMES_PER_SECOND -i IMAGE_PATHS -q:a 0 -q:v 0 -vcodec mpeg4 -vb 20M -r FRAMES_PER_SECOND_MOV OUTPUT_FILE

`-qscale 0` - Forces lossless quality conversion -> should use `-q:a 0 -q:v 0`
`FRAMES_PER_SECOND` - Number of images to display per second, can be fractional
`IMAGE_PATHS` - Image paths, use normal substitution macros, i.e. frame%04dfig4.png would expand to frameXXXXfig4.png where XXXX is zero filled.
`FRAMES_PER_SECOND_MOV` - Frames per second of output, probably should be 24 or greater
`OUTPUT_FILE` - Output movie name, note that the file extension needs to be something useful such as mp4
"""

from __future__ import print_function

import os
import sys
import subprocess

# figures = range(1, 18)
figures = [1003, 1004]
# figures = [1]
frames_per_second = 4

def make_movie(fig_num, base_path="_plots", out_path="./"):

    image_glob = r"frame%04dfig"
    image_glob += "%s.png" % fig_num
    image_paths = os.path.join(base_path, image_glob)
    out_file = "fig%s.mp4" % fig_num
    cmd = "ffmpeg -r %s -i %s -q:a 0 -q:v 0 -vcodec mpeg4 -vb 20M -r %s %s" % (frames_per_second, image_paths, 24, out_file)
    print(cmd)
    subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    base_path = os.getcwd()
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    for fig_num in figures:
        make_movie(fig_num, base_path)