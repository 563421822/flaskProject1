from flask import jsonify, session
from sqlalchemy import func

from api import db
from api.lending.model import Lending
from api.utils.dic_util import model_to_dict


def ftch_lend():
    query = db.session.query(Lending)
    results = [model_to_dict(row) for row in query.all()]
    return ({"status": "success", 'code': 0, 'data': results, 'count': len(query.all())}), 200


def delete_lending(lending_id):
    r = db.session.delete(Lending.query.get(lending_id))
    db.session.commit()
    return jsonify({"status": "success", 'code': 0}), 200


def lend_bk(book_id):
    lending = Lending()
    lending.debtor_id = session.get("user_info")["id"]
    lending.book_id = book_id
    lending.lending_time = func.now()
    lending.state = True
    db.session.add(lending)
    db.session.commit()
    return jsonify({"status": "success", 'code': 0}), 200
