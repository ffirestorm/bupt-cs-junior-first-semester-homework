from sanic import Sanic # 提前自行下载该模块
from sanic.response import json

app = Sanic(__name__)

@app.route("/")
async def test(request):
  return json({"hello": "world"})

if __name__ == "__main__":
  app.run(host="localhost", port=8000)
