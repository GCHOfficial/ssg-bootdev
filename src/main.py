import sys

from utils import copy_static, generate_pages_recursive


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static(f".{basepath}static/", f".{basepath}docs/")
    generate_pages_recursive(
        f".{basepath}content/",
        f".{basepath}src/template.html",
        f".{basepath}docs/",
        basepath,
    )


if __name__ == "__main__":
    main()
