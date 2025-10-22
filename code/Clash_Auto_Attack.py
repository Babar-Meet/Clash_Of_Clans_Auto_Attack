import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pytesseract
import pyautogui
import keyboard
import time
import random
from PIL import ImageGrab, Image
from datetime import datetime
import threading
import os
import queue
import mouse

class CocAutoFarmerGUI:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(r"img\clash_of_clans_img.ico")
        self.root.title("COC Farm ")
        self.root.geometry("360x200")
        self.root.resizable(True, True)

        self.tesseract_path = tk.StringVar(value=r'Tesseract-OCR\tesseract.exe')
        self.tiers = {
            1: {'thresholds': {'gold': 950000, 'elixir': 950000, 'dark_elixir': 150000}, 'time': 69},
            2: {'thresholds': {'gold': 750000, 'elixir': 750000, 'dark_elixir': 120000}, 'time': 60},
            3: {'thresholds': {'gold': 600000, 'elixir': 600000, 'dark_elixir': 80000}, 'time': 51}
        }
        self.just_attack_timer = tk.IntVar(value=21)
        self.is_running = False
        self.stop_requested = False
        self.current_coord_index = 0
        self.coord_logging_active = False
        self.coord_logging_thread = None
        
        # 13 drag
        """
    326,413
    514,289
    729,117
    1015,0
    1198,132
    1351,259
    1526,375
    1677,516
    1539,665
    1301,816
    1097,955
    727,957
    505,785
    352,647

"""

# (261, 453)
# (388, 355)
# (527, 263)
# (733, 103)
# (834, 11)
# (1095, 55)
# (1254, 176)
# (1404, 293)
# (1557, 399)
# (1672, 538)
# (1549, 626)
# (1444, 711)
# (1324, 818)
# (1214, 896)
# (685, 895)
# (565, 805)
# (441, 708)
# (330, 603)


# surander
# 128,915

        # this 2 are same for consistenct
        self.troop_coordinates = [
            (444, 327), (759, 93), (1067, 29), (1308, 208),
            (1511, 348), (1708, 532), (1487, 691), (1295, 836), (676, 861), (480, 727)
        ]

        self.troop_coordinates_different = [
            (444, 327), (759, 93), (1067, 29), (1308, 208),
            (1511, 348), (1708, 532), (1487, 691), (1295, 836), (676, 861), (480, 727)
        ]

        # different cord for anti ban
        # self.troop_coordinates_different = [
        #     (540, 271), (835, 46), (1158, 74), (1419, 268),
        #     (1606, 605), (1661, 601), (1381, 822), (1307, 881), (514, 772), (308, 621)
        # ]



        self.spell_coordinates = [
            (195, 522), (444, 327), (759, 93), (1067, 29), (1308, 208),
            (1511, 348), (1708, 532), (1487, 691), (1295, 836), (676, 861), (480, 727)
        ]

        self.spell_coordinates_different = [
            (195, 522), (444, 327), (759, 93), (1067, 29), (1308, 208),
            (1511, 348), (1708, 532), (1487, 691), (1295, 836), (676, 861), (480, 727)
        ]
        
        
        # self.spell_coordinates_different = [
        #     (200, 512), (540, 271), (835, 46), (1158, 74), (1419, 268),
        #     (1606, 605), (1661, 601), (1381, 822), (1307, 881), (514, 772), (308, 621)
        # ]

# 323,427
# 586,240
# 776,89
# 1151,60
# 1327,203
# 1520,332
# 1705,475
# 1530,723
# 1338,876
# 555,799
# 340,640

        # cord for miniton attcakcs
        # self.troop_coordinates = [
        #     (261, 453),(388, 355),(527, 263),(733, 103),(834, 11),(1095, 55),(1254, 176),
        #     (1404, 293),(1557, 399),(1672, 538),(1549, 626),(1444, 711),(1324, 818),(1214, 896),
        #     (685, 895),(565, 805),(441, 708),(330, 603)]

        # self.troop_coordinates_different = [
        #     (261, 453),(388, 355),(527, 263),(733, 103),(834, 11),(1095, 55),(1254, 176),
        #     (1404, 293),(1557, 399),(1672, 538),(1549, 626),(1444, 711),(1324, 818),(1214, 896),
        #     (685, 895),(565, 805),(441, 708),(330, 603)]


        self.hero_coordinates = [(195, 522)]
        
        self.CC_coordinates = [(195, 522)]
        
        self.gold_coords = (72, 116, 214, 158)
        self.elixir_coords = (72, 165, 213, 205)
        self.dark_elixir_coords = (72, 208, 187, 246)
        
        self.fight_btn = (99, 973)
        self.fight_btn_failsafe = (131,857)
        self.find_base_btn = (106, 785)
        self.surrender_btn = (102, 846)
        self.confirm_btn = (1267, 716)
        self.return_home_btn = (955, 901)
        self.return_with_chest_btn = (955, 901)
        self.next_btn = (1770, 819)
        
        self.troops = {'2': 15,'1': 15}
        self.heroes = ['q', 'w', 'e', 'r']
        self.spells = {'o': 1, 'a': 18}
        self.cc = ['z']
        
        self.error_images = [r"img\server_eoror.png",
                            r"img\connection_lost.png"]
        self.army_imgs = [
            r"img\army_0.png",
            r"img\army_1.png",
            r"img\army_2.png",
            r"img\army_3.png",
            r"img\army_4.png",
            r"img\army_5.png",
            r"img\army_6.png",
            r"img\BH_army_0.png"
        ]
        self.attack_imgs = [
            r"img\attck_null.png",
            r"img\attck_0.png",
            r"img\attck_1.png",
            r"img\attck_2.png",
            r"img\attck_3.png",
            r"img\attck_4.png",
            r"img\attck_0_tresure.png",
            r"img\attck_1_tresure.png",
            r"img\attck_2_tresure.png",
            r"img\attck_3_tresure.png",
            r"img\attck_4_tresure.png",
            r"img\attck_null_tresure.png"
        ]
        self.return_home_img = r"img\return_home.png"
        self.return_with_chest_img = r"img\return_with_chest.png"
                                    
        
        self.message_queue = queue.Queue()
        self.last_log_message = ""
        
        self.create_widgets()
        self.setup_keybindings()
        self.update_status("Ready")
        self.process_queue()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
    
        first_row = ttk.Frame(main_frame)
        first_row.pack(fill=tk.X, pady=5)
        self.surrender_button = ttk.Button(first_row, text="Surrender", command=lambda: threading.Thread(target=self.surrender).start())
        self.surrender_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        self.start_button = ttk.Button(first_row, text="Start", command=self.start_farming)
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
    
        self.stop_button = ttk.Button(first_row, text="Stop", command=self.stop_farming, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
    
        second_row = ttk.Frame(main_frame)
        second_row.pack(fill=tk.X, pady=5)
        self.just_attack_button = ttk.Button(second_row, text="Just Attack", command=lambda: threading.Thread(target=self.just_attack).start())
        self.just_attack_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        self.attack_right_now_button = ttk.Button(second_row, text="Attack Right Now", command=lambda: threading.Thread(target=self.attack_right_now).start())
        self.attack_right_now_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        third_row = ttk.Frame(main_frame)
        third_row.pack(fill=tk.X, pady=5)
        self.edit_troops_button = ttk.Button(third_row, text="Edit Troop Keys", command=self.edit_troops)
        self.edit_troops_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        self.edit_coords_button = ttk.Button(third_row, text="Edit Coordinates", command=self.edit_coordinates)
        self.edit_coords_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        fourth_row = ttk.Frame(main_frame)
        fourth_row.pack(fill=tk.X, pady=5)
    
        self.ocr_button = ttk.Button(fourth_row, text="loot_bonous", command=lambda: threading.Thread(target=self.loot_bonous).start())
        self.ocr_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        self.get_coord_button = ttk.Button(fourth_row, text="Get Coordinate", command=self.toggle_get_coordinate)
        self.get_coord_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        self.edit_thresholds_button = ttk.Button(fourth_row, text="Edit Loot Thresholds", command=self.edit_thresholds)
        self.edit_thresholds_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
        ttk.Label(main_frame, text="Clash of Clans Auto Farmer", font=("Arial", 16, "bold")).pack(pady=10)
    
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=10)
    
        ttk.Label(settings_frame, text="Tesseract Path:").pack(side=tk.LEFT)
        ttk.Entry(settings_frame, textvariable=self.tesseract_path, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(settings_frame, text="Browse", command=self.browse_tesseract).pack(side=tk.LEFT)
    
        images_frame = ttk.LabelFrame(main_frame, text="Required Images", padding=10)
        images_frame.pack(fill=tk.X, pady=10)
    
        army_frame = ttk.Frame(images_frame)
        army_frame.pack(fill=tk.X, pady=5)
        ttk.Label(army_frame, text="Army Images:").pack(side=tk.LEFT)
        self.army_img_label = ttk.Label(army_frame, text=f"{len(self.army_imgs)} army images selected")
        self.army_img_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(army_frame, text="Browse", command=lambda: self.browse_image("army")).pack(side=tk.LEFT)
    
        attack_frame = ttk.Frame(images_frame)
        attack_frame.pack(fill=tk.X, pady=5)
        ttk.Label(attack_frame, text="Attack Images:").pack(side=tk.LEFT)
        self.attack_img_label = ttk.Label(attack_frame, text=f"{len(self.attack_imgs)} attack images selected")
        self.attack_img_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(attack_frame, text="Browse", command=lambda: self.browse_image("attack")).pack(side=tk.LEFT)
    
        return_frame = ttk.Frame(images_frame)
        return_frame.pack(fill=tk.X, pady=5)
        ttk.Label(return_frame, text="Return Home Image:").pack(side=tk.LEFT)
        self.return_img_label = ttk.Label(return_frame, text=os.path.basename(self.return_home_img))
        self.return_img_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(return_frame, text="Browse", command=lambda: self.browse_image("return")).pack(side=tk.LEFT)
    
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X) 

    def setup_keybindings(self):
        keyboard.add_hotkey('ctrl+shift+backspace', self.stop_farming)
        keyboard.add_hotkey('ctrl+shift+enter', self.start_farming)
        keyboard.add_hotkey('ctrl+shift+a', self.attack_right_now)
        keyboard.add_hotkey('ctrl+shift+s', self.surrender)
        keyboard.add_hotkey('ctrl+shift+r', self.check_for_errors)
        keyboard.add_hotkey('ctrl+shift+j', self.just_attack)
        keyboard.add_hotkey('ctrl+shift+f', self.just_find_base_nothing_more)
        

    def browse_tesseract(self):
        path = filedialog.askopenfilename(title="Select Tesseract executable", filetypes=[("Executable files", "*.exe")])
        if path:
            self.tesseract_path.set(path)

    def browse_image(self, img_type):
        if img_type in ["army", "attack"]:
            paths = filedialog.askopenfilenames(title=f"Select {img_type} images", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
            if paths:
                if img_type == "army":
                    self.army_imgs = list(paths)
                    self.army_img_label.config(text=f"{len(paths)} army images selected")
                elif img_type == "attack":
                    self.attack_imgs = list(paths)
                    self.attack_img_label.config(text=f"{len(paths)} attack images selected")
        elif img_type == "return":
            path = filedialog.askopenfilename(title="Select return home image", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
            if path:
                self.return_home_img = path
                self.return_img_label.config(text=os.path.basename(path))

    def log(self, message, update_timeout=False):
        if update_timeout and self.last_log_message:
            self.log_text.delete("end-2l", "end-1l")
            self.message_queue.put({'type': 'log', 'text': message})
            self.last_log_message = message
        else:
            self.message_queue.put({'type': 'log', 'text': message})
            self.last_log_message = message

    def update_status(self, message):
        self.message_queue.put({'type': 'status', 'text': message})

    def _log(self, message):
        timestamp = datetime.now().strftime("")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def _update_status(self, message):
        self.status_bar.config(text=message)

    def process_queue(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            if message['type'] == 'log':
                self._log(message['text'])
            elif message['type'] == 'status':
                self._update_status(message['text'])
        self.root.after(100, self.process_queue)

    def toggle_get_coordinate(self):
        if not self.coord_logging_active:
            self.coord_logging_active = True
            self.get_coord_button.config(text="Stop Get Coordinate")
            self.coord_logging_thread = threading.Thread(target=self.coordinate_logging_loop, daemon=True)
            self.coord_logging_thread.start()
        else:
            self.coord_logging_active = False
            self.get_coord_button.config(text="Get Coordinate")

    def coordinate_logging_loop(self):
        while self.coord_logging_active:
            if mouse.is_pressed(button='right'):
                x, y = pyautogui.position()
                self.log(f"{x},{y}")
                while mouse.is_pressed(button='right'):
                    time.sleep(0.01)
            time.sleep(0.1)

    def start_farming(self):
        if not os.path.exists(self.tesseract_path.get()):
            messagebox.showerror("Error", "Tesseract path is not valid")
            return
        
        if not self.army_imgs or not self.attack_imgs or not os.path.exists(self.return_home_img):
            messagebox.showerror("Error", "One or more required images are missing")
            return
        
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path.get()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.edit_troops_button.config(state=tk.DISABLED)
        self.edit_coords_button.config(state=tk.DISABLED)
        self.just_attack_button.config(state=tk.DISABLED)
        self.surrender_button.config(state=tk.NORMAL)
        self.attack_right_now_button.config(state=tk.DISABLED)
        self.ocr_button.config(state=tk.DISABLED)
        self.get_coord_button.config(state=tk.DISABLED)
        self.edit_thresholds_button.config(state=tk.DISABLED)
        
        self.is_running = True
        self.stop_requested = False
        self.current_coord_index = 0
        
        self.update_status("Running")
        self.log("Starting farming process...")
        
        threading.Thread(target=self.farming_loop, daemon=True).start()

    def stop_farming(self):
        if not self.is_running:
            return
        self.stop_requested = True
        self.log("Stopping farming process...")
        self.update_status("Stopping...")

    def farming_loop(self):
        try:
            while self.is_running and not self.stop_requested:
                if self.check_for_errors():
                    self.log("Error handled, continuing...")
                    continue
                
                self.log("Clicking FIGHT button")
                pyautogui.click(*self.fight_btn_failsafe)
                time.sleep(0.01)
                pyautogui.click(*self.fight_btn)
                time.sleep(1)
                
                self.log("Clicking FIND A BASE button")
                pyautogui.click(*self.find_base_btn)
                time.sleep(1)
                
                while not self.stop_requested:
                    if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
                        self.log("Army screen found! Reading loot...")
                        attack_time = self.get_loot_from_screen()
                        if attack_time > 0:
                            self.log(f"Starting attack in 0.1 seconds... (Duration: {attack_time}s)")
                            time.sleep(0.1)
                            self.perform_attack(attack_time)
                            self.current_coord_index = 0
                            break
                        else:
                            self.log("Clicking NEXT...")
                            pyautogui.click(*self.next_btn)
                            time.sleep(1)
                    else:
                        self.log("Timeout waiting for army screen. Skipping...")
                        break
                
                self.wait_for_image_timeout(self.attack_imgs, confidence=0.8, timeout=60)
                self.log("Base ready. Starting next round...")
                
            self.log("Farming stopped")
        except Exception as e:
            self.log(f"Error in farming loop: {str(e)}")
        finally:
            self.is_running = False
            self.stop_requested = False
            self.root.after(0, self.update_ui_after_stop)

    def update_ui_after_stop(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.edit_troops_button.config(state=tk.NORMAL)
        self.edit_coords_button.config(state=tk.NORMAL)
        self.just_attack_button.config(state=tk.NORMAL)
        self.surrender_button.config(state=tk.NORMAL)
        self.attack_right_now_button.config(state=tk.NORMAL)
        self.ocr_button.config(state=tk.NORMAL)
        self.get_coord_button.config(state=tk.NORMAL)
        self.edit_thresholds_button.config(state=tk.NORMAL)
        self.update_status("Ready")

    def just_find_base_nothing_more(self):
        self.log("Starting Just Attack...")
        pyautogui.click(*self.fight_btn_failsafe)
        time.sleep(0.01)
        pyautogui.click(*self.fight_btn)
        time.sleep(1)
        pyautogui.click(*self.find_base_btn)
        time.sleep(1)
        
    def just_attack(self):
        self.log("Starting Just Attack...")
        pyautogui.click(*self.fight_btn_failsafe)
        time.sleep(0.01)
        pyautogui.click(*self.fight_btn)
        time.sleep(1)
        pyautogui.click(*self.find_base_btn)
        time.sleep(1)
        if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
            self.log(f"Army screen found! Attacking with {self.just_attack_timer.get()}s timeout...")
            self.perform_attack(self.just_attack_timer.get())
            self.current_coord_index = 0
            self.log("Just Attack completed, returning immediately...")
            pyautogui.click(*self.return_home_btn)
            time.sleep(3)
    
    def loot_bonous(self):
        #1
        try:
            
            if self.check_for_errors():
                self.log("Error handled, continuing...")
            self.log("Starting Just Attack...")
            pyautogui.click(*self.fight_btn_failsafe)
            time.sleep(0.01)
            pyautogui.click(*self.fight_btn)
            time.sleep(0.3)
            pyautogui.click(*self.find_base_btn)
            time.sleep(0.3)
            if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
                self.log(f"Army screen found! Attacking with {self.just_attack_timer.get()}s timeout...")
                self.perform_attack(self.just_attack_timer.get())
                self.current_coord_index = 0
                self.log("Just Attack completed, returning immediately...")
                pyautogui.click(*self.return_home_btn)
                time.sleep(5)
        except Exception as e:
            self.log(f"Error in farming loop: {str(e)}")
        #2
        try:
            
            if self.check_for_errors():
                self.log("Error handled, continuing...")
            self.log("Starting Just Attack...")
            pyautogui.click(*self.fight_btn_failsafe)
            time.sleep(0.01)
            pyautogui.click(*self.fight_btn)
            time.sleep(0.3)
            pyautogui.click(*self.find_base_btn)
            time.sleep(0.3)
            if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
                self.log(f"Army screen found! Attacking with {self.just_attack_timer.get()}s timeout...")
                self.perform_attack(self.just_attack_timer.get())
                self.current_coord_index = 0
                self.log("Just Attack completed, returning immediately...")
                pyautogui.click(*self.return_home_btn)
                time.sleep(5)
        except Exception as e:
            self.log(f"Error in farming loop: {str(e)}")    
        #3
        try:
            
            if self.check_for_errors():
                self.log("Error handled, continuing...")
            self.log("Starting Just Attack...")
            pyautogui.click(*self.fight_btn_failsafe)
            time.sleep(0.01)
            pyautogui.click(*self.fight_btn)
            time.sleep(0.3)
            pyautogui.click(*self.find_base_btn)
            time.sleep(0.3)
            if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
                self.log(f"Army screen found! Attacking with {self.just_attack_timer.get()}s timeout...")
                self.perform_attack(self.just_attack_timer.get())
                self.current_coord_index = 0
                self.log("Just Attack completed, returning immediately...")
                pyautogui.click(*self.return_home_btn)
                time.sleep(5)
        except Exception as e:
            self.log(f"Error in farming loop: {str(e)}")    
        #4
        try:
            
            if self.check_for_errors():
                self.log("Error handled, continuing...")
            self.log("Starting Just Attack...")
            pyautogui.click(*self.fight_btn_failsafe)
            time.sleep(0.01)
            pyautogui.click(*self.fight_btn)
            time.sleep(0.3)
            pyautogui.click(*self.find_base_btn)
            time.sleep(0.3)
            if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
                self.log(f"Army screen found! Attacking with {self.just_attack_timer.get()}s timeout...")
                self.perform_attack(self.just_attack_timer.get())
                self.current_coord_index = 0
                self.log("Just Attack completed, returning immediately...")
                pyautogui.click(*self.return_home_btn)
                time.sleep(5)
        except Exception as e:
            self.log(f"Error in farming loop: {str(e)}")    
        #5
        try:
            
            if self.check_for_errors():
                self.log("Error handled, continuing...")
            self.log("Starting Just Attack...")
            pyautogui.click(*self.fight_btn_failsafe)
            time.sleep(0.01)
            pyautogui.click(*self.fight_btn)
            time.sleep(0.3)
            pyautogui.click(*self.find_base_btn)
            time.sleep(0.3)
            if self.wait_for_image_timeout(self.army_imgs, confidence=0.6, timeout=60):
                self.log(f"Army screen found! Attacking with {self.just_attack_timer.get()}s timeout...")
                self.perform_attack(self.just_attack_timer.get())
                self.current_coord_index = 0
                self.log("Just Attack completed, returning immediately...")
                pyautogui.click(*self.return_home_btn)
                time.sleep(5)
        except Exception as e:
            self.log(f"Error in farming loop: {str(e)}")    
        
    def attack_right_now(self):
        self.log("Deploying troops immediately...")
        time.sleep(3)
        self.deploy_all()
        self.current_coord_index = 0
        self.log("Troops deployed.")

    def deploy_all(self):
        self.spell_coordinates_to_use = random.choice([self.spell_coordinates, self.spell_coordinates_different])

        for key, count in self.spells.items():
            if self.stop_requested:
                return
            self.log(f"Deploying Spell: {key} with {count} clicks")
            self.current_coord_index = 0
            keyboard.press_and_release(key)
            for _ in range(count):
                if self.stop_requested:
                    return
                self.click_next_coordinate(self.spell_coordinates_to_use)
            
        self.troop_coordinates_to_use = random.choice([self.troop_coordinates, self.troop_coordinates_different])    

        for key, count in self.troops.items():
            if self.stop_requested:
                return
            self.log(f"Deploying Troop: {key} with {count} clicks")
            self.current_coord_index = 0
            keyboard.press_and_release(key)
            for _ in range(count):
                if self.stop_requested:
                    return
                self.click_next_coordinate(self.troop_coordinates_to_use)

        for key in self.cc:
            if self.stop_requested:
                return
            self.log(f"Deploying Clan Castle: {key}")
            self.current_coord_index = 0
            keyboard.press_and_release(key)
            self.click_next_coordinate(self.CC_coordinates)

        for i, key in enumerate(self.heroes):
            if self.stop_requested:
                return
            self.log(f"Deploying Hero: {key}")
            keyboard.press_and_release(key)
            if self.hero_coordinates:
                coord_index = i % len(self.hero_coordinates)
                x, y = self.hero_coordinates[coord_index]
                pyautogui.click(x, y)
                time.sleep(0.5)
            else:
                x, y = self.troop_coordinates[0]
                pyautogui.click(x, y)
                time.sleep(0.5)
            keyboard.press_and_release(key)
            time.sleep(2.1)

    def perform_attack(self, timeout):
        self.deploy_all()
        self.wait_for_battle_end_or_timeout(timeout)

    def wait_for_battle_end_or_timeout(self, timeout):
        start_time = time.time()
        self.log(f"Waiting {timeout}s or until battle ends...")
        while time.time() - start_time < timeout:
            if self.stop_requested:
                return
            elapsed = int(time.time() - start_time)
            self.log(f"Waiting {timeout-elapsed}s or until battle ends...", update_timeout=True)
    
            # Check Return Home
            try:
                if pyautogui.locateOnScreen(self.return_home_img, confidence=0.8):
                    self.log("Return Home detected. Clicking...")
                    pyautogui.click(*self.return_home_btn)
                    time.sleep(3)
                    return
            except pyautogui.ImageNotFoundException:
                pass
    
            # Check Return with Chest
            try:
                if pyautogui.locateOnScreen(self.return_with_chest_img, confidence=0.7):
                    self.log("Return with Chest detected. Waiting 6 sec then clicking 7 times...")
                    pyautogui.click(*self.return_with_chest_btn)
                    time.sleep(6)
                    for _ in range(9):
                        pyautogui.click(*self.return_with_chest_btn)
                        time.sleep(1)
                    return
            except pyautogui.ImageNotFoundException:
                pass
    
            time.sleep(0.5)
    
        # Timeout reached
        self.log("Timeout reached. Surrendering...")
        pyautogui.click(*self.surrender_btn)
        time.sleep(1)
        pyautogui.click(*self.confirm_btn)
        time.sleep(1)
        pyautogui.click(*self.return_home_btn)
        time.sleep(1)
    
        # Timeout reached
        self.log("Timeout reached. Surrendering...")
        pyautogui.click(*self.surrender_btn)
        time.sleep(1)
        pyautogui.click(*self.confirm_btn)
        time.sleep(1)
        pyautogui.click(*self.return_home_btn)
        time.sleep(1)

    def surrender(self):
        self.log("Surrendering...")
        pyautogui.click(*self.surrender_btn)
        time.sleep(0.3)
        pyautogui.click(*self.confirm_btn)
        time.sleep(0.3)
        pyautogui.click(*self.return_home_btn)
        time.sleep(0.5)

    def manual_ocr(self):
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path.get()
        self.log("Performing manual OCR...")
        try:
            img_gold = ImageGrab.grab(bbox=self.gold_coords)
            img_elixir = ImageGrab.grab(bbox=self.elixir_coords)
            img_dark_elixir = ImageGrab.grab(bbox=self.dark_elixir_coords)
            
            text_gold = pytesseract.image_to_string(img_gold)
            text_elixir = pytesseract.image_to_string(img_elixir)
            text_dark_elixir = pytesseract.image_to_string(img_dark_elixir)
            
            gold_value = int(''.join(filter(str.isdigit, text_gold))) if text_gold.strip() else 0
            elixir_value = int(''.join(filter(str.isdigit, text_elixir))) if text_elixir.strip() else 0
            dark_elixir_value = int(''.join(filter(str.isdigit, text_dark_elixir))) if text_dark_elixir.strip() else 0
            
            self.log(f"Gold: {gold_value}")
            self.log(f"Elixir: {elixir_value}")
            self.log(f"Dark Elixir: {dark_elixir_value}")
        except Exception as e:
            self.log(f"OCR failed: {str(e)}")

    def check_for_errors(self):
        for image_path in self.error_images:
            try:
                if pyautogui.locateOnScreen(image_path, confidence=0.5):
                    self.log(f"Error detected with {os.path.basename(image_path)}. Resolving...")
                    pyautogui.click(626, 615)
                    time.sleep(7)
                    return True
            except pyautogui.ImageNotFoundException:
                continue
        return False

    def wait_for_image_timeout(self, image_paths, confidence=0.8, timeout=60):
        if not image_paths:
            self.log("No images to wait for.")
            return False
        self.log(f"Waiting for any of the images: {[os.path.basename(path) for path in image_paths]} (timeout {timeout}s)...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.stop_requested:
                return False
            for image_path in image_paths:
                try:
                    if pyautogui.locateOnScreen(image_path, confidence=confidence):
                        self.log(f"Found {os.path.basename(image_path)}")
                        return True
                except pyautogui.ImageNotFoundException:
                    pass
            time.sleep(0.5)
        self.log(f"Timeout waiting for any of the images")
        return False

    def get_loot_from_screen(self):
        try:
            img_gold = ImageGrab.grab(bbox=self.gold_coords)
            img_elixir = ImageGrab.grab(bbox=self.elixir_coords)
            img_dark_elixir = ImageGrab.grab(bbox=self.dark_elixir_coords)
            
            text_gold = pytesseract.image_to_string(img_gold)
            text_elixir = pytesseract.image_to_string(img_elixir)
            text_dark_elixir = pytesseract.image_to_string(img_dark_elixir)
            
            gold_value = int(''.join(filter(str.isdigit, text_gold))) if text_gold.strip() else 0
            elixir_value = int(''.join(filter(str.isdigit, text_elixir))) if text_elixir.strip() else 0
            dark_elixir_value = int(''.join(filter(str.isdigit, text_dark_elixir))) if text_dark_elixir.strip() else 0
            
            self.log(f"Gold: {gold_value} | Elixir: {elixir_value} | Dark Elixir: {dark_elixir_value}")
            
            for tier in range(1, 4):
                if (gold_value >= self.tiers[tier]['thresholds']['gold'] or
                    elixir_value >= self.tiers[tier]['thresholds']['elixir'] or
                    dark_elixir_value >= self.tiers[tier]['thresholds']['dark_elixir']):
                    return self.tiers[tier]['time']
            return 0
        except Exception as e:
            self.log(f"Error analyzing loot: {str(e)}")
            return 0

    def click_next_coordinate(self, coord_list):
        if coord_list:
            x, y = coord_list[self.current_coord_index]
            pyautogui.click(x, y)
            self.current_coord_index = (self.current_coord_index + 1) % len(coord_list)
            time.sleep(0.001)

    def edit_thresholds(self):
        thresholds_window = tk.Toplevel(self.root)
        thresholds_window.title("Edit Loot Thresholds")
        thresholds_window.geometry("400x600")
        thresholds_window.transient(self.root)
        thresholds_window.grab_set()
        
        tier_entries = []
        for tier in range(1, 4):
            tier_frame = ttk.LabelFrame(thresholds_window, text=f"Tier {tier}")
            tier_frame.pack(pady=5, fill=tk.X, padx=10)
            
            ttk.Label(tier_frame, text="Gold Threshold:").grid(row=0, column=0, sticky=tk.W)
            gold_entry = ttk.Entry(tier_frame, width=10)
            gold_entry.insert(0, str(self.tiers[tier]['thresholds']['gold']))
            gold_entry.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(tier_frame, text="Elixir Threshold:").grid(row=1, column=0, sticky=tk.W)
            elixir_entry = ttk.Entry(tier_frame, width=10)
            elixir_entry.insert(0, str(self.tiers[tier]['thresholds']['elixir']))
            elixir_entry.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(tier_frame, text="Dark Elixir Threshold:").grid(row=2, column=0, sticky=tk.W)
            dark_elixir_entry = ttk.Entry(tier_frame, width=10)
            dark_elixir_entry.insert(0, str(self.tiers[tier]['thresholds']['dark_elixir']))
            dark_elixir_entry.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Label(tier_frame, text="Attack Time (sec):").grid(row=3, column=0, sticky=tk.W)
            time_entry = ttk.Entry(tier_frame, width=10)
            time_entry.insert(0, str(self.tiers[tier]['time']))
            time_entry.grid(row=3, column=1, padx=5, pady=2)
            
            tier_entries.append({
                'gold': gold_entry,
                'elixir': elixir_entry,
                'dark_elixir': dark_elixir_entry,
                'time': time_entry
            })
        
        def save_thresholds():
            try:
                for tier in range(1, 4):
                    self.tiers[tier]['thresholds']['gold'] = int(tier_entries[tier-1]['gold'].get())
                    self.tiers[tier]['thresholds']['elixir'] = int(tier_entries[tier-1]['elixir'].get())
                    self.tiers[tier]['thresholds']['dark_elixir'] = int(tier_entries[tier-1]['dark_elixir'].get())
                    self.tiers[tier]['time'] = int(tier_entries[tier-1]['time'].get())
                self.log("Loot thresholds updated")
                thresholds_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "All values must be integers")
        
        ttk.Button(thresholds_window, text="Save", command=save_thresholds).pack(pady=10)

    def edit_troops(self):
        troops_window = tk.Toplevel(self.root)
        troops_window.title("Edit Troop Deployment Keys")
        troops_window.geometry("400x500")
        troops_window.transient(self.root)
        troops_window.grab_set()
        
        ttk.Label(troops_window, text="Troop Keys and Counts (e.g., 1:10,2:5):").pack(pady=5)
        troops_entry = ttk.Entry(troops_window, width=20)
        troops_entry.insert(0, ",".join([f"{k}:{v}" for k, v in self.troops.items()]))
        troops_entry.pack(pady=5)
        
        ttk.Label(troops_window, text="Hero Keys (comma separated):").pack(pady=5)
        heroes_entry = ttk.Entry(troops_window, width=20)
        heroes_entry.insert(0, ",".join(self.heroes))
        heroes_entry.pack(pady=5)
        
        ttk.Label(troops_window, text="Spell Keys and Counts (e.g., a:2,b:3):").pack(pady=5)
        spells_entry = ttk.Entry(troops_window, width=20)
        spells_entry.insert(0, ",".join([f"{k}:{v}" for k, v in self.spells.items()]))
        spells_entry.pack(pady=5)
        
        ttk.Label(troops_window, text="Clan Castle Key:").pack(pady=5)
        cc_entry = ttk.Entry(troops_window, width=20)
        cc_entry.insert(0, ",".join(self.cc))
        cc_entry.pack(pady=5)
        
        def save_keys():
            try:
                troops_str = troops_entry.get()
                self.troops = {k.strip(): int(v.strip()) for k, v in (item.split(":") for item in troops_str.split(",") if item.strip())}
            except ValueError:
                messagebox.showerror("Invalid Input", "Troops must be in format key:count, e.g., 1:10,2:5")
                return
            
            self.heroes = [k.strip() for k in heroes_entry.get().split(",") if k.strip()]
            
            try:
                spells_str = spells_entry.get()
                self.spells = {k.strip(): int(v.strip()) for k, v in (item.split(":") for item in spells_str.split(",") if item.strip())}
            except ValueError:
                messagebox.showerror("Invalid Input", "Spells must be in format key:count, e.g., a:2,b:3")
                return
            
            self.cc = [k.strip() for k in cc_entry.get().split(",") if k.strip()]
            self.log(f"Updated keys: Troops={self.troops}, Heroes={self.heroes}, Spells={self.spells}, CC={self.cc}")
            troops_window.destroy()
        
        ttk.Button(troops_window, text="Save", command=save_keys).pack(pady=10)

    def edit_coordinates(self):
        coords_window = tk.Toplevel(self.root)
        coords_window.title("Edit Game Coordinates")
        coords_window.geometry("450x600")
        coords_window.resizable(True, True)
        coords_window.transient(self.root)
        coords_window.grab_set()
        
        canvas = tk.Canvas(coords_window)
        scrollbar = ttk.Scrollbar(coords_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def create_coord_entry(parent, label_text, coord_tuple, row):
            ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            x_entry = ttk.Entry(parent, width=5)
            x_entry.insert(0, str(coord_tuple[0]))
            x_entry.grid(row=row, column=1, padx=2)
            y_entry = ttk.Entry(parent, width=5)
            y_entry.insert(0, str(coord_tuple[1]))
            y_entry.grid(row=row, column=2, padx=2)
            return (x_entry, y_entry)
        
        ttk.Label(scrollable_frame, text="Game Button Coordinates").grid(row=0, column=0, columnspan=3, pady=10)
        coords_frame = ttk.Frame(scrollable_frame)
        coords_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        entries = {}
        entries["fight"] = create_coord_entry(coords_frame, "Fight Button:", self.fight_btn, 1)
        entries["find"] = create_coord_entry(coords_frame, "Find Base Button:", self.find_base_btn, 2)
        entries["surrender"] = create_coord_entry(coords_frame, "Surrender Button:", self.surrender_btn, 3)
        entries["confirm"] = create_coord_entry(coords_frame, "Confirm Button:", self.confirm_btn, 4)
        entries["return"] = create_coord_entry(coords_frame, "Return Home Button:", self.return_home_btn, 5)
        entries["next"] = create_coord_entry(coords_frame, "Next Button:", self.next_btn, 6)
        
        ttk.Label(scrollable_frame, text="Resource Coordinates (x1, y1, x2, y2)").grid(row=2, column=0, columnspan=3, pady=10)
        resources_frame = ttk.Frame(scrollable_frame)
        resources_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        ttk.Label(resources_frame, text="Gold Area:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        gold_x1 = ttk.Entry(resources_frame, width=5)
        gold_x1.insert(0, str(self.gold_coords[0]))
        gold_x1.grid(row=1, column=1, padx=2)
        gold_y1 = ttk.Entry(resources_frame, width=5)
        gold_y1.insert(0, str(self.gold_coords[1]))
        gold_y1.grid(row=1, column=2, padx=2)
        gold_x2 = ttk.Entry(resources_frame, width=5)
        gold_x2.insert(0, str(self.gold_coords[2]))
        gold_x2.grid(row=1, column=3, padx=2)
        gold_y2 = ttk.Entry(resources_frame, width=5)
        gold_y2.insert(0, str(self.gold_coords[3]))
        gold_y2.grid(row=1, column=4, padx=2)
        
        ttk.Label(resources_frame, text="Elixir Area:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        elixir_x1 = ttk.Entry(resources_frame, width=5)
        elixir_x1.insert(0, str(self.elixir_coords[0]))
        elixir_x1.grid(row=2, column=1, padx=2)
        elixir_y1 = ttk.Entry(resources_frame, width=5)
        elixir_y1.insert(0, str(self.elixir_coords[1]))
        elixir_y1.grid(row=2, column=2, padx=2)
        elixir_x2 = ttk.Entry(resources_frame, width=5)
        elixir_x2.insert(0, str(self.elixir_coords[2]))
        elixir_x2.grid(row=2, column=3, padx=2)
        elixir_y2 = ttk.Entry(resources_frame, width=5)
        elixir_y2.insert(0, str(self.elixir_coords[3]))
        elixir_y2.grid(row=2, column=4, padx=2)
        
        ttk.Label(resources_frame, text="Dark Elixir:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        dark_x1 = ttk.Entry(resources_frame, width=5)
        dark_x1.insert(0, str(self.dark_elixir_coords[0]))
        dark_x1.grid(row=3, column=1, padx=2)
        dark_y1 = ttk.Entry(resources_frame, width=5)
        dark_y1.insert(0, str(self.dark_elixir_coords[1]))
        dark_y1.grid(row=3, column=2, padx=2)
        dark_x2 = ttk.Entry(resources_frame, width=5)
        dark_x2.insert(0, str(self.dark_elixir_coords[2]))
        dark_x2.grid(row=3, column=3, padx=2)
        dark_y2 = ttk.Entry(resources_frame, width=5)
        dark_y2.insert(0, str(self.dark_elixir_coords[3]))
        dark_y2.grid(row=3, column=4, padx=2)
        
        ttk.Label(scrollable_frame, text="Troop Deployment Coordinates (one per line, x,y):").grid(row=4, column=0, columnspan=3, pady=10)
        troop_coords_text = tk.Text(scrollable_frame, height=10, width=40)
        troop_coords_text.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
        for x, y in self.troop_coordinates:
            troop_coords_text.insert(tk.END, f"{x},{y}\n")
        
        ttk.Label(scrollable_frame, text="Spell Deployment Coordinates (one per line, x,y):").grid(row=6, column=0, columnspan=3, pady=10)
        spell_coords_text = tk.Text(scrollable_frame, height=10, width=40)
        spell_coords_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5)
        for x, y in self.spell_coordinates:
            spell_coords_text.insert(tk.END, f"{x},{y}\n")
        
        ttk.Label(scrollable_frame, text="Hero Deployment Coordinates (one per line, x,y):").grid(row=8, column=0, columnspan=3, pady=10)
        hero_coords_text = tk.Text(scrollable_frame, height=10, width=40)
        hero_coords_text.grid(row=9, column=0, columnspan=3, padx=10, pady=5)
        for x, y in self.hero_coordinates:
            hero_coords_text.insert(tk.END, f"{x},{y}\n")
        
        ttk.Label(scrollable_frame, text="Just Attack Timer (seconds):").grid(row=10, column=0, columnspan=2, pady=10)
        just_attack_timer_entry = ttk.Entry(scrollable_frame, width=10)
        just_attack_timer_entry.insert(0, str(self.just_attack_timer.get()))
        just_attack_timer_entry.grid(row=10, column=2, padx=10, pady=5)
        
        ttk.Button(scrollable_frame, text="Save Coordinates", command=lambda: save_coords()).grid(row=11, column=0, columnspan=3, pady=10)
        
        def save_coords():
            try:
                self.fight_btn = (int(entries["fight"][0].get()), int(entries["fight"][1].get()))
                self.find_base_btn = (int(entries["find"][0].get()), int(entries["find"][1].get()))
                self.surrender_btn = (int(entries["surrender"][0].get()), int(entries["surrender"][1].get()))
                self.confirm_btn = (int(entries["confirm"][0].get()), int(entries["confirm"][1].get()))
                self.return_home_btn = (int(entries["return"][0].get()), int(entries["return"][1].get()))
                self.next_btn = (int(entries["next"][0].get()), int(entries["next"][1].get()))
                
                self.gold_coords = (int(gold_x1.get()), int(gold_y1.get()), int(gold_x2.get()), int(gold_y2.get()))
                self.elixir_coords = (int(elixir_x1.get()), int(elixir_y1.get()), int(elixir_x2.get()), int(elixir_y2.get()))
                self.dark_elixir_coords = (int(dark_x1.get()), int(dark_y1.get()), int(dark_x2.get()), int(dark_y2.get()))
                
                troop_coords_lines = troop_coords_text.get("1.0", tk.END).strip().split("\n")
                self.troop_coordinates = [tuple(map(int, line.split(","))) for line in troop_coords_lines if line.strip()]
                
                spell_coords_lines = spell_coords_text.get("1.0", tk.END).strip().split("\n")
                self.spell_coordinates = [tuple(map(int, line.split(","))) for line in spell_coords_lines if line.strip()]
                
                hero_coords_lines = hero_coords_text.get("1.0", tk.END).strip().split("\n")
                self.hero_coordinates = [tuple(map(int, line.split(","))) for line in hero_coords_lines if line.strip()]
                
                self.just_attack_timer.set(int(just_attack_timer_entry.get()))
                
                self.log("Coordinates and settings updated successfully")
                coords_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "All coordinates and timer must be numbers")
        
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CocAutoFarmerGUI(root)
#     root.protocol("WM_DELETE_WINDOW", root.quit)
#     root.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    app = CocAutoFarmerGUI(root)
    root.protocol("WM_DELETE_WINDOW", root.quit)

    # --- auto-refresh section ---
    def refresh_hotkeys():
        try:
            keyboard.unhook_all_hotkeys()
            app.setup_keybindings()
            print("Hotkeys refreshed ✅")
        except Exception as e:
            print(f"Hotkey refresh failed ❌: {e}")
        root.after(60000, refresh_hotkeys)  # run again in 60 s

    refresh_hotkeys()        # start periodic refresh
    # --- end section ---

    root.mainloop()
