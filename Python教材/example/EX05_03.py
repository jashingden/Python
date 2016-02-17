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

a = Demo('Tom')
print(Demo.getX())