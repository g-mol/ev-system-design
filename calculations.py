import math
import numpy as np
from config import AIR_DENSITY, GRAVITY, C_DRAG


def calculate_rolling_resistance_force(mass, angle_rad, speed_mps=0, C0=None, C1=None):
    return math.copysign(mass * GRAVITY * math.cos(angle_rad) * (C0 + C1 * speed_mps ** 2), speed_mps)


def calculate_gravitational_force(mass, angle_rad):
    return mass * GRAVITY * math.sin(angle_rad)


def calculate_aerodynamic_drag_force(relative_speed, frontal_area):
    return math.copysign(0.5 * AIR_DENSITY * C_DRAG * frontal_area * relative_speed ** 2, relative_speed)


def calculate_road_load_force(rolling_force, gravitational_force, drag_force):
    return rolling_force + gravitational_force + drag_force


def calculate_traction_force(road_load_force, mass, acceleration, km):
    return road_load_force + km * mass * acceleration


def calculate_power_required(traction_force, vehicle_speed):
    return traction_force * vehicle_speed


def calculate_angular_velocity(vehicle_speed, wheel_radius):
    return vehicle_speed / wheel_radius


def calculate_torque_required(power_required, angular_velocity):
    return power_required / angular_velocity


def calculate_required_tractive_force_near_zero(mass, gradeability_percent):
    gradeability_rad = math.atan(gradeability_percent / 100)
    return (mass * GRAVITY * math.tan(gradeability_rad)) / math.sqrt(1 + math.tan(gradeability_rad) ** 2)


def calculate_k1(tractive_force, mass, gravity, C0):
    return (tractive_force / mass) - (gravity * C0)


def calculate_k2(air_density, drag_coefficient, frontal_area, mass, gravity, C1):
    return ((air_density * drag_coefficient * frontal_area) / (2 * mass)) + (gravity * C1)


def calculate_velocity_profile(k1, k2, time_array):
    velocity = np.sqrt(k1 / k2) * np.tanh(np.sqrt(k1 * k2) * time_array)
    return velocity


def calculate_terminal_velocity(k1, k2):
    return np.sqrt(k1 / k2)


def calculate_time_to_terminal_velocity(k1, k2, terminal_velocity):
    # Calculate the time to reach 98% of the terminal velocity
    time_vt = 2.3 / np.sqrt(k1 * k2)
    return time_vt


def calculate_distance_traversed(k2, terminal_velocity, time_array):
    k2_vt_t = k2 * terminal_velocity * time_array
    distance = (1 / k2) * np.log(np.cosh(k2_vt_t))
    return distance


def calculate_instantaneous_power(f_tr, terminal_velocity, k2, time_array):
    return f_tr * terminal_velocity * np.tanh(k2 * terminal_velocity * time_array)


def calculate_terminal_power(f_tr, terminal_velocity):
    return f_tr * terminal_velocity


def calculate_peak_power(f_tr, terminal_velocity, k1, k2, tf):
    sqrt_k1_k2 = np.sqrt(k1 * k2)
    pt = f_tr * terminal_velocity
    return pt * np.tanh(sqrt_k1_k2 * tf)


def calculate_mean_power(f_tr, terminal_velocity, k1, k2, tf):
    sqrt_k1_k2 = np.sqrt(k1 * k2)
    pt = f_tr * terminal_velocity
    ln_cosh = np.log(np.cosh(sqrt_k1_k2 * tf))
    return (pt / (tf * sqrt_k1_k2)) * ln_cosh
