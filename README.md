# Mood-Based Smart Lighting System

This project uses **AI emotion detection** to dynamically change lighting color in real time.  
It uses the webcam feed + the FER model to classify facial expressions and displays a mood-based light panel.

---

## 💡 Features
- Real-time webcam emotion detection
- Smooth mood prediction using a rolling window
- Custom CSV dataset for color mapping
- Dynamic on-screen "Mood Light" display
- Lightweight and completely local (no cloud needed)

---

## 🧠 Tech Stack
- Python
- OpenCV
- FER (Facial Expression Recognition)
- NumPy

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/miguelaj01/mood-based-smart-lighting.git
cd mood-based-smart-lighting
```

### 2. Create a virtual environment
```bash
python -m venv moodlight_env
```

### 3. Activate the environment
**Windows PowerShell**
```bash
.\moodlight_env\Scripts\Activate.ps1
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Program
After activating the virtual environment:

```bash
python mood_light_demo.py
```

- Press **`q`** to quit the program.

---

## 🖼️ Mood Dataset
Colors and moods are fully customizable using the CSV file:

`mood_color_mapping.csv`

---

## 📌 Future Improvements
- Smart bulb integration (Alexa, Philips Hue)
- Full-screen ambiance mode
- Mobile app version
- Multi-modal mood detection (voice, text, posture)

---

## 👤 Author
Michael Irving  
GitHub: [@miguelaj01](https://github.com/miguelaj01)
