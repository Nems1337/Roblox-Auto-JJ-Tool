import customtkinter as ctk
import pyautogui
import pyperclip
import threading
import time
import random
import os
import tkinter as tk
from pynput import keyboard
from enum import Enum

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

class Mode(Enum):
	JJ = "JJ"
	GJ = "GJ"
	HJ = "HJ"

class Lang(Enum):
	EN = "en"
	TR = "tr"

class Main:
	def __init__(self):
		self.root = ctk.CTk()
		self.root.title("The time that I reincarnated as a JJ Tool to Rank up in a Lego Game")
		self.root.geometry("450x420")
		self.load_icon()
		
		self.running = False
		self.counter = 0
		self.mode = Mode.JJ
		self.lang = Lang.EN
		self.delay = 1
		self.countdown = 3
		self.start_num = 1
		self.end_num = 100
		self.always_on_top = False
		self.hotkey_listener = None
		
		self.text = {
			Lang.EN: {"start":"Start", "stop":"Stop", "counting":"Counting", "mode":"Mode", 
				"cooldown":"Cooldown (s)", "language":"Language", "warning":"Warning: May violate ToS!", 
				"stopped":"Stopped", "countdown":"Countdown (s)", "starting_in":"Starting in", 
				"esc_stop":"Press ESC to stop", "start_num":"Start Number", "end_num":"End Number", 
				"range_error":"Start must be < End", "completed":"Completed", "range":"Range",
				"always_on_top":"Always On Top"},
			Lang.TR: {"start":"Başlat", "stop":"Durdur", "counting":"Sayım", "mode":"Mod", 
				"cooldown":"Bekleme (sn)", "language":"Dil", "warning":"Uyarı: ToS ihlali edebilir!", 
				"stopped":"Durduruldu", "countdown":"Geri sayım (sn)", "starting_in":"Başlangıç", 
				"esc_stop":"Durdurmak için ESC", "start_num":"Başlangıç", "end_num":"Bitiş", 
				"range_error":"Başlangıç < Bitiş olmalı", "completed":"Tamamlandı", "range":"Aralık",
				"always_on_top":"Her Zaman Üstte"}
		} # u can add more if want to im just too lazy :P
		
		self.setup_ui()
		self.setup_keys()
		print(self.text[self.lang]["warning"])
	
	def load_icon(self):
		try:
			if os.path.exists("icon.ico"):
				self.root.iconbitmap("icon.ico")
			elif os.path.exists("icon.png"):
				img = tk.PhotoImage(file="icon.png")
				self.root.iconphoto(True, img)
		except:
			pass
	
	def num_to_en(self, n):
		if n == 0: return "ZERO"
		
		ones = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
		teens = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
		tens = ["", "", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
		
		def under_1000(num):
			if num < 10:
				return ones[num]
			elif num < 20:
				return teens[num - 10]
			elif num < 100:
				return tens[num // 10] + (" " + ones[num % 10] if num % 10 else "")
			else:
				result = ones[num // 100] + " HUNDRED"
				if num % 100:
					result += " " + under_1000(num % 100)
				return result
		
		if n < 1000:
			return under_1000(n)
		elif n < 1000000:
			result = under_1000(n // 1000) + " THOUSAND"
			if n % 1000:
				result += " " + under_1000(n % 1000)
			return result
		elif n < 1000000000:
			result = under_1000(n // 1000000) + " MILLION"
			remainder = n % 1000000
			if remainder >= 1000:
				result += " " + under_1000(remainder // 1000) + " THOUSAND"
				if remainder % 1000:
					result += " " + under_1000(remainder % 1000)
			elif remainder:
				result += " " + under_1000(remainder)
			return result
		else:
			return str(n)
	
	def num_to_tr(self, n):
		if n == 0: return "SIFIR"
		
		ones = ["", "BİR", "İKİ", "ÜÇ", "DÖRT", "BEŞ", "ALTI", "YEDİ", "SEKİZ", "DOKUZ"]
		tens = ["", "ON", "YİRMİ", "OTUZ", "KIRK", "ELLİ", "ALTMIŞ", "YETMİŞ", "SEKSEN", "DOKSAN"]
		
		def under_1000(num):
			if num < 10:
				return ones[num]
			elif num < 100:
				return tens[num // 10] + (" " + ones[num % 10] if num % 10 else "")
			else:
				result = "YÜZ" if num // 100 == 1 else ones[num // 100] + " YÜZ"
				if num % 100:
					result += " " + under_1000(num % 100)
				return result
		
		if n < 1000:
			return under_1000(n)
		elif n < 1000000:
			result = "BİN" if n // 1000 == 1 else under_1000(n // 1000) + " BİN"
			if n % 1000:
				result += " " + under_1000(n % 1000)
			return result
		elif n < 1000000000:
			result = under_1000(n // 1000000) + " MİLYON"
			remainder = n % 1000000
			if remainder >= 1000:
				thousands = remainder // 1000
				result += " " + ("BİN" if thousands == 1 else under_1000(thousands) + " BİN")
				if remainder % 1000:
					result += " " + under_1000(remainder % 1000)
			elif remainder:
				result += " " + under_1000(remainder)
			return result
		else:
			return str(n)
	
	def tr_caps(self, text):
		tr_map = {'ı': 'I', 'i': 'İ', 'ş': 'Ş', 'ğ': 'Ğ', 'ü': 'Ü', 'ö': 'Ö', 'ç': 'Ç'}
		tr_lower = {'I': 'ı', 'İ': 'i', 'Ş': 'ş', 'Ğ': 'ğ', 'Ü': 'ü', 'Ö': 'ö', 'Ç': 'ç'}
		
		words = text.split(" ")
		for i, word in enumerate(words):
			if word:
				first = tr_map.get(word[0], word[0].upper())
				rest = "".join(tr_lower.get(c, c.lower()) for c in word[1:])
				words[i] = first + rest
		return " ".join(words)
	
	def setup_ui(self):
		# modes
		mode_frame = ctk.CTkFrame(self.root)
		mode_frame.pack(pady=10)
		
		self.jj_btn = ctk.CTkButton(mode_frame, text="JJ", width=80, command=lambda: self.set_mode(Mode.JJ))
		self.jj_btn.grid(row=0, column=0, padx=5)
		
		self.gj_btn = ctk.CTkButton(mode_frame, text="GJ", width=80, command=lambda: self.set_mode(Mode.GJ))
		self.gj_btn.grid(row=0, column=1, padx=5)
		
		self.hj_btn = ctk.CTkButton(mode_frame, text="HJ", width=80, command=lambda: self.set_mode(Mode.HJ))
		self.hj_btn.grid(row=0, column=2, padx=5)
		
		# always on top
		options_frame = ctk.CTkFrame(self.root)
		options_frame.pack(pady=10)
		
		self.always_on_top_checkbox = ctk.CTkCheckBox(options_frame, text=self.text[self.lang]["always_on_top"], command=self.toggle_always_on_top)
		self.always_on_top_checkbox.pack(padx=20, pady=10)
		
		# language
		lang_frame = ctk.CTkFrame(self.root)
		lang_frame.pack(pady=10)
		
		self.lang_lbl = ctk.CTkLabel(lang_frame, text=self.text[self.lang]["language"])
		self.lang_lbl.grid(row=0, column=0, padx=10)
		
		self.lang_combo = ctk.CTkComboBox(lang_frame, values=["English (en)", "Türkçe (tr)"], command=self.change_lang, width=150, state="readonly")
		self.lang_combo.set("English (en)")
		self.lang_combo.grid(row=0, column=1)
		
		# delay
		delay_frame = ctk.CTkFrame(self.root)
		delay_frame.pack(pady=10)
		
		self.delay_lbl = ctk.CTkLabel(delay_frame, text=f"{self.text[self.lang]['cooldown']}: {self.delay}")
		self.delay_lbl.grid(row=0, column=0, padx=10)
		
		self.delay_slider = ctk.CTkSlider(delay_frame, from_=0.1, to=5.0, command=self.update_delay, width=200)
		self.delay_slider.set(0.5)
		self.delay_slider.grid(row=0, column=1)
		
		# countdown
		countdown_frame = ctk.CTkFrame(self.root)
		countdown_frame.pack(pady=10)
		
		self.countdown_lbl = ctk.CTkLabel(countdown_frame, text=f"{self.text[self.lang]['countdown']}: {self.countdown}")
		self.countdown_lbl.grid(row=0, column=0, padx=10)
		
		self.countdown_slider = ctk.CTkSlider(countdown_frame, from_=0, to=10, number_of_steps=10, command=self.update_countdown, width=200)
		self.countdown_slider.set(3)
		self.countdown_slider.grid(row=0, column=1)
		
		# range
		range_frame = ctk.CTkFrame(self.root)
		range_frame.pack(pady=10)
		
		start_lbl = ctk.CTkLabel(range_frame, text=self.text[self.lang]["start_num"])
		start_lbl.grid(row=0, column=0, padx=5)
		
		self.start_entry = ctk.CTkEntry(range_frame, width=80, placeholder_text="1")
		self.start_entry.insert(0, "1")
		self.start_entry.bind("<KeyRelease>", self.validate_range)
		self.start_entry.grid(row=0, column=1, padx=5)
		
		end_lbl = ctk.CTkLabel(range_frame, text=self.text[self.lang]["end_num"])
		end_lbl.grid(row=0, column=2, padx=5)
		
		self.end_entry = ctk.CTkEntry(range_frame, width=80, placeholder_text="100")
		self.end_entry.insert(0, "100")
		self.end_entry.bind("<KeyRelease>", self.validate_range)
		self.end_entry.grid(row=0, column=3, padx=5)
		
		self.start_lbl = start_lbl
		self.end_lbl = end_lbl
		
		# main button
		self.toggle_btn = ctk.CTkButton(self.root, text=self.text[self.lang]["start"], 
			command=self.toggle, width=200, height=40)
		self.toggle_btn.pack(pady=20)
		
		# status
		self.status_lbl = ctk.CTkLabel(self.root, text=f"{self.text[self.lang]['stopped']}", font=("Arial", 14))
		self.status_lbl.pack(pady=10)
		
		# watermark :v
		watermark = ctk.CTkLabel(self.root, text="Made by Nems1337", font=("Arial", 10), text_color=("gray60", "gray40"))
		watermark.pack(side="bottom", pady=(0, 5))
		
		self.update_ui()
		self.validate_range()
	
	def set_mode(self, mode):
		self.mode = mode
		self.update_ui()
	
	def update_ui(self):
		self.jj_btn.configure(fg_color="green" if self.mode == Mode.JJ else "gray")
		self.gj_btn.configure(fg_color="green" if self.mode == Mode.GJ else "gray")
		self.hj_btn.configure(fg_color="green" if self.mode == Mode.HJ else "gray")
	
	def change_lang(self, value):
		self.lang = Lang.EN if "en" in value else Lang.TR
		self.refresh_ui()
		print(self.text[self.lang]["warning"])
	
	def refresh_ui(self):
		self.lang_lbl.configure(text=self.text[self.lang]["language"])
		self.always_on_top_checkbox.configure(text=self.text[self.lang]["always_on_top"])
		self.delay_lbl.configure(text=f"{self.text[self.lang]['cooldown']}: {self.delay}")
		self.countdown_lbl.configure(text=f"{self.text[self.lang]['countdown']}: {self.countdown}")
		self.start_lbl.configure(text=self.text[self.lang]["start_num"])
		self.end_lbl.configure(text=self.text[self.lang]["end_num"])
		self.toggle_btn.configure(text=self.text[self.lang]["stop"] if self.running else self.text[self.lang]["start"])
		if not self.running:
			self.status_lbl.configure(text=self.text[self.lang]["stopped"])
	
	def update_delay(self, value):
		self.delay = round(value, 1)
		self.delay_lbl.configure(text=f"{self.text[self.lang]['cooldown']}: {self.delay}")
	
	def update_countdown(self, value):
		self.countdown = int(value)
		self.countdown_lbl.configure(text=f"{self.text[self.lang]['countdown']}: {self.countdown}")
	
	def toggle_always_on_top(self):
		self.always_on_top = self.always_on_top_checkbox.get()
		self.root.wm_attributes("-topmost", self.always_on_top)
	
	def validate_range(self, event=None):
		try:
			start_val = self.start_entry.get().strip()
			end_val = self.end_entry.get().strip()
			
			if start_val and end_val:
				self.start_num = int(start_val)
				self.end_num = int(end_val)
				
				if self.start_num >= self.end_num:
					self.status_lbl.configure(text=self.text[self.lang]["range_error"], text_color="red")
				elif not self.running:
					self.status_lbl.configure(text=f"{self.text[self.lang]['range']}: {self.start_num} - {self.end_num}", text_color="white")
			elif start_val:
				self.start_num = int(start_val)
			elif end_val:
				self.end_num = int(end_val)
		except ValueError:
			if not self.running:
				self.status_lbl.configure(text=self.text[self.lang]["range_error"], text_color="red")
	
	def handle_key(self, key):
		try:
			if key == keyboard.Key.esc and self.running:
				self.stop()
		except AttributeError:
			pass
	
	def setup_keys(self):
		self.hotkey_listener = keyboard.Listener(on_press=self.handle_key)
		self.hotkey_listener.daemon = True
		self.hotkey_listener.start()
	
	def stop(self):
		self.running = False
		self.toggle_btn.configure(text=self.text[self.lang]["start"])
		self.status_lbl.configure(text=self.text[self.lang]["stopped"])
	
	def toggle(self):
		if not self.running:
			try:
				start_val = self.start_entry.get().strip()
				end_val = self.end_entry.get().strip()
				
				if not start_val or not end_val:
					self.status_lbl.configure(text=self.text[self.lang]["range_error"], text_color="red")
					return
				
				self.start_num = int(start_val)
				self.end_num = int(end_val)
				
				if self.start_num >= self.end_num:
					self.status_lbl.configure(text=self.text[self.lang]["range_error"], text_color="red")
					return
			except ValueError:
				self.status_lbl.configure(text=self.text[self.lang]["range_error"], text_color="red")
				return
			
			self.running = True
			self.counter = self.start_num
			self.toggle_btn.configure(text=self.text[self.lang]["stop"])
			
			if self.countdown > 0:
				threading.Thread(target=self.start_countdown, daemon=True).start()
			else:
				threading.Thread(target=self.main_loop, daemon=True).start()
		else:
			self.stop()
	
	def start_countdown(self):
		for i in range(self.countdown, 0, -1):
			if not self.running:
				return
			self.status_lbl.configure(text=f"{self.text[self.lang]['starting_in']}: {i}... {self.text[self.lang]['esc_stop']}")
			time.sleep(1)
		
		if self.running:
			self.main_loop()
	
	def main_loop(self):
		while self.running and self.counter <= self.end_num:
			self.status_lbl.configure(text=f"{self.text[self.lang]['counting']}: {self.counter} | {self.text[self.lang]['mode']}: {self.mode.value}")
			
			word = self.num_to_en(self.counter) if self.lang == Lang.EN else self.num_to_tr(self.counter)
			
			if self.mode == Mode.JJ:
				self.do_jj(word.upper())
			elif self.mode == Mode.GJ:
				formatted = self.tr_caps(word.upper()) + "." if self.lang == Lang.TR else word.capitalize() + "."
				self.do_gj(formatted)
			else:
				self.do_hj(word.upper())
			
			if not self.running:
				break
			
			if self.counter % 10 == 0:
				print(f"Count: {self.counter}")
			
			if self.counter >= self.end_num:
				break
			
			self.counter += 1
			
			delay = random.uniform(0.5, self.delay) if self.delay > 0.5 else self.delay
			time.sleep(delay)
		
		if self.running and self.counter >= self.end_num:
			self.status_lbl.configure(text=f"{self.text[self.lang]['completed']} ({self.start_num}-{self.end_num})")
		
		self.running = False
		self.toggle_btn.configure(text=self.text[self.lang]["start"])
	
	def type_text(self, text):
		if not self.running:
			return
		
		tr_chars = {'ı', 'İ', 'ş', 'Ş', 'ğ', 'Ğ', 'ü', 'Ü', 'ö', 'Ö', 'ç', 'Ç'}
		use_clipboard = any(char in tr_chars for char in text) and self.lang == Lang.TR
		
		if use_clipboard:
			pyperclip.copy(text)
			time.sleep(0.01)
			if self.running:
				pyautogui.hotkey('ctrl', 'v')
		else:
			try:
				pyautogui.typewrite(text, interval=0)
			except:
				pyperclip.copy(text)
				time.sleep(0.01)
				if self.running:
					pyautogui.hotkey('ctrl', 'v')
	
	def do_jj(self, word):
		if not self.running: return
		pyautogui.press('space')
		time.sleep(0.05)
		if not self.running: return
		pyautogui.press('/')
		time.sleep(0.05)
		if not self.running: return
		self.type_text(word)
		if not self.running: return
		pyautogui.press('enter')
	
	def do_gj(self, word):
		if not self.running: return
		pyautogui.press('space')
		time.sleep(0.05)
		if not self.running: return
		pyautogui.press('/')
		time.sleep(0.05)
		if not self.running: return
		self.type_text(word)
		if not self.running: return
		pyautogui.press('enter')
	
	def do_hj(self, word):
		if not self.running: return
		
		letters = word.replace(" ", "")
		for i, letter in enumerate(letters):
			if not self.running: return
			
			pyautogui.press('space')
			time.sleep(0.05)
			pyautogui.press('/')
			time.sleep(0.05)
			if not self.running: return
			
			self.type_text(letter)
			pyautogui.press('enter')
			
			if i < len(letters) - 1:
				if not self.running: return
				delay = random.uniform(0.5, self.delay) if self.delay > 0.5 else self.delay
				time.sleep(delay)
		
		if not self.running: return
		
		delay = random.uniform(0.5, self.delay) if self.delay > 0.5 else self.delay
		time.sleep(delay)
		
		pyautogui.press('space')
		time.sleep(0.05)
		pyautogui.press('/')
		time.sleep(0.05)
		if not self.running: return
		
		self.type_text(word)
		pyautogui.press('enter')
	
	def run(self):
		try:
			self.root.mainloop()
		finally:
			self.cleanup()
	
	def cleanup(self):
		self.running = False
		if self.hotkey_listener:
			self.hotkey_listener.stop()

if __name__ == "__main__":
	app = Main()
	app.run()