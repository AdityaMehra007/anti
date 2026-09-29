"""
Neural Network Architectures: Neuron, Layer, and Multi-Layer Perceptron (MLP).
"""

import random
from typing import List, Union
from byox.neural_net.engine import Value

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0.0

    def parameters(self) -> List[Value]:
        return []


class Neuron(Module):
    def __init__(self, nin: int, nonlin: bool = True):
        # Xavier/uniform initialization
        limit = (1.0 / nin) ** 0.5 if nin > 0 else 1.0
        self.w = [Value(random.uniform(-limit, limit)) for _ in range(nin)]
        self.b = Value(0.0)
        self.nonlin = nonlin

    def __call__(self, x: List[Union[Value, float]]) -> Value:
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return act.tanh() if self.nonlin else act

    def parameters(self) -> List[Value]:
        return self.w + [self.b]


class Layer(Module):
    def __init__(self, nin: int, nout: int, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]

    def __call__(self, x: List[Union[Value, float]]) -> Union[Value, List[Value]]:
        outs = [n(x) for n in self.neurons]
        return outs[0] if len(outs) == 1 else outs

    def parameters(self) -> List[Value]:
        params = []
        for n in self.neurons:
            params.extend(n.parameters())
        return params


class MLP(Module):
    def __init__(self, nin: int, nouts: List[int]):
        sz = [nin] + nouts
        self.layers = [
            Layer(sz[i], sz[i+1], nonlin=(i != len(nouts) - 1))
            for i in range(len(nouts))
        ]

    def __call__(self, x: List[Union[Value, float]]) -> Union[Value, List[Value]]:
        for layer in self.layers:
            x = layer(x)
            if not isinstance(x, list):
                x = [x]
        return x if len(x) > 1 else x[0]

    def parameters(self) -> List[Value]:
        params = []
        for layer in self.layers:
            params.extend(layer.parameters())
        return params
