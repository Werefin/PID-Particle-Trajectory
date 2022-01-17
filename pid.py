import numpy as np


# Implementation of a PID controller
# Set the coefficients of the three terms to certain values and call PID.update with constant time steps

class PID(object):

    def __init__(self, kp=0.5, ki=0.0, kd=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.first = True

    # Update the PID controller
    # Computes the new control signal as: u(t) = kp*err(t) + ki*I(e) + kd*d/dt(err(t)),
    # where I(e) is the integral of the error up to the current time point
    # Args:
    #  error: Error between set point and measured value;
    #  dt: Time step delta
    # Returns:
    #  Returns the control signal u(t)

    def update(self, error, dt):
        if self.first:
            self.last_error = np.copy(error)
            self.sum_error = np.zeros(error.shape)
            self.first = False

        derr = (error - self.last_error) / dt

        self.sum_error += error * dt
        self.last_error[:] = error

        u = self.kp * error + self.ki * self.sum_error + self.kd * derr

        return u
