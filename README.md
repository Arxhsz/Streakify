![enter image description here](https://github.com/Arxhsz/Streakify/blob/main/logo.png?raw=true)
![enter image description here](https://github.com/Arxhsz/Streakify/blob/main/image.png?raw=true)
# Streakify

**Streakify** is a sleek desktop application that automates the restoration of your Snapchat streaks. Built with Python, undetected-chromedriver, and Tkinter for a lightweight GUI, Streakify makes it easy to submit a streak restore request without leaving your desktop.

----------


## 🚀 Features

-   **Automated Form Submission**: Fills in your Snapchat username, email, phone number, and friend’s username in a human-like fashion.
    
-   **Customizable Browser Window**: Launch Chrome on a secondary monitor with preset position and size.
    
-   **Built-in Logging**: Real-time logs of each step in the GUI.
    
-   **Settings Panel**: Adjust window position, size, and clear logs.
    
-   **Single-File Distribution**: Available as a standalone EXE for Windows.
    
-   **Custom Icons**: Modern iconography in the taskbar and title bar.

 

# 

# *!!IMPORTANT!!*
***This application does not save or export any sensitive information if you are hesitant to use this app because you think your data will be stolen don't just have a look at the source code.***

## 🛠️ Requirements

-   Python 3.8+
    
-   Windows 10 or later
    
-   [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
    
-   [selenium](https://pypi.org/project/selenium/)
    

----------

## 💾 Installation

### 1. Using the Windows Installer

Download the `Streakify_Setup.exe` from the [Releases](https://github.com/<your-username>/Streakify/releases) page and run the installer. This will automatically install Streakify and create shortcuts.

### 2. From Source

1.  Clone the repository:
    
    ```
    git clone https://github.com/<your-username>/Streakify.git
    cd Streakify
    ```
    
2.  Create and activate a virtual environment:
    
    ```
    python -m venv .venv
    .venv\\Scripts\\activate        # Windows
    source .venv/bin/activate         # macOS/Linux
    ```
    
3.  Install dependencies:
    
    ```
    pip install -r requirements.txt
    ```
    
4.  Run the application:
    
    ```
    python Streak_Restore.py
    ```
    

----------

## 🎮 Usage

1.  Launch Streakify from your Start Menu or desktop shortcut.
    
2.  Enter your Snapchat **Username**, **Email**, **Phone Number**, and **Friend's Username**.
    
3.  Click **Restore Streak**.
    
4.  Watch the log at the bottom for progress and success/error messages.
    

----------

## ⚙️ Configuration

Open **Settings → Window Position/Size…** to adjust where Chrome opens on your secondary monitor. Save and retry as needed.

----------

## 🛟 Troubleshooting & Common Errors

-   **Error 1: Please verify you are human**  
    _Fix_: Wait a moment and try again—sometimes the CAPTCHA bypass needs extra time.
    
-   **Error 2: Invalid email**  
    _Fix_: Ensure your email includes at least one `@` and a valid domain like `.com`, `.co`, etc.
    
-   **Error 3: Username must be 3 characters**  
    _Fix_: Your Snapchat username must be at least 3 letters long.
    
-   **Error 4: Friend's username must be 3 characters**  
    _Fix_: Your friend’s Snapchat username must be at least 3 characters long.
    
-   **Error 5: Phone must be 10 digits**  
    _Fix_: Enter exactly 10 digits (numbers only) with no spaces or symbols.
    

----------

## 🤝 Contributing

1.  Fork the repository.
    
2.  Create your feature branch:
    
    ```
    git checkout -b feature/MyFeature
    ```
    
3.  Commit your changes:
    
    ```
    git commit -m "Add MyFeature"
    ```
    
4.  Push to the branch:
    
    ```
    git push origin feature/MyFeature
    ```
    
5.  Submit a pull request.
    

Please ensure your code adheres to PEP8 and include relevant tests.

----------

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

----------

## 📞 Contact

Created by [Arxhsz](https://github.com/Arxhsz). Feel free to open issues or contact me for anything!
