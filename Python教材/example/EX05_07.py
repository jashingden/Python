class Demo:
	def __init__(self, i):
		self.i = i

	def __str__(self):
		return 'hello world'

	def __del__(self):
		print("del called: " + self.__str__())

	def hello(self):
		print("hello " + self.__str__())
a = Demo("Tommy")
a.hello()
print( str(a) )







