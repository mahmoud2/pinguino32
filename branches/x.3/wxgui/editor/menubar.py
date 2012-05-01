#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""-------------------------------------------------------------------------
    General methos to Pinguino IDE.

    author:		Yeison Cardona
    contact:		yeison.eng@gmail.com
    first release:	02/April/2012
    last release:	03/April/2012

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
-------------------------------------------------------------------------"""

import codecs, sys, os
from wxgui._ import _


HOME_DIR    = sys.path[0]
TEMP_DIR = os.path.join(HOME_DIR, '.temp')

########################################################################
class Menubar:

    #----------------------------------------------------------------------
    def OnNew(self, event):
        self.background.Hide()
        
        #print self.filename
        
        
        file = os.path.join(TEMP_DIR, _("Newfile%d") %self.noname)
        while file + ".pde" in self.filename:
            self.noname += 1
            file = os.path.join(TEMP_DIR, _("Newfile%d") %self.noname)
            
        #self.addFile2Recent(file)
        #print file              
            
        self.New(file)
        self.noname+=1
        self.updatenotebook()

    #----------------------------------------------------------------------
    def OnOpen(self, event):
        self.background.Hide()
        self.OpenDialog("Pde Files",
                        "pde")
        self.updatenotebook()
        self.update_dockFiles()


    #----------------------------------------------------------------------
    def OnSave(self, event=None):
        """ Save file without dialog box """
        if len(self.onglet)>0:
            path=self.filename[self.notebookEditor.GetSelection()]
            fichier=codecs.open(path,'w','utf8')
            for i in range(0,self.stcpage[self.notebookEditor.GetSelection()].GetLineCount()):
                fichier.writelines(self.stcpage[self.notebookEditor.GetSelection()].GetLine(i))
            fichier.close()
            if self.notebookEditor.GetPageText(self.notebookEditor.GetSelection())[0]=="*":
                chaine=self.notebookEditor.GetPageText(self.notebookEditor.GetSelection())
                chaine=chaine[1:len(chaine)]
                self.notebookEditor.SetPageText(self.notebookEditor.GetSelection(),chaine)
            self.stcpage[self.notebookEditor.GetSelection()].SetSavePoint()
           
            self.addFile2Recent(path)
            
            
    #----------------------------------------------------------------------
    def OnSaveAll(self, event=None):
        if len(self.onglet) <= 0: return
        for i in range(len(self.filename)):
            path = self.filename[i]
            fichier=codecs.open(path,'w','utf8')
            for j in range(0,self.stcpage[i].GetLineCount()):
                fichier.writelines(self.stcpage[i].GetLine(j))
            fichier.close()
            if self.notebookEditor.GetPageText(i)[0]=="*":
                chaine=self.notebookEditor.GetPageText(i)
                chaine=chaine[1:len(chaine)]
                self.notebookEditor.SetPageText(i,chaine)
            self.stcpage[i].SetSavePoint()
            self.addFile2Recent(path)

    #----------------------------------------------------------------------
    def OnSaveAs(self, event):
        self.Save("Pde Files","pde")

    #----------------------------------------------------------------------
    def OnClose(self, event):
        self.CloseTab()
        self.updatenotebook()
        self.update_dockFiles()
        
    #----------------------------------------------------------------------
    def OnCloseAll(self, event):
        while self.CloseTab():
            self.updatenotebook()
            self.update_dockFiles()

    #----------------------------------------------------------------------
    def OnCopy(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].Copy()

    #----------------------------------------------------------------------
    def OnPaste(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].Paste()

    #----------------------------------------------------------------------
    def OnCut(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].Cut()

    #----------------------------------------------------------------------
    def OnClear(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].Clear()

    #----------------------------------------------------------------------
    def OnUndo(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].Undo()

    #----------------------------------------------------------------------
    def OnRedo(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].Redo()

    #----------------------------------------------------------------------
    def OnSelectall(self, event):
        self.stcpage[self.notebookEditor.GetSelection()].SelectAll()

    #----------------------------------------------------------------------
    def OnComment(self, event=None):
        textEdit = self.stcpage[self.notebookEditor.GetSelection()]
        lineStart, lineEnd = map(textEdit.LineFromPosition,textEdit.GetSelection())
        countLines = lineEnd - lineStart
        posLineStart, posLineEnd = map(textEdit.PositionFromLine, [lineStart, lineEnd+1])
        textEdit.SetSelection(posLineStart, posLineEnd)
        selected = textEdit.GetSelectedText()
        if selected.startswith("//"): comented = selected.replace("//","")
        else: comented = "//" + selected.replace("\n","\n//", countLines)
        textEdit.Clear()
        textEdit.InsertText(textEdit.CurrentPos, comented)
        textEdit.SetSelection(*map(textEdit.PositionFromLine, [lineStart, lineEnd]))
        
        
    #----------------------------------------------------------------------
    def OnIndent(self, event=None):
        textEdit = self.stcpage[self.notebookEditor.GetSelection()]
        lineStart, lineEnd = map(textEdit.LineFromPosition,textEdit.GetSelection())
        countLines = lineEnd - lineStart
        posLineStart, posLineEnd = map(textEdit.PositionFromLine, [lineStart, lineEnd+1])
        textEdit.SetSelection(posLineStart, posLineEnd)
        selected = textEdit.GetSelectedText()
        indent = "\t" + selected.replace("\n","\n\t", countLines)
        textEdit.Clear()
        textEdit.InsertText(textEdit.CurrentPos, indent)
        textEdit.SetSelection(*map(textEdit.PositionFromLine, [lineStart, lineEnd]))
        
    #----------------------------------------------------------------------
    def OnUnIndent(self, event=None):
        textEdit = self.stcpage[self.notebookEditor.GetSelection()]
        lineStart, lineEnd = map(textEdit.LineFromPosition,textEdit.GetSelection())
        countLines = lineEnd - lineStart
        posLineStart, posLineEnd = map(textEdit.PositionFromLine, [lineStart, lineEnd+1])
        textEdit.SetSelection(posLineStart, posLineEnd)
        selected = textEdit.GetSelectedText()
        if str(selected.split("\n")[0]).startswith("\t"):
            indent = selected.replace("\t", "", 1).replace("\n\t", "\n", countLines)
            textEdit.Clear()
            textEdit.InsertText(textEdit.CurrentPos, indent)
            textEdit.SetSelection(*map(textEdit.PositionFromLine, [lineStart, lineEnd]))
        

    #----------------------------------------------------------------------
    def OnExit(self, event):

        self.closing = True  #Signal for Threads

        try:
            self.pinguino.close()
            fclose(self.debug_handle)
        except: pass
        
        w, h = self.GetSize()
        self.setConfig("IDE", "Window/Width", w)
        self.setConfig("IDE", "Window/Height", h)
        
        x, y = self.GetPosition()
        self.setConfig("IDE", "Window/Xpos", x)
        self.setConfig("IDE", "Window/Ypos", y)
        
        
        w, h = self.logwindow.GetSize()
        self.setConfig("IDE", "Output/Width", w)
        self.setConfig("IDE", "Output/Height", h)
        
        
        
        i = 0
        self.setConfig("Recents", "Recents_count", len(self.recentsFiles))
        for file in self.recentsFiles:
            try: file = unicode(file).encode("utf-8")
            except: pass
            self.setConfig("Recents", "Recents_%d" %i, file)
            i += 1
            
            
        i = 0
        self.setConfig("Last", "Last_count", len(self.filename))
        for file in self.filename:
            try: file = unicode(file).encode("utf-8")
            except: pass          
            self.setConfig("Last", "Last_%d" %i, file)
            i += 1
        
            
        
        self.setConfig("IDE", "Theme", self.theme)
        
        self.setConfig("IDE","Board", self.curBoard.name)
        
        self.saveConfig()

        ## ---save settings-----------------------------------------------
        ##if not self.IsIconized() and not self.IsMaximized():
        #w, h = self.GetSize()
        #self.config.WriteInt('Window/Width', w)
        #self.config.WriteInt('Window/Height', h)
        ##self.config.WriteInt("frame/sashposition", self.splitterWindow1.GetSashPosition())
        ##x, y = self.GetPosition()
        ##self.config.WriteInt('Window/Posx', x)
        ##self.config.WriteInt('Window/Posy', y)

        #w, h = self.logwindow.GetSize()
        #self.config.WriteInt('Output/Width', w)
        #self.config.WriteInt('Output/Height', h)

        #i = 0
        #self.config.WriteInt("LastEdit/count", len(self.filename))
        #for file in self.filename:
            #self.config.Write("LastEdit/file%d" %i, file)
            #i += 1

        ##for t in self.themeList:
        ##	tid = self.theme_menu.FindItem(t)
        ##	if self.theme_menu.IsChecked(tid):
        #self.config.Write('Theme/name', self.theme)

        ##Save the last files in the editor
        ##for b in range(len(self.boardlist)):
            ##bid = self.boardlist[b].id
            ##if self.board_menu.IsChecked(bid):
                ##self.config.WriteInt('Board', bid)
        #self.config.WriteInt('Board', self.curBoard.id)
                
        

        ##if DEV:
            ##for d in range(self.ID_ENDDEBUG - self.ID_DEBUG - 1):
                ##did = self.ID_DEBUG + d + 1
                ##if self.menu.menuDebugMode.IsChecked(did):
                    ##self.config.WriteInt('Debug', did)

        #self.config.Flush()

        # ----------------------------------------------------------------------
        # deinitialize the frame manager
        self._mgr.UnInit()
        # delete the frame
        self.Destroy()
        sys.exit(0)

    #----------------------------------------------------------------------
    def OnViewTools(self, event):
        pane = self._mgr.GetPane(self.lat)  # wxAuiPaneInfo
        if self.menu.menuItemTools.IsChecked():
            pane.Show()
        else:
            pane.Hide()
        self.updateIDE()

    #----------------------------------------------------------------------
    def OnViewOutput(self, event):
        pane = self._mgr.GetPane(self.panelOutput)  # wxAuiPaneInfo
        if self.menu.menuItemOutput.IsChecked():
            pane.Show()
        else:
            pane.Hide()
        self.updateIDE()

    #----------------------------------------------------------------------
    def OnViewToolbar(self, event):
        if self.menu.menuItemToolbar.IsChecked():
            self.DrawToolbar()
            #self.toolbar.Show()
        else:
            self.toolbar.Destroy()
        self.updateIDE()