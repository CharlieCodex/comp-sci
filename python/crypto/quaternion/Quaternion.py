from numbers import Number
class Quaternion:
	'''Quaternion class that allows for basic operation'''
	def __init__(self, *vals):
		if not all([isinstance(v, Number) for v in vals]):
			raise ValueError("Error, all components must be of type Number")
		self.vals = vals

	def __mod__(self, n):
		return self.__class__(*[val % n for val in self.vals])

	def __add__(self, other):
		vals = [(self.vals[i] + other.vals[i]) for i in range(4)]
		result = self.__class__(*vals)
		return result

	def __sub__(self, other):
		return self + -other

	def __neg__(self):
		return self.__class__(*[-v for v in self.vals])

	def _conj(self):
		return self.__class__(*([self.vals[0]] + [-v for v in self.vals[1:]]))

	def __abs__(self):
		r2 = 0
		for val in self.vals:
			r2 += val ** 2
		return r2 ** 0.5

	def _components(self):
		'''Return a tuple representation of Q,
		   described as components (a, b, c, d)
		   a + b + c + d = Q'''
		return tuple(self.__class__(*[[0]*i+self.vals+[i]*(3-i)]) for i in range(3))

	def _pre_rot(self, unit):
		if unit == 0:
			return self.__class__(*self.vals)
		vals = [0]*4
		#a' will always be -unit component,
		#unit' will always be real component
		vals[0] = -self.vals[unit]
		vals[unit] = self.vals[0]
		if unit == 1:
			#ij = k
			vals[3] = self.vals[2]
			#-ik = j
			vals[2] = -self.vals[3]
		if unit == 2:
			#-jk = i
			vals[1] = self.vals[3]
			#ji = k
			vals[3] = -self.vals[1]
		if unit == 3:
			#ki = j
			vals[2] = self.vals[1]
			#-kj = i
			vals[1] = -self.vals[2]
		return self.__class__(*vals)

	def _post_rot(self, unit):
		if unit == 0:
			return self.__class__(*self.vals)
		if unit >= 4:
			raise ValueError("Error, Quaternion rotation undefined for units after k (3)")
		vals = [0]*4
		#a' will always be -unit component,
		#unit' will always be real component
		vals[0] = -self.vals[unit]
		vals[unit] = self.vals[0]
		if unit == 1:
			#ij = k
			vals[3] = -self.vals[2]
			#-ik = j
			vals[2] = self.vals[3]
		if unit == 2:
			#-jk = i
			vals[1] = -self.vals[3]
			#ji = k
			vals[3] = self.vals[1]
		if unit == 3:
			#ki = j
			vals[2] = -self.vals[1]
			#-kj = i
			vals[1] = self.vals[2]
		return self.__class__(*vals)

	def _scale(self, real):
		if isinstance(real, Quaternion):
			raise ValueError("Error, cannot scale Quaternion by Quaternion, call __mul__ instead")
		if isinstance(real, Number):
			result = self.__class__(*[real*v for v in self.vals])
			return result
		else:
			raise ValueError("Unsupported operands for _scale", Quaternion, real.__class__)

	def __mul__(self, other):
		if isinstance(other, Number):
			return self._scale(other)
		result = self.__class__._0()
		for unit, r in enumerate(other.vals):
			result += self._post_rot(unit)._scale(r)
		return result

	def _inverse(self):
		#return Q^-1 or Q'/|Q|^2 (Note how the abs of Q'/|Q|^2 = 1/|Q| or |1/Q|)
		return self._conj() / abs(self) ** 2

	def __truediv__(self, other):
		'''Returns Q * P^-1 = Q/P
		   note that / is ambiguous with P^-1 * Q
		   for P^-1 * Q either use P._inverse() * Q
		   or call Q._pre__div__(P)
		   or call Q.__div__(P)._conj()
		   or call (Q/P)._conj()'''
		if isinstance(other, Number):
			print(self.__class__)
			return self._scale(1 / other)
		#return Q * P^-1 = Q/P
		return self * other._inverse()

	def _pre__div__(self, other):
		'''Returns P^-1 * Q = Q/P
		   note that / is ambiguous with Q * P^-1
		   for Q * P^-1 either use Q * P._inverse()
		   or call Q.__div__(P)
		   or Q / P
		   or call Q._pre__div__(P)._conj()'''
		if isinstance(other, Number):
			return self._scale(1 / other)
		return other._inverse() * self

	def __repr__(self):
		a = str(self.vals[0])
		b = str(self.vals[1])
		c = str(self.vals[2])
		d = str(self.vals[3])
		return self.__class__.__name__+'(' + a + ' + ' + b + 'i + ' + c + 'j + ' + d +'k)'

	@classmethod
	def _0(cls):
		return cls(0, 0, 0, 0)

	@classmethod
	def _1(cls, r=1):
		return cls(r, 0, 0, 0)

	@classmethod
	def _i(cls, r=1):
		return cls(0, r, 0, 0)

	@classmethod
	def _j(cls, r=1):
		return cls(0, 0, r, 0)

	@classmethod
	def _k(cls, r=1):
		return cls(0, 0, 0, r)

	def __eq__(self, other):
		if self.__class__ == other.__class__:
			return self.__dict__ == other.__dict__
		elif isinstance(other, Quaternion):
			return self.vals == other.vals

	def is_re(self):
		return sum(self.vals[1:]) == 0

	def is_im(self):
		return self.vals[0] == 0

class GaussianQuaternion(Quaternion):
	def __init__(self, *vals):
		super().__init__(*[int(v) for v in vals])
		if self.vals != vals:
			assert TypeError("Warning: data lost in int conversion", vals, self.vals)

class BoundedQuaternion(GaussianQuaternion):
	#todo: add garbage collector for unused instance types
	__instances__ = {}
	
	def _inverse(self):
		'''Find the multiplative inverse self/1 mod self.n
		   ie: self * self._inverse = 1'''

	def __init__(self, *vals, n=None):
		if len(vals) == 5:
			n = vals[4]
			vals = vals[:4]
		super().__init__(*vals)
		if n:
			self.vals = [v % n for v in self.vals]
		else:
			assert TypeError(
				"Warning: unpredictable behavior for BoundedQuaternions of modulus None")
		self.n = n
		if self.__class__ == BoundedQuaternion:
			if not n in BoundedQuaternion.__instances__:
				class _BoundedQuaternion_(BoundedQuaternion):
					n = self.n
					def __init__(_, *args, **kwargs):
						kwargs.update({'n': self.n})
						super().__init__(*args, **kwargs)
					def __div__(self, other):
						return super().__div__(other)
				_BoundedQuaternion_.__name__ += str(n)
				self.__class__ = _BoundedQuaternion_
				BoundedQuaternion.__instances__[n] = _BoundedQuaternion_
			else:
				self.__class__ = BoundedQuaternion.__instances__[n]

	def _cast(self, other):
		return self % other.n

	def __mod__(self, n):
		if n != None:
			return self.__class__(*self.vals, n)
		return self.__class__(*self.vals, n)
