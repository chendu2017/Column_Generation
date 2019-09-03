# Column_Generation

This file provides two comparable models in Integer Pragramming about the cutting stock problems

Before runnming the models, one should input demand for each kinds of stock length and the length of stocks, with a same length.
For example:
demand = [20,50,30]
L = [10,5,15]
Tha above input means, customers require 10cm (or m, whatever) stocks with the amount 30, and 5cm with 50, 15cm with 30.

One is general Integer Programming with decision variable Y_{i} and X_{ij}. Y_{i}, \in {0,1}, means whether i-th stock should be used. X_{ij} means how many parts should i-th stock be cut in j-th style for customers.

The another model is based on column generation. Each column means one way to cut the stock. Of course at the very beginning, we don't exactly know all cutting ways. But with known cutting ways, we can easily get a feasible solution if we cut stocks only in these way. Then, with the feasible solution, a subproblem is defined to find another cutting way to lower the number of used stocks. Iteratively, more cutting styles will be found until we get an optimal solution.

Running two models respectively will give an evident comparison in terms of running time. When there are 20 demand styles, models with column generation can be solved immediately while the general model takes about 20 second to obtain the optimal solution.
