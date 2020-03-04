import numpy as np

class LinearRegression:
    def __init__(self):
        pass
    
    def initialize_weights(self, weights_len):
        return np.zeros((weights_len, 1)), 0
    
    def fit(self, X, y, epochs=1, learning_rate=0.01):
        self.X = X.T
        self.y = y.T
        self.epochs = epochs
        self.learning_rate = learning_rate
        
        m = len(X)
        features_count = X.shape[1]

        self.W, self.b = self.initialize_weights(features_count)

        for i in range(epochs):
            A = self.forward_propagate(self.W, self.b, self.X)
            
            if (i + 1) % 100 == 0 or i == 0:
                print('Epoch ' + str(i + 1) + ' cost: ' + str(self.compute_cost(m, A, self.y)))
            
            # -------------------- #
            bp_result = self.backward_propagate(m, self.X, A, self.y)
            result = self.optimize(learning_rate, self.W, bp_result['dW'], self.b, bp_result['db'])
            self.W = result['W']
            self.b = result['b']
        
    def forward_propagate(self, W, b, X):
        return np.dot(W.T, X) + b
    
    def backward_propagate(self, m, X, A, y):
        dZ = A - y
        dW = (1 / m) * dZ.dot(X.T)
        db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)
        
        return {
            'dW': dW.T,
            'db': db,
        }
    
    def optimize(self, learning_rate, W, dW, b, db):
        return {
            'W': W - learning_rate * dW,
            'b': b - learning_rate * db,
        }
    
    def compute_cost(self, m, A, y):
        return np.sum(np.power(A - y, 2)) / (2 * m)
    
    def predict(self, X):
        return self.forward_propagate(self.W, self.b, X.T)