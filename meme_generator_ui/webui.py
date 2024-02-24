import gradio as gr
from meme_generator import get_meme, get_memes
from meme_generator.exception import MemeGeneratorException
import json
import filetype
import os
import secrets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_file_exists(output_dir, key, name, exts=None):
    if exts == None:
        exts = ["jpg", "png", "gif"]

    for ext in exts:
        path = os.path.join(output_dir, f"{key}-{name}.{ext}")
        if os.path.exists(path):
            return path
    return False


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

    return output_path


async def meme_creator(key, images=None, texts_input="", args_input: dict = None):
    texts = texts_input.split()
    if images is None:
        images = []
    try:
        args = json.loads(args_input)
    except json.JSONDecodeError:
        args = {}

    try:
        output_path = await generate_meme_from_images(
            key=key,
            images=images,
            texts=texts,
            args=args,
            output_dir="outputs",
            name_override=secrets.token_urlsafe(4),
        )
        return gr.Image(output_path)

    except MemeGeneratorException as e:
        raise gr.Error(e.message)


meme_choices = [(f"{m.key:16} - {m.keywords}", m.key) for m in get_memes()]


with gr.Blocks() as webui:
    with gr.Row():
        with gr.Column():
            i1 = gr.Dropdown(meme_choices, label="Meme Keyword")
            i2 = gr.File(file_count="multiple", file_types=["image"], label="images")
            i3 = gr.Textbox("", lines=6, label="texts", info="separate by break line")
            i4 = gr.Textbox(
                '{"format": "json"}', lines=6, label="args", info="require json format"
            )
            but = gr.Button()
        with gr.Column():
            o1 = gr.Image()

    but.click(fn=meme_creator, inputs=[i1, i2, i3, i4], outputs=[o1])

    with gr.Blocks():
        gr.Markdown(
            "[memes docs](https://github.com/MeetWq/meme-generator/blob/main/docs/memes.md)"
        )


def main():
    webui.launch(inbrowser=True)
