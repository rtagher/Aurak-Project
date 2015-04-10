import random
from itertools import product

##suit_symbols = {0: u'\u2663', 1: u'\u2666', 2: u'\u2665', 3: u'\u2660'}
##suit_symbols = {0: u'\u2667', 1: u'\u2662', 2: u'\u2661', 3: u'\u2664'}
##suit_symbols = {0: u'\u2663', 1: u'\u2662', 2: u'\u2661', 3: u'\u2660'}
suit_symbols = {0: u'\u2667'.encode('utf-8'), 1: u'\u2666'.encode('utf-8'),
                2: u'\u2665'.encode('utf-8'), 3: u'\u2664'.encode('utf-8')}
suit_letters = {0: 'c', 1: 'd', 2: 'h', 3: 's'}
rank_symbols = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
                9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

class Card(object):

    cardCount = 0

    def __init__(self, rank, suit, suit_symbols = True):
        self.rank = rank
        self.suit = suit
        self.suit_symbols = suit_symbols
        Card.cardCount += 1

    def __str__(self):
        return '%s%s' % (rank_symbols[self.rank], suit_letters[self.suit])

    def face(self):
        if self.suit_symbols == True:
            return '%s%s' % (rank_symbols[self.rank], suit_symbols[self.suit])
        else:
            return '%s%s' % (rank_symbols[self.rank], suit_letters[self.suit])

    def get_value(self):
        return (self.rank - 2) + 13 * self.suit

    def print_count(self):
        print 'Number of cards: %s' % Card.cardCount

    def print_info(self):
        print 'Rank: %s Suit: %s' % (self.rank, self.suit)

    def get_face(self):
        face = self.face()
        if len(face) == 2:
            return face + ' '
        else:
            return face


class DurakDeck(object):

    ranks = range(6,15)
    suits = range(4)

    def __init__(self, suit_symbols = True):
        ##self.suits = ['c', 'd', 'h', 's']
        self.cards = []
        for i in self.ranks:
            for j in self.suits:
                self.cards.append(Card(i,j, suit_symbols))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_cards(self, player_list, number_to_deal = 52):
        i = 0
        num_players = len(player_list)
        for i in range(number_to_deal):
            player_list[i % num_players].add_card(self.cards.pop())
            i += 1

    def draw_cards(self, num):
        draw = []
        for i in range(num):
            draw.append(self.cards.pop())
            if len(self.cards) == 0:
                break
        return draw

    def print_deck(self):
        string = ''
        for card in self.cards:
            string += card.print_face()
        return string

    def print_deck_row(self):
        count = 0
        string = ''
        for card in self.cards:
            string += card.print_face() + ' '
            if count % 33 == 32:
                string += '\n'
            count += 1
        return string

    def get_size(self):
        return len(self.cards)


class Player(object):

    def __init__(self, index, draw_length):

        self.index = index
        self.hand = []
        self.deck = []
        self.bids_won = []
        self.cards_won = []
        self.trump_card = None
        self.trump = 3
        self.suit_order = []
        self.status = 'active'
        self.draw_length = draw_length
        self.initial_draw_length = 13

    def reset_status(self):
        self.status = 'active'

    def assign_trump(self, trump):
        self.trump = trump

    def assign_trump_card(self, trump_card):
        self.trump_card = trump_card
        self.trump = trump_card.suit

    def reset_trump_card(self):
        self.trump_card = None
        self.trump = 3

    def assign_bot(self, bot):
        self.bot = bot

    def get_values(self):
        values = []
        for card in self.hand:
            values.append(card.get_value())
        return values

    def sort_hand_suit(self):
        def compare_cards_suit(card1, card2):
            s1 = card1.suit
            s2 = card2.suit
            if s1 == self.trump and s2 == self.trump:
                return cmp(card1.rank, card2.rank)
            if s1 == self.trump:
                return 1
            if s2 == self.trump:
                return -1
            ## Compare by suit. If that ties, compare by rank
            if cmp(s1, s2) != 0:
                return cmp(s1, s2)
            else:
                return cmp(card1.rank, card2.rank)
        self.hand = sorted(self.hand, cmp = compare_cards_suit)

    def sort_hand_suit_order(self):
        def compare_cards_suit_order(card1, card2):
            s1 = self.suit_order.index(card1.suit)
            s2 = self.suit_order.index(card2.suit)
            ## Compare by suit (custom order)
            if cmp(s1, s2) != 0:
                return cmp(s1, s2)
            ## If that ties, compare by rank
            else:
                return cmp(card1.rank, card2.rank)
        self.hand = sorted(self.hand, cmp = compare_cards_suit_order)

    def sort_hand_rank(self):
        def compare_cards_rank(card1, card2):
            s1 = card1.suit
            s2 = card2.suit
            r1 = card1.rank
            r2 = card2.rank
            if s1 == self.trump and s2 == self.trump:
                return cmp(card1.rank, card2.rank)
            if s1 == self.trump:
                return 1
            if s2 == self.trump:
                return -1
            ##Compare by rank. If that ties, compare by suit
            if cmp(r1, r2) != 0:
                return cmp(r1, r2)
            else:
                return cmp(s1, s2)
        self.hand = sorted(self.hand, cmp = compare_cards_rank)

    def sort_hand(self):
        def compare_cards_rank(card1, card2):
            s1 = card1.suit
            s2 = card2.suit
            r1 = card1.rank
            r2 = card2.rank
            ##Compare by rank. If that ties, compare by suit
            if cmp(r1, r2) != 0:
                return cmp(r1, r2)
            else:
                return cmp(s1, s2)
        self.hand = sorted(self.hand, cmp = compare_cards_rank)

    def add_card(self, card):
        self.hand.append(card)
        self.sort_hand()
        self.status = 'active'

    def extend_hand(self, card_list):
        self.hand.extend(card_list)
        self.sort_hand()
        self.status = 'active'

    def remove_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            if len(self.hand) == 0:
                self.status = 'empty'
        else:
            print 'Error: card %s not in player %d\'s hand.' % (card, self.index)

    def play(self, mode, trump_card = None, bot_card = None):
        if mode not in ['trump', 'bot'] and self.hand == []:
            print 'Error: can\'t play from empty hand.'
            print 'Player ' + str(self.index + 1)
            for p in empty_list:
                print 'Empty: player ' + str(self.index + 1)
            inp = raw_input(' ')
            return 'error'
        inp = ''
        while True:
            if mode == 'bid':
                inp = raw_input('Choose a bid card: ')
            elif mode == True:
                inp = raw_input('Player ' + str(self.index + 1) + ' attack: ')
            else:
                inp = raw_input('Player ' + str(self.index + 1) + ' defend: ')
            if inp == '':
                print 'Error: no input'
                continue
            elif inp.lower() in ['x', 'p', 'pass', 'n', 'take']:
                self.status = 'pass'
                return 'pass'
            elif inp[-1] in 'cdhsCDHS':
                ## Fix so that JQKA are recognized (upper or lower)
                ## and both suit/rank are converted to integers for comparison
                input_rank = inp[:-1].upper()
                if input_rank not in rank_symbols.values():
                    print 'Error: value'
                    continue
                input_suit = inp[-1].lower()
                for card in self.hand:
                    if (rank_symbols[card.rank] == input_rank and
                        suit_letters[card.suit] == input_suit):
                        return card
                print 'Error: not in player %d\'s hand' % (self.index + 1)
                continue
            else:
                try:
                    input_index = int(inp)
                except ValueError:
                    print 'Error: value'
                    continue
                if input_index in range(1, len(self.hand) + 1):
                    return self.hand[input_index - 1]
                else:
                    print ('Error: player %d has fewer than %d cards' %
                           (self.index + 1, input_index))
                    continue

    def draw_from_deck(self, deck):
        if len(deck.cards) <= self.draw_to - len(self.hand):
            self.extend_hand(deck.draw_cards(len(deck.cards)))
        else:
            self.extend_hand(deck.draw_cards(self.draw_to - len(self.hand)))

    def draw(self):
        while len(self.hand) < self.draw_length:
            if len(self.deck) == 0:
                break
            self.hand.append(self.deck.pop(0))
        self.sort_hand_suit_order()
        return

    def print_hand_faces(self):
        for card in self.hand:
            print card.face()

    def print_hand_faces_row(self, row = None, cards_per_row = 6):
        string = ''
        if row == None:
            for card in self.hand:
                string += card.print_face() + ' '
        else:
            print_list = self.hand[(row * cards_per_row):
                                   ((row + 1)* cards_per_row)]
            space = cards_per_row - len(print_list)
            if row == 0:
                for i in range(space):
                    string += '  '
                for card in print_list:
                    string += card.print_face() + ' '
                for i in range(space):
                    string += '  '
            else:
                for i in range(cards_per_row - len(print_list)):
                    string += ' ' * 4
                for card in print_list:
                    string += card.print_face() + ' '
        return string

    def print_hand(self):
        string = ''
        for card in self.hand:
            string += card.face() + '\n'
        return string

    def print_bids_won(self):
        string = ''
        for card in self.bids_won:
            string += card.print_face() + ' '
        return string

    def assign_suit_order(self, table):
        self.suit_order = []
        for j in range(len(table.player_count)):
            new_suit = table.player_list[(player.index + j) % table.player_count].trump
            if new_suit not in player.suit_order and suit != 5:
                player.suit_order.append(new_suit)
        for j in range(4)[::-1]:
            if j not in player.suit_order:
                player.suit_order.append(j)


class Table(object):

    def __init__(self, player_count = 4, deck_length = 36, draw_length = 4, dealer = 0,
                 initial_attacker = None):
        self.attacks = []
        self.defenses = []
        self.attackers = []
        self.trump = 4
        self.trump_card = []
        self.bot = 4
        self.bot_card = []
        self.attack_count = 0
        self.discard_pile = []
        self.attacker = None
        self.defender = None
        self.player_count = player_count
        self.deck_length = deck_length
        self.draw_length = cards_per_player
        self.dealer = dealer
        self.initial_attacker = initial_attacker
        self.player_list = []
        self.message = ''

    def assign_trump(self, trump):
        self.trump = trump

    def assign_bot(self, bot):
        self.bot = bot

    def find_initial_attacker(self, player_list, initial_attacker,
                              special_suit = 3):
        if initial_attacker == None:
            for rank in range(2,14):
                for player in player_list:
                    for card in player.hand:
                        if card.rank == rank and card.suit == special_suit:
                            self.initial_attacker = player
                            return
            self.initial_attacker = player_list[0]
            return
        self.initial_attacker = player_list[(initial_attacker.index + 1)
                                            % len(player_list)]
        return

    def find_next_attacker(self, attacker, player_list):
        for i in range(len(player_list) - 1):
            if player_list[(attacker.index + i) %
                           len(player_list)].status == 'active':
                return player_list[(attacker.index + i) % len(player_list)]

    def find_defender(self, attacker, player_list):
        for i in range(len(player_list) - 1):
            if player_list[(attacker.index + i + 1) %
                           len(player_list)].status == 'active':
                return player_list[(attacker.index + i + 1) % len(player_list)]

    def defense_validity(self, attack, defense, trump = None, bot = None):
        if trump == None:
            trump = self.trump_card.suit
        if bot == None:
            bot = self.bot_card.suit
        if ((defense.suit == attack.suit and defense.rank > attack.rank) or
            (defense.suit == trump and attack.suit != trump) or
            (defense.suit != bot and attack.suit == bot)):
            return True
        return False

    def trump_validity(self, trump, defense = None):
        if trump == self.bot_card.suit:
            print 'Trump and bitch cannot be the same suit.'
            return False
        for i in range(len(self.defenses)):
            if (self.defense_validity(self.attacks[i], self.defenses[i], trump, None)
                == False):
                return False
        if defense != None:
            if (self.defense_validity(self.attacks[-1], defense, trump, None)
                == False):
                return False
        return True

    def bot_validity(self, bot, defense = None):
        if bot == self.trump_card.suit:
            print 'Trump and bitch cannot be the same suit.'
            return False
        for i in range(len(self.defenses)):
            if (self.defense_validity(self.attacks[i], self.defenses[i], None, bot)
                == False):
                return False
        if defense != None:
            if (self.defense_validity(self.attacks[-1], defense, None, bot)
                == False):
                return False
        return True

    def check_attack(self, attack, attacker, replacement = None):
        if attack == 'pass':
            if self.attacks != []:
                return True
            print 'Passing not allowed.'
            return False
        ## If attacker chose a card to play
        elif isinstance(attack, Card):
            ## Check whether it's a valid attack
            if len(self.attacks) > 0 and not any(attack.rank == c.rank
                                                 for c in (self.attacks +
                                                           self.defenses)):
                print 'Attack invalid, try again.'
                return False
            return True
        print 'Not a card ???'
        return False

    def process_attack(self):
        while True:
            if len(message) > 0:
                print message
            attack = attacker.play(True)
            ## If attacker chose to pass, move to next attacker
            ## (attacker cannot pass if no cards are on the table)
            if self.check_attack(attack, attacker) == False:
                continue
            if attack == 'pass':
                attacker.status = 'pass'
                return False
            ## If attacker chose a valid card
            self.attack_count += 1
            self.add_attack(attack)
            attacker.remove_card(attack)
            if attacker not in self.attackers:
                self.attackers.append(attacker)
            if defender.status == 'pass':
                return False
            return True

    def check_defense(self, defense, replacement = None):
        if defense == 'pass':
            return True
        elif not isinstance(defense, Card):
            print 'Defense invalid.'
            return False
        if self.defense_validity(self.attacks[-1], defense):
            return True
        print 'Defense invalid, try again.'
        return False

    def process_defense(self, player_list, attacker, defender, message):
        while True:
            if len(message) > 0:
                print message
                message = ''
            defense = defender.play(False)
            if self.check_defense(defense) == False:
                continue
            ## If defender chose to take cards
            if defense == 'pass':
                # Initiate card dump phase
                defender.status = 'pass'
                for p in player_list:
                    if (p != defender and p.status == 'pass'):
                        p.status = 'active'
                print ('Player %d taking cards.' %
                           (defender.index + 1))
                return
            # If defender played a card
            else:
                self.add_defense(defense)
                defender.remove_card(defense)
                return

    def end_condition(deck, player_list):
        if len(deck.cards) > 0:
            return False
        else:
            for player in player_list:
                if len(player.hand) > 0:
                    return False
            return True

    def add_attack(self, card):
        self.attacks.append(card)

    def add_defense(self, card):
        self.defenses.append(card)

    def clear_table(self):
        self.attacks = []
        self.defenses = []

    def discard_all(self):
        self.discard_pile.extend(self.attacks + self.defenses)
        self.clear()

    def print_attacks_row(self, num_cards = 6):
        string = ''
        for card in self.attacks:
            string += card.print_face() + ' '
        string += ' ' * (4 * (num_cards - len(self.attacks)))
        return string

    def print_defenses_row(self, num_cards = 6):
        string = ''
        for card in self.defenses:
            string += card.print_face() + ' '
        string += ' ' * (4 * (num_cards - len(self.defenses)))
        return string

    def bidding_phase(self):
        for i in range(len(self.player_count)):
            bid = self.player_list[(self.attacker.index + i) %
                                   self.player_count].bid()
            self.bid_list.append(bid)

    def assign_suit_orders(self):
        ## assign trump orders for each player
        for i in range(len(self.player_count)):
            player = self.player_list[(self.attacker.index + i) % self.player_count]
            player.assign_suit_order(self)

    def deck_build_phase(self, manual_build = [False]*player_count]):
        for i in range(self.player_count):
            index = (self.dealer.index + 1 + i) % self.player_count
            if manual_build[index] == False:
                self.autobuild_deck(self.player_list[index])
            else:
                print 'Manual deck building not yet implemented. Restart game.'
            self.player_list[index].sort_hand_suit_order()
        return

    def autobuild_deck(self, player):
        random.shuffle(player.hand)
        for i in range(len(player.hand) - self.draw_length):
            player.deck.append(player.hand.pop(0))
        return

    def play_phase(self):
        while True:
            self.initialize_turn()
            self.play_turn()
            print_board(self.durak, self, player_list, cards_per_row, self.defender,
                        print_mode)

            ## self.finalize_turn()
            ## Cards on table are discarded or put into defender's hand
            ## Then defender draws cards if necessary and initiative is passed
            if self.defender.status == 'pass':
                ## self.defender.status = 'active'
                ## add cards to defender's hand in Rak!
                self.defender.extend_hand(self.attacks + self.defenses)
                self.clear_table()
                self.initial_attacker = self.player_list[(self.defender.index + 1)
                                                           % self.player_count]
                ##for i in range(self.player_count - 1):
                ##    if self.player_list[(self.defender.index + 1 + i) %
                ##                   self.player_count].status in ['active', 'pass']:
                ##        self.attacker = player_list[(self.defender.index + i + 1) %
                ##                               self.player_count]
                ##        break
            else:
                self.defender.winnings.append(self.attacks + self.defenses)
                self.clear_table()
                self.initial_attacker = self.defender
            ## This is the draw phase for both attackers and defenders
            self.draw_phase()
            ## Put players in out list if out of cards, then reset (passed not out)
            ## players to active
            ##
            ## Check for end of game
            self.update_player_statuses()
            ## self.update_out_list
            ##for player in self.player_list:
            ##    if player.status == 'empty' and player not in self.out_list:
            ##        self.out_list.append(player)
            if len(self.out_list) == 3 or len(self.out_list) == 4:
                break

    def initialize_turn(self):
        self.attackers = []
        self.attack_count = 0
        for player in self.player_list:
            if player.status == 'pass':
                player.status = 'active'
        self.find_next_attacker(self.attacker, self.player_list)
        self.find_defender(self.attacker, self.player_list)
        self.trump = self.defender.trump
        max_attacks = min(self.defender.initial_draw_length,
                          len(self.defender.hand),
                          self.defender.trump_card.rank)

    def play_turn(self):
        while (self.attack_count < self.draw_length and
               any((a.status == 'active') for a in self.player_list if
                   a != self.defender)):
            if self.attack_phase() == False:
                continue
            self.defense_phase()

    def draw_phase(self):
        if len(message) > 0:
            print message
            message = ''
        raw_input('Press Enter when ready for draw phase. ')
        for player in self.attackers:
            if len(player.hand) < player.draw_length and len(player.deck) > 0:
                player.draw()
        if len(defender.hand) < defender.draw_length and len(defender.deck) > 0:
            defender.draw()

    def attack_phase(self):
        ## If attacker passed or the attack just got passed
        ## to an ineligible player, find the next active attacker
        while (self.attacker == self.defender or
               self.attacker.status != 'active'):
            self.attacker = self.player_list[(self.attacker.index + 1) %
                                   self.player_count]
        print_board(self.durak, self, player_list, cards_per_row,
                    self.defender, print_mode)
        if len(message) > 0:
            print message
            message = ''
        ## Ask attacker for his move and record whether to prompt for
        ## a defense
        return self.process_attack()

    def defense_phase(self):
        ## If defense is required, reset all passed players to active
        for player in self.player_list:
            if player.status == 'pass':
                player.status = 'active'
        ## Initiate defense stage
        ## Print game board
        print_board(self.durak, self, player_list, cards_per_row, self.defender,
                    print_mode)
        if len(message) > 0:
            print message
            message = ''
        ## Ask defender for his move
        self.process_defense(self.player_list, self.attacker, self.defender,
                                        message)


def print_board(deck, table, player_list, cards_per_row, defender = None,
                mode = 'list'):

    if mode == 'list':
        print '-' * 101
    else:
        print '-' * 124
    print '\n'
    ## Print player 3 hand
    line = ''
    if mode == 'list':
        rows2 = [player_list[2].print_hand_faces_row(i, cards_per_row)
                 for i in range(4)]
        ner2 = 4
        for i in range(4)[::-1]:
            line = ' ' * 39
            if rows2[i] == ' ' * 4 * cards_per_row:
                ner2 = i
                line += rows2[i]
            else:
                line += rows2[ner2 - 1 - i]
            line += ' ' * 10
            print line[:-1]
    elif mode == 'grid':
        for i in range(4)[::-1]:
            line = ' ' * 57
            suit = player_list[2].suit_order[i]
            line += suit_symbols[suit] + ' '
            for j in range(13):
                if suit * 13 + j in player_list[2].get_values():
                    if len(rank_symbols[j + 2] + suit_symbols[suit]) == 2:
                        line += '%s%s  ' % (rank_symbols[j + 2],
                                            suit_symbols[suit])
                    else:
                        line += '%s%s ' % (rank_symbols[j + 2],
                                           suit_symbols[suit])
                else:
                    line += ' ' * 4
            line += ' ' * 10
            print line
    print
    line = ' ' * 44
    if mode == 'grid':
        line += ' ' * 32
    if defender != None:
        if 2 == defender.index:
            line += ('**Player ' + str(2 + 1) + '**')
        else:
            line += ('  Player ' + str(2 + 1) + '  ')
    else:
        line += ('  Player ' + str(2 + 1) + '  ')
    line += ' ' * 10
    print line
    ## Print deck
    print '\n\n'
    line = ' ' * 46
    if mode == 'grid':
        line += ' ' * 32
    line += 'Trump: %s' % table.trump_card.face()
    print line
    '''line = ' ' * 46
    if mode == 'grid':
        line += ' ' * 12
    line += 'Bitch: %s' % table.bot_card.face()
    print line'''
    line = ' ' * 41
    if mode == 'grid':
        line += ' ' * 32
    if len(deck.cards) == 0 or len(deck.cards) == 1:
        line += 'No cards face down '
    elif len(deck.cards) == 2:
        line += ' 1 card face down  '
    elif len(str(len(deck.cards) - 1)) == 1:
        line += str(len(deck.cards) - 1) + ' cards face down  '
    else:
        line += str(len(deck.cards) - 1) + ' cards face down '
    print line
    ## Players 2 and 4
    if mode == 'list':
        rows1 = [player_list[1].print_hand_faces_row(i, cards_per_row)
                 for i in range(4)]
        rows3 = [player_list[3].print_hand_faces_row(i, cards_per_row)
                 for i in range(4)]
        ner1 = 4
        ner3 = 4
        for i in range(4)[::-1]:
            line = ' ' * 1
            if rows1[i] == ' ' * 4 * cards_per_row:
                ner1 = i
                line += rows1[i]
            else:
                line += rows1[ner1 - 1 - i]
            line += ' ' * 52
            if rows3[i] == ' ' * 4 * cards_per_row:
                ner3 = i
                line += rows3[i]
            else:
                line += rows3[ner3 - 1 - i]
            print line[:-1]
    elif mode == 'grid':
        for i in range(4)[::-1]:
            line = ' ' * 1
            suit = player_list[1].suit_order[i]
            line += suit_symbols[suit] + ' '
            for j in range(13):
                if suit * 13 + j in player_list[1].get_values():
                    if len(rank_symbols[j + 2] + suit_symbols[suit]) == 2:
                        line += '%s%s  ' % (rank_symbols[j + 2],
                                            suit_symbols[suit])
                    else:
                        line += '%s%s ' % (rank_symbols[j + 2],
                                           suit_symbols[suit])
                else:
                    line += ' ' * 4
            '''if i in [2,3]:'''
            line += ' ' * 60
            '''elif i == 1:
                line += ' ' * 14
                line += table.print_defenses_row()
                line += ' ' * 14
            elif i == 0:
                line += ' ' * 14
                line += table.print_attacks_row()
                line += ' ' * 14
            '''
            suit = player_list[3].suit_order[i]
            line += suit_symbols[suit] + ' '
            for j in range(13):
                if suit * 13 + j in player_list[3].get_values():
                    if len(rank_symbols[j + 2] + suit_symbols[suit]) == 2:
                        line += '%s%s  ' % (rank_symbols[j + 2],
                                            suit_symbols[suit])
                    else:
                        line += '%s%s ' % (rank_symbols[j + 2],
                                           suit_symbols[suit])
                else:
                    line += ' ' * 4
            print line[:-1]
    print
    line = ' ' * 6
    if mode == 'grid':
        line += ' ' * 14
    if defender != None:
        if 1 == defender.index:
            line += ('**Player ' + str(1 + 1) + '**')
        else:
            line += ('  Player ' + str(1 + 1) + '  ')
    else:
        line += ('  Player ' + str(1 + 1) + '  ')
    line += ' ' * 21
    if mode == 'grid':
        line += ' ' * 38
    line += table.print_defenses_row()
    line += ' ' * 19
    if defender != None:
        if 3 == defender.index:
            line += ('**Player ' + str(3 + 1) + '**')
        else:
            line += ('  Player ' + str(3 + 1) + '  ')
    else:
        line += ('  Player ' + str(3 + 1) + '  ')
    line += ' ' * 6
    print line
    line = ' ' * 39
    if mode == 'grid':
        line += ' ' * 12
    line += table.print_attacks_row()
    print line
    ## Print player 1 hand
    print '\n' * 3
    line = ''
    if mode == 'list':
        rows0 = [player_list[0].print_hand_faces_row(i, cards_per_row)
                 for i in range(4)]
        ner0 = 4
        for i in range(4)[::-1]:
            line = ' ' * 39
            if rows0[i] == ' ' * 4 * cards_per_row:
                ner0 = i
                line += rows0[i]
            else:
                line += rows0[ner0 - 1 - i]
            line += ' ' * 10
            print line[:-1]
    elif mode == 'grid':
        for i in range(4)[::-1]:
            line = ' ' * 57
            suit = player_list[0].suit_order[i]
            line += suit_symbols[suit] + ' '
            for j in range(13):
                if suit * 13 + j in player_list[0].get_values():
                    if len(rank_symbols[j + 2] + suit_symbols[suit]) == 2:
                        line += '%s%s  ' % (rank_symbols[j + 2],
                                            suit_symbols[suit])
                    else:
                        line += '%s%s ' % (rank_symbols[j + 2],
                                           suit_symbols[suit])
                else:
                    line += ' ' * 4
            line += ' ' * 10
            print line
    print
    line = ' ' * 44
    if mode == 'grid':
        line += ' ' * 32
    if defender != None:
        if 0 == defender.index:
            line += ('**Player ' + str(0 + 1) + '**')
        else:
            line += ('  Player ' + str(0 + 1) + '  ')
    else:
        line += ('  Player ' + str(0 + 1) + '  ')
    line += ' ' * 10
    line += '\n'
    print line


if __name__ == "__main__":

    player_count = 4
    deck_length = 36
    draw_length = 4
    table = Table(player_count, deck_length, draw_length)
    print_mode = 'grid'
    print_suits_as_symbols = True
    table.durak = DurakDeck(print_suits_as_symbols)
    print table.durak.print_deck()
    table.durak.shuffle()
    cards_per_row = 6
    initial_attacker = None
    player_list = []
    message = ''
    ## table.initiate_round
    for i in range(table.player_count):
        table.player_list.append(Player(i, table.cards_per_player))
    ## Deal cards to players and find trump suit
    table.durak.deal_cards(table.player_list, table.deck_length / table.player_count)
    ##try:
    ##    table.trump_card = table.durak.cards[0]
    ##    table.durak.cards.remove(table.trump_card)
    ##    for card in table.durak.cards:
    ##        if card.suit != table.trump_card.suit:
    ##            table.bot_card = card
    ##            table.durak.cards.remove(card)
    ##    table.trump = table.trump_card.suit
    ##    table.bot = table.bot_card.suit
    ##except IndexError:
    ##    print 'Deck is empty, restart game.'
    ## Clean up and sort player hands
    for i in range(len(table.player_list)):
        table.player_list[i].sort_hand()
    ## Board print testing
    '''for i in range(len(player_list)):
        remove = int(raw_input('Cards to remove from player ' + str(i + 1) + ': '))
        for j in range(remove):
            player_list[i].hand.pop(0)'''
    print_board(table.durak, table, player_list, cards_per_row, None, print_mode)
    ## table.play_game with special_suit = 3

    while True:
        out_list = []
        table.find_initial_attacker(table.player_list, table.initial_attacker)
        table.attacker = table.initial_attacker
        table.bidding_phase()
        table.assign_suit_orders()

        ##for player in table.player_list:
        ##    player.initial_draw_length = cards_per_player

        table.build_decks() ## False means Auto-build the personal decks

        table.play_phase()

        ## Game over, print name of losing player
        ## table.scoring_phase
        team02_cards_won = table.player_list[0].cards_won + table.player_list[2].cards_won
        team02_suits_bid = [player.trump for player in
                            [table.player_list[0], table.player_list[2]]]
        team02_score = 0
        for card in team02_cards_won:
            if card.suit in team02_suits_bid:
                team13_score += 1

        team13_cards_won = table.player_list[1].cards_won + table.player_list[3].cards_won
        team13_suits_bid = [player.trump for player in
                            [table.player_list[1], table.player_list[3]]]
        team13_score = 0
        for card in team13_cards_won:
            if card.suit in team13_suits_bid:
                team13_score += 1

        print ('Round complete. \nPlayers 1 and 3 bid %s + %s for a total '
               % (table.bid_list[0].face(), table.bid_list[2].face()) +
               'of %d %s+%s and won %d.' (table.bid_list[0].rank +
                                          table.bid_list[2].rank,
                                          suit_symbols[table.bid_list[0].suit],
                                          suit_symbols[table.bid_list[2].suit],
                                          team02_score))
        if team02_score >= table.bid_list[0].rank + table.bid_list[2].rank:
            print 'Success!'
            table.player_list[0].bids_won.append(table.player_list[0].trump_card)
            table.player_list[2].bids_won.append(table.player_list[2].trump_card)
        else:
            print 'Failure.'
            table.durak.append(table.player_list[0].trump_card)
            table.durak.append(table.player_list[2].trump_card)

        print ('Round complete. \nPlayers 1 and 3 bid %s + %s for a total '
               % (table.bid_list[0].face(), table.bid_list[2].face()) +
               'of %d %s+%s and won %d.' (table.bid_list[0].rank +
                                          table.bid_list[2].rank,
                                          suit_symbols[table.bid_list[0].suit],
                                          suit_symbols[table.bid_list[2].suit],
                                          team02_score))
        if team13_score >= table.bid_list[1].rank + table.bid_list[3].rank:
            print 'Success!'
            table.player_list[1].bids_won.append(table.player_list[1].trump_card)
            table.player_list[3].bids_won.append(table.player_list[3].trump_card)
        else:
            print 'Failure.'
            table.durak.append(player_list[1].trump_card)
            table.durak.append(player_list[3].trump_card)

        print 'PLAYER WINNINGS'
        for player in table.player_list:
            line = 'Player %d: %s' (player.index, player.print_bids_won)
        raw_input('Press Enter to continue. ')
