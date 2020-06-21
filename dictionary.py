from enum import Enum
import re

class ReleaseTrack(Enum):
    OTHER      = 0
    CLASSIC    = 1
    INDEV      = 2
    INFDEV     = 3
    ALPHA      = 4
    BETA       = 5
    RELEASE    = 6
    SNAPSHOT   = 7
    PRERELEASE = 8
    APRILFOOL  = 9



class Version:
    track = ReleaseTrack.OTHER
    major = 0
    minor = 0
    revision = 0
    mcmeta_format = -1
    date = 0
    
    def __init__(self, track, major, minor, revision):
        self.track = track
        self.major = major
        self.minor = minor
        self.revision = revision
    
    def __init__(self, track, major, minor, revision, mcmeta_format):
        self.track = track
        self.major = major
        self.minor = minor
        self.revision = revision
        self.mcmeta_format = mcmeta_format
    
    def __init__(self, track, version_string):
        self.track = track
        

def get_resourcepack_format_from_version(v):
    if (v.track == ReleaseTrack.SNAPSHOT):
        v = v.getNearestRelease()
    if ((not v.track == ReleaseTrack.RELEASE) or (not v.major == 1) or (v.minor < 6)):
        return -1
    if (v.minor in (6,7,8)):
        return 1
    if (v.minor in (9,10)):
        return 2
    if (v.minor in (11,12)):
        return 3
    if (v.minor in (13,14)):
        return 4
    if (v.minor in (15,16)):
        return 5
    return -1
