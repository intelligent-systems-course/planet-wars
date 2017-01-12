import argparse
import multiprocessing
import multiprocessing.pool
import sys

import itertools
import random

from api import State, util, engine

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
colors = {
    'SUCCESS': GREEN,
    'INFO': BLUE,
    'WARN': YELLOW,
    'FAIL': RED
}

args = None

NOTIFY_AMOUNT = 5

def main():

    pool = multiprocessing.pool.ThreadPool(args.parallelism)

    bots = []
    for id, botname in enumerate(args.players):
        bots.append((id, util.load_player(botname)))

    wins = [0] * len(bots)

    games = list(itertools.combinations(bots, 2))
    random.shuffle(games)

    matches = len(games)*args.matches*len(args.planets)
    rounds = matches * args.rounds

    log("{} Bots, {} Maps, {} Games, {} Matches, {} Rounds, 1 victor".format(len(bots), len(args.planets),
                                                                             len(games), matches, rounds))

    scores = lambda: sorted(zip(wins, args.players), key=lambda x: x[0], reverse=True)[:3]

    i = 0
    for ret in pool.imap_unordered(execute, gen_rounds(games)):
        i += 1
        (gid, mid, rid), winner, (pid1, pid2), (map_size, seed) = ret
        if winner is None:
            result = "DRAW"
        else:
            result = args.players[winner]
            wins[winner] += 1

        log("({}:{}:{} | {}:{} | {}:{}): {}".format(gid, mid, rid, map_size, seed, pid1, pid2, result), lvl=2)

        if i % NOTIFY_AMOUNT == 0:
            log("Finished {}/{} rounds {:.2f}%. Current top 3: {}".format(i, rounds, (float(i) / rounds * 100),
                                                                          scores()[:3]))

    pool.close()
    log("All games finished", type="SUCCESS")
    for i, (wins, bot) in enumerate(scores()):
        log("{:3}. ({})".format(i, bot))


def gen_rounds(games):
    for gid, game in enumerate(games):
        for map_id, map_size in enumerate(args.planets):
            for i in range(args.matches):
                mid = map_id * args.matches + i
                seed = random.randint(0, 10000)
                for j in range(args.rounds):
                    players = (game[0], game[1]) if j % 2 == 0 else (game[1], game[0])
                    yield ((gid, mid, j), players, (map_size, seed))


def execute(params):
    ids, (player1, player2), (map_size, seed) = params
    start, _ = State.generate(map_size, seed)

    winner = engine.play(player1[1], player2[1], start, verbose=False, outfile=None,
                         max_time=args.max_time * 1000, max_turns=args.max_turns)
    return ids, (player1[0], player2[0])[winner-1], (player1[0], player2[0]), (map_size, seed)


# following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False  # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False


def log(s, type='INFO', lvl=0):
    color = WHITE
    if type in colors:
        color = colors[type]
    if args.verbose >= lvl:
        sys.stdout.write("[")
        printout("%07s" % type, color)
        sys.stdout.write("] %s\n" % s)


def printout(text, colour=WHITE):
    if args.color:
        seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)


def optparse():
    global args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-c', '--color', action='store_true', dest='color',
                        help="force color output")
    parser.add_argument('-n', '--no-color', action='store_false', dest='color',
                        help="force disable color output")

    parser.add_argument("-p", "--num-planets",
                        dest="planets",
                        help="List of map sizes to use",
                        type=int, nargs='*',
                        default=[6])

    parser.add_argument("-m", "--num-matches",
                        dest="matches",
                        help="Amount of matches played per map size",
                        type=int, default=10)

    parser.add_argument("-r", "--rounds",
                        dest="rounds",
                        help="Amount of rounds played to determine victor of a match.",
                        type=int, default=2)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="Maximum amount of time allowed per turn in seconds",
                        type=float, default=5)

    parser.add_argument("-T", "--max-turns",
                        dest="max_turns",
                        help="Maximum amount of turns per game",
                        type=int, default=5000)

    parser.add_argument("players",
                        metavar="player",
                        help="Players for the game",
                        type=str, nargs='*',
                        default=["rand", "bully", "rdeep"])

    parser.add_argument("-P", "--pool-size",
                        dest="parallelism",
                        help="Pool size for parallelism. Do not use unless you know what you are doing",
                        type=int, default=multiprocessing.cpu_count())

    parser.add_argument("-v", "--verbose",
                        action="count", default=0,
                        help="Show more output")

    parser.set_defaults(color=has_colours(sys.stdout))

    args = parser.parse_args()


if __name__ == "__main__":
    optparse()
    main()
