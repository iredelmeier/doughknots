from sanic import Sanic

from shopfront import factory as shopfront_factory

if __name__ == "__main__":
    app = Sanic()

    shopfront_bp = shopfront_factory()
    app.blueprint(shopfront_bp)

    @app.middleware("request")
    async def print_on_request(request):
        print("hello there")

    app.run(host="127.0.0.1", port=8080, debug=True)
#  from flask import Flask


#  def create_app():
#  app = Flask(__name__)

#  @app.route("/hello")
#  def hello():
#  return "Hello, World!"

#  return app
