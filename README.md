Redzone Ranking: Project Description

The aim of this project is creating a ranking system for Ultimate Frisbee practices, that will also be able to group players into two teams based on their ranking and number of times they played with their teammates.

Context:
Every week, a group of Ultimate Frisbee Players practice together. The group changes, some people come and go, but the core stays. Every practice, we do a "Redzone Game" - it means we are grouped into two teams and each team has three tries to score. So, the resulting score varies from 0-0 to 3-3 (with possible scores 3-1, 0-2, etc.).

Each week, we will write down the results in a csv file. The record for one practice will have one row. In each row, there will be the following columns: date, number of points scored by the first team, number of points scored by the second team, the diff for first-team players (i.e. first score minus second score), the diff for second-team players (the previous number times minus one), players in the first team (in a list []), players in the second team (again in a list). 

The ranking: each individual player will have his own ranking updated each week. The score is the difference of scores of every week, i.e., if the score is 3-2, all players from the first team will get +1, all players from the second team will recieve -1. If the score is 2-2, noones ranking will change. 

Division into groups: a linear program will be solved to divide the players into two groups. The linear program looks as follows: 

- for every player i, there is his associated ranking r_i (his overall score).
- for every player i, there is a variable x_i, which has values 0 or 1. If it is 1, player i is in team A, if it is zero, he is in team B
- for every player i, there is a variable y_i with value 1 - x_i, which thus has 1 if player i is in team B and 0 if in team A.
- for every two players i, j, there is a set number c_i,j holding the value of how many times players i and j played together. c_ij is the same as c_ji.
- number of players in team A denoted as N and computed beforehand as the lower ceiling of the number of players divided by two.

Constraints:
- The sum of x_i is N (thus the rest are in team B).
- We want to minimize the difference of the sum of player rankings of the two teams so they are as equal as possible.
- We also want to minimize the overall number of connections in both teams (times a weighting constant alpha).