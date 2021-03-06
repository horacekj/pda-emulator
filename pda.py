#!/usr/bin/env python2
"""Classes and methods for working with non-deterministic pushdown automata."""

import copy

from automaton import Automaton
import exc as exceptions
from stack import PDAStack
from collections import deque


class PDA(Automaton):
    """A non-deterministic pushdown automaton."""

    def __init__(self, obj=None, **kwargs):
        """Initialize a complete DPDA."""
        if isinstance(obj, PDA):
            self._init_from_pda(obj)
        else:
            self._init_from_formal_params(**kwargs)

    def _init_from_pda(self, pda):
        """Initialize this PDA as a deep copy of the given PDA."""
        self.__init__(
            states=pda.states, input_symbols=pda.input_symbols,
            stack_symbols=pda.stack_symbols, transitions=pda.transitions,
            initial_state=pda.initial_state,
            initial_stack_symbol=pda.initial_stack_symbol,
            final_states=pda.final_states)

    def _init_from_formal_params(self, states, input_symbols, stack_symbols,
                                 transitions, initial_state,
                                 initial_stack_symbol, final_states):
        """Initialize a PDA from the formal definition parameters."""
        self.states = states.copy()
        self.input_symbols = input_symbols.copy()
        self.stack_symbols = stack_symbols.copy()
        self.transitions = copy.deepcopy(transitions)
        self.initial_state = initial_state
        self.initial_stack_symbol = initial_stack_symbol
        self.final_states = final_states.copy()
        self.validate_self()

    def _validate_transition_invalid_symbols(self, start_state, paths):
        """Raise an error if transition symbols are invalid."""
        self._validate_transition_invalid_state(start_state)
        for input_symbol, symbol_paths in paths.items():
            self._validate_transition_invalid_input_symbols(
                start_state, input_symbol)
            for symbol_path in symbol_paths:
                for stack_symbol, (new_state, new_stack) in symbol_path.items():
                    self._validate_transition_invalid_stack_symbols(
                        start_state, stack_symbol)
                    self._validate_transition_invalid_state(new_state)
                    for stack_symbol in new_stack:
                        self._validate_transition_invalid_stack_symbols(
                            start_state, stack_symbol)

    def _validate_transition_invalid_state(self, state):
        """Raise an error if state are invalid."""
        if state not in self.states:
            raise exceptions.InvalidStateError(
                'state {} does not exist'.format(
                    state))

    def _validate_transition_invalid_input_symbols(self, start_state,
                                                   input_symbol):
        """Raise an error if transition input symbols are invalid."""
        if input_symbol not in self.input_symbols and input_symbol != '':
            raise exceptions.InvalidSymbolError(
                'state {} has invalid transition input symbol {}'.format(
                    start_state, input_symbol))

    def _validate_transition_invalid_stack_symbols(self, start_state,
                                                   stack_symbol):
        """Raise an error if transition stack symbols are invalid."""
        if stack_symbol not in self.stack_symbols:
            raise exceptions.InvalidSymbolError(
                'state {} has invalid transition stack symbol {}'.format(
                    start_state, stack_symbol))

    def _validate_initial_stack_symbol(self):
        """Raise an error if initial stack symbol is invalid."""
        if self.initial_stack_symbol not in self.stack_symbols:
            raise exceptions.InvalidSymbolError(
                'initial stack symbol {} is invalid'.format(
                    self.initial_stack_symbol))

    def validate_self(self):
        """Return True if this DPDA is internally consistent."""
        for start_state, paths in self.transitions.items():
            self._validate_transition_invalid_symbols(start_state, paths)
        self._validate_initial_state()
        self._validate_initial_stack_symbol()
        self._validate_final_states()
        return True

    def validate_input(self, input_str):
        """
        Check if the given string is accepted by this PDA via BFS algorithm.
        """
        states = deque([(self.initial_state,
                         PDAStack([self.initial_stack_symbol]), 0)])
        visited = set()

        while len(states) > 0:
            state, stack, index = states.popleft()
            visited.add((state, stack, index))

            if index == len(input_str) and state in self.final_states:
                return True

            if len(stack) == 0:
                continue

            if index > len(input_str):
                continue

            stack_symbol = stack.top()

            # check lambda transitions
            if state in self.transitions and '' in self.transitions[state]:
                for path in self.transitions[state]['']:
                    if stack_symbol in path:
                        new_stack = stack.copy()
                        new_state, new_stack_top = path[stack_symbol]
                        new_stack.replace(new_stack_top)

                        if (new_state, new_stack, index) not in visited:
                            states.append((new_state, new_stack, index))

            if index == len(input_str):
                continue
            input_symbol = input_str[index]

            # check all-but-lambda transitions
            if (state in self.transitions and
                    input_symbol in self.transitions[state]):
                for path in self.transitions[state][input_symbol]:
                    if stack_symbol in path:
                        new_stack = stack.copy()
                        new_state, new_stack_top = path[stack_symbol]
                        new_stack.replace(new_stack_top)

                        if (new_state, new_stack, index+1) not in visited:
                            states.append((new_state, new_stack, index+1))

        return False
