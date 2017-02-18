#!/usr/bin/env python2
"""Exception classes for PDA."""


class AutomatonError(Exception):
    """The base class for all automaton-related errors."""

    pass


class InvalidStateError(AutomatonError):
    """A state is not a valid state for this automaton."""

    pass


class InvalidSymbolError(AutomatonError):
    """A symbol is not a valid symbol for this automaton."""

    pass


class MissingStateError(AutomatonError):
    """A state is missing from the automaton definition."""

    pass


class MissingSymbolError(AutomatonError):
    """A symbol is missing from the automaton definition."""

    pass


class InitialStateError(AutomatonError):
    """The initial state fails to meet some required condition."""

    pass


class FinalStateError(AutomatonError):
    """A final state fails to meet some required condition."""

    pass


class RejectionError(AutomatonError):
    """The input was rejected by the automaton after validation."""

    pass


class PDAError(AutomatonError):
    """The base class for all PDA-related errors."""

    pass
