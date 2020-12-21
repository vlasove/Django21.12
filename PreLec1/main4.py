"""
Один из принципов ООП - наследование.

Наследование - это процесс передачи состояний и поведений одного объекта другому. Объект ПЕРЕДАЮЩИЙ состояния и повоедение -
родительский объект. Объект ПРИНИМАЮЩИЙ состояния и поведение - дочерний.
"""

# Le Question 1
class Foo:
    def foo(self):
        print("foo!")


class Buzz(Foo):
    def foo(self):
        super().foo()
        print("foo from buzz!")


b = Buzz()
b.foo()

# Le Question 2
class A:
    a = "a"
    def print(self):
        print("a is:", self.a)

class B(A):
    b = "b"
    def print(self):
        print("b is:", self.b)

class C(A):
    c = "c"
    def print(self):
        print("c is:", self.c)

class D(B,C):
    d = "d"

obj_d = D()
obj_d.print()