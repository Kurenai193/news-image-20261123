"""news-image-20261123 entry: copy the bundled front-page image to the output.

The image (entry.png, beside this file) sums up the world news of Monday
23 November 2026 in one front page: COP31 ends with no climate pact
(centre), an Indonesian factory fire with 36 missing, a drone strike on a
Kyiv apartment block, BepiColombo reaching Mercury, a Nigerian boat
disaster that killed 24, and a Russian cargo ship burning off Finland,
with a ticker for the Iran-Bahrain strike, the China-US telecom row and
South Korea's AI-cheating resignation.
"""

import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    # Copy byte-for-byte so repeated runs write identical bytes,
    # as the competition rules require (no network, deterministic).
    shutil.copyfile(src, dst)
    assert os.path.getsize(dst) == os.path.getsize(src)


if __name__ == "__main__":
    main()
