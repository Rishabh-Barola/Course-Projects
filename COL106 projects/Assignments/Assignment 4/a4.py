#                                                         ASSIGNMENT 4


from cmath import log10
from operator import mod
import random
import math

#To generate random prime less than N

def randPrime(N):

	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	#input specification : eps : error bound , p : pattern , x : text
	#output specification : list of starting indices where p matches x , if we say p matches x at i if for all j in {0,1,...,m-1} p[j] = x[i+j]
	#but we are only comparing f(p)modq = f(x[i...i+m-1])modq through modPatternMatch 
	N = findN(eps,len(p))
	q = randPrime(N)
	#since q <= N , and since time complexity of modPatternMatch is O((m+n)logq) , so time complexity of randPatternMatchWildcard is O((n+m)*log2(N)),
	#  log2(N)<2*(log2(m/eps)+log2(log2(m/eps) + c)) ,where c is a constant
	#and since (loglogn) = O(logn) , so time complexity of randPatternMatch is O((n+m)*log2(m/eps))

	# space complexity of modPatternMatch is O(k+logn+logq) , so space complexity of randPatternMatch is O(k+logn +log2(m/eps)) with similar reasoning as above
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	 
	#input specification : eps : error bound , p : pattern , x : text
	#output specification : list of starting indices where p matches x , if we say p matches x at i if for all j in {0,1,...,m-1} p[j] = x[i+j] or p[j] = '?' 
	#but we are only using one wildcard AND comparing only f(p)modq = f(x[i...i+m-1])modq through modPatternMatchWildcard
	N = findN(eps,len(p))
	q = randPrime(N)
	#since q <= N , and since time complexity of modPatternMatchWildcard is O((m+n)logq) , so time complexity of randPatternMatchWildcard is O((n+m)*log2(N)),
	#  log2(N)<2*(log2(m/eps)+log2(log2(m/eps) + c)) ,where c is a constant
	#and since (loglogn) = O(logn) , so time complexity of randPatternMatchWildcard is O((n+m)*log2(m/eps))

	# space complexity of modPatternMatch is O(k+logn+logq) , so space complexity of randPatternMatch is O(k+logn +log2(m/eps)) with similar reasoning as above
	
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	# input specification : eps : error bound , m : length of pattern
	# output specification : N : integer such that any random prime less than N satisfies the error bound
	# we know from claim 1 prime factors of a number d is at most log2d
	#we know from claim 2 that number of primes less than N is at least N/2logN
	# probability that a random prime "q" selected from {1,2,...,N} is such that, f(p)modq = f(x[i...i+m-1])modq ,but p!=x[i...i+m-1] < (probability that a random prime "q" selected from {1,2,...,N} is such that, f(p)modq = f(x[i...i+m-1])modq )
	# so probabilty that a random prime "q" selected from {1,2,...,N} is such that, f(p)modq = f(x[i...i+m-1])modq < eps will get us a bound of N
	# x(A)= cases that a prime q is a factor of [f(p)-f(x[i...i+m-1])] or [f(p)-f(x[i...i+m-1])]modq = 0 
	# means that q is a prime factor of [f(p)-f(x[i...i+m-1])]
	#x(B) = cases that a prime q is chosen is pi(N)>=N/2logN 
	# probability that a random prime "q" selected from {1,2,...,N} is such that, f(p)modq = f(x[i...i+m-1])modq  = x(A)/x(B)
	# x(A)/x(B) < eps
	# x(B) > x(A)/eps
	# N/2logN > x(A)/eps
	# since we need an upperbound so if x(A) is maximum then we can proceed , x(A) will be maximum when f(p)-f(x[i...i+m-1]) is maximum that is (26^m)-1 - 0 = 26^m - 1
	# so from claim 1 , number of prime factors of 26^m - 1 , we know that log2(26^m - 1) <= mlog2(26) = mlog2(26) = mlog2(26)
	# so x(A) <= mlog2(26)
	# x(A)/x(B) < eps => mlog2(26)/(N/2logN) < eps => N/log2N > 2*mlog2(26)/eps
	# f(N)= N/log2N, g(N) = N^0.5 , since log2N < n^0.5 => 1/log2N > 1/N^0.5 => N/log2N > N^0.5
	# so if N^0.5 > 2*mlog2(26)/eps => N/log2N > 2*mlog2(26)/eps
	# so N > 4*m^2*(log2(26))^2/eps^2
	# so N = ceilfunction (4*m^2*(log2(26))^2/eps^2)

	return (math.ceil(2*m*math.log(26,2)/(eps)))**2
	

def modhorner(x,q):
	#helper function to evaluate a polynomial in O(len(x))
	#input specification : x : string , q : prime
	#output specification : f(x)modq where f(x) = x[0]*26^m-1 + x[1]*26^m-2 + ... + x[m-1]*26^0 , where x[i] = ord(x[i])-ord('a')

	ascii = lambda c: ord(c) - ord('A') # function to calculate values of characters , ord('A') = 65 , ord('?') = 63
	
	#loop to calculate f(x)modq using horners rule , f(x) = (((x[0]*26+ x[1])*26 + x[2])*26 + x[3])*26 + ... + x[m-1]
	# time complexity of this loop is O(len(x)) so time complexity of modhorner is O(len(x))
	# so auxillary space of modhorner is O(logq)
	for i in range(0,len(x)):
		if(i == 0):
			result = ascii(x[i])%q
		else:
			result = ((result * 26)%q + ascii(x[i])%q)%q
	return result


def modPatternMatch(q,p,x):
	#input specification : q : prime , p : pattern , x : text
	#output specification : list of starting indices where p matches x , if we say p matches x at i if for all j in {0,1,...,m-1} ,f(p)modq  = f(x[i...i+m-1])modq
	m = len(p)
	n = len(x)
	#function to return ascii value of a character
	ascii = lambda c: ord(c) - ord('A')
	L=[]															# assume L is an empty list
	mult= pow(26,m-1,q) 											# calculate 26^(m-1)modq so that we don't need to do this again and again in loop & stored in log(q) space computed in logm time
	a = modhorner(x[:m],q) 											# calculate f(x[0...m-1])modq   , stored in O(logq) space and computed in O(m) time
	b = modhorner(p,q)   											# calculate f(p)modq 			, stored in O(logq) space and computed in O(m) time
	
	for i in range(0,n-m+1):
		if(a == b): 												# if f(x[i...i+m-1])modq = f(p)modq then p matches x at i
			L.append(i)												# append i to L
		if(i < n-m):
			a = (a - (ascii(x[i])) * mult)%q						# calculate f(x[i+1...i+m])modq from f(x[i...i+m-1])modq in O(1) time
			a = (a * 26 + ascii(x[i+m]))%q							# subtract x[i]*26^(m-1)modq , multiply by 26 and add x[i+m]modq as all are after taking modq, so only additional space used is O(logq)
																	# another log(n) space is used to store current index
																	# and if we report k matches then we store k indices in L
																	# so total auxillary space used is O(logq) + O(logn) + O(k) = O(logq + logn + k)
																	#
																	# time complexity of this loop is (n+m)*log2(q) as we are doing log2(q) operations in each iteration as these are log2q bits number for modhorner and this function.
	return L


def Wildcardlocation(x):
	#helper function to return the location of wildcard in a string
	#input specification : x : string
	#output specification : index where wildcard is present in x

	#time complexity of this function is O(len(x)) as we are iterating over the string
	ascii = lambda c: ord(c) - ord('A')
	m = len(x)
	for i in range(0,len(x)):
		if ord(x[i])==63:
			a = i 
			break
	return a


def modPatternMatchWildcard(q,p,x):
	#input specification : q : prime , p : pattern , x : text
	#output specification : list of starting indices where p matches x , if we say p matches x at i if for all j in {0,1,...,m-1} ,f(p)modq  = f(x[i...i+m-1])modq
	m,n = len(p),len(x)
	#function to return ascii value of a character
	L=[]
	ascii = lambda c: ord(c) - ord('A')
	
	#for solving the pattern matching when wildcard is present, we use the following idea that whereever '?' is present in pattern , we can ignore that location in text while calculating f(x[i...i+m-1])modq
	#which means to say that don't change our modhorner function , just subtract the contribution of '?' if ascii('?') = 63 was used while evaluating f(p)modq 
	# and similarly while evaluating f(x[i...i+m-1])modq , subtract the contribution of 'x[i+a]' . where a is the location of '?' in pattern
	a = Wildcardlocation(p) 										# calculate the location of wildcard in pattern
	mult= pow(26,m-1,q) 											# calculate 26^(m-1)modq so that we don't need to do this again and again in loop & stored in log(q) space computed in logm time
	mult2 = pow(26,m-a-1,q)											# contribution of 'x[i+a]' in f(x[i...i+m-1])modq or '?' in f(p)modq
	mult3 = pow(26,m-a,q)											# contribution of 'x[i+a+1]' in f(x[i...i+m-1])modq
	p_ans =  modhorner(p,q)										# calculate f(p)modq
	p_ans = (p_ans - (ascii(p[a])) * mult2)%q					# subtract the contribution of '?' in f(p)modq

	x_ans = modhorner(x[:m],q)									# calculate f(x[0...m-1])modq
	x_ans = (x_ans - (ascii(x[a])) * mult2)%q					# subtract the contribution of 'x[a]' in f(x[0...m-1])modq
	

	for i in range(0,n-m+1):
		if(x_ans == p_ans):										# if f(x[i...i+m-1])modq = f(p)modq then p matches x at i after we have modified f(x[i...i+m-1])modq and f(p)modq
			L.append(i)											
		if(i < n-m): 											
																							#updating f(x[i+1...i+m])modq from f(x[i...i+m-1])modq in O(1) time
			x_ans = (x_ans - (ascii(x[i])) * mult)%q						# subtract the contribution of letter present at i as when we compare the next m places , we need to subtract the contribution of x[i]
			x_ans = (x_ans * 26 + ascii(x[i+m]))%q							# multiply by 26 and add x[i+m]modq as all are after taking modq, so only additional space used is O(logq)
			x_ans = (x_ans + (ascii(x[i+a])) * mult3)%q						# add the contribution of x[i+a] as when we compare the next m places , we need to add the contribution of x[i+a] which we earlier ignored while calculating f(p)modq as this place had '?' in pattern
			x_ans = (x_ans - (ascii(x[i+a+1])) * mult2 )%q					# subtract the contribution of x[i+a+1] as when we compare the next m places , we need to subtract the contribution of x[i+a+1] which we earlier considered while calculating f(p)modq as this place has '?' in pattern but earlier it was not there.
																			
																			# space complexity :additional space used is O(logq) as we are storing x_ans in logq bits number
																			# auxillary space O(k+ logn + logq) where k is the length of pattern and n is the length of text and q is the prime number

																			# time complexity of this loop is (m+n)*log2(q) as we are doing log2(q) operations in each iteration as these are log2q bits number and while calculating pattern we use modhorner which takes m*log2(q)
																			# time complexity of this function is O((m+n)*log2(q)) 	
	return L
x = "ACTATCAGTACCCGTGTCTCGACTCTGCCGCGGCTACCTATCGCCTGAAAGCCAGTTGGTGTTAAGGGGTGCTCTGTCCAGGACGCCACGCGTAGTGAGACTTACATGTTCGTTGGGTTCACCCGACTCGGACCTGAGTCGACCAAGGACGCACTCGAGCTCTGAGCCCTACTGTCGAGAAATATGTATCTCGCCCCCGCAGCTTGCCAGCTCTTTCAGTATCATGGAGCCCATGGTTGAATGACTCCTATAACGAACTTCGACATGGCAAAATCCCCCCCTCGCGACTTCTAGAGAAGAAGAGTACTGACTTGAGCGCTCCCAGCACTTCAGCCAAGGAAGTTACCAATTTCTTGTTTCCGAATGACACGCGTCTCCTTGCGGGTAAATCGCCGACCGCAGAACTTACGAGCCAGGGGAAACAGTAAGGCCTAATTAGGTAAAGGGAGTAAGTGCTCGAACGGTTCAGTTGTAACCATATACTTACGCTGGATCTTCTCCGGCGAATTTTTACCGTCACCAACTACGAGATTTGAGGTAAACCAAATGAGCACATAGTGGCGCTATCCGACTATTTCCAAATTGTAACATATCGTTCCATGAAGGCCAGAGTTACTTACCGGCCCTTTCCATGCGCGCGCCATACCCTCCTAGTTCCCCGGTTATCTCTCCGAGGAGAGAGTGAGCGATCCTCCGTTAACATATTGTTACCAATGACGTAGCTATGTATTTTGCACAGGTAGCCAACGGGTTTCACATTTCACAGATAGTGGGGATCCCGGCAAAGGGCGTATATTTGCGGTCCAACATAGGCGTAAACTACGATGGCACCTACTCAGACGCAGCTCGTGCGGCGTAAATAACGTACTCATCCCAACTGATTCTCGGCAATCTACGGAGCGACATGATTATCAACAGCTGTCTAGCAGTTCTAATCTTTTGCCATGGTCGTAAAAGCCTCCAAGAGATTGATCATACCTATCGGCACAGAAGTGACACGACGCCGATGGGTAGCGGACTTTAGGTCAACCACAGTTCGGTAGGGGACAGGCCCTGCGGCGTACATCACTTTGTATGTGCAACGTGCCCAAGTGGCGCCAGGCAAGACTCAGCTGGTTCCTGTGTTAGCTCGAGGCTAGGCATGACAGCTCTTTGAACATGGGCTGGGGGCCTCGAACGGTCGAGAAGCCCATAGTACCTCGGATACCAAGTTGCGCAGGCTATAGCTTGAAGCTGTACTATTTCAGGGGGGGAGCCCTGATGGTCTCTTCTTCTGATGACTCAACTCGCTAGGGTCGTGAAGTCGATTCCTTCGATGGTTAAAAATCAAAGGCTCAGAGTGCAGACTGGAGCGCCCATCTAACGGTTCGCATCTCGAATGCTCGGTCGCCTTTCACATTCCGCGAAAATTCATACCGCTCATTCACTAGGTTGCGAAGTCTACACTGATATATGAATCCGAGCTAGAGCAGGGCTCTTAAAATTCGGAGTCGTTGATGCTCAATACTCCAATCGGTTTTTTCGTGCACCACCGCGAGTGGCTGACAAGGGTTTGACATTGAGTAGCAAGGCAGTTCCGGGCTGAATGAAGCGCCGGGAAAGGTACGCGCCTGGTATGGCAGGATTAAGAAGCCAATACAAAGGCTACATCCTCACTCGGATGGAGGCAAACGCAGAACAATGGTTACTTTTTCGATACGTGAAACATGTCCCACGGTAGCCCAAAGACTTGAGAGTCTATCACCCCTAGGGCCCTTTCCCGGATATAAACGCCAGGTTGAATCCGCATTTGGAGGTACGATGGATCAGTCTGGGTGGGGCGCGCCCCATTTATACCGTGAGTAGGGTCGACCAAGAACCGCAAGATGCGACGGTGTACAAGTAATTGTCAACAGACCATCGTGTTTTCATAATGGTACCAGGATCTTCAAGCCGTGTCAATCAAGCTCGGATTACGGTGTTTACTCCGTCCTGCGGTTACTCACGGTCTGTAATCCACCTCAAGTCAAGCCATTGCCTCTCTGAGACGCCGCATGAATTAATACGTATACTTTGCGCGGGTTCACTGCGATCCGTTCAGAGTCGTCCAAGGGCACAATCGAGCTCCCATTTGTATGTTCGGCTAACTTGTACCCAACCCCCGAAGTTTAGCAGGTCGTGGGGTGTCATGGAGCCTCTGGTTCATCCCGTGGGATATCAAGCTTCGTCTTGATAAAGCTCCCCGCTCGGGTGTAGCAGAGAAGACGCCTACTGAATTGTGCGATCCCTGCACCTCAGCTAAGGTAGCTACCAATATTTAGTTTCTAAGCCTTGCGACAGACCTCCCACTTAGATTGCCACGCATAGAGCTAGCGAGTCAGCGAAAAGCATGACGCGCTTTCAAGCGTGGCGAGTATGTGAACCAAGGCTTCGGACAGGACTATATACTTAGGTTTGATCTCGCCCCGAGAACTGTAAACCTCAACATTTATAGATTATAAGGTTAGCCGAAAATGCACGTGGTGGCGCCCGCCGACTGCTCCCTGAGTGTGGCTCTTTGTTCTGTCAACGCCCGACCTTCATCGCGGCCGATTCCTTCTGCGGACCATGTCGTCCTGATACTTTGGCCATGTTTCCGTTGTAGGAGTGAAGCCACTTGGCTTTGCGCCGTAGTTCCAATGAAAAACCTATGGACTTTGTTTAGGGTAGCATCAGGAATCTGAACCCTCAGAAAGTGGGGATCCCGGGTATAGACCTTTATCTGCGGTTCAAGTTAGGCATAAGGCTGCATGCTACCTTGTCACACCTACACTGCTCGAAGTAAATATGGGAAGCGTGCGACCTGGCTCCAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGTAATACCATGGTCCCTCAAATTCGGCTCAGTTACCTCGAGCGTTATGTCTCAAATGGCGTAGAACGGCATTGACTGTTTGACACTAGCTGGTGTTCGGTTCGGTAACGGAGAATCTGTGCGGCAATGTCATTAATACATTTGAAACGCGCCGTACCGATGCTGAGCAAGTCAGTGCAGGCTCCCGTGTTAGGATAAGGGTAAACATACAAGTCGATAGAAGATGGGTAGGGGCCTTCAATTCATCCAACACTCTACGGCTCCTCCGAGAGCTAGTAGGGCACCCTGTAGTTGGAAGGGGAACTATTTCGTGGGGCGAGCCCATACCGTCTCTCTTGCGGAAGACTTAACACGATAGGAAGCTGGAATAGTTTCGAACGATGGTTATTAATCCTAATAACGGAACGCTGTCTGGAGGATGAGTCTGACGGAGTGTAACTCGATCAGTCACTCGCTATTCGAACTGGGCGAAAGATCCCAGCGCTCATGCACTTGATCCCGAGGCCTGACCCGATATATGAGCTCAGACTAGAGCGGGGCTGTTGACGTTTGGAGTTGAAAAAATCTATTATACCAATCGGCTTCAACGTGCTCCACGGCAGGCGCCTGACGAGGGGCCCACACCGAGGAAGTAGACTGTTGCACGTTGGGGATAGCGGTAGCTAACTAAGACGCCTGCCACAACAGCAGTATCAAACCCGTACAAAGGGAACATCCACACTTTGGTGAATCGAAGCGCGGCATCAGAATTTCCTTTTGGATACCTGATACAAAGCCCATCGTGGTCCTTAGACTTCGTACACTTACACCTGCACCGCGCGCATGTGGAATTAGAGGCGAAGTACGATCCCTAGACCGACGTACGATGCAACTGTGTGGATGTGACGAGCTTCTTTTATATGCTTCGCCCGCCGGACCGGCCTCGGCATGGCGTAGCAGTGCACAAGCAAATGACAATTAACCACCGTGTATTCGTTATAACATCAGGCAGTTTAAGTCGGGACAATAGGAGCCGCAATACACAGTTTACCGCATCTTGACCTAACTGACATACTGCCATGGACGACTAGCCATGCCACTGGCTCTTAGATAGCCCGATACAGTGATTATGAAAGGTTTGCGGGGCATAGCTACGACTTGCTTAGCTACGTGCGAGGGAAGAAACTTTTGCGTATTTGTATGTTCACCCGTCTACTACCCATGCCCGGAGATTATGTAGGTTGTGAGATGCGGGAGAAGTTCTCGACCTTCCCGTGGGACGTCAACCTATCCCTTAATAGAGCATTCCGTTCGGGCATGGCAGTAAGTACGCCTTCTCAATTGTGCTAACCTTCATCCTTATCAAAGCTTGGAGCCAATGATCAGGATTATTGCCTTGCGACAGACTTCCTACTCACAGTCGCTCACATTGAGCTACTCGATGGGTCATCAGCTTGACCCGGTCTGTTGGGCCGCGATTACGTGAGTTAGGGCTCCGGACTGCGCTGTATAGTCGAATCTGATCCGGCCCCCACAACTGCAAACCCCAACTTATTTAGATAACATGATTAGCCGAAGTTGCACGGGGTGCCCACCGTGGAGTCCTCCCCGGGTGTCCCTCCTTCATTTGACGATAAGCAGCCGCTACCACCATCGATTAATACAAGGAACGGTGATGTTATCATAGATTCGGCACATTACCCTTGTAGGTGTGGAATCACTTAGCTACGCGCCGAAGTCTTATGGCAAAACCGATGGACAATGATTCGGGTAGCACTAAAAGTCCATAGCACGTGCATCCCAACGTGGCGTGCGTACAGCTTAACCACCGCTTCATGCTAAGGTGCTGGCTGCATGCTAAGTTGATACGCCTGCACTGCTCGAAGAAAATATACGAAGCGGGCGGCCTGGCCGGAGCACTACCCCATCGACGCGTACTCGAATACTGTTAATTGCTCACACATGAACAAAATAGTAGAGTGTCACTTTCAGCCCTCTTATCCTCGGCGATGTGTGTAAAATGGCGTTGATCTGGATTGACTCTATGACGGTATCTGCTGATGGGTAGGGAGATCCGGAATCTATCGGCCTATGTCACTGAAACTATCCAAACACCCCATGTCGATACTGAACGTATCGACGCATACCTCCTTCCTTGAAAACGCACAATCATACAACTGGGCACATAATGCGTACGCCCATCTAGTACACCCATCTCTGTAGGTCCAGTTCAAGAGCTGGAAGAGCACCCTCCACTTGGTCAAGTGATATCCTGGTAAGGTAAGCTCGTACCGTGATTCATGCGGCAGGGGTAAGACCATTAGAAGTAGGGATAGTCCCAAACCTCACTTACCACTGCCAATAAGGGGTCCTTATCTGAAGGATGAGTGTCAGCCAGTGTAACCCGATGAGGAACCCAGAAGCCGAACTGGGCCAGACAACCCGGCGCTAACGCACTCAAAGCCGGGACGCGACGCGACATAACGGCTAAGAGTAGCCCCGGAGTGTAGACCTTTGGGGTTGGATAAATCTGTCGTGGTAACCGGCTTCAACGACCCGTACACGTGGCACTTCAGGAGGCGCCCGCAGGGGGGAAGTTTTCTGCTATTCGAGGCCGTTCGTGGTAACTAGTTGCGTTCCTAGCCGCTATAATTGTTTCTATGCCGAGTAATGAGAACAACCACACCATAGCGATTTGACGCGGCGCCTCGGAATACCGTTTTGGCAGGCGCTTGCTAAGGCCATCGCGAATTCCAGGTATCGTGCATGTAGCGTAGGGCCGCACGCAAGTTAAACTGCTGGGGAACCGCGTTTCCACGACCGGTGCACGATTTAATTTCGCCGACGTGACGACATTCCTGCTAATGCCTCACCCGCCGGACCCCTCTCGTGATGGGGTAGCTGGACATGTCCTTGTGAGATATAACAAGAGCCTGCCTGTTTAATGATCTCACGGCGAAAGTCGGGGGGACAGCAGCGGCTGCAGACATTATACCGCAACAACACTAAGGTGAGATAACTCCGTAGTTGACTACGCATTCCTCTAGACCTTACTTGACCGGATACAGTGACTTTGACACGTTTGTGGGTTACAGCAATCACATCCAAGACTGCCTATGGAGGAAGCAACTCTTGAGTGTTAATATGTTGACCCCTGTATTAGGGATGCGGGTAGTAGATGAGCGCAGGGACACCGAGGTCAAGTACATTACCCTCTCATAGGAGGTGTTCTAGATCACCATACCACCATATCATTCGAGCATGACACTATCTGCGCTGTCCCCATCCTGGTAGTCATTATTCCTATCACGCTTTCGAGTGACTGGTGACGGATATCCCCCACGAATGAAAATCTTTTTCACTGACAGTCATATTGGGGTGCTCCTAAGCTTTTCCACTTGGCTGGGTCTGCTAGGCCTCCGTGCCCGGAGTTTCGGCGCTGTGCTGCCGAGAGCCGGCCATTGTCATTGGGGCCTCACTTGAGGATACCCCGACCTATTTTGTCGGGACCACTCGGGGTAGTCGTTGGGCTTATGCACCGTAAAGTCCTCCGCCGGCCTCCCCGCTACAGAAGATGATAAGCTCCGGCAAGCAATTATGAACAACGCAAGGATCGGCGATATAAACAGAGAAACGGCTGATTACACTTGTTCGTGTGGTATCGCTAAATAGCCTCGCGGAGCCTTATGCCATACTCGTCCGCGGAGCACTCTGGTAACGCTTATGGTCCATAGGACATTCATCGCTTCCGGGTATGCGCTCTATTTGACGATCCTTTGGCGCACAGATGCTGGCCACGAGCTAAATTAGAGCGACTGCACAACTGTAAGGTCCGTCACGCAGACGACGGCCCAGGGAGACCACTGACCCATCAACCTGTACGGGAACCTTCTGTATCGTTCTCGGACGGAGAGATAACTACAGTGCCGCTTACAGCCCCTCTGTCGTCGCCGACGTCTGTAATGTAGCCTCATTGTGATTCCACCCTATTGAGGCATTGACTGATGCGGGAAGAGATCTGAAATGAACTGGTCTATGCGACAGAAACTGTGCAGCTACCTAATCTCCTTAGTGTAGGTTCTGACCGATTCGTGCTTCGTTGAGAACTCACAATTTAACAACAGAGGACATAAGCCCTACGCCCATGATCTACTGACGTCCCTGAGGCTGCAATTCATGTAATGGGACAGTATCCGCGGCAAGTCCTAGTGCAATGGCGGTATTCTACCCTCGTACTGTAGTAGAGGCGACGCGGGTGCGGTCATCACTAATAAGGATATTGGGAAGACTCACAGGCCTCCGCCTTTAGGCGGTGCTTACTCTTACATAAAGGGGCTGTTAGTATTACCCCGCGAGGATTCGAAAAGGTGAGCCAACCCGGCCGATCCGGAGAGACGGGCCTCAAAGCCGCGTGACGACGGCTGTGGGCCCGTAACAAAATCCCCGCAATAAGCTCCCGTGAGCGTCGGTTGAACAGCCCTGGTCGGCCCCATCAGTAGCCCGAATATGTCGCTTTACGGGTCCTGGGCCGGGGTGCGATACCTTGCAGAAATCGAGGCCGTTCGTTAATTCCTGTTGCATTCGTACCGCCTATATTTGTCTCTTTGCCGGCTTATATGGACAAGCATAGCATAGCCATTTATCGGAGCGCCTCCGTACACGGTATGATCGGACGCCTCGTGAGATCAATACGTATACCAGGTGTCCTGTGAGCAGCGAAAGCCTATACGCGAGATACACTGCCAAAAATCCGCGTGATTACGAGTCGTGGCAAATTTGGTCTGGCTGTGGTCTAGACATTCCAGGCGGTGCGTCTGCTCTCGGGTGCCTCTAGTGGCTGGCTAGATAGACTAGCCGCTGGTAAACACACCATGACCCCGGCTCTCCATTGATGCCACGGCGATTGTTGGAGAGCCAGCAGCGACTGCAAACATCAGATCAGAGTAATACTAGCATGCGATAAGTCCCTAACTGACTATGGCCTTCTGTAGAGTCAACTTCACCACATATGCTGTCTCTGGCACGTGGATGGTTTAGAGGAATCAGATTCAAGTCTGGTTAACCATCAAACAGGTCTTGAGTCTAAAATTGTCGTCTCCTGCGTACGAGATGGAAATACTAGGTAACTACAGGGACTCCGACGTTATGTACGTTGCTCCGTCAGAGGCGCCATTCAGGATCACGTTACCGCGAAAAAAAGGGACCAGGAGCTCTTCTCCCCTGCGGTCACGTCTATAGAAATTACACCATTAACCCTCCTGAGAACCGGGAGGCGGGAATCCGTCACGTATGAGAAGGTATTTGCCCGATAATCAATACCCCAGGCTTCTAACTTTTTCCACTCGCTTGAGCCGGCTAGGCCTTTCTGCCCGAAGTTTCGATGGACTGGTGCCAACGCGCAGGCATAGTTTTAGGAGAATTATTCGGGGGCAGTGACAACCAACATCTCGGGTCCTGCCCAACCGGTCTACACGCTAATATAGCGAATCACCGAGAACCCGGCGCCACGCAATGGAACGTCCTTAACTCCGGCAGGCAATTAAAGGGAACGTATGTATAACGCAAAAAAACAGAAAAATAGGCGAATGAATCTTTTCTCTGTGTATCGAAGAATGGCCTCGCGGAGGCATGCGTCATGCTAGCGTGCGGGGTACTCTTGCTATCCATATGGTCCACAGGACACTCGTTGTTTTCGGATTTACCCTTTATGCGCCGGTTTTCAGCCACGCTTATGCCCAGCATCGTTACAACCAGACCGATACTAGATGTATAAAGTCCGCCATGCAGACGAGACCAGTCGGAGATTACCGAGCATTCTATCAGGTCGGCGACCACTAGTGAGCTACTGGAGCCGAGGGGTAACCACGATGCCGCTAAGAACCTCTCGGTCGACGCAAGCGATTACACTCCTGTCACATCATAATCGTTTGCTATTCAGGGGTTGACCAACACCGGAAAACTTTTCACTTGAAGTATTGTATACGACAGGGTGCGTGTACCTACCAAACCTGTTTAAACTAAGTTCAGACTAGTTGGAAGTGTGTCTAGATCTTAGTTTTCGTCACTAGAGGGCCCACGCTTTATTTTTATGATCCATTGATCTCCCAGACGCTGCAAGATTTGCAACCAGGCAGACTTGGCGGTAGGTCCTAGTGCAGCGGGACTTTTTTTCTATAGTCCTTGAGAGGAGGAGTCGTCAGTCCAGATACCTTTGATGTCCTGATTGGAAGGACCGTTGGCCCCCCACCCTTAGGCAGTGTACTCAGTTCCATAAACGAGCTATTAGATATGAGGTCCGTAGATTGAAAAGGGTGACGGAATTCGCCCGAACGGGAAAGACGGACAACTAGGTATCCTGAGCACGGTTGCGCGTCCGTATCAAGCTCCTCTTTATAGGCCCCGGTTTCTGTTGGTCGTAGAGCGCAGAACGGGTTGGGGGGATGTACGACAATATCGCTTAGTCACCTTTGGGCCACGGTCCGCTACCTTACAGGAATTGAGACCGTCCTTTAATTTCCCTTGCATATATGTTGCGTTTCTTCGACCTTTTAACCGCTCCCTTAGGAGAAAGACAGATAGCTTCTTACCCGTACTCCACCGTTGGCAGCACGATCGCATGTCCCACGTGAACCATTGGTAAACCCTGTGGCCTGTGAGCGACAAAAGCTTTAATGGGAAATTCGCGCCCATAACTTGGTCCGAATACGGGTCCTAGCAACGTTCGTCTGAGTTTGATCTATATAATACGGGCGGTATGTCTGCTTTGATCAACCTCCAATAGCTCGTATGATAGTGCACCCGCTGGTGATCACTCAATGATCTGGGCTCCCCGTTGCAACTACGGGGATTTTTCGAGACCGACCTGCGTTCGGCATTGTGGGCACAGTGAAGTATTAGCAAACGTTAAGTCCCGAACTAGATGTGACCTAACGGTAAGAGAATTTCATAATACGTCCTGCCGCACGCGCAAGGTACATTTGGACAGTATTGAATGGACTCTGATCAACCTTCACACCGATCTAGAATCGAATGCGTAGATCAGCCAGGTGCAAACCAAAAATTCTAGGTTACTAGAAGTTTTGCGACGTTCTAAGTGTTGGACGAAATGATTCGCGACCCAGGATGAGGTCGCCCTAAAAAAT"

p = "ATGC"
L = []
for i in range(len(x)):
	if x[i:i+len(p)] == p:
		L.append((i,modhorner(x[i:i+len(p)],11),modhorner(p,11)))
print((L))

# print(len(x))
print(len(modPatternMatch(11,p,x)))
print(len([1, 4, 15, 21, 37, 43, 54, 110, 111, 113, 125, 132, 150, 152, 166, 169, 182, 199, 207, 215, 235, 243, 247, 269, 278, 283, 304, 314, 322, 324, 329, 330, 372, 465, 468, 480, 488, 491, 502, 550, 563, 571, 593, 613, 623, 631, 645, 684, 685, 687, 694, 722, 723, 732, 733, 770, 774, 786, 827, 832, 833, 834, 835, 842, 865, 866, 867, 878, 898, 899, 905, 915, 920, 952, 969, 970, 978, 984, 1007, 1012, 1051, 1052, 1073, 1077, 1106, 1107, 1108, 1109, 1112, 1118, 1145, 1159, 1160, 1163, 1164, 1167, 1210, 1220, 1236, 1238, 1243, 1255, 1256, 1258, 1263, 1274, 1279, 1280, 1284, 1321, 1322, 1333, 1334, 1340, 1346, 1350, 1378, 1402, 1405, 1418, 1430, 1433, 1438, 1446, 1451, 1471, 1479, 1491, 1492, 1494, 1496, 1499, 1504, 1505, 1524, 1525, 1533, 1578, 1589, 1609, 1610, 1614, 1651, 1654, 1685, 1735, 1737, 1744, 1749, 1752, 1776, 1803, 1805, 1808, 1810, 1811, 1815, 1817, 1865, 1867, 1922, 1962, 1963, 1970, 1978, 1979, 1980, 1986, 1999, 2048, 2067, 2069, 2073, 2076, 2090, 2092, 2113, 2158, 2176, 2189, 2205, 2209, 2248, 2259, 2261, 2264, 2265, 2267, 2268, 2272, 2273, 2274, 2312, 2350, 2351, 2356, 2357, 2358, 2359, 2362, 2382, 2388, 2393, 2419, 2424, 2434, 2435, 2459, 2489, 2492, 2493, 2494, 2520, 2521, 2593, 2595, 2598, 2615, 2616, 2660, 2661, 2666, 2667, 2690, 2703, 2705, 2706, 2714, 2718, 2765, 2768, 2804, 2806, 2811, 2816, 2820, 2821, 2832, 2853, 2861, 2863, 2872, 2893, 2895, 2906, 2907, 2919, 2921, 2924, 2927, 2929, 2968, 3038, 3050, 3054, 3103, 3110, 3130, 3157, 3159, 3162, 3163, 3169, 3182, 3190, 3192, 3194, 3207, 3241, 3288, 3290, 3301, 3316, 3320, 3322, 3328, 3333, 3342, 3343, 3344, 3346, 3352, 3357, 3358, 3362, 3365, 3366, 3367, 3372, 3373, 3383, 3395, 3401, 3402, 3411, 3415, 3420, 3425, 3433, 3437, 3438, 3439, 3444, 3484, 3493, 3517, 3519, 3520, 3523, 3524, 3526, 3533, 3553, 3563, 3613, 3622, 3642, 3644, 3687, 3689, 3690, 3715, 3724, 3727, 3744, 3745, 3777, 3778, 3818, 3819, 3852, 3862, 3930, 3951, 3957, 3982, 3986, 4001, 4030, 4057, 4068, 4071, 4079, 4091, 4098, 4106, 4133, 4145, 4149, 4166, 4171, 4194, 4237, 4238, 4240, 4256, 4269, 4270, 4271, 4281, 4293, 4294, 4300, 4307, 4308, 4320, 4324, 4326, 4327, 4332, 4348, 4378, 4379, 4396, 4423, 4435, 4437, 4438, 4474, 4496, 4531, 4550, 4558, 4595, 4599, 4605, 4620, 4631, 4636, 4647, 4652, 4675, 4693, 4704, 4709, 4712, 4719, 4721, 4728, 4730, 4731, 4744, 4755, 4758, 4764, 4765, 4774, 4793, 4794, 4801, 4813, 4826, 4846, 4847, 4850, 4864, 4875, 4882, 4883, 4885, 4886, 4889, 4897, 4900, 4901, 4916, 4919, 4929, 4939, 4947, 4948, 4961, 4983, 5016, 5021, 5035, 5036, 5037, 5039, 5046, 5095, 5103, 5106, 5123, 5129, 5130, 5152, 5158, 5202, 5248, 5249, 5286, 5287, 5288, 5311, 5313, 5314, 5328, 5333, 5373, 5377, 5425, 5430, 5462, 5473, 5488, 5492, 5504, 5516, 5517, 5518, 5547, 5548, 5575, 5604, 5621, 5628, 5634, 5639, 5656, 5657, 5667, 5682, 5683, 5715, 5722, 5726, 5740, 5748, 5751, 5759, 5790, 5794, 5803, 5804, 5807, 5813, 5829, 5832, 5833, 5839, 5876, 5884, 5909, 5937, 5943, 5950, 5972, 5973, 5986, 6001, 6004, 6010, 6011, 6023, 6039, 6069, 6073, 6091, 6125, 6144, 6145, 6161, 6180, 6206, 6232, 6260, 6261, 6264, 6326, 6328, 6332, 6353, 6369, 6381, 6382, 6384, 6385, 6390, 6391, 6392, 6393, 6433, 6454, 6469, 6474, 6496, 6543, 6544, 6550, 6551, 6564, 6566, 6569, 6580, 6611, 6612, 6619, 6628, 6639, 6645, 6648, 6668, 6669, 6674, 6675, 6733, 6755, 6791, 6795, 6813, 6827, 6834, 6842, 6844, 6860, 6862, 6873, 6886, 6889, 6891, 6892, 6893, 6895, 6908, 6910, 6955, 6956, 6963, 6964, 6992, 7003, 7004, 7008, 7017, 7018, 7026, 7040, 7067, 7085, 7091, 7104, 7138, 7145, 7146, 7175, 7176, 7190, 7209, 7220, 7241, 7254, 7258, 7282, 7283, 7294, 7319, 7326, 7332, 7335, 7336, 7337, 7350, 7363, 7380, 7381, 7382, 7383, 7393, 7402, 7417, 7421, 7429, 7432, 7434, 7448, 7456, 7473, 7504, 7521, 7523, 7524, 7541, 7563, 7571, 7572, 7573, 7581, 7587, 7602, 7603, 7613, 7637, 7639, 7648, 7670, 7695, 7715, 7747, 7749, 7757, 7763, 7773, 7776, 7777, 7778, 7783, 7791, 7794, 7796, 7805, 7812, 7814, 7823, 7833, 7834, 7865, 7866, 7871, 7875, 7878, 7900, 7910, 7912, 7931, 7938, 7942, 7951, 7955, 7974, 7992, 7999, 8002, 8008, 8009, 8018, 8031, 8035, 8040, 8047, 8050, 8051, 8052, 8053, 8076, 8077, 8088, 8090, 8111, 8115, 8146, 8198, 8243, 8285, 8311, 8323, 8339, 8340, 8383, 8409, 8421, 8422, 8423, 8424, 8431, 8432, 8439, 8486, 8493, 8498, 8509, 8510, 8517, 8524, 8539, 8542, 8543, 8559, 8564, 8565, 8577, 8578, 8588, 8589, 8594, 8600, 8617, 8639, 8640, 8674, 8677, 8685, 8701, 8703, 8725, 8754, 8755, 8763, 8766, 8782, 8788, 8792, 8798, 8813, 8865, 8881, 8889, 8900, 8905, 8927, 8945, 8947, 8948, 8955, 8956, 8970, 8979, 9011, 9013, 9014, 9029, 9054, 9070, 9076, 9078, 9091, 9092, 9104, 9117, 9118, 9119, 9120, 9137, 9145, 9163, 9212, 9217, 9222, 9266, 9277, 9289, 9291, 9326, 9327, 9374, 9378, 9384, 9387, 9391, 9415, 9448, 9449, 9456, 9457, 9462, 9464, 9468, 9499, 9500, 9507, 9513, 9514, 9519, 9530, 9576, 9581, 9590, 9591, 9594, 9605, 9611, 9614, 9622, 9623, 9643, 9645, 9651, 9652, 9659, 9663, 9664, 9668, 9669, 9674, 9675, 9678, 9679, 9680, 9688, 9689, 9691, 9719, 9723, 9735, 9736, 9738, 9759, 9812, 9818, 9853, 9857, 9858, 9874, 9887, 9894, 9896, 9897, 9905, 9913, 9914, 9926, 9939, 9943, 9953, 9964, 9970, 9989, 9993, 9994, 9995]))