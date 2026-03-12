import math

# Given data
A = (1, 3)
B = (3, 8)
C = (8, 4)
RSSI_A = -9
RSSI_B = -10
RSSI_C = -9
RSSI_0 = -3  # Reference RSSI at 1 meter
n = 1  # Path-loss exponent for free space

# Function to calculate distance from RSSI
def rssi_to_distance(rssi, rssi0=RSSI_0, path_loss_exponent=n):
    return 10 ** ((rssi0 - rssi) / (10 * path_loss_exponent))

# Convert RSSI values to distances
d1 = rssi_to_distance(RSSI_A)
d2 = rssi_to_distance(RSSI_B)
d3 = rssi_to_distance(RSSI_C)

print(f"Distances (from RSSI): d1 = {d1:.2f}, d2 = {d2:.2f}, d3 = {d3:.2f}")

# Trilateration equations
x1, y1 = A
x2, y2 = B
x3, y3 = C

# Solving x and y based on the derived distances
x = (d1**2 - d2**2 + x2**2) / (2 * x2)
y1_solution = math.sqrt(d1**2 - x**2)
y2_solution = -y1_solution

# Solutions for point P
AP1 = (x, y1_solution)
AP2 = (x, y2_solution)

print(f"Possible locations of AP: {AP1} and {AP2}")
