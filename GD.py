import rps.robotarium as robotarium
import rps.utilities.graph as graph
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.misc import *
from rps.utilities.controllers import *
from setpos import setpos

import numpy as np
import time
import gd_utils
import sys

init_pt = np.array([[-1.0], [1.0], [0]])

def f(x):
    return x[0]**2 + x[1]**2

def df(x):
    return np.array([[2 * x[0,0]], [2 * x[1,0]], [0]])

#one iteration of gradient descent
def iterate(x, eta, df):
    return 0 -  eta * df(x)

# Instantiate Robotarium object
N = 1
r = robotarium.Robotarium(number_of_agents=N, show_figure=True, save_data=True, update_time=0.1)


# Create barrier certificates to avoid collision
si_barrier_cert = create_single_integrator_barrier_certificate(N)

# define x initially
x = r.get_poses()
r.step()

gd_utils.draw_f(r, f)
max_iters = 20
goal_point = init_pt
eta = 0.1

setpos(r, x, goal_point, si_barrier_cert, N)
input()
goal_point = np.array([[0.0], [0.0], [0.0]])
vel = iterate(x, eta, df)
while(np.size(at_pose(x, np.array([[0.0], [0.0], [0.0]]), rotation_error=5)) != 1):

    # Get poses of agents
    x = r.get_poses()
    x_si = x[:2, :]

    # Create single-integrator control inputs
    #dxi = single_integrator_position_controller(x_si, goal_point[:2, :], magnitude_limit=0.08)
    dxi = vel[:2, :]

    # Create safe control inputs (i.e., no collisions)
    #dxi = si_barrier_cert(dxi, x_si)

    # Set the velocities by mapping the single-integrator inputs to unciycle inputs
    r.set_velocities(np.arange(N), single_integrator_to_unicycle2(dxi, x))
    # Iterate the simulation
    r.step()

    vel = iterate(x, eta, df)
    print(vel)
    time.sleep(0.01)
input()
# Always call this function at the end of your scripts!  It will accelerate the
# execution of your experiment
r.call_at_scripts_end()
