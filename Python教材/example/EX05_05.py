class Demo:
	__x = 0
	def __init__(self, i):
		self.__i = i
		Demo.__x += 1
	def hello(self):
		print("hello", self.__i)
	@classmethod
	def getX(cls):
		return cls.__x
	@classmethod
	def add(cls):
		Demo.__x +=1
class subDemo(Demo):
	def __init__(self, i, j):
		self.__i = i
		self.__j = j
	def hello(self):
		print("hello", self.__i,self.__j)
a = Demo("Tom")
a.hello()
b = subDemo("John","Mary")
b.hello()
print("Demo.x =", Demo.getX())
