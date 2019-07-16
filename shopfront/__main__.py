from sanic import Sanic

from . import factory


def main():
    app = Sanic()

    app.blueprint(factory())

    app.run(host="127.0.0.1", port=8000, debug=True)


if __name__ == "__main__":
    main()
