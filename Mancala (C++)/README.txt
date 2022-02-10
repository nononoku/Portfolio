Title: Mancala
Programmed by Noah Kuperberg in 2019

Description: C++ implementation of the popular board game Mancala.

Usage (in a terminal):
	make mancala
	./mancala


Each inner number represents the number of stones in that pit. Each upper
number represents how many stones are in that player's goal. Enter a number
to pick up the stones on your side and drop them one-by-one into the pits.
The player with more stones in their goal at the end wins. Ending by dropping
a stone in an empty pit on your side, captures your opponent's stones opposite
that pit. Ending in your own goal gives you an extra turn.