import random
import matplotlib.pyplot as plt

class Sim():
	def __init__(self, episode_length, shards, floor, cieling):

		self.episode_length = episode_length
		self.shards = shards

		self.long_term_trend = []

		for x in range(episode_length):
			val = random.uniform(floor, cieling)
			self.long_term_trend.append(val)

	def granulize(self):
		self.granulized = []

		for save_point in self.long_term_trend:
			print(save_point)
			indx = self.long_term_trend.index(save_point)

			if indx < len(self.long_term_trend) - 1:

				next_point = self.long_term_trend[indx + 1]

				sliced_list = []
				for shard in range(self.shards - 1):

					shard += 1
					fraction = shard / self.shards

					to_add = (next_point - save_point) * fraction/2
					cut = save_point + to_add	

					self.granulized.append(cut)
		

		self.granulized2 = []

		for save_point in self.granulized:
			print(save_point)
			indx = self.granulized.index(save_point)

			if indx < len(self.granulized) - 2:

				next_point = self.granulized[indx + 1]

				sliced_list = []
				for shard in range(self.shards - 1):

					shard = random.choice(range(1, self.shards))
					fraction = shard / self.shards

					to_add = (next_point - save_point) * fraction
					cut = save_point + to_add	

					self.granulized2.append(cut)


		self.granulized3 = []

		for save_point in self.granulized2:
			print(save_point)
			indx = self.granulized2.index(save_point)

			if indx < len(self.granulized2) - 2:

				next_point = self.granulized2[indx + 1]

				sliced_list = []
				for shard in range(self.shards - 1):

					shard += 1
					fraction = shard / self.shards

					to_add = (next_point - save_point) * fraction
					cut = save_point + to_add	

					self.granulized3.append(cut)
					
		

		return self.granulized3



simulation = Sim(10, 5, 1, 1.1)

pre_data = simulation.long_term_trend
data = simulation.granulize()

plt.plot(pre_data)
plt.show()
plt.plot(data)
plt.show()



