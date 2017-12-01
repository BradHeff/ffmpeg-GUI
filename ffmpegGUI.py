#!/usr/bin/env python3
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from os.path import basename

aspectRatio = ["16:9", "1.85", "2.40"]

res16_9 = ["1920x1080", "1280x720", "720x406"]
res1_85 = ["1920x1038", "1280x692", "720x388"]
res2_40 = ["1920x801", "1280x534", "720x300"]

Profiles = ["high", "main", "baseline"]
high = ["4.2", "4.1", "4.0"]
main = ["4.0", "3.1"]
baseline = ["3.1", "3.0"]

Audio = ["aac", "libmp3lame"]

TERMINAL = "gnome-terminal" # <-- Change to your terminal name if needed.

PID = 0


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="x264 Ripper GUI")
        self.set_resizable(False)
        self.set_icon_from_file('icon.png')
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.vbox)

# =====================================================================================================================
        #ListBox 1
        self.listview1 = Gtk.ListBox()
        self.listview1.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview1, True, True, 0)

        #ListRow 1
        self.listRow1 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow1.add(self.hbox1)

        #ListRow 1 Elements
        self.label1 = Gtk.Label("Auto Close", xalign=0)
        self.switch = Gtk.Switch()
        self.switch.set_active(True)

        self.hbox1.pack_start(self.label1, True, True, 0)
        self.hbox1.pack_start(self.switch, False, False, 0)
        self.listview1.add(self.listRow1)

# =====================================================================================================================
        # ListBox 2
        self.listview2 = Gtk.ListBox()
        self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview2, True, True, 0)

        # ListRow 1
        self.listRow1 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow1.add(self.hbox1)

        # ListRow 1 Elements
        self.label2 = Gtk.Label("In File", xalign=0)
        self.textbox1 = Gtk.Entry()
        self.button1 = Gtk.Button(label="...")
        self.button1.connect("clicked", self.on_button_open_clicked)

        self.hbox1.pack_start(self.label2, True, True, 0)
        self.hbox1.pack_start(self.textbox1, False, False, 0)
        self.hbox1.pack_start(self.button1, False, False, 0)
        self.listview2.add(self.listRow1)

        #==============================================================
        # ListRow 2
        self.listRow2 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow2.add(self.hbox1)

        # ListRow 2 Elements
        self.label3 = Gtk.Label("Out File", xalign=0)
        self.textbox2 = Gtk.Entry()
        self.button2 = Gtk.Button(label="...")
        self.button2.connect("clicked", self.on_button_save_clicked)

        self.hbox1.pack_start(self.label3, True, True, 0)
        self.hbox1.pack_start(self.textbox2, False, False, 0)
        self.hbox1.pack_start(self.button2, False, False, 0)
        self.listview2.add(self.listRow2)

# =====================================================================================================================
        # ListBox 3
        self.listview3 = Gtk.ListBox()
        self.listview3.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview3, True, True, 0)

        # ListRow 1
        self.listRow3 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow3.add(self.hbox1)

        # ListRow 1 Elements
        self.label4 = Gtk.Label("Aspect Ratio", xalign=0)
        self.comboAspect = Gtk.ComboBoxText()
        self.comboAspect.set_size_request(100, 0)
        for aspect in aspectRatio:
            self.comboAspect.append_text(aspect)
        self.comboAspect.set_active(0)

        self.hbox1.pack_start(self.label4, True, True, 0)
        self.hbox1.pack_start(self.comboAspect, False, False, 0)
        self.listview3.add(self.listRow3)

        # ==============================================================
        # ListRow 2
        self.listRow4 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow4.add(self.hbox1)

        # ListRow 1 Elements
        self.label5 = Gtk.Label("Resolution", xalign=0)
        self.comboRes = Gtk.ComboBoxText()
        self.comboRes.set_size_request(100,0)
        for res in res16_9:
            self.comboRes.append_text(res)
        self.comboRes.set_active(0)

        self.hbox1.pack_start(self.label5, True, True, 0)
        self.hbox1.pack_start(self.comboRes, False, False, 0)
        self.listview3.add(self.listRow4)

        self.comboAspect.connect("changed", self.on_aspect_changed)

# =====================================================================================================================
        # ListBox profile
        self.listview_profile = Gtk.ListBox()
        self.listview_profile.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview_profile, True, True, 0)

        # ListRow 1
        self.listRow8 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow8.add(self.hbox1)

        # ListRow 1 Elements
        self.label9 = Gtk.Label("x264 Profile", xalign=0)
        self.comboProfile = Gtk.ComboBoxText()
        self.comboProfile.set_size_request(100, 0)
        for profile in Profiles:
            self.comboProfile.append_text(profile)
        self.comboProfile.set_active(0)

        self.hbox1.pack_start(self.label9, True, True, 0)
        self.hbox1.pack_start(self.comboProfile, False, False, 0)
        self.listview_profile.add(self.listRow8)

        # ==============================================================
        # ListRow 2
        self.listRow9 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow9.add(self.hbox1)

        # ListRow 1 Elements
        self.label10 = Gtk.Label("Profile Level", xalign=0)
        self.comboLevel = Gtk.ComboBoxText()
        self.comboLevel.set_size_request(100, 0)
        for level in high:
            self.comboLevel.append_text(level)
        self.comboLevel.set_active(0)

        self.hbox1.pack_start(self.label10, True, True, 0)
        self.hbox1.pack_start(self.comboLevel, False, False, 0)
        self.listview_profile.add(self.listRow9)

        self.comboProfile.connect("changed", self.on_profile_change)
# =====================================================================================================================
        # ListBox 4
        self.listview4 = Gtk.ListBox()
        self.listview4.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview4, True, True, 0)

        # ListRow 1
        self.listRow5 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow5.add(self.hbox1)

        # ListRow 1 Elements
        self.label6 = Gtk.Label("Audio Format", xalign=0)
        self.comboAudio = Gtk.ComboBoxText()
        self.comboAudio.set_size_request(100, 0)
        for audio in Audio:
            self.comboAudio.append_text(audio)
        self.comboAudio.set_active(0)

        self.hbox1.pack_start(self.label6, True, True, 0)
        self.hbox1.pack_start(self.comboAudio, False, False, 0)
        self.listview4.add(self.listRow5)

# =====================================================================================================================
        # ListBox 5
        self.listview5 = Gtk.ListBox()
        self.listview5.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listview5, True, True, 0)

        # ListRow 1
        self.listRow6 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow6.add(self.hbox1)

        # ListRow 1 Elements
        self.label7 = Gtk.Label("Video Bitrate", xalign=0)
        self.textbox3 = Gtk.Entry()
        self.textbox3.set_size_request(80, 0)
        self.textbox3.set_text("1800")

        self.hbox1.pack_start(self.label7, True, True, 0)
        self.hbox1.pack_start(self.textbox3, False, False, 0)
        self.listview5.add(self.listRow6)

        #=========================================================================
        # ListRow 2
        self.listRow7 = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRow7.add(self.hbox1)

        # ListRow 1 Elements
        self.label8 = Gtk.Label("Audio Bitrate (kbps)", xalign=0)
        self.textbox4 = Gtk.Entry()
        self.textbox4.set_size_request(80, 0)
        self.textbox4.set_text("128")

        self.hbox1.pack_start(self.label8, True, True, 0)
        self.hbox1.pack_start(self.textbox4, False, False, 0)
        self.listview5.add(self.listRow7)

        self.comboAudio.connect("changed", self.on_audio_changed)
#=====================================================================================================================
        # ListBox BTM
        self.listviewBTM = Gtk.ListBox()
        self.listviewBTM.set_selection_mode(Gtk.SelectionMode.NONE)
        self.vbox.pack_start(self.listviewBTM, True, True, 0)

        # ListRow 1
        self.listRowBTM = Gtk.ListBoxRow()
        self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.listRowBTM.add(self.hbox1)

        # ListRow 1 Elements
        self.labelBTM = Gtk.Label("Calculate ffmpeg GUI", xalign=0)
        self.buttonBTM = Gtk.Button(label="RUN")
        self.buttonBTM.connect("clicked", self.on_buttonBTM_changed)

        self.hbox1.pack_start(self.labelBTM, True, True, 0)
        self.hbox1.pack_start(self.buttonBTM, False, False, 0)
        self.listviewBTM.add(self.listRowBTM)

    def on_button_open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file",
                                       self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filter = Gtk.FileFilter()
        filter.set_name("VIDEO Files")
        filter.add_mime_type("video/x-msvideo")
        filter.add_mime_type("video/msvideo")
        filter.add_mime_type("video/avi")
        filter.add_mime_type("video/x-matroska")
        filter.add_mime_type("video/mpeg")
        filter.add_mime_type("video/mp4")
        dialog.set_filter(filter)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            #print("Open clicked")
            self.textbox1.set_text(dialog.get_filename())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            #print("Cancel clicked")
            dialog.destroy()

    def on_button_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file",
                                       self, Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # print("Save clicked")
            filename = dialog.get_filename()
            if ".mp4" in filename:
                self.textbox2.set_text(filename)
            else:
                self.textbox2.set_text(filename + ".mp4")
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            # print("Cancel clicked")
            dialog.destroy()

    def on_audio_changed(self, combo):
        text = combo.get_active_text()
        if text == "aac":
            self.textbox4.set_text("128")
        elif text == "libmp3lame":
            self.textbox4.set_text("320")

    def on_aspect_changed(self, combo):
        text = combo.get_active_text()
        if text == "16:9":
            self.comboRes.get_model().clear()
            for res in res16_9:
                self.comboRes.append_text(res)
            self.comboRes.set_active(0)
        elif text == "1.85":
            self.comboRes.get_model().clear()
            for res in res1_85:
                self.comboRes.append_text(res)
            self.comboRes.set_active(0)
        elif text == "2.40":
            self.comboRes.get_model().clear()
            for res in res2_40:
                self.comboRes.append_text(res)
            self.comboRes.set_active(0)

    def on_profile_change(self, combo):
        text = combo.get_active_text()
        if text == "high":
            self.comboLevel.get_model().clear()
            for level in high:
                self.comboLevel.append_text(level)
            self.comboLevel.set_active(0)
        elif text == "main":
            self.comboLevel.get_model().clear()
            for level in main:
                self.comboLevel.append_text(level)
            self.comboLevel.set_active(0)
        elif text == "baseline":
            self.comboLevel.get_model().clear()
            for level in baseline:
                self.comboLevel.append_text(level)
            self.comboLevel.set_active(0)

    def on_buttonBTM_changed(self, widget):
        if not self.checkBoxes():
            md = Gtk.MessageDialog(self,
                                   0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Infile or Outfile missing")
            md.format_secondary_text(
                "Both fields need to be filled for the encoder to work")

            md.run()
            md.destroy()
            print("In File or Out File not selected.")
            return False

        self.set_sensitive(False)
        filename = basename(self.textbox2.get_text())

        aCodec = "aac"
        if self.comboAudio.get_active_text() == "libmp3lame":
            aCodec = "libmp3lame -qscale:a 2"

        command = "ffmpeg -i '" + self.textbox1.get_text() + "' -metadata title='" + filename + "' -vf scale=" + \
                  self.comboRes.get_active_text() + \
                  " -aspect " + self.comboAspect.get_active_text() + " -acodec " \
                  + aCodec + " -b:a " + self.textbox4.get_text() + "k -vcodec mpeg4 -b:v " + \
                  self.textbox3.get_text() + "K -c:v libx264 -profile:v " + self.comboProfile.get_active_text() + \
                  " -level " + self.comboLevel.get_active_text() + " '" + self.textbox2.get_text() + "'"

        p = subprocess.Popen([TERMINAL, "--command=" + command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        PID = p.pid
        print(PID)

        if self.switch.get_active():
            Gtk.main_quit(0)
        else:
            self.set_sensitive(True)

    def checkBoxes(self):
        if self.textbox1.get_text() == "":
            return False
        elif self.textbox2.get_text() == "":
            return False
        else:
            return True


if __name__ == '__main__':
    window = MainWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
