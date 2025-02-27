import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

# Define the system parameters (example values)
m1 = 1.0  # mass of the first object (kg)
m2 = 2.0  # mass of the second object (kg)
L1 = 2.0  # length of the first rod (m)
L2 = 1.0  # length of the second rod (m)
g = 9.81  # gravitational acceleration (m/s^2)

# Initial conditions (example values)
theta1 = np.pi / 4  # initial angle of the first rod (radians)
theta2 = np.pi / 6  # initial angle of the second rod (radians)
omega1 = 0.0  # initial angular velocity of the first rod (rad/s)
omega2 = 0.0  # initial angular velocity of the second rod (rad/s)

# Time parameters
t_max = 10.0  # total time (s)
dt = 0.01  # time step (s)
t = np.arange(0, t_max, dt)  # time array

# Equations of motion
def equations_of_motion(theta1, theta2, omega1, omega2, t):
    alpha1 = -g / L1 * np.sin(theta1)
    alpha2 = -g / L2 * np.sin(theta2)
    return alpha1, alpha2

# Integrate the equations of motion using Euler's method
theta1_array = np.zeros_like(t)
theta2_array = np.zeros_like(t)
omega1_array = np.zeros_like(t)
omega2_array = np.zeros_like(t)

theta1_array[0] = theta1
theta2_array[0] = theta2
omega1_array[0] = omega1
omega2_array[0] = omega2
    
for i in range(1, len(t)):
    alpha1, alpha2 = equations_of_motion(theta1_array[i - 1], theta2_array[i - 1], omega1_array[i - 1], omega2_array[i - 1], t[i - 1])
    omega1_array[i] = omega1_array[i - 1] + alpha1 * dt
    omega2_array[i] = omega2_array[i - 1] + alpha2 * dt
    theta1_array[i] = theta1_array[i - 1] + omega1_array[i - 1] * dt
    theta2_array[i] = theta2_array[i - 1] + omega2_array[i - 1] * dt             

# Plot displacement, velocity, and acceleration
sns.set(style="whitegrid")
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

axs[0].plot(t, theta1_array, label='Theta1', color=sns.color_palette()[0], linestyle='-', linewidth=2)
axs[0].plot(t, theta2_array, label='Theta2', color=sns.color_palette()[1], linestyle='--', linewidth=2)
axs[0].set_title('Displacement vs Time', fontsize=14)
axs[0].set_ylabel('Displacement (rad)', fontsize=12)
axs[0].legend()
axs[0].grid(True)

axs[1].plot(t, omega1_array, label='Omega1', color=sns.color_palette()[0], linestyle='-', linewidth=2)
axs[1].plot(t, omega2_array, label='Omega2', color=sns.color_palette()[1], linestyle='--', linewidth=2)
axs[1].set_title('Velocity vs Time', fontsize=14)
axs[1].set_ylabel('Velocity (rad/s)', fontsize=12)
axs[1].legend()
axs[1].grid(True)

alpha1_array = np.gradient(omega1_array, dt)
alpha2_array = np.gradient(omega2_array, dt)
axs[2].plot(t, alpha1_array, label='Alpha1', color=sns.color_palette()[0], linestyle='-', linewidth=2)
axs[2].plot(t, alpha2_array, label='Alpha2', color=sns.color_palette()[1], linestyle='--', linewidth=2)
axs[2].set_title('Acceleration vs Time', fontsize=14)
axs[2].set_ylabel('Acceleration (rad/s^2)', fontsize=12)
axs[2].legend()
axs[2].grid(True)

plt.xlabel('Time (s)', fontsize=12)
plt.tight_layout()
plt.savefig('displacement_velocity_acceleration.png')
plt.show()

# Animate the system
fig, ax = plt.subplots()

line1, = ax.plot([], [], 'b-', lw=2)
line2, = ax.plot([], [], 'r-', lw=2)

def init():
    ax.set_xlim(-L1 - L2, L1 + L2)
    ax.set_ylim(-L1 - L2, L1 + L2)
    ax.set_title('Double Pendulum Animation')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    return line1, line2

def update(frame):
    x1 = L1 * np.sin(theta1_array[frame])
    y1 = -L1 * np.cos(theta1_array[frame])
    x2 = x1 + L2 * np.sin(theta2_array[frame])
    y2 = y1 - L2 * np.cos(theta2_array[frame])

    line1.set_data([0, x1], [0, y1])
    line2.set_data([x1, x2], [y1, y2])
    return line1, line2

ani = FuncAnimation(fig, update, frames=range(len(t)), init_func=init, blit=True)
plt.show()

# Save the animation (optional)
ani.save('animation.mp4', writer='ffmpeg')

# Plot the free-body diagram
def plot_free_body_diagram():
    # Parameters
    theta = np.radians(75)  # Convert angle to radians
    L = 2  # Length of the arm in meters

    # Points
    O = [0, 0]
    A = [L * np.cos(theta), L * np.sin(theta)]
    B = [A[0], A[1]]

    # Forces (Assumed values for illustration)
    F_OA = 50  # Force applied by the arm OA in N
    F_B = 25  # Force applied by the slider in N

    # Directions
    dir_OA = [np.cos(theta), np.sin(theta)]
    dir_B = [0, -1]  # Assuming vertical force

    # Free-body diagram
    fig, ax = plt.subplots()
    ax.plot([O[0], A[0]], [O[1], A[1]], 'bo-', lw=2)  # Arm OA
    ax.plot([A[0]], [A[1]], 'ro')  # Point B

    # Plotting forces
    ax.quiver(O[0], O[1], F_OA * dir_OA[0], F_OA * dir_OA[1], angles='xy', scale_units='xy', scale=1, color='r',
              label='F_OA')
    ax.quiver(B[0], B[1], F_B * dir_B[0], F_B * dir_B[1], angles='xy', scale_units='xy', scale=1, color='b',
              label='F_B')

    # Annotations
    ax.annotate('O', xy=(O[0], O[1]), xytext=(-0.1, -0.1))
    ax.annotate('A', xy=(A[0], A[1]), xytext=(A[0] + 0.1, A[1] + 0.1))
    ax.annotate('B', xy=(B[0], B[1]), xytext=(B[0] + 0.1, B[1] - 0.1))
    ax.annotate('F_OA', xy=(F_OA * dir_OA[0] / 2, F_OA * dir_OA[1] / 2),
                xytext=(F_OA * dir_OA[0] / 2 + 0.1, F_OA * dir_OA[1] / 2 + 0.1), color='r')
    ax.annotate('F_B', xy=(B[0], B[1] - F_B / 2), xytext=(B[0] + 0.1, B[1] - F_B / 2 - 0.1), color='b')

    # Settings
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 3)
    ax.set_aspect('equal', 'box')
    ax.legend()
    ax.grid(True)

    plt.title('Free-Body Diagram of the System')
    plt.savefig('free_body_diagram.png')
    plt.show()

# Call the function to plot the free-body diagram
plot_free_body_diagram()

# Plot forces acting on the system
def plot_forces():
    # Calculate tensions and gravitational forces
    T1 = m1 * g * np.cos(theta1_array) + m1 * (L1 * omega1_array**2) * np.sin(theta1_array)
    T2 = m2 * g * np.cos(theta2_array) + m2 * (L2 * omega2_array**2) * np.sin(theta2_array)
    F1x = -m1 * g * np.sin(theta1_array)
    F1y = m1 * g * np.cos(theta1_array)
    F2x = -m2 * g * np.sin(theta2_array)
    F2y = m2 * g * np.cos(theta2_array)

    # Plotting tensions
    fig, axs = plt.subplots(2, figsize=(10, 8))

    axs[0].plot(t, T1, label='Tension in rod 1', color=sns.color_palette()[0], linestyle='-', linewidth=2)
    axs[0].plot(t, T2, label='Tension in rod 2', color=sns.color_palette()[1], linestyle='--', linewidth=2)
    axs[0].set_title('Tensions vs Time', fontsize=14)
    axs[0].set_ylabel('Tension (N)', fontsize=12)
    axs[0].legend()
    axs[0].grid(True)

    # Plotting gravitational forces
    axs[1].plot(t, F1x, label='F1x (Gravity) for rod 1', color=sns.color_palette()[0], linestyle='-', linewidth=2)
    axs[1].plot(t, F1y, label='F1y (Gravity) for rod 1', color=sns.color_palette()[1], linestyle='--', linewidth=2)
    axs[1].plot(t, F2x, label='F2x (Gravity) for rod 2', color=sns.color_palette()[2], linestyle='-', linewidth=2)
    axs[1].plot(t, F2y, label='F2y (Gravity) for rod 2', color=sns.color_palette()[3], linestyle='--', linewidth=2)
    axs[1].set_title('Gravitational Forces vs Time', fontsize=14)
    axs[1].set_ylabel('Force (N)', fontsize=12)
    axs[1].legend()
    axs[1].grid(True)

    plt.xlabel('Time (s)', fontsize=12)
    plt.tight_layout()
    plt.savefig('forces.png')
    plt.show()

# Call the function to plot forces
plot_forces()

# Plot phase space
def plot_phase_space():
    fig, axs = plt.subplots(2, figsize=(10, 8))

    axs[0].plot(theta1_array, omega1_array, label='Phase Space for Rod 1', color=sns.color_palette()[0], linestyle='-', linewidth=2)
    axs[0].set_title('Phase Space for Rod 1', fontsize=14)
    axs[0].set_xlabel('Theta1 (rad)')
    axs[0].set_ylabel('Omega1 (rad/s)')
    axs[0].grid(True)

    axs[1].plot(theta2_array, omega2_array, label='Phase Space for Rod 2', color=sns.color_palette()[1], linestyle='--', linewidth=2)
    axs[1].set_title('Phase Space for Rod 2', fontsize=14)
    axs[1].set_xlabel('Theta2 (rad)')
    axs[1].set_ylabel('Omega2 (rad/s)')
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig('phase_space.png')
    plt.show()

# Call the function to plot phase space
plot_phase_space()
