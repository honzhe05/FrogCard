import requests
from utils.error_handler import log_error

def check_update(current_version):
    try:
        r = requests.get("https://api.github.com/repos/honzhe05/FrogCard/tags", timeout=5)
        r.raise_for_status()
        tags = r.json()
        if tags:
            latest_version = tags[0]["name"]
            if latest_version != current_version:
                return {
                    "version": latest_version,
                    "changelog": "",
                    "apk_url": f"https://github.com/honzhe05/FrogCard/releases/download/{latest_version}/frogcard_{latest_version}.apk"
                }
    except Exception as e:
        log_error("check_version", e)
    return None