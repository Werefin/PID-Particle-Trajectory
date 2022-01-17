import numpy as np


# A particle in n-dimensions driven by forces

class Particle(object):

    def __init__(self, x0=[0, 0], v0=[0, 0], inv_mass=1.):
        self.x = np.asarray(x0, dtype=float)
        self.prev_x = np.asarray(self.x - np.asarray(v0), dtype=float)
        self.inv_mass = inv_mass
        self.f_sum = np.zeros(self.x.shape)

    def add_force(self, f):
        self.f_sum += f

    @property
    def v(self):
        return self.x - self.prev_x

    @property
    def mass(self):
        return 1.0 / self.inv_mass

    def update(self, dt):
        a = self.f_sum * self.inv_mass  # acceleration

        # Update particle position
        temp = np.copy(self.x)
        self.x += (self.x - self.prev_x) + a * dt * dt
        self.prev_x[:] = temp

        # Clear force accumulator
        self.f_sum[:] = 0.
