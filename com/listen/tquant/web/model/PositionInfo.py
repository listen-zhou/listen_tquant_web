# coding: utf-8


class PositionInfo():
    def __init__(self, position_hands, left_money, close):
        self.position_hands = position_hands
        self.left_money = left_money
        self.close = close

    def get_total_money(self):
        return self.position_hands * 100 * self.close + self.left_money