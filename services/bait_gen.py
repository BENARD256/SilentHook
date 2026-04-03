from __future__ import absolute_import
import datetime, random
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


URL_PLACEHOLDER = b"CALLBACK_URL"
CREATED_TS_PLACEHOLDER = b"aaaaaaaaaaaaaaaaaaaa"
MODIFIED_TS_PLACEHOLDER = b"bbbbbbbbbbbbbbbbbbbb"

def _ts(dt): return dt.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    

def make_bait(template_path: Path, callback_url: str, bait_name: str, output_dir: Path) -> Path:
    now = datetime.datetime.now()
    created = now - datetime.timedelta(days=random.randint(1,25), hours=random.randint(1,24))
    
    ext = template_path.suffix  # dynamic extension from template

    out = BytesIO()
    with ZipFile(template_path, "r") as src, ZipFile(out, "w", ZIP_DEFLATED) as dst:
        for entry in src.filelist:
            if entry.external_attr & (0x10 << 16): continue
            data = src.read(entry.filename)
            data = data.replace(URL_PLACEHOLDER, callback_url.encode())
            data = data.replace(CREATED_TS_PLACEHOLDER, _ts(created))
            data = data.replace(MODIFIED_TS_PLACEHOLDER, _ts(now))
            dst.writestr(entry, data)

    out_path = output_dir / f"{bait_name}{ext}"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(out.getvalue())
    return out_path


if __name__ == "__main__":
    out = make_bait(
        template_path=Path("static/baits/xlsx/template.xlsx"),
        callback_url="http://192.168.100.10/trigger.png",
        bait_name="test_bait",
        output_dir=Path("static/downloads/")
    )
    print(f"Generated: {out}")
