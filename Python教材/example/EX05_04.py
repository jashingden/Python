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
	pass
a = Demo("Tom")
b = subDemo("John")
#isinstance
print(isinstance(a, Demo))
print(isinstance(a, subDemo))
print(isinstance(b, Demo))
print(isinstance(b, subDemo))
#issubclass
print(issubclass(subDemo, Demo))
print(issubclass(Demo, subDemo))
