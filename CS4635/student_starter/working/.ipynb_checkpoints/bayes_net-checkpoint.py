
class BayesNet:
    """
    Feel free to add additional internal methods to this class.
    """

    def __init__(self):
        """
        Add any code to the constructor if you need.
        """
        self.nodes = {
            "Necronia flu": {"P(T)": 0.8, "P(F)": 0.2},
            "Typhonus worm": {"P(T)": 0.05, "P(F)": 0.95},
            "Scleraitis": {"P(T)": 0.25, "P(F)": 0.75},
            "Hydrophobia": {
                ("Necronia flu", True): {"P(T)": 0.95, "P(F)": 0.05},
                ("Necronia flu", False): {"P(T)": 0.01, "P(F)": 0.99}
            },
            "Fatigue": {
                ("Hydrophobia", True): {"P(T)": 0.9, "P(F)": 0.1},
                ("Hydrophobia", False): {"P(T)": 0.3, "P(F)": 0.7}
            },
            "Mania": {
                ("Hydrophobia", True, "Typhonus worm", True): {"P(T)": 0.99, "P(F)": 0.01},
                ("Hydrophobia", True, "Typhonus worm", False): {"P(T)": 0.4, "P(F)": 0.6},
                ("Hydrophobia", False, "Typhonus worm", True): {"P(T)": 0.7, "P(F)": 0.3},
                ("Hydrophobia", False, "Typhonus worm", False): {"P(T)": 0.05, "P(F)": 0.95}
            },
            "Cysts": {
                ("Typhonus worm", True): {"P(T)": 0.6, "P(F)": 0.4},
                ("Typhonus worm", False): {"P(T)": 0.5, "P(F)": 0.5}
            },
            "Tumors": {
                ("Cysts", True, "Scleraitis", True): {"P(T)": 0.85, "P(F)": 0.15},
                ("Cysts", True, "Scleraitis", False): {"P(T)": 0.7, "P(F)": 0.3},
                ("Cysts", False, "Scleraitis", True): {"P(T)": 0.7, "P(F)": 0.3},
                ("Cysts", False, "Scleraitis", False): {"P(T)": 0.15, "P(F)": 0.85}
            },
            "Skin lesions": {
                ("Scleraitis", True): {"P(T)": 0.55, "P(F)": 0.45},
                ("Scleraitis", False): {"P(T)": 0.2, "P(F)": 0.8}
            },
            "Necrosis": {
                ("Skin lesions", True, "Scleraitis", True): {"P(T)": 0.9, "P(F)": 0.1},
                ("Skin lesions", True, "Scleraitis", False): {"P(T)": 0.25, "P(F)": 0.75},
                ("Skin lesions", False, "Scleraitis", True): {"P(T)": 0.35, "P(F)": 0.65},
                ("Skin lesions", False, "Scleraitis", False): {"P(T)": 0.1, "P(F)": 0.9}
            }
        }

    def query(self, variable: str, evidence: dict[str, bool]) -> float:
        """
        This is the main function you need to implement.
        """
        if variable in evidence:
            return 1.0 if evidence[variable] else 0.0

        if variable in ["Necronia flu", "Typhonus worm", "Scleraitis"]:
            return self.nodes[variable]["P(T)"] if evidence.get(variable, True) else self.nodes[variable]["P(F)"]

        table = self.nodes[variable]

        total_prob = 0.0
        for conditions, probs in table.items():
            match = True
            conditional_prob = 1.0
            for i in range(0, len(conditions), 2):
                cond_var, cond_value = conditions[i], conditions[i+1]
                if cond_var in evidence:
                    if evidence[cond_var] != cond_value:
                        match = False
                        break
                else:
                    prob = self.query(cond_var, evidence)
                    conditional_prob *= prob if cond_value else (1 - prob)

            if match:
                total_prob += conditional_prob * probs["P(T)"]

        return round(total_prob, 10)

if __name__ == "__main__":

    net = BayesNet()
    print(net.query('Typhonus worm', {'Mania': True, 'Tumors': False}))