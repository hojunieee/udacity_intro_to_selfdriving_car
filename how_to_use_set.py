# Initializing two sets
odds   = set([1,3,5,7,9])
primes = set([2,3,5,7])

#How to append an element
my_set.add("a")

# Demonstration of the "intersection" between two sets
# The intersection corresponds to the overlapping region in the Venn Diagram above.
odd_AND_prime = odds.intersection(primes)
print(odd_AND_prime)

# Demonstration of the "union" of two sets. The union
# of sets A and B includes ANY element that is in A OR B or both.
odd_OR_prime = odds.union(primes)
print(odd_OR_prime)

# Demonstration of the "set difference" between two sets.
# Will return {1,9}
odd_not_prime = odds - primes
print(odd_not_prime)
