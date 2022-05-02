# N-Queens-Knight-Variation
Comparing two approaches to solving the problem

## Simple visuals to illustrate the solution
![visuals](https://i.imgur.com/1CXlSG0.png)

## Comparing Depth-first search with a genetic algorithm
### Depth-first search
|Size(N)|Time(seconds)|Accuracy(%)|Trials|
|---|---|---|---|
|10|0.001|100|1|
|15|0.002|100|1|
|20|1|100|1|
|25|27|100|1|
|30|1981|100|1|
### Genetic algorithm
|Size(N)|Time(seconds)|Accuracy(%)|Trials|
|---|---|---|---|
|10|0.4|100|100|
|15|0.9|100|100|
|20|2.9|98|100|
|25|4.8|98|100|
|30|7.8|95|100|
|50|33.5|40|10|

## How to run
To install the dependencies with pip `pip install -r requirements.txt`

To run the program `python ./nqueensknightvariation {genetic,dfs} n` where n is the size of the board and either algorithm is chosen.

