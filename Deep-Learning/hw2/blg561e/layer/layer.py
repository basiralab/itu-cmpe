# Adapted from Stanford CS231n Course
import numpy as np
from abc import ABC, abstractmethod
from .helpers import flatten_unflatten


class Layer(ABC):
    def __init__(self, input_size, output_size):
        self.W = np.random.rand(input_size, output_size)
        self.b = np.zeros(output_size)
        self.x = None
        self.db = np.zeros_like(self.b)
        self.dW = np.zeros_like(self.W)

    @abstractmethod
    def forward(self, x):
        raise NotImplementedError('Abstract class!')

    @abstractmethod
    def backward(self, x):
        raise NotImplementedError('Abstract class!')

    def __repr__(self):
        return 'Abstract layer class'


class Dropout(Layer):
    def __init__(self, p=.5):
        '''
            :param p: dropout factor
        '''
        self.mask = None
        self.mode = 'train'
        self.p = p

    def forward(self, x, seed=None):
        '''
            :param x: input to dropout layer
            :param seed: seed (used for testing purposes)
        '''
        if seed is not None:
            np.random.seed(seed)
        # YOUR CODE STARTS
        if self.mode == 'train':
            # Create a dropout mask
            # The mask is divided with the probability to regularize the output
            # p is the probability that a random neuron will be kept
            mask = (np.random.rand(*np.shape(x)) < self.p) / self.p

            # Do not forget to save the created mask for dropout in order to use it in backward
            self.mask = mask.copy()
            # Apply the mask
            out = np.multiply(x, mask)

            return out
        elif self.mode == 'test':
            # Don't apply dropout when testing
            out = x
            return out
        # YOUR CODE ENDS
        else:
            raise ValueError('Invalid argument!')

    def backward(self, dprev):
        if self.mode == "train":
            # Use dropout
            dx = np.multiply(dprev, self.mask)
        elif self.mode == "test":
            # Don't use dropout
            dx = dprev
        else:
            raise ValueError('Invalid argument!')
        return dx


class BatchNorm(Layer):
    def __init__(self, D, momentum=.9):
        self.mode = 'train'
        self.normalized = None

        self.x_sub_mean = None
        self.momentum = momentum
        self.D = D
        self.running_mean = np.zeros(D)
        self.running_var = np.zeros(D)
        self.gamma = np.ones(D)
        self.beta = np.zeros(D)
        self.ivar = np.zeros(D)
        self.sqrtvar = np.zeros(D)

    # @flatten_unflatten
    def forward(self, x, gamma=None, beta=None):
        if self.mode == 'train':
            sample_mean = np.mean(x, axis=0)
            sample_var = np.var(x, axis=0)
            if gamma is not None:
                self.gamma = gamma.copy()
            if beta is not None:
                self.beta = beta.copy()

            # Normalise our batch
            self.normalized = ((x - sample_mean) / np.sqrt(sample_var + 1e-5)).copy()
            self.x_sub_mean = x - sample_mean

            # YOUR CODE HERE
            # Update our running mean and variance then store.
            # Running mean and variance are calculated to use in backprop
            running_mean = self.running_mean * self.momentum + sample_mean * (1 - self.momentum)
            running_var = self.running_var * self.momentum + sample_var * (1 - self.momentum)
            # Below formula is obtained from the original batch norm paper in section 3, algo. 1
            # y_i = \gamma*Xhat+\beta
            out = self.gamma * self.normalized + self.beta

            # YOUR CODE ENDS
            self.running_mean = running_mean.copy()
            self.running_var = running_var.copy()

            self.ivar = 1. / np.sqrt(sample_var + 1e-5)
            self.sqrtvar = np.sqrt(sample_var + 1e-5)

            return out
        elif self.mode == 'test':
            out = self.gamma * ((x - self.running_mean) / np.sqrt(self.running_var + 1e-5)) + self.beta
        else:
            raise Exception(
                "INVALID MODE! Mode should be either test or train")
        return out

    def backward(self, dprev):
        N, D = dprev.shape
        # YOUR CODE HERE
        dx, dgamma, dbeta = None, None, None
        # Partial derivatives of gamme and beta
        # Below formulae are obtained from the original batch norm paper in section 3, par. 8
        dgamma = np.sum(np.multiply(dprev, self.normalized), axis=0)
        dbeta = np.sum(dprev, axis=0)
        # Intermediary partial derivatives
        # For relatively large multiplications I prefer numpy's multiply method over python multiply
        dx_ = np.multiply(dprev, self.gamma)
        # Below formula is obtained from the original batch norm paper in section 3, par. 8
        # Formula: 1/(N*var)*(N*dXhat-\Sigma(dXhat)-X_norm*\Sigma(dXhat*X_norm))
        dx = 1/N * self.ivar * (N * dx_ - np.sum(dx_, axis=0) - np.multiply(self.normalized, np.sum(np.multiply(dx_, self.normalized), axis=0)))
        # Calculate the gradients
        return dx, dgamma, dbeta


class MaxPool2d(Layer):
    def __init__(self, pool_height, pool_width, stride):
        self.pool_height = pool_height
        self.pool_width = pool_width
        self.stride = stride
        self.x = None

    def forward(self, x):
        N, C, H, W = x.shape
        out_H = np.int(((H - self.pool_height) / self.stride) + 1)
        out_W = np.int(((W - self.pool_width) / self.stride) + 1)

        self.x = x.copy()

        # Initiliaze the output
        out = np.zeros([N, C, out_H, out_W])

        # Implement MaxPool
        for instance in range(N):  # for each input data
            for channel in range(C):  # per filter
                for height in range(out_H):
                    for width in range(out_W):
                        h = height * self.stride  # Starting height
                        w = width * self.stride  # Starting width
                        window = x[instance, channel, h:h + self.pool_height, w:w + self.pool_width]
                        # Get max window
                        out[instance, channel, height, width] = np.max(window)

        return out

    def backward(self, dprev):
        x = self.x
        N, C, H, W = x.shape
        _, _, dprev_H, dprev_W = dprev.shape

        dx = np.zeros_like(self.x)

        # Calculate the gradient (dx)
        # YOUR CODE HERE
        for instance in range(N):  # for each input data
            for channel in range(C):  # per filter
                for height in range(dprev_H):
                    for width in range(dprev_W):
                        h = height * self.stride  # Starting height
                        w = width * self.stride  # Starting width
                        window = x[instance, channel, h:h + self.pool_height, w:w + self.pool_width]
                        # Get max window (max window is recalculated because switches are not being
                        # used in this implementation)
                        activation_window = np.max(window)
                        neurons_to_activate = activation_window == window
                        dx[instance, channel, h:h + self.pool_height, w:w + self.pool_width] = np.multiply(neurons_to_activate, dprev[instance, channel, height, width])
        return dx


class Flatten(Layer):
    def __init__(self):
        self.N, self.C, self.H, self.W = 0, 0, 0, 0

    def forward(self, x):
        self.N, self.C, self.H, self.W = x.shape
        out = x.reshape(self.N, -1)
        return out

    def backward(self, dprev):
        return dprev.reshape(self.N, self.C, self.H, self.W)
