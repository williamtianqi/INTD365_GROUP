#!/usr/bin/env python3
"""
601.465/665 — Natural Language Processing
Assignment 1: Designing Context-Free Grammars

Assignment written by Jason Eisner
Modified by Kevin Duh
Re-modified by Ravneet, Tianqui, Pedro
"""
import os
import sys
import random
import argparse

# Want to know what command-line arguments a program allows?
# Commonly you can ask by passing it the --help option, like this:
#     python randsent.py --help
# This is possible for any program that processes its command-line
# arguments using the argparse module, as we do below.
#
# NOTE: When you use the Python argparse module, parse_args() is the
# traditional name for the function that you create to analyze the
# command line.  Parsing the command line is different from parsing a
# natural-language sentence.  It's easier.  But in both cases,
# "parsing" a string means identifying the elements of the string and
# the roles they play.

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


class Grammar:
    def __init__(self, grammar_file):
        """
        Context-Free Grammar (CFG) Sentence Generator

        Args:
            grammar_file (str): Path to a .gr grammar file

        Returns:
            self
        """
        self.rules = {}
        self._load_rules_from_file(grammar_file)

    def _load_rules_from_file(self, grammar_file):
        """
        Read grammar file and store its rules in self.rules

        Args:
            grammar_file (str): Path to the raw grammar file
        """
        with open(grammar_file, 'r') as file:
            for line in file:
                # Skip comments and empty lines
                if line.startswith("#") or line.strip() == "":
                    continue

                # Split the line into rule components
                parts = line.strip().split()

                rule_id, nonterminal, *production = parts

                if nonterminal not in self.rules:
                    self.rules[nonterminal] = []

                self.rules[nonterminal].append(production)

    def sample(self, derivation_tree, max_expansions, start_symbol):
        """
        Sample a random sentence from this grammar

        Args:
            derivation_tree (bool): if true, the returned string will represent
                the tree (using bracket notation) that records how the sentence
                was derived

            max_expansions (int): max number of nonterminal expansions we allow

            start_symbol (str): start symbol to generate from

        Returns:
            str: the random sentence or its derivation tree
        """

        if start_symbol not in self.rules:
            raise ValueError(f"Start symbol '{start_symbol}' not found in grammar rules.")

        # Helper function to recursively expand nonterminals and build the tree
        def expand_nonterminal_and_build_tree(symbol, depth):
            if depth > max_expansions:
                return [], f'({symbol})'

            if symbol not in self.rules:
                return [symbol], f'({symbol})'

            chosen_rule = random.choice(self.rules[symbol])

            expansion = []
            tree_parts = [f'({symbol}']

            for sub_symbol in chosen_rule:
                sub_expansion, sub_tree = expand_nonterminal_and_build_tree(sub_symbol, depth + 1)
                expansion += sub_expansion
                tree_parts.append(sub_tree)

            tree_parts.append(')')
            return expansion, ' '.join(tree_parts)

        sentence, tree = expand_nonterminal_and_build_tree(start_symbol, depth=0)

        if derivation_tree:
            return tree
        else:
            return ' '.join(sentence)



            


####################
### Main Program
####################
def main():
    # Parse command-line options
    args = parse_args()

    # Initialize Grammar object
    grammar = Grammar(args.grammar)

    # Generate sentences
    for i in range(args.num_sentences):
        # Use Grammar object to generate sentence
        if args.start_symbol:
            # Start generation from the specified symbol
            sentence = grammar.sample(
                derivation_tree=args.tree,
                max_expansions=args.max_expansions,
                start_symbol=args.start_symbol
            )
        else:
            # Generate full sentences starting from ROOT
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
