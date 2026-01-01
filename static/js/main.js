// Global variables
let uploadedPhotoPath = '';
let currentData = {};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadTemplates();
    autoCalculateYears();
});

function initializeEventListeners() {
    // Photo upload
    const uploadArea = document.getElementById('uploadArea');
    const photoInput = document.getElementById('photo');

    uploadArea.addEventListener('click', () => {
        photoInput.click();
    });

    photoInput.addEventListener('change', handlePhotoUpload);

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--border-color)';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            photoInput.files = files;
            handlePhotoUpload();
        }
    });

    // Year auto-calculation
    document.getElementById('year_cs').addEventListener('input', (e) => {
        const yearCS = parseInt(e.target.value);
        if (!isNaN(yearCS)) {
            document.getElementById('year_be').value = yearCS + 543;
        }
    });

    document.getElementById('year_be').addEventListener('input', (e) => {
        const yearBE = parseInt(e.target.value);
        if (!isNaN(yearBE)) {
            document.getElementById('year_cs').value = yearBE - 543;
        }
    });

    // Template selection
    document.getElementById('template_select').addEventListener('change', loadSelectedTemplate);
}

async function handlePhotoUpload() {
    const photoInput = document.getElementById('photo');
    const file = photoInput.files[0];

    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('กรุณาอัพโหลดไฟล์รูปภาพเท่านั้น (PNG, JPG, JPEG, GIF, WEBP)');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('ไฟล์ใหญ่เกินไป กรุณาใช้ไฟล์ที่มีขนาดไม่เกิน 16MB');
        return;
    }

    // Upload file
    const formData = new FormData();
    formData.append('photo', file);

    try {
        const response = await fetch('/upload-photo', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            uploadedPhotoPath = data.filepath;

            // Show preview
            const preview = document.getElementById('photoPreview');
            const placeholder = document.getElementById('uploadPlaceholder');

            preview.src = data.filepath;
            preview.style.display = 'block';
            placeholder.style.display = 'none';

            showSuccess('อัพโหลดรูปภาพสำเร็จ!');
        } else {
            showError(data.error || 'เกิดข้อผิดพลาดในการอัพโหลดรูปภาพ');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('เกิดข้อผิดพลาดในการอัพโหลดรูปภาพ');
    }
}

async function generateCard() {
    // Validate
    if (!uploadedPhotoPath) {
        showError('กรุณาอัพโหลดรูปภาพก่อน');
        return;
    }

    const signature = document.getElementById('signature').value.trim();
    if (!signature) {
        showError('กรุณากรอกชื่อผู้ส่ง');
        return;
    }

    // Collect data
    const cardData = collectFormData();

    // Show loading
    showLoading();

    try {
        const response = await fetch('/generate-card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cardData)
        });

        const data = await response.json();

        hideLoading();

        if (data.success) {
            showSuccess(data.message || 'สร้างการ์ดสำเร็จ!');

            // Show download section
            showDownloadSection(data.html_file, data.jpg_file);

            // Show preview (JPG)
            showPreview(data.jpg_file);
        } else {
            showError(data.error || 'เกิดข้อผิดพลาดในการสร้างการ์ด');
        }
    } catch (error) {
        hideLoading();
        console.error('Generate error:', error);
        showError('เกิดข้อผิดพลาดในการสร้างการ์ด');
    }
}

function collectFormData() {
    const wishes = [];
    const wish1 = document.getElementById('wish1').value.trim();
    const wish2 = document.getElementById('wish2').value.trim();

    if (wish1) wishes.push(wish1);
    if (wish2) wishes.push(wish2);

    return {
        year_cs: parseInt(document.getElementById('year_cs').value),
        year_be: parseInt(document.getElementById('year_be').value),
        wishes: wishes,
        signature: document.getElementById('signature').value.trim(),
        photo_path: uploadedPhotoPath,
        theme: document.getElementById('theme').value,
        thai_font: document.getElementById('thai_font').value,
        english_font: document.getElementById('english_font').value,
        font_sizes: {
            'year-badge': document.getElementById('size_year_badge').value,
            'main-title': document.getElementById('size_main_title').value,
            'thai-title': document.getElementById('size_thai_title').value,
            'wishes': document.getElementById('size_wishes').value,
            'signature': document.getElementById('size_signature').value
        }
    };
}

function showPreview(jpgFile) {
    const previewArea = document.getElementById('previewArea');
    const jpgPath = `/static/generated/${jpgFile}?t=${Date.now()}`;

    previewArea.innerHTML = `
        <img src="${jpgPath}" alt="Card Preview" class="preview-image">
    `;
}

function showDownloadSection(htmlFile, jpgFile) {
    const downloadSection = document.getElementById('downloadSection');
    const downloadHtml = document.getElementById('downloadHtml');
    const downloadJpg = document.getElementById('downloadJpg');

    downloadHtml.href = `/download/${htmlFile}`;
    downloadJpg.href = `/download/${jpgFile}`;

    downloadSection.style.display = 'block';
}

async function saveTemplate() {
    const templateName = document.getElementById('template_name').value.trim();

    if (!templateName) {
        showError('กรุณากรอกชื่อ Template');
        return;
    }

    const cardData = collectFormData();
    cardData.template_name = templateName;

    // Remove photo_path from template
    delete cardData.photo_path;

    try {
        const response = await fetch('/save-template', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cardData)
        });

        const data = await response.json();

        if (data.success) {
            showSuccess(data.message || 'บันทึก Template สำเร็จ!');
            document.getElementById('template_name').value = '';
            loadTemplates();
        } else {
            showError(data.error || 'เกิดข้อผิดพลาดในการบันทึก Template');
        }
    } catch (error) {
        console.error('Save template error:', error);
        showError('เกิดข้อผิดพลาดในการบันทึก Template');
    }
}

async function loadTemplates() {
    try {
        const response = await fetch('/load-templates');
        const data = await response.json();

        const select = document.getElementById('template_select');

        // Clear existing options (except first one)
        select.innerHTML = '<option value="">-- เลือก Template --</option>';

        // Add templates
        if (data.templates) {
            Object.keys(data.templates).forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Load templates error:', error);
    }
}

async function loadSelectedTemplate() {
    const select = document.getElementById('template_select');
    const templateName = select.value;

    if (!templateName) return;

    try {
        const response = await fetch('/load-templates');
        const data = await response.json();

        if (data.templates && data.templates[templateName]) {
            const template = data.templates[templateName];

            // Fill form with template data
            document.getElementById('year_cs').value = template.year_cs || 2026;
            document.getElementById('year_be').value = template.year_be || 2569;
            document.getElementById('wish1').value = template.wishes[0] || '';
            document.getElementById('wish2').value = template.wishes[1] || '';
            document.getElementById('signature').value = template.signature || '';
            document.getElementById('theme').value = template.theme || 'blue-gold';
            document.getElementById('thai_font').value = template.thai_font || 'noto-sans-thai';
            document.getElementById('english_font').value = template.english_font || 'poppins';

            // Font sizes
            if (template.font_sizes) {
                document.getElementById('size_year_badge').value = template.font_sizes['year-badge'] || 'medium';
                document.getElementById('size_main_title').value = template.font_sizes['main-title'] || 'medium';
                document.getElementById('size_thai_title').value = template.font_sizes['thai-title'] || 'medium';
                document.getElementById('size_wishes').value = template.font_sizes['wishes'] || 'medium';
                document.getElementById('size_signature').value = template.font_sizes['signature'] || 'medium';
            }

            showSuccess(`โหลด Template "${templateName}" สำเร็จ!`);
        }
    } catch (error) {
        console.error('Load selected template error:', error);
        showError('เกิดข้อผิดพลาดในการโหลด Template');
    }
}

function autoCalculateYears() {
    const yearCS = parseInt(document.getElementById('year_cs').value);
    if (!isNaN(yearCS)) {
        document.getElementById('year_be').value = yearCS + 543;
    }
}

function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showSuccess(message) {
    showMessage(message, 'success');
}

function showError(message) {
    showMessage(message, 'error');
}

function showMessage(message, type) {
    // Remove existing messages
    const existing = document.querySelectorAll('.success-message, .error-message');
    existing.forEach(el => el.remove());

    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;

    const formCard = document.querySelector('.form-card');
    formCard.insertBefore(messageDiv, formCard.firstChild);

    // Auto remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}
