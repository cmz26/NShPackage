# tool

neosh 包打包工具（纯标准库，无需安装依赖）。

## pack.py

把一个包目录（含 `__init__.py`，暴露 `info()` / `main(args)`）打包成
neosh 可安装的 `<name>.neopackage.tar.gz`（或 `.zip`）归档。

```
python pack.py <包目录> [--out DIR] [--type tar-gz|zip]
                       [--register URL] [--index PATH]
```

| 参数 | 说明 | 默认 |
| --- | --- | --- |
| `包目录` | 包文件夹，必须包含 `__init__.py` | 必填 |
| `--out` | 产物输出目录 | `pkgs/dist/` |
| `--type` | 归档格式：`tar-gz` 或 `zip` | `tar-gz` |
| `--register URL` | 同时把该包写入索引（URL 为下载地址） | 不写入 |
| `--index` | 索引文件路径（配合 `--register`） | `pkgs/__index__.json` |

示例：

```
python pack.py ../code/echo
python pack.py ../code/echo --type zip
python pack.py ../code/echo --register https://example.com/echo.neopackage.tar.gz
```

归档内统一带顶层目录 `<name>.neopackage/`，打包时自动跳过
`__pycache__/`、`.pyc` 等文件。打包后在 neosh 中：

```
install echo
echo hello
```
