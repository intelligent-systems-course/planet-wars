Intelligent Systems 2017
========================
This is the practical material for the Intelligent Systems course, based on the
turn based strategy game _Planet Wars_.

## Getting started

To get to know the concept of the game, please visit 
[Galcon's website](http://www.galcon.com/flash). The challenge was inspired by this 
project and resembles it a lot. (Free downloads for android and iphone 
[here](http://www.galcon.com/g2/download.php)).

Your job is to make a bot that will play a turn-based version of this game. 
General rules about the project, including the rules of the game and the rules 
of the competition can be found on blackboard.

## Technical requirements

You require a working python3 environment and a good text editor or an IDE. If 
that's enough information, read on below. If you're not quite sure how to go
about this, see the installation tutorial on Blackboard. There will be a handson
session in the first week to help you get started. 
 
### Python knowledge

You will of course also need a working knowledge of python. If you're looking to 
brush up on your skills, there are many good tutorials available. For instance:
 * https://www.learnpython.org/
 * https://www.codecademy.com/ 
 
You do not need to be an expert in python to write a functioning bot. If you
already know another programming language, you should be able to get going within 
a day. You'll pick up the details as the project progresses. However, there are 
a few things that are important to understand. Check if you know what the 
following mean. If not, take some time to google them and read up:

#### Call-by-reference (and "call-by-value")

What happens if I pass a function a 'State' object, and the function changes the
object? Do I keep an unchanged state, or does my state change as well? 
 

## FAQ

### I found a bit that could be implemented much better/more efficiently.

Our main goal was to write code that was easy to read and to understand. To achieve
this, we've made many methods much less efficient than they need to be. This
is especially important for a project like this where many of the students are 
novice programmers. It is also a 
[good principle](https://en.wikipedia.org/wiki/Program_optimization#When_to_optimize) 
in general, at least when you write the first version of your code.

You may feel that your bot is to slow with our State and Fleet objects for 
instance if you're creating an evaluating lots of State objects in a deep
minimax tree. Luckily, you're not tied to our API: simply take the State object 
you're given and copy it to your own, more efficient, implementation. This may 
get you another plie or two in the search tree, so if you really want to win the 
competition it might be worth it.  

### I found a bug/improvement. Can I fork the project and send a pull request?

Sure! Just remember this is not a regular project: we've tried to minimize the 
amount of advanced python, and the number of dependencies. So, it might be that 
we're aware of the potential improvement, but we haven't used it just to keep the 
code simple for novice programmers.  

### The command-line scripts (play.py, tournament.py) make it difficult to do X

The command line scripts provide a convenient starting point, but if you want to do 
something more complex (like try a range of parameters for your bot), they are probably 
too limited. 

Your best bet is to write your own script that does what you want, and have it call the 
engine. Have a look at the function play(...) in  api/engine.py . You can write a 
script that sets up the bots in the way you need and calls that function.

## Changes from last year's challenge

The codebase has been rewritten entirely, so bots from last year won't work. To
reduce overhead, Java is no longer supported, only python.

The Python version has been upgraded to version 3. 

The game can now be played in two modes: full information and imperfect 
information. This is also the case in the [Galcon game](http://www.galcon.com/flash); 
later levels reduce the amount of information you see.

