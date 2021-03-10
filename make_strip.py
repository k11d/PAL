#!/usr/bin/env python3

import sys
import os
import numpy as np
from PIL import Image


def main():

    def _load_frames(frames_path_gen, direction):
        _frames = []
        h, w = 0, 0
        for frame in frames_path_gen:
            im = Image.open(frame)
            iar = np.array(im)
            _frames.append(iar)
            ih, iw = iar.shape[:2]
            if direction == 'H':
                if h == 0:
                    h = ih
                w += iw
            elif direction == 'V':
                if w == 0:
                    w = iw
                h += ih
        return _frames, (h,w)

    def _create_strip(frames, direction):
        h,w = frames[0].shape[:2]
        for n, frame in enumerate(frames):
            if direction == 'H':
                ret[:, n*w : (n+1)*w, :] = frame[:,:,:3]
            elif direction == 'V':
                ret[n*h:(n+1)*h, :, :] = frame[[:,:,:3]

    if len(sys.argv) != 4 or '-h' in sys.argv or '--help' in sys.argv:
        print(f"Usage: {os.path.basename(sys.argv[0])} FRAMES_DIR/ H|V DESTNAME.PNG")
        return 0

    frames_dir = sys.argv[1]
    strip_direction = sys.argv[2]
    dest_filename = sys.argv[3]
    frames_path = (os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith('.png'))
    frames, dims = _load_frames(frames_path, strip_direction)
    ret = np.zeros((*dims, 3), dtype=np.uint8)
    _create_strip(frames, strip_direction)
    Image.fromarray(ret).save(f"{os.path.splitext(dest_filename)[0]}_{len(frames)}{os.path.splitext(dest_filename)[1]}")

if __name__ == '__main__':
    main()

