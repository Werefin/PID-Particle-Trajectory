import matplotlib.pyplot as plt
import numpy as np
import control as ctrl


# Models a dynamic system in which a particle driven by forces follows a desired trajectory

class MoveParticleProcess(ctrl.Process):

    def __init__(self, particle=ctrl.Particle(), pid=ctrl.PID()):
        super(MoveParticleProcess, self).__init__()
        self.particle = particle
        self.pid = pid

    # Return set-point position for particle to reach
    # Simple step function from t = 5 to t = 15

    def set_point(self, t):
        if t < 5. or t >= 15.:
            return np.asarray([0.])
        else:
            return np.array([1.])

    # Sense particle position

    def sense(self, t):
        return self.particle.x

    # Compute correction based on error

    def correct(self, error, dt):
        return self.pid.update(error, dt)

    # Update particle position; takes the correction value 'u' and interprets it as force acting on the particle,
    # then updates the motion equations by 'dt'

    def actuate(self, u, dt):
        self.particle.add_force(u)
        # self.particle.add_force(np.array([-0.5 * self.particle.mass]))  # External force actuates on process
        self.particle.update(dt)


def runner(pid_params):
    process = MoveParticleProcess(particle=ctrl.Particle(x0=[0], v0=[0], inv_mass=1.), pid=ctrl.PID(**pid_params))
    result = process.loop(t_sim=100, dt=0.1)
    e = np.sum(np.square(result['e']))  # ISE: Integral Square Error
    return e


def run():
    # Various PID controller parameters to run simulation with
    pid_params = [
        dict(kp=0.1, ki=0., kd=0.),
        dict(kp=1.5, ki=0., kd=0.5),
    ]

    # Additionally tune PID parameters
    params = ctrl.tune_twiddle(params=dict(kp=0., ki=0., kd=0.), cost_function=runner, threshold=0.001)
    pid_params.append(params)

    # Run simulation for each set of PID parameters
    simulation_results = []
    for idx, c in enumerate(pid_params):
        process = MoveParticleProcess(particle=ctrl.Particle(x0=[0], v0=[0], inv_mass=1.), pid=ctrl.PID(**c))
        result = process.loop(t_sim=100, dt=0.1)

        if idx == 0:
            fh, = plt.step(result['t'], result['y'], label='set-point')
            simulation_results.append(fh)

        xh, = plt.plot(result['t'], result['x'],
                       label='PID: $k_P = {:.2f}$; $k_I = {:.2f}$; $k_D = {:.2f}$'.format(c['kp'], c['ki'], c['kd']))
        simulation_results.append(xh)

    plt.title('Particle trajectory')
    plt.legend(handles=simulation_results, loc="upper right")
    plt.tight_layout()
    plt.xlabel('Time [s]')
    plt.ylabel('Position [m]')
    plt.show()
    plt.close()


if __name__ == "__main__":
    run()
