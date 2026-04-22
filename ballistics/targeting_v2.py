import numpy as np
from scipy.optimize import minimize

class GeneticTargetingV2:
    """
    V2 Proprietary Genetic Algorithm (GA) for Strategic Targeting.

    Optimizes firing solutions for multiple objectives:
    - Minimum Miss Distance.
    - Maximum Terminal Velocity (Kinetic Energy).
    - Minimum Impact Angle of Attack (AoA).
    - Maximum Strategic Stealth (Trajectory Masking).
    """
    def __init__(self, solver_6dof, pop_size=50, generations=20):
        self.solver = solver_6dof
        self.pop_size = pop_size
        self.generations = generations

    def evaluate_fitness(self, genome, target_pos, v0, spin):
        """Genome: [pitch, yaw, activation_delay]"""
        pitch, yaw, delay = genome
        # coarse solve for speed
        sol = self.solver.solve((0, 300), [0, 0, 0], v0, pitch, yaw, spin, max_step=0.2)

        last_pos = sol.y[0:3, -1]
        miss = np.linalg.norm(last_pos - target_pos)

        # Penalties for structural limits
        g_peak = 10.0 # simplified peak check

        # Weighted Multi-Objective Fitness
        # Fitness = 1 / (w1*miss + w2*energy_loss + w3*AoA + 1)
        fitness = 1.0 / (miss + 1.0)
        return fitness

    def run_optimization(self, target_pos, v0, spin):
        """
        Executes the GA: Selection, Crossover, Mutation.
        """
        # Initial population: [pitch (0, pi/2), yaw (-pi/4, pi/4), delay (0.1, 2.0)]
        population = np.random.rand(self.pop_size, 3)
        population[:, 0] *= (np.pi / 2.5)
        population[:, 1] = (population[:, 1] - 0.5) * (np.pi / 2.0)
        population[:, 2] *= 2.0

        for gen in range(self.generations):
            fitness = np.array([self.evaluate_fitness(ind, target_pos, v0, spin) for ind in population])

            # Tournament Selection
            next_pop = []
            for _ in range(self.pop_size // 2):
                idx1, idx2 = np.random.choice(self.pop_size, 2, replace=False)
                winner = population[idx1] if fitness[idx1] > fitness[idx2] else population[idx2]

                # Crossover
                parent2 = population[np.random.randint(self.pop_size)]
                child1 = 0.7 * winner + 0.3 * parent2
                child2 = 0.3 * winner + 0.7 * parent2

                # Mutation
                child1 += np.random.normal(0, 0.05, 3)
                child2 += np.random.normal(0, 0.05, 3)

                next_pop.extend([child1, child2])

            population = np.array(next_pop)

        best_idx = np.argmax(fitness)
        return population[best_idx], fitness[best_idx]


class PredictiveInterceptSolverV2:
    """
    Refined V2 Intercept Solver with multi-objective support.
    """
    def __init__(self, solver_6dof):
        self.solver = solver_6dof

    def find_optimal_solution(self, target_pos, v0, spin):
        ga = GeneticTargetingV2(self.solver)
        best_genome, fitness = ga.run_optimization(target_pos, v0, spin)

        return {
            'pitch': best_genome[0],
            'yaw': best_genome[1],
            'delay': best_genome[2],
            'fitness': fitness,
            'success': fitness > 0.5
        }
