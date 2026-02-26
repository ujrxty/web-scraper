import re
import urllib.request
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from tkinter import ttk
import pandas as pd  # Import pandas for Excel export

# Email regex pattern
emailRegex = re.compile(r'''
(
    [a-zA-Z0-9._%+-]+      # username
    @                      # '@' symbol
    [a-zA-Z0-9.-]+         # domain name
    \.[a-zA-Z]{2,}         # top-level domain
)
''', re.VERBOSE)

def is_relevant_email(email):
    irrelevant_keywords = ['sentry', 'seenError', 'wrapped', 'context', 'id', 'original']
    return not any(keyword in email for keyword in irrelevant_keywords)

def extractEmailsFromUrlText(urlText):
    extractedEmail = emailRegex.findall(urlText)
    allemails = []
    seen = set()
    
    for email in extractedEmail:
        email = email[0] if isinstance(email, tuple) else email
        if is_relevant_email(email) and email not in seen:
            seen.add(email)
            allemails.append(email)

    return allemails

def htmlPageRead(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        return urlText
    except Exception:
        return None  # Return None on error

def scrape_emails():
    urls_file_path = urls_file_entry.get()
    output_file_path = emails_file_entry.get()
    
    if not urls_file_path or not output_file_path:
        output_area.insert(tk.END, "Please upload both files.\n")
        return

    results = []  # List to hold our results
    try:
        with open(urls_file_path, 'r') as url_file:
            urls = url_file.readlines()
        
        for url in urls:
            url = url.strip('\'"')
            urlText = htmlPageRead(url)
            if urlText:
                emails = extractEmailsFromUrlText(urlText)
                if emails:
                    results.append({"URL": url, "Emails": ', '.join(emails)})
                else:
                    results.append({"URL": url, "Emails": "Emails not found"})
            else:
                results.append({"URL": url, "Emails": "Error reading URL"})
        
        # Create a DataFrame and export to Excel
        df = pd.DataFrame(results)
        df.to_excel(output_file_path, index=False)

        output_area.insert(tk.END, f"Emails scraped and saved to {output_file_path}.\n")

    except Exception as e:
        output_area.insert(tk.END, f"Error reading files: {e}\n")

    # Show completion message
    messagebox.showinfo("Task Completed", "Email scraping task is completed.")

def upload_urls_file():
    file_path = filedialog.askopenfilename(title="Select URLs File", filetypes=[("Text Files", "*.txt")])
    if file_path:
        urls_file_entry.delete(0, tk.END)
        urls_file_entry.insert(0, file_path)

def upload_emails_file():
    file_path = filedialog.asksaveasfilename(title="Select Emails Output File", filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
    if file_path:
        if not file_path.endswith('.xlsx'):
            file_path += '.xlsx'  # Ensure the file has .xlsx extension
        emails_file_entry.delete(0, tk.END)
        emails_file_entry.insert(0, file_path)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    """Draw a rounded rectangle."""
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)
    canvas.create_oval(x1, y1, x1 + 2 * radius, y1 + 2 * radius, **kwargs)
    canvas.create_oval(x2 - 2 * radius, y1, x2, y1 + 2 * radius, **kwargs)
    canvas.create_oval(x1, y2 - 2 * radius, x1 + 2 * radius, y2, **kwargs)
    canvas.create_oval(x2 - 2 * radius, y2 - 2 * radius, x2, y2, **kwargs)

def create_rounded_button(frame, text, command):
    button = tk.Canvas(frame, width=150, height=40, bg="#f0f0f0", highlightthickness=0, borderwidth=0)
    button.pack(pady=10)
    create_rounded_rectangle(button, 0, 0, 150, 40, radius=20, fill="#2196F3", outline="")
    button.create_text(75, 20, text=text, fill="white", font=("Montserrat", 14, "bold"))
    button.bind("<Button-1>", lambda e: command())
    return button

# Setting up the GUI
window = tk.Tk()
window.title("Email Scraper by UJ")
window.geometry("600x600")  # Set window size
window.config(bg="#f0f0f0")  # Background color

# Header
header_frame = tk.Frame(window, bg="#4CAF50")
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="Email Scraper", bg="#4CAF50", fg="white", font=("Montserrat", 20, "bold"))
header_label.pack(pady=10)

# Frame for the input section
input_frame = tk.Frame(window, bg="#f0f0f0")
input_frame.pack(pady=20)

# URL File Upload
urls_file_label = tk.Label(input_frame, text="Upload URLs File:", bg="#f0f0f0", font=("Montserrat", 12, "bold"))
urls_file_label.pack()

urls_file_entry = tk.Entry(input_frame, width=50, font=("Montserrat", 12, "bold"))
urls_file_entry.pack(pady=5)

urls_file_button = ttk.Button(input_frame, text="Browse", command=upload_urls_file)
urls_file_button.pack(pady=5)

# Emails Output File Upload
emails_file_label = tk.Label(input_frame, text="Export Emails:", bg="#f0f0f0", font=("Montserrat", 12, "bold"))
emails_file_label.pack()

emails_file_entry = tk.Entry(input_frame, width=50, font=("Montserrat", 12, "bold"))
emails_file_entry.pack(pady=5)

emails_file_button = ttk.Button(input_frame, text="Browse", command=upload_emails_file)
emails_file_button.pack(pady=5)

# Create Rounded Scrape Button
create_rounded_button(input_frame, "Scrape Emails", scrape_emails)

# Output Area
output_area = scrolledtext.ScrolledText(window, width=70, height=20, font=("Montserrat", 12, "bold"))
output_area.pack(pady=10)

# Start the GUI loop
window.mainloop()