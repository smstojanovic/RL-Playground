from itertools import product

class BJPlayer:
    def __init__(self, deck):
        self._deck = deck
        self.bust = False

        self.hand = []
        self.values = [0]

        self.critical_value = 22

    def hit(self, verbose = False):
        if self.bust:
            raise EnvironmentError('Player is bust.')

        card = self._deck.draw()
        self.hand.append(card)
        if verbose:
            card.render()

        add_vals = []
        for i in range(card.get_num_values()):
            add_vals += [card.get_value(i)]

        self.values = [ v+nv for v,nv in product(self.values, add_vals) if v+nv < self.critical_value]

        if len(self.values) == 0:
            self.bust = True

    def get_values_from_hand(self):
        values = [0]

        for card in self.hand:
            add_vals = []
            for i in range(card.get_num_values()):
                add_vals += [card.get_value(i)]

            values = [ v+nv for v,nv in product(values, add_vals)]

        return values

    def is_bust(self):
        return self.bust

    def get_max_value(self):
        try:
            return max(self.values)
        except:
            return min(self.get_values_from_hand())

    def get_num_values(self):
        return len(self.values)

    def get_values(self):
        return self.values

    def get_hand(self):
        return self.hand

    def render(self):
        for card in self.hand:
            card.render()

#
# player = BJPlayer(deck)
# player.hit(True)
#
# player.bust
#
# player.render()
#
# player.get_values()

# values = [1,11]
#
# add_values = [1,11]
