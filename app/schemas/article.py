from marshmallow import Schema, fields


class ArticleBaseSchema(Schema):
    title = fields.Str()
    content = fields.Str()


class ArticleResponseSchema(ArticleBaseSchema):
    id = fields.Int(required=True)
    author_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime()


class ArticleCreateSchema(ArticleBaseSchema): ...


class ArticleUpdateSchema(ArticleBaseSchema): ...


class ArticleSearchSchema(Schema):
    title = fields.Str(required=True)
