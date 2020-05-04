# from games.cards.cards import Card, Deck, _suits, _classes
from games.cards.blackjack.player import BJPlayer

class BJDealer(BJPlayer):
    def __init__(self, deck):
        super().__init__(deck)

        self.critical_value = 22 # change to 23 be used to push at 22.
        self.stop_value = 17
        self.hit()


    def play(self):
        playing = True

        while playing:
            self.hit()

            if self.bust:
                break

            val = self.get_max_value()
            if val >= self.stop_value:
                playing = False


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
