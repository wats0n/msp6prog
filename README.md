##msp6prog - Minispartan6+ Configure Tool

This is a side-project for understanding the interaction between `FT2232H` and `Spartan6` FPGA.
msp6prog use `JTAG` as configuration interface for FPGA.
Program support a GUI interface under windows system by wxPython.
Tested on Win7 x64 with Minispartan6+ [6SLX9].
This tool would to be useful, but may not comprehensive for all condition.

##How to use?

Pre-requirement:
* 1. Intall driver from http://www.ftdichip.com/Drivers/D2XX.htm
* 2. Check only one FT2232H Device (Minispartan6+) plug on the USB.

####Easy Way:
* 1. Download packed executable: [msp6prog_v0.1_win32.7z](./win32_executable/msp6prog_v0.1_win32.7z?raw=true)
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
  
Contact FPGA is done, but Flash is another problem.

##Useful Reference

####Xilinx Spartan 6
  * Spartan-6 FPGA Configuration User Guide (UG380)
    * Chapter 3: Boundary-Scan and JTAG Configuration
    * Chapter 10: Advanced JTAG Configurations
    * **Figure 10-2: Boundary-Scan TAP Controller**
    * **Table 10-2: Spartan-6 FPGA Boundary-Scan Instructions**
    * **Table 5-13: ID Codes**
    * **Table 10-4: Single Device Configuration Sequence**
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
    *Good start point form this example.
    
####JTAG
  * http://www.fpga4fun.com/JTAG.html
    *Very very useful for newbie like me.
    
####FPGA Course
  * http://hamsterworks.co.nz/mediawiki/index.php/Main_Page
  * http://hamsterworks.co.nz/mediawiki/index.php/MiniSpartan6%2B_bringup
    *I am testing my program function by this ledtest project.

##License

I choose MIT License for free to use this program.
Because I think the most important for programming is algorithm design and data structure arrangement.
Good document and specification should contain these information, not only in the codes.
So I wish most developer could share thinking as clear as possible, so I share how to do on this project in detail.