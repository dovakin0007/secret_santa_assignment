from typing import Dict, Set
from secret_santa.employee.emp import Employee
from secret_santa.prev_secret_santa.secret_santa import PreviousSecretSanta
import csv
import random
import networkx as nx


def generate_secret_santa_graph(emps_dict: Dict[str, Employee], visited_combs: Dict[str, Set[str]]):
    G = nx.DiGraph()
    for emp in emps_dict.keys():
        G.add_node(emp)
    for giver in emps_dict.keys():
        for receiver in emps_dict.keys():
            if giver != receiver and receiver not in visited_combs[giver]:
                G.add_edge(giver, receiver)

    for _ in range(100):
        if nx.is_strongly_connected(G):
            cycle = nx.algorithms.tournament.hamiltonian_path(G)
            if cycle:
                assignment = {cycle[i]: cycle[i + 1]
                              for i in range(len(cycle) - 1)}
                assignment[cycle[-1]] = cycle[0]
                return assignment

        G = nx.DiGraph()
        shuffled_emps = list(emps_dict.keys())
        random.shuffle(shuffled_emps)
        for giver in shuffled_emps:
            for receiver in shuffled_emps:
                if giver != receiver and receiver not in visited_combs[giver]:
                    G.add_edge(giver, receiver)

    raise ValueError("Failed to generate a valid Secret Santa cycle.")


def generate_secret_santa(emps_dict, visited_combs):
    emps_list = list(emps_dict.keys())
    for _ in range(100):
        random.shuffle(emps_list)
        assignment = {}
        available_receivers = set(emps_list)
        for giver in emps_list:
            possible_receivers = available_receivers - visited_combs[giver]
            if not possible_receivers:
                break
            receiver = random.choice(list(possible_receivers))
            assignment[giver] = receiver
            available_receivers.remove(receiver)
        if len(assignment) == len(emps_dict):
            return assignment

    raise ValueError(
        "Failed to generate valid Secret Santa assignments after 100 attempts.")


def save_to_csv(secret_santa_pairs, emps_dict, output_file="Secret-Santa-Assignments.csv"):
    with open(output_file, mode="w", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(["Employee_Name", "Employee_EmailID",
                        "Secret_Child_Name", "Secret_Child_EmailID"])
        for giver, receiver in secret_santa_pairs.items():
            writer.writerow([emps_dict[giver].emp_name, giver,
                            emps_dict[receiver].emp_name, receiver])
    print(f"Secret Santa assignments saved to {output_file}")


def main():
    emps = Employee.read_employee_data("Employee-List.xlsx")
    previous_results = PreviousSecretSanta.read_secret_santa_data(
        "Secret-Santa-Game-Result-2023.xlsx")
    emps_dict = {emp.emp_id: emp for emp in emps}
    prev_santa_dict = {
        previous_result.giver_email: previous_result for previous_result in previous_results}

    visited_combs = {emp_id: {emp_id} for emp_id in emps_dict.keys()}
    for emp_id, previous_result in prev_santa_dict.items():
        receiver_email = previous_result.receiver_email
        if receiver_email:
            visited_combs[emp_id].add(receiver_email)

    try:
        secret_santa_pairs = generate_secret_santa(emps_dict, visited_combs)
        print("\nUsing standard random assignment method:")
    except ValueError:
        print("\nStandard method failed! Switching to graph-based approach...")
        secret_santa_pairs = generate_secret_santa_graph(
            emps_dict, visited_combs)

    print("\nSecret Santa Assignments:")
    for giver, receiver in secret_santa_pairs.items():
        print(f"{emps_dict[giver].emp_name} ({giver}) → {
              emps_dict[receiver].emp_name} ({receiver})")

    save_to_csv(secret_santa_pairs, emps_dict)


if __name__ == "__main__":
    main()
