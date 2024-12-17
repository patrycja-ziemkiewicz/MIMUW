import numpy as np

def calculate_MSE(w_A, w_B, data):
    
    w_AB = np.meshgrid(w_A, w_B)
    w_AB[0] = w_AB[0].flatten(order='C')
    w_AB[1] = w_AB[1].flatten(order='C')

    x_A = data[:, 0]
    x_B = data[:, 1]
    probs_C = data[:, 2]

    M_w = 1 / (1 + np.exp(-(w_AB[0][:, None].dot(x_A[None, :]) + w_AB[1][:, None].dot(x_B[None, :]))))

    MSE = ((probs_C - M_w)**2).mean(axis=1)

    MSE = MSE.reshape(len(w_A), len(w_B))

    return MSE

def main():

    w_A = np.arange(0, 1.1, 0.1)
    w_B = np.arange(2, 3.1, 0.1)

    data = np.array([
        [1.0, 1.3, 0],
        [2.2, 1.1, 1],
        [2.0, 2.4, 1],
        [1.5, 3.2, 0],
        [3.2, 1.2, 1]
    ])

    MSE = calculate_MSE(w_A, w_B, data)

    print(MSE)

if __name__ == "__main__":
    main()


