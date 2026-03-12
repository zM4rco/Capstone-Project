import numpy as np

def trilaterate(positions, distances):
    # Extract positions and distances
    A, B, C = positions
    dA, dB, dC = distances

    # Coordinates of the points
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    # Calculating the trilateration
    P1 = 2 * B - 2 * A
    P2 = 2 * C - 2 * B

    # Distances squared
    dA2 = dA ** 2
    dB2 = dB ** 2
    dC2 = dC ** 2

    # Solving the equations
    A_matrix = np.array([[P1[0], P1[1]], [P2[0], P2[1]]])
    b = np.array([
        dA2 - dB2 - A[0]**2 + B[0]**2 - A[1]**2 + B[1]**2,
        dB2 - dC2 - B[0]**2 + C[0]**2 - B[1]**2 + C[1]**2
    ])

    # Calculate the position using the least squares solution
    position = np.linalg.lstsq(A_matrix, b, rcond=None)[0]

    # Adding the coordinates of point A to find the actual position
    return A + position

# Example usage
if __name__ == "__main__":
    # Coordinates of the access points (x, y)
    positions = [
        (0, 0),    # Access Point A
        (4, 0),    # Access Point B
        (2, 3)     # Access Point C
    ]

    # Distances to the access points
    distances = [
        2.5,  # Distance to Access Point A
        2.0,  # Distance to Access Point B
        1.5   # Distance to Access Point C
    ]

    estimated_position = trilaterate(positions, distances)
    print(f"Estimated Position: {estimated_position}")
