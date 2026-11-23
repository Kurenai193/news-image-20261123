"""THE WORLD TODAY - Monday 23 November 2026 (news-image-20261123).

This program is the whole entry. It carries one finished front-page
image, entry.png, in the repository root and writes that exact file
to the competition output location. The front page sums up the
world news of 23 November 2026 in a single 1024 by 1024 picture:

- centre: COP31 in Antalya ends with no climate pact, after the
  longest COP on record; the EU rejected a draft deal that never
  mentioned fossil fuels, and the UN chief spoke of deep
  disappointment at the lack of consensus
- Indonesia: a confectionery factory fire in Serang kills three
  people and leaves thirty-six workers missing
- Ukraine: a Russian drone strikes a five-storey apartment block
  in Dymer in the Kyiv region, with fourteen people missing
- space, the bright story of the day: the Japan-Europe probe
  BepiColombo arrives at Mercury after an eight-year cruise
- Nigeria: a boat carrying mourners to a funeral capsizes in
  Bayelsa State and twenty-four people lose their lives
- Baltic: the Russian cargo ship Sparta II burns in the Gulf
  of Finland after a drone hit, its crew evacuated
- ticker: Iran and Bahrain at the UN, China and the US in a
  telecom row, and South Korea's education chief resigning
  over an AI cheating scandal

The program uses only the Python standard library, needs no
network, and is deterministic: every run writes identical bytes.
"""

import hashlib
import os
import shutil

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024


def source_image_path() -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, "entry.png")


def check_image(path: str) -> int:
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError("entry image is larger than one mebibyte")
    with open(path, "rb") as handle:
        head = handle.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        raise ValueError("entry image is not a PNG file")
    return size


def output_directory() -> str:
    # The grader sets MAKEFUN_OUTPUT_DIR; /output is the fallback
    # named in the competition rules, so local runs agree with it.
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def deliver() -> str:
    src = source_image_path()
    expected = check_image(src)
    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != expected:
        raise IOError("copied image has the wrong size")
    with open(dst, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote", dst, expected, "bytes, sha256", digest)
    return dst


if __name__ == "__main__":
    deliver()
