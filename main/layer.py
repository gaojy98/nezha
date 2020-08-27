class ConvLayer:
    '''
    Convolutional Layer:
    Batch size: N
    Output Image size: W * H
    Input Channel size: C
    Output Channel size: K
    Filter Size: R * S
    Stride size: strideW, strideH
    '''
    def __init__(self, N, W, H, C, K, R, S, strideW = 1, strideH = 1):
        self.N = N
        self.W = W
        self.H = H
        self.C = C
        self.K = K
        self.R = R
        self.S = S
        self.strW = strideW
        self.strH = strideH
        self.inW = strideW * (W - 1) + R
        self.inH = strideH * (H - 1) + S

    def get_sizes(self):
        return [self.N, self.W, self.H, self.C, self.K, self.R, self.S]

    def get_image_size(self):
        return self.N * self.inW * self.inH * self.C

    def get_filter_size(self):
        return self.C * self.K * self.R * self.S

    def get_output_size(self):
        return self.N * self.W * self.H * self.K

class FCLayer(ConvLayer):
    '''
    Fully Connected Layer:
    Batch size: N
    Input Neural Number: C
    Output Neural Number: K
    '''
    def __init__(self, N, C, K):
        ConvLayer.__init__(self, N, 1, 1, C, K, 1, 1)
