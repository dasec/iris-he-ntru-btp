from itertools import chain, starmap, zip_longest
import math, random

def extgcd(a, b):
    u, v, s, t = 1, 0, 0, 1
    while b!=0:
        q=a//b
        a, b = b, a-q*b
        u, s = s, u-q*s
        v, t = t, v-q*t
    return a, u, v

def invModQ(a,q):
    g, u, v=extgcd(a, q)
    if g > 1:
        print("{} has no inverse mod {}, gcd={}".format(a,q,g))
        return None
    return u%q

class ConvPoly(object):
	def __init__(self, coef=[0], N=None):
		if N is None:
			self.N = len(coef)
			self.coef = coef
		else:
			self.N = N
			self.coef = coef + [0]*(N-len(coef))
	def __repr__(self):
		return type(self).__name__ + str(self.coef)
	def __add__(self, other):
		if isinstance(other, type(self)) and (self.N == other.N):
			return ConvPoly(list(starmap(sum,zip_longest(zip(self.coef, other.coef)))))
		elif isinstance(other, int):
			return ConvPoly([self.coef[0]+other] + self.coef[1:])
		else:
			return NotImplemented
	def __radd__(self, other):
		return self + other
	def __eq__(self, other):
		if self.coef == other.coef:
			return True
		return False
	def __ne__(self, other):
		return not (self == other)
	def __neg__(self):
		return type(self)(list(starmap(lambda x: -x, other.coef), zip_longest(other.q)))
	def __sub__(self, other):
		return self + (-other)
	def __rsub__(self, other):
		return self - other
	def __mul__(self, other):
		if isinstance(other, type(self)) and self.N == other.N:
			coefs = []
			for k in range(self.N):
				s = 0
				for i in range(self.N):
					s += self.coef[i] * other.coef[(k-i)%self.N]
				coefs.append(s)
			return type(self)(coefs)
		elif isinstance(other, int):
			return type(self)([ other*c for c in self.coef ])
		else:
			return NotImplemented
	def __rmul__(self, other):
		return self*other

class PolyModQ(object):
    def __init__(self, coef, q):
        coef = list(starmap(lambda x: x%q, zip_longest(coef)))
        for index, val in enumerate(coef[::-1]):
            if val != 0:
                break
        self.coef = coef[:len(coef)-index]
        self.degree = len(self.coef)-1
        self.q = q
    def __repr__(self):
        return type(self).__name__ + "(" + str(self.coef) + ", " + str(self.q) + ")"
    def __eq__(self, other):
        if self.degree == other.degree:
            for pair in zip(self.coef, other.coef):
                if pair[0] != pair[1]:
                    return False
            return True
        return False
    def __ne__(self, other):
        return not (self == other)
    def __neg__(self):
        return type(self)(map(lambda x: -x, self.coef), self.q)
    def __add__(self, other):
        if isinstance(other, type(self)) and self.q == other.q:
            if self.degree > other.degree:
                return type(self)(map(sum,zip(self.coef, other.coef + [0]*(self.degree-other.degree))),self.q)
            elif self.degree < other.degree:
                return other + self
            else:
                return type(self)(map(sum,zip(self.coef, other.coef)),self.q)
        elif isinstance(other, ConvPoly):
            return self + ConvModQ(other.coef, self.q, self.N)
        elif isinstance(other, int):
            return type(self)([self.coef[0]+other] + self.coef[1:],self.q)
        else:
            return NotImplemented
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        if isinstance(other, type(self)) or isinstance(other, int):
            return self + (-other)
        else:
            return NotImplemented
    def __rsub__(self, other):
        return self - other
    def __mul__(self, other):
        if isinstance(other, type(self)) and self.q == other.q:
            coef = [0]*(self.degree+other.degree+1)
            for index1,c1 in enumerate(self.coef):
                for index2,c2 in enumerate(other.coef):
                    coef[index1+index2] += c1*c2
            return type(self)(coef, self.q)
        elif isinstance(other, int):
            return type(self)([ other*c for c in self.coef], self.q)
        else:
            return NotImplemented
    def __rmul__(self, other):
        return self*other
    def polydiv(self, denom):
        nom = PolyModQ([1]*(self.realdegree(self.coef)+1), self.q)
        for i in range(0, nom.realdegree(nom.coef)+1):
            nom.coef[i] = self.coef[i]
        n = nom.realdegree(nom.coef)
        d = denom.realdegree(denom.coef)
        if n < d:
            return (PolyModQ([0], nom.q), nom)
        quot = PolyModQ([1]*(n-d+1), nom.q) 
        leadcoefinv = invModQ(denom.coef[d], nom.q) 
        if leadcoefinv == None:
            print("The leadcoefinv of the divisor could not create an inverse mod {}".format(nom.q)) #this error should not occur for f,g 
            return None
        for i in reversed(range(0, n-d+1)):
            quot.coef[i] = nom.coef[i + d]*leadcoefinv
            quot.coef[i] = quot.coef[i]%nom.q
            for j in reversed(range(0, d)):
                nom.coef[i+j] = nom.coef[i+j] - denom.coef[j]*quot.coef[i]
                nom.coef[i+j] = nom.coef[i+j]%nom.q
        rem = PolyModQ([1]*d, nom.q) 
        for j in reversed(range(0, d)):
            rem.coef[j] = nom.coef[j]
        return (quot, rem)
    def realdegree(self, coef):
        for i in reversed(range(0, len(coef))):
            if self.coef[i] != 0:
                return i
        return 0
    def extgcdPoly(self, b):
        a = PolyModQ([1]*(self.realdegree(self.coef)+1), self.q) 
        for i in range(0, a.realdegree(a.coef)+1):
            a.coef[i] = self.coef[i]
        u = PolyModQ([1], self.q)
        v = PolyModQ([0], self.q)
        s = PolyModQ([0], self.q)
        t = PolyModQ([1], self.q)
        degb = b.realdegree(b.coef)
        while degb != 0:
            qr = a.polydiv(b)
            if qr is None:
                return None
            q = qr[0] #a//b
            a, b = b, a-q*b
            degb = b.realdegree(b.coef)
            u, s = s, u-q*s
            v, t = t, v-q*t
        if b.coef[0] == 0:
            print("Found a true divisor  =", q, ". Hence, computationally impossible to find an iverse of f!")
            return None
        if invModQ(b.coef[0], self.q) == None:
            print("{} has no inverse mod {}, Creating a fresh random f and trying again.".format(b.coef[0], self.q))
            return None
        else:
            #print("Found inverse!")
            u = s
            v = t
            c = invModQ(b.coef[0], self.q)
            for i in range(0, u.realdegree(u.coef)+1):
                u.coef[i] = c*u.coef[i]%self.q
            for i in range(0, v.realdegree(v.coef)+1):
                v.coef[i] = c*v.coef[i]%self.q
            return b, u, v
    def centerLift(self):
        coefs = []
        for c in self.coef:
            if c>self.q/2.0:
                coefs.append(c-self.q)
            else:
                coefs.append(c)
        return ConvPoly(coefs)


class ConvModQ(PolyModQ):
    def __init__(self, coef, q, N=None):
        coef = list(starmap(lambda x: x%q, zip_longest(coef)))
        if N is None:
            self.N = len(coef)
            self.coef = coef
        else:
            self.N = N
            self.coef = coef + [0]*(N-len(coef))
        self.degree = len(self.coef)-1
        self.q = q
    def __repr__(self):
        return type(self).__name__ + "(" + str(self.coef) + ", " + str(self.q) + ")"
    def __mul__(self, other):
        if isinstance(other, type(self)) and self.N == other.N:
            coefs = []
            for k in range(self.N):
                s = 0
                for i in range(self.N):
                    s += self.coef[i] * other.coef[(k-i)%self.N]
                coefs.append(s)
            return type(self)(coefs, self.q, self.N)
        elif isinstance(other, ConvPoly):
            other = ConvModQ(other.coef, self.q, self.N)
            return self*other
        elif isinstance(other, int):
            return type(self)([ other*c for c in self.coef ], self.q, self.N)
        else:
            return NotImplemented
    def __div__(self, other):
        if isinstance(other, type(self)):
            return self*other.inverse()
        elif isinstance(other, int):
            otherinv = invModQ(other, self.q)
            if otherinv is None:
                raise Exception("{} not invertible mod {}".format(other, self.q))
            return self*otherinv
        else:
            return NotImplemented
    def modQ(self, q):
        return ConvModQ(self.coef, q, self.N)
    def extgcdPoly(self, other):
        ggTuv = PolyModQ.extgcdPoly(self, other)
        if ggTuv == None:
            return None
        c = ggTuv[1].coef
        u = ConvModQ(c, self.q, self.N)
        return u
    def inverse(self, N=None, debug=False):
        if N == None:
            N = self.N
        Modulus = PolyModQ([-1] + [0]*(N-1) + [1], self.q)
        inv = self.extgcdPoly(Modulus)
        if inv is None:
            return None
        return inv
    def mult(self, other):
        return self.__mul__(other)

class NTRUParams(object):
	def __init__(self, security_in_bits): 
		if security_in_bits == 112: 
			self.N=401
			self.d1=8
			self.d2=8
			self.d3=6
			self.dg=133
			self.df=71
		elif security_in_bits == 128: 
			self.N=439
			self.d1=9
			self.d2=8
			self.d3=5
			self.dg=146
			self.df=75
		elif security_in_bits == 192: 
			self.N=593
			self.d1=10
			self.d2=10
			self.d3=8
			self.dg=197
			self.df=84
		elif security_in_bits == 256: 
			self.N=743
			self.d1=11
			self.d2=11
			self.d3=15
			self.dg=247
			self.df=90
		else:
			raise Exception("Not implemented. :(")
		self.q = 2053
		self.p = 2

class NTRUKey(object):
    r=random.SystemRandom()
    def __init__(self, ring=None, f=None, g=None, simplef=False):
        if ring is None:
            ring = NTRUParams(128)
        elif isinstance(ring, int):
            ring = NTRUParams(ring)
        self.ring = ring
        if simplef == True:
            self.a1 = self.randomTrinary(self.ring.d1+1, self.ring.d1, self.ring.N)
            self.a2 = self.randomTrinary(self.ring.d2+1, self.ring.d2, self.ring.N)
            self.a3 = self.randomTrinary(self.ring.d3+1, self.ring.d3, self.ring.N)
            self.ai = self.a1*self.a2+self.a3
            self.f1 = ConvPoly(self.ai.coef)
            self.f1p = self.ring.p*self.f1
            self.f = 1+self.f1p
            self.f = ConvModQ(self.f.coef, self.ring.q)
            self.finvp = ConvModQ([1]+ [0]*(self.ring.N-1), self.ring.p)  
        if f is None and simplef == False:
            self.f = self.randomTrinary(self.ring.df+1, self.ring.df,self.ring.N)
        if g is None:
            self.g = self.randomTrinary(self.ring.dg, self.ring.dg-1, self.ring.N)
        self.finvq = self.f.inverse()
        if simplef == False:
            while self.finvq is None:
                print("finv was None. Retrying 1.")
                self.f = self.randomTrinary(self.ring.df+1, self.ring.df, self.ring.N)
                self.finvq = self.f.inverse()
            if simplef == False:
                self.finvp = ConvModQ(self.f.centerLift().coef, self.ring.p).inverse()
        if simplef == True:
            while self.finvq is None:
                print("simple finvq was None. Retrying 1.")
                self.a1 = self.randomTrinary(self.ring.d1+1, self.ring.d1, self.ring.N)
                self.a2 = self.randomTrinary(self.ring.d2+1, self.ring.d2, self.ring.N)
                self.a3 = self.randomTrinary(self.ring.d3+1, self.ring.d3, self.ring.N)
                self.ai = self.a1*self.a2+self.a3
                self.f1 = ConvPoly(self.ai.coef)
                self.f1p = self.ring.p*self.f1
                self.f = 1+self.f1p
                self.f = ConvModQ(self.f.coef, self.ring.q)
                self.finvp = ConvModQ([1]+ [0]*(self.ring.N-1), self.ring.p)
        while self.finvq is None and simplef == False or self.finvp is None:
            print("finv was None. Retrying 2.")
            self.f = self.randomTrinary(self.ring.df+1, self.ring.df,self.ring.N)
            self.finvq = self.f.inverse()
            if self.finvq is None:
                continue
            self.finvp = ConvModQ(self.f.coef, self.ring.p).inverse()
        self.h = self.finvq * self.g * self.ring.p #if p is multiplied into pk h, we save multiplications during the encryption process
    def randomTrinary(self, d1,d2,polylength):
        arr = [1]*d1 + [-1]*d2 + [0]*(polylength - d1 - d2)
        self.r.shuffle(arr)
        return ConvModQ(arr, self.ring.q, self.ring.N)
    def publicKey(self):
        return (self.ring, self.h)

def chunk(N, iter):
	for i in range(int(math.ceil(len(iter)/float(N)))):
		yield iter[i*N:(i+1)*N]

def NTRUBlockEncrypt(ring, h, m):
	rvars = [1]*ring.dg + [-1]*ring.dg + [0]*(ring.N-2*ring.dg)
	random.shuffle(rvars)
	r = ConvModQ(rvars, ring.q)
	#c = ring.p*r*h+m #better to multiply p into the pk h, saves 1 multiplication for every encrypted block
	c = r*h+m
	return c

def NTRUEncrypt(ring, pub, m):
    if len(m) > ring.N:
        msplit = [ m for m in chunk(ring.N, m) ]
        n = len(msplit[-1])
        m = list(starmap(lambda m: ConvPoly(m, ring.N), zip_longest(msplit)))
    else:
        n = len(m)
        m = [ConvPoly(m, ring.N)]
    menc = list(starmap(lambda m: NTRUBlockEncrypt(ring, pub, m), zip_longest(m)))
    return (menc,n)

def NTRUBlockDecrypt(key, c):
    a = key.f*c
    if key.finvp.realdegree(key.finvp.coef) == 1 and key.finvp.coef[0] ==1: #Fall simplef=True
        a = ConvModQ(a.coef, key.ring.p)
        return ConvPoly(a.coef)
    aprime = a.centerLift()
    m = key.finvp*aprime
    return m.centerLift()

def NTRUDecrypt(key, cl, n):
    if len(cl)==1:
        m = NTRUBlockDecrypt(key, cl[0])
        return m.coef[:n]
    cl = list(starmap(lambda c: NTRUBlockDecrypt(key, c), zip_longest(cl)))
    mlist = [ c.coef for c in cl[:-1] ]
    mlist.append(cl[-1].coef[:n])
    m = list(chain.from_iterable(mlist))
    return m

def __sum2ciphertexts(c1, c2):
    c_sum = []
    for block in range(len(c1)):
        c_sum.append(([c1[block][0][0] + c2[block][0][0]], c1[block][1]))
    return c_sum


