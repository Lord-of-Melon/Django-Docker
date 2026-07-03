
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


<img width="1101" height="580" alt="image" src="https://github.com/user-attachments/assets/6199f7f4-ccd1-431b-9f5c-f2e88ec60bce" />
<img width="813" height="689" alt="image" src="https://github.com/user-attachments/assets/549b0e0a-20d6-438a-bc9a-71915eeb228e" />
<img width="851" height="650" alt="Screenshot 2026-07-03 175903" src="https://github.com/user-attachments/assets/c9dea802-b89c-4052-97bd-e8b542bbe2a2" />




---

## 2. Category

Kategori course dengan struktur hierarki menggunakan Self ForeignKey.

Contoh:

```
Programming
├── Web Development
└── Mobile Development
```

<img width="1099" height="549" alt="image" src="https://github.com/user-attachments/assets/7a28c6d3-02c7-404e-a028-32971b406419" />
<img width="1365" height="525" alt="image" src="https://github.com/user-attachments/assets/d1417f6d-75e2-44b8-a906-415e3bbe285f" />
<img width="1365" height="606" alt="image" src="https://github.com/user-attachments/assets/f6d7e88d-e4d3-489d-88b7-47e50e6028d3" />
<img width="1365" height="536" alt="image" src="https://github.com/user-attachments/assets/297450b3-a940-4677-8cb3-9753aa28f50d" />

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


<img width="1365" height="536" alt="image" src="https://github.com/user-attachments/assets/e23f0dc6-9c92-4d87-b488-9b3df33f1b50" />
<img width="1365" height="604" alt="image" src="https://github.com/user-attachments/assets/15326575-d857-4902-8264-7e058872573c" />
<img width="1365" height="672" alt="image" src="https://github.com/user-attachments/assets/a3fc27f0-e9eb-4565-8dc0-a1f3d1870253" />

---

## 4. Lesson

Setiap Course memiliki banyak Lesson.

Fitur:

- Ordering lesson
- Inline editing pada Django Admin


<img width="1101" height="567" alt="image" src="https://github.com/user-attachments/assets/2b933c01-b427-4b50-9a2d-dc89e49380ab" />
<img width="778" height="595" alt="image" src="https://github.com/user-attachments/assets/bc4e52f3-1533-4836-9f35-cd13f2069f2d" />
<img width="1365" height="536" alt="image" src="https://github.com/user-attachments/assets/2be95fcf-2cea-4ee3-9fee-1d9441e71b18" />

---

## 5. Enrollment

Relasi antara Student dan Course.

Constraint:

- Satu student tidak dapat mendaftar course yang sama lebih dari satu kali.

Menggunakan:

```python
unique_together = ('student', 'course')
```


<img width="1365" height="540" alt="image" src="https://github.com/user-attachments/assets/826768ef-0727-4398-8568-4d1f68f37559" />
<img width="785" height="556" alt="image" src="https://github.com/user-attachments/assets/61955cbd-6c67-4c47-b711-f2fb31b0dabf" />
<img width="1365" height="547" alt="image" src="https://github.com/user-attachments/assets/42c8d111-9b25-4274-978b-b9dc7e7b85af" />

---

## 6. Progress

Mencatat progress penyelesaian lesson.

Status:

- Completed
- In Progress

<img width="1365" height="534" alt="image" src="https://github.com/user-attachments/assets/1074874a-e2c9-4a35-8938-99f1dd02a0fd" />
<img width="1363" height="538" alt="image" src="https://github.com/user-attachments/assets/9fe1fe00-9346-4f0d-adbc-d096866c034f" />
<img width="1365" height="536" alt="image" src="https://github.com/user-attachments/assets/aa2cdf06-a818-4f17-ae76-607a62909533" />

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



