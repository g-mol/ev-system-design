# config.py

# Physical Constants
AIR_DENSITY = 1.22007  # kg/m³ (Air density at sea level)
GRAVITY = 9.81  # m/s² (Acceleration due to gravity)
C_DRAG = 0.4  # Drag coefficient for a light van (default)

# User Inputs
mass = None
top_speed = None
time_to_100 = None
km = None
current_road_angle = None
vehicle_height = None
vehicle_width = None
headwind_speed = None
wheel_radius = None
gradeability_percent = None
C0 = None
C1 = None

# Calculated Values
top_speed_mps = None
headwind_speed_mps = None
relative_speed = None
road_angle_rad = None
frontal_area = None
acceleration = None

# Forces and Power
rolling_force = None
gravitational_force = None
drag_force = None
road_load_force = None
traction_force = None
power_required = None
required_tractive_force_near_zero = None

# Constants K1 and K2
k1 = None
k2 = None

# Terminal Velocity and Time to Reach
terminal_velocity = None
time_to_vt = None
