import ayasdi.core as ac
from flask import jsonify


class GraphService():

    def get(self):
        data = [
            {'from': 'A', 'to': 'C'},
            {'from': 'A', 'to': 'D'},
            {'from': 'A', 'to': 'E'},
            {'from': 'A', 'to': 'F'},
            {'from': 'A', 'to': 'G'},
            {'from': 'B', 'to': 'C'},
            {'from': 'B', 'to': 'D'}
        ]
        return jsonify(data)
