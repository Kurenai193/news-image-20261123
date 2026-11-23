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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT_DIR, "entry.png"))
