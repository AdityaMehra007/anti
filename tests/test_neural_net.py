import math
import unittest
from byox.neural_net.engine import Value
from byox.neural_net.nn import Neuron, Layer, MLP
from byox.neural_net.optim import SGD, mse_loss

class TestNeuralNet(unittest.TestCase):
    def test_autograd_basic_operations(self):
        # f(x, y) = (x * y) + (x + y)^2
        x = Value(2.0)
        y = Value(3.0)
        
        xy = x * y           # 6.0
        x_plus_y = x + y     # 5.0
        sq = x_plus_y ** 2   # 25.0
        f = xy + sq          # 31.0
        
        self.assertAlmostEqual(f.data, 31.0)
        
        f.backward()
        
        # df/dx = y + 2*(x+y) = 3 + 2*(5) = 13.0
        # df/dy = x + 2*(x+y) = 2 + 2*(5) = 12.0
        self.assertAlmostEqual(x.grad, 13.0)
        self.assertAlmostEqual(y.grad, 12.0)

    def test_activations_and_chain_rule(self):
        x = Value(0.5)
        # tanh(0.5)
        t = x.tanh()
        t.backward()
        # d/dx tanh(x) = 1 - tanh(x)^2
        expected_grad = 1.0 - math.tanh(0.5) ** 2
        self.assertAlmostEqual(t.data, math.tanh(0.5))
        self.assertAlmostEqual(x.grad, expected_grad, places=5)

        # ReLU test
        a = Value(-2.0)
        b = a.relu()
        b.backward()
        self.assertEqual(b.data, 0.0)
        self.assertEqual(a.grad, 0.0)

        c = Value(3.0)
        d = c.relu()
        d.backward()
        self.assertEqual(d.data, 3.0)
        self.assertEqual(c.grad, 1.0)

    def test_mlp_training_convergence(self):
        import random
        random.seed(42)
        # Train an MLP on XOR pattern:
        # [0, 0] -> 0
        # [0, 1] -> 1
        # [1, 0] -> 1
        # [1, 1] -> 0
        xs = [
            [2.0, 3.0, -1.0],
            [3.0, -1.0, 0.5],
            [0.5, 1.0, 1.0],
            [1.0, 1.0, -1.0],
        ]
        ys = [1.0, -1.0, -1.0, 1.0]

        mlp = MLP(3, [4, 4, 1])
        optimizer = SGD(mlp.parameters(), lr=0.1)

        initial_loss = None
        final_loss = None

        for step in range(60):
            # Forward pass
            ypred = [mlp(x) for x in xs]
            loss = mse_loss([y[0] if isinstance(y, list) else y for y in ypred], ys)
            
            if step == 0:
                initial_loss = loss.data
                
            final_loss = loss.data

            # Backward pass
            optimizer.zero_grad()
            loss.backward()

            # Update weights
            optimizer.step()

        self.assertIsNotNone(initial_loss)
        self.assertIsNotNone(final_loss)
        self.assertLess(final_loss, initial_loss)
        self.assertLess(final_loss, 0.2)

if __name__ == "__main__":
    unittest.main()
