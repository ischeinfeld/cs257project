import re 
import exrex

#for this first attempt at generating a simple data set, we will consider
# the class of regex that match some string of characters of finite length
# with no wildcards. We consider a language with just 3 symbols: a, b, c. 
# here we demonstrate what all the permutations for such a set might look like

symbols = ['a', 'b', 'c']

for x in range(3):

	for y in exrex.generate('[abc]{3}'): 
		print(y)