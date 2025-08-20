# update_checker.py
import requests
import config
from utils.error_handler import log_error

def check_update(current_version):
    try:
        if config.UPDATE_CHANNEL == "developer":
            return None  # No updates for developer channel
        elif config.UPDATE_CHANNEL == "release":
            headers = {
                "User-Agent": "FrogCardApp/1.0"
            }
            r = requests.get("https://api.github.com/repos/honzhe05/FrogCard/releases", headers=headers,  timeout=5)
            r.raise_for_status()
            releases = r.json()
            if releases:
                latest_version = releases[0]["tag_name"]
                # get apk
                for asset in releases[0]["assets"]:
                    if asset["content_type"] == "application/vnd.android.package-archive":
                        apk_url = asset["browser_download_url"]
                if latest_version != current_version:
                    return {
                        "version": latest_version,
                        "description": releases[0]["body"],
                        "html_url": releases[0]["html_url"],
                        "apk_url": apk_url,
                    }
        elif config.UPDATE_CHANNEL == "nightly":
            workflows_url = "https://api.github.com/repos/honzhe05/FrogCard/actions/workflows"
            res = requests.get(workflows_url).json()
            workflow_url = next((s["url"] for s in res.get("workflows") if s["name"] == "Build"), None)
            if not workflow_url:
                return None
            workflow_url += "/runs?per_page=1"
            res = requests.get(workflow_url).json()
            hash = res.get("workflow_runs")[0].get("head_sha")[0:7].strip().lower()
            app_version = config.HASH.strip().lower()
            if not hash == app_version:
                if res.get("workflow_runs")[0].get("status") == "completed":
                    return {
                        "version": hash,
                        "description": f"### New commit: {hash}\n\n**Full Changelog**: [{app_version}...{hash}](https://github.com/honzhe05/FrogCard/compare/{app_version}...{hash})",
                        "html_url": f"https://github.com/honzhe05/FrogCard/compare/{app_version}...{hash}",
                        "apk_url": f"https://nightly.link/honzhe05/FrogCard/workflows/build/main/FrogCard-{config.platform}-signed.zip",
                    }
            return None
    except Exception as e:
        log_error("check_version", e)
    return None