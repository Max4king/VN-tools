from datetime import datetime
from struct import unpack
from pprint import pformat
from typing import Tuple, Dict


DEFAULT_CHARSET = 'cp1251'
_SIGNATURE = b'L\x00\x00\x00'
_GUID = b'\x01\x14\x02\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00F'
_LINK_FLAGS = (
    'HasLinkTargetIDList',
    'HasLinkInfo',
    'HasName',
    'HasRelativePath',
    'HasWorkingDir',
    'HasArguments',
    'HasIconLocation',
    'IsUnicode',
    'ForceNoLinkInfo',
    # new
    'HasExpString',
    'RunInSeparateProcess',
    'Unused1',
    'HasDarwinID',
    'RunAsUser',
    'HasExpIcon',
    'NoPidlAlias',
    'Unused2',
    'RunWithShimLayer',
    'ForceNoLinkTrack',
    'EnableTargetMetadata',
    'DisableLinkPathTracking',
    'DisableKnownFolderTracking',
    'DisableKnownFolderAlias',
    'AllowLinkToLink',
    'UnaliasOnSave',
    'PreferEnvironmentPath',
    'KeepLocalIDListForUNCTarget',
)


# ---- only read binary data

def read_int(buf):
    return unpack('<I', buf.read(4))[0]


def read_cstring(buf, padding=False):
    s = b""
    b = buf.read(1)
    while b != b'\x00' and b != b'':
        s += b
        b = buf.read(1)
    if padding and not len(s) % 2:
        buf.read(1)  # make length + terminator even
    return s.decode(DEFAULT_CHARSET)



def assert_lnk_signature(f):
    f.seek(0)
    sig = f.read(4)
    guid = f.read(16)
    if sig != _SIGNATURE:
        raise FormatException("This is not a .lnk file.")
    if guid != _GUID:
        raise FormatException("Cannot read this kind of .lnk file.")

def convert_time_to_unix(windows_time):
    # Windows time is specified as the number of 0.1 nanoseconds since January 1, 1601.
    # UNIX time is specified as the number of seconds since January 1, 1970.
    # There are 134774 days (or 11644473600 seconds) between these dates.
    unix_time = windows_time / 10000000.0 - 11644473600
    try:
        return datetime.fromtimestamp(unix_time)
    except OSError:
        return datetime.now()

class FormatException(Exception):
    pass

class Flags(object):
    
    def __init__(self, flag_names: Tuple[str, ...], flags_bytes=0):
        self._flag_names = flag_names
        self._flags: Dict[str, bool] = dict([(name, False) for name in flag_names])
        self.set_flags(flags_bytes)
    
    def set_flags(self, flags_bytes):
        for pos, flag_name in enumerate(self._flag_names):
            self._flags[flag_name] = bool(flags_bytes >> pos & 0x1)

    @property
    def bytes(self):
        bytes = 0
        for pos in range(len(self._flag_names)):
            bytes = (self._flags[self._flag_names[pos]] and 1 or 0) << pos | bytes
        return bytes
    
    def __getitem__(self, key):
        if key in self._flags:
            return object.__getattribute__(self, '_flags')[key]
        return object.__getattribute__(self, key)
    
    def __setitem__(self, key, value):
        if key not in self._flags:
            raise KeyError("The key '%s' is not defined for those flags." % key)
        self._flags[key] = value
    
    def __getattr__(self, key):
        if key in self._flags:
            return object.__getattribute__(self, '_flags')[key]
        return object.__getattribute__(self, key)
    
    def __setattr__(self, key, value):
        if '_flags' not in self.__dict__:
            object.__setattr__(self, key, value)
        elif key in self.__dict__:
            object.__setattr__(self, key, value)
        else:
            self.__setitem__(key, value)

    def __str__(self):
        return pformat(self._flags, indent=2)

class LinkInfo(object):
    def __init__(self, lnk=None):
        if lnk is not None:
            self.start = lnk.tell()
            link_info_flags = read_int(lnk)
            self.local = link_info_flags & 1
            self.remote = link_info_flags & 2
            self.offs_local_base_path = read_int(lnk)
            self.offs_base_name = read_int(lnk)
            self._parse_path_elements(lnk)
        else:
            self._path = None

    def _parse_path_elements(self, lnk):
        if self.remote:
            lnk.seek(self.start + self.offs_base_name)
            self.base_name = read_cstring(lnk)
        if self.local:
            lnk.seek(self.start + self.offs_local_base_path)
            self.local_base_path = read_cstring(lnk)
        self.make_path()

    def make_path(self):
        if self.remote:
            self._path = self.base_name
        if self.local:
            self._path = self.local_base_path

    @property
    def path(self):
        return self._path


class Lnk(object):
    def __init__(self, f=None):
        self.file = None
        if type(f) == str or type(f) == str:
            self.file = f
            try:
                f = open(self.file, 'rb')
            except IOError:
                self.file += ".lnk"
                f = open(self.file, 'rb')
        self.link_flags = Flags(_LINK_FLAGS)
        self._link_info = LinkInfo()
        if f is not None:
            assert_lnk_signature(f)
            self._parse_lnk_file(f)
        if self.file:
            f.close()

    def _parse_lnk_file(self, lnk):
        lnk.seek(20)  # after signature and guid
        self.link_flags.set_flags(read_int(lnk))
        if self.link_flags.HasLinkInfo and not self.link_flags.ForceNoLinkInfo:
            self._link_info = LinkInfo(lnk)
            lnk.seek(self._link_info.start + self._link_info.size)

    def _get_link_info(self):
        return self._link_info

    def _set_link_info(self, link_info):
        self._link_info = link_info
        self.link_flags.ForceNoLinkInfo = link_info is None
        self.link_flags.HasLinkInfo = link_info is not None
    link_info = property(_get_link_info, _set_link_info)

    @property
    def path(self):
        link_info_path = self._link_info.path if self._link_info and self._link_info.path else None
        return link_info_path

    def __str__(self):
        return "Used Path: %s" % self.path


def get_lnk_target(lnk_path):
    lnk = Lnk(lnk_path)
    return lnk.target_path()

shortcut_path = "C:\Games\VN\VN-collection\deeper\童貞兄妹.exe - Shortcut.lnk"

ans = get_lnk_target(shortcut_path)
print(ans)