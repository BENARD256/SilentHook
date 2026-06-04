from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

# Constants in deploy.ps1 template
CALLBACK_TOKEN  = b"TOKEN"
URL_PLACEHOLDER = b"CALLBACK_URL"
MONITORED_PATH  = b"MONITORED_PATH"

DOWNLOADS_DIR = Path("static/downloads") # Where Final Zip is saved
DEFAULT_DIR = "C:\Program Files (x86)\critical"

def make_bait(callback_token : str, callback_url: str, monitored_path: str,  template_dir: Path) -> str:
    data = Path(template_dir / "deploy.ps1").read_bytes()
    
    # REPLACEMENT PROCESS
    data = data.replace(CALLBACK_TOKEN, callback_token.encode())
    data = data.replace(URL_PLACEHOLDER, callback_url.encode())
    data = data.replace(MONITORED_PATH, monitored_path.encode())
    
    # WRITING CHANGES
    TEMP_DIR = template_dir / "tmp"
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    deploy_path = TEMP_DIR / f"deploy_{callback_token}.ps1"
    deploy_path.write_bytes(data)
    
    # Uninstallation Script
    uninstall_data = Path(template_dir / "uninstall.ps1").read_bytes()
    uninstall_data = uninstall_data.replace(CALLBACK_TOKEN, callback_token.encode())
    uninstall_data = uninstall_data.replace(MONITORED_PATH, monitored_path.encode())

    uninstall_path = TEMP_DIR / f"uninstall_{callback_token}.ps1"
    uninstall_path.write_bytes(uninstall_data)

    return TEMP_DIR # static/baits/fim/tmp


def fim_bait(callback_token: str, callback_url: str, template_dir: Path, monitored_path: str = DEFAULT_DIR):
    if monitored_path is None:
        monitored_path = DEFAULT_DIR

    template_dir = Path(template_dir) # Converts path to PosixPath Object

    temp = make_bait( callback_token=callback_token, callback_url=callback_url, monitored_path=monitored_path, template_dir=template_dir)
    
    #print("Patched path: ", type(deploy_injected), deploy_injected)

    # Creating Zip file
    zip_name = f"FIM_{callback_token}.zip"
    out_zip  = DOWNLOADS_DIR / zip_name

    with ZipFile(out_zip, "w", ZIP_DEFLATED) as zf:
        zf.write(temp/f"deploy_{callback_token}.ps1", arcname="deploy.ps1")
        zf.write(temp/f"uninstall_{callback_token}.ps1", arcname=f"uninstall_{callback_token}.ps1")
        zf.write(template_dir / "watcher.ps1", arcname="watcher.ps1")
        zf.write(template_dir / "README.md", arcname="README.md")

    # Cleaning up the file temp
    (temp / f"deploy_{callback_token}.ps1").unlink()
    (temp / f"uninstall_{callback_token}.ps1").unlink()
    
    
    #print("Zip ready:", out_zip) # posix.Path
    return zip_name
	
if __name__ == "__main__":
    template_dir = "static/baits/fim/"
    token = "ae99ed54340fb22f"
    path = "c:\Program files(x86)\Stealthy" 
    url = "https://dbbd.com:5000"
    
    #make_bait(callback_token=token, callback_url=url, monitored_path=path, template=template)
    final_zipfile_name = fim_bait(callback_token=token, callback_url=url, monitored_path=path, template_dir=Path(template_dir))
    
    print("FILENAME:", final_zipfile_name)
