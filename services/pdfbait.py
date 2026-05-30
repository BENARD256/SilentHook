import re
import zlib
import random
from io import BytesIO
from pathlib import Path

STREAM_OFFSET = 793


def make_pdf_bait(callback_url: bytes, template: Path, token: str) -> str:
    contents = Path(template).read_bytes()

    stream_size  = int(re.match(rb".*\/Length ([0-9]+)\/.*", contents[STREAM_OFFSET:]).group(1))
    stream_start = STREAM_OFFSET + contents[STREAM_OFFSET:].index(b"stream\r\n") + 8
    header       = contents[STREAM_OFFSET:stream_start]
    stream       = contents[stream_start:stream_start + stream_size]

    PLACEHOLDER = b"abcdefghijklmnopqrstuvwxyz.zyxwvutsrqponmlkjihgfedcba.aceegikmoqsuwy.bdfhjlnprtvxz"
    old_len     = len(stream)
    candidate   = None

    for count in range(0, 10000):
        padding   = ("".join([chr(random.randrange(65, 90)) for _ in range(count)])).encode()
        injection = callback_url + (b"/" + padding if padding else b"")
        candidate = zlib.compress(zlib.decompress(stream).replace(PLACEHOLDER, injection))
        if len(candidate) == old_len:
            break
    else:
        raise Exception("Could not match stream size after padding attempts")

    output = BytesIO()
    output.write(contents[:STREAM_OFFSET])
    output.write(header)
    output.write(candidate)
    output.write(contents[stream_start + stream_size:])

    out_path = Path("static/downloads") / f"{token}.pdf"
    out_path.write_bytes(output.getvalue())

    return out_path.name

def pdf_bait(CALLBACK_URL, TEMPLATE, TOKEN):

    return make_pdf_bait(CALLBACK_URL.encode(), Path(TEMPLATE), TOKEN)

if __name__ == "__main__":
    CALLBACK_URL = "http://127.0.0.1/callback"
    TOKEN = "123ABC"
    TEMPLATE = "template.pdf"
    pdf_bait(CALLBACK_URL, TEMPLATE, TOKEN)

