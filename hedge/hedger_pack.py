from pandas import *
import matplotlib.pyplot as plt
import time

df = read_csv('sand.csv')

class Hedge():
	def __init__(self, df, TP, SL):

		self.df = df
		self.TP = TP
		self.SL = SL

		self.indx = list(range(len(self.df)))
		self.state_list = self.df['close'].tolist()
		self.result = False

		self.wins = 0
		self.losses = 0

	def move(self):

		del self.indx[0]

	def trade(self, x):
		self.x = x

		self.hedge_point = self.state_list[self.indx[x]]

		limitS = 0
		limitL = 0

		no_profit = False

		profit_with_L, hit_LSL, limitL = self._check_for_long(SL=False, lim=None)
		profit_with_S, hit_SSL, limitS = self._check_for_short(SL=False, lim=None)

		
		if profit_with_S:
			#time.sleep(10)
			self.wins += 1
		if profit_with_L:
			#time.sleep(10)
			self.wins += 1

		if not profit_with_L and not profit_with_S:
			no_profit = True

		if profit_with_L or profit_with_S:
			no_profit = False

		if hit_SSL and hit_LSL:
			#time.sleep(10)
			print("loss")
			self.losses += 1


	def _check_for_long(self, SL, lim):

		long_take_profit = self.hedge_point * self.TP
		long_stop_loss = self.hedge_point * self.SL

		if SL:
			print("adjusting long stop loss to break even")
			long_stop_loss = self.hedge_point

		profit = False
		hit_SL = False

		limit = 0

		for x in self.indx:

			x += 1
			if x > self.indx[self.x]:
				print("going long", x)

				highview = self.df['high'].tolist()
				highview = highview[self.indx[self.x]:x]

				lowview = self.df['low'].tolist()
				lowview = lowview[self.indx[self.x]:x]

				if max(highview[:lim]) >= long_take_profit:

					print("profit with long")
					profit = True
					break

				#print("for long", min(lowview), long_stop_loss, max(highview), long_take_profit)

				if min(lowview) <= long_stop_loss:

					print("hit long SL")
					hit_SL = True
					break

				limit = lowview.index(min(lowview))

		return profit, hit_SL, limit

	def _check_for_short(self, SL, lim):

		short_take_profit = self.hedge_point * abs(self.TP - 2)
		short_stop_loss = self.hedge_point * abs(self.SL - 2)

		if SL:
			print("adjusting short stop loss to break even")
			short_stop_loss = self.hedge_point

		profit = False
		hit_SL = False

		limit = 0

		for x in self.indx:

			x += 1
			if x > self.indx[self.x]:
				print("shorting", x)

				highview = self.df['high'].tolist()
				highview = highview[self.indx[self.x]:x]

				lowview = self.df['low'].tolist()
				lowview = lowview[self.indx[self.x]:x]
			
				if max(highview[lim:]) < short_stop_loss:

					print("profit with short")
					profit = True
					break


				#print("for short", max(highview), short_stop_loss, min(lowview), short_take_profit)


				if max(highview) >= short_stop_loss :

					print("hit short SL")
					hit_SL = True
					break

				limit = highview.index(max(highview))

		return profit, hit_SL, limit


data = df

plt.plot(data['close'])
plt.show()

hedge = Hedge(data, 1.02, 0.99)

while True:
	print([hedge.indx[1]])

	if hedge.indx[0] >= len(hedge.state_list) - 10:
		break

	p = abs((hedge.state_list[hedge.indx[2]] - hedge.state_list[hedge.indx[0]]) / hedge.state_list[hedge.indx[0]]) * 100

	if p >= 5:
		results = hedge.trade(2)
		print('traded')
	_ = hedge.move()
	print("made a move")

print("Wins: ", hedge.wins, "Losses: ", hedge.losses)

plt.plot(data['close'])
plt.show()



