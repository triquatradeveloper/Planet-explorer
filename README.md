# Planet Explorer 3D 🌍🚀

Planet Explorer 3D is an interactive Python application that lets you explore planets in stunning 3D! With a custom home menu, beautiful planet thumbnails, and an interactive OpenGL view for each planet, you'll be on a cosmic adventure in no time. ✨

## Features ⭐
- **Custom Home Screen:**  
  Enjoy a stylish menu with a custom banner image and clickable planet thumbnails.
- **3D Planet View:**  
  Click on a planet to see it in a 3D OpenGL view. Rotate the planet by dragging the mouse and zoom in/out using the scroll wheel. 🔄🔍
- **Error Handling:**  
  If a planet image is missing, a placeholder image will be displayed instead.

## Installation 🔧
1. **Clone or Download the Repository:**  
   Get the code on your local machine.
2. **Install Required Packages:**  
   Ensure you have Python 3 installed, then install the following dependencies using pip:
   ```bash
   pip install pygame PyOpenGL PyOpenGL_accelerate
   ```
3. **Add Image Files:**  
   Place the following image files in the same directory as the script:
   - `earth.jpg`
   - `mars.jpg`
   - `jupiter.jpg`
   - `menu_bg.jpg` (for the custom banner on the menu)

   *Tip:* If any file is missing, the code will use a placeholder image.

## Usage 🚀
1. **Run the Application:**  
   Execute the script with:
   ```bash
   python your_script_name.py
   ```
2. **Home Screen:**  
   - View the custom banner and planet thumbnails.
   - Hover over a thumbnail to see a highlighted border.
   - Click on a planet thumbnail to explore its 3D view.
3. **3D Planet View:**  
   - **Rotate:** Click and drag with the left mouse button.
   - **Zoom:** Use the mouse scroll wheel (scroll up to zoom in, scroll down to zoom out).
   - **Return:** Press **ESC** to go back to the home screen.

## Code Overview 📝
- **Home Screen UI:**  
  Displays a custom banner and neatly arranged planet thumbnails with labels and hover effects.
- **3D Planet View:**  
  Uses PyOpenGL to render a textured sphere representing each planet. Interactivity includes rotation and zooming.
- **Error Handling:**  
  Missing image files are handled gracefully by displaying a placeholder image.

## Enjoy Your Journey! 🎉
Explore the cosmos, learn about planets, and have fun with this interactive 3D experience! 🚀🌌
