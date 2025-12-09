import numpy as np
import random

class AntColonyOptimization:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        distances: Şehirler arası mesafe matrisi (numpy array)
        n_ants: Karınca sayısı
        n_best: En iyi kaç yolun feromon bırakacağı
        n_iterations: İterasyon sayısı
        decay: Buharlaşma oranı
        alpha: Feromon etkisi
        beta: Mesafe etkisi
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = int(n_ants)
        self.n_best = int(n_best)
        self.n_iterations = int(n_iterations)
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        history = []

        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            # Bu iterasyondaki en iyiyi bul
            shortest_path = min(all_paths, key=lambda x: x[1])
            
            # Genel en iyiyi güncelle
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            
            # Feromon güncelleme (Sadece en iyi yollara)
            self.spread_pheronome(all_paths, self.n_best)
            
            # Buharlaşma
            self.pheromone *= self.decay
            
            history.append(all_time_shortest_path[1])
            
        return all_time_shortest_path, history

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                # Mesafe ne kadar kısaysa o kadar çok feromon bırak
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # Merkeze dönüş
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        # Olasılık formülü: (Feromon^alpha) * ((1/Mesafe)^beta)
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        
        if row.sum() == 0:
             possible_moves = [i for i in range(len(dist)) if i not in visited]
             return random.choice(possible_moves)

        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move
