from src.strategies.metadata_aggregator import data_sets, methods, generators


def register_strategy(name, data) -> None:  # TODO make types for all functions
    data_sets.update({name: data})


def register_method(name, data) -> None:  # TODO make types for all functions
    methods.update({name: data})


def register_generator(name, data) -> None:  # TODO make types for all functions
    generators.update({name: data})