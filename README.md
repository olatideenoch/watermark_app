# 📸 Watermark App (Tkinter + Pillow)

A simple and powerful desktop watermarking application built with **Python, Tkinter, and Pillow**.
This app allows users to upload an image, apply a fully customizable text watermark, and save the final watermarked image.

---

## ✨ Features

- Add customizable **text watermarks** to any image  
- Choose from multiple **fonts**, **colors**, and **text sizes**  
- Adjust watermark **transparency**, **position**, and **alignment**  
- Automatically detects and displays **image dimensions**  
- Supports common image formats: PNG, JPG, JPEG, BMP, GIF  
- Preview watermark directly inside the app  
- Save the final watermarked image to your computer  
- Lightweight, offline, cross-platform (Windows / Mac)

---

## 📸 Screenshot  
*(`/Demo/watermark_app_demo.jpg`)*

---

## 🛠️ Installation

### 1. Clone the repository  
```bash
git clone https://github.com/olatideenoch/Watermark_Generator_App.git
cd Watermark_Generator_App
```
## Install dependencies
```bash
pip install pillow
```
## Run the application
```bash
python main.py
```
---

## 🖥️ Cross-Platform Font Support

The project includes **Windows font paths** by default.
For macOS users, a commented-out macOS font map is included inside save_img() they can simply uncomment it.

---

## 📝 Known Limitations

• Watermark preview may not match exact pixel scaling (due to canvas resizing)
• Rotated text might shift slightly depending on font metrics
• Font availability depends on the OS

---

## 🤝 Contributions

Pull requests are welcome!
• Submit Pull Requests(PRs)
• Report issues
• Suggest new features

---

## 📄 Licensing

The project is open-source under the MIT License

---

## ⭐ A Note from the Creator

This Watermark App was built to combine simplicity with professional-level watermarking features — clean, intuitive, and effective.

If you use it or improve it, consider giving the project a ⭐ on GitHub!
