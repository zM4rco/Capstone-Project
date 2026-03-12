import numpy as np

def trilateration(p1, p2, p3, d1, d2, d3):
    """
    Trilateration function to find the intersection point based on distances from three known points.
    
    Args:
    p1, p2, p3 : tuple
        Coordinates of the three known reference points (x, y).
    d1, d2, d3 : float
        Distances from the unknown point to each of the three reference points.

    Returns:
    (x, y) : tuple
        Coordinates of the unknown point.
    """

    # Coordinates of reference points
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # Using the equations derived from distance formulas
    # 1. (x - x1)^2 + (y - y1)^2 = d1^2
    # 2. (x - x2)^2 + (y - y2)^2 = d2^2
    # 3. (x - x3)^2 + (y - y3)^2 = d3^2
    # Expand these equations and arrange terms to set up a linear system

    # Create coefficients for the linear equations derived from the distances
    A = np.array([
        [2 * (x2 - x1), 2 * (y2 - y1)],
        [2 * (x3 - x1), 2 * (y3 - y1)]
    ])
    
    b = np.array([
        [d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2],
        [d1**2 - d3**2 - x1**2 + x3**2 - y1**2 + y3**2]
    ])

    # Solve for (x, y) using linear algebra
    try:
        x, y = np.linalg.solve(A, b)
        return (float(x), float(y))
    except np.linalg.LinAlgError:
        return None

# Example usage with three reference points and distances
p1 = (1, 3)     # Point A
p2 = (3, 8)     # Point B
p3 = (8, 4)     # Point C
d1 = 3.98       # Distance to point A
d2 = 5.01       # Distance to point B
d3 = 3.98       # Distance to point C

result = trilateration(p1, p2, p3, d1, d2, d3)
print("Calculated location of unknown access point:", result)
