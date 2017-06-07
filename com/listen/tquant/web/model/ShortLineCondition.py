# coding: utf-8


class ShortLineCondition():
    def __init__(self, field_name, relation, field_value):
        self.field_name = field_name
        self.relation = relation
        self.field_value = field_value