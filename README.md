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

