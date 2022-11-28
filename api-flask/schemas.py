from marshmallow import Schema, fields

class KpiCardSchema(Schema):
    name=fields.Str(required=True)
    value=fields.Float(required=True)