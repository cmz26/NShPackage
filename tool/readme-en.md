# tool

neosh package packaging tool (standard library only, no dependencies required).

## pack.py

Packages a package directory (containing `__init__.py` and exposing `info()` / `main(args)`) into a
neosh-installable `<name>.neopackage.tar.gz` (or `.zip`) archive.

```
python pack.py <package-directory> [--out DIR] [--type tar-gz|zip]
                       [--register URL] [--index PATH]
```

| Argument | Description | Default |
| --- | --- | --- |
| `package-directory` | Package folder; must contain `__init__.py` | Required |
| `--out` | Output directory for the artifact | `pkgs/dist/` |
| `--type` | Archive format: `tar-gz` or `zip` | `tar-gz` |
| `--register URL` | Also write the package to the index (URL is the download address) | Not written |
| `--index` | Index file path (used with `--register`) | `pkgs/__index__.json` |

Example:

```
python pack.py ../code/echo
python pack.py ../code/echo --type zip
python pack.py ../code/echo --register https://example.com/echo.neopackage.tar.gz
```

Archives always include the top-level directory `<name>.neopackage/`; when packaging, files such as
`__pycache__/` and `.pyc` are skipped automatically. After packaging, in neosh:

```
install echo
echo hello
```
