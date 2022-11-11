"""Calculate interception with the trivial interception approach."""
import manim
import random
import numpy as np

random.seed(123456789)


class trivialInterception(manim.Scene):
    """Trivial Interception scene."""

    t_step = 0.5  # Time step factor. The smaller the longer the animation

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
        # A maximal rotation of +/- 90 degrees
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
        LH = pos_L - pos_H
        while np.linalg.norm(LH) >= np.linalg.norm(vel_H) * self.t_step:
            # Calculate the traveled distance in t_step
            x_H = (LH / np.linalg.norm(LH)) * np.linalg.norm(vel_H) * \
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
            # Create the line between pos_H and pos_L
            line = manim.Line(pos_H, pos_L,
                              color=manim.WHITE).set_stroke(width=0.6)
            # Create an old hunter to keep track of previous positions
            old_hunter = manim.Dot(pos_H).set_color(manim.WHITE)

            # Create the animations
            self.play(manim.Create(line))
            self.add(line_H)
            self.add(old_hunter)
            self.bring_to_front(hunter)
            self.bring_to_front(liner_vel)
            self.play(manim.Create(rad_H))
            self.play(manim.MoveAlongPath(hunter, line_H),
                      manim.MoveAlongPath(liner, line_L),
                      manim.MoveAlongPath(liner_vel, line_L_arrow),
                      rate_func=manim.linear)
            self.remove(rad_H, line)

            # Update the positions
            pos_H = newPos_H
            pos_L = newPos_L

            # Update velocity vector
            vel_L = self.update_vel(vel_L)
            self.remove(liner_vel)
            liner_vel = manim.Arrow(start=pos_L,
                                    end=pos_L + vel_L * self.t_step,
                                    color=manim.YELLOW)
            self.add(liner_vel)

            # Update the vector pos_H -> pos_L
            LH = pos_L - pos_H
