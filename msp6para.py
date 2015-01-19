'''
//----------------------------------------------------------------------------
// Name:        msp6para.py
// Purpose:     Default parameters for msp6prog.dll.
//
// Author:      Watson Huang <wats0n.edx@gmail.com>
//
// Created:     01/19, 2015
// Copyright:   (c) 2015 by Watson Huang
// License:     MIT License
//----------------------------------------------------------------------------
'''

import ctypes

#reference nest structure
#http://www.sagemath.org/doc/numerical_sage/ctypes_examples.html

class dctrlcmd_t(ctypes.Structure):
    _fields_ = [("bycmd", ctypes.c_ubyte),
                ("bicmd", ctypes.c_ubyte)]

class jtagpara_t(ctypes.Structure):
    _fields_ = [("handle", ctypes.c_void_p),
                ("freq", ctypes.c_uint),
                ("devidx", ctypes.c_uint),
                ("cmd_tms", ctypes.c_ubyte),
                ("ir", dctrlcmd_t),
                ("drlo", dctrlcmd_t),
                ("drli", dctrlcmd_t),
                ("drmo", dctrlcmd_t),
                ("drmi", dctrlcmd_t)]

class ircmd_t(ctypes.Structure):
    _fields_ = [("cmd", ctypes.c_uint),
                ("tckdly", ctypes.c_uint),
                ("name", ctypes.c_char_p)]

class fpgajcmd_t(ctypes.Structure):
    _fields_ = [("ir_len", ctypes.c_uint),
                ("dr_stride", ctypes.c_uint),
                ("cmdlist", ctypes.POINTER(ircmd_t))]

class fpgapara_t(ctypes.Structure):
    _fields_ = [("name", ctypes.c_char_p),
                ("idcode", ctypes.c_uint),
                ("maxbits", ctypes.c_uint),
                ("jcmd", ctypes.POINTER(fpgajcmd_t))]

#declare nest structure
jtagpara = jtagpara_t( 0,
                       30000000,
                       0,
                       0x4B,
                       (0x19, 0x1B),
                       (0x19, 0x1B),
                       (0x2C, 0x2E),
                       (0x11, 0x13),
                       (0x24, 0x26));
#declare array
#http://python.net/crew/theller/ctypes/tutorial.html#arrays
#first declare an array class, then set real variable
ircmd_arr7 = (ircmd_t * 7); #ircmd_t ircmd_list[7];
ircmd_list = ircmd_arr7((0x09, 0, "IDCODE"),
                        (0x05, 0, "CFGIN"),
                        (0x04, 0, "CFGOUT"),
                        (0x0C, 16, "JSTART"),
                        (0x0B, 24, "JPROGRAM"),
                        (0x0D, 24, "JSHUTDOWN"),
                        (0, 0, None));
# ctypes.cast(ircmd_list, ctypes.POINTER(ircmd_t)) for transforming array to poiner
#ctypes.POINTER() use for class
#ctypes.pointer() use for object
fpga_cmd = fpgajcmd_t( 6,
                       0xFFFF,
                       ctypes.cast(ircmd_list, ctypes.POINTER(ircmd_t)));

fpgapara_arr4 = (fpgapara_t * 4);
#one object use ctypes.byref
fpga_arr = fpgapara_arr4(("6SLX9", 0x4001093, 2742528, ctypes.pointer(fpga_cmd)),
                         ("6SLX25", 0x4004093, 6440432, ctypes.pointer(fpga_cmd)),
                         ("6SLX25T", 0x4004093, 6440432, ctypes.pointer(fpga_cmd)),
                         (None, 0, 0, None))

#Configure FPGA Parameters
fpga_list = ctypes.cast(fpga_arr, ctypes.POINTER(fpgapara_t));
cur_fpga = fpgapara_t(None, 0, 0, None); #Current Use FPGA, Detect by DLL 'jtag_blankinterrogation' function
