import sys
from ctypes import *


def import_api(root):
    try:
        if sys.platform.startswith('win32'):
            libEDK = cdll.LoadLibrary(root + "/bin/win32/edk.dll")
        elif sys.platform.startswith('linux'):
            if platform.machine().startswith('arm'):
                libPath = root + "/bin/armhf/libedk.so"
            else:
                libPath = root + "/bin/linux64/libedk.so"
            libEdk = CDLL(libPath)
        if sys.platform.startswith('darwin'):
            libEDK = cdll.LoadLibrary(root + '/lib/mac/edk.framework/edk')
        else:
            raise Exception('System not supported.')
    except Exception as e:
        print('Error: cannot load EDK lib:', e)
        exit(0)
    return libEDK
