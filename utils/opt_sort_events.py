#!/usr/bin/env python3

from itertools import cycle, chain

def chunks(q, n):
    q = list(q)
    for i in range(0, len(q), n):
       yield q[i:i+n]

def shuffle(q, n):
    q = list(q)
    m = len(q)//2
    left =  list(chunks(q[:m],n))
    right = list(chunks(reversed(q[m:]),n)) + [[]]
    return chain(*(a+b for a,b in zip(left, right)))

def listarray(n):
    return [list() for _ in range(n)]

def mean(q):
    return sum(q)/len(q)
    
def sort_events_opt(jobN, eventN):
	NBUCKETS = jobN
	COUNT    = eventN
	data 	 = range(eventN)

	order = shuffle(range(COUNT), NBUCKETS)
	posts = cycle(range(NBUCKETS))
	buckets = listarray(NBUCKETS)
	for o in order:
		i = next(posts)
		buckets[i].append(data[o])

	eventids = [sorted(x) for x in buckets]

	return eventids