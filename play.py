#!usr/bin/env python
"""
@author Arthur de Fluiter
@author Jur van den Berg
@author Peter Bloem
@version 3.14159

This program is meant to make running the bots a whole lot easier.

For all the options run
python play.py -h
or
python play.py --help
"""
from argparse import ArgumentParser
from subprocess import Popen, PIPE
import sys
import os.path
import multiprocessing
import functools

# these paths are crawled for programs by default, you can add paths here (more permanent)
# or run -e <path> as described in help
default_paths = ["src/python", "out/", "out/artifacts"]


def execution_path(program, paths):
    """
    Given a vague program description, tries to figure out what it's supposed 
    to point to and how to execute it.

    example input with expected output:
    "RandomBot.py"             -> "python src/RandomBot.py"
    "RandomBot.jar"            -> "java -jar out/artifacts/RandomBot.jar"
    "RandomBot.java"           -> "java -cp out/classes RandomBot" OR
                                  "java -cp out RandomBot"         (Depending on where it finds it)
    "java out/RandomBot"       -> "java out/RandomBot"
    "shadyCExecutable.exe"     -> Exception
    "java"                     -> Exception

    @type program : string
    @type paths: list[string]
    """
    command = program.strip().split()  # remove trailing whitespace and split into chunks

    # an argument like 'python src/RandomBot.jar'
    if len(command) > 1 and (command[0][:6] == "python" or command[0] == "java"):
        # assume the person knows what they're doing
        return program

    # I assume the last var will be the variable it is trying to execute
    file_name = command[-1]

    if file_name.endswith(".py"):
        exec_path = resolve_path(file_name, paths)
        return "{} {}".format(options.python_exec, exec_path)
    
    else:
        raise LookupError("Error: incomplete name? ({})".format(program))


def wizard():
    # check for python
    if sys.version_info[0] != 3:
        print("You're running python3, please use python2")
        exit(-1)

def resolve_path(file_name, paths, include_file=True):
    """Checks the currently selected paths for whether it can find the file"""
    for path in paths:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            if include_file:
                return file_path
            else:
                return path
    err_message = "Could not resolve '{}'\nLooked in paths: {}\n".format(file_name, paths)
    raise LookupError(err_message)


def in_path(program):
    """Checks whether a program, like java, is in path (automatically checks for program and program.exe)"""
    
    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path.strip('"'), program)
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return True
        exe_file = os.path.join(path.strip('"'), program + ".exe")
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return True
    return False


def play_game(id, command, options):
    engine_process = Popen(command, stdout=PIPE, stderr=PIPE)
    engine_out, engine_err = engine_process.communicate()  # blocks

    winner = 0
    output = ""

    if options.verbose:
        output += "For a full overview of the game state at all times, please check 'log.txt'\n"
        output += "Errors/Messages picked up by engine\n"
        output += "----------------------------\n"
        output += engine_err
        output += "\n"
    else:
        # find out who won and display
        import re
        output += ("Game[%d]: " % id)
        m = re.findall("(Draw!\s*$|Player \d Wins!\s*$)", engine_err)
        if len(m) is 0:
            output += "Something went wrong, engine output dump: \n"
            output += "-------------------------\n"
            output += engine_err
            output += "\n"
            sys.stdout.write(output)
            sys.stdout.flush()
            exit()
        else:
            output += m[0]
            m2 = re.findall("Player (\d) Wins!\s*$", m[0])
            if m2:
                winner = 1 if m2[0] == '1' else -1

    # visualiser
    if options.show:
        visualizer = [options.python_exec, "tools/visualizer/visualize.py"]
        visualizer_process = Popen(visualizer, stdin=PIPE)
        visualizer_process.communicate(input=engine_out)

    if options.output:
        output += engine_out
        output += "\n"

    sys.stdout.write(output)
    sys.stdout.flush()
    return winner

if __name__ == "__main__":
    parser = ArgumentParser()

    # map option (relative paths)
    parser.add_argument("-m", "--map", dest="map",
                        help="the map to play on",
                        default="simplemaps/3planets/map1.txt")

    # player 1 & 2, I want only the bare minimum to be mentioned here (EmptyBot.py for instance)
    parser.add_argument("-1", "--p1", "--player1", dest="player1",
                        help="the program to run for player 1 (default: RandomBot.py)",
                        default="RandomBot.py")
    parser.add_argument("-2", "--p2", "--player2", dest="player2",
                        help="the program to run for player 2 (default: RandomBot.py)",
                        default="RandomBot.py")

    # parallel mode (see the playgame engine)
    parser.add_argument("-p", "--parrallel", dest="parallel",
                        help="different game mode  (default: serial)",
                        action="store_true")

    parser.add_argument("-t", "--max-time", dest="max_time",
                        help="maximum amount of time allowed per turn in msec (default: 1000)",
                        type=int, default=1000)

    parser.add_argument("-x", "--max-turns", dest="max_turns",
                        help="maximum amount of turns in a game  (default: 100)",
                        type=int, default=100)

    # Visualisation (with the visualisation tools, if this is easier, we could put the code right here)
    parser.add_argument("-s", "--show", dest="show",
                        help="whether the game should be visualised (default: False)",
                        action="store_true")

    parser.add_argument("-o", "--output", dest="output",
                        help="whether the information required for visualization should be printed (default:False)",
                        action="store_true")

    parser.add_argument("-v", "--verbose", dest="verbose",
                        help="whether to output extra logging information  (default: False)",
                        action="store_true")

    parser.add_argument("-e", "--exec-path", dest="exec_path",
                        help="This resolves the path to the executable, if you place the executable in a different place, "
                             "add the string to this list (default included: 'src/python', 'out/', 'out/artifacts')",
                        action="append", default=[])

    parser.add_argument("-y", "--python", dest="python_exec",
                        help="This defines the python executable used. Should you get issues with python3/python2 "
                        "mismatches, it might be a good idea to set this to 'python2'. (default: 'python')",
                        default="python")

    parser.add_argument("-r", "--rounds", dest="rounds",
                        help="This amounts to the amount of games played. If this is greater than one, it will "
                        "automatically disable the -s and -o flags, and affect the function of -v (default: 1)",
                        type=int, default=1)

    parser.add_argument("-w", "--workers", dest="workers",
                        help="The amount of workers available to run games. Do NOT think making this number be bigger "
                        "makes it run x times faster. The runner will spawn w subprocesses, but the game will spawn 2 "
                        "subprocesses for each instance as well. Has no effect if -r is not set (default: 4)",
                        type=int, default=4)

    options = parser.parse_args()
    wizard()

    game_maps = options.map.split(',')
    mode = 'parallel' if options.parallel else 'serial'
    max_turns = str(options.max_turns)
    max_turn_time = str(options.max_time)

    player1, player2 = "", ""
    paths = options.exec_path + default_paths

    rounds = options.rounds

    if rounds > 1:
        options.verbose = False
        #options.output = False
        options.show = False

    try:
        player1 = execution_path(options.player1, paths)
        player2 = execution_path(options.player2, paths)
    except LookupError as inst:
        print("Error: %s" % inst)
        exit(-1)

    if options.verbose:
        print("Play.py configurations")
        print("---------------------")
        print("Map location(s): \"%s\"" % game_maps)
        print("Player 1: '%s'" % player1)
        print("Player 2: '%s'" % player2)
        print("Game mode: '%s'" % mode)
        print("Maximum amount of turns: %s" % max_turns)
        print("Time per turn: %s" % max_turn_time)
        print("Visualization: %s" % str(options.show))
        print("Python executable: %s" % str(options.python_exec))
        print("Rounds: %s" % str(rounds))
        print("---------------------\n")

    if rounds == 1 and len(game_maps) == 1:
        command = ['java', '-jar', 'tools/PlayGame.jar', game_maps[0], player1, player2, mode, max_turns, max_turn_time]
        play_game(1, command, options)
    else:
        pool = multiprocessing.Pool(options.workers)
        scores = [0, 0, 0]

        game_count = 1
        for game_map in game_maps:
            if not os.path.isfile(game_map):
                continue

            command = ['java', '-jar', 'tools/PlayGame.jar', game_map, player1, player2, mode, max_turns, max_turn_time]
            partial_play = functools.partial(play_game, options=options, command=command)
            it = pool.imap_unordered(partial_play, range(game_count, game_count + rounds))
            game_count += rounds

            for result in it:
                scores[cmp(result, 0)] += 1

        pool.close()
        pool.join()

        print("\nFINAL TALLY:")
        print("Draws   : %d" % scores[0])
        print("Player 1: %d" % scores[1])
        print("Player 2: %d" % scores[2])
        print("")
        print(["Draw!", "Player 1 Wins!", "Player 2 Wins!"][cmp(scores[1], scores[2])])
