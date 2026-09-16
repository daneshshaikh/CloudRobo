from flask import Flask, jsonify, render_template
import subprocess
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/retrieve/<cid>")
def retrieve(cid):

    try:

        result = subprocess.check_output(
            ["ipfs", "cat", cid],
            text=True
        )

        data = json.loads(result)

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 404


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
