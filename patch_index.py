import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the PDF viewer CSS and add the contact form CSS
css_old = """    .pdf-viewer {
      width: 100%;
      height: 100%;
      border: none;
      border-radius: 0 12px 12px 0;
    }

    .floating-btn {
      display: none;
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: rgba(59, 130, 246, 0.6);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      color: white;
      font-size: 24px;
      border: none;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
      z-index: 2000;
      cursor: pointer;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, background 0.2s;
    }"""

css_new = """    .floating-btn {
      display: flex;
      position: fixed;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: rgba(59, 130, 246, 0.6);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      color: white;
      font-size: 24px;
      border: none;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
      z-index: 2000;
      cursor: pointer;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, background 0.2s;
      text-decoration: none;
    }

    .download-btn {
      bottom: 24px;
      right: 24px;
    }

    .contact-btn {
      display: none;
    }

    .contact-page {
      display: flex;
      flex-direction: column;
      padding: 3rem;
      background: var(--paper);
    }

    .contact-header {
      margin-bottom: 2rem;
    }

    .contact-header h2 {
      font-size: 2rem;
      color: #111827;
      margin-bottom: 0.5rem;
    }

    .contact-header p {
      color: #6b7280;
    }

    .contact-form {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .form-group label {
      font-size: 0.9rem;
      font-weight: 600;
      color: #374151;
    }

    .form-group input, .form-group textarea {
      padding: 0.75rem;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      font-family: inherit;
      background: #f9fafb;
      transition: border-color 0.2s;
    }

    .form-group input:focus, .form-group textarea:focus {
      outline: none;
      border-color: #3b82f6;
      background: white;
    }

    .contact-submit {
      padding: 0.85rem;
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.2s;
    }

    .contact-submit:hover {
      background: #2563eb;
    }

    .contact-submit:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }

    .contact-status {
      text-align: center;
      font-size: 0.9rem;
      font-weight: 500;
      min-height: 20px;
    }
    .status-success { color: #10b981; }
    .status-error { color: #ef4444; }"""

content = content.replace(css_old, css_new)

# 2. Replace media query logic
media_old = """      .pdf-viewer {
        border-radius: 16px;
      }

      .floating-btn {
        display: flex;
        top: calc(5vh + 16px);
        bottom: auto;
        right: calc(5vw + 16px);
      }"""

media_new = """      .contact-page {
        padding: 1.5rem;
        overflow-y: auto;
      }

      .contact-btn {
        display: flex;
        top: calc(5vh + 16px);
        right: calc(5vw + 16px);
      }

      .download-btn {
        bottom: calc(5vh + 16px);
        right: calc(5vw + 16px);
      }"""

content = content.replace(media_old, media_new)

# 3. Replace right page HTML
html_old = """      <div class="page right" style="padding: 0;">
        <iframe src="/data/bandaruvenkateshrao_resume.pdf" class="pdf-viewer" title="Resume PDF"></iframe>
      </div>"""

html_new = """      <div class="page right contact-page">
        <div class="contact-header">
          <h2>Contact Venkatesh</h2>
          <p>Have a question or a proposal? Shoot me a message!</p>
        </div>
        <form id="contactForm" class="contact-form">
          <div class="form-group">
            <label for="contactName">Name</label>
            <input type="text" id="contactName" required placeholder="John Doe">
          </div>
          <div class="form-group">
            <label for="contactEmail">Email</label>
            <input type="email" id="contactEmail" required placeholder="john@example.com">
          </div>
          <div class="form-group">
            <label for="contactMessage">Message</label>
            <textarea id="contactMessage" rows="5" required placeholder="Hello Venkatesh, I'd like to..."></textarea>
          </div>
          <button type="submit" id="contactSubmit" class="contact-submit">Send Message 🚀</button>
          <div id="contactStatus" class="contact-status"></div>
        </form>
      </div>"""

content = content.replace(html_old, html_new)

# 4. Replace floating button
btn_old = """  <button id="resumeToggleBtn" class="floating-btn">📄</button>"""

btn_new = """  <a href="/data/bandaruvenkateshrao_resume.pdf" download id="resumeDownloadBtn" class="floating-btn download-btn" title="Click to download resume">📄</a>
  <button id="contactToggleBtn" class="floating-btn contact-btn" title="Contact Me">✉️</button>"""

content = content.replace(btn_old, btn_new)

# 5. Replace Javascript
js_old = """    // Mobile Resume Toggle
    const resumeToggleBtn = document.getElementById('resumeToggleBtn');
    const rightPage = document.querySelector('.right.page');

    if (resumeToggleBtn && rightPage) {
      resumeToggleBtn.addEventListener('click', () => {
        rightPage.classList.toggle('active');
        if (rightPage.classList.contains('active')) {
          resumeToggleBtn.innerHTML = '✖';
        } else {
          resumeToggleBtn.innerHTML = '📄';
        }
      });
    }"""

js_new = """    // Mobile Contact Form Toggle
    const contactToggleBtn = document.getElementById('contactToggleBtn');
    const rightPage = document.querySelector('.right.page');

    if (contactToggleBtn && rightPage) {
      contactToggleBtn.addEventListener('click', () => {
        rightPage.classList.toggle('active');
        if (rightPage.classList.contains('active')) {
          contactToggleBtn.innerHTML = '✖';
        } else {
          contactToggleBtn.innerHTML = '✉️';
        }
      });
    }

    // Contact Form Submission
    const contactForm = document.getElementById('contactForm');
    const contactSubmit = document.getElementById('contactSubmit');
    const contactStatus = document.getElementById('contactStatus');

    if (contactForm) {
      contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('contactName').value;
        const email = document.getElementById('contactEmail').value;
        const message = document.getElementById('contactMessage').value;

        contactSubmit.disabled = true;
        contactSubmit.textContent = 'Sending...';
        contactStatus.textContent = '';
        contactStatus.className = 'contact-status';

        try {
          const res = await fetch('/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
          });

          if (!res.ok) throw new Error('Failed to send');
          
          contactForm.reset();
          contactStatus.textContent = 'Message sent successfully! Check your email.';
          contactStatus.className = 'contact-status status-success';
        } catch (err) {
          contactStatus.textContent = 'Error sending message. Please try again later.';
          contactStatus.className = 'contact-status status-error';
          console.error(err);
        } finally {
          contactSubmit.disabled = false;
          contactSubmit.textContent = 'Send Message 🚀';
        }
      });
    }"""

content = content.replace(js_old, js_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Patch successful!")
