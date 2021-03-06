# from games.cards.cards import Card, Deck, _suits, _classes
from games.cards.blackjack.player import BJPlayer

class BJDealer(BJPlayer):
    def __init__(self, deck):
        super().__init__(deck)

        self.critical_value = 23 # change to 23 be used to push at 22.
        self.stop_value = 17
        self.hit()


    def play(self):
        playing = True

        while playing:
            self.hit()

            if self.bust:
                break

            if self.is_push():
                break

            val = self.get_max_value()
            if val >= self.stop_value:
                playing = False

    def is_push(self):
        return self.get_min_value() == 22

#
# dealer = BJDealer(deck)
# self = dealer
# dealer.render()
# dealer.get_max_value()
#
# dealer.play()
#
# dealer.bust
#
# dealer.get_max_value()
# dealer.render()
