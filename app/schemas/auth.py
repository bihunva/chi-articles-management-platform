from marshmallow import Schema, fields


class AuthBaseSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterSchema(AuthBaseSchema): ...


class RegisterResponseSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)


class LoginSchema(AuthBaseSchema): ...


class LoginResponseSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class RefreshBaseSchema(Schema):
    refresh_token = fields.Str(required=True)


class RefreshSchema(RefreshBaseSchema): ...


class RefreshResponseSchema(RefreshBaseSchema):
    access_token = fields.Str(required=True)
