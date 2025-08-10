from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from textwrap import wrap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import arabic_reshaper
from bidi.algorithm import get_display

# ---------------------------
# Arabic text preparation
# ---------------------------
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # Connect letters
    bidi_text = get_display(reshaped_text)         # Correct RTL order
    return bidi_text

# Load the CSV file
csv_path = 'csv/nrct.csv'
data = pd.read_csv(csv_path)

# Certificate settings
certificate_template = 'imgs/nrct_certificate_temp.png'
output_folder = 'certificates'
# font_path = 'fonts/Rubik-Bold.ttf'
font_path = 'fonts/NotoNaskhArabic-Bold.ttf'  # new Arabic-supporting font

# Event details
event_title = 'الملتقي القومي الدولي الثالث بعنوان'
event_name = '"الشعر الفكاهي دراسات ونماذج "'
event_date = " 28 يناير 2025"

# Gmail account credentials
gmail_user = 'your_email@gmail.com'
gmail_password = 'your_app_password'

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Load the font
name_font = ImageFont.truetype(font_path, 60)
details_font = ImageFont.truetype(font_path, 45)
event_font = ImageFont.truetype(font_path, 55)
date_font = ImageFont.truetype(font_path, 35)

# Function to draw wrapped and centered text
def draw_centered_text(draw, text, font, fill, center_position, max_width):
    wrapped_text = wrap(text, width=max_width)
    total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)
    current_y = center_position[1] - total_height // 2
    for line in wrapped_text:
        text_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        draw.text((center_position[0] - text_width // 2, current_y), line, font=font, fill=fill)
        current_y += font.getbbox(line)[3] - font.getbbox(line)[1]

# Function to create a certificate
def create_certificate(name, job, event_title, event_name, event_date, output_path):
    image = Image.open(certificate_template)
    draw = ImageDraw.Draw(image)
    
    image_center = (image.width // 2, image.height // 2)
    
    name_offset = -110
    job_offset = -40
    event_title_offset = 70
    event_name_offset = 140
    date_offset = 270

    wrap_max = 70
    
    draw_centered_text(draw, prepare_arabic_text(name), name_font, "black", (image_center[0], image_center[1] + name_offset), wrap_max)
    draw_centered_text(draw, prepare_arabic_text(job), details_font, "black", (image_center[0], image_center[1] + job_offset), wrap_max)
    draw_centered_text(draw, prepare_arabic_text(event_title), event_font, "black", (image_center[0], image_center[1] + event_title_offset), wrap_max)
    draw_centered_text(draw, prepare_arabic_text(event_name), event_font, "black", (image_center[0], image_center[1] + event_name_offset), wrap_max)
    draw_centered_text(draw, prepare_arabic_text(event_date), date_font, "black", (image_center[0], image_center[1] + date_offset), wrap_max)
    
    image.save(output_path)

# Function to send email with PDF attachment
def send_email(recipient_email, recipient_name, job_title, pdf_path):
    try:
        message = MIMEMultipart()
        message['From'] = gmail_user
        message['To'] = recipient_email
        message['Subject'] = "Certificate of Participation"
        
        body = f"Dear {recipient_name},\n\nWe are pleased to send you your certificate for participating as a {job_title} in our event. Please find your certificate attached.\n\nBest regards,\nEvent Team"
        message.attach(MIMEText(body, 'plain'))
        
        with open(pdf_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename=certificate.pdf',
        )
        message.attach(part)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(message)
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {e}")

# Generate certificates and send emails
total = len(data)
for index, row in data.iterrows():
    name = row.get('الاسم كامل كما ترغب أن يكون في الشهادة', 'Participant')
    job = row.get('الوظيفة  كما ترغب أن تكتب بالشهادة', 'Unknown')
    email = row.get('Gmail', None)
    
    if email:
        pdf_path = os.path.join(output_folder, f'{name}.pdf')
        create_certificate(
            " بأن / " + name, 
            job, 
            " قد حضر/ت  " + event_title, 
            event_name, 
            " تحريراً  " + event_date, 
            pdf_path
        )
        send_email(email, name, job, pdf_path)
        print(f"Certificates created and email sent: {index + 1}/{total}", end="\r")

print("\nAll certificates created and emails sent successfully!")
