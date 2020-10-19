#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class TaskType(object):
    COPY = 1
    UPLOAD = 2
    MOCK = 3

    _VALUES_TO_NAMES = {
        1: "COPY",
        2: "UPLOAD",
        3: "MOCK",
    }

    _NAMES_TO_VALUES = {
        "COPY": 1,
        "UPLOAD": 2,
        "MOCK": 3,
    }


class WorkerStatus(object):
    """
    Attributes:
     - wid
     - running
     - pending
     - available

    """


    def __init__(self, wid=None, running=None, pending=None, available=None,):
        self.wid = wid
        self.running = running
        self.pending = pending
        self.available = available

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.wid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.running = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.pending = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.available = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('WorkerStatus')
        if self.wid is not None:
            oprot.writeFieldBegin('wid', TType.STRING, 1)
            oprot.writeString(self.wid.encode('utf-8') if sys.version_info[0] == 2 else self.wid)
            oprot.writeFieldEnd()
        if self.running is not None:
            oprot.writeFieldBegin('running', TType.I32, 2)
            oprot.writeI32(self.running)
            oprot.writeFieldEnd()
        if self.pending is not None:
            oprot.writeFieldBegin('pending', TType.I32, 3)
            oprot.writeI32(self.pending)
            oprot.writeFieldEnd()
        if self.available is not None:
            oprot.writeFieldBegin('available', TType.I32, 4)
            oprot.writeI32(self.available)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Task(object):
    """
    Attributes:
     - tid
     - type
     - params

    """


    def __init__(self, tid=None, type=None, params=None,):
        self.tid = tid
        self.type = type
        self.params = params

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.tid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.type = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.MAP:
                    self.params = {}
                    (_ktype1, _vtype2, _size0) = iprot.readMapBegin()
                    for _i4 in range(_size0):
                        _key5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val6 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.params[_key5] = _val6
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Task')
        if self.tid is not None:
            oprot.writeFieldBegin('tid', TType.STRING, 1)
            oprot.writeString(self.tid.encode('utf-8') if sys.version_info[0] == 2 else self.tid)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.I32, 2)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        if self.params is not None:
            oprot.writeFieldBegin('params', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.params))
            for kiter7, viter8 in self.params.items():
                oprot.writeString(kiter7.encode('utf-8') if sys.version_info[0] == 2 else kiter7)
                oprot.writeString(viter8.encode('utf-8') if sys.version_info[0] == 2 else viter8)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.tid is None:
            raise TProtocolException(message='Required field tid is unset!')
        if self.type is None:
            raise TProtocolException(message='Required field type is unset!')
        if self.params is None:
            raise TProtocolException(message='Required field params is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class FileSystem(object):
    """
    Attributes:
     - name
     - parameters

    """


    def __init__(self, name=None, parameters=None,):
        self.name = name
        self.parameters = parameters

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.MAP:
                    self.parameters = {}
                    (_ktype10, _vtype11, _size9) = iprot.readMapBegin()
                    for _i13 in range(_size9):
                        _key14 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val15 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.parameters[_key14] = _val15
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('FileSystem')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.parameters is not None:
            oprot.writeFieldBegin('parameters', TType.MAP, 2)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.parameters))
            for kiter16, viter17 in self.parameters.items():
                oprot.writeString(kiter16.encode('utf-8') if sys.version_info[0] == 2 else kiter16)
                oprot.writeString(viter17.encode('utf-8') if sys.version_info[0] == 2 else viter17)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.name is None:
            raise TProtocolException(message='Required field name is unset!')
        if self.parameters is None:
            raise TProtocolException(message='Required field parameters is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(WorkerStatus)
WorkerStatus.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'wid', 'UTF8', None, ),  # 1
    (2, TType.I32, 'running', None, None, ),  # 2
    (3, TType.I32, 'pending', None, None, ),  # 3
    (4, TType.I32, 'available', None, None, ),  # 4
)
all_structs.append(Task)
Task.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'tid', 'UTF8', None, ),  # 1
    (2, TType.I32, 'type', None, None, ),  # 2
    (3, TType.MAP, 'params', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 3
)
all_structs.append(FileSystem)
FileSystem.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
    (2, TType.MAP, 'parameters', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 2
)
fix_spec(all_structs)
del all_structs
