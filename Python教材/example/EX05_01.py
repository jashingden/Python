class Demo:
	__x = 0
	def __init__(self, i):
		self.i = i
		Demo.__x += 1

	def hello(self):
		print("hello", self.i)
a = Demo("Tom")
print(a.__x)