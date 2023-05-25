import quart
import quart_cors
from quart import request
from datetime import datetime, timedelta
import datetime


app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of the current ranked map.
CURRENT_RANKED_MAP = ""

# Define the map rotation and change time.
MAP_ROTATION = ["Kings Canyon", "World's Edge", "Olympus"]

def get_current_ranked_map():
    # Get the current date (year, month, day)
    current_date = datetime.datetime.now().date()

    # Subtract a base date (the date when "Kings Canyon" was the map)
    base_date = datetime.date(2023, 5, 25)  # replace with the actual date when "Kings Canyon" was the map
    days_passed = (current_date - base_date).days

    # Use the number of days passed to determine the map
    map_index = days_passed % len(MAP_ROTATION)
    
    return MAP_ROTATION[map_index]

@app.get("/apex/ranked-map")
async def get_ranked_map():
    global CURRENT_RANKED_MAP
    CURRENT_RANKED_MAP = get_current_ranked_map()
    return quart.Response(response=CURRENT_RANKED_MAP, status=200)

@app.get("/apex/predict-future-map")
async def predict_future_map():
    current_map = get_current_ranked_map()
    map_rotation = MAP_ROTATION
    current_time = datetime.datetime.now()
    info = {
        "start_date": "The map rotation started on May 25th 2023 at 11:30 am CST with Olympus. At 12:01 PM CST on May 25th 2023, the map is Kings Canyon.",
        "current_map": current_map,
        "map_rotation": map_rotation,
        "current_time": current_time,
        "map_change": "the map changes every 24 hours at 12 pm CST"
    }
    return quart.jsonify(info)

## Below is the GPT side of the code.

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
