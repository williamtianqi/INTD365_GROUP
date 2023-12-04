#!/usr/bin/env python3
"""
601.465/665 — Natural Language Processing
Assignment 1: Designing Context-Free Grammars

Assignment written by Jason Eisner
Modified by Kevin Duh
Re-modified by Alexandra DeLucia

Code template written by Alexandra DeLucia,
based on the submitted assignment with Keith Harrigian
and Carlos Aguirre Fall 2019
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
            return " ".join(sentence)
        else:
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

        # Print the sentence with the specified format.
        # If it's a tree, we'll pipe the output through the prettyprint script.
        if args.tree:
            prettyprint_path = os.path.join(os.getcwd(), 'prettyprint')
            t = os.system(f"echo '{sentence}' | perl {prettyprint_path}")
        else:
            print(sentence)

if __name__ == "__main__":
    main()
