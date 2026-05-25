from __future__ import absolute_import
import datetime, random
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

#CALLBACK_URL = "http://127.0.0.1:5000/token/b63fb9b4-9b2b-4dfa-a9b9-e6c2bcdf1596/callback"


URL_PLACEHOLDER = b"CALLBACK_URL" # in the Template

DOWNLOADS_DIR = Path("static/downloads")


CREATED_TS_PLACEHOLDER = b"aaaaaaaaaaaaaaaaaaaa"
MODIFIED_TS_PLACEHOLDER = b"bbbbbbbbbbbbbbbbbbbb"

def _ts(dt): return dt.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    
def make_bait(CALLBACK_URL, template: Path, token: str) -> Path:
    now = datetime.datetime.now()
    created = now - datetime.timedelta(days=random.randint(1,25), hours=random.randint(1,24))

    out = BytesIO()
    with ZipFile(template, "r") as src, ZipFile(out, "w", ZIP_DEFLATED) as dst:
        for entry in src.filelist:
            if entry.external_attr & (0x10 << 16): continue
            data = src.read(entry.filename)
            data = data.replace(URL_PLACEHOLDER,         CALLBACK_URL.encode())
            data = data.replace(CREATED_TS_PLACEHOLDER,  _ts(created))
            data = data.replace(MODIFIED_TS_PLACEHOLDER, _ts(now))
            dst.writestr(entry, data)

    #out_path = template.with_stem(name)
    out_path = DOWNLOADS_DIR / f"{token}{template.suffix}"

    out_path.write_bytes(out.getvalue())

    print("output path: ", out_path)

    return str(out_path.name) # Fixing POSTFIX json serialization error & returning only filename


def msoffice_bait(CALLBACK_URL, TEMPLATE, TOKEN):

    return make_bait(CALLBACK_URL, Path(TEMPLATE), TOKEN)
    


if __name__ == "__main__":
	
	# Supplying the 3 fields the bait has to generated to the download paths
	# callback_url : URL callback if bait is opened
	# Token		   : Used for Filenaming
	# Template:		Bait Template
	
	CALLBACK_URL = "http://127.0.0.1/callback"
	TOKEN = "123ABC"
	TEMPLATE = "template.docx"

	msoffice_bait(CALLBACK_URL, TEMPLATE, TOKEN)
	
