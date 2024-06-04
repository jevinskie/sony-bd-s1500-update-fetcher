#!/usr/bin/env python3

import hashlib

from path import Path
from requests import Session
from rich import print


def check_url(ses: Session, url: str) -> bool:
    r = ses.head(url)
    if r.status_code == 200:
        print(f"\nGood response at: {url}\n{r}\n{r.headers}\n")
        return True
    elif r.status_code == 404:
        return False
    else:
        print(f"Something funky with {url}... status_code: {r.status_code} r: {r}")
        return False


def get_url(ses: Session, url: str) -> None:
    r = ses.get(url)
    assert r.status_code == 200
    name = url.split(sep="/")[-1]
    out_path = Path("update_zips")
    out_path.mkdir_p()
    out_path /= Path(name)
    sha256_digest = hashlib.sha256(r.content).hexdigest()
    print(f"FW: {name} SHA-256: {sha256_digest}\n")
    with open(out_path, "wb") as f:
        f.write(r.content)


def main() -> None:
    s = Session()
    print("Starting search for BDV-E190 FWs")
    for i in reversed(range(530)):
        print(f"M12R FW #{i}")
        url = f"https://hav.update.sony.net/BDP/data/UPDATA_M12R{i:04d}.zip"
        if check_url(s, url):
            get_url(s, url)
    print("Starting search for BDP-S5100 FWs")
    for i in reversed(range(275)):
        print(f"M15R FW #{i}")
        url = f"https://hav.update.sony.net/BDP/data/UPDATA_M15R{i:04d}.zip"
        if check_url(s, url):
            get_url(s, url)
    print("Starting search for BDP-S1500 FWs")
    for i in reversed(range(370)):
        print(f"M24R FW #{i}")
        url = f"https://hav.update.sony.net/BDP/data/UPDATA_M24R{i:04d}.zip"
        if check_url(s, url):
            get_url(s, url)


if __name__ == "__main__":
    main()
