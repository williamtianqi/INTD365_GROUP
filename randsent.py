
"""
Natural Language Processing
Assignment: Designing Context-Free Grammars
Re-Write Co-Authots: Pedro, Ravneet, Tianqui

"""
import os
import sys
import random
import argparse

class Grammar:

    def __init__(self, grammar_file):
        """
        Context-Free Grammar (CFG) Sentence Generator

        Args:
            grammar_file (str): Path to a .gr grammar file

        Returns:
            self
        """
        self.rules = {}  # Dictionary to store grammar rules
        self._load_rules_from_file(grammar_file)

    def _load_rules_from_file(self, grammar_file):
        """     
        Read grammar file and store its rules in self.rules

        Args:
            grammar_file (str): Path to the raw grammar file
        """
        with open(grammar_file, 'r') as file:
            current_rule = None
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split(None, 2)
                    if len(parts) == 3 and parts[0].isdigit():
                        rule_id, nonterminal, production = parts
                        rule_id = int(rule_id)
                        if rule_id not in self.rules:
                            self.rules[rule_id] = {"nonterminal": nonterminal, "production": production}
                    elif current_rule:
                        current_rule["production"] += f" {line}"
                    else:
                        current_rule = None

        # Print loaded rules for debugging
        for rule_id, rule in self.rules.items():
            print(f"Rule {rule_id}: {rule['nonterminal']} -> {rule['production']}")



    def _expand(self, symbol):
        """
        Expand a nonterminal symbol into its production rule

        Args:
            symbol (str): The nonterminal symbol to expand

        Returns:
            list: The expanded production rule as a list of tokens
        """
        if symbol in self.rules:
            production = self.rules[symbol]["production"]
            return production.split()
        else:
            return [symbol]

    def sample(self, derivation_tree, max_expansions, start_symbol):
        sentence = []
        stack = [(start_symbol, 0)]  # Initialize the stack with the start symbol

        while stack:
            symbol, expansions = stack.pop()

            if expansions >= max_expansions:
                continue  # Avoid excessive expansions

            expansion = self._expand(symbol)

            for token in reversed(expansion):
                stack.append((token, expansions + 1))

            sentence.extend(expansion)

        if derivation_tree:
            print("Derivation Tree Sentence:", " ".join(sentence))  # Add this line for debugging
            return " ".join(sentence)
        else:
            print("Generated Sentence:", " ".join([token for token in sentence if not token.isupper()]))  # for debugging
            return " ".join([token for token in sentence if not token.isupper()])

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        args (an argparse.Namespace): Stores command-line attributes
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description="Generate random sentences from a PCFG")
    # Grammar file (required argument)
    parser.add_argument(
        "-g",
        "--grammar",
        type=str, required=True,
        help="Path to grammar file",
    )
    # Start symbol of the grammar
    parser.add_argument(
        "-s",
        "--start_symbol",
        type=str,
        help="Start symbol of the grammar (default is ROOT)",
        default="ROOT",
    )
    # Number of sentences
    parser.add_argument(
        "-n",
        "--num_sentences",
        type=int,
        help="Number of sentences to generate (default is 1)",
        default=1,
    )
    # Max number of nonterminals to expand when generating a sentence
    parser.add_argument(
        "-M",
        "--max_expansions",
        type=int,
        help="Max number of nonterminals to expand when generating a sentence",
        default=450,
    )
    # Print the derivation tree for each generated sentence
    parser.add_argument(
        "-t",
        "--tree",
        action="store_true",
        help="Print the derivation tree for each generated sentence",
        default=False,
    )
    return parser.parse_args()

def main():
    # Parse command-line options
    args = parse_args()

    # Print the grammar file path
    print("Grammar File:", args.grammar)

    # Initialize Grammar object
    grammar = Grammar(args.grammar)

    # Generate sentences
    for i in range(args.num_sentences):
        # Use Grammar object to generate sentence
        sentence = grammar.sample(
            derivation_tree=args.tree,
            max_expansions=args.max_expansions,
            start_symbol=args.start_symbol
        )

        # If it's a tree, print the formatted tree structure
        if args.tree:
            formatted_tree = format_tree(sentence)
            print(formatted_tree)
        else:
            print(sentence)

#1.3 Printing Trees

def format_tree(sentence):
    # Split the sentence into tokens
    tokens = sentence.split()

    # Initialize variables for tracking parentheses
    open_parentheses = 0
    formatted_tree = ""

    # Iterate through tokens to format the tree structure
    for token in tokens:
        if token.isupper():
            # Nonterminal symbol (e.g., NP, VP)
            formatted_tree += f"({token} "
            open_parentheses += 1
        elif token == ".":
            # End of the sentence
            formatted_tree += ")"
        else:
            # Terminal symbol or word
            formatted_tree += f"{token} "

    # Add closing parentheses for any remaining open parentheses
    formatted_tree += (open_parentheses * ") ")

    return formatted_tree.strip()

if __name__ == "__main__":
    main()
