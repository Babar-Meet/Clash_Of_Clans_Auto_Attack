# 🏰 Clash of Clans Auto Farmer

A simple program that helps automate farming in Clash of Clans! 🤖

## What It Does

This program automatically:
- Finds enemy bases to attack 🎯
- Checks if they have good loot 💰
- Deploys your troops and spells ⚔️
- Collects resources for you 🏆
- Returns home when done 🏠

## ⚠️ Important Notes

**Use this at your own risk!** 
- This is for educational purposes only
- Using automation tools may violate game rules
- I'm not responsible for any account issues

## 🚀 Quick Start

### What You Need:
- Windows computer
- Clash of Clans on BlueStacks or similar
- Python installed

### Easy Setup:

1. **Download all files** to a folder

2. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Run installer and check "Add to PATH"
   - Program will find it automatically

4. **Run the program**:
   ```bash
   python Clash_Auto_Attack.py
   ```

## 🎮 How to Use

1. **Setup**:
   - Make sure Clash of Clans is open on your emulator
   - Set up your army with troops and spells
   - Configure the program settings

2. **Basic Controls**:
   - **Start**: Begins automatic farming
   - **Stop**: Stops the program
   - **Just Attack**: Does one quick attack
   - **Surrender**: Ends current battle
   - **Attack Right Now**: Deploys troops immediately
   - **Loot Bonus**: Quick attack sequence

3. **Hotkeys** (quick keys):
   - `Ctrl+Shift+Enter`: Start farming
   - `Ctrl+Shift+Backspace`: Stop farming
   - `Ctrl+Shift+A`: Attack right now
   - `Ctrl+Shift+S`: Surrender
   - `Ctrl+Shift+J`: Just attack
   - `Ctrl+Shift+F`: Find base only

## ⚙️ Configuration

You can customize:
- **Troop deployment**: Which troops to use and how many (Mass E-drag Wroks All the Time)
- **Attack timing**: How long to attack for
- **Loot thresholds**: Only attack bases with good loot
- **Coordinates**: Where to click on screen
- **Army composition**: Set your troop keys and counts

## 🛠️ Troubleshooting

**Common issues:**
- Make sure game window is visible
- Check that coordinates match your screen
- Verify required images are in the `img` folder
- Ensure Tesseract OCR is installed
- Run as Administrator if hotkeys don't work

**Hotkeys not working?**
- Program auto-refreshes hotkeys every 60 seconds
- Try running as Administrator
- Check if other programs are using same hotkeys

## 📁 Files Needed

- `Clash_Auto_Attack.py` - Main program
- `requirements.txt` - Python packages
- `img/` folder with game images
- `Tesseract-OCR/` for text reading

## 🔧 Requirements

Install all needed packages:
```bash
pip install pytesseract pyautogui keyboard Pillow mouse
```

## ❓ Need Help?

- Check that all images are in the `img` folder
- Make sure Tesseract is installed and in PATH
- Adjust coordinates for your screen resolution
- Start with "Just Attack" to test before full farming

---

**Remember**: Use responsibly and have fun! 🎮✨
