"""
Scalar Autograd Engine: Computational Graph and Reverse-Mode Differentiation.
"""

import math
from typing import Set, Tuple, Union

class Value:
    def __init__(self, data: float, _children: Tuple["Value", ...] = (), _op: str = ""):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other: Union["Value", float, int]) -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward

        return out

    def __radd__(self, other: Union[float, int]) -> "Value":
        return self + other

    def __neg__(self) -> "Value":
        return self * -1.0

    def __sub__(self, other: Union["Value", float, int]) -> "Value":
        return self + (-other)

    def __rsub__(self, other: Union[float, int]) -> "Value":
        return (-self) + other

    def __mul__(self, other: Union["Value", float, int]) -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __rmul__(self, other: Union[float, int]) -> "Value":
        return self * other

    def __pow__(self, other: Union[int, float]) -> "Value":
        assert isinstance(other, (int, float)), "Power must be int or float"
        out = Value(self.data ** other, (self,), f"**{other}")

        def _backward():
            self.grad += (other * (self.data ** (other - 1))) * out.grad
        out._backward = _backward

        return out

    def __truediv__(self, other: Union["Value", float, int]) -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        return self * (other ** -1)

    def __rtruediv__(self, other: Union[float, int]) -> "Value":
        return Value(other) / self

    def relu(self) -> "Value":
        out = Value(max(0.0, self.data), (self,), "ReLU")

        def _backward():
            self.grad += (1.0 if out.data > 0 else 0.0) * out.grad
        out._backward = _backward

        return out

    def tanh(self) -> "Value":
        x = self.data
        t = math.tanh(x)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1.0 - t ** 2) * out.grad
        out._backward = _backward

        return out

    def sigmoid(self) -> "Value":
        x = self.data
        # Clip to prevent overflow
        x_clipped = max(-500.0, min(500.0, x))
        s = 1.0 / (1.0 + math.exp(-x_clipped))
        out = Value(s, (self,), "sigmoid")

        def _backward():
            self.grad += (s * (1.0 - s)) * out.grad
        out._backward = _backward

        return out

    def backward(self):
        # Topological sort of all nodes in computational graph
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        # Seed the gradient at root
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()
