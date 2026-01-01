# New Year Card Generator

Web Application สำหรับสร้างการ์ดปีใหม่ที่สวยงามและปรับแต่งได้ตามต้องการ

## ฟีเจอร์หลัก

- กรอกข้อมูลการ์ด (ปี ค.ศ., พ.ศ., ข้อความอวยพร, ชื่อผู้ส่ง)
- อัพโหลดรูปภาพ
- เลือกธีมสี (6 ธีม: Blue & Gold, Red & Green, Purple & Pink, Cyan & Violet, Orange & Yellow, Silver & Gold)
- เลือกฟอนต์ภาษาไทยและอังกฤษ (5 ฟอนต์ต่อภาษา)
- ปรับขนาดฟอนต์ (เล็ก, กลาง, ใหญ่)
- Preview การ์ดก่อนสร้าง
- บันทึกและโหลด Template
- ดาวน์โหลดไฟล์ HTML และ JPG

## โครงสร้างโปรเจค

```
Card/
├── app.py                      # Flask application หลัก
├── config.py                   # Configuration (themes, fonts, font sizes)
├── requirements.txt            # Python dependencies
├── README.md                   # เอกสารนี้
│
├── templates/
│   ├── index.html             # หน้าแรก (form page)
│   └── card_template.html     # Template สำหรับสร้างการ์ด
│
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet หลัก
│   ├── js/
│   │   └── main.js            # JavaScript หลัก
│   ├── uploads/               # รูปภาพที่อัพโหลด
│   └── generated/             # ไฟล์การ์ดที่สร้าง (HTML, JPG)
│
├── utils/
│   └── card_generator.py      # Logic สำหรับสร้างการ์ด
│
└── data/
    └── templates.json         # Template ที่บันทึกไว้
```

## การติดตั้ง

### 1. ติดตั้ง Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. ติดตั้ง Playwright Browsers

```bash
playwright install chromium
```

## การใช้งาน

### 1. รันโปรแกรม

```bash
python app.py
```

### 2. เปิดเว็บเบราว์เซอร์

ไปที่ `http://localhost:5000`

### 3. กรอกข้อมูล

1. กรอกปี ค.ศ. (จะคำนวณปี พ.ศ. อัตโนมัติ)
2. กรอกข้อความอวยพร (2 ข้อความ)
3. กรอกชื่อผู้ส่ง
4. อัพโหลดรูปภาพ (PNG, JPG, JPEG, GIF, WEBP สูงสุด 16MB)

### 4. ปรับแต่ง

1. เลือกธีมสี
2. เลือกฟอนต์ภาษาไทยและอังกฤษ
3. ปรับขนาดฟอนต์ (ถ้าต้องการ)

### 5. สร้างการ์ด

กดปุ่ม "สร้างการ์ด" และรอสักครู่

### 6. ดาวน์โหลด

เมื่อสร้างเสร็จ จะมีปุ่มดาวน์โหลดไฟล์ HTML และ JPG

## การบันทึกและโหลด Template

### บันทึก Template

1. กรอกข้อมูลและตั้งค่าที่ต้องการ
2. พิมพ์ชื่อ Template ในช่อง "บันทึก Template"
3. กดปุ่ม "บันทึก"

### โหลด Template

1. เลือก Template จาก dropdown "โหลด Template"
2. ข้อมูลจะถูกกรอกอัตโนมัติ (ยกเว้นรูปภาพ)

## ธีมสีที่มี

1. **Blue & Gold (Classic)** - น้ำเงิน-ทอง สไตล์คลาสสิก
2. **Red & Green (Christmas)** - แดง-เขียว สไตล์คริสต์มาส
3. **Purple & Pink (Modern)** - ม่วง-ชมพู สไตล์โมเดิร์น
4. **Cyan & Violet (Neon)** - ฟ้า-ม่วงแดง สไตล์นีออน
5. **Orange & Yellow (Sunset)** - ส้ม-เหลือง สไตล์พระอาทิตย์ตก
6. **Silver & Gold (Luxury)** - เงิน-ทอง สไตล์หรูหรา

## ฟอนต์ที่มี

### ภาษาไทย
- Noto Sans Thai
- Sarabun
- Prompt
- Kanit
- Bai Jamjuree

### ภาษาอังกฤษ
- Poppins
- Playfair Display
- Montserrat
- Roboto
- Inter

## การแก้ไขปัญหา

### รูปภาพไม่แสดง
- ตรวจสอบว่าอัพโหลดรูปภาพสำเร็จ (มีข้อความ "อัพโหลดรูปภาพสำเร็จ!")
- ตรวจสอบประเภทไฟล์ (ต้องเป็น PNG, JPG, JPEG, GIF, WEBP)
- ตรวจสอบขนาดไฟล์ (ไม่เกิน 16MB)

### การ์ดไม่ถูกสร้าง
- ตรวจสอบว่ามี Playwright installed: `playwright install chromium`
- ตรวจสอบว่ากรอกข้อมูลครบ (รูปภาพและชื่อผู้ส่ง)

### Template ไม่บันทึก
- ตรวจสอบว่ากรอกชื่อ Template แล้ว
- ตรวจสอบว่ามีโฟลเดอร์ `data/` อยู่

## License

MIT License
