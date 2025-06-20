# Study With Style - PUP Merchandise App

Ang **Study With Style** is a e-commerce mobile application na binuo gamit ang Kivy framework ng Python. This is a sample online store para sa pagbenta ng mga merchandise na may temang PUP (Polytechnic University of the Philippines).


## Mga Features

*   **User Authentication:** Secure na pag-login at pag-register para sa mga user.
*   **Admin Role:** Special na 'admin' user na may access sa inventory management.
*   **Product Browsing:** Tingnan mga products, kasama ang "Best Seller" section.
*   **Shopping Cart:** Magdagdag, magbawas, or mag-remove ng mga product sa cart.
*   **Inventory Management (Admin Only):** Mag-add, mag-update, and mag-delete ng mga product, kasama ang pag-upload ng product images.
*   **Checkout System:** I-place yung order, na nagbabawas ng stock mula sa inventory.
*   **Profile Management:** I-update ang personal info tulad ng address at contact number.
*   **Order History:** Tingnan ang mga nakaraang order (basic implementation).

## Tech Stack

*   **Framework:** Kivy (Python)
*   **Database:** SQLite3
*   **Password Hashing:** Werkzeug (with a fallback to hashlib) MICO's IDEA?

---

## How to setup and run

ito yunga mga step para i-run ang application sa iyong computer. (Or just download the APK file from the [Releases])

### for LINUX


**Step 1: clone Repository**
Buksan ang iyong terminal at i-clone ang project.
```bash
git clone https://github.com/Golgrax/Study-With-Style---PUP-Merchandise-App.git
cd Study-With-Style---PUP-Merchandise-App.git
```

**Step 2: Gumawa ng Virtual Environment**
Magandang practice na gumamit ng virtual environment para sa mga Python projects.
```bash
python3 -m venv venv
source venv/bin/activate
```
Makikita mo ang `(venv)` sa simula ng iyong terminal prompt.

**Step 3: I-install ang mga Dependencies**
I-install muna ang Kivy at ang mga system libraries na kailangan nito.
```bash
# Para sa mga system dependencies ng Kivy
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

pip install -r requirements.txt
```

**Step 4: I-setup ang Database at Gumawa ng Admin User**
Ito ay kailangan lang gawin sa unang beses.
```bash
# Papatakbuhin nito ang script para gumawa ng tables at admin user
python create_admin.py
```
*   **Admin Username:** `admin`
*   **Admin Password:** `admin`

**Step 5: Patakbuhin ang Main Application**
Ready ka na!
```bash
python main.py
```

### Para sa mga **Windows** Users

Medyo iba ang pag-install ng Kivy sa Windows.

**Step 1: I-clone ang Repository**
Gamit ang Git Bash, Command Prompt, o PowerShell.
```bash
git clone https://github.com/Golgrax/Study-With-Style---PUP-Merchandise-App.git
cd Study-With-Style---PUP-Merchandise-App.git
```

**Step 2: Gumawa ng Virtual Environment** (Optional pero I'm recoommending this.)
```bash
python -m venv venv
venv\Scripts\activate
```
Makikita mo ang `(venv)` sa simula ng iyong command prompt.

**Step 3: I-install ang mga Dependencies**
Sa Windows, kailangan mong i-install muna ang Kivy bago ang ibang packages sa `requirements.txt`.
```bash
# I-update ang pip
python -m pip install --upgrade pip

# I-install ang Kivy
python -m pip install kivy[base] kivy_examples

# Ngayon, i-install ang iba pang packages
pip install -r requirements.txt
```

**Step 4: I-setup ang Database at Gumawa ng Admin User**
Kailangan lang gawin sa unang beses.
```bash
# Papatakbuhin nito ang script para gumawa ng tables at admin user
python create_admin.py
```
*   **Admin Username:** `admin`
*   **Admin Password:** `admin`

**Step 5: Patakbuhin ang Main Application**
Ready ka na!
```bash
python main.py
```
