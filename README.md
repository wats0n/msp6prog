##msp6prog - Minispartan6+ Configure Tool

This is a side-project on `Windows` for understanding the interaction between `FT2232H` and `Spartan6` FPGA. msp6prog use `JTAG` as FPGA configuration interface.
  * GUI interface on Windows implemented by wxPython.
  * Control hardware msp6prog.dll build from Visual C++ 2008 Express.
    * Using FTDI API (ftdXX.dll).
  * Tested on Win7 x64 with Minispartan6+ [6SLX9].
This tool would to be useful, but may not comprehensive for all condition.

I wish it could be ready Flash Programming function for the course
`6.004.2x Computation Structures: Programmable Architectures` on edX.org.
I want to implement the programmable architecture on Minispartan6+.

But there is no clear schedule to accomplish it.

##How to use?

######Pre-requirement:
* 1. Intall driver `CDM v2.12.00 WHQL Certified.exe`
  * from http://www.ftdichip.com/Drivers/D2XX.htm
* 2. Check only one FT2232H Device (Minispartan6+) plug on the USB.

####Easy Way:
* 1. Download packed executable: [msp6prog_v0.1_win32.7z](https://github.com/wats0n/msp6prog/releases/download/v0.1_freeze/msp6prog_v0.1_win32.7z)
* 2. Extract and execute msp6prog.exe
* 3. Select Bitstream file and wait finish information on console.
![MSP6 Example](/images/msp6prog_v0.1_usecase.png)

**Hard Way:**
* 1. Ready Python 2.7 Environment, needs:
  * Python 2.7, python-2.7.9_x86.msi
  * wxPython for py27, wxPython3.0-win32-3.0.2.0-py27.exe
* 2. Download below files in same folder:
  * msp6prog.py - Main procedure, wxPython and ctypes heavily been used in here. 
  * msp6para.py - Default parameter to call low-level function in msp6prog.dll
  * msp6info.py - Display information for msp6prog.py
  * msp6prog.dll - low-level control function for FT2232H, send JTAG interface message.
  * ftd2xx.dll - FTDI support APIs for FT2232H.
* 3. Execute msp6prog.py in console or IDLE to invoke window.

*Very Hard Way:*
* 1. Download DLL source file: [msp6prog_dll_src_v0.1.7z](./msp6prog_dll_src/msp6prog_dll_src_v0.1.7z?raw=true)
* 2. Review and figure how to compile to dll or exe.
* 3. if you need default parameter for msp6prog, trace msp6para.py .
* 4. Rewrite new operation for FPGA by JTAG Interface.
* 5. I build DLL on Visual C++ 2008 Express.

##Software Structure

![MSP6 Structure](/images/msp6prog_v0.1_structurediagram.png)

* Python - Main process system
  * wxPython - Windows GUI Interface
  * ctypes - Access C program DLL
  * os - write information to console window
* msp6prog.dll - low-level control DLL
  * jtag_blankinterrogation - Set FPGA to Test-Logic-Reset (JTAG State) to read FPGA IDCODE.
  * jtag_cfgfpga - Configure FPGA by CFG_IN IR command and bitstream.
  * con_init - initial console window to log process.
  * con_cls - clear console window screen.

* msp6para.py - all parameters related to msp6prog.dll
  * dctrlcmd_t - catalog commands for FT2232H by bit/byte operation.
    * bycmd - byte operation command
    * bicmd - bit operation command
  * jtagpara_t - FT2232H and JTAG preferences
    * handle - FT2232H ID in Windows hardware management system
    * freq - Frequency setting by Hz, default set 30000000 (30M) Hz.
    * devidx - Device Index, default set 0 in v0.1.
    * cmd_tms - FT2232H MPSSE command to control JTAG TMS(Test Mode Select) signal.
    * ir - FT2232H MPSSE command for IR(Instruction Register) operation
    * drlo - FT2232H MPSSE command for DR(Data Register) LSB first Output operation
    * drli - FT2232H MPSSE command for DR(Data Register) LSB first Input operation
    * drmo - FT2232H MPSSE command for DR(Data Register) MSB first Output operation
    * drmi - FT2232H MPSSE command for DR(Data Register) MSB first Input operation
  * ircmd_t - JTAG IR command parameters.
    * cmd - Command value by Xilinx ug380 Table 10-2
    * tckdly - TCK(Test Clock) delay for FPGA internal operation.
    * name - Command name define in Xilinx ug380 Table 10-2
  * fpgajcmd_t - FPGA JTAG Command List
    * ir_len - IR length (bits) by ug380 Table 10-2
    * dr_stride - DR data packet maxinum size (byte)
      * form 1 to 0xFFFF by FTDI AN_108
    * cmdlist - IR command list in array, see ircmd_list in msp6para.py.
  * fpgapara_t - FPGA Properties, see fpga_arr in msp6para.py.
    * name - FPGA Name in Xilinx ug380 Table 5-13
    * idcode - FPGA IDCODE by Xilinx ug380 Table 5-13
    * maxbits - FPGA configure size for readback, no usage yet.
    * jcmd - JTAG command define in fpgajcmd_t.

FPGA Configuration is done, but Flash Programming is another problem.

##Useful Reference

####Xilinx Spartan 6
  * Spartan-6 FPGA Configuration User Guide (UG380)
    * Chapter 3: Boundary-Scan and JTAG Configuration
    * Chapter 10: Advanced JTAG Configurations
    * **Figure 10-2: Boundary-Scan TAP Controller**
    * **Table 10-2: Spartan-6 FPGA Boundary-Scan Instructions**
    * **Table 5-13: ID Codes**
    * **Table 10-4: Single Device Configuration Sequence**
    * **Figure 10-1: Typical JTAG Architecture**
    * Table 5-5: Spartan-6 FPGA Bitstream Length
    * Table 6-5: Status Register Readback Command Sequence (JTAG)
  * Bitstream File Format
    * http://www.fpga-faq.com/FAQ_Pages/0026_Tell_me_about_bit_files.htm
    
####FT2232H
  * AN_129_FTDI_Hi_Speed_USB_To_JTAG_Example.pdf
  * AN_135_MPSSE_Basics.pdf
  * AN_108_Command_Processor_for_MPSSE_and_MCU_Host_Bus_Emulation_Modes.pdf
  * D2XX_Programmer's_Guide(FT_000071).pdf
  * http://www.ftdichip.com/Support/SoftwareExamples/MPSSE.htm#JTAG0
    * Good start point form this example.
    
####JTAG
  * http://www.fpga4fun.com/JTAG.html
    * Very very useful for newbie like me.
    
####FPGA Course
  * http://hamsterworks.co.nz/mediawiki/index.php/Main_Page
  * http://hamsterworks.co.nz/mediawiki/index.php/MiniSpartan6%2B_bringup
    * I have verified function by this wiki `ledtest` project.

##Development Task List
- [x] FPGA Configuration
- [ ] Flash Programming
  * reference: http://www.scarabhardware.com/forums/topic/boot-from-on-board-spi-flash/

##License
I choose MIT License for free to use this program.
Because I think the most important for programming is algorithm design and data structure arrangement.
Good document and specification should contain these information, not only in the codes.
So I wish most developer could share thinking as clear as possible, so I share how to do on this project in detail.