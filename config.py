"""
Configuration for themes, colors, and fonts
"""

THEMES = {
    'blue-gold': {
        'name': 'Blue & Gold (Classic)',
        'primary': '#3b82f6',
        'secondary': '#fbbf24',
        'gradient_start': '#3b82f6',
        'gradient_end': '#fbbf24',
        'bg_gradient': 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%)',
    },
    'ai-tech': {
        'name': 'AI & Tech (Digital)',
        'primary': '#00d4ff',
        'secondary': '#7c3aed',
        'gradient_start': '#00d4ff',
        'gradient_end': '#7c3aed',
        'bg_gradient': 'linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%)',
    },
    'chinese-new-year': {
        'name': 'Chinese New Year (ตรุษจีน)',
        'primary': '#dc2626',
        'secondary': '#fbbf24',
        'gradient_start': '#dc2626',
        'gradient_end': '#fbbf24',
        'bg_gradient': 'linear-gradient(135deg, #1a0000 0%, #2a0a00 50%, #1a0000 100%)',
    },
    'red-green': {
        'name': 'Christmas (คริสต์มาส)',
        'primary': '#ef4444',
        'secondary': '#10b981',
        'gradient_start': '#ef4444',
        'gradient_end': '#10b981',
        'bg_gradient': 'linear-gradient(135deg, #1a0a0a 0%, #0a1a0a 50%, #1a0a0a 100%)',
    },
    'songkran': {
        'name': 'Songkran (สงกรานต์)',
        'primary': '#06b6d4',
        'secondary': '#f97316',
        'gradient_start': '#06b6d4',
        'gradient_end': '#f97316',
        'bg_gradient': 'linear-gradient(135deg, #0a1a1a 0%, #1a1a0a 50%, #0a1a1a 100%)',
    },
    'halloween': {
        'name': 'Halloween (ฮาโลวีน)',
        'primary': '#f97316',
        'secondary': '#8b5cf6',
        'gradient_start': '#f97316',
        'gradient_end': '#8b5cf6',
        'bg_gradient': 'linear-gradient(135deg, #1a0a00 0%, #0a0a1a 50%, #1a0a00 100%)',
    },
    'business': {
        'name': 'Business (มืออาชีพ)',
        'primary': '#1e40af',
        'secondary': '#64748b',
        'gradient_start': '#1e40af',
        'gradient_end': '#64748b',
        'bg_gradient': 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%)',
    },
    'islamic': {
        'name': 'Islamic (อิสลาม)',
        'primary': '#16a34a',
        'secondary': '#f59e0b',
        'gradient_start': '#16a34a',
        'gradient_end': '#f59e0b',
        'bg_gradient': 'linear-gradient(135deg, #0a1a0a 0%, #1a1a0a 50%, #0a1a0a 100%)',
    },
    'purple-pink': {
        'name': 'Purple & Pink (Modern)',
        'primary': '#a855f7',
        'secondary': '#ec4899',
        'gradient_start': '#a855f7',
        'gradient_end': '#ec4899',
        'bg_gradient': 'linear-gradient(135deg, #0a0a1a 0%, #1a0a1a 50%, #0a0a1a 100%)',
    },
    'cyan-violet': {
        'name': 'Cyan & Violet (Neon)',
        'primary': '#06b6d4',
        'secondary': '#8b5cf6',
        'gradient_start': '#06b6d4',
        'gradient_end': '#8b5cf6',
        'bg_gradient': 'linear-gradient(135deg, #0a1a1a 0%, #0a0a1a 50%, #0a1a1a 100%)',
    },
    'orange-yellow': {
        'name': 'Orange & Yellow (Sunset)',
        'primary': '#f97316',
        'secondary': '#eab308',
        'gradient_start': '#f97316',
        'gradient_end': '#eab308',
        'bg_gradient': 'linear-gradient(135deg, #1a0a00 0%, #1a1a0a 50%, #1a0a00 100%)',
    },
    'silver-gold': {
        'name': 'Silver & Gold (Luxury)',
        'primary': '#94a3b8',
        'secondary': '#fbbf24',
        'gradient_start': '#94a3b8',
        'gradient_end': '#fbbf24',
        'bg_gradient': 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%)',
    },
}

FONTS = {
    'thai': {
        'noto-sans-thai': {
            'name': 'Noto Sans Thai',
            'url': 'https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700;800&display=swap',
            'family': "'Noto Sans Thai', sans-serif"
        },
        'sarabun': {
            'name': 'Sarabun',
            'url': 'https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&display=swap',
            'family': "'Sarabun', sans-serif"
        },
        'prompt': {
            'name': 'Prompt',
            'url': 'https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&display=swap',
            'family': "'Prompt', sans-serif"
        },
        'kanit': {
            'name': 'Kanit',
            'url': 'https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700;800&display=swap',
            'family': "'Kanit', sans-serif"
        },
        'bai-jamjuree': {
            'name': 'Bai Jamjuree',
            'url': 'https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@300;400;500;600;700&display=swap',
            'family': "'Bai Jamjuree', sans-serif"
        }
    },
    'english': {
        'poppins': {
            'name': 'Poppins',
            'url': 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap',
            'family': "'Poppins', sans-serif"
        },
        'playfair': {
            'name': 'Playfair Display',
            'url': 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap',
            'family': "'Playfair Display', serif"
        },
        'montserrat': {
            'name': 'Montserrat',
            'url': 'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&display=swap',
            'family': "'Montserrat', sans-serif"
        },
        'roboto': {
            'name': 'Roboto',
            'url': 'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap',
            'family': "'Roboto', sans-serif"
        },
        'inter': {
            'name': 'Inter',
            'url': 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap',
            'family': "'Inter', sans-serif"
        }
    }
}

FONT_SIZES = {
    'year-badge': {
        'small': '24px',
        'medium': '36px',
        'large': '48px'
    },
    'main-title': {
        'small': '48px',
        'medium': '72px',
        'large': '96px'
    },
    'thai-title': {
        'small': '32px',
        'medium': '48px',
        'large': '64px'
    },
    'wishes': {
        'small': '16px',
        'medium': '20px',
        'large': '24px'
    },
    'signature': {
        'small': '24px',
        'medium': '36px',
        'large': '48px'
    }
}

DEFAULT_SETTINGS = {
    'theme': 'blue-gold',
    'thai_font': 'noto-sans-thai',
    'english_font': 'poppins',
    'year_cs': 2026,
    'year_be': 2569,
    'wishes': [
        'ขอให้ปีนี้ เป็นปีแห่งความก้าวหน้า ความมั่นคง<br>และความสำเร็จในทุกภารกิจที่ตั้งใจ',
        'ขอให้ทุกท่านมีพลังใจที่เข้มแข็ง พร้อมความสุข<br>ความราบรื่น และการเติบโตที่ดีตลอดไป'
    ],
    'signature': 'เสกศักดิ์ ช่อปลอด',
    'font_sizes': {
        'year-badge': 'medium',
        'main-title': 'medium',
        'thai-title': 'medium',
        'wishes': 'medium',
        'signature': 'medium'
    }
}
