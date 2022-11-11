"""Calculate interception with interception point estimation approach."""
import manim
import random
import numpy as np

random.seed(123456789)


def get_intersection(pos_H: np.ndarray, vel_H: np.ndarray, pos_L: np.ndarray,
                     vel_L: np.ndarray) -> np.ndarray:
    """
    Get the fastest intersection point for two flying objects.

    Args:
        pos_H: A numpy array containing the position of the hunter
        vel_H: A numpy array containing the velocity vector of the hunter. The
        direction has no influence on the result
        pos_L: A numpy array containing the position of the intercepted aircraft
        vel_L: A numpy array containing the velocity vector of the intercepted
        aircraft
    Returns: A numpy array containing the interception point of the two
    aircrafts.
    """
    a = np.linalg.norm(vel_H)**2 - np.linalg.norm(vel_L)**2
    b = 2 * vel_L[0] * pos_H[0] - 2 * vel_L[0] * pos_L[0] + \
        2 * vel_L[1] * pos_H[1] - 2 * vel_L[1] * pos_L[1]
    c = - pos_L[0]**2 + 2 * pos_L[0] * pos_H[0] - pos_H[0]**2 \
        - pos_L[1]**2 + 2 * pos_L[1] * pos_H[1] - pos_H[1]**2

    t = np.abs((-b + np.sqrt(b**2 - 4 * a * c)) / (2 * a))

    return pos_L + vel_L * t


class interceptionPointEstimation(manim.Scene):
    """Trivial Interception scene."""

    t_step = 0.5  # Time step factor. The smaller the longer the animation
    # The factor of how much the interception point estimation should
    # considired. k = 0 equals to the trivial approach. k = 1 we fly directly to
    # the estimated interception point.
    k = 0.5

    # Set positions and velocity vectors
    pos_H = np.array([-4, -2, 0])
    vel_H = np.array([1.5, 0, 0])
    pos_L = np.array([0, 0, 0])
    vel_L = np.array([0.3, 0.4, 0])

    def update_vel(self, vel: np.ndarray) -> np.ndarray:
        """
        Update the velocity vector.

        Generate random number which rotates the velocity vector. Currently, the
        actual position of the aircraft has no influence

        Args:
            vel: A numpy array containing the current velocity vector.
        Returns: A numpy array containing the updated velocity vector.
        """
        # A maximal rotation of +/- 45 degrees
        angle = random.uniform(-np.pi / 4, np.pi / 4)
        newVel = np.array([
            vel[0] * np.cos(angle) + vel[1] * np.sin(angle),
            (-vel[0]) * np.sin(angle) + vel[1] * np.cos(angle),
            0,
        ])
        return newVel

    def construct(self):
        """Construct the scene."""
        # Set positions and velocity vectors
        pos_H = self.pos_H
        vel_H = self.vel_H
        pos_L = self.pos_L
        vel_L = self.vel_L

        # Create the points for the aircrafts
        hunter = manim.Dot(pos_H).set_color(manim.RED)
        old_hunter = manim.Dot(pos_H).set_color(manim.WHITE)
        liner = manim.Dot(pos_L).set_color(manim.YELLOW)
        liner_vel = manim.Arrow(start=pos_L,
                                end=pos_L + vel_L * self.t_step,
                                color=manim.YELLOW)
        self.add(old_hunter)
        self.add(hunter)
        self.add(liner)
        self.add(liner_vel)

        # Create the vector pos_H -> pos_L
        pos_I = get_intersection(pos_H, vel_H, pos_L, vel_L)
        pos_Ii = pos_L + self.k * (pos_I - pos_L)
        HIi = pos_Ii - pos_H
        while np.linalg.norm(HIi) >= np.linalg.norm(vel_H) * self.t_step:
            # Calculate the traveled distance in t_step
            x_H = (HIi / np.linalg.norm(HIi)) * np.linalg.norm(vel_H) * \
                self.t_step
            x_L = vel_L * self.t_step
            # Calculate the future positions
            newPos_H = pos_H + x_H
            newPos_L = pos_L + x_L

            # Create the radius of where the hunter could go in t_step
            rad_H = manim.Circle(
                radius=np.linalg.norm(vel_H) * self.t_step,
                color=manim.WHITE).move_to(pos_H).set_stroke(width=0.6)
            # Create the line the hunter travels in t_step
            line_H = manim.Line(pos_H, newPos_H,
                                color=manim.WHITE).set_stroke(width=0.6)
            # Create the line the liner travels in t_step
            line_L = manim.Line(pos_L, newPos_L,
                                color=manim.WHITE).set_stroke(width=0.6)
            line_L_arrow = manim.Line(pos_L + vel_L * self.t_step / 2,
                                      newPos_L + vel_L * self.t_step / 2,
                                      color=manim.WHITE).set_stroke(width=0.6)
            # Create the line between pos_H and pos_I
            line_HI = manim.Line(pos_H, pos_I,
                                 color=manim.WHITE).set_stroke(width=0.6)
            # Create the line between pos_H and pos_I
            line_HIi = manim.Line(pos_H, pos_Ii,
                                  color=manim.WHITE).set_stroke(width=0.6)
            # Create the line between pos_L and pos_I
            line_LI = manim.Line(pos_L, pos_I,
                                 color=manim.WHITE).set_stroke(width=0.6)
            # Create an old hunter to keep track of previous positions
            old_hunter = manim.Dot(pos_H).set_color(manim.WHITE)

            # Create the animations
            self.play(manim.Create(line_HI), manim.Create(line_HIi),
                      manim.Create(line_LI))
            self.add(line_H)
            self.add(old_hunter)
            self.bring_to_front(hunter)
            self.bring_to_front(liner_vel)
            self.play(manim.Create(rad_H))
            self.play(manim.MoveAlongPath(hunter, line_H),
                      manim.MoveAlongPath(liner, line_L),
                      manim.MoveAlongPath(liner_vel, line_L_arrow),
                      rate_func=manim.linear)
            self.remove(rad_H, line_HI, line_HIi, line_LI)

            # Update the positions
            pos_H = newPos_H
            pos_L = newPos_L

            # Update velocity vector
            print(vel_L)
            vel_L = self.update_vel(vel_L)
            self.remove(liner_vel)
            liner_vel = manim.Arrow(start=pos_L,
                                    end=pos_L + vel_L * self.t_step,
                                    color=manim.YELLOW)
            self.add(liner_vel)

            # Update the vector pos_H -> pos_I
            pos_I = get_intersection(pos_H, vel_H, pos_L, vel_L)
            pos_Ii = pos_L + self.k * (pos_I - pos_L)
            HIi = pos_Ii - pos_H
