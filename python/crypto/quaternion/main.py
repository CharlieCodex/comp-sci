from Quaternion import Quaternion, GaussianQuaternion, BoundedQuaternion
import random


def randquat(upper):
	return BoundedQuaternion(random.randint(0,upper), random.randint(0,upper), random.randint(0,upper), random.randint(0,upper), upper)

def main():
	g = BoundedQuaternion(36300, 29533, 24140, 16980, 2**8)
	d = randquat(2**16)
	print(g)
	print(d)
	print(d * g)
	pub = d * g
	k = randquat(2**16)
	print(k)
	print('gk', g * k)
	print('(dg)k', pub * k)
	print('d(gk)', d * (g * k))

if __name__ == '__main__':
	main()