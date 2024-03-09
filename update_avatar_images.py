import httpx
import os
import filetype


def get_qq_avatar(qq, nickname, output_dir):
    resp = httpx.get(
        "https://api.xingzhige.com/API/get_QQavatar/", params={"qq": qq, "s": 5}
    )
    url = resp.json()["data"]["avatar"]

    resp2 = httpx.get(url=url)
    ext = filetype.guess_extension(resp2.content)
    filepath = os.path.join(output_dir, f"{nickname}.{ext}")
    with open(filepath, "wb") as f:
        f.write(resp2.content)
        print(f"saving file to {filepath=}")
