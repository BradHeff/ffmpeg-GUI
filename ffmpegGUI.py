#!/usr/bin/env python3

import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject
import threading
import time
import signal


aspectRatio = ["16:9", "1.85", "2.40"]

res16_9 = ["1920x1080", "1280x720", "720x406"]
res1_85 = ["1920x1038", "1280x692", "720x388"]
res2_40 = ["1920x801", "1280x534", "720x300"]

vcodecs = ["x264", "x264_lossless", "x265", "x265_lossless", "matroska"]

x265_profiles = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
x264_profiles = ["high", "main", "baseline"]

high = ["4.2", "4.1", "4.0"]
main = ["4.0", "3.1"]
baseline = ["3.1", "3.0"]

MP4_Acodecs = ["aac", "mp3", "ac3"]
MKV_Acodecs = ["aac", "mp3", "ac3", "vorbis", "opus"]

bit = ["8bit", "10bit", "12bit"]

SYSTERMS = ["urxvt", "xfce4-terminal", "gnome-terminal", "xterm", "terminator", "tilda", 
"lxterminal", "konsole", "st"]

error = 0;

base_dir = os.path.dirname(os.path.realpath(__file__))

class ffmpegGUI(Gtk.Window):
	
	def __init__(self):
		super(ffmpegGUI, self).__init__()
		Gtk.Window.__init__(self, title="HEFFS FFMPEG GUI")
		self.set_resizable(False)
		self.set_border_width(10)
		self.set_icon_from_file(os.path.join(base_dir, 'icon.png'))
		self.set_position(Gtk.WindowPosition.CENTER)

		#===========================================
		#				Main Container				
		#===========================================
		
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(self.vbox)

		#===========================================
		#				HEADER Section				
		#=========================================== 
		self.listviewHDR = Gtk.ListBox()
		self.listviewHDR.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listviewHDR, True, True, 0)

		#ListRow 1
		self.listRowHDR = Gtk.ListBoxRow()
		self.hboxHDR = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRowHDR.add(self.hboxHDR)

		#ListRow 1 Elements
		self.image = Gtk.Image()
		self.image.set_from_file(os.path.join(base_dir, 'logo.png'))
		self.image_area = Gtk.Box()
		self.image_area.add(self.image)
		self.image_area.show_all()

		self.hboxHDR.pack_start(self.image_area, True, True, 0)		
		self.listviewHDR.add(self.listRowHDR)

		#===========================================
		#				1st Section				
		#=========================================== 
		self.listview1 = Gtk.ListBox()
		self.listview1.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listview1, True, True, 0)

		#ListRow 1
		self.listRow1 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow1.add(self.hbox1)

		#ListRow 1 Elements
		self.label1 = Gtk.Label(xalign=0)
		self.label1.set_text("Auto Close")
		self.switch = Gtk.Switch()
		self.switch.set_active(True)

		self.hbox1.pack_start(self.label1, True, True, 0)
		self.hbox1.pack_start(self.switch, False, False, 0)
		self.listview1.add(self.listRow1)

		#===========================================
		#				TERM Section				
		#=========================================== 
		self.listviewTERM = Gtk.ListBox()
		self.listviewTERM.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listviewTERM, True, True, 0)

		#ListRow 1
		self.listRowTERM = Gtk.ListBoxRow()
		self.hbox1TERM = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRowTERM.add(self.hbox1TERM)

		#ListRow 1 Elements
		self.labelTERM = Gtk.Label(xalign=0)
		self.labelTERM.set_text("Terminal")
		self.comboTERM = Gtk.ComboBoxText()
		self.comboTERM.set_size_request(170, 0)
		for TERM in SYSTERMS:
			self.comboTERM.append_text(TERM)
		self.comboTERM.set_active(0)

		self.hbox1TERM.pack_start(self.labelTERM, True, True, 0)
		self.hbox1TERM.pack_start(self.comboTERM, False, False, 0)
		self.listviewTERM.add(self.listRowTERM)

		#===========================================
		#				2nd Section				
		#=========================================== 
		self.listview2 = Gtk.ListBox()
		self.listview2.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listview2, True, True, 0)

		#==================
		#		Row 1				
		#==================
		self.listRow1 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow1.add(self.hbox1)

		# ListRow 1 Elements
		self.label2 = Gtk.Label(xalign=0)
		self.label2.set_text("In File")
		self.textbox1 = Gtk.Entry()
		self.button1 = Gtk.Button(label="...")
		self.button1.connect("clicked", self.on_button_open_clicked)

		self.hbox1.pack_start(self.label2, True, True, 0)
		self.hbox1.pack_start(self.textbox1, False, False, 0)
		self.hbox1.pack_start(self.button1, False, False, 0)
		self.listview2.add(self.listRow1)

		#==================
		#		Row 2				
		#==================
		self.listRow2 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow2.add(self.hbox1)

		# ListRow 2 Elements
		self.label3 = Gtk.Label(xalign=0)
		self.label3.set_text("Out File")
		self.textbox2 = Gtk.Entry()
		self.button2 = Gtk.Button(label="...")
		self.button2.connect("clicked", self.on_button_save_clicked)

		self.hbox1.pack_start(self.label3, True, True, 0)
		self.hbox1.pack_start(self.textbox2, False, False, 0)
		self.hbox1.pack_start(self.button2, False, False, 0)
		self.listview2.add(self.listRow2)


		#===========================================
		#				3rd Section				
		#=========================================== 
		self.listview3 = Gtk.ListBox()
		self.listview3.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listview3, True, True, 0)

		#==================
		#		Row 1				
		#==================
		self.listRow3 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow3.add(self.hbox1)

		# ListRow 1 Elements
		self.label4 = Gtk.Label(xalign=0)
		self.label4.set_text("Aspect Ratio")
		self.comboAspect = Gtk.ComboBoxText()
		self.comboAspect.set_size_request(170, 0)
		for aspect in aspectRatio:
			self.comboAspect.append_text(aspect)
		self.comboAspect.set_active(0)

		self.hbox1.pack_start(self.label4, True, True, 0)
		self.hbox1.pack_start(self.comboAspect, False, False, 0)
		self.listview3.add(self.listRow3)

		#==================
		#		Row 2				
		#==================
		self.listRow4 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow4.add(self.hbox1)

		# ListRow 1 Elements
		self.label5 = Gtk.Label(xalign=0)
		self.label5.set_text("Resolution")
		self.comboRes = Gtk.ComboBoxText()
		self.comboRes.set_size_request(170,0)
		for res in res16_9:
			self.comboRes.append_text(res)
		self.comboRes.set_active(0)

		self.hbox1.pack_start(self.label5, True, True, 0)
		self.hbox1.pack_start(self.comboRes, False, False, 0)
		self.listview3.add(self.listRow4)

		self.comboAspect.connect("changed", self.on_aspect_changed)

		#===========================================
		#				4th Section				
		#=========================================== 
		self.listview_profile = Gtk.ListBox()
		self.listview_profile.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listview_profile, True, True, 0)

		#==================
		#		Row 1				
		#==================
		self.listRowC = Gtk.ListBoxRow()
		self.hboxC = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRowC.add(self.hboxC)

		# ListRow 1 Elements
		self.labelC = Gtk.Label(xalign=0)
		self.labelC.set_text("Codec")
		self.comboCodec = Gtk.ComboBoxText()
		self.comboCodec.set_size_request(170, 0)
		for codec in vcodecs:
			self.comboCodec.append_text(codec)
		self.comboCodec.set_active(0)

		self.hboxC.pack_start(self.labelC, True, True, 0)
		self.hboxC.pack_start(self.comboCodec, False, False, 0)
		self.listview_profile.add(self.listRowC)

		self.comboCodec.connect("changed", self.on_codec_change)

		#==================
		#		Row 2
		#==================
		self.listRow8 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow8.add(self.hbox1)

		# ListRow 1 Elements
		self.label9 = Gtk.Label(xalign=0)
		self.label9.set_text("x264 Profile")
		self.comboProfile = Gtk.ComboBoxText()
		self.comboProfile.set_size_request(170, 0)
		for profile in x264_profiles:
			self.comboProfile.append_text(profile)
		self.comboProfile.set_active(0)

		self.hbox1.pack_start(self.label9, True, True, 0)
		self.hbox1.pack_start(self.comboProfile, False, False, 0)
		self.listview_profile.add(self.listRow8)

		#==================
		#		Row 3
		#==================
		self.listRow9 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow9.add(self.hbox1)

		# ListRow 1 Elements
		self.label10 = Gtk.Label(xalign=0)
		self.label10.set_text("Profile Level")
		self.comboLevel = Gtk.ComboBoxText()
		self.comboLevel.set_size_request(170, 0)
		for level in high:
			self.comboLevel.append_text(level)
		self.comboLevel.set_active(0)

		self.hbox1.pack_start(self.label10, True, True, 0)
		self.hbox1.pack_start(self.comboLevel, False, False, 0)
		self.listview_profile.add(self.listRow9)

		self.comboProfile.connect("changed", self.on_profile_change)

		#===========================================
		#				5th Section				
		#=========================================== 
		self.listview4 = Gtk.ListBox()
		self.listview4.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listview4, True, True, 0)

		#==================
		#		Row 1				
		#==================
		self.listRow5 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow5.add(self.hbox1)

		# ListRow 1 Elements
		self.label6 = Gtk.Label(xalign=0)
		self.label6.set_text("Audio Format")
		self.comboAudio = Gtk.ComboBoxText()
		self.comboAudio.set_size_request(170, 0)
		for audio in MP4_Acodecs:
			self.comboAudio.append_text(audio)
		self.comboAudio.set_active(0)

		self.hbox1.pack_start(self.label6, True, True, 0)
		self.hbox1.pack_start(self.comboAudio, False, False, 0)
		self.listview4.add(self.listRow5)

		#===========================================
		#				6th Section				
		#=========================================== 
		self.listview5 = Gtk.ListBox()
		self.listview5.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listview5, True, True, 0)

		#==================
		#		Row 1				
		#==================
		self.listRow6 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow6.add(self.hbox1)

		# ListRow 1 Elements
		self.label7 = Gtk.Label(xalign=0)
		self.label7.set_text("Video Bitrate")
		self.textbox3 = Gtk.Entry()
		self.textbox3.set_size_request(80, 0)
		self.textbox3.set_text("1800")

		self.hbox1.pack_start(self.label7, True, True, 0)
		self.hbox1.pack_start(self.textbox3, False, False, 0)
		self.listview5.add(self.listRow6)

		#==================
		#		Row 2				
		#==================
		self.listRow7 = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRow7.add(self.hbox1)

		# ListRow 1 Elements
		self.label8 = Gtk.Label(xalign=0)
		self.label8.set_text("Audio Bitrate (kbps)")
		self.textbox4 = Gtk.Entry()
		self.textbox4.set_size_request(80, 0)
		self.textbox4.set_text("128")

		self.hbox1.pack_start(self.label8, True, True, 0)
		self.hbox1.pack_start(self.textbox4, False, False, 0)
		self.listview5.add(self.listRow7)

		self.comboAudio.connect("changed", self.on_audio_changed)
		
		#===========================================
		#				7th Section				
		#===========================================
		self.listviewBTM = Gtk.ListBox()
		self.listviewBTM.set_selection_mode(Gtk.SelectionMode.NONE)
		self.vbox.pack_start(self.listviewBTM, True, True, 0)

		#==================
		#		Row 1				
		#==================
		self.listRowBTM = Gtk.ListBoxRow()
		self.hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		self.listRowBTM.add(self.hbox1)

		# ListRow 1 Elements
		self.buttonBTM = Gtk.Button(label="RUN")
		self.buttonBTM.set_size_request(100, 0)
		self.buttonBTM.connect("clicked", self.on_buttonBTM_changed)

		self.hbox1.pack_end(self.buttonBTM, True, True, 0)
		self.listviewBTM.add(self.listRowBTM)


	def on_button_save_clicked(self, widget):
		dialog = Gtk.FileChooserDialog(
			title="Please choose a file",
			action=Gtk.FileChooserAction.SAVE,
		)

		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
			"Save", Gtk.ResponseType.OK)

		response = dialog.run()

		if response == Gtk.ResponseType.OK:			
			filename = dialog.get_filename()
			if self.comboCodec.get_active_text() == "matroska":
				if ".mkv" in filename:
					self.textbox2.set_text(filename)
				else:
					self.textbox2.set_text(filename + ".mkv")			
			else:
				if ".mp4" in filename:
					self.textbox2.set_text(filename)
				else:
					self.textbox2.set_text(filename + ".mp4")
						
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			# print("Cancel clicked")
			dialog.destroy()
		pass

	def on_button_open_clicked(self, widget):
		
		dialog = Gtk.FileChooserDialog(
			title="Please choose a file",
			action=Gtk.FileChooserAction.OPEN,
		)

		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
			"Open", Gtk.ResponseType.OK)

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
		pass


	def on_codec_change(self,combo):
		text = combo.get_active_text()		

		self.comboProfile.get_model().clear()

		if text == "x264":
			for profs in x264_profiles:
				self.comboProfile.append_text(profs)

			self.comboAudio.get_model().clear()
			for codes in MP4_Acodecs:
				self.comboAudio.append_text(codes)
		elif text == "x264_lossless":
			for profs in x265_profiles:
				self.comboProfile.append_text(profs)

			self.comboAudio.get_model().clear()
			for codes in MP4_Acodecs:
				self.comboAudio.append_text(codes)				
		elif text == "x265" or text == "x265_lossless":
			for profs in x265_profiles:
				self.comboProfile.append_text(profs)

			self.comboAudio.get_model().clear()
			for codes in MP4_Acodecs:
				self.comboAudio.append_text(codes)

		else:
			self.comboProfile.append_text('---')

			self.comboAudio.get_model().clear()
			for codes in MKV_Acodecs:
				self.comboAudio.append_text(codes)
		
		self.comboProfile.set_active(0);
		self.comboAudio.set_active(0);
		


	def on_audio_changed(self, combo):
		text = combo.get_active_text()
		if text == "aac":
			self.textbox4.set_text("128")
		elif text == "mp3":
			self.textbox4.set_text("192")
		elif text == "vorbis":
			self.textbox4.set_text("128");
		elif text == "opus":
			self.textbox4.set_text("64");
		else:
			self.textbox4.set_text("160");
		

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
		
		self.comboLevel.get_model().clear()

		if text == "high":			
			for level in high:
				self.comboLevel.append_text(level)			
		elif text == "main":			
			for level in main:
				self.comboLevel.append_text(level)			
		elif text == "baseline":			
			for level in baseline:
				self.comboLevel.append_text(level)		
		elif text == "ultrafast" or text == "superfast" or text == "veryfast" or text == "faster" or text == "fast" \
		or text == "medium" or text == "slow" or text == "slower" or text == "veryslow" or text == "placebo":			
			for level in bit:
				self.comboLevel.append_text(level)
		else:
			self.comboLevel.append_text("---")

		self.comboLevel.set_active(0)


	def on_buttonBTM_changed(self,widget):
		if not self.checkBoxes():
			md = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Infile or Outfile missing")
			md.format_secondary_text("Both fields need to be filled for the encoder to work")
			md.run()
			md.destroy()
			return False

		error = 0;
		TERMINAL = self.comboTERM.get_active_text()

		G_SIZE="120x23"
		GEOMETRY = "--geometry=" + G_SIZE
		TITLE = "-T"

		if TERMINAL == "urxvt" or TERMINAL == "xterm":
			GEOMETRY = "-geometry"
			TITLE = "-title"
		elif TERMINAL == "lxterminal":
			TITLE = "-t"
		elif TERMINAL == "konsole":
			TITLE = "--nofork"
		elif TERMINAL == "st":
			GEOMETRY = "-g"
			


		if self.comboAudio.get_active_text() == "mp3":
			aCodec = "libmp3lame"
			aArg = "-q:a"
			aVal = "2"
		elif self.comboAudio.get_active_text() == "aac":
			aCodec = "aac"
			aArg = "-q:a"
			aVal = "3"
		elif self.comboAudio.get_active_text() == "vorbis":
			aCodec = "libvorbis"
			aArg = "-q:a"
			aVal = "4"
		elif self.comboAudio.get_active_text() == "opus":
			aCodec = "libopus"
			aArg = "-q:a"
			aVal = "2"
		else:
			aCodec = "ac3"
			aArg = "-q:a"
			aVal = "2"		

		if self.comboCodec.get_active_text() == "x264" or self.comboCodec.get_active_text() == "x264_lossless":			
			bits = "-pix_fmt"
			if self.comboLevel.get_active_text() == "8bit":				
				bits_val = "yuv420p"
			elif self.comboLevel.get_active_text() == "10bit":
				bits_val = "yuv420p10le"		    
			elif self.comboLevel.get_active_text() == "12bit":
				bits_val = "yuv420p12le"
			else:
				bits = "-level"
				bits_val = self.comboLevel.get_active_text()

			if self.comboCodec.get_active_text() == "x264_lossless":
				INPUT = "-preset"
				CRF = "-crf"
				CRF_VAL = "0"
			else:
				INPUT = "-profile:v"
				CRF = "-crf"
				CRF_VAL = "30"

			COMMAND = [TERMINAL, TITLE, "bash", GEOMETRY, G_SIZE, "-e", "ffmpeg", "-i", self.textbox1.get_text(), "-metadata", "title=" + os.path.basename(self.textbox2.get_text()), "-vf", "scale=" + self.comboRes.get_active_text(),
				"-aspect", self.comboAspect.get_active_text(), "-acodec", aCodec, aArg, aVal, "-ar", "48000", "-b:a", self.textbox4.get_text() + "k", "-vcodec", "mpeg4", "-b:v", 
				self.textbox3.get_text() + "K", "-c:v", "libx264", CRF, CRF_VAL, INPUT, self.comboProfile.get_active_text(), bits, bits_val, "-hide_banner", self.textbox2.get_text()]
			

		elif self.comboCodec.get_active_text() == "x265" or self.comboCodec.get_active_text() == "x265_lossless":
			bits = "-pix_fmt"
			bits_val = "yuv420p"

			if self.comboLevel.get_active_text() == "8bit":				
				bits_val = "yuv420p"
			elif self.comboLevel.get_active_text() == "10bit":
				bits_val = "yuv420p10le"		    
			elif self.comboLevel.get_active_text() == "12bit":
				bits_val = "yuv420p12le"

			if self.comboCodec.get_active_text() == "x265_lossless":
				CRF = "crf=0"
			else:
				CRF = "crf=30"

			COMMAND = [TERMINAL, TITLE, "bash", GEOMETRY, G_SIZE, "-e", "ffmpeg", "-i", self.textbox1.get_text(), "-metadata", "title=" + os.path.basename(self.textbox2.get_text()), "-vf", "scale=" + self.comboRes.get_active_text(),
				"-aspect", self.comboAspect.get_active_text(), "-acodec", aCodec, aArg, aVal, "-ar", "48000", "-b:a", self.textbox4.get_text() + "k", "-b:v", self.textbox3.get_text() + "K", "-c:v", "libx265", "-x265-params",
				CRF, bits, bits_val, "-preset", self.comboProfile.get_active_text(), "-hide_banner", self.textbox2.get_text()]
			

		else:
			COMMAND = [TERMINAL, TITLE, "bash", GEOMETRY, G_SIZE, "-e", "ffmpeg", "-i", self.textbox1.get_text(), "-metadata", "title=" + os.path.basename(self.textbox2.get_text()), "-f", "matroska", "-vf", 
				"scale=" + self.comboRes.get_active_text(), "-aspect", self.comboAspect.get_active_text(), "-acodec", aCodec, aArg, aVal, "-ar", "48000", "-b:a", self.textbox4.get_text() + "k", 
				"-vcodec", "vp8", "-b:v", self.textbox3.get_text() + "K", "-hide_banner", self.textbox2.get_text()]
			
		
		self.set_sensitive(False)
		
		if not os.path.isfile(self.textbox1.get_text()):
			self.callError(0)
			return False		

		try:
			t = threading.Thread(target=self.RunEncode, args=(COMMAND,))
			t.daemon = True
			t.start()
		except:			
			self.callError(1)
		
	def callError(self, errorCode):
		if errorCode == 0:
			message = "Seems ffmpegGUI can not find the file you wish to encode.\n Please check your file exists."
		else:
			message = "Seems the terminal selected is incorrect or the command input is not properly coded for your terminals excecution option."

		md = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="An Error has occured")
		md.format_secondary_text(message)
		md.run()
		md.destroy()
		self.set_sensitive(True)
		error = 1;

	def checkEncoder(self,CODE):
		if CODE == 0 and not error == 1:
			print("ENCODING COMPLETE!")
			if self.switch.get_active():
				Gtk.main_quit(0)
			else:
				self.set_sensitive(True)				
		return False
	
	def RunEncode(self, command):
		
		p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		res = p.communicate()		

		while True:
			GLib.idle_add(self.checkEncoder, p.returncode)
			time.sleep(0.2)
			if p.returncode == 0:
				break
		

	def checkBoxes(self):
		if self.textbox1.get_text() == "":
			return False
		elif self.textbox2.get_text() == "":
			return False
		else:
			return True


def signal_handler(sig, frame):
	print('\nYou pressed Ctrl+C!\nHEFFS ffmpeg GUI is Closing.')
	Gtk.main_quit(0)

if __name__ == '__main__':
	#GObject.threads_init()
	signal.signal(signal.SIGINT, signal_handler)
	window = ffmpegGUI()
	window.connect("delete-event", Gtk.main_quit)
	window.show_all()	
	Gtk.main()