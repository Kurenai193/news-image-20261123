"""Deliver the day's front page as the program's output artifact.

The picture itself is painted by build_frontpage.py, which writes
entry.png beside this file. This entrypoint's job is acceptance and
delivery: confirm the stored picture is a genuine PNG of at most
1024 by 1024 pixels and at most one mebibyte, prove it by hashing
the bytes, then copy it to the output path named on the command
line (a plain copy of the file when no argument is given).

Standard library only, no network, and the output is a byte-for-byte
copy of the verified input, so repeated runs agree exactly.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
LIMIT_BYTES = 1024 * 1024
LIMIT_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(blob: bytes) -> tuple[int, int]:
    """Read width and height from the IHDR chunk of a PNG byte string."""
    if blob[:8] != PNG_MAGIC:
        raise ValueError("entry.png does not start with the PNG signature")
    if blob[12:16] != b"IHDR":
        raise ValueError("entry.png is missing its IHDR chunk")
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def checked_payload() -> bytes:
    """Load entry.png and enforce the competition's size rules."""
    blob = SOURCE.read_bytes()
    if len(blob) > LIMIT_BYTES:
        raise ValueError(f"entry.png is {len(blob)} bytes, over the 1 MiB cap")
    width, height = png_dimensions(blob)
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the 1024 cap")
    digest = hashlib.sha256(blob).hexdigest()
    print(f"verified entry.png: {width}x{height}, {len(blob)} bytes, sha256 {digest}")
    return blob


def default_destination() -> Path:
    """Where to write when no output path is given on the command line.

    The grading sandbox mounts this repository read-only and names a
    writable output directory in MAKEFUN_OUTPUT_DIR, so the default
    must never be a file beside this program.
    """
    named = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if named:
        return Path(named) / "output.png"
    return Path("/tmp/output.png")


def main(argv: list[str]) -> int:
    payload = checked_payload()
    destination = Path(argv[1]) if len(argv) > 1 else default_destination()
    destination.write_bytes(payload)
    if destination.read_bytes() != payload:
        raise ValueError("output copy does not match the verified bytes")
    print(f"wrote {destination} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
