# coding: utf-8


class ShortLineCondition():
    def __init__(self, field_name, relation, field_value):
        self.field_name = field_name
        self.relation = relation
        self.field_value = field_value

    def to_string(self):
        dict_item = {}
        dict_item['field_name'] = self.field_name
        dict_item['relation'] = self.relation
        dict_item['field_value'] = self.field_value
        return dict_item