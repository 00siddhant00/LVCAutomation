# Batch Lyrics Video Creation Automation System

### Hyper-Efficient Video Automation Suite 🎥✨  
Transform static backgrounds and subtitles into stunning animated lyric videos with ease! This tool automates the creation of videos by seamlessly integrating animated backgrounds, styled text overlays, and subtitle syncing.

---

## **Key Benefits 🚀**
- **Effortless Automation**: Batch process multiple videos without manual intervention.  
- **Dynamic Animations**: Bring static backgrounds to life with "breathing" animations.  
- **Customizable Text Styling**: Add subtitles with shadows, custom fonts, and smooth animations.  
- **High-Quality Output**: Export MP4 videos with professional-grade quality.  
- **Error-Free Workflow**: Automatically detects missing or completed files to avoid duplication.  
- **Set It and Forget It**: Continuous monitoring ensures no pending files are left behind!  

---

## **Desired Result Output**

https://raw.githubusercontent.com/00siddhant00/LVCAutomation/master/output_demo.mp4

---

## **How It Works 📜**
1. **Animated Background**:  
   - Adds a subtle "breathing" effect to static background images using sinusoidal scaling.  

2. **Subtitle Integration**:  
   - Parses `.srt` subtitle files and synchronizes text overlays to exact timings.  

3. **Batch Processing**:  
   - Detects and processes pending `.png` and `.srt` files automatically, generating output videos.  

4. **Error Handling**:  
   - Skips corrupted or incomplete files to ensure smooth processing.  

---

## **Quick Start Guide ⚡**
1. **Installation**:  
   - Clone the repository:  
     ```bash
     git clone https://github.com/00siddhant00/LVCAutomation.git
     cd LVCAutomation
     ```  
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```

2. **Directory Setup**:  
   - Place input files in the `input_files` directory:  
     - Background images: `<video_number>.png` (e.g., `1.png`)  
     - Subtitle files: `<video_number>.srt` (e.g., `1.srt`)  

   - Outputs will be saved to `output_files`.

3. **Font Selection**:  
   - Add your desired `.ttf` font to the root directory (e.g., `arial.ttf`).  

4. **Run the Processor**:  
   - Start batch processing:  
     ```bash
     python main.py
     ```

---

## **Detailed Instructions 🛠️**
### **Input Files**:
- **Background Images**:  
  - Resolution: Recommended size matches video resolution (e.g., 1920x1080).  

- **Subtitle Files**:  
  - Format: `.srt`  
  - Example:  
    ```
    1
    00:00:01,000 --> 00:00:04,000
    This is your first subtitle.
    ```

### **Batch Processor**:
- Monitors the `input_files` directory for new files.  
- Ensures no duplicates are processed.  

---

## **Customization Options 🎨**
- **Breathing Animation**:  
  - Modify amplitude and frequency in `background_animator.py`:  
    ```python
    def animate_background(self, duration, amplitude=0.1, frequency=0.5):
    ```

- **Text Styling**:  
  - Adjust font size, color, and shadow in `text_overlay.py`:  
    ```python
    def __init__(self, font_path, font_size=40, font_color=(255, 255, 255),
                 shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
    ```

- **Batch Interval**:  
  - Change waiting time for new files in `batch_processor.py`:  
    ```python
    time.sleep(30)  # Default: 30 seconds
    ```

---

## **Output Format 📼**
- **File Type**: MP4  
- **Codec**: H.264  
- **Audio Codec**: AAC  
- **Frame Rate**: 30 FPS  

---

## **Why Use This Tool? 🤔**
- **Save Time**: Automate repetitive tasks and focus on creativity.  
- **High Scalability**: Process hundreds of videos in one go!  
- **Professional Results**: Elevate your video quality with minimal effort.  

### **Perfect for Content Creators, Marketers, and Video Enthusiasts!**

---

## **Contact & Support 🧑‍💻**
Feel free to submit issues or feature requests on our [GitHub Issues Page](https://github.com/00siddhant00/LVCAutomation/issues/new).  

**Happy Creating! 🎉**
