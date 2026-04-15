# Django-Docker
Project django-docker app

Cara menjalankan project:
  -docker compose build (untuk pertama kali)
  -docker compose up -d (untuk pertama kali)
  -docker compose exec web python manage.py migrate (untuk pertama kali)
  -docker compose start

Cara menutup project:
  -docker compose stop
  -docker compose down (jika ingin menghentikan dan menghapus compose)

Environment variables explanation:
  -SECRET_KEY → kunci rahasia Django (buat security, jangan bocor)
  -DEBUG → mode dev (True = tampilkan error detail)
  -ALLOWED_HOSTS → domain/IP yang boleh akses app
  
  -DB_NAME → nama database
  -DB_USER → user login DB
  -DB_PASSWORD → password DB
  -DB_HOST → alamat DB (db = nama service Docker)
  -DB_PORT → port DB (default PostgreSQL: 5432)

<img width="1366" height="768" alt="Screenshot (48)" src="https://github.com/user-attachments/assets/7bac839d-2c0f-4e96-b00e-660f5970294d" />
