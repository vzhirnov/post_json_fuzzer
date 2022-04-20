import pytest

from src.core.parser.view import parser_view


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
        ('+', ['+']), ('++', ['+', '+']), ('+++', ['+', '+', '+']), ('|', ['|']), ('||', ['|', '|']),
        ('|||', ['|', '|', '|']), ('Îäíàæäû', ['Îäíàæäû']), ('Ǽ1', ['Ǽ1']),

  # must not detect
        ('_', ['_']),  # TODO what to do with this case?
        ('#', []), (';', []), ('\n', []), ('None', ['None']), ('True', ['True']), ('False', ['False']), ('[]', ['[]']),
        ('[][]', ['[]', '[]']), ('[][][]', ['[]', '[]', '[]']), ('[]|', ['[]', '|']), ('|[]|', ['|', '[]', '|']),
        ('+|', ['+', '|']),
        ('|+|', ['|', '+', '|']),

  # ('*', ['*']),  TODO: check in combinations with other elems within DSL
        ('1', ['1']),
        (
            '1623761273615273651762351726357162357162357162357162537165237162537615237615273651726351726176235716357162357162',
            [
                '1623761273615273651762351726357162357162357162357162537165237162537615237615273651726351726176235716357162357162'
            ]
        ), ('-1', ['-1']),
        (
            '-1623761273615273651762351726357162357162357162357162537165237162537615237615273651726351726176235716357162357162',
            [
                '-1623761273615273651762351726357162357162357162357162537165237162537615237615273651726351726176235716357162357162'
            ]
        ), ('0.1', ['0.1']), ('-0.1', ['-0.1']), ('1, 2', ['1', '2']), ('1, -2', ['1', '-2']), ('(1, 2)', ['1', '2']),
        ('(1, 2, 3)', ['1', '2', '3']), ('(-1, -2)', ['-1', '-2']), ('(-1, -2, -3)', ['-1', '-2', '-3']),
        ("('1', '+')", ['1', '+']), ("('+', '1')", ['+', '1']), ("('+1', '1')", ['+', '1', '1']),
        ("('A', 'B')", ['A', 'B']), ("('Aa', 'Ab')", ['Aa', 'Ab']), ("('a', 'b')", ['a', 'b']),
        ("('test1', 'TEST2')", ['test1', 'TEST2']), ("('a + b')", ['a', '+', 'b']), ("('ab+')", ['ab', '+']),
        ("('a', 'b+')", ['a', 'b', '+']), ("('a', 'b', '+')", ['a', 'b', '+']),
        ("('a - b')", ['a', '-', 'b']),  # TODO think what to do with minus
        ('Check_1', ['Check_1']), ('["1"]', ['["1"]']), ('["One"]', ['["One"]']), ('["One_1"]', ['["One_1"]']),
        ('[1]', ['[1]']), ("[132, 1]", ["[132, 1]"]), ("['132', 1]", ["['132', 1]"]),
        (
            "('100', 1, None, True, False, -0.1, 0.1, [], [1], '+', '|)",
            ['100', '1', 'None', 'True', 'False', '-0.1', '0.1', '[]', '[1]', '+', '|']
        ), ('[["1"]]', ['[["1"]]']),  # TODO losing square bracket as in cases below \|/
        ('[[]]', ['[[]]']), ('[["test"]]', ['[["test"]]']), ('["1", "2"]', ['["1", "2"]']),
        ('["1", "A"]', ['["1", "A"]']), ('{}', ['{}']), ('{"a": 1}', ['{"a": 1}']), ('{"a": []}', ['{"a": []}']),
        ('{"a": [True, 1]}', ['{"a": [True, 1]}']),
        ('{"a": [True, 1, "a", {1: 1}]}', ['{"a": [True, 1, "a", {1: 1}]}']),
        ('{"a": [1, {1: 1}, {1: 1}]}', ['{"a": [1, {1: 1}, {1: 1}]}']),
        (
            "'1','#STRATEGY#default$', '+', '#FUNC#MUTATE_IT#mutate$'",
            ['1', '#STRATEGY#default$', '+', '#FUNC#MUTATE_IT#mutate$']
        ), ("'1','#FUNC#LIST_IT#2$'", ['1', '#FUNC#LIST_IT#2$']),
    ]
)
def test_check_parser_view(pattern: str, expected_result: list) -> None:
    assert parser_view(pattern) == expected_result
