'''
//----------------------------------------------------------------------------
// Name:        msp6info.py
// Purpose:     Information for msp6prog about button.
//
// Author:      Watson Huang <wats0n.edx@gmail.com>
//
// Created:     01/19, 2015
// Copyright:   (c) 2015 by Watson Huang
// License:     MIT License
//----------------------------------------------------------------------------
'''

iname = "MSP6+ Configure Tool";
iversion = "v0.1";

icopyright = "\
(c) 2015 Watson Huang for MSP6+ Configure Tool\n \
(c) Xilinx belong to Xilinx Inc.\n \
(c) FT2232H belong to FTDI Ltd.\n \
(c) MiniSpartan6+ Belong to Scarab Hardware."

iwebsite = ("https://github.com/wats0n/msp6prog", "MSP6+ Configure Tool on Github.com");
ideveloper = ["Watson Huang <wats0n.edx@gmail.com>"]
ilicense = " \
The MIT License (MIT)\n\
Copyright (c) 2015 Watson Huang\n\
Permission is hereby granted, free of charge, to any person obtaining a copy \
of this software and associated documentation files (the \"Software\"), to deal \
in the Software without restriction, including without limitation the rights \
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \
copies of the Software, and to permit persons to whom the Software is \
furnished to do so, subject to the following conditions: \
The above copyright notice and this permission notice shall be included in \
all copies or substantial portions of the Software.\n\
THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN \
THE SOFTWARE.";

idescription = "\
  This program is a side-project for understanding \
how to control FTDI FT2232H to operate Xilinx Spartan6.\
In order to learning and implement the MITx 6.004.2x Computation Structures: Programmable Architectures (2015 Q3).\
Main target is to design a Hi-Speed (USB2.0, 480MBps) interface form computer to Spartan6. \n\
There are three stages: \n\
  1. Configure FPGA via FT2232H.\n\
  2. Program Flash through Spartan6.\n\
  3. Perform Partial Reconfigure with this interface.\n\
Finished stage 1 by follow abstraction:\n\
  1. Implement FT2232H Low-Level programming in DLL by Visual C++ 2008 Express.\n\
  2. Layout window by wxPython and operate DLL by ctypes in Python.\n\
Stage 2 is underway but no clear schedule.\n\
It's done when it's done.\n\
  -wats0n\
";
