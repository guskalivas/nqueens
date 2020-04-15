# nqueens
Hill Climbing Algorithm to Solve NQueens Problem. NQueens is the problem of placing N chess queens on an N×N chessboard so that no two queens attack each other, however, included is a twist to the problem: a boulder is placed on the board with x,y coordinates. 
The queens cannot move where the boulder is and the boulder can block queens attacks. 

Program uses hill climbing algorithm to find solve and find the states that minimize herusitic value (the number of queens that can currently attack eachother). 

As hill climbing can get stuck at local minimums, included is a random restart function to restart x times to find the global minimium, or solution, a state that 0 queens can attack eachother. 


![NQueens](https://user-images.githubusercontent.com/56047433/75491816-29c7d400-597c-11ea-8d7d-447a9a074c4a.png)


