
import qrcode
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# --- Generate QR Code ---
def generate_qr():
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("⚠️ Warning", "Please enter text or URL to generate a QR code.")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=fg_color.get(), back_color=bg_color.get()).convert("RGB")

    # Optional or default logo overlay
    logo_file = logo_path.get() or ("logo.png" if os.path.exists("logo.png") else "")
    if logo_file:
        try:
            logo = Image.open(logo_file)
            qr_width, qr_height = qr_img.size
            logo_size = qr_width // 4
            logo = logo.resize((logo_size, logo_size))
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos)
        except Exception as e:
            messagebox.showerror("Error", f"Logo overlay failed:\n{e}")

    qr_img.save("qrcode_result.png")
    display_qr(qr_img)
    messagebox.showinfo("✅ Success", "QR code generated and saved as qrcode_result.png")

def display_qr(img):
    img_tk = ImageTk.PhotoImage(img.resize((250, 250)))
    qr_label.config(image=img_tk)
    qr_label.image = img_tk

def browse_logo():
    file_path = filedialog.askopenfilename(
        title="Select Logo Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_path:
        logo_path.set(file_path)
        logo_label.config(text=f"Logo: {file_path.split('/')[-1]}")

# --- UI Setup ---
root = Tk()
root.title("QR Code Generator")
root.geometry("450x640")
root.config(bg="#F2F4F6")
root.resizable(False, False)

# --- Title ---
Label(root, text="QR Code Generator", font=("Segoe UI", 20, "bold"), fg="#2E3A59", bg="#F2F4F6").pack(pady=(25, 10))
Label(root, text="Enter text or URL below:", font=("Segoe UI", 12), bg="#F2F4F6", fg="#555").pack()

# --- Entry Box ---
entry_frame = Frame(root, bg="#F2F4F6")
entry_frame.pack(pady=10)
entry = Entry(entry_frame, width=38, font=("Segoe UI", 12), bd=0, relief=FLAT, highlightthickness=1, highlightbackground="#CCC")
entry.pack(ipady=7, padx=10)

# --- Color Inputs ---
frame_colors = Frame(root, bg="#F2F4F6")
frame_colors.pack(pady=10)

Label(frame_colors, text="Foreground:", bg="#F2F4F6", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
fg_color = StringVar(value="black")
Entry(frame_colors, textvariable=fg_color, width=10, relief=FLAT, highlightthickness=1, highlightbackground="#CCC").grid(row=0, column=1, padx=5, ipady=3)

Label(frame_colors, text="Background:", bg="#F2F4F6", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5)
bg_color = StringVar(value="white")
Entry(frame_colors, textvariable=bg_color, width=10, relief=FLAT, highlightthickness=1, highlightbackground="#CCC").grid(row=0, column=3, padx=5, ipady=3)

# --- Logo Selection ---
Button(root, text="Select Logo (Optional)", command=browse_logo, bg="#E3EAFD", fg="#1B3B82", font=("Segoe UI", 10, "bold"), relief=FLAT, bd=0, width=25, height=1, cursor="hand2").pack(pady=(15, 3))
logo_path = StringVar()
logo_label = Label(root, text="No logo selected", bg="#F2F4F6", fg="gray", font=("Segoe UI", 9))
logo_label.pack()

# --- Generate Button ---
Button(root, text="Generate QR Code", command=generate_qr, font=("Segoe UI", 12, "bold"), bg="#5A8DEE", fg="white", relief=FLAT, width=22, height=2, cursor="hand2").pack(pady=25)

# --- QR Display ---
qr_label = Label(root, bg="#F2F4F6")
qr_label.pack(pady=10)

# --- Footer ---
Label(root, text="Made with ❤️ by TagTrueCodingJr", bg="#F2F4F6", fg="#888", font=("Segoe UI", 9, "italic")).pack(side=BOTTOM, pady=15)

root.mainloop()
