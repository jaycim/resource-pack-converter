"""dictionary.py: aims to provide a comprehensive dictionary to translate data between all minecraft versions."""

__author__    = "Nicholas Cline"
__license__   = "GNU GPL v3.0"

import sys
from enum import Enum
import json

VERSION_LOOKUP_FAILED_GENERIC  = 100
VERSION_LOOKUP_FAILED_KEYERROR = 101

versions = json.load(open("versions.json"))["versions"]

class ReleaseTrack(Enum):
    OTHER       = 0b0000000000
    CLASSIC     = 0b0000000001
    INDEV       = 0b0000000010
    INFDEV      = 0b0000000100
    ALPHA       = 0b0000001000
    BETA        = 0b0000010000
    RELEASE     = 0b0000100000
    SNAPSHOT    = 0b0001000000
    PRERELEASE  = 0b0010000000
    APRILFOOL   = 0b0100000000

def get_version(version_string):
    try:
        return versions[version_string]
    except(KeyError):
        sys.exit(1)

def get_version(track, major, minor, revision, build=0):
    if (track == ReleaseTrack.RELEASE):
        try:
            suffix = ""
            if (not revision == 0):
                suffix = ".{}".format(revision)
            return versions["{}.{}".format(major,minor)+suffix]
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track == ReleaseTrack.BETA):
        try:
            suffix = ""
            if (not revision == 0):
                suffix = ".{}".format(revision)
            return versions["b{}.{}".format(major,minor)+suffix]
        except(KeyError):
            try:
                return versions["b{}.{}_0{}".format(major,minor,revision)]
            except(KeyError):
                sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track == ReleaseTrack.ALPHA):
        try:
            suffix = ""
            if (not build == 0):
                suffix = "_0{}".format(build)
            return versions["a{}.{}.{}".format(major,minor,revision)+suffix]
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track & ReleaseTrack.PRERELEASE > 0):
        try:
            prefix = ""
            suffix = ""
            if (track & ReleaseTrack.BETA > 0):
                prefix="b"
            if (not revision == 0):
                suffix = str(revision)
            return versions[prefix+"{}.{}-pre".format(major,minor)+suffix]
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track == ReleaseTrack.SNAPSHOT):
        try:
            return versions["{}w{}{}".format(major,minor,revision)] #yeah this seems gross
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track == ReleaseTrack.CLASSIC):
        try:
            suffix = ""
            if (not revision == 0):
                if (not build == 0):
                    suffix = ".{}_0{}".format(revision,build)
                else:
                    suffix = ".{}".format(revision)
            return versions["c{}.{}".format(major,minor)+suffix]
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track == ReleaseTrack.INFDEV):
        try:
            return versions["inf{}{}{}".format(major,minor,revision)] #also gross
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
    if (track == ReleaseTrack.INDEV or track == ReleaseTrack.APRILFOOL):
        sys.exit(VERSION_LOOKUP_FAILED_GENERIC) #we are not currently tracking any indev or aprilfool versions
    if (track == ReleaseTrack.OTHER):
        try:
            return versions["rd-{}".format(major)] #in this case there's no obvious breakup of the numbers so just using first argument after track
        except(KeyError):
            sys.exit(VERSION_LOOKUP_FAILED_KEYERROR)
