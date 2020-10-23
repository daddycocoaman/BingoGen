import pathlib
import platform
import azure.functions as func
import pandas as pd
import imgkit
from random import sample

curdir = pathlib.Path(__file__).parent
staticdir = curdir / "static"
bindir = curdir / "binaries"
listdir = curdir / "lists"
dist = platform.system()
print(dist)

if dist == "Linux":
    imgconfig = imgkit.config(wkhtmltoimage=bindir / "wkhtmltoimage-nix")
elif dist == "Windows":
    imgconfig = imgkit.config(wkhtmltoimage=bindir / "wkhtmltoimage-win.exe")

typeDict  = {
                "conference": ["Conference Call", listdir / "conference.txt", staticdir / "conference.css"],
                "replystorm": ["Reply Storm", listdir / "replystorm.txt", staticdir / "replystorm.css"],
                "kjlife": ["KJ Life", listdir / "kjlife.txt", staticdir / "kjlife.css"],
                "mitreattack": ["MITRE ATT&CK", listdir / "mitreattack.txt", staticdir / "mitreattack.css"],
                "presdebate": ["Presidental Debate 2020", listdir / "presdebate.txt", staticdir / "presdebate.css"]
            }

FREE_SPACES = ["kjlife"]
def main(req: func.HttpRequest) -> func.HttpResponse:

    card = typeDict.get(req.params.get("type"), None)
    if card:
        phrases = open(card[1]).read().splitlines()

        opts = sample(phrases, 25)
        entries = [opts[i:i+5] for i in range(0, 25, 5)]

        # Handle FREE SPACE slots
        if req.params.get("type") in FREE_SPACES:
            entries[2][2] = "FREE"
        elif req.params.get("type") == "mitreattack":
            entries[2][2] = "POWERSHELL"
        elif req.params.get("type") == "presdebate":
            entries[2][2] = "SOCIALIST SPACE"

        df = pd.DataFrame(entries)
        pd.set_option('display.width', 300)
        html = f"""
                <h1>{card[0]} Bingo Card</h1>
                {df.to_html(index=False, header=False)}
                """

        response = imgkit.from_string(html, False, css=card[2], config=imgconfig)
        return func.HttpResponse(response, mimetype="image/png")
    else:
        return func.HttpResponse(status_code=404)

