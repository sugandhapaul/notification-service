from flask import Flask, request, jsonify
from models import db, Notification
from config import Config
from tasks import send_notification_task

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/notifications", methods=["POST"])
def send_notification():
    data = request.json
    notification = Notification(
        user_id=data["user_id"],
        type=data["type"],
        message=data["message"]
    )
    db.session.add(notification)
    db.session.commit()
    send_notification_task.delay(notification.id)  # Asynchronous
    return jsonify({"message": "Notification queued"}), 202

@app.route("/users/<int:user_id>/notifications", methods=["GET"])
def get_notifications(user_id):
    notes = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": n.id,
        "type": n.type,
        "message": n.message,
        "status": n.status,
        "timestamp": n.timestamp
    } for n in notes])

if __name__ == "__main__":
    app.run(debug=True)

