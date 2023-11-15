# import pcbnew
# import wx
# import os

# class KicadAtoAction(pcbnew.ActionPlugin):

#     def defaults(self):
#         self.name = "ato -> kicad"
#         self.category = "Import tools"
#         self.description = "Tools for atopile projects"
#         self.icon_file_name = os.path.join(os.path.dirname(__file__), "./icon.png")
#         self.show_toolbar_button = True

#     def run(self):
#         print("Hello World, from atopile!")
#         dialog = KicadAtoDialog(None)
#         dialog.ShowModal()
#         dialog.Destroy()

# class KicadAtoDialog ( wx.Dialog ):
#     def __init__(self, parent ):
#         wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Fill Area parameters", pos = wx.DefaultPosition, size = wx.Size( 402,590 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

#         self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

#         bSizer3 = wx.BoxSizer( wx.VERTICAL )

#         fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
#         fgSizer1.SetFlexibleDirection( wx.BOTH )
#         fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

#         self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Via copper size (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
#         self.m_staticText3.Wrap( -1 )

#         self.ok_button = wx.Button(self, label='OK')
#         self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

#     def on_ok(self, event):
#         self.Close()

# KicadAtoAction().register()


import pcbnew
import wx
import os

class KicadAtoAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "ato -> kicad"
        self.category = "Import tools"
        self.description = "Tools for atopile projects"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./icon.png")
        self.show_toolbar_button = True

    def run(self):
        print("Running plugin")
        dialog = KicadAtoDialogEx(None)
        result = dialog.ShowModal()
        dialog.Destroy()

class KicadAtoDialog(wx.Dialog):
    def __init__(self, parent):
        print("Initializing dialog")
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Basic Dialog",
                           pos=wx.DefaultPosition, size=wx.Size(200, 200),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.ok_button = wx.Button(self, label='OK')
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

    def on_ok(self, event):
        print("Closing dialog")
        self.Close()

class KicadAtoDialogEx(KicadAtoDialog):

    def onDeleteClick(self, event):
        return self.EndModal(wx.ID_DELETE)

KicadAtoAction().register()