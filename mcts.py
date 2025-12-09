#Taka Irizarry
import random
import csv
import math
from copy import deepcopy
import time

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
    return random.choice(actions)

#Run simulation from the state until terminal(play 2048 game until gameover)
def rollout(state):
    grid = deepcopy(state)
    total_score = 0
    while not gameover(grid):
        action = rollout_policy_random(grid)
        grid, score_gain, moved = apply_action(grid, action)
        if moved:
            total_score += score_gain
    return total_score

# Perform mcts search and return best action
def mcts_search(root_state, num_simulations=50, c_param=1.414):
    # create instance of MCTS node
    root = MCTSNode(deepcopy(root_state))
    # for each simulation
    for _ in range(num_simulations):
        # set current node to root node
        node = root
        #SELECTION (based on UCB, select successive child nodes until a leaf node is reached)
        while (not node.is_terminal()) and node.is_fully_expanded():
            node = node.best_child(c_param)

        #EXPANSION (use expand leaf node by 1 node and choose new expanded child leaf node)
        # if node's state is not gameover and has untried actions
        if (not node.is_terminal()) and node.untried_actions:
            # get the first untried action in the list (maybe change this to be randomized?)
            action = node.untried_actions.pop()
            # do action on node's state
            new_state, _, _ = apply_action(deepcopy(node.state), action)
            # create new instance on MCTS node storing the new state, parent node, and action
            child = MCTSNode(new_state, parent=node, action=action)
            # append child node to node's children
            node.children.append(child)
            # set current node to child node
            node = child

        #SIMULATION (complete one playout from new expanded child left node using the rollout policy)
        # (is the reward the final score or the highest numbered tile the final score?)
        reward = rollout(node.state)

        #BACKPROPAGATION (update all node value's from expanded left node to root node)
        # for each node
        while node is not None:
            node.visits += 1 # increase visit by 1
            node.total_reward += reward # increase total_reward by reward (metric used for evaluation)
            node = node.parent # move to next lower branch

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

    # while game is not over
    while not gameover(grid):
        # perform MCTS and get most optimal action
        action = mcts_search(grid, num_simulations=num_simulations, c_param=c_param)
        grid, score_gain, moved = apply_action(grid, action)
        if moved:
            total_score += score_gain
            moves += 1
    return total_score, max_tile(grid), moves

# Run multiple experiments and log results to CSV
def run_experiments():
    random.seed(0)#for reproducibility
    experiments = [
        # random agent experiment
        {
            "name": "baseline_random",
            "method": "random",
            "c_param": None,
            "num_simulations": None
        },
        # MCTS agent experiements with different exploration constants (c)
        # and a fixed rollout budget (num_simulations) of value 30.
        {
            "name": "c_sweep_c0.5",
            "method": "mcts",
            "c_param": 0.5,
            "num_simulations": 30
        },
        {
            "name": "c_sweep_c1.0",
            "method": "mcts",
            "c_param": 1.0,
            "num_simulations": 30
        },
        {
            "name": "c_sweep_c1.414",
            "method": "mcts",
            "c_param": 1.414,
            "num_simulations": 30
        },
        # MCTS agent experiements with different rollout budgets (num_simulations)
        # and a fixed exploration constant (c) of value 1.414.
        {
            "name": "budget_sweep_b5",
            "method": "mcts",
            "c_param": 1.414,
            "num_simulations": 5
        },
        {
            "name": "budget_sweep_b15",
            "method": "mcts",
            "c_param": 1.414,
            "num_simulations": 15
        },
        {
            "name": "budget_sweep_b30",
            "method": "mcts",
            "c_param": 1.414,
            "num_simulations": 30
        },
        {
            "name": "budget_sweep_b60",
            "method": "mcts",
            "c_param": 1.414,
            "num_simulations": 60
        },
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
