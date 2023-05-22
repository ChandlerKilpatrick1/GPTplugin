import quart
import quart_cors
from quart import request
from datetime import datetime, timedelta

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of the current ranked map.
CURRENT_RANKED_MAP = ""

# Define the map rotation and change time.
MAP_ROTATION = ["Kings Canyon", "World's Edge", "Olympus"]
CHANGE_TIME = datetime.strptime("12:00", "%H:%M").time()

def get_current_ranked_map():
    current_time = datetime.now().time()
    if current_time >= CHANGE_TIME:
        elapsed_time = (current_time.hour - CHANGE_TIME.hour) * 60 + (current_time.minute - CHANGE_TIME.minute)
        map_index = (elapsed_time // (24 * 60)) % len(MAP_ROTATION)
        return MAP_ROTATION[map_index]
    else:
        return MAP_ROTATION[0]

@app.get("/apex/ranked-map")
async def get_ranked_map():
    global CURRENT_RANKED_MAP
    CURRENT_RANKED_MAP = get_current_ranked_map()
    return quart.Response(response=CURRENT_RANKED_MAP, status=200)

@app.get("/apex/get-future-map")
async def get_future_map():
    current_map = get_current_ranked_map()
    map_rotation = MAP_ROTATION
    change_time = CHANGE_TIME.strftime("%H:%M")
    info = {
        "current_map": current_map,
        "map_rotation": map_rotation,
        "change_time": change_time,
        "map_change": "the map changes every 24 hours at 12 pm CST"
    }
    return quart.jsonify(info)

# Links to the logo.png file in this repo
@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    # global CURRENT_RANKED_MAP
    # CURRENT_RANKED_MAP = get_current_ranked_map()
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
