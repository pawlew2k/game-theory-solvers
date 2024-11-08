from itertools import permutations
import numpy as np
from math import factorial

from strategies import find_strategies, find_all_strategies, extend_strategies, strategies_with_caret
from src.payoff_table_solver import solve_payoff_table


def blotto_game(strategies1, strategies2, points_for_kills=True) -> np.array:
    if len(strategies1[0]) != len(strategies2[0]):
        raise ValueError('Number of bridgeheads must be the same in both strategies')
    else:
        num_permutations = factorial(len(strategies1[0]))

    matrix = np.zeros((len(strategies1), len(strategies2)))
    for idx1, strategy1 in enumerate(strategies1):
        for idx2, strategy2 in enumerate(strategies2):
            score = 0
            for permuted_strategy1 in permutations(strategy1):
                for permuted_strategy2 in permutations(strategy2):
                    bridgeheads = zip(permuted_strategy1, permuted_strategy2)
                    for units1, units2 in bridgeheads:
                        units1, units2 = int(units1), int(units2)

                        if units1 > units2:
                            score += 1
                            if points_for_kills:
                                score += units2
                        if units2 > units1:
                            score -= 1
                            if points_for_kills:
                                score -= units1
            score /= num_permutations * num_permutations
            matrix[idx1, idx2] = float(score)
    return matrix


if __name__ == '__main__':
    num_bridgeheads = 3
    strategiesB = find_strategies(8, num_bridgeheads)
    strategiesK = find_strategies(5, num_bridgeheads)
    A = blotto_game(strategiesB, strategiesK, points_for_kills=True)

    v, X, Y = solve_payoff_table(A)
    extended_strategiesB, extended_X = extend_strategies(strategiesB, X)
    extended_strategiesK, extended_Y = extend_strategies(strategiesK, Y)

    print(f'Omega_B^={strategies_with_caret(strategiesB)}',
          f'Omega_K^={strategies_with_caret(strategiesK)}',
          '',
          f'A^=\n{A}',
          f'X^={X}',
          f'Y^={Y}',
          f'{v=}',
          '',
          f'Omega_B={extended_strategiesB}',
          f'X={extended_X}',
          '',
          f'Omega_K={extended_strategiesK}',
          f'Y={extended_Y}', sep='\n')
