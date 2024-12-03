from marshmallow import Schema, fields, validate

from app.models.user import Role


class UserBaseSchema(Schema):
    username = fields.Str(required=True)
    role = fields.Str(required=True, validate=validate.OneOf([role.value for role in Role]))


class UserResponseSchema(UserBaseSchema):
    id = fields.Int(required=True)


class CreateUserSchema(UserBaseSchema):
    password = fields.Str(required=True)


class UpdateUserSchema(UserBaseSchema):
    username = fields.Str()
