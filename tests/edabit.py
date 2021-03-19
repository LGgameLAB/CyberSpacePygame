def pentagonal(num):
	dots = 1
	for x in range(0, num-1):
		dots = dots + 5*x
	return dots

def two_powers_of_two(n):
	for x in range(-1, 10):
		for i in range(-1, 10):
			#print(str(2**x) + '|' + str(2**i))
			if 2**x + 2**i == n:
				return True
	
	return False

def two_powers_of_two2(n):
	return bin(n).count('1') == 2

print(two_powers_of_two2(8))