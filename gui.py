import wx
from wx import adv
from datetime import datetime, date

class InputFrame(wx.Frame):
    """Window for user to input event date and optional time."""
    def __init__(self):
        super().__init__(None, title="Enter Event Date/Time", size=(350, 200))
        panel = wx.Panel(self)

        v = wx.BoxSizer(wx.VERTICAL)

        v.Add(wx.StaticText(panel, label="Select date:"), 0, wx.ALL, 5)
        self.date_picker = adv.DatePickerCtrl(panel)  # date picker control
        v.Add(self.date_picker, 0, wx.ALL | wx.EXPAND, 5)

        v.Add(wx.StaticText(panel, label="Enter time (HH:MM, optional):"), 0, wx.ALL, 5)
        h = wx.BoxSizer(wx.HORIZONTAL)
        self.hour_txt = wx.TextCtrl(panel, size=(40, -1))
        self.min_txt = wx.TextCtrl(panel, size=(40, -1))
        h.Add(self.hour_txt, 0, wx.ALL, 5)
        h.Add(wx.StaticText(panel, label=":"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        h.Add(self.min_txt, 0, wx.ALL, 5)
        v.Add(h, 0, wx.ALL, 5)

        btn = wx.Button(panel, label="Prepare Countdown")
        v.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        panel.SetSizer(v)

        btn.Bind(wx.EVT_BUTTON, self.on_start)

        self.Show()

    def on_start(self, event):
        wx_date = self.date_picker.GetValue()
        py_date = date(
            wx_date.GetYear(),
            wx_date.GetMonth() + 1,   # wx months are zero-based
            wx_date.GetDay()
        )

        hour = 0
        minute = 0
        try:
            h = self.hour_txt.GetValue().strip()
            m = self.min_txt.GetValue().strip()
            if h:
                hour = int(h)
            if m:
                minute = int(m)
        except ValueError:
            wx.MessageBox("Invalid time input. Use HH and MM as integers.", "Error")
            return

        target = datetime(py_date.year, py_date.month, py_date.day, hour, minute, 0)
        now = datetime.now()
        if target <= now:
            wx.MessageBox("Please choose a future date/time.", "Error")
            return

        self.Hide()
        CountdownFrame(target)


class CountdownFrame(wx.Frame):
    """Window that shows the live countdown and has Start / Stop controls."""
    def __init__(self, target_datetime):
        super().__init__(None, title="Countdown Timer", size=(400, 200))
        self.target = target_datetime
        self.timer = wx.Timer(self)

        panel = wx.Panel(self)
        v = wx.BoxSizer(wx.VERTICAL)

        self.time_label = wx.StaticText(panel, label="00:00:00", style=wx.ALIGN_CENTER)
        font = self.time_label.GetFont()
        font.PointSize += 12
        self.time_label.SetFont(font)
        v.Add(self.time_label, 0, wx.ALL | wx.ALIGN_CENTER, 20)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_start = wx.Button(panel, label="Start")
        self.btn_stop = wx.Button(panel, label="Stop")
        btn_sizer.Add(self.btn_start, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.btn_stop, 0, wx.LEFT, 10)
        v.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        panel.SetSizer(v)

        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_start)
        self.btn_stop.Bind(wx.EVT_BUTTON, self.on_stop)

        # Initially, Stop is disabled until we actually start
        self.btn_stop.Disable()

        self.Show()

    def on_start(self, event):
        now = datetime.now()
        if self.target <= now:
            wx.MessageBox("Target time is already passed.", "Error")
            return
        # start timer: 1000 ms = 1 second
        self.timer.Start(1000)
        self.btn_start.Disable()
        self.btn_stop.Enable()

    def on_stop(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        self.btn_stop.Disable()
        self.btn_start.Enable()

    def on_timer(self, event):
        now = datetime.now()
        delta = self.target - now
        total = int(delta.total_seconds())

        if total > 0:
            hrs, rem = divmod(total, 3600)
            mins, secs = divmod(rem, 60)
            self.time_label.SetLabel(f"{hrs:02d}:{mins:02d}:{secs:02d}")
        else:
            self.timer.Stop()
            self.time_label.SetLabel("Time's up!")
            wx.MessageBox("🎉 The event time has been reached!", "Done")
            self.btn_stop.Disable()
            # optionally keep start disabled, or you can let user start again with updated target


if __name__ == "__main__":
    app = wx.App(False)
    InputFrame()
    app.MainLoop()
