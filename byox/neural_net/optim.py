"""
Optimization Algorithms and Loss Functions for Neural Networks.
"""

from typing import List, Union
from byox.neural_net.engine import Value

class SGD:
    def __init__(self, parameters: List[Value], lr: float = 0.01):
        self.parameters = parameters
        self.lr = lr

    def zero_grad(self):
        for p in self.parameters:
            p.grad = 0.0

    def step(self):
        for p in self.parameters:
            p.data -= self.lr * p.grad


def mse_loss(
    predictions: List[Union[Value, float]],
    targets: List[Union[Value, float]]
) -> Value:
    assert len(predictions) == len(targets), "Predictions and targets must match length"
    losses = []
    for ypred, ytarget in zip(predictions, targets):
        p = ypred if isinstance(ypred, Value) else Value(ypred)
        t = ytarget if isinstance(ytarget, Value) else Value(ytarget)
        diff = p - t
        losses.append(diff ** 2)

    total = sum(losses, Value(0.0))
    return total / len(predictions)
