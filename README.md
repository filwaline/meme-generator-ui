
# Meme Generator UI

依赖 [meme-generator](https://github.com/MeetWq/meme-generator/tree/main)

1. 编写yaml，批量生成表情
2. 启动webui，交互式生成表情

## Installation

```sh
poetry install
poetry run meme download
```

## Usage

1. 编写yaml，并直接生成多个表情
```sh
poetry run meme-from-yaml --config-file config-memes-example.yaml
```


1. 或者启动一个WebUI，手动设置参数
```sh
poetry run meme-web-ui
```

## Note

所有生成的表情，默认输出到 outputs 文件夹
