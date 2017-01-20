import argparse
import multiprocessing
import multiprocessing.pool
import sys
import random

from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

from api import State, util

from bots.ml.ml import features

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
colors = {
    'SUCCESS': GREEN,
    'INFO': BLUE,
    'WARN': YELLOW,
    'FAIL': RED
}

args = None

NOTIFY_AMOUNT = 50


def main():

    pool = multiprocessing.Pool(processes=args.parallelism)

    bots = []
    for id, botname in enumerate(args.players):
        bots.append(util.load_player(botname))

    matches = len(bots) * args.matches * len(args.planets)

    log("Training against {} Bots, {} Maps, {} Matches".format(len(bots), len(args.planets), matches))
    data, target = [], []

    try:
        i = 0
        for ret in pool.imap_unordered(execute, gen_rounds(bots)):
            i += 1
            (bid, mid), winner, state_vectors, (map_size, seed) = ret

            # Treat DRAW as losing
            result = 'won' if winner == 1 else 'lost'

            data  += state_vectors
            target += [result] * len(state_vectors)

            log("({}:{} | {}:{}): {}".format(bid, mid, map_size, seed, result), lvl=1)

            if i % NOTIFY_AMOUNT == 0:
                log("Finished {}/{} matches ({:.2f})%.".format(i, matches, (float(i) / matches * 100)))
    except KeyboardInterrupt:
        log("Tournament interrupted by user", type="FAIL")
        pool.terminate()
        pool.join()
        sys.exit(1)

    pool.close()
    pool.join()

    log("All games finished", type="SUCCESS")
    generate_model(data, target)


# If you wish to use a different model, this
# is where to edit
def generate_model(data, target):
    log("Training logistic regression model", lvl=1)
    learner = LogisticRegression()
    model = learner.fit(data, target)

    log("Checking class imbalance", lvl=1)
    count = {}
    for str in target:
        if str not in count:
            count[str] = 0
        count[str] += 1

    log("Instances per class: {}".format(count))
    joblib.dump(model, args.model)
    log("Done", type="SUCCESS")


def gen_rounds(bots):
    for bid, bot in enumerate(bots):
        for map_id, map_size in enumerate(args.planets):
            for i in range(args.matches):
                mid = map_id * args.matches + i
                seed = random.randint(0, 10000)
                yield ((bid, mid), bot, (map_size, seed))


def execute(params):
    ids, bot, (map_size, seed) = params
    state, _ = State.generate(map_size, seed)

    state_vectors = []
    i = 0
    while not state.finished() and i <= args.max_turns:
        state_vectors.append(features(state))
        move = bot.get_move(state)
        state = state.next(move)

        i += 1

    winner = state.winner()

    return ids, winner, state_vectors, (map_size, seed)


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
                        type=int, default=1000)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="Maximum amount of time allowed per turn in seconds",
                        type=float, default=5)

    parser.add_argument("-T", "--max-turns",
                        dest="max_turns",
                        help="Maximum amount of turns per game",
                        type=int, default=100)

    parser.add_argument("model",
                        help="Output file for model",
                        type=str, default="./bots/ml/model.pkl")

    parser.add_argument("players",
                        metavar="player",
                        help="Players for the game",
                        type=str, nargs='+')

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
