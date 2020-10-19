from kraken.filesystem.local.local_filesystem import LocalFileSystem

from ...filesystem.ioutils import FileSystemError
from .thrift.ttypes import FileContent
from .thrift.ttypes import FileContentOrNull
from .thrift.ttypes import FileStatus
from .thrift.ttypes import FileStatusOrNull
from .thrift.ttypes import FileSystemException


class LocalFileSystemHandler(object):
    def __init__(self):
        self.fs = LocalFileSystem()
        self.file_descs = {}

    def start(self):
        pass

    def stop(self):
        for file in self.file_descs.values():
            file.close()

    def ls(self, path, status, glob):
        try:
            _list = self.fs.list(path, status, glob)
        except Exception as e:
            raise FileSystemException(str(e))
        if not status:
            return [FileStatusOrNull(path=path) for path in _list]
        else:
            return [
                FileStatusOrNull(
                    path=st[0],
                    status=FileStatus(
                        fileId=str(st[1]["fileId"]),
                        length=str(st[1]["length"]),
                        type=str(st[1]["type"]),
                        modificationTime=str(st[1]["modificationTime"]),
                    ),
                )
                for st in _list
            ]

    def status(self, path, strict):
        try:
            status = self.fs.status(path, False)
        except Exception as e:
            raise FileSystemException(str(e))
        if status is None:
            if strict:
                raise FileSystemException("File %s does not exist" % path)
            else:
                return FileStatusOrNull(path=path)
        else:
            return FileStatusOrNull(
                path=path,
                status=FileStatus(
                    fileId=str(status["fileId"]),
                    length=str(status["length"]),
                    type=str(status["type"]),
                    modificationTime=str(status["modificationTime"]),
                ),
            )

    def content(self, path, strict):
        try:
            content = self.fs.content(path, False)
        except Exception as e:
            raise FileSystemException(str(e))
        if content is None:
            if strict:
                raise FileSystemException("File %s does not exist" % path)
            else:
                return FileContentOrNull(path=path)
        else:
            return FileContentOrNull(
                path=path,
                content=FileContent(
                    length=str(content["length"]),
                    fileCount=str(content["fileCount"]),
                    directoryCount=str(content["directoryCount"]),
                ),
            )

    def rm(self, path, recursive):
        try:
            self.fs.delete(path, recursive)
        except FileSystemError:
            raise FileSystemException("File %s does not exist" % path)
        except Exception as e:
            raise FileSystemException(str(e))

    def rename(self, src_path, dst_path):
        try:
            self.fs.rename(src_path, dst_path)
        except Exception as e:
            raise FileSystemException(str(e))

    def set_owner(self, path, owner, group):
        try:
            self.fs.set_owner(path, owner, group)
        except Exception as e:
            raise FileSystemException(str(e))

    def set_permission(self, path, permission):
        try:
            self.fs.set_permission(path, permission)
        except Exception as e:
            raise FileSystemException(str(e))

    def mkdir(self, path, permission):
        try:
            self.fs.mkdir(path, permission)
        except Exception as e:
            raise FileSystemException(str(e))

    def open(self, path, mode):
        if "b" not in mode:
            mode += "b"
        try:
            file = self.fs.open(path=path, mode=mode)
        except Exception as e:
            raise FileSystemException(str(e))
        desc = str(file.fileno())
        self.file_descs[desc] = file
        return desc

    def flush(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            file.flush()
        except Exception as e:
            raise FileSystemException(str(e))

    def close(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            file.close()
        except Exception as e:
            raise FileSystemException(str(e))
        self.file_descs.pop(filedesc)

    def read(self, filedesc, size):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.read(size)
        except Exception as e:
            raise FileSystemException(str(e))

    def readline(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.readline()
        except Exception as e:
            raise FileSystemException(str(e))

    def readlines(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.readlines()
        except Exception as e:
            raise FileSystemException(str(e))

    def write(self, filedesc, data):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.write(data)
        except Exception as e:
            raise FileSystemException(str(e))

    def writelines(self, filedesc, lines):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.writelines(lines)
        except Exception as e:
            raise FileSystemException(str(e))

    def tell(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.tell()
        except Exception as e:
            raise FileSystemException(str(e))

    def seek(self, filedesc, position):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.seek(position)
        except Exception as e:
            raise FileSystemException(str(e))

    def readable(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]

        try:
            return file.readable()
        except Exception as e:
            raise FileSystemException(str(e))

    def writable(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.writable()
        except Exception as e:
            raise FileSystemException(str(e))

    def seekable(self, filedesc):
        if filedesc not in self.file_descs:
            raise FileSystemException(
                "No such file descriptor %s, is the file open !" % filedesc
            )
        file = self.file_descs[filedesc]
        try:
            return file.seekable()
        except Exception as e:
            raise FileSystemException(str(e))
