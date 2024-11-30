class BayesNet:
    """
    Feel free to add additional internal methods to this class.
    """

    def __init__(self):
        """
        Add any code to the constructor if you need.
        """
        self.nodes = {
            'Necronia flu': {'P': [0.8, 0.2]},
            'Typhonus worm': {'P': [0.05, 0.95]},
            'Scleraitis': {'P': [0.25, 0.75]},
            'Hydrophobia': {'P': [[0.95, 0.05], [0.01, 0.99]]},
            'Mania': {'P': [[[0.99, 0.01], [0.4, 0.6]], [[0.7, 0.3], [0.05, 0.95]]]},
            'Fatigue': {'P': [[0.9, 0.1], [0.3, 0.7]]},
            'Cysts': {'P': [[0.6, 0.4], [0.5, 0.5]]},
            'Tumors': {'P': [[[0.85, 0.15], [0.7, 0.3]], [[0.7, 0.3], [0.15, 0.85]]]},
            'Skin lesions': {'P': [[0.55, 0.45], [0.2, 0.8]]},
            'Necrosis': {'P': [[[0.9, 0.1], [0.25, 0.75]], [[0.35, 0.65], [0.1, 0.9]]]},
        }

    def query(self, variable: str, evidence: dict[str, bool]) -> float:
        """
        This is the main function you need to implement.
        """

        probabilities = self.compute_distribution(variable, evidence)
        return probabilities[True]
        
    def compute_distribution(self, target_variable: str, evidence: dict[str, bool]) -> dict[bool, float]:
        """
        Computes the probability distribution for the target variable.
        """
        distribution = {}
        for target_value in [True, False]:
            evidence_copy = evidence.copy()
            evidence_copy[target_variable] = target_value
            distribution[target_value] = self.enumerate_all_variables(list(self.nodes.keys()), evidence_copy)
        
        total_probability = sum(distribution.values())
        for target_value in distribution:
            distribution[target_value] /= total_probability
        
        return distribution

    def enumerate_all_variables(self, variables: list[str], evidence: dict[str, bool]) -> float:
        """
        Recursively compute probabilities for all variables in the network.
        """
        if not variables:
            return 1.0
        
        current_variable = variables[0]
        remaining_variables = variables[1:]

        if current_variable in evidence:
            return (
                self.get_conditional_probability(current_variable, evidence)
                * self.enumerate_all_variables(remaining_variables, evidence)
            )
        else:
            total_probability = 0
            for variable_value in [True, False]:
                evidence_copy = evidence.copy()
                evidence_copy[current_variable] = variable_value
                total_probability += (
                    self.get_conditional_probability(current_variable, evidence_copy)
                    * self.enumerate_all_variables(remaining_variables, evidence_copy)
                )
            return total_probability

    def get_conditional_probability(self, node: str, evidence: dict[str, bool]) -> float:
        """
        Calculate the conditional probability of a node given its parents.
        """
        parent_nodes = self.get_parents(node)
        if not parent_nodes:
            return self.nodes[node]['P'][0] if evidence[node] else self.nodes[node]['P'][1]
        
        parent_values = tuple(evidence[parent] for parent in parent_nodes)
        conditional_prob_table = self.nodes[node]['P']
        for value in parent_values:
            conditional_prob_table = conditional_prob_table[0] if value else conditional_prob_table[1]
        return conditional_prob_table[0] if evidence[node] else conditional_prob_table[1]


    def get_parents(self, node: str) -> list[str]:
        """
        Return the list of parent nodes for a given node.
        """
        parent_map = {
            'Hydrophobia': ['Necronia flu'],
            'Mania': ['Hydrophobia', 'Typhonus worm'],
            'Fatigue': ['Hydrophobia'],
            'Cysts': ['Typhonus worm'],
            'Tumors': ['Cysts', 'Scleraitis'],
            'Skin lesions': ['Scleraitis'],
            'Necrosis': ['Skin lesions', 'Scleraitis']
        }
        return parent_map.get(node, [])

if __name__ == "__main__":

    net = BayesNet()
    print(net.query('Typhonus worm', {'Mania': True, 'Tumors': False}))
