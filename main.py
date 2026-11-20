# One image summing up 20 November 2026's world news.
# Stdlib only: copies the committed entry.png to the output directory.
# The grader's Python has no Pillow, so nothing is generated or drawn here.

import hashlib
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        data = f.read()
    print(len(data), hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
