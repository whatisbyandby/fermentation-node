from quart import Quart, request, Response
import json
from fermentation_controller import FermentationController

app = Quart(__name__)
controller = FermentationController()

@app.route('/', methods=["GET", "POST", "PUT"])
async def step():
    if request.method == "GET":
        return Response(json.dumps(controller.get_step()), mimetype="application/json")
    elif request.method == "POST":
        new_step = await request.get_json()
        return Response(json.dumps(controller.set_step(new_step)), mimetype="application/json")
    elif request.method == "PUT":
        return Response("True")


@app.route('/run')
async def run():
    success = controller.run()
    return Response("True")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)