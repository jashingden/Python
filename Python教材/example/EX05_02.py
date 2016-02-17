class Demo:
	i=0   #i 類別變數
	def __init__(self,i):
		self.i = i  #i 實體變數
		Demo.i += 1
	def hello(self):
		print("hello",self.i)

		
print("There are", Demo.i, "instances.")
a = Demo(1122)
a.hello()
print("a.i =", a.i)
b = Demo(3344)
b.hello()
print("b.i =", b.i)
c = Demo(5566)
c.hello()
print("c.i =", c.i)
d = Demo(7788)
d.hello()
print("d.i =", d.i)
e = Demo(9900)
e.hello()
print("e.i =", e.i)
'''
print("a.i =", a.i)
print("b.i =", b.i)
print("c.i =", c.i)
print("d.i =", d.i)
'''

print("After all, there are", Demo.i, "instances.")
