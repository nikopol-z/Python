import random
import os
import math

clear = lambda: os.system('cls')
ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
suits = ('♣','♦','♥','♠')
values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':11}

class Card():

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit

	def __str__(self):
		return self.rank + self.suit

class Deck():

	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				single_card = Card(rank, suit)
				self.deck.append(single_card)

	def __str__(self):
		deck_composition = ''
		for card in self.deck:
			deck_composition += '\n'+card.__str__()
		return 'The deck has: ' + deck_composition

	def __len__(self):
		return len(self.deck)

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		one_card = self.deck.pop()
		return one_card

class Hand():

	def __init__(self,name,chips=100):
		self.cards = []
		self.chips = chips
		self.name = name
		self.score = 0
		self.aces = 0
		self.bet = 0

	def take(self, card):
		self.cards.append(card)
		if card.rank == 'A':
			self.aces += 1
		self.score += values[card.rank]
		if self.score > 21 and self.aces > 0:
			self.score -= 10
			self.aces -= 1

	def win_bet(self):
		self.chips += self.bet
		print(self.name+' won! And got '+str(self.bet))
		self.bet = 0

	def lose_bet(self):
		print(self.name+' lose! And lost '+str(self.bet))
		self.chips -= self.bet
		self.bet = 0
	
	def drop_cards(self):
		self.cards = []
		self.score = 0
		self.aces = 0
		self.bet = 0
		self.temp_string = ''

	def make_bet(self):
		while True:
			self.bet = input('\n'+ self.name +', make your bet! Insert integer value.' )
			if self.bet == '':
				if self.chips >= 10:
					self.bet = 10
					print("Your bet is 10")
				else:
					self.bet = self.chips
					print("Your bet is {}".format(self.bet))
				break
			try:
				self.bet = int(self.bet)
			except:
				print("Whoops, that isn't an integer.")
			else:
				if self.bet > self.chips:
					print("You don't have enough money. Your chips: "+str(self.chips))
					continue
				elif self.bet == -500:
					print("That's a cheeting, but it's OK )")
					break
				elif self.bet < 0:
					print("You can't bet a negative sum!")
					continue 
				elif self.bet == 0:
					print("You not going to play, but you have to pay! 10 chips or less.")
					if self.chips >= 10:
						self.chips -= 10
						self.bet = 0
					else:
						self.chips = 0
						self.bet = 0
					break
				else:
					print("Thank you. Your bet "+str(self.bet)+" is accepted.")
					break

	def stay_or_hit(self,deck):
		while True:
			turn = input(self.name+"! Stay or Hit? Press 's' or 'h' ")
			if turn == '':
				continue
			if turn[0].lower() == 'h':
				self.hit(deck)
				if self.score > 21:
					# Maybe write win or busts conditins here
					self.lose_bet()
					print(self.name+' busted!')
					break
				continue
			elif turn[0].lower() == 's':
				print(self.name+" stands.")
			else:
				print("Whoops, looks like you didn't press 's' or 'h'. ")
				continue
			break

	def hit(self,deck):
		self.take(deck.deal())
		print(self.__str__())

	def __str__(self):
		self.temp_string = ''
		for card in self.cards:
			self.temp_string += card.__str__()
			self.temp_string += ' '
		return self.name + ' cards: \n\t' + self.temp_string + ' (' + str(self.score) + ')' + ' Chips: ' + str(self.chips)

class HumanHand(Hand):
	pass

class DealerHand(Hand):

	def __init__(self,name,chips=100):
		Hand.__init__(self,name,chips=100)
		self.should_hide_card = True

	def make_bet(self):
		pass

	def stay_or_hit(self,deck):
		while True:
			if self.score < 17:
				self.take(deck.deal())
			else:
				break

	def __str__(self):
		self.temp_string = ''
		for card in self.cards:
			self.temp_string += card.__str__()
			if self.should_hide_card:
				break	
			self.temp_string += ' '
		if self.should_hide_card:
			self.should_hide_card = False
			return self.name + ' cards: \n\t' + self.temp_string + ' + hidden card'
		else:
			self.should_hide_card = True
			return self.name + ' cards: \n\t' + self.temp_string + ' (' + str(self.score) + ')'


def playAgain():
	global isPlaing, players
	while True:
		playMore = input("Do you want to play more? Y/N ")
		if playMore == '':
			continue
		if playMore[0].lower() == 'y':
			if len(players) == 1:
				print("Sorry, no more players with money! Bye!")
				isPlaing = False
				break
			isPlaing = True
			break
		elif playMore[0].lower() == 'n':
			isPlaing = False
			print('Goodbye!')
			break
		else:
			print("Please, insert 'y' or 'n'. ")
			continue


# MAIN LOGIC
# Make new deck and shuffle it
my_deck = Deck()
my_deck.shuffle()
print("Testing!!!!!!")	 
# Make a list for Players and a Dealer
players = []
players.append(DealerHand('Dealer'))

# Make new human players
## TO-DO: Insert Name and Number verification and limitation of max and min players
## TO-DO: Maybe make a default values
howManyPlayers = input("How many players?")
if howManyPlayers == '':
	howManyPlayers = 1
#TO-DO: add try for not integers values
for i in range(1,int(howManyPlayers)+1):
	new_players_name = input("Please, want's your name? ")
	if new_players_name != '':
		players.append(HumanHand(str(new_players_name)))
	else:
		players.append(HumanHand("Player #" + str(i)))

# Main Game Cycle
isPlaing = True
while isPlaing:
	clear()
	# Recreate a deck if only 20 cards remaning
	if len(my_deck) < 20:
		del my_deck
		my_deck = Deck()
		my_deck.shuffle()
		print("New deck!!!")
	# Give 2 cards to a Players
	for player in players:
		player.take(my_deck.deal())
		player.take(my_deck.deal())

	for player in players:
		print(player)

	# Make a bet
	for player in players:
		player.make_bet()
	#clear()
	# Ask Players with not zero bet for stay or hit
	for player in players:
		player.stay_or_hit(my_deck)

	# Count who win
	print("===================================")
	for player in players:
		if player.bet != 0:
			# Players Not Busted
			if players[0].score <= 21:
				# Dealer Not Busted
				if players[0].score > player.score:
					player.lose_bet()
				elif players[0].score < player.score:
					player.win_bet()
				else:
					print(player.name+' and Dealer tie!')
			else:
				print("Dealer busted!")
				player.win_bet()
	
	for player in players:
		print(player)

	# Delete player if no money
	for player in players:
		if player.chips == 0:
			print(players.pop(players.index(player)).name+' has no money. Buy!')
	
	# Drop old cards
	for player in players:
		player.drop_cards()

	# Ask to play more
	playAgain()