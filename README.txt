Hello! Welcome to AI Snake Game!
This demo utilizes the A* pathfinding algorithm to play a game of Snake!

--------------------------------------------------------------------------------------------------------------------------------------------------------

To play a regular game of Snake, navigate to this directory in your command prompt or equivalent environment and type "python snake.py"
In this regular game, you can control the snake with the arrow keys. Collect the fruit to grow!
If you crash into the borders or your own body, it's Game Over! Press Q to exit the game and return to the command prompt.
I did not implement command-line argument parsing, but you can manually change the arena size by changing the row and column variables from lines 13-17
You can also change the speed of the snake by increasing the clock tickrate, on line 43. Increasing this increases the speed.

--------------------------------------------------------------------------------------------------------------------------------------------------------

Alternatively, if you're not in the mood to play for yourself, you're in luck! Type "python astarsnake.py" instead to have AI play it for you!
This algorithm has changed a bit from the example code that was demonstrated in my presentation to improve its efficiency and problem-solving skills.
First, the algorithm now only acts on a single move calculated by the A* pathfinder, and tosses the rest to start over.

By doing this, we can make a new path on every single move, meaning that we can optimize our path on the fly as our tail recedes out of our way.
During execution, you can see that the snake is now much more aggressive in its moves toward the food than before.
During my demonstration, you saw the snake move in ways that seemed to place itself farther away from the food, for seemingly no reason.
This was because it had calculated the entire path with the tail in the way, and then performed the entire thing. The new way is much more efficient.
NOTE: Because of this change, the algorithm will ALWAYS be busy making calculations. As a result, it may seize up if its tab loses focus.
      To avoid freezing the algorithm, don't tab out while it is executing (or else you will need to force-close it)

In addition to increasing efficiency, I have also made the algorithm capable of (not very intelligent) problem-solving.
The code itself includes comments as to my decision process, but originally I had made it so that if there is trapped food, a new path would be made:
	- The new path was defined with the tail being the new food and the snake subtract this piece.
	- This would recursively repeat until a non-trapped tail piece was found, and then travel toward there (since it's to be removed soon)
	- Unfortunately, subtracting from the snake did not bode well, because the head would then occasionally pass through the 'real' snake
Improving on this, I added a new parameter to count the number of hops:
	- An "attempts" variable was used to count incompatible tail pieces
	- This now acted in the exact same manner as the previous iteration, but without making the 'real' and 'temp' snakes inconsistent
	- Unfortunately, this still did not work well because it would frequently just trap itself even further in the rest of the body
Finally, I tried a different approach altogether:
	- If the food is trapped, completely ignore it for this 'turn'
	- Calculate a random new location to travel to from the available open positions
	- Travel toward there instead
	- By wasting turns like this, we can slowly uncoil the tail of the snake without needing to chase it
	- This is not perfect, because it's statistically impossible for a million billion (hyperbole) random choices to play a perfect game
	- It is very good, though! We reach the recursion limits for Python long before we run out of random places to visit! (see below)

I consider this a success! My algorithm outlives Python's internal limitations!
I'm satisfied with these solutions, and I hope that in watching the algorithm in action you can come to a similar conclusion!
There is additional documentation within the program explaining what everything included is for and the purpose they serve.
NOTE: If it's taking too long for your liking, you can change the speed of this one as well, the clock tick is on line 137.

--------------------------------------------------------------------------------------------------------------------------------------------------------

Outstanding Success Error!:
File "D:\CS\snake\astarsnake.py", line 48, in getAction
    dummyfood = grid[randint(0, rows - 1)][randint(0, cols - 1)]
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.9_3.9.1264.0_x64__qbz5n2kfra8p0\lib\random.py", line 339, in randint
    return self.randrange(a, b+1)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.9_3.9.1264.0_x64__qbz5n2kfra8p0\lib\random.py", line 315, in randrange
    return istart + self._randbelow(width)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.9_3.9.1264.0_x64__qbz5n2kfra8p0\lib\random.py", line 244, in _randbelow_with_getrandbits
    k = n.bit_length()  # don't use (n-1) here because n can be 1
RecursionError: maximum recursion depth exceeded while calling a Python object