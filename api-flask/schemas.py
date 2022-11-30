from marshmallow import Schema, fields

class KpiCardSchema(Schema):
    name=fields.Str(required=True)
    value=fields.Float(required=True)


class FilterSchema(Schema):
    name=fields.Str(required=True)

    categorical = fields.Bool(required=True)
    value=fields.Str(required=False)
    is_equal=fields.Bool(required=False)
    
    min=fields.Float(required=False)
    max=fields.Float(required=False)

class AppliedFilter(Schema):
    id=fields.Str(required=True)
    name=fields.Str(required=True)
    