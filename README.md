https://daffa-syafitra-tokofootballerjago.pbp.cs.ui.ac.id

1) Implementasi checklist – langkah demi langkah (versi saya)
1. Siapkan environment lokal
python -m venv venv && source venv/bin/activate (Windows: venv\Scripts\activate)
pip install django
2. Buat proyek & app
django-admin startproject config .
python manage.py startapp main
3. Registrasi app & konfigurasi dasar
Tambah "main" ke INSTALLED_APPS di config/settings.py.
Set LANGUAGE_CODE, TIME_ZONE, ALLOWED_HOSTS (tambahkan host PWS).
4. Routing URL
Di config/urls.py, arahkan path ke main.urls (pakai include).
Buat main/urls.py dan mapping path("", views.index, ...).
5. Views + Template (MTV)
Di main/views.py buat view index(request) yang membentuk context (misal nama app, nama, kelas).
Buat folder templates/main/index.html, render variabel dari context.
6. Static & template dirs
Pastikan TEMPLATES[0]['DIRS'] atau pakai struktur templates/.
(Opsional) siapkan STATIC_URL, STATICFILES_DIRS untuk CSS sederhana.
7. Model & migrasi (kalau butuh data)
Definisikan model di main/models.py.
python manage.py makemigrations && python manage.py migrate.
8. Cek lokal
python manage.py runserver → buka http://127.0.0.1:8000/ dan pastikan halaman tampil.
9. Versioning & repo
Inisialisasi git, commit perubahan penting (config, urls, views, templates, model).
10. Deploy ke PWS
Push ke repo yang dikaitkan ke PWS kamu, set ALLOWED_HOSTS ke domain PWS, jalankan collectstatic (jika pakai static), lalu uji URL PWS-mu.

2) bagan yang berisi request client ke web aplikasi berbasis Django
![alt text](<WhatsApp Image 2025-09-10 at 11.26.44_c6514c14.jpg>)

3) Peran settings.py pada proyek Django
settings.py adalah pusat konfigurasi:
1. INSTALLED_APPS (registrasi app), MIDDLEWARE, TEMPLATES, DATABASES.
2. STATIC/MEDIA (asset), ALLOWED_HOSTS/CSRF (keamanan & host deploy), TIME_ZONE/LANGUAGE_CODE.
3. Menyimpan SECRET_KEY dan pengaturan lain yang memengaruhi seluruh proyek.

4) Cara kerja migrasi database di Django
1. Ubah/definisikan model di models.py.
2. Jalankan python manage.py makemigrations → Django membuat berkas migrasi (riwayat skema).
3. Jalankan python manage.py migrate → menerapkan migrasi ke DB.
4. Setiap perubahan model → ulangi langkah 2–3. Riwayat migrasi membuat skema bisa berkembang aman dari waktu ke waktu.

5) Kenapa Django cocok jadi permulaan belajar pengembangan perangkat lunak? 
Open source (gratis & komunitas besar)
Ridiculously fast (cepat untuk dikembangkan)
Fully loaded (fitur bawaan lengkap: ORM, admin, auth, dll.)
Reassuringly secure (banyak proteksi keamanan bawaan)
Exceedingly scalable (siap untuk skala besar)
Incredibly versatile (serbaguna untuk berbagai jenis aplikasi)

6) Feedback untuk asdos
asdosnya udah baik dan sangat membantu saya yg kesusahan di tutorial 1 kemarin