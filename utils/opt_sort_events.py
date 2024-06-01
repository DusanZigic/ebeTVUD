#!/usr/bin/env python3

from itertools import cycle, chain

class optEventSort:
	def __init__(self, jobN, eventN):
		self.jobN = jobN
		self.eventN = eventN

	def __chunks(self, q, n):
		q = list(q)
		for i in range(0, len(q), n):
			yield q[i:i+n]

	def __shuffle(self, q, n):
		q = list(q)
		m = len(q)//2
		left =  list(self.__chunks(q[:m],n))
		right = list(self.__chunks(reversed(q[m:]),n)) + [[]]
		return chain(*(a+b for a,b in zip(left, right)))

	def __listarray(self, n):
		return [list() for _ in range(n)]

	def __mean(self, q):
		return sum(q)/len(q)
    
	def sort_events_opt(self):
		NBUCKETS = self.jobN
		COUNT    = self.eventN
		data 	 = range(self.eventN)

		order = self.__shuffle(range(COUNT), NBUCKETS)
		posts = cycle(range(NBUCKETS))
		buckets = self.__listarray(NBUCKETS)
		for o in order:
			i = next(posts)
			buckets[i].append(data[o])

		eventids = [sorted(x) for x in buckets]

		return eventids