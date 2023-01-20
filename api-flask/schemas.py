from marshmallow import Schema, fields, validate

class KpiCardSchema(Schema):
    name=fields.Str(required=True)
    value=fields.Str(required=True)

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
    percentage=fields.Bool(required=False)

class AppliedFilter(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(dump_only=True)
    msg=fields.Str(dump_only=True, required=False)
    filters=fields.Nested(FilterSchema, required=False, many=True)
    cohort=fields.Bool(required=False)

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
    simplified=fields.Bool(required=True)
    # data=fields.List(dump_only=True)
    # nodes=fields.Nested(GraphNodeSchema(), dump_only=True)

class DetailedPatientSchema(Schema):
    patient_id=fields.Str(required=True)
    neighbor_criteria = fields.Str(validate=validate.OneOf(["meds", "visits"]), required=True)
    medicine_threshold = fields.Int(required=True)

class PatientCardSchema(Schema):
    ID=fields.Str(required=True)
    Gender=fields.Str(required=True)
    Age=fields.Int(required=True)
    Vaccination_Status=fields.Float(required=True)
    Race=fields.Str(required=True)
    Ethnicity=fields.Str(required=True)
    Marital_Status=fields.Str(required=True)
    Rurality=fields.Str(required=True)
    A1C_Increase_Risk=fields.Str(required=True)
    Engagement_Decrease_Risk=fields.Str(required=True)