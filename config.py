# config.py

# Physical Constants
AIR_DENSITY = 1.22007  # kg/m³ (Air density at sea level)
GRAVITY = 9.81  # m/s² (Acceleration due to gravity)
C_DRAG = 0.4  # Drag coefficient for a light van (default)

# Mode booleans
debug_mode = False
formula_mode = True

# Saved in profile
mass = None
vehicle_height = None
vehicle_width = None
wheel_radius = None

top_speed = None
time_to_100 = None
gradeability_percent = None

# Coefficients
km = None
C0 = None
C1 = None
