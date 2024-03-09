set shell := ["nu", "-c"]

memes:
    poetry run meme-from-yaml

webui:
    poetry run meme-web-ui


update-avatars:
    poetry run python .\update_avatar_images.py