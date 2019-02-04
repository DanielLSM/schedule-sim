## Conditioned-based real-time scheduling simulator

Currently, most (if not all) scheduling tasks are approached by formulating the task in a mixed integer programming form. The latter formulation results in (conceputally) a graph, which is searched by open/closed source non-commercial/commercial solvers. 

The present simulator corresponds to an alternative formulation of the scheduling problem. Thus, the scheduling problem is re-formulated as a markov decision process. Markov decision processes are useful for studying optimization problems solved via dynamic programming and reinforcement learning. The final goal of this effort is to apply the former tecnhiques to this simulator and observe wether the hypothesis is confirmed.

The high-level formulation is, as follows:

State space - $S : N \times M$, where $N$ corresponds to the number of objects to schedule and $M$ their current state/score.

Action space - $A_s: K$ where $K$ is a finite set of actions available from state $S_t$. Each action corresponds to assigning a certain task.

Transition function: $P_a(s_t, s_{t+1}) = Pr(s_{t+1} | s_t, a_t = a)$ in the case of this simulation, the actions are deterministic

Reward function: $R_a(s_t, s_{t+1}) = R(s_{t+1} | s_t, a_t = a)$