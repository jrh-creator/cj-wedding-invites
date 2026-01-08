import uuid
import os
import shutil
import base64

# =====================
# CONFIG
# =====================
MAKE_WEBHOOK_URL = "https://hook.make.com/YOUR_WEBHOOK_URL"




dict_guests = {
    "parentsJohn": "Tim & Trish",
    "parentsChristiane": "Rolf & Waltraud",
    "gehrungsMarkus":"Markus, Simone & kinder"
}
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
INVITES_DIR = os.path.join(BASE_DIR, "invites")

TEMPLATE_FILE = os.path.join(BASE_DIR, "invite_template.html")
BACKGROUND_IMAGE = "save-the-date.png"

os.makedirs(INVITES_DIR, exist_ok=True)

# Read external template file
with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template = f.read()

# =====================
# GENERATE INVITES
# =====================
for guest in dict_guests.keys():
    guest_slug = guest              # folder name
    guest_name = dict_guests[guest] # human-readable name
    invite_uuid = guest_slug        # UUID for Make

    guest_dir = os.path.join(INVITES_DIR, guest_slug)
    os.makedirs(guest_dir, exist_ok=True)

    # Copy PNG asset
    src_bg = os.path.join(ASSETS_DIR, BACKGROUND_IMAGE)
    dst_bg = os.path.join(guest_dir, BACKGROUND_IMAGE)
    if os.path.exists(src_bg):
        shutil.copy(src_bg, dst_bg)

    # Embed as data URI
    if os.path.exists(src_bg):
        with open(src_bg, "rb") as imgf:
            b64 = base64.b64encode(imgf.read()).decode('ascii')
        bg_value = f"data:image/png;base64,{b64}"
    else:
        bg_value = BACKGROUND_IMAGE

    # Replace placeholders
    html = template.replace("{{GUEST}}", guest_name)
    html = html.replace("{{UUID}}", invite_uuid)
    html = html.replace("{{WEBHOOK}}", MAKE_WEBHOOK_URL)
    html = html.replace("{{BG}}", bg_value)

    output_file = os.path.join(guest_dir, "index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Created invite for {guest_name}: {invite_uuid}")

print("✅ All invites generated.")
