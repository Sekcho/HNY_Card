# Claude.md - New Year Card Generator

> เอกสารนี้สร้างขึ้นเพื่อให้ AI ในอนาคตสามารถเข้าใจและต่อยอดโปรเจคนี้ได้ง่ายขึ้น

## ภาพรวมโปรเจค

**New Year Card Generator** เป็น Web Application สำหรับสร้างการ์ดปีใหม่แบบ Custom ที่ผู้ใช้สามารถ:
- กรอกข้อมูล (ปี, ข้อความอวยพร, ชื่อผู้ส่ง)
- อัพโหลดรูปภาพ
- เลือกธีมสีและฟอนต์
- ดาวน์โหลดไฟล์ HTML และ JPG

### Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Template Engine**: Jinja2
- **Image Generation**: Playwright (HTML to JPG conversion)
- **Fonts**: Google Fonts

---

## โครงสร้างโปรเจค

```
Card/
├── app.py                          # Flask application หลัก (routes, endpoints)
├── config.py                       # Configuration (themes, fonts, font sizes)
├── requirements.txt                # Python dependencies
├── README.md                       # คู่มือผู้ใช้
├── claude.md                       # เอกสารนี้ (สำหรับ AI)
│
├── templates/
│   ├── index.html                 # หน้าแรก - Form สำหรับกรอกข้อมูล
│   └── card_template.html         # Template สำหรับสร้างการ์ด (Jinja2)
│
├── static/
│   ├── css/
│   │   └── style.css              # Stylesheet หลัก (Dark theme)
│   ├── js/
│   │   └── main.js                # JavaScript หลัก (AJAX, file upload, form handling)
│   ├── uploads/                   # รูปภาพที่ผู้ใช้อัพโหลด
│   └── generated/                 # ไฟล์การ์ดที่สร้าง (HTML + JPG)
│
├── utils/
│   ├── __init__.py
│   └── card_generator.py          # Logic สำหรับสร้างการ์ดและแปลง HTML เป็น JPG
│
└── data/
    └── templates.json             # Template ที่ผู้ใช้บันทึกไว้
```

---

## สถาปัตยกรรม (Architecture)

### 1. Frontend (Client Side)

**index.html** - หน้า Form
- Form สำหรับกรอกข้อมูล
- Upload area สำหรับรูปภาพ (รองรับ drag & drop)
- Preview area แสดงการ์ดที่สร้าง
- Download buttons สำหรับดาวน์โหลด HTML/JPG

**main.js** - JavaScript Logic
- `handlePhotoUpload()` - อัพโหลดรูป via AJAX → `/upload-photo`
- `generateCard()` - สร้างการ์ด via AJAX → `/generate-card`
- `saveTemplate()` - บันทึก template → `/save-template`
- `loadTemplates()` - โหลด templates → `/load-templates`
- Auto-calculate ปี พ.ศ. จาก ค.ศ.

### 2. Backend (Server Side)

**app.py** - Flask Routes
```python
/ (GET)                    → แสดงหน้าแรก
/upload-photo (POST)       → รับไฟล์รูป, บันทึก, return path
/generate-card (POST)      → สร้างการ์ด HTML + JPG
/download/<filename> (GET) → ดาวน์โหลดไฟล์
/save-template (POST)      → บันทึก template
/load-templates (GET)      → ดึงรายการ templates
/delete-template (POST)    → ลบ template
/get-theme-info/<key> (GET)→ ดึงข้อมูล theme
```

**utils/card_generator.py** - Card Generation Logic
```python
CardGenerator.generate_html(data)
    → อ่าน card_template.html
    → Render ด้วย Jinja2 + data
    → บันทึก HTML file
    → return (html_content, html_filepath)

CardGenerator.convert_to_jpg(html_filepath)
    → เปิด HTML ด้วย Playwright
    → รอโหลด fonts (3 วินาที)
    → Screenshot → JPG (quality=95)
    → return jpg_path

CardGenerator.generate_card(data)
    → generate_html() + convert_to_jpg()
    → return (html_path, jpg_path)
```

### 3. Template System

**card_template.html** - Jinja2 Template
- รับ variables: `year_cs`, `year_be`, `wishes`, `signature`, `photo_path`, `theme`, `fonts`, `font_sizes`
- ใช้ inline CSS (เพื่อให้ HTML ใช้งานได้แบบ standalone)
- มี animations: gradient move, line move, particle float, shine effect
- Responsive design (media queries)

---

## Configuration (config.py)

### Themes
มี 12 ธีม:
1. `blue-gold` - Classic
2. `ai-tech` - AI & Digital
3. `chinese-new-year` - ตรุษจีน
4. `red-green` - Christmas
5. `songkran` - สงกรานต์
6. `halloween` - ฮาโลวีน
7. `business` - มืออาชีพ
8. `islamic` - อิสลาม
9. `purple-pink` - Modern
10. `cyan-violet` - Neon
11. `orange-yellow` - Sunset
12. `silver-gold` - Luxury

แต่ละ theme มี:
```python
{
    'name': 'Display Name',
    'primary': '#hex',      # สีหลัก
    'secondary': '#hex',    # สีรอง
    'gradient_start': '#hex',
    'gradient_end': '#hex',
    'bg_gradient': 'linear-gradient(...)'
}
```

### Fonts
**ภาษาไทย**: 5 ฟอนต์
- Noto Sans Thai (default)
- Sarabun
- Prompt
- Kanit
- Bai Jamjuree

**ภาษาอังกฤษ**: 5 ฟอนต์
- Poppins (default)
- Playfair Display
- Montserrat
- Roboto
- Inter

### Font Sizes
แต่ละส่วนมี 3 ขนาด: small, medium, large
- `year-badge`: 24px, 36px, 48px
- `main-title`: 48px, 72px, 96px
- `thai-title`: 32px, 48px, 64px
- `wishes`: 16px, 20px, 24px
- `signature`: 24px, 36px, 48px

---

## Data Flow

### การสร้างการ์ด (Generate Card Flow)

```
1. User กรอกข้อมูลใน Form
   ↓
2. User คลิกปุ่ม "สร้างการ์ด"
   ↓
3. JavaScript collectFormData()
   - รวบรวมข้อมูลทั้งหมด
   - สร้าง JSON object
   ↓
4. AJAX POST → /generate-card
   ↓
5. Flask app.py รับ request
   ↓
6. CardGenerator.generate_card(data)
   ├─ generate_html()
   │  ├─ อ่าน card_template.html
   │  ├─ แปลง photo_path เป็น absolute path
   │  ├─ ดึง theme, fonts จาก config
   │  ├─ Render template ด้วย Jinja2
   │  └─ บันทึกเป็น card_YYYY.html
   │
   └─ convert_to_jpg()
      ├─ เปิด HTML ด้วย Playwright
      ├─ รอโหลด fonts (3 วินาที)
      ├─ Screenshot full page
      └─ บันทึกเป็น card_YYYY.jpg
   ↓
7. Return {success: true, html_file, jpg_file}
   ↓
8. JavaScript รับ response
   ├─ แสดง preview (JPG)
   ├─ แสดง download buttons
   └─ แสดง success message
```

### การอัพโหลดรูป (Photo Upload Flow)

```
1. User เลือกรูป (click หรือ drag & drop)
   ↓
2. JavaScript handlePhotoUpload()
   - Validate: file type, file size (< 16MB)
   ↓
3. AJAX POST → /upload-photo (FormData)
   ↓
4. Flask app.py
   - ตรวจสอบ file type (PNG, JPG, JPEG, GIF, WEBP)
   - สร้าง unique filename (เพิ่ม timestamp)
   - บันทึกใน static/uploads/
   - Return {filepath: '../static/uploads/xxx.jpg'}
   ↓
5. JavaScript รับ response
   - เก็บ uploadedPhotoPath
   - แสดง preview ในช่อง upload
```

---

## สิ่งสำคัญที่ต้องรู้ (Critical Points)

### 1. Photo Path Conversion
**ปัญหา**: Photo path ที่ส่งมาจาก client เป็น relative path (`../static/uploads/xxx.jpg`) แต่ Playwright ต้องการ absolute path

**วิธีแก้**: ใน `card_generator.py` มี logic แปลง path:
```python
if photo_path.startswith('../static/'):
    relative_part = photo_path.replace('../static/', '')
    photo_path = os.path.join(self.base_dir, 'static', relative_part).replace('\\', '/')
```

### 2. Playwright Screenshot Timing
ต้องรอ 3 วินาทีก่อน screenshot เพื่อให้:
- Google Fonts โหลดเสร็จ
- Animations render ครบ
- รูปภาพโหลดเสร็จ

```python
await asyncio.sleep(3)  # ⚠️ สำคัญ!
```

### 3. File URL for Playwright
Windows path ต้องแปลงเป็น file URL:
```python
html_url = f'file:///{html_filepath.replace(chr(92), "/")}'
# D:\2026\Card\file.html → file:///D:/2026/Card/file.html
```

### 4. Template System
Template ไม่บันทึก `photo_path` เพราะรูปเป็นไฟล์ชั่วคราว ผู้ใช้ต้องอัพโหลดใหม่ทุกครั้ง

---

## วิธีเพิ่มฟีเจอร์ใหม่

### เพิ่ม Theme ใหม่
1. แก้ไข `config.py` → เพิ่มใน `THEMES` dict
2. กำหนด `primary`, `secondary`, `bg_gradient`
3. Refresh browser → theme จะปรากฏใน dropdown อัตโนมัติ

### เพิ่มฟอนต์ใหม่
1. แก้ไข `config.py` → เพิ่มใน `FONTS['thai']` หรือ `FONTS['english']`
2. ระบุ `name`, `url` (Google Fonts), `family` (CSS)
3. Refresh browser → ฟอนต์จะปรากฏใน dropdown

### เพิ่มฟิลด์ข้อมูลใหม่
1. แก้ไข `templates/index.html` → เพิ่ม form field
2. แก้ไข `static/js/main.js` → เพิ่มใน `collectFormData()`
3. แก้ไข `templates/card_template.html` → เพิ่มการแสดงผล
4. (ถ้าต้องการ) แก้ไข `config.py` → เพิ่มใน `DEFAULT_SETTINGS`

### เพิ่ม Route ใหม่
1. แก้ไข `app.py` → เพิ่ม `@app.route()`
2. เขียน logic ใน function
3. Return JSON สำหรับ API หรือ `render_template()` สำหรับหน้าใหม่

---

## การ Debug

### ดู Flask Logs
Server รันใน debug mode → ดู errors ใน terminal

### ดู Playwright Errors
ถ้า JPG generation ล้มเหลว → ดู error ใน Flask logs
- ตรวจสอบว่า chromium installed: `playwright install chromium`
- ตรวจสอบว่า HTML path ถูกต้อง
- ตรวจสอบว่า photo path เป็น absolute path

### ดู Network Requests
เปิด Browser DevTools → Network tab
- ดู AJAX requests ไป `/upload-photo`, `/generate-card`
- ตรวจสอบ response data

### ตรวจสอบไฟล์ที่สร้าง
```bash
static/uploads/        # รูปที่อัพโหลด
static/generated/      # HTML + JPG ที่สร้าง
data/templates.json    # Templates ที่บันทึก
```

---

## Limitations & Known Issues

1. **File Size Limit**: รูปภาพสูงสุด 16MB (ตั้งค่าใน `app.py`)
2. **Single User**: ไม่มี user authentication, ทุกคนใช้ folder เดียวกัน
3. **No Cleanup**: ไฟล์ใน `uploads/` และ `generated/` จะสะสม (ต้องลบเอง)
4. **Playwright Performance**: สร้าง JPG ใช้เวลา 3-5 วินาที
5. **Template Overwrites**: ถ้าบันทึก template ชื่อซ้ำจะ overwrite ทันที

---

## Future Improvements (แนวทางพัฒนา)

### Features
- [ ] เพิ่มการแก้ไขรูป (crop, rotate, filter)
- [ ] เพิ่มการเลือก layout หลายแบบ
- [ ] เพิ่มสติกเกอร์/decorations
- [ ] Export เป็น PDF
- [ ] Export เป็น PNG (transparent background)
- [ ] Preview แบบ real-time (ไม่ต้องกดปุ่ม)
- [ ] Multiple photos support
- [ ] Video/GIF export

### Technical
- [ ] User authentication & multi-user support
- [ ] Database สำหรับเก็บ templates (แทน JSON file)
- [ ] File cleanup job (ลบไฟล์เก่าอัตโนมัติ)
- [ ] Image optimization (resize before upload)
- [ ] Caching (ไม่ต้อง regenerate ถ้าข้อมูลเหมือนเดิม)
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Docker support
- [ ] Cloud deployment guide (Heroku, Railway, etc.)

### UI/UX
- [ ] Dark/Light mode toggle
- [ ] Mobile responsive improvements
- [ ] Tutorial/onboarding
- [ ] More theme categories
- [ ] Theme preview before select
- [ ] Font preview

---

## Dependencies

```
Flask==3.0.0          # Web framework
Jinja2==3.1.2         # Template engine
playwright==1.40.0    # Headless browser
Werkzeug==3.0.1       # WSGI utilities
```

---

## สรุป

โปรเจคนี้ใช้สถาปัตยกรรมแบบ **Client-Server** ที่:
- Client (Browser) ส่งข้อมูล via AJAX
- Server (Flask) ประมวลผลและสร้างไฟล์
- Playwright แปลง HTML → JPG
- Jinja2 render template แบบ dynamic

**จุดเด่น**:
- ใช้งานง่าย (Web-based, no installation)
- Customizable (12 themes, 10 fonts, adjustable sizes)
- Standalone HTML output (มี CSS inline)
- Professional JPG output (high quality)

**Architecture ที่ดี**:
- Separation of concerns (config, logic, presentation แยกกัน)
- Template system (ง่ายต่อการเพิ่ม theme/font)
- Modular code (easy to extend)

---

**สร้างโดย**: Claude Sonnet 4.5
**วันที่**: 2026-01-01
**เวอร์ชัน**: 1.0.0
