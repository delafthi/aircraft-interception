# A jet intercepting another aircraft

This repository contains animations and mathematical foundations on how a jet
can intercept another aircraft. We assume that the jet intercepting the other
aircraft is a military aircraft with a **high maximal velocity**. The
intercepted aircraft is assumed to be a liner with **lower velocity**.
Additionally, the current velocity, the position as well as the direction of the
velocity vector are known at any time. For simplicity, we will call the
intercepting jet $H$ (for hunter) and the intercepted jet $L$ (for Liner). We
define the position, the velocity, and the velocity vector of the aircraft as
$P_X$, $v_X$, and $\vec{v}_X$, respectively. $X$ is the corresponding letter for
the aircraft (e.g. $P_H$ is the position of the hunter). Note, $v_X =
||\vec{v}_X||$. Additionally, we assume that the hunter can change its velocity
vector without any constraints, such as limiting G forces.

## Trivial interception approach

The simplest solution is the trivial approach, where $I$ will fly directly
towards the current position of $L$. Thus, we calculate the velocity vector of
$\vec{v}_I$, which is defined as

```math
\vec{v}_H = \frac{\overrightarrow{P_H P_L}}{||\overrightarrow{P_H P_L}||}
v_H
```

After some time we reevaluate the above expression with the updated values and
adjust $H$'s velocity vector. This approach is the slowest and wouldn't work if
$I$'s velocity is faster than $L$'s velocity. Accordingly, this is a stable but
slow solution to the problem.

### Example Animation

Adjustable parameters in the file `trivialInterception.py`:

- `pos_H`: starting position of the hunter
- `vel_H`: velocity of the hunter. Only the norm is relevant not the direction
- `pos_L`: starting position of the liner
- `vel_H`: starting velocity vector of the liner
- `t_step`: Size of the time steps
- `update_vel()` function: A function which updates the velocity vector of the
  liner over time. Currently, randomly rotate the vector between [-pi/4, pi/4]

```bash
manim -pqh trivialInterception.py trivialInterception
```

## Interception approach based on the interception point estimation

The travelled distance of a vehicle with constant velocity is calculated by

```math
x = v t
```

Thus, the velocity is directly proportional to the travelled distance. In
mathematic notation:

```math
\frac{x_1}{x_2} = \frac{v_1 \not{t}}{v_2 \not{t}}
```

In a first step we assume that $L$ has a constant velocity vector. Thus, $L$ is
flying straight ahead with constant speed. In this case as stated above, the
traveled distance is proportional to the speed

```math
\frac{||\overrightarrow{P_L P_I}||}{||\overrightarrow{P_H P_I}||} =
\frac{v_L}{v_H}
```

Let's define the $||\overrightarrow{P_L P_I}||$ and
$||\overrightarrow{P_H P_I}||$ in dependence of $t$

```math
\begin{array}{ccl}
||\overrightarrow{P_L P_I}|| & = & ||\vec{v}_L t|| \\
||\overrightarrow{P_H P_I}|| & = & ||\vec{v}_L t + \overrightarrow{P_H P_L}||
\end{array}
```

Inserting the above equations into the previous equation we can build a
binomial.

```math
\begin{array}{ccl}
\frac{v_L}{v_H} & = & \frac{||\vec{v}_L t||}{||\vec{v}_L t + \overrightarrow{P_H
P_L}||} \\
\frac{v_L^2}{v_H^2} & = & \frac{u_L^2 t^2 + w_L^2 t^2}{(u_L t + x_L - x_H)^2 +
(w_L t + y_L - y_H)^2} \\
\frac{v_L^2}{v_H^2} & = & \frac{u_L^2 t^2 + w_L^2 t^2}{u_L^2 t^2 + 2 u_L x_L t -
2 u_L x_H t + x_L^2 - 2 x_L x_H + x_H^2 + w_L^2 t^2 + 2 w_L y_L t - 2 w_L y_H t
+ y_L^2 - 2 y_L y_H + y_H^2} \\
\frac{v_L^2}{v_H^2} & = & \frac{(u_L^2 + w_L^2) t^2}{(u_L^2 + w_L^2) t^2 + (2
u_L x_L - 2 u_L x_H + 2 w_L y_L - 2 w_L y_H) t + x_L^2 - 2 x_L x_H + x_H^2 +
y_L^2 - 2 y_L y_H + y_H^2} \\
v_H^2(u_L^2 + w_L^2) t^2 & = & v_L^2 ((u_L^2 + w_L^2) t^2 \\
& & + (2 u_L x_L - 2 u_L x_H + 2 w_L y_L - 2 w_L y_H) t \\
& & + x_L^2 - 2 x_L x_H + x_H^2 + y_L^2 - 2 y_L y_H + y_H^2) \\
v_H^2 \not{v_L^2} t^2 & = & \not{v_L^2} (v_L^2 t^2 \\
& & + (2 u_L x_L - 2 u_L x_H + 2 w_L y_L - 2 w_L y_H) t \\
& & + x_L^2 - 2 x_L x_H + x_H^2 + y_L^2 - 2 y_L y_H + y_H^2) \\
0 & = & (v_H^2 - v_L^2) t^2 \\
& & + (2 u_L x_H - 2 u_L x_L + 2 w_L y_H - 2 w_L y_L) t \\
& & - x_L^2 2 x_L x_H - x_H^2 - y_L^2 + 2 y_L y_H - y_H^2
\end{array}
```

We can solve the binomial using the quadratic function.

```math
t_{1, 2} = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

where

```math
\begin{array}{ccl}
a & = & v_H^2 - v_L^2 \\
b & = & 2 u_L x_H - 2 u_L x_L + 2 w_L y_H - 2 w_L y_L \\
c & = & - x_L^2 + 2 x_L x_H - x_H^2 - y_L^2 + 2 y_L y_H - y_H^2
\end{array}
```

The quadratic function will give us two solutions. However, we only need the
positive one. Thus, $t = |t_{1, 2}|$.

Now, that we have an estimation of the interception point we can directly fly
towards it to intercept at the as soon as possible. However, we assumed that the
intercepted aircraft does not change direction nor speed. In the next section
we will see how we account for that.

## Interception with adaptive adjustments
