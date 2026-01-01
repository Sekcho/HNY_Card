# คู่มือ Deploy โปรเจค New Year Card Generator

## เตรียมโปรเจค

### 1. สร้าง Git Repository

ถ้ายังไม่มี Git Repository:

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. Push ขึ้น GitHub

สร้าง repository ใหม่บน GitHub แล้ว push:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

---

## Deploy บน Render.com (แนะนำ - ฟรี)

### ขั้นตอน

1. **สมัครบัญชี Render**
   - ไปที่ https://render.com
   - สมัครด้วย GitHub account

2. **สร้าง Web Service**
   - คลิก "New" → "Web Service"
   - เชื่อมต่อ GitHub repository ของคุณ
   - เลือก repository ของโปรเจคนี้

3. **ตั้งค่า Service**
   - **Name**: ตั้งชื่ออะไรก็ได้ (เช่น `new-year-card`)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: เลือก `Free`

4. **Environment Variables (ถ้าต้องการ)**
   - คลิก "Advanced" → "Add Environment Variable"
   - เพิ่ม `SECRET_KEY`: ใส่ค่า secret key ของคุณ (สุ่มจาก [https://randomkeygen.com/](https://randomkeygen.com/))

5. **Deploy**
   - คลิก "Create Web Service"
   - รอประมาณ 5-10 นาที (ติดตั้ง Playwright จะใช้เวลานาน)
   - เสร็จแล้วจะได้ URL เช่น `https://your-app.onrender.com`

### ข้อจำกัด Free Tier

- **Server Sleep**: หลัง 15 นาทีไม่มีการใช้งาน server จะ sleep
  - ครั้งแรกที่เข้าจะโหลดช้า 30-60 วินาที
- **No Persistent Storage**: ไฟล์ที่อัพโหลดจะหายเมื่อ server restart
  - แก้ไข: ใช้ cloud storage เช่น Cloudinary (มี free tier)
- **RAM**: 512MB (พอสำหรับ screenshot)
- **Bandwidth**: 100 GB/เดือน

### เคล็ดลับ

1. **Keep Server Awake**: ใช้ service เช่น [UptimeRobot](https://uptimerobot.com/) ping ทุก 10 นาที
2. **External Storage**: ถ้าต้องการเก็บรูปแบบถาวร ใช้ Cloudinary
   ```bash
   pip install cloudinary
   ```

---

## Deploy บน Railway.app (ทางเลือก)

### ขั้นตอน

1. **สมัครบัญชี Railway**
   - ไปที่ https://railway.app
   - สมัครด้วย GitHub account
   - ได้ $5 credit/เดือน

2. **สร้าง Project**
   - คลิก "New Project"
   - เลือก "Deploy from GitHub repo"
   - เลือก repository ของคุณ

3. **ตั้งค่า**
   - Railway จะ auto-detect Flask app
   - ไม่ต้องตั้งค่าอะไรเพิ่ม (ใช้ Procfile และ build.sh ที่มีอยู่แล้ว)

4. **Environment Variables**
   - ไปที่ "Variables" tab
   - เพิ่ม `SECRET_KEY`: ใส่ค่า secret key

5. **Deploy**
   - Railway จะ deploy อัตโนมัติ
   - ได้ URL เช่น `https://your-app.up.railway.app`

### ข้อจำกัด

- **Free Tier**: $5 credit/เดือน (ประมาณ 500 ชม.)
- **Sleep**: ไม่ sleep แต่ credit หมดเร็ว

---

## ตรวจสอบการ Deploy

### 1. ตรวจสอบ Logs

**Render:**
- ไปที่ Dashboard → เลือก service → "Logs"

**Railway:**
- ไปที่ Project → "Deployments" → คลิก deployment → "Logs"

### 2. ทดสอบ

เปิด URL ที่ได้:
- ควรเห็นหน้า form สร้างการ์ด
- ลองอัพโหลดรูป → สร้างการ์ด → ดาวน์โหลด JPG

---

## Troubleshooting

### ปัญหา: Playwright ติดตั้งไม่สำเร็จ

**อาการ:** Build ล้มเหลว, log แสดง error เกี่ยวกับ chromium

**วิธีแก้:**
1. ตรวจสอบว่า `build.sh` มี execute permission:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Add execute permission to build.sh"
   git push
   ```

2. ตรวจสอบ log ว่ามีพื้นที่เพียงพอหรือไม่

### ปัญหา: ไฟล์อัพโหลดหายหลัง restart

**อาการ:** รูปที่อัพโหลดหายไปเมื่อ server restart

**คำอธิบาย:** Free tier ของ Render ไม่มี persistent storage

**วิธีแก้:**
1. ใช้ Cloudinary สำหรับเก็บรูป (free tier: 25 GB)
2. หรือใช้ AWS S3 (free tier: 5 GB)

### ปัญหา: Server ช้ามาก

**อาการ:** สร้างการ์ด JPG ใช้เวลานาน

**คำอธิบาย:** Free tier มี RAM จำกัด (512MB)

**วิธีแก้:**
1. ลดขนาดรูปก่อนอัพโหลด (< 2MB)
2. ใช้ plan ที่สูงขึ้น (ไม่ฟรี)

### ปัญหา: Build ใช้เวลานานเกิน 10 นาที

**อาการ:** Render timeout ระหว่าง build

**วิธีแก้:**
1. เช็ค build.sh ว่า install เฉพาะ chromium
   ```bash
   playwright install chromium  # ถูกต้อง
   # ไม่ใช่ playwright install (จะ install ทุก browser)
   ```

---

## ตัวเลือกอื่นๆ (ไม่แนะนำ)

### Vercel / Netlify
❌ **ไม่รองรับ** - เหมาะกับ static sites / serverless เท่านั้น, Playwright ใช้ไม่ได้

### PythonAnywhere
❌ **Free tier ไม่รองรับ Playwright** - ติดตั้ง chromium ไม่ได้

### Google Cloud Run
✅ **ใช้ได้** แต่ซับซ้อน - ต้องสร้าง Docker image

### Heroku
❌ **ไม่มี free tier แล้ว** - ต้องจ่ายเงินทุก plan

---

## สรุป

| Platform | ฟรี | Playwright | Persistent Storage | Sleep | แนะนำ |
|----------|-----|------------|-------------------|-------|-------|
| **Render** | ✅ | ✅ | ❌ | ✅ (15 min) | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ ($5/mo) | ✅ | ✅ | ❌ | ⭐⭐⭐⭐ |
| PythonAnywhere | ✅ | ❌ | ✅ | ❌ | ❌ |
| Vercel | ✅ | ❌ | ❌ | ❌ | ❌ |

**แนะนำ: Render.com** เพราะตั้งค่าง่าย รองรับทุกอย่าง และฟรีจริงๆ

---

## ติดต่อ & Issues

- หาก deploy ไม่สำเร็จ ส่ง logs มาที่ issues
- ตรวจสอบให้แน่ใจว่าไฟล์ทั้งหมดถูก push ขึ้น GitHub แล้ว

---

**สร้างโดย**: Claude Sonnet 4.5
**วันที่**: 2026-01-01
