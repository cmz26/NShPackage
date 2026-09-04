"""
echo - neosh 包（多文件示例）

包含多个文件:
    __init__.py    入口: info() / main(args)
    core.py        参数解析与输出逻辑
    _version.py    版本号

用法（在 neosh 中）:
    echo [文本...]      打印一行文本
    echo -n [文本...]   打印文本但不换行
"""

import sys

from ._version import __version__
from .core import render


def info() -> dict:
    """返回包信息（发现/列表阶段调用，勿在此放重逻辑）"""
    return {
        "name": "echo",
        "version": __version__,
        "description": "Print text back to the terminal",
        "author": "neosh",
    }


def main(args: list) -> None:
    """包的主函数"""
    text, newline = render(args)
    sys.stdout.write(text)
    if newline:
        sys.stdout.write("\n")
