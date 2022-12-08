from marshmallow import Schema, fields

class KpiCardSchema(Schema):
    name=fields.Str(required=True)
    value=fields.Float(required=True)

class ExplainerSchema(Schema):
    id=fields.Str(required=True)
    name=fields.Str(required=True)
    group_size=fields.Int(required=True)
    explains=fields.List(fields.String(required=True))

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

class GraphDataSchema(Schema):
    # from = fields.Str(Required=True)
    to = fields.Str(Required=True)

class GraphNodeSchema(Schema):
    id = fields.Str(Required=True)
    colorIndex = fields.Float(Required=True)
    radius = fields.Float(Required=True)

class NetworkSchema(Schema):
    filter_id=fields.Str(required=False)
    color_name=fields.Str(required=True)
    # data=fields.List(dump_only=True)
    # nodes=fields.Nested(GraphNodeSchema(), dump_only=True)
