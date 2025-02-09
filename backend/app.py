import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import htmlmin

from .business import VRResource, RawResource
from .utils import load_template
from settings import JS_FOLDER, PATTERN_FOLDER, MEDIA_FOLDER

from icecream import ic
from random import randbytes
import pdb

app = Flask(__name__)


templates = {
    "list": "resources_list.html",
    "aframe": "aframe.html",
    "three": "three.html",
}


@app.route("/", methods=["GET"])
def get_resources():
    resources = VRResource.list()
    template = templates.get("list")
    text = render_template(template, resources=resources)
    return htmlmin.minify(text, remove_comments=True, remove_empty_space=True)


@app.route("/", methods=["POST"])
def upload_resource():
    try:
        name = request.form["name"]
        pattern = RawResource("pattern", request.files["pattern"].stream.read())
        media = RawResource("png", request.files["media"].stream.read())
        created_resource = VRResource.create(name=name, pattern=pattern, media=media)
        return jsonify(created_resource.public_info), 201
    except KeyError as err:
        return jsonify({"error": "no complete data in multipart form"}), 422
    except Exception as err:
        return jsonify({"error": f"found error {type(err)}"}), 500


@app.route("/st/<content_type>/<filename>", methods=["GET"])
def statics(content_type: str, filename: str):
    resource_mapping = {
        "js": JS_FOLDER,
        "pattern": PATTERN_FOLDER,
        "media": MEDIA_FOLDER,
    }
    folder = resource_mapping.get(content_type, None)
    if folder:
        return send_from_directory(folder, filename)
    else:
        return jsonify({"error": f"file {filename} dont exist"}), 404


@app.route("/vr/aframe/<res_id>", methods=["GET"])
def get_aframe(res_id: str):
    # This function should fetch data for A-Frame based on ID from a database or storage
    resource = VRResource(res_id)
    template = templates.get("aframe")
    text = render_template(template, resource=resource)
    return htmlmin.minify(text, remove_comments=True, remove_empty_space=True)


# @app.route("/tree/<int:id>", methods=["GET"])
# def get_tree(id):
#     # This function should fetch data for Tree structure based on ID from a database or storage
#     return jsonify({"message": "Fetching Tree structure resource"}), 200
