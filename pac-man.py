import sys

from src.application import Application
from src.exceptions.base import PacmanError


def main() -> None:
    try:
        if len(sys.argv) != 2:
            raise PacmanError("Invald number of arguments")

        config_file_path: str = sys.argv[1]

        app = Application(config_file_path=config_file_path)
        app.run(1200, 800)
    except PacmanError as e:
        print(f"[Error] {e}")
        exit(1)
    except Exception as e:
        print(f"[Error] {e}")
        exit(2)


if __name__ == "__main__":
    main()
