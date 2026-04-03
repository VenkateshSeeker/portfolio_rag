import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix mobile centering
old_css = """      .right.page {
        display: none;
        position: fixed;
        top: 5vh;
        left: 5vw;
        width: 90vw;
        height: 90vh;
        height: 90dvh;
        z-index: 1500;
        border-radius: 16px;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6);
        overflow: hidden;
      }"""

new_css = """      .right.page {
        display: none;
        position: fixed;
        top: 5vh;
        left: 50%;
        transform: translateX(-50%);
        width: 90vw;
        height: 90vh;
        height: 90dvh;
        z-index: 1500;
        border-radius: 16px;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6);
        overflow: hidden;
      }"""

content = content.replace(old_css, new_css)

# 2. Add an image and popup
old_btn = """  <a href="/data/bandaruvenkateshrao_resume.pdf" download id="resumeDownloadBtn" class="floating-btn download-btn"
    title="Click to download resume">📄</a>
  <button id="contactToggleBtn" class="floating-btn contact-btn" title="Contact Me">✉️</button>"""

new_btn = """  <div id="resume-tooltip" style="position:fixed; bottom: 85px; right: 85px; background: #3b82f6; padding: 10px 15px; border-radius: 8px; color: white; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.4); z-index: 3000; transition: opacity 0.5s; font-family: var(--font-sans); pointer-events: none;">
    Click here to download my resume! 👇
  </div>
  
  <a href="/data/bandaruvenkateshrao_resume.pdf" download id="resumeDownloadBtn" class="floating-btn download-btn"
    title="Click to download resume" style="padding: 0; overflow: hidden; border: 2px solid white;">
    <img src="/data/venkatesh.jpg" alt="Resume" style="width: 100%; height: 100%; object-fit: cover;">
  </a>
  <button id="contactToggleBtn" class="floating-btn contact-btn" title="Contact Me">✉️</button>"""

content = content.replace(old_btn, new_btn)

# 3. Add JS logic for the popup fade out
old_js = """    // Focus input on load
    window.addEventListener('DOMContentLoaded', () => chatInput.focus());"""

new_js = """    // Focus input on load
    window.addEventListener('DOMContentLoaded', () => chatInput.focus());

    // Hide tooltip after 5 seconds
    setTimeout(() => {
      const tooltip = document.getElementById('resume-tooltip');
      if (tooltip) {
        tooltip.style.opacity = '0';
        setTimeout(() => tooltip.remove(), 500);
      }
    }, 5000);"""

content = content.replace(old_js, new_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied")
