import pulp

def portfolio_optimizer(bonds, target_duration, target_convexity, target_rating):
    num_bonds = len(bonds)

    prob = pulp.LpProblem("Bond Portfolio Optimization", pulp.LpMaximize)

    # Define the decision variables (weights of each bond)
    weights = [pulp.LpVariable(f"weight_{i}", lowBound=0, upBound=1) for i in range(num_bonds)]

    # Define the objective function (maximize yield)
    prob += pulp.lpSum([bonds[i][1] * weights[i] for i in range(num_bonds)]), "Total Yield"

    # Define the duration constraint
    prob += pulp.lpSum([bonds[i][0] * weights[i] for i in range(num_bonds)]) == target_duration, "Duration Constraint"

    # Define the convexity constraint
    prob += pulp.lpSum([bonds[i][2] * weights[i] for i in range(num_bonds)]) == target_convexity, "Convexity Constraint"

    # Define the ratings contraint
    prob += pulp.lpSum([bonds[i][3] * weights[i] for i in range(num_bonds)]) == target_rating, "Ratings Contraint"

    # Define the weight constraint (weights must sum to 1)
    prob += pulp.lpSum(weights) == 1, "Weight Constraint"

    #
    # prob += pulp.lpSum([bonds[i][4] * weights[i] for i in range(num_bonds)]) == target_par, "Portfolio Par Value"

    status = prob.solve()

    # Get the optimal weights
    optimal_weights = {f"weight_{i}": weights[i].value() for i in range(num_bonds)}

    return status, optimal_weights


bonds = [(5, 0.03, 3, 0), (3, 0.04, 2, 2), (7, 0.02, 4, 1), (4, 0.05, 1, 3)]
target_duration = 5
target_convexity = 3
target_rating = 1



status, optimal_weights = portfolio_optimizer(bonds, target_duration, target_convexity, target_rating)

print(f"Optimization Status: {pulp.LpStatus[status]}")
for bond, weight in optimal_weights.items():
    print(f"{bond}: {weight:.2f}")
