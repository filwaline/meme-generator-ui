import yaml
from meme_generator import get_meme
import asyncio
import filetype
import os
import logging
import typer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_avatar_name(path):
    _, tail = os.path.split(path)
    name, _ = os.path.splitext(tail)
    return name


def check_file_exists(output_dir, key, name, exts=None):
    if exts == None:
        exts = ["jpg", "png", "gif"]

    for ext in exts:
        path = os.path.join(output_dir, f"{key}-{name}.{ext}")
        if os.path.exists(path):
            return path
    return False


async def generate_meme_from_avatar(
    key, images, texts, args, output_dir, name_override=None, force_update=False
):
    avatar = images[0]
    worker = get_meme(key)
    name = get_avatar_name(avatar)
    if name_override:
        name = name_override
    if (output_path := check_file_exists(output_dir, key, name)) and not force_update:
        logger.debug(f"skip exists: {output_path}")
        return

    result = await worker(images=[avatar], texts=texts, args=args)
    content = result.getvalue()
    ext = filetype.guess_extension(content)
    output_path = os.path.join(output_dir, f"{key}-{name}.{ext}")
    with open(output_path, "wb") as f:
        logger.info(f"save: {output_path=}")
        f.write(content)


async def generate_meme_from_images(
    key, images, texts, args, output_dir, name_override=None, force_update=False
):
    worker = get_meme(key)
    name = "".join(texts)[:10]
    if name_override:
        name = name_override
    if (output_path := check_file_exists(output_dir, key, name)) and not force_update:
        logger.debug(f"skip exists: {output_path}")
        return

    result = await worker(images=images, texts=texts, args=args)
    content = result.getvalue()
    ext = filetype.guess_extension(content)
    output_path = os.path.join(output_dir, f"{key}-{name}.{ext}")
    with open(output_path, "wb") as f:
        logger.info(f"save: {output_path=}")
        f.write(content)


async def generate_meme_from_texts(
    key, texts, args, output_dir, name_override=None, force_update=False
):
    worker = get_meme(key)
    name = "".join(texts)[:10]
    if name_override:
        name = name_override
    if (output_path := check_file_exists(output_dir, key, name)) and not force_update:
        logger.debug(f"skip exists: {output_path}")
        return

    result = await worker(texts=texts, args=args)
    content = result.getvalue()
    ext = filetype.guess_extension(content)
    output_path = os.path.join(output_dir, f"{key}-{name}.{ext}")
    with open(output_path, "wb") as f:
        logger.info(f"save: {output_path=}")
        f.write(content)


async def generate(item, output_dir):
    match item:
        case {"key": key, "images": images} if len(images) == 1:
            await generate_meme_from_avatar(
                key,
                images=images,
                texts=item.get("texts", []),
                args=item.get("args", {}),
                name_override=item.get("name_override"),
                force_update=item.get("force_update", False),
                output_dir=output_dir,
            )
        case {"key": key, "images": images}:
            await generate_meme_from_images(
                key,
                images=images,
                texts=item.get("texts", []),
                args=item.get("args", {}),
                name_override=item.get("name_override"),
                force_update=item.get("force_update", False),
                output_dir=output_dir,
            )
        case {"key": key, "texts": texts}:
            await generate_meme_from_texts(
                key,
                texts=texts,
                args=item.get("args", {}),
                name_override=item.get("name_override"),
                force_update=item.get("force_update", False),
                output_dir=output_dir,
            )


async def generate_from_config(data: dict):
    for item in data["memes"]:
        logger.debug(item)
        await generate(item, data["output_dir"])


def read_config(config_file="config-memes.yaml") -> dict:
    with open(config_file, encoding="utf-8") as cf:
        data = yaml.load(cf, Loader=yaml.FullLoader)
        return data


def command(config_file="config-memes.yaml"):
    data = read_config(config_file)
    asyncio.run(generate_from_config(data))


def main():
    typer.run(command)


if __name__ == "__main__":
    main()
