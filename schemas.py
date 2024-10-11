from marshmallow import Schema, fields, validate

class WebtoonSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    summary = fields.Str(validate=validate.Length(max=500))

    characters = fields.List(fields.Str(validate=validate.Length(max=50)), missing=[])
