'''
//----------------------------------------------------------------------------
// Name:        msp6prog.py
// Purpose:     Make user interface by wxPython for msp6 configure tool.
//              and use ctype to call Low-Level control DLL msp6prog.dll.
//
// Author:      Watson Huang <wats0n.edx@gmail.com>
//
// Created:     01/19, 2015
// Copyright:   (c) 2015 by Watson Huang
// License:     MIT License
//----------------------------------------------------------------------------
'''

import wx
from wx.lib.wordwrap import wordwrap
import os
import ctypes
import win32api

import msp6para
import msp6info

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

class WinFrame(wx.Frame):
    def __init__(
        self, parent, title, ID, pos=wx.DefaultPosition,
        size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        
        self.Frame = wx.Frame.__init__(self, parent, title, ID, pos, size, style);
        
        self.SetBackgroundColour((255, 255, 255));
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #Load ICON from Current Executable
        exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
        self.icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        
        self.vbox = wx.BoxSizer(wx.HORIZONTAL);
        self.cfgfpgabtn = wx.Button(self, -1, "Configure FPGA");
        self.cfgflashbtn = wx.Button(self, -1, "Program Flash");
        self.progabout = wx.Button(self, -1, "About");
        
        self.Bind(wx.EVT_BUTTON, self.OnClickFPGA, self.cfgfpgabtn);
        self.Bind(wx.EVT_BUTTON, self.OnClickFlash, self.cfgflashbtn);
        self.Bind(wx.EVT_BUTTON, self.OnClickAbout, self.progabout);
        
        self.vbox.Add(self.cfgfpgabtn, 0, wx.EXPAND);
        self.vbox.Add(self.cfgflashbtn, 0, wx.EXPAND);
        self.vbox.Add(self.progabout, 0, wx.EXPAND);

        self.vbox.SetSizeHints(self); #Auto Adjust Frame Size
        self.SetSizer(self.vbox);

        #Ready Libraries
        self.kernel32 = ctypes.windll.kernel32;
        self.user32 = ctypes.windll.user32;
        
        try:
            self.hCFGDLL = ctypes.CDLL ("msp6prog.dll");
        except:
            dlg = wx.MessageDialog(self,
                                   'Missing msp6prog.dll!!\nProgram will close Window after press OK.',
                                   'Error!!',
                                   wx.OK | wx.ICON_ERROR);
            dlg.ShowModal()
            dlg.Destroy()
            self.Destroy()
            return; #force exit __init__ process

        self.Show() #show window
        
        #Load Functions
        self.func_coninit = getattr(self.hCFGDLL, "con_init");
        self.func_concls = getattr(self.hCFGDLL, "con_cls");
        self.func_jbi = getattr(self.hCFGDLL, 'jtag_blankinterrogation');
        self.func_jcfg = getattr(self.hCFGDLL, 'jtag_cfgfpga');
        
        #Ready Console Window
        self.hcon = self.func_coninit()     #Console Initialize
        self.func_concls(self.hcon);        #Console Clear Screen
        # CONOUT$ would be available after console initialized
        self.cfd = os.open("CONOUT$", os.O_WRONLY|os.O_TEXT);
        
        #Get Current Fram Position
        fpos = self.GetPosition();
        fsize = self.GetSize();
        #Move Console to moderate position
        self.wcon = self.kernel32.GetConsoleWindow()
        wrect = RECT(0, 0, 0, 0);
        self.user32.GetWindowRect(self.wcon, ctypes.pointer(wrect));
        self.user32.MoveWindow(self.wcon, fpos[0], fpos[1]+fsize[1], wrect.right-wrect.left, wrect.bottom-wrect.top, 1)

        self.cfgflashbtn.Disable(); #Future Function.
        
        #self.Show(); //Show before console.

    def conprint(self, tstr):
        try:
            os.write(self.cfd, tstr);
        except AttributeError:
            pass #do nothing
    
    def OnCloseWindow(self, event):
        self.kernel32.FreeConsole();
        self.Destroy()

    def OnClickAbout(self, event):
        info = wx.AboutDialogInfo()

        info = wx.AboutDialogInfo()
        info.Name = msp6info.iname
        info.Version = msp6info.iversion
        info.Copyright = msp6info.icopyright
        info.Description = wordwrap((msp6info.idescription), 550, wx.ClientDC(self))
        info.WebSite = msp6info.iwebsite
        info.Developers = msp6info.ideveloper
        info.License = wordwrap(msp6info.ilicense, 850, wx.ClientDC(self))

        wx.AboutBox(info)
                
    def OnClickFPGA(self, event):
        self.func_concls(self.hcon);
        #http://stackoverflow.com/questions/8832714/how-to-use-multiple-wildcards-in-python-file-dialog
        wildcard = "Xilinx Bitstream (*.bit)|*.bit"
        
        dlg = wx.FileDialog(
            self, message="Select Xilinx Bitstream file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:

            bitfilename = dlg.GetFilename()
            bitfilepath = dlg.GetPath()

            self.conprint("[Action] Assign Bitstream File: "+ bitfilepath + "\n");
            self.conprint("[Action] Detect FPGA:\n");
            self.func_jbi.restype = ctypes.c_ulong;
            self.func_jbi.argtypes = [ctypes.POINTER(msp6para.jtagpara_t), ctypes.POINTER(msp6para.fpgapara_t), ctypes.POINTER(msp6para.fpgapara_t)]
            self.func_jbi(ctypes.pointer(msp6para.jtagpara), msp6para.fpga_list, ctypes.pointer(msp6para.cur_fpga));
            self.conprint("[Action] Analysis Bitstream and Configure FPGA:\n");
            self.func_jcfg.restype = ctypes.c_ulong;
            self.func_jcfg.argtypes = [ctypes.POINTER(msp6para.jtagpara_t), ctypes.POINTER(msp6para.fpgapara_t), ctypes.c_char_p]
            self.func_jcfg(ctypes.pointer(msp6para.jtagpara), ctypes.pointer(msp6para.cur_fpga), bitfilepath);
            self.conprint("[Finish] Configure FPGA by " + bitfilename +" Done.\n");
        
    def OnClickFlash(self, event):
        pass #to be done

    
if __name__ == '__main__':
    #start app
    app = wx.App();
    winframe = WinFrame(None, -1, "MSP6+ Configure Tool",
                        pos = (120, 120) ,size = (300, 100),
                        style = wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN);
    app.MainLoop();
