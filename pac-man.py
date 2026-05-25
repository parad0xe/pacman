import sys

from src.application import Application
from src.exceptions.base import PacmanError


def main() -> None:
    if len(sys.argv) != 2:
        raise PacmanError("Invald number of arguments")

    config_file_path: str = sys.argv[1]

    try:
        app = Application(config_file_path=config_file_path)
        app.run(1200, 800)
    except PacmanError as e:
        print(e)


if __name__ == "__main__":
    main()
