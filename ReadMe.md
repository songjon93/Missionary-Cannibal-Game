# Missionary and Cannibal

### Introduction

Through cannibal and missionary game, we intend to explore the basics of artificial intelligence.
Because the following program goes through an uninformed search, it is significant that we understand that the program ought to explore every possible legal state for the current state at every stage to find out whether the desired end state can be reached.
And it aids our understanding to determine the type and number of variables used to describe the state and number of possible state at a given moment.

For instance, when there are 3 missionaries and 3 cannibals, the total number of states without considering their legalities would be 4 * 4 * 2, 32.
Individually, there are four possible states for the missionaries (0 ~ 4), four possible states for the cannibals (0 ~ 4), and two possible states for the boat (0 ~ 1).
And the aforementioned states for each variable are fused into one 3 dimensional-coordinates.
To aid our understanding, let's say that there is one cubicle, and let this cubicle represent a single state.
In this case, we initially have 4 cubicles.
And we have 4 more of the 4 cubicles, and now we have 16 cubicles.
And we have 2 more of the 16 cubicles, and now we have 32 cubicles.

![States Graph](./States.svg)

> The graph above shows all possible states
