#Taka Irizarry
import random
import csv
import math
from copy import deepcopy
import time

EPSILON = 1e-6 #small constant to avoid division by zero
ALPHA = 0.7  #weighting factor for final score weigt
BETA = 0.3   #weighting factor for max tile weight

from engine import (
    new_grid,
    apply_action,
    get_valid_actions,
    gameover,
    max_tile,
)

#Random agent plays one game returns score max tile and number of moves
def play_random_game():
    grid = new_grid()
    total_score = 0
    moves = 0

    while not gameover(grid):
        actions = get_valid_actions(grid)
        if not actions:
            break
        action = random.choice(actions)
        grid, score_gain, moved = apply_action(grid, action)
        if not moved:
            continue
        total_score += score_gain
        moves += 1

    return total_score, max_tile(grid), moves


#MCTS implementation
class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state# 4x4 grid
        self.parent = parent
        self.action = action# action taken from parent to this node
        self.children = []
        self.visits = 0
        self.total_reward = 0.0
        self.untried_actions = get_valid_actions(state)

    def is_terminal(self):
        return gameover(self.state)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    # Selection using UCB
    def best_child(self, c_param):
        best_value = float("-inf")
        best_nodes = []

        for child in self.children:
            if child.visits == 0:
                uct_value = float("inf")
            else:
                exploit = child.total_reward / child.visits
                explore = math.sqrt(2 * math.log(self.visits) / child.visits)
                uct_value = exploit + c_param * explore

            if uct_value > best_value:
                best_value = uct_value
                best_nodes = [child]
            elif uct_value == best_value:
                best_nodes.append(child)

        return random.choice(best_nodes)

#Rollout policy is random action
def rollout_policy_random(grid):
    actions = get_valid_actions(grid)
    if not actions:
        return None
    return random.choice(actions)

#### NEW STUF FOR ROLLOUT AND REWARD 

#Counts the empty cells.
def count_empty_cells(grid):
    return sum(1 for r in range(4) for c in range(4) if grid[r][c] == 0)

def max_tile_in_corner(grid):
    m = max_tile(grid)
    corners = [(0,0), (0,3), (3,0), (3,3)]
    return 1 if any(grid[r][c] == m for r,c in corners) else 0

def weighted_value(grid):
    empty_w = 10.0
    corner_w = 1.0
    return empty_w * count_empty_cells(grid) + corner_w * max_tile_in_corner(grid)


def rollout_policy_weighted(grid):
    actions = get_valid_actions(grid)
    if not actions:
        return None

    if random.random() < EPSILON:
        return random.choice(actions)
    
    best_action = None
    best_value = float("-inf")

    for a in actions:
        next_grid, _, moved = apply_action(deepcopy(grid), a)
        if not moved:
            continue
        v = weighted_value(next_grid)
        if v > best_value:
            best_value = v
            best_action = a

    return best_action if best_action is not None else random.choice(actions)

#Run simulation from the state until terminal(gameover)
def rollout(state):
    grid = deepcopy(state)
    total_score = 0

    while not gameover(grid):
        action = rollout_policy_weighted(grid)
        if action is None:
            break
        grid, score_gain, moved = apply_action(grid, action)
        if not moved:
            continue
        total_score += score_gain
    return total_score
    #return max_tile(grid) / (total_score + EPSILON)
    #return (total_score + EPSILON) / max_tile(grid)
    #return (total_score + EPSILON) * (max_tile(grid))
    #return ALPHA * total_score + BETA * (max_tile(grid))


# Perform mcts search and return best action
def mcts_search(root_state, num_simulations=50, c_param=1.414):
    root = MCTSNode(deepcopy(root_state))
    for _ in range(num_simulations):
        node = root
        #SELECTION
        while (not node.is_terminal()) and node.is_fully_expanded():
            node = node.best_child(c_param)

        #EXPANSION
        if (not node.is_terminal()) and node.untried_actions:
            action = node.untried_actions.pop()
            new_state, _, _ = apply_action(deepcopy(node.state), action)
            child = MCTSNode(new_state, parent=node, action=action)
            node.children.append(child)
            node = child

        #SIMULATION(ROLLOUT)
        reward = rollout(node.state)

        #BACKPROPAGATION
        while node is not None:
            node.visits += 1
            node.total_reward += reward
            node = node.parent

    #Choose child with highest visit count
    if not root.children:
        return None
    best_child = max(root.children, key=lambda n: n.visits)
    return best_child.action

#Play a game using mcts at each move.
def play_mcts_game(num_simulations=50, c_param=1.414):
    grid = new_grid()
    total_score = 0
    moves = 0

    while not gameover(grid):
        actions = get_valid_actions(grid)
        if not actions:
            break
        action = mcts_search(grid, num_simulations=num_simulations, c_param=c_param)
        if action is None:
            break
        grid, score_gain, moved = apply_action(grid, action)
        if not moved:
            break
        total_score += score_gain
        moves += 1
    return total_score, max_tile(grid), moves


# Run multiple experiments and log results to CSV
def run_experiments():
    random.seed(0)#for reproducibility
    experiments = [
        #random agent
        {"name": "baseline_random", "method": "random",
         "c_param": None, "num_simulations": None},

        # experiements for c value budget fixed at 30.
        {"name": "c_sweep_c0.5",   "method": "mcts",
         "c_param": 0.5,   "num_simulations": 30},
        {"name": "c_sweep_c1.0",   "method": "mcts",
         "c_param": 1.0,   "num_simulations": 30},
        {"name": "c_sweep_c1.414", "method": "mcts",
         "c_param": 1.414, "num_simulations": 30},

        #experiement for budget c fixed at 1.414
        {"name": "budget_sweep_b5",   "method": "mcts",
         "c_param": 1.414, "num_simulations": 5},
        {"name": "budget_sweep_b15",  "method": "mcts",
         "c_param": 1.414, "num_simulations": 15},
        {"name": "budget_sweep_b30",  "method": "mcts",
         "c_param": 1.414, "num_simulations": 30},
        {"name": "budget_sweep_b60",  "method": "mcts",
         "c_param": 1.414, "num_simulations": 60},
    ]

    games_per_setting = 5
    output_file = "results.csv"
    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "experiment_name",
            "method",
            "c_param",
            "num_simulations",
            "game_index",
            "final_score",
            "max_tile",
            "num_moves",
        ])

        for config_idx, config in enumerate(experiments):
            name = config["name"]
            method = config["method"]
            c_param = config["c_param"]
            num_simulations = config["num_simulations"]

            print(f"\n***Experiment {config_idx+1}/{len(experiments)}")
            print(f"name={name}, method={method}, c={c_param}, rollouts={num_simulations}")
            setting_start = time.time()

            for game_idx in range(games_per_setting):
                game_start = time.time()

                if method == "random":
                    final_score, max_t, num_moves = play_random_game()
                elif method == "mcts":
                    final_score, max_t, num_moves = play_mcts_game(
                        num_simulations=num_simulations,
                        c_param=c_param
                    )
                else:
                    raise ValueError("Unknown method: " + str(method))

                game_elapsed = time.time() - game_start

                # Per-game info
                print(
                    f"  Game {game_idx+1}/{games_per_setting}:  "
                    f" score={final_score}, max_tile={max_t}, "
                    f"moves={num_moves}, time={game_elapsed:.2f}s"
                )

                writer.writerow([
                    name,
                    method,
                    c_param if c_param is not None else "",
                    num_simulations if num_simulations is not None else "",
                    game_idx,
                    final_score,
                    max_t,
                    num_moves,
                ])

            setting_elapsed = time.time() - setting_start
            print(
                f"Finished setting: name={name}, method={method}, "
                f"c={c_param}, rollouts={num_simulations}, "
                f"total time={setting_elapsed:.2f}s"
            )
if __name__ == "__main__":
    run_experiments()