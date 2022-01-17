# PID: motion control of a particle #

In particle_trajectory.py a one-dimensional particle is asked to to follow a trajectory that changes over time.
The target trajectory is given by sharp step function. It is assumed that the particle position cannot be directly controlled, but rather the PID controller
outputs a force that is being applied to the particle. Over time these forces are then integrated to velocities and particle position.

The image below illustrates the effects of different PID parameters on the particle's trajectory.
Blue is the target trajectory, green shows a P-controller, red a PD-controller and a trajectory of an auto-tuned particle is shown in mint.
