"""echo 的核心逻辑（被 __init__ 通过包内相对导入引用）"""


def render(args: list):
    """解析参数，返回 (输出文本, 是否追加换行)。

    支持:
        echo [文本...]      打印文本并换行
        echo -n [文本...]   打印文本但不换行
    """
    newline = True
    if args and args[0] == "-n":
        newline = False
        args = args[1:]
    return " ".join(args), newline
