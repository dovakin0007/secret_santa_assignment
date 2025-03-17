import unittest
import openpyxl
from typing import List, Dict
import random

# Assuming the original code is in a module named `secret_santa`
from secret_santa import generate_secret_santa
from secret_santa.employee.emp import Employee


class TestGenerateSecretSanta(unittest.TestCase):
    def test_generate_secret_santa(self):
        emps_dict = {
            "john.doe@example.com": Employee(name="John Doe", email="john.doe@example.com"),
            "jane.doe@example.com": Employee(name="Jane Doe", email="jane.doe@example.com"),
            "alice@example.com": Employee(name="Alice", email="alice@example.com")
        }
        visited_combs = {
            "john.doe@example.com": {"john.doe@example.com"},
            "jane.doe@example.com": {"jane.doe@example.com"},
            "alice@example.com": {"alice@example.com"}
        }

        random.seed(42)
        assignment = generate_secret_santa(emps_dict, visited_combs)

        self.assertEqual(len(assignment), 3)
        self.assertNotEqual(
            assignment["john.doe@example.com"], "john.doe@example.com")
        self.assertNotEqual(
            assignment["jane.doe@example.com"], "jane.doe@example.com")
        self.assertNotEqual(
            assignment["alice@example.com"], "alice@example.com")


class TestGenerateSecretSanta(unittest.TestCase):
    def test_generate_secret_santa(self):
        emps_dict = {
            "john.doe@example.com": Employee(name="John Doe", email="john.doe@example.com"),
            "jane.doe@example.com": Employee(name="Jane Doe", email="jane.doe@example.com"),
            "alice@example.com": Employee(name="Alice", email="alice@example.com")
        }
        visited_combs = {
            "john.doe@example.com": {"john.doe@example.com"},
            "jane.doe@example.com": {"jane.doe@example.com"},
            "alice@example.com": {"alice@example.com"}
        }

        random.seed(42)  # Set seed for reproducibility
        assignment = generate_secret_santa(emps_dict, visited_combs)

        self.assertEqual(len(assignment), 3)
        self.assertNotEqual(
            assignment["john.doe@example.com"], "john.doe@example.com")
        self.assertNotEqual(
            assignment["jane.doe@example.com"], "jane.doe@example.com")
        self.assertNotEqual(
            assignment["alice@example.com"], "alice@example.com")

    def test_generate_secret_santa_with_previous_assignments(self):
        emps_dict = {
            "john.doe@example.com": Employee(name="John Doe", email="john.doe@example.com"),
            "jane.doe@example.com": Employee(name="Jane Doe", email="jane.doe@example.com"),
            "alice@example.com": Employee(name="Alice", email="alice@example.com"),
            "bob@example.com": Employee(name="Bob", email="bob@example.com")
        }

        previous_assignments = {
            "john.doe@example.com": "jane.doe@example.com",
            "jane.doe@example.com": "alice@example.com",
            "alice@example.com": "bob@example.com",
            "bob@example.com": "john.doe@example.com"
        }

        visited_combs = {emp_id: {emp_id} for emp_id in emps_dict.keys()}
        for giver, receiver in previous_assignments.items():
            visited_combs[giver].add(receiver)

        random.seed(42)
        new_assignments = generate_secret_santa(emps_dict, visited_combs)

        for giver, receiver in new_assignments.items():
            self.assertNotEqual(giver, receiver, f"{
                                giver} is assigned to themselves!")

            self.assertNotEqual(
                receiver,
                previous_assignments.get(giver, None),
                f"{giver} is assigned to the same person as last year!"
            )

        self.assertEqual(len(new_assignments), len(emps_dict))
        self.assertEqual(set(new_assignments.keys()), set(emps_dict.keys()))
        self.assertEqual(set(new_assignments.values()), set(emps_dict.keys()))


class TestSecretSanta(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.emps_dict = {
            "john.doe@example.com": Employee(name="John Doe", email="john.doe@example.com"),
            "jane.doe@example.com": Employee(name="Jane Doe", email="jane.doe@example.com"),
            "alice@example.com": Employee(name="Alice", email="alice@example.com"),
            "bob@example.com": Employee(name="Bob", email="bob@example.com"),
        }
        self.visited_combs = {emp: {emp} for emp in self.emps_dict.keys()}

    def test_generate_secret_santa_valid_assignment(self):
        """
        Test if generate_secret_santa assigns everyone a valid recipient.
        """
        assignments = generate_secret_santa(self.emps_dict, self.visited_combs)

        # Ensure everyone has an assignment
        self.assertEqual(len(assignments), len(self.emps_dict))

        # Ensure no one is assigned to themselves
        for giver, receiver in assignments.items():
            self.assertNotEqual(giver, receiver, f"{
                                giver} was assigned to themselves!")

        # Ensure all assigned people are from the original list
        self.assertEqual(set(assignments.values()), set(self.emps_dict.keys()))

    def test_generate_secret_santa_with_previous_assignments(self):
        """
        Test that no one gets the same assignment as last year.
        """
        prev_assignments = {
            "john.doe@example.com": "jane.doe@example.com",
            "jane.doe@example.com": "alice@example.com",
            "alice@example.com": "bob@example.com",
            "bob@example.com": "john.doe@example.com",
        }

        # Update visited_combs to include last year's assignments
        for giver, receiver in prev_assignments.items():
            self.visited_combs[giver].add(receiver)

        assignments = generate_secret_santa(self.emps_dict, self.visited_combs)

        for giver, receiver in assignments.items():
            self.assertNotEqual(receiver, prev_assignments.get(giver), f"{
                                giver} got the same person as last year!")

    def test_generate_secret_santa_handles_unassignable_case(self):
        """
        Test that generate_secret_santa raises an error when a valid assignment isn't possible.
        """
        # Set up a case where no valid assignments can exist
        self.visited_combs = {emp: set(self.emps_dict.keys())
                              for emp in self.emps_dict.keys()}

        with self.assertRaises(ValueError):
            generate_secret_santa(self.emps_dict, self.visited_combs)


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
