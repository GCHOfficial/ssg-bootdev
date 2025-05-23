import sys

from utils import copy_static, generate_pages_recursive


def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("./static/", "./docs/")
    generate_pages_recursive(
        "./content/",
        "./src/template.html",
        "./docs/",
        basepath,
    )


if __name__ == "__main__":
    main()
