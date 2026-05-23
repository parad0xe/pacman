from src.application import Application
from src.exceptions.base import PacmanError


def main() -> None:
    try:
        app = Application()
        app.run(1200, 800)
    except PacmanError as e:
        print(e)


if __name__ == "__main__":
    main()
