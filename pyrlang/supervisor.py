# Copyright 2018, Erlang Solutions Ltd, and S2HC Sweden AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from typing import Callable, List, Tuple, Dict

from pyrlang.process import Process
from pyrlang.gen.server import GenServer
from pyrlang.gen.decorators import call as main_call
from pyrlang.util import as_str
from term.atom import Atom
from term.pid import Pid

LOG = logging.getLogger("pyrlang.supervisor")

CHILD_SPEC_REF = {
    'id': [Atom, str],
    'start': [Process, GenServer],
    'restart': [Atom],
    'shutdown': [Atom, int],
}


def call(name, msg_len=2):
    """ specific decorator function

        Handle the decorator where we expect a tuple of a specific size and
        the first item being an atom with specific name
    """
    atom = Atom(name)

    def pattern_match(msg):
        if type(msg) != tuple:
            return False
        if len(msg) != msg_len:
            return False
        if msg[0] != atom:
            return False
        return True

    return main_call(pattern_match)


def _is_child_spec(child_spec):
    if not isinstance(child_spec, dict):
        return False
    else:
        return all([
            key_ in CHILD_SPEC_REF.keys()
            and type(child_spec[key_]) in CHILD_SPEC_REF[key_]
            for key_ in child_spec.keys()
        ])


class Supervisor(GenServer):
    def __init__(self, child_specs: list, sup_flags: dict):
        self.state = 'init'
        super().__init__()
        self._childs = {}
        for child_spec in child_specs:
            if _is_child_spec(child_spec):
                self.start_child(child_spec)

    # Process graceful exit
    @call('exit')
    def sv_exit(self, msg):
        pass

    # Process dead
    @call('exit2')
    def sv_exit2(self, msg):
        pass

    def start_child(self, child_spec):
        self._start_child(child_spec)

    def stop_child(self, child_id):
        pass

    def restart_child(self, child_id):
        pass

    def terminate_child(self, child_id):
        pass

    def which_childern(self):
        pass

    def get_childspec(self):
        pass

    def _monitor_child(self, child_id):
        pass
