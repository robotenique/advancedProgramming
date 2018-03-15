Challenges
==
**Author**: Juliano Garcia de Oliveira
- Challenge 01: exploring branch prediction
	The program shows the difference betweeen two executions of the same code, but one uses the [Branch Predictor ](https://en.wikipedia.org/wiki/Branch_predictor) to increase its performance, while the other don't.

	The idea is, given an array with length N, with integer numbers from 1 to N, read the entire array and counts how many of the elements are bigger than N/2, and less or equal than N/2. Of course, considering that N is even, the program enter exactly N/2 times in each condition.

	To show the difference, we first do the test with an ordered array, and then an unordered array, but with the same elements, so the total times that the program enters each condition is always the same (N/2, as stated above). The difference is mainly because the branch predictor can optimize the first case, because the first N/2-the numbers of the array will never be bigger than N/2, and it'll choose the second branch (the *else*).  WIth an unordered array, there isn't a pattern to be followed, so the branch predictor will miss 50% of the time, thus making it much less efficient than the first one.
	*OBS: the array is randomized using the [Fisher-Yates Shuffle](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)*

![A railroad with a branch](https://upload.wikimedia.org/wikipedia/commons/c/cf/Entroncamento_do_Transpraia.JPG)
