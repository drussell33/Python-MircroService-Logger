from flask import Flask, abort, request, url_for, jsonify
from datetime import datetime
from mongoengine import connect, StringField, IntField, DateTimeField, Document
import json
from bson.json_util import dumps, loads
import os
import dns
import time


app = Flask(__name__)

mongo_host = os.getenv('DB_HOST')
mongo_db = os.getenv('DB')
mongo_user = os.getenv('DB_USER')
mongo_password = os.getenv('DB_PASSWORD')

db = connect(db=os.environ.get("DB"), host=os.environ.get("DB_HOST"), username=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD") , port=27017)

sleep_time = os.getenv('SLEEP_TIME', default=0)

class activity_log(Document):
    user_id = IntField(required=True)
    username = StringField(required=True, max_length=64)
    timestamp = DateTimeField(default=datetime.utcnow)
    details = StringField(required=True)


@app.route("/api/activities/<int:activity_id>", methods=["GET"])
def activity(activity_id):
    logs = activity_log.objects.all().order_by('-timestamp').limit(activity_id).to_json()
    json_string = json.loads(logs)
    return jsonify(json_string)


@app.route("/api/activities", methods=["GET"])
def activities():
    logs = activity_log.objects.all().order_by('-timestamp').limit(10).to_json()
    json_string = json.loads(logs)
    return jsonify(json_string)


@app.route("/api/activities", methods=["POST"])
def new_incoming_activity():
    if not request.json:
        abort(400)
    new_activity = dumps(request.get_json())
    building_new_activity = loads(new_activity)
    if "user_id" not in building_new_activity or "username" not in building_new_activity:
        abort(400)
    this_activity_log = activity_log._get_collection()
    new_id = this_activity_log.insert_one(building_new_activity).inserted_id
    building_new_activity['_id'] = str(new_id)
    building_new_activity['timestamp'] = datetime.utcnow()
    building_new_activity['location'] = '/api/activities/' + str(new_id)
    my_query = {"_id": new_id}
    new_values = {"$set": {"timestamp": datetime.utcnow(), "location": '/api/activities/' + str(new_id)}}
    json_string = dumps(building_new_activity)
    this_activity_log.update_one(my_query, new_values)
    time.sleep(int(sleep_time))
    return jsonify(json_string), 201
