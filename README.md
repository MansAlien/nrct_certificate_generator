# 🎓 Certificate Generator & Email Sender

This Python script automates the process of:

1. Generating participation certificates from a template image.
2. Customizing each certificate with the participant's **name**, **job title**, and **event details**.
3. Saving certificates as PDF files.
4. Sending certificates via email automatically.

---

## 📂 Project Structure

```
project/
├── csv/
│   └── nrct.csv               # Participant details (names, jobs, emails)
├── fonts/
│   └── Rubik-Bold.ttf          # Font used for writing on the certificates
├── imgs/
│   └── nrct_certificate_temp.png  # Certificate template image
├── certificates/               # Generated certificates will be stored here
├── main.py                    # Main Python script
└── README.md                    # This file
```

---

## 📋 Requirements

- Python 3.x
- UV
- numpy
- pandas
- pillow
- Install dependencies:

```bash
uv sync
```

---

## 📄 CSV File Format

Your CSV (`nrct.csv`) should contain at least the following columns:

| الاسم كامل كما ترغب أن يكون في الشهادة | الوظيفة  كما ترغب أن تكتب بالشهادة | Gmail                                          |
| -------------------------------------- | ---------------------------------- | ---------------------------------------------- |
| أحمد محمد علي                          | أستاذ الأدب العربي                 | [example@gmail.com](mailto\:example@gmail.com) |

---

## ⚙️ Configuration

Before running the script, update these variables in `script.py`:

```python
# Certificate template and font
certificate_template = 'imgs/nrct_certificate_temp.png'
font_path = 'fonts/Rubik-Bold.ttf'

# Event details
event_title = 'الملتقي القومي الدولي الثالث بعنوان'
event_name = '"الشعر الفكاهي دراسات ونماذج "'
event_date = "28 يناير 2025"

# Gmail account credentials (use Gmail App Password)
gmail_user = 'your_email@gmail.com'
gmail_password = 'your_app_password'
```

**Note:**\
For security, you should store your Gmail credentials in environment variables instead of hardcoding them.

---

## 🚀 Usage

Run the script:

```bash
python script.py
```

The script will:

1. Read participant details from the CSV file.
2. Generate personalized certificates and save them as PDFs in the `certificates` folder.
3. Email each participant their certificate.

---

## 📌 Notes

- **App Password:** If using Gmail, you need to enable 2FA and create an App Password to use with `smtplib`.
- **Fonts:** Make sure the font file supports Arabic if your certificates contain Arabic text.
- **Certificate Template:** Should be a high-resolution `.png` image with enough space for the text.

---

## 🛡 License

This project is licensed under the MIT License.\
You are free to use and modify it as needed.


