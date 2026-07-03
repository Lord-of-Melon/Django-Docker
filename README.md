
# Django-Docker
Project django-docker app

# Tech Stack
- Python
- Django
- PostgreSQL
- Docker
- Docker Compose

Cara menjalankan project:
```
    docker compose build (untuk pertama kali)
    docker compose up -d (untuk pertama kali)
    docker compose exec web python manage.py migrate 
    docker compose start
```
Cara menutup project:
```  
    docker compose stop
    docker compose down (jika ingin menghentikan dan menghapus compose)
```
Environment variables explanation:
```
    SECRET_KEY → kunci rahasia Django (buat security, jangan bocor)
    DEBUG → mode dev (True = tampilkan error detail)
    ALLOWED_HOSTS → domain/IP yang boleh akses app
 
    DB_NAME → nama database
    DB_USER → user login DB
    DB_PASSWORD → password DB
    DB_HOST → alamat DB (db = nama service Docker)
    DB_PORT → port DB (default PostgreSQL: 5432)
```
Buka di browser:
```
http://localhost:8000 - halaman depan djanggo
http://localhost:8000 - halaman admin
```
<img width="1366" height="768" alt="Screenshot (48)" src="https://github.com/user-attachments/assets/7bac839d-2c0f-4e96-b00e-660f5970294d" />
halaman depan djanggo

<< Progress 2 >>

<img width="979" height="715" alt="image" src="https://github.com/user-attachments/assets/81e8e8a7-7d0c-4dd7-b8f7-65d7ea818336" />
halaman depan admin

# Penambahan pada data models:
## 1. User
Custom User menggunakan `AbstractUser`.

Role yang tersedia:
- Admin
- Instructor
- Student

---

## 2. Category

Kategori course dengan struktur hierarki menggunakan Self ForeignKey.

Contoh:

```
Programming
├── Web Development
│   ├── Django
│   └── Flask
└── Mobile Development
```

---

## 3. Course

Setiap course memiliki:

- Instructor
- Category

Relasi:

```
Instructor (User)
        │
        ▼
      Course
        ▲
        │
    Category
```

---

## 4. Lesson

Setiap Course memiliki banyak Lesson.

Fitur:

- Ordering lesson
- Inline editing pada Django Admin

---

## 5. Enrollment

Relasi antara Student dan Course.

Constraint:

- Satu student tidak dapat mendaftar course yang sama lebih dari satu kali.

Menggunakan:

```python
unique_together = ('student', 'course')
```

---

## 6. Progress

Mencatat progress penyelesaian lesson.

Status:

- Completed
- In Progress
# Custom Model Managers

## Course Manager

### `Course.objects.for_listing()`

Digunakan untuk mengoptimalkan query pada halaman daftar course menggunakan `select_related()`.

Contoh:

```python
Course.objects.for_listing()
```

---

## Enrollment Manager

### `Enrollment.objects.for_student_dashboard()`

Mengoptimalkan dashboard student dengan memanfaatkan:

- `select_related()`
- `prefetch_related()`

untuk mengurangi jumlah query database.

Contoh:

```python
Enrollment.objects.for_student_dashboard()
```

---
# Query Optimization

Project ini mendemonstrasikan masalah **N+1 Query Problem**.

## Tanpa Optimasi

```
Enrollment
 ├── Query Enrollment
 ├── Query Course
 ├── Query Instructor
 ├── Query Category
 ├── Query Lesson
 └── ...
```

Jumlah query meningkat seiring bertambahnya data.

---

## Dengan Optimasi

Menggunakan:

```python
select_related()
prefetch_related()
```

Sehingga data terkait diambil dalam jumlah query yang jauh lebih sedikit.

# Django Admin

Konfigurasi Admin meliputi:

- Informative List Display
- Search Functionality
- Filter Data
- Lesson Inline pada Course
- Optimized Query menggunakan `list_select_related()`



