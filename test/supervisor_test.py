import pytest

from time import sleep

from pyrlang import Node
from pyrlang.process import Process
from pyrlang.gen.server import GenServer
from pyrlang.supervisor import Supervisor, _is_child_spec
from term import Atom

node_name_ = "py@127.0.0.1"
node_ = Node(node_name=node_name_, cookie="COOKIE")


@pytest.mark.parametrize("child_spec, expected", [
    ({
        'id': 'Test',
        'start': Process(node_name_),
        'restart': Atom('force'),
        'shutdown': 1
    }, True),
    ({
        'id': Atom('Test'),
        'start': Process(node_name_),
        'restart': Atom('force'),
        'shutdown': 1
    }, True),
    ({
        'id': Atom('Test'),
        'start': GenServer(),
        'restart': Atom('force'),
        'shutdown': 1
    }, True),
    ({
        'id': 1,
        'start': Process(node_name_),
        'restart': Atom('force'),
        'shutdown': 1
    }, False),
    ({
        'id': 'Test',
        'start': node_name_,
        'restart': Atom('force'),
        'shutdown': 1
    }, False),
    ({
        'id': 'Test',
        'start': Process(node_name_),
        'restart': 'force',
        'shutdown': 1
    }, False),
    ({
        'id': 'Test',
        'start': Process(node_name_),
        'restart': Atom('force'),
        'shutdown': '1'
    }, False),
    (['id', 'start', 'restart', 'shutdown'], False),
])
def test_is_child_spec(child_spec, expected):
    assert _is_child_spec(child_spec) == expected


def test_supervisor_instantiate():
    child_spec = {
        'id': 'Test',
        'start': Process(node_name_),
        'restart': Atom('force'),
        'shutdown': 1
    }
    sup = Supervisor([child_spec])
    assert len(sup._childs) == 1
