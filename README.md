# SplitBill Smart

Aplikasi fullstack berbasis **Microservices** untuk membagi tagihan grup secara otomatis berdasarkan item yang dikonsumsi masing-masing anggota.

**Mata Kuliah:** Perangkat Lunak Berbasis Komponen (PLBK)

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 5173)                   │
│              Vite + Tailwind CSS + Axios + React Router          │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   API Gateway (Port 8000)                        │
│                     Django REST Proxy                            │
└──┬────────┬────────┬────────┬────────┬────────┬─────────────────┘
   │        │        │        │        │        │
   ▼        ▼        ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ User │ │Group │ │ Bill │ │Settle│ │ OCR  │ │ Notif│
│ 8001 │ │ 8002 │ │ 8003 │ │ 8004 │ │ 8005 │ │ 8006 │
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘
   │        │        │        │        │        │
   ▼        ▼        ▼        ▼        ▼        ▼
 SQLite  SQLite  SQLite  SQLite  SQLite  SQLite
 (db)    (db)    (db)    (db)    (db)    (db)
```

### Diagram Alur Workflow

```
Login → Buat Grup → Tambah Anggota → Upload Struk → OCR Parse
   → Assign Item ke Anggota → Hitung Total → Settlement → Notifikasi
```

### Routing API Gateway

| Gateway Route | Target Service | Port |
|---------------|----------------|------|
| `/api/auth/*` | User Service | 8001 |
| `/api/groups/*` | Group Service | 8002 |
| `/api/bills/*` | Bill Service | 8003 |
| `/api/settlement/*` | Settlement Service | 8004 |
| `/api/receipt/*` | Receipt OCR Service | 8005 |
| `/api/notifications/*` | Notification Service | 8006 |

---

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Frontend | React, Vite, Tailwind CSS, Axios, React Router |
| Backend | Django REST Framework |
| Database | SQLite (per service) |
| Auth | JWT (SimpleJWT) |
| OCR | pytesseract / easyocr |
| Gateway | Django API Gateway |

---

## Struktur Folder

```
SplitBill/
├── frontend/                 # React frontend
├── services/
│   ├── api_gateway/          # Port 8000
│   ├── user_service/         # Port 8001
│   ├── group_service/        # Port 8002
│   ├── bill_service/         # Port 8003
│   ├── settlement_service/   # Port 8004
│   ├── receipt_ocr_service/  # Port 8005
│   └── notification_service/ # Port 8006
├── scripts/
│   ├── migrate_all.bat
│   ├── start_all.bat
│   └── seed_data.py
├── requirements.txt
└── README.md
```

---

## Persyaratan

- Python 3.10+
- Node.js 18+
- npm
- (Opsional) Tesseract OCR untuk fitur scan struk asli

---

## Instalasi

### 1. Clone / buka project

```bash
cd "d:\Nisa\Lab PLBK\UAS\SplitBill"
```

### 2. Setup Python virtual environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Jalankan migrasi semua service

```bash
scripts\migrate_all.bat
```

### 4. Seed sample data (opsional)

```bash
python scripts\seed_data.py
```

### 5. Setup frontend

```bash
cd frontend
npm install
```

---

## Menjalankan Aplikasi

### Cara Cepat (Windows)

```bash
scripts\start_all.bat
```

Script ini akan membuka 8 terminal: 6 microservices + gateway + frontend.

### Cara Manual

Jalankan setiap service di terminal terpisah (dari root project, dengan venv aktif):

```bash
# Terminal 1 - User Service
cd services/user_service && python manage.py runserver 8001

# Terminal 2 - Group Service
cd services/group_service && python manage.py runserver 8002

# Terminal 3 - Bill Service
cd services/bill_service && python manage.py runserver 8003

# Terminal 4 - Settlement Service
cd services/settlement_service && python manage.py runserver 8004

# Terminal 5 - Receipt OCR Service
cd services/receipt_ocr_service && python manage.py runserver 8005

# Terminal 6 - Notification Service
cd services/notification_service && python manage.py runserver 8006

# Terminal 7 - API Gateway
cd services/api_gateway && python manage.py runserver 8000

# Terminal 8 - Frontend
cd frontend && npm run dev
```

### Akses Aplikasi

| URL | Keterangan |
|-----|------------|
| http://localhost:5173 | Frontend |
| http://localhost:8000 | API Gateway |

---

## Akun Demo (setelah seed)

| Username | Password |
|----------|----------|
| andi | password123 |
| budi | password123 |
| citra | password123 |
| dodi | password123 |

---

## Contoh Settlement

**Skenario:** Andi bayar Rp120.000

| Anggota | Konsumsi |
|---------|----------|
| Budi | Rp30.000 |
| Citra | Rp40.000 |
| Dodi | Rp50.000 |

**Output Settlement:**

- Budi bayar Andi Rp30.000
- Citra bayar Andi Rp40.000
- Dodi bayar Andi Rp50.000

Endpoint: `GET /api/settlement/{bill_id}`

---

## API Endpoints

### User Service (via `/api/auth/`)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/auth/register` | Registrasi user |
| POST | `/api/auth/login` | Login & dapat JWT |
| GET | `/api/auth/profile` | Profil user |

### Group Service (via `/api/groups/`)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/groups` | Buat grup |
| GET | `/api/groups` | List grup |
| POST | `/api/groups/{id}/members` | Tambah anggota |
| GET | `/api/groups/{id}/members` | List anggota |

### Bill Service (via `/api/bills/`)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/bills` | Buat tagihan |
| GET | `/api/bills` | List tagihan |
| POST | `/api/bills/{id}/items` | Tambah item |
| GET | `/api/bills/{id}` | Detail tagihan |

### Settlement Service

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/settlement/{bill_id}` | Hitung settlement |

### Receipt OCR Service

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/receipt/upload` | Upload & scan struk |

### Notification Service

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/notify` | Kirim notifikasi |
| GET | `/api/notifications` | List notifikasi user |

---

## Halaman Frontend

1. **Login** — `/login`
2. **Register** — `/register`
3. **Dashboard** — `/dashboard`
4. **Group Management** — `/groups`
5. **Create Bill** — `/bills/create`
6. **Upload Receipt** — `/receipt`
7. **Assign Item To Members** — `/assign/:billId`
8. **Settlement Result** — `/settlement/:billId`
9. **Notification Page** — `/notifications`

---

## Komunikasi Antar Service

- **Settlement Service** → Bill Service (REST) untuk data tagihan
- **Settlement Service** → Group Service (REST) untuk data anggota
- **Bill Service** → Notification Service (REST) saat tagihan/item baru
- Semua service menggunakan **JWT shared secret** untuk validasi token

---

## OCR (Receipt Scan)

Service OCR mendukung:
1. **pytesseract** (butuh install Tesseract OCR)
2. **easyocr** (fallback)
3. **Demo mode** — jika OCR tidak tersedia, mengembalikan item sample

Install Tesseract (Windows): https://github.com/UB-Mannheim/tesseract/wiki

---

## PLBK Compliance

- ✅ Setiap service memiliki database SQLite sendiri
- ✅ Setiap service berjalan independen di port berbeda
- ✅ Komunikasi antar service via REST API
- ✅ Struktur folder dipisah per service
- ✅ API Gateway sebagai single entry point
- ✅ Tanpa Docker / Kubernetes
- ✅ Siap dijalankan di localhost

---

## Troubleshooting

**Port sudah digunakan:** Pastikan tidak ada proses lain di port 8000–8006 dan 5173.

**401 Unauthorized:** Login ulang untuk refresh JWT token.

**Service unavailable:** Pastikan semua 7 backend service sudah running sebelum akses frontend.

**OCR tidak akurat:** Install Tesseract OCR atau gunakan input manual di halaman Assign Items.

---

## Lisensi

Project ini dibuat untuk keperluan akademik mata kuliah PLBK.
