"""
Path     PyPoE/poe/file/idl.py
Name     .idl File Format
Version  1.0.0a0
Revision $Id$
Author   [#OMEGA]- K2

INFO

File Format handler for Grinding Gear Games' .idl format.


AGREEMENT

See PyPoE/LICENSE


TODO

...
"""

# =============================================================================
# Imports
# =============================================================================

# Python
import re

# self
from PyPoE.shared.containers import Record, TypedList, TypedContainerMeta

# =============================================================================
# Globals
# =============================================================================

__all__ = ['IDLRecord', 'IDLFile']

# =============================================================================
# Classes
# =============================================================================

class IDLRecord(Record):
    __slots__ = ['destination', 'source', 'x1', 'y1', 'x2', 'y2']

    def __init__(self, destination, source, x1, y1, x2, y2):
        self.destination = destination
        self.source = source
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def __str__(self):
        return '"%s" "%s" %i %i %i %i' % (
            self.destination,
            self.source,
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        )


class IDLFile(TypedList, metaclass=TypedContainerMeta):

    ACCEPTED_TYPES = IDLRecord

    _regex_parse = re.compile(
        r'^'
        r'"(?P<destination>[\w\./_]+)"[ ]+'
        r'"(?P<source>[\w\./_]+)"[ ]+'
        r'(?P<x1>[0-9]+)[ ]+'
        r'(?P<y1>[0-9]+)[ ]+'
        r'(?P<x2>[0-9]+)[ ]+'
        r'(?P<y2>[0-9]+)[ ]*'
        r'$',
        re.UNICODE | re.MULTILINE
    )

    def __init__(self):
        list.__init__(self)

    def read(self, path):
        # Reset
        list.__init__(self)

        with open(path, 'r') as f:
            data = f.read()

        for match in self._regex_parse.finditer(data):
            self.append(IDLRecord(**match.groupdict()))

    def write(self, path):
        lines = []
        for record in self:
            lines.append(str(record))
            lines.append('\n')

        with open(path, 'w') as f:
            f.writelines(lines)