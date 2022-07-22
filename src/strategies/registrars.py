from src.strategies.aggregator import data_sets, methods, generators


def register_strategy(name: str, data) -> None:
    data_sets.update({name: data})


def register_method(name: str, data) -> None:
    methods.update({name: data})


def register_generator(name: str, data) -> None:
    generators.update({name: data})
