#多重繼承
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
class Demo2:
	def __init__(self, i):
		self.__i = i
	def reverseString(self,string):
		reverse=''
		for i in range(len(string)-1, -1, -1):
			reverse += string[i]
		return reverse
class subDemo(Demo,Demo2):
	def __init__(self, i, j="guest"):
		super().__init__(i)
		self.__i = i
		self.__j = j
	def hello(self):
		print("hello", self.__i,self.__j)
	def superHello(self):
		super().__init__(self.__i)
		super().hello()
a = subDemo("Tom")
print(a.reverseString("Tom"))
print("Demo.x =", Demo.getX())