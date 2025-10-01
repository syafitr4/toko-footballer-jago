<details>
<summary><b>Tugas 2</b></summary>

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
</details>

<details>
<summary><b>Tugas 3</b></summary>

1. Mengapa perlu data delivery
   Agar frontend dan layanan lain bisa memakai data yang sama, memisahkan UI dari logic, memudahkan skalabilitas dan otomasi, serta membuat respons terstruktur yang mudah divalidasi dan di cache
   Di tugas ini aku buat endpoint products json, products xml, dan versi per id

2. XML vs JSON
   JSON lebih ringkas, mudah dipakai di JavaScript dan banyak SDK, tipe datanya langsung sesuai, dan parsing biasanya lebih cepat
   XML tetap berguna jika butuh skema ketat atau dokumen campuran
   Untuk CRUD produk, JSON lebih praktis

3. Fungsi is_valid pada Form Django
   Menjalankan validator, mengonversi tipe, mengisi cleaned data, dan menyiapkan pesan error
   Dipakai sebelum simpan agar data kotor ditolak, aman, dan pengguna dapat umpan balik

4. Mengapa perlu csrf_token pada form
   Server memeriksa token unik di setiap POST
   Tanpa token, permintaan ditolak 403 dan situs rentan CSRF

5. Langkah implementasi yang kulakukan
   – Setup proyek dan app, daftarkan app dan template dasar
   – Model Product berisi name, price, category choices, description, stock, thumbnail, is featured, lalu migrasi
   – ModelForm untuk Product dan halaman tambah produk dengan csrf token
   – View show main untuk identitas dan daftar, create product untuk proses form dengan is valid lalu simpan, show product untuk detail
   – Hapus increment views yang bikin error
   – Routing untuk halaman utama, tambah produk, dan detail
   – Endpoint json dan xml untuk semua produk dan per id
   – Uji tambah produk, pastikan tampil dan endpoint sesuai data di database

6. Asdos sudah membantu banyak di tutorial2
</details>
<details>
<summary><b>Tugas 4</b></summary>

1. Apa itu Django AuthenticationForm? Kelebihan dan kekurangan
   AuthenticationForm adalah form bawaan untuk login yang memvalidasi username dan password lewat auth backend Django.
   Kelebihan: siap pakai, aman karena pakai hashing Django, pesan error standar rapi.
   Kekurangan: tampilan polos, kustomisasi flow terbatas (misal login pakai email), tidak ada throttling atau lockout bawaan.

2. Perbedaan autentikasi dan otorisasi serta implementasinya di Django
   Autentikasi = verifikasi identitas pengguna. Implementasi: authenticate, login, logout, request.user, user.is\authenticated.
   Otorisasi = cek hak akses setelah terautentikasi. Implementasi: permissions dan groups (user.has\perm), decorator login\required dan permission\required, flag staff dan superuser.

3. Kelebihan dan kekurangan session dan cookies untuk state
   Cookies: kelebihan ringan dan tidak perlu storage server; kekurangan mudah dibaca atau diubah klien jika tidak diamankan, ukuran terbatas, tidak cocok data sensitif.
   Session: kelebihan data disimpan di server sehingga lebih aman dan bisa lebih besar; kekurangan butuh storage server dan manajemen kedaluwarsa, ada overhead skalabilitas.

4. Apakah cookies aman secara default dan bagaimana Django menangani
   Tidak otomatis aman. Risiko: XSS, sniffing pada koneksi tanpa HTTPS, CSRF, pelacakan lintas situs.
   Penanganan Django: aktifkan CSRF middleware dan gunakan csrf\token pada form; gunakan flag HttpOnly, Secure, dan SameSite pada session cookie dan CSRF cookie; gunakan HTTPS; bisa pakai signed cookie untuk menjaga integritas nilai.

5. Cara mengimplementasikan checklist secara step-by-step
   Inisialisasi proyek dan app, daftarkan app di INSTALLED\APPS dan set ALLOWED\HOSTS
   Atur routing di config/urls.py dan main/urls.py
   Buat model Product lalu makemigrations dan migrate
   Buat ModelForm dan template form yang menyertakan csrf
   Implementasi views show\main, show\product, create\product
   Buat endpoint JSON dan XML (semua dan per id)
   Uji lokal halaman dan endpoint
   Deploy ke PWS dengan ALLOWED\HOSTS yang benar

</details>

<details>
<summary><b>Tugas 5</b></summary>

1. Saat sebuah elemen HTML cocok dengan banyak aturan CSS, browser menentukan gaya akhir berdasarkan kombinasi specificity dan urutan kemunculan aturan. Deklarasi dengan tanda penting menggunakan !important berada pada prioritas tertinggi, diikuti gaya inline yang ditulis langsung pada elemen. Setelah itu barulah skor spesifisitas bekerja, selector berbasis ID lebih kuat daripada selector berbasis kelas, atribut, atau pseudo class, dan semuanya lebih kuat daripada selector berbasis tipe elemen atau pseudo element. Kombinator tidak menambah skor. Jika dua aturan memiliki kekuatan yang sama, aturan yang muncul lebih akhir di sumber CSS yang digunakan akan menang. Prinsip praktisnya adalah menghindari pemakaian !important kecuali keadaan darurat, gunakan struktur stylesheet yang rapi agar aturan yang diinginkan secara alami mengalahkan aturan lain, dan pahami bahwa ID mengalahkan kelas, lalu kelas mengalahkan selector tipe.

2. Responsive design penting karena memastikan tampilan, keterbacaan, serta interaksi tetap nyaman di berbagai ukuran layar, mulai dari ponsel hingga desktop. Pengguna tidak perlu melakukan zoom atau menggulir ke samping, tombol tetap mudah disentuh, dan konten tersusun ulang agar tetap enak dilihat. Dampaknya terasa pada pengalaman pengguna, performa, dan peringkat mesin pencari, sebab situs yang ramah seluler biasanya dinilai lebih baik. Contoh yang sudah menerapkan desain responsif adalah Tokopedia, di mana grid produk bergeser dari satu kolom di ponsel menjadi beberapa kolom di tablet atau desktop, dan navigasi berubah menjadi menu hamburger pada layar sempit. Contoh yang belum responsif adalah situs Berkshire Hathaway yang mempertahankan tampilan lawas berlebar tetap, sehingga pada ponsel tampak mengecil, tidak proporsional, dan mengharuskan pengguna menggulir horizontal, kondisi ini jelas menurunkan kenyamanan dan konversi.

3. Margin, border, dan padding adalah tiga komponen dalam box model. Margin adalah ruang di luar kotak elemen yang memisahkan elemen dari elemen lain. Border adalah garis yang mengelilingi kotak elemen. Padding adalah ruang di dalam kotak elemen yang memisahkan konten dari bordernya. Dalam praktik, margin dipakai untuk memberi jarak antar komponen pada halaman, border memberi batas visual agar elemen terlihat tegas, dan padding memastikan konten tidak mepet ke tepi. Dengan memahami peran ketiganya, kita bisa menata tata letak yang lapang, rapi, dan mudah dibaca tanpa menambah elemen pembungkus.

4. Flexbox dan Grid adalah dua sistem tata letak modern yang saling melengkapi. Flexbox cocok untuk tata letak satu dimensi, baris atau kolom, dengan kontrol perataan, distribusi ruang, dan pembungkusan item saat layar mengecil. Ia sangat berguna untuk navbar, deretan tombol, serta pemusatan konten secara vertikal atau horizontal. CSS Grid cocok untuk tata letak dua dimensi, baris dan kolom sekaligus, sehingga ideal untuk galeri dan katalog produk, juga halaman yang kompleks. Dengan Grid, jumlah kolom dapat menyesuaikan lebar layar, jarak antar item konsisten, dan area tampilan bisa diatur lebih sistematis. Ringkasnya, gunakan Flexbox untuk susunan linear yang fleksibel, gunakan Grid ketika membutuhkan kanvas dua dimensi yang lebih terstruktur.

5. Implementasi checklist saya mulai dari sisi logika aplikasi, yaitu menambahkan fitur edit dan hapus produk. Saya menambahkan rute untuk edit dan delete, lalu menulis dua fungsi view yang mewajibkan pengguna login. Untuk fitur edit, saya mengambil objek produk berdasarkan identitasnya, mengikatnya ke form produk, kemudian pada pengiriman yang valid saya simpan perubahan, menampilkan pesan sukses, dan mengarahkan kembali ke halaman utama. Untuk fitur delete, saya menampilkan halaman konfirmasi sederhana, jika pengguna menekan tombol hapus maka produk dihapus dan aplikasi kembali ke daftar dengan pesan sukses. Pada tampilan kartu produk, saya menambahkan dua tombol, satu menuju halaman edit dan satu lagi berupa form penghapusan kecil agar alur kerja cepat. Setelah CRUD berfungsi, saya melakukan kustomisasi tampilan pada halaman login, register, tambah produk, edit produk, dan detail produk, saya menyatukan gaya form agar konsisten, menggunakan latar gelap, teks kontras, sudut membulat, dan efek fokus yang jelas. Untuk halaman daftar produk, saya menggunakan susunan grid yang responsif, jumlah kolom menyesuaikan lebar layar, setiap kartu berisi gambar bila tersedia, nama, harga, deskripsi singkat, serta tombol edit dan hapus. Saya juga menambahkan empty state, jika belum ada produk maka pengguna melihat ilustrasi dan pesan bahwa belum ada produk yang terdaftar beserta ajakan untuk menambahkan produk pertama. Navigasi saya buat responsif, di desktop menu tampil penuh, sementara di ponsel menu disederhanakan, dan navbar hanya ditampilkan setelah login menggunakan kondisi pada template sehingga halaman publik tetap bersih. Terakhir, saya menguji tampilan pada beberapa lebar layar untuk memastikan tidak ada overflow, pergeseran tata letak yang mengganggu, atau elemen yang saling bertabrakan, hasilnya alur CRUD terasa mulus dan antarmuka nyaman digunakan pada perangkat apa pun.

</details>
