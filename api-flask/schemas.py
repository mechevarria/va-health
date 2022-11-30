from marshmallow import Schema, fields

class KpiCardSchema(Schema):
    name=fields.Str(required=True)
    value=fields.Float(required=True)


class FilterSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)

class CategoricalFilterSchema(FilterSchema):
    name=fields.Str(required=True)
    value=fields.Str(required=True)
    is_equal=fields.Bool(required=True)

class NumericFilterSchema(FilterSchema):
    name=fields.Str(required=True)
    min=fields.Float(required=True)
    max=fields.Float(required=True)