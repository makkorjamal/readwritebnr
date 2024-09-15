import ctypes as c
import numpy as np
import os

libc = c.CDLL("libc.so.6")
class HeaderStruct(c.Structure):
    _fields_ = [("HEADER", c.c_char * 80),
                ("WSTART", c.c_double),
                ("WSTOP", c.c_double),
                ("DELW", c.c_double),
                ("LENGTH", c.c_int)
                ]


libc.fread.argtypes = [c.POINTER(HeaderStruct), c.c_size_t, c.c_size_t, 
                       c.c_void_p]
libc.fwrite.argtypes = [c.POINTER(HeaderStruct), c.c_size_t, c.c_size_t, 
                       c.c_void_p]
libc.fread.restype = c.c_size_t
libc.fwrite.restype = c.c_size_t
libc.fopen.argtypes = [c.c_char_p, c.c_char_p]
libc.fopen.restype = c.c_void_p  
libc.fclose.argtypes = [c.c_void_p]  
libc.fclose.restype = c.c_int
libc.fseek.restype = c.c_int
libc.fseek.argtypes = (c.c_void_p,c.c_long, c.c_int)

def read_bnr(filename):
    bnrdata = HeaderStruct()
    try:
        f = libc.fopen(filename.encode(), b"rb")
        if not f:
            raise FileNotFoundError(f"Could not open file: {filename}")

        libc.fread(c.byref(bnrdata), c.sizeof(bnrdata), 1, f)
        length = bnrdata.LENGTH
        data = (c.c_float * length)()
        if libc.fseek(f, c.sizeof(bnrdata), os.SEEK_SET) != 0:
            libc.fclose(f)
            raise IOError("fseek to {} failed".format(file_offset))
        libc.fread.argtypes = (c.c_void_p, c.c_size_t, c.c_size_t, c.c_void_p)
        libc.fread.restype = c.c_size_t
        libc.fread(c.addressof(data), length, 1, f)
        bnrdata.DATA = data # Add data field after knowing the length
        libc.fclose(f)
    except Exception as e:
        libc.fclose(f)
        print(e)
        return None
    return bnrdata

def write_bnr(filename, bnrdata):
    f = libc.fopen(filename.encode(), b"wb")
    if not f:
        raise ValueError(f"Could not open file: {filename}")

    libc.fwrite(c.byref(bnrdata), c.sizeof(bnrdata), 1, f)
    data = bnrdata.DATA
    if libc.fseek(f, c.sizeof(bnrdata), os.SEEK_SET) != 0:
        libc.fclose(f)
        raise IOError("fseek to {} failed".format(file_offset))
    libc.fwrite.argtypes = (c.c_void_p, c.c_size_t, c.c_size_t, c.c_void_p)
    libc.fwrite.restype = c.c_size_t
    libc.fwrite(c.addressof(data), bnrdata.LENGTH, 1, f)
    libc.fclose(f)
    print('File written successfully.')

pyData = read_bnr("101543.bnr")
write_bnr("written.bnr", pyData)
bnrData = read_bnr("written.bnr")
print(np.array_equal(np.asarray(pyData.DATA), np.asarray(bnrData.DATA)))
