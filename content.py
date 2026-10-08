# Site copy, transcribed from WEBSITE-SPEC.md v1.0. Every value is (Bahasa Indonesia, English).
# Edit copy here, then run `python build.py`. Inline markers:
#   {{CONTACT_EMAIL}}  replaced from config.CONTACT_EMAIL
#   **bold**           rendered as <strong>

SITE = "obscur4"
DOMAIN = "obscur4.online"

SLUGS = {
    "home":      ("/", "/en/"),
    "awareness": ("/kesadaran-phishing/", "/en/awareness-phishing/"),
    "mobile":    ("/penilaian-aplikasi-mobile/", "/en/mobile-assessment/"),
    "how":       ("/cara-kerja/", "/en/how-we-work/"),
    "partners":  ("/mitra/", "/en/partners/"),
    "about":     ("/tentang/", "/en/about/"),
    "contact":   ("/kontak/", "/en/contact/"),
    "privacy":   ("/privasi/", "/en/privacy/"),
    "sent":      ("/kontak/terkirim/", "/en/contact/sent/"),
}

CHROME = {
    "nav": [
        ("home", ("Beranda", "Home")),
        ("awareness", ("Kesadaran & Phishing", "Awareness & Phishing")),
        ("mobile", ("Penilaian Aplikasi Mobile", "Mobile Assessment")),
        ("how", ("Cara Kerja", "How We Work")),
        ("partners", ("Mitra", "Partners")),
        ("about", ("Tentang", "About")),
        ("contact", ("Kontak", "Contact")),
    ],
    "nav_button": ("Ajukan permintaan", "Make a request"),
    "lang_switch": ("English", "Bahasa Indonesia"),
    "menu": ("Menu", "Menu"),
    "skip": ("Langsung ke konten", "Skip to content"),
    "tagline": ("Kesadaran keamanan dan penilaian aplikasi mobile untuk organisasi di Indonesia.",
                "Security awareness and mobile app assessment for organizations in Indonesia."),
    "footer_privacy": ("Pemberitahuan Privasi", "Privacy Notice"),
    "footer_contact": ("Kontak", "Contact"),
    "menu_close": ("Tutup", "Close"),
    "to_top": ("Back to top", "Back to top"),
    "footer_services": ("Services", "Services"),
    "footer_company": ("Company", "Company"),
    "scroll_hint": ("Scroll", "Scroll"),
    "preview_bar": ("Pratinjau. Belum untuk publikasi: beberapa isi masih menunggu keputusan.",
                    "Preview. Not for publication: some content is still pending decisions."),
}

PAGES = {}

# ---------------------------------------------------------------- 1. Home
PAGES["home"] = {
    "meta_title": ("obscur4 | Simulasi phishing dan penilaian aplikasi mobile",
                   "obscur4 | Phishing simulation and mobile app assessment"),
    "meta_desc": ("Program kesadaran keamanan dan simulasi phishing berbahasa Indonesia, serta penilaian aplikasi mobile dengan bukti yang dapat diperiksa.",
                  "Managed security awareness and phishing simulation in Bahasa Indonesia, plus mobile app assessment with evidence you can check."),
    "hero_h": ("Simulasi phishing dan kesadaran keamanan ==berbahasa Indonesia==, kami kelola untuk Anda.",
               "Phishing simulation and security awareness ==in Bahasa Indonesia==, run for you."),
    "hero_sub": ("Kami menjalankan kampanye phishing dan pelatihan dalam Bahasa Indonesia untuk Anda, lalu melaporkannya dalam format yang siap dipakai tim audit dan risiko.",
                 "We run localized phishing campaigns and Bahasa Indonesia training for you, and report in a form your audit and risk teams can use."),
    "cta1": ("Ajukan Baseline", "Request a Baseline"),
    "cta2": ("Lihat cara kerja kami", "See how we work"),
    "services_h": ("Dua layanan", "Two services"),
    "svc_a_t": ("Kesadaran keamanan dan simulasi phishing", "Awareness and phishing simulation"),
    "svc_a_b": ("Program terkelola: kampanye phishing yang disusun untuk konteks Indonesia, modul pelatihan berbahasa Indonesia, dan pelaporan triwulanan. Mulai dari satu kampanye Baseline.",
                "A managed programme: phishing campaigns written for Indonesian context, Bahasa Indonesia training modules and quarterly reporting. Start with one Baseline campaign."),
    "svc_b_t": ("Penilaian aplikasi mobile", "Mobile app assessment"),
    "svc_b_b": ("Penilaian spesialis atas satu build aplikasi. Setiap temuan disertai artefak dan langkah reproduksinya.",
                "A specialist assessment of one app build. Each finding comes with its artifact and the steps to reproduce it."),
    "more": ("Selengkapnya", "Read more"),
    "problem_h": ("Pengujian keamanan kini bagian dari pekerjaan yang diatur",
                  "Security testing is now part of regulated work"),
    "problem_b": ("Regulator sektor keuangan menetapkan ekspektasi pengujian ketahanan siber, dan UU PDP berlaku bagi setiap organisasi yang memproses data pribadi. Tim Anda membutuhkan pengujian yang dapat dipertanggungjawabkan.",
                  "Financial regulators set cyber-resilience testing expectations, and the personal data protection law (UU PDP) applies to any organization that processes personal data. Your team needs testing it can account for."),
    "trust_h": ("Otorisasi, bukti, dan penanganan data", "Authorization, evidence and data handling"),
    "trust": [
        (("Otorisasi", "Authorization"),
         ("Tidak ada pekerjaan dimulai tanpa catatan otorisasi tertulis yang menetapkan ruang lingkup. Pekerjaan di luar ruang lingkup itu tidak kami lakukan.",
          "No work starts without a written authorization record that sets the scope. We do not work outside that scope.")),
        (("Bukti", "Evidence"),
         ("Setiap temuan yang dilaporkan dapat ditelusuri ke artefak tersimpan dan urutan perintah yang tercatat.",
          "Every reported finding traces to a stored artifact and a recorded command sequence.")),
        (("Sanitasi dan data", "Sanitization and data"),
         ("Lingkungan uji bersifat sekali pakai dan terpisah. Data tiap klien dipisahkan, ekspor disamarkan, dan identitas dihapus dari apa pun yang dibagikan ke vendor.",
          "Test environments are disposable and segmented. Each client's data is kept apart, exports are redacted, and identifiers are removed from anything shared with a vendor.")),
    ],
    "trust_link": ("Baca selengkapnya di Cara Kerja", "Read more in How We Work"),
    "who_h": ("Untuk siapa", "Who it is for"),
    "who_b": ("Kepala keamanan siber dan risiko TI di bank, perusahaan pendanaan fintech, dan asuransi; pimpinan teknik yang perlu merilis tanpa terhambat keamanan; penyedia lapisan proteksi aplikasi yang menginginkan verifikasi independen atas kualitas integrasinya.",
              "Cyber and IT-risk heads at banks, fintech lenders and insurers; engineering leads who need to ship without security becoming the blocker; app-protection providers that want independent verification of their integration quality."),
    "closing_h": ("Sampaikan apa yang perlu Anda uji.", "Tell us what you need to test."),
    "closing_a": ("Ajukan Baseline", "Request a Baseline"),
    "closing_b": ("Ajukan penilaian aplikasi mobile", "Request a mobile assessment"),
}

# ---------------------------------------------------------------- 2. Awareness
PAGES["awareness"] = {
    "meta_title": ("Simulasi Phishing & Kesadaran Keamanan | obscur4", "Phishing Simulation & Security Awareness | obscur4"),
    "hero_h": ("Kampanye phishing untuk ==lingkungan kerja Indonesia==, dengan laporan yang dapat ditelusuri auditor.",
               "Phishing campaigns written for ==Indonesian workplaces==, with reports your auditors can follow."),
    "hero_sub": ("Program terkelola: kampanye berlokal, modul pelatihan berbahasa Indonesia, dan laporan triwulanan. Mulai dari satu kampanye Baseline.",
                 "A managed programme: localized campaigns, Bahasa Indonesia training modules and quarterly reports. Start with one Baseline campaign."),
    "cta1": ("Ajukan Baseline", "Request a Baseline"),
    "cta2": ("Tanyakan tentang Program", "Ask about the Programme"),
    "problem_h": ("Materi yang ditulis untuk pasar lain tidak menjangkau staf Anda",
                  "Content written for another market does not reach your staff"),
    "problem_b": ("Pelatihan dan umpan phishing yang sekadar diterjemahkan, bukan disusun untuk lingkungan kerja di Indonesia, menguji situasi yang tidak dihadapi staf Anda. Kami menyusun umpan dari jenis pesan yang lazim di tempat kerja Indonesia, seperti pemberitahuan bank, pengiriman paket, pajak, dan pesan dari atasan.",
                  "Training and lures that are translated, not written for Indonesian workplaces, test a situation your staff do not face. We write lures from message types common in Indonesian workplaces, such as bank notices, parcel deliveries, tax and messages from a manager."),
    "how_h": ("Cara program berjalan", "How a programme runs"),
    "steps": [
        (("Tetapkan ruang lingkup dan otorisasi", "Scope and authorize"),
         ("Kami menyepakati kelompok sasaran, domain pengirim, dan waktu, lalu mencatat otorisasi tertulis sebelum pesan pertama dikirim.",
          "We agree target groups, sending domains and timing, and record written authorization before the first message is sent.")),
        (("Susun dalam Bahasa Indonesia", "Write in Bahasa Indonesia"),
         ("Umpan phishing dan halaman tujuan ditulis untuk lingkungan kerja di Indonesia.",
          "Lures and landing pages are written for Indonesian workplaces.")),
        (("Luncurkan dari platform", "Launch from the platform"),
         ("Kampanye diluncurkan dan dipantau dari platform kami, bukan dirakit manual.",
          "Campaigns are launched and tracked from our platform, not assembled by hand.")),
        (("Latih", "Train"),
         ("Modul pelatihan berbahasa Indonesia menyertai kampanye.",
          "Bahasa Indonesia training modules accompany the campaigns.")),
        (("Laporkan", "Report"),
         ("Hasil disusun menjadi laporan, dengan tanda tangan penanggung jawab.",
          "Results are compiled into a report with a named sign-off.")),
    ],
    "ways_h": ("Dua bentuk layanan", "Two ways to buy"),
    "offers": [
        (("Baseline", "Baseline"),
         ("Satu kampanye phishing berlokal dan laporan awal tingkat kesadaran. Ruang lingkup dan penawaran disusun per kebutuhan.",
          "One localized phishing campaign and an awareness baseline report. Scope and quote are set per engagement.")),
        (("Program", "Programme"),
         ("Tahunan: kampanye berlokal berulang, modul pelatihan berbahasa Indonesia, dan laporan triwulanan yang tersusun untuk tinjauan audit dan risiko. Dikelola oleh kami; ruang lingkup dan penawaran disusun per kebutuhan.",
          "Annual: recurring localized campaigns, Bahasa Indonesia training modules and quarterly reports structured for audit and risk review. Managed by us; scope and quote are set per engagement.")),
    ],
    "get_h": ("Yang Anda terima", "What you get"),
    "get": [
        ("Laporan kampanye per kelompok sasaran: terkirim, dibuka, diklik, dilaporkan, dan pengiriman formulir.",
         "Campaign reports by target group: delivered, opened, clicked, reported and form submissions."),
        ("Catatan penyelesaian pelatihan.", "Training completion records."),
        ("Tren antarkampanye dalam laporan triwulanan.", "Trends across campaigns in the quarterly report."),
        ("Ekspor yang dihasilkan platform untuk tim audit dan risiko.", "Platform-generated exports for audit and risk teams."),
        ("Nilai yang diketik staf pada halaman simulasi tidak pernah dikirim ataupun disimpan.",
         "Values staff type into a simulation page are never transmitted or stored."),
    ],
    "who_h": ("Untuk siapa", "Who it is for"),
    "who_b": ("Kepala keamanan siber dan risiko TI di perusahaan jasa keuangan yang diawasi OJK, seperti bank, perusahaan pendanaan fintech, dan asuransi; serta konsultan ISO 27001 yang ingin menambahkan kampanye dan bukti ke pekerjaan mereka.",
              "Cyber and IT-risk heads at OJK-supervised firms such as banks, fintech lenders and insurers; and ISO 27001 consultancies that want to add a campaign and its evidence to their engagements."),
    "closing_h": ("Mulai dari satu kampanye.", "Start with one campaign."),
    "closing_cta": ("Ajukan Baseline", "Request a Baseline"),
}

# ---------------------------------------------------------------- 3. Mobile
PAGES["mobile"] = {
    "meta_title": ("Penilaian Keamanan Aplikasi Mobile | obscur4", "Mobile App Security Assessment | obscur4"),
    "hero_h": ("Penilaian keamanan aplikasi mobile dengan ==bukti== yang sulit dibantah vendor Anda.",
               "Mobile app security assessment with ==evidence== your vendor can't argue with."),
    "hero_sub": ("Ketahui apa yang sebenarnya dilakukan lapisan proteksi aplikasi Anda. Setiap temuan disertai artefak dan langkah reproduksinya.",
                 "Find out what your app's protection layer is actually doing. Each finding ships with its artifact and the steps to reproduce it."),
    "cta1": ("Ajukan penilaian", "Request an assessment"),
    "cta2": ("Lihat metodologi", "See the methodology"),
    "problem_h": ("Lapisan proteksi bisa gagal tanpa menjelaskan sebabnya", "A protection layer can fail without saying why"),
    "problem_b": ("Saat build yang diproteksi crash, menolak berjalan, atau berperilaku berbeda antarplatform, penyebabnya bisa aplikasi, lapisan proteksi, atau lingkungan uji. Tanpa pemisahan, temuan tidak dapat dialamatkan kepada pihak mana pun.",
                  "When a protected build crashes, refuses to launch or behaves differently across platforms, the cause may be the app, the protection layer or the test environment. Without separating them, a finding cannot be assigned to anyone."),
    "what_h": ("Apa yang kami lakukan", "What we do"),
    "what": [
        (("Verifikasi statis", "Static verification"),
         ("Tanda tangan kode, segel, dan pemeriksaan tingkat halaman; kesesuaian entitlement dengan provisioning profile; cacat pengemasan; serta diff tingkat seksi yang membedakan build yang ditandatangani ulang dari yang dikompilasi ulang.",
          "Code signature, seal and page-level checks; entitlement and provisioning-profile conformance; packaging defects; and a section-level diff that tells a re-signed build from a recompiled one.")),
        (("Uji runtime", "Runtime testing"),
         ("Pemasangan dan peluncuran pada perangkat uji terisolasi dalam kondisi jailbroken/rooted dan stock, dengan umur proses, kode keluar, dan backtrace tercatat.",
          "Install and launch on isolated test devices in jailbroken/rooted and stock states, with process lifetime, exit code and backtrace recorded.")),
        (("Atribusi", "Attribution"),
         ("Artefak dari alat uji dihilangkan agar aplikasi, lapisan proteksi, dan lingkungan uji terpisah sebelum klaim apa pun dibuat.",
          "Harness artifacts are eliminated so that app, protection layer and test environment are separated before any claim is made.")),
        (("Perbandingan terkontrol", "Controlled comparison"),
         ("Tabel perbandingan terkontrol, termasuk iOS dengan Android untuk produk yang sama.",
          "Controlled comparison tables, including iOS against Android for the same product.")),
        (("Bukti minimal", "Minimal proof"),
         ("Bila penyebab teridentifikasi, perubahan statis minimal menunjukkan bahwa penyebab itu perlu sekaligus cukup.",
          "Where a cause is identified, a minimal static change shows it is both necessary and sufficient.")),
    ],
    "how_h": ("Cara kerjanya", "How it works"),
    "how_steps": [
        ("Otorisasi dan ruang lingkup", "Authorize and scope"),
        ("Verifikasi statis", "Verify statically"),
        ("Uji pada perangkat uji terisolasi", "Test on isolated test devices"),
        ("Atribusi dan laporan", "Attribute and report"),
    ],
    "how_alt": ("Empat langkah: otorisasi dan ruang lingkup, verifikasi statis, uji pada perangkat uji terisolasi, serta atribusi dan laporan.",
                "Four steps: authorize and scope, verify statically, test on isolated test devices, then attribute and report."),
    "get_h": ("Yang Anda terima", "What you get"),
    "get": [
        ("Artefak tersimpan dengan hash.", "Stored artifacts with hashes."),
        ("Log, keluaran konsol, dan tangkapan layar.", "Logs, console output and screenshots."),
        ("Tabel perbandingan terkontrol.", "Controlled comparison tables."),
        ("Jalur reproduksi untuk setiap temuan.", "A reproduction path for each finding."),
        ("Laporan tersanitasi untuk tindak lanjut dengan vendor.", "A sanitized report for vendor follow-up."),
    ],
    "formats": [
        (("Penilaian", "Assessment"), ("Satu aplikasi, satu build.", "One app, one build.")),
        (("Regresi", "Regression"), ("Build berikutnya dibandingkan dengan sebelumnya.", "The next build compared with the last.")),
    ],
    "formats_note": ("Penawaran disusun per kebutuhan.", "Quoted per engagement."),
    "who_h": ("Untuk siapa", "Who it is for"),
    "who_b": ("Kepala keamanan aplikasi yang membutuhkan posisi yang dapat dipertanggungjawabkan dan kesiapan audit; pimpinan teknik yang perlu merilis tanpa terhambat keamanan; penyedia lapisan proteksi aplikasi yang memerlukan verifikasi independen atas kualitas integrasinya.",
              "Heads of application security who need a defensible position and audit readiness; engineering leads who must ship without security becoming the blocker; app-protection providers that need independent verification of their integration quality."),
    "trust_h": ("Otorisasi dan keamanan pengujian", "Authorization and test safety"),
    "trust_b": ("Pengujian dimulai setelah otorisasi tertulis. Teknik yang bersifat intrusif memerlukan otorisasi tercatat dan dibatasi waktu. Lingkungan uji sekali pakai dan tidak menyentuh produksi.",
                "Testing starts after written authorization. Intrusive techniques need recorded authorization and are time-boxed. Test environments are disposable and do not touch production."),
    "closing_h": ("Kirim detail aplikasi Anda.", "Tell us about your app."),
    "closing_cta": ("Ajukan penilaian", "Request an assessment"),
}

# ---------------------------------------------------------------- 4. How We Work
PAGES["how"] = {
    "meta_title": ("Cara Kerja Kami | obscur4", "How We Work | obscur4"),
    "hero_h": ("Cara kerja kami: ==otorisasi lebih dulu==, ==bukti== untuk setiap temuan.",
               "How we work: ==authorization first==, ==evidence== for every finding."),
    "hero_sub": ("Apa yang kami syaratkan sebelum mulai, apa yang kami simpan, dan bagaimana kami menangani data Anda. Kedua layanan mengikuti aturan yang sama.",
                 "What we require before we start, what we keep, and how we handle your data. Both services follow the same rules."),
    "sections": [
        ("authorization", ("Otorisasi", "Authorization"), [
            ("Catatan otorisasi tertulis memuat ruang lingkup, sasaran, waktu, dan pemberi persetujuan.",
             "A written authorization record states scope, targets, timing and approver."),
            ("Setiap tindakan dapat ditelusuri ke pelaku dan rujukan otorisasi.",
             "Every action is attributable to an actor and an authorization reference."),
            ("Kami memulai dengan pendekatan pasif dan baca-saja; teknik intrusif hanya dengan otorisasi tercatat dan dibatasi waktu.",
             "We begin passive and read-only; intrusive techniques need recorded authorization and are time-boxed."),
            ("Kami hanya menguji sistem dan aplikasi yang Anda miliki atau berwenang untuk diuji.",
             "We test only systems and apps you own or are authorized to test."),
        ]),
        ("evidence", ("Bukti", "Evidence"), [
            ("Tidak ada temuan tanpa artefak.", "No finding without an artifact."),
            ("Setiap temuan dapat direproduksi dari artefak dan urutan perintah yang tercatat.",
             "Each finding can be reproduced from its artifacts and a recorded command sequence."),
            ("Artefak disimpan dengan hash.", "Artifacts are stored with hashes."),
            ("Laporan dihasilkan platform, lalu ditandatangani seorang penanggung jawab.",
             "Reports are generated by the platform, then signed off by a named person."),
            ("Atribusi dilakukan sebelum klaim dibuat.", "Attribution comes before any claim."),
        ]),
        ("data-handling", ("Sanitasi dan penanganan data", "Sanitization and data handling"), [
            ("Lingkungan uji sekali pakai dan tersegmentasi jaringan; pembongkaran diverifikasi.",
             "Test environments are disposable and network-segmented; teardown is verified."),
            ("Kredensial dipisahkan per klien dan tidak ada jalur lintas klien. Rahasia tidak pernah masuk laporan atau log.",
             "Credentials are separate per client and there is no cross-client path. Secrets never enter reports or logs."),
            ("Artefak klien dibatasi pada ruang kerja klien; ekspor disamarkan, dan identitas dihapus dari apa pun yang dibagikan ke vendor.",
             "Client artifacts stay in the client's workspace; exports are redacted, and identifiers are removed from anything shared with a vendor."),
            ("Pada simulasi phishing, nilai yang diketik staf tidak pernah dikirim ataupun disimpan; yang tercatat hanya bahwa pengiriman terjadi.",
             "In phishing simulations, values staff type are never transmitted or stored; only the fact that a submission happened is recorded."),
            ("Hasil dilaporkan per kelompok; hasil per orang hanya terlihat oleh administrator yang ditunjuk klien.",
             "Results are reported by group; person-level results are visible only to administrators the client designates."),
            ("Data pekerjaan disimpan selama jangka waktu yang ditetapkan dalam kontrak klien, lalu dihapus.",
             "Engagement data is kept for the term set in the client contract, then deleted."),
        ]),
    ],
    "layers_h": ("Satu platform, tujuh lapisan", "One platform, seven layers"),
    "layers_intro": ("Setiap pekerjaan melewati lapisan yang sama, dari permintaan sampai laporan. Setiap tindakan melewati lapisan otorisasi.",
                     "Every engagement passes through the same layers, from request to report. Every action passes through the authorization layer."),
    "layers": [
        ("Antarmuka pekerjaan", "Engagement interface"),
        ("Kendali otorisasi dan ruang lingkup", "Authorization and scope control"),
        ("Inti orkestrasi", "Orchestration core"),
        ("Harness eksekusi", "Execution harnesses"),
        ("Perangkat penilaian", "Assessment tooling"),
        ("Lingkungan uji terisolasi", "Isolated test environments"),
        ("Bukti, analisis, dan pelaporan", "Evidence, analysis and reporting"),
    ],
    "cross": ("Di setiap lapisan: isolasi identitas dan rahasia, kendali batas data, keterlacakan, dan default yang aman.",
              "At every layer: identity and secret isolation, data-boundary control, auditability and safe defaults."),
    "not_h": ("Yang tidak kami lakukan", "What we do not do"),
    "not": [
        ("Pemindaian otomatis tanpa pengawasan terhadap sasaran internet sembarang.", "Unattended scanning of arbitrary internet targets."),
        ("Jasa eksploitasi terhadap sistem yang bukan milik Anda.", "Exploitation services against systems you do not own."),
        ("Pekerjaan yang dipilih semata berdasarkan harga terendah per pemindaian.", "Work chosen purely on lowest price per scan."),
    ],
    "band_h": ("Ingin penjelasan teknis?", "Want the technical detail?"),
    "band_cta": ("Minta sesi briefing teknis", "Request a technical briefing"),
}

# ---------------------------------------------------------------- 5. Partners
PAGES["partners"] = {
    "meta_title": ("Kemitraan | obscur4", "Partners | obscur4"),
    "hero_h": ("Bermitra dengan kami untuk menghadirkan program kesadaran keamanan bagi klien Anda.",
               "Partner with us to bring awareness programmes to your clients."),
    "hero_sub": ("Kami bekerja sama dengan konsultan ISO 27001, reseller TI, dan kantor audit, masing-masing dengan model yang berbeda.",
                 "We work with ISO 27001 consultancies, IT resellers and audit firms. Each has a different model."),
    "why_h": ("Mengapa bermitra", "Why partner"),
    "why_b": ("Konsultan ISO 27001 sudah menyediakan pelatihan kesadaran. Baseline menambahkan kampanye phishing berlokal dan laporan bukti ke pekerjaan yang sudah Anda jalankan.",
              "ISO 27001 consultancies already deliver awareness training. Baseline adds a localized phishing campaign and an evidence report to work you already do."),
    "models_h": ("Model kemitraan", "Partner models"),
    "models": [
        (("Konsultan ISO 27001", "ISO 27001 consultancies"),
         ("Mulai dengan rujukan; Baseline sebagai tambahan atas pekerjaan Anda. Seiring bertambahnya volume, kita dapat membahas pengiriman layanan atas nama Anda melalui platform kami.",
          "Start with referral, with Baseline as an add-on to your engagements. As volume grows, we can discuss delivery under your name through our platform.")),
        (("Reseller TI dan distributor bernilai tambah", "IT resellers and value-added distributors"),
         ("Jual layanan kesadaran sebagai bagian dari portofolio keamanan Anda.",
          "Resell the awareness service as part of your security portfolio.")),
        (("Kantor audit", "Audit firms"),
         ("Hanya rujukan, agar independensi audit tidak terpengaruh.",
          "Referral only, so audit independence is not affected.")),
    ],
    "terms": ("Ketentuan komersial disepakati secara individual.", "Commercial terms are agreed individually."),
    "cta": ("Diskusikan kemitraan", "Discuss a partnership"),
}

# ---------------------------------------------------------------- 6. About
PAGES["about"] = {
    "meta_title": ("Tentang obscur4", "About obscur4"),
    "hero_h": ("Layanan keamanan untuk organisasi di Indonesia, dijalankan di ==satu platform==.",
               "Security services for Indonesian organizations, run on ==one platform==."),
    "hero_sub": ("obscur4 menyediakan layanan kesadaran keamanan dan penilaian aplikasi mobile, dijalankan lewat satu platform agar setiap pekerjaan menghasilkan bukti yang seragam.",
                 "obscur4 provides security awareness and mobile app assessment, delivered through one platform so that every engagement produces the same kind of evidence."),
    "operate_h": ("Cara kami beroperasi", "How we operate"),
    "operate": [
        ("Permintaan, ruang lingkup, dan otorisasi dicatat di platform.", "Intake, scope and authorization are recorded in the platform."),
        ("Pelaksanaan berjalan dari platform.", "Execution runs from it."),
        ("Laporan dan bukti dihasilkan platform; tangan manusia hanya untuk tanda tangan akhir.",
         "Reports and evidence are generated by it; human work is limited to final sign-off."),
        ("Setiap pekerjaan menambah templat atau runbook yang dapat dipakai ulang.", "Each engagement adds a reusable template or runbook."),
    ],
    "lang_h": ("Mengapa Bahasa Indonesia lebih dulu", "Why Bahasa Indonesia matters"),
    "lang_b": ("Bahasa Indonesia adalah bahasa pengadaan dan bahasa orang-orang yang kami uji. Karena itu situs ini berbahasa Indonesia secara bawaan, dengan versi Inggris tersedia.",
               "Bahasa Indonesia is the language of the people we test. Every lure and training module is written in it, for Indonesian workplaces."),
    "material_h": ("Materi yang kami terbitkan", "Published material"),
    "material_b": ("Kami hanya menerbitkan materi kasus dengan izin tertulis klien dan dalam bentuk tersanitasi.",
                   "We publish case material only with the client's written permission and in sanitized form."),
    "company_h": ("", ""),
    "company_b": ("", ""),
    "cta": ("Hubungi kami", "Contact us"),
}

# ---------------------------------------------------------------- 7. Contact
PAGES["contact"] = {
    "meta_title": ("Kontak & Permintaan | obscur4", "Contact & Requests | obscur4"),
    "hero_h": ("Ajukan Baseline, penilaian, atau sesi briefing.", "Request a Baseline, an assessment or a briefing."),
    "hero_sub": ("Ceritakan kebutuhan Anda. Kami membalas ke alamat email yang Anda berikan.",
                 "Tell us what you need. We reply to the email address you provide."),
    "form_h": ("Formulir permintaan", "Request form"),
    "alt": ("Atau tulis langsung ke {{CONTACT_EMAIL}}.", "Or write directly to {{CONTACT_EMAIL}}."),
    "submit": ("Kirim permintaan", "Send request"),
    "required_note": ("Kolom bertanda * wajib diisi.", "Fields marked * are required."),
    "topics": [
        ("awareness", ("Kesadaran & phishing", "Awareness & phishing")),
        ("mobile", ("Penilaian aplikasi mobile", "Mobile assessment")),
        ("partner", ("Kemitraan", "Partnership")),
        ("briefing", ("Briefing teknis", "Technical briefing")),
        ("other", ("Lainnya", "Other")),
    ],
    "org_types": [
        ("bank", ("Bank", "Bank")),
        ("fintech", ("Perusahaan pendanaan fintech", "Fintech lender")),
        ("insurer", ("Asuransi", "Insurer")),
        ("payment", ("Penyedia pembayaran", "Payment provider")),
        ("consultancy", ("Konsultan atau reseller", "Consultancy or reseller")),
        ("other", ("Lainnya", "Other")),
    ],
    "platforms": [
        ("ios", ("iOS", "iOS")), ("android", ("Android", "Android")),
        ("both", ("Keduanya", "Both")), ("unsure", ("Belum pasti", "Not sure")),
    ],
    "labels": {
        "topic": ("Topik", "Topic"), "name": ("Nama lengkap", "Full name"), "email": ("Email", "Email"),
        "organization": ("Organisasi", "Organization"), "role": ("Jabatan", "Role"),
        "org_type": ("Jenis organisasi", "Organization type"), "phone": ("Telepon", "Phone"),
        "platform": ("Platform aplikasi", "App platform"), "message": ("Pesan", "Message"),
        "reply_language": ("Bahasa balasan", "Reply language"),
    },
    "choose": ("Pilih", "Choose"),
    "reply_opts": (("Bahasa Indonesia", "Bahasa Indonesia"), ("English", "English")),
    "helper": ("Mohon tidak mencantumkan kata sandi, kunci, build aplikasi, atau data pribadi orang lain. Pertukaran berkas yang aman kami atur setelah otorisasi.",
               "Please do not include passwords, keys, app builds or other people's personal data. We arrange secure file exchange after authorization."),
    "consent": ("Saya menyetujui obscur4 memproses data pribadi yang saya isikan pada formulir ini (nama, email, organisasi, jabatan, nomor telepon, dan pesan) untuk menanggapi permintaan saya, sebagaimana diuraikan dalam [Pemberitahuan Privasi]. Saya memahami bahwa saya dapat menarik persetujuan ini kapan saja dengan menghubungi {{CONTACT_EMAIL}}.",
                "I consent to obscur4 processing the personal data I enter in this form (name, email, organization, role, phone and message) in order to respond to my request, as described in the [Privacy Notice]. I understand I can withdraw this consent at any time by contacting {{CONTACT_EMAIL}}."),
    "success": ("Terima kasih. Permintaan Anda sudah kami terima dan akan kami balas ke alamat email yang Anda berikan.",
                "Thank you. We have received your request and will reply to the email address you provided."),
    "err_required": ("Kolom ini wajib diisi.", "This field is required."),
    "err_email": ("Masukkan alamat email yang valid.", "Enter a valid email address."),
    "err_consent": ("Centang persetujuan agar kami dapat memproses permintaan Anda.", "Tick the consent box so that we can process your request."),
    "err_server": ("Permintaan Anda belum terkirim. Silakan coba lagi nanti, atau tulis ke {{CONTACT_EMAIL}}.",
                   "Your request was not sent. Please try again later, or write to {{CONTACT_EMAIL}}."),
    # Added at build (not in WEBSITE-SPEC): length/format hints for fields that have rules but no error copy.
    "err_format": ("Periksa kembali isian ini.", "Check this field."),
    "err_message_len": ("Pesan minimal 20 dan maksimal 2.000 karakter.", "The message must be 20 to 2,000 characters."),
    "err_phone": ("Masukkan 8 sampai 15 digit; boleh memakai +, spasi, atau tanda hubung.", "Enter 8 to 15 digits; +, spaces and hyphens are allowed."),
    "back_home": ("Kembali ke beranda", "Back to home"),
}

# ---------------------------------------------------------------- 8. Privacy
PAGES["privacy"] = {
    "meta_title": ("Pemberitahuan Privasi | obscur4", "Privacy Notice | obscur4"),
    "hero_h": ("Pemberitahuan Privasi", "Privacy Notice"),
    "banner": ("DRAF - MEMERLUKAN TINJAUAN HUKUM SEBELUM PUBLIKASI.", "DRAFT - REQUIRES LEGAL REVIEW BEFORE PUBLICATION."),
    "effective": ("Tanggal berlaku: 8 Oktober 2026", "Effective date: 8 October 2026"),
    "sections": [
        (("Ruang lingkup", "Scope"),
         ("Pemberitahuan ini berlaku untuk situs ini dan formulir permintaannya. Data dalam pekerjaan klien (misalnya data staf klien dalam program kesadaran, atau artefak aplikasi) diatur oleh kontrak pekerjaan, bukan pemberitahuan ini.",
          "This notice covers this website and its request form. Data in client engagements (for example client staff data in an awareness programme, or app artifacts) is governed by the engagement contract, not this notice.")),
        (("Pihak yang bertanggung jawab", "Who is responsible"),
         ("Pengendali data: obscur4. Kontak: {{CONTACT_EMAIL}}.",
          "Data controller: obscur4. Contact: {{CONTACT_EMAIL}}.")),
        (("Data yang kami kumpulkan", "Data we collect"),
         ("Data pada formulir: nama, email, organisasi, jabatan, jenis organisasi, telepon, platform aplikasi, bahasa balasan, dan pesan. Data teknis: penyedia hosting kami menyimpan log server standar, seperti alamat IP dan waktu akses, untuk keamanan dan keandalan. Cookie dan analitik: situs ini tidak memakai cookie pelacakan; statistik kunjungan dihitung secara agregat tanpa cookie.",
          "Form data: name, email, organization, role, organization type, phone, app platform, reply language and message. Technical data: our hosting provider keeps standard server logs, such as IP address and time of access, for security and reliability. Cookies and analytics: this site sets no tracking cookies; visit statistics are counted in aggregate without cookies.")),
        (("Tujuan", "Purposes"),
         ("Menanggapi permintaan, mengatur briefing atau pekerjaan, mencatat permintaan, dan melindungi situs dari penyalahgunaan.",
          "To respond to requests, arrange briefings or engagements, keep a record of the request, and protect the site from abuse.")),
        (("Dasar pemrosesan", "Legal basis"),
         ("Persetujuan Anda pada formulir, dan kepentingan sah kami untuk melindungi situs dari penyalahgunaan.",
          "Your consent on the form, and our legitimate interest in protecting the site from abuse.")),
        (("Pembagian data", "Sharing"),
         ("Kami tidak menjual data pribadi. Data dibagikan hanya kepada penyedia layanan yang mendukung situs dan email berdasarkan kontrak: penyedia hosting dan jaringan pengiriman konten kami, serta penyedia email kami.",
          "We do not sell personal data. Data is shared only with service providers that support the site and email under contract: our hosting and content delivery provider, and our email provider.")),
        (("Lokasi dan transfer", "Location and transfers"),
         ("Situs dilayani melalui jaringan global penyedia hosting kami, sehingga data dapat diproses di luar Indonesia. Transfer tersebut dilindungi sebagaimana disyaratkan UU PDP.",
          "The site is served through our hosting provider's global network, so data may be processed outside Indonesia. Such transfers are protected as required by UU PDP.")),
        (("Retensi", "Retention"), ("Data permintaan disimpan paling lama dua belas bulan setelah kontak terakhir kami dengan Anda, lalu dihapus.",
                              "Request data is kept for at most twelve months after our last contact with you, then deleted.")),
        (("Hak Anda", "Your rights"),
         ("Berdasarkan UU PDP, Anda dapat meminta informasi tentang, akses ke, dan salinan data Anda, perbaikan atau penghapusannya, pembatasan pemrosesan, penarikan persetujuan, serta mengajukan keberatan atas keputusan yang diambil semata-mata melalui pemrosesan otomatis. Hubungi {{CONTACT_EMAIL}}.",
          "Under UU PDP you can ask for information about, access to and a copy of your data, its correction or deletion, restriction of processing, withdrawal of consent, and you can object to decisions made solely by automated processing. Contact {{CONTACT_EMAIL}}.")),
        (("Keamanan dan insiden", "Security and incidents"),
         ("Kami menerapkan langkah pengamanan yang wajar, seperti enkripsi HTTPS, pembatasan akses, dan pencatatan akses. Bila terjadi kegagalan pelindungan data pribadi, kami memberi tahu pihak terdampak dan regulator sesuai jangka waktu yang ditetapkan undang-undang.",
          "We apply reasonable safeguards such as HTTPS encryption, restricted access and access logging. If a personal data protection failure occurs, we notify affected people and the regulator within the period the law sets.")),
        (("Anak-anak", "Children"), ("Situs ini tidak ditujukan bagi anak-anak.", "This site is not directed at children.")),
        (("Perubahan", "Changes"), ("Perubahan diumumkan di halaman ini dengan tanggal berlaku yang baru.", "Changes are posted on this page with a new effective date.")),
    ],
}

# ---------------------------------------------------------------- system pages
PAGES["sent"] = {
    "meta_title": ("Permintaan terkirim | obscur4", "Request sent | obscur4"),
}
# ---------------------------------------------------------------- illustrations and microcopy
# Example phishing-simulation message shown as an annotated artifact. The lure itself is always Indonesian.
LURE = {
    "label": ("Example simulation lure", "Example simulation lure"),
    "from_name": "Layanan Pengiriman",
    "from_addr": "notifikasi@kirim-paket.example",
    "subject": "Paket Anda tertahan di gudang",
    "body": "Alamat pengiriman tidak lengkap. Konfirmasi alamat hari ini agar paket tidak dikembalikan ke pengirim.",
    "button": "Konfirmasi alamat",
    "link": "lacak-paket.example/konfirmasi",
    "cues": [
        ("Sender name does not match the domain", "Sender name does not match the domain"),
        ("Time pressure", "Time pressure"),
        ("Link points to a different domain", "Link points to a different domain"),
    ],
    "caption": ("Our simulations use messages common in Indonesian workplaces. Staff learn to spot the signs.",
                "Our simulations use messages common in Indonesian workplaces. Staff learn to spot the signs."),
    "to": "Kepada: staf@organisasi-anda.example",
}

# Schematic illustration of the controlled-comparison method (mobile page).
COMPARE = {
    "title": ("One variable, one cause", "One variable, one cause"),
    "label": ("Method illustration, not a client result", "Method illustration, not a client result"),
    "cols": [("Build", "Build"), ("Device state", "Device state"),
             ("Protection layer", "Protection layer"), ("Outcome", "Outcome")],
    "rows": [
        [("Reference build", "Reference build"), ("stock", "stock"), ("none", "none"), ("runs normally", "runs normally")],
        [("Wrapped build", "Wrapped build"), ("stock", "stock"), ("on", "on"), ("exits at launch", "exits at launch")],
    ],
    "verdict": ("Only the protection layer differs, so the cause is attributed to it, then proven with a minimal change.",
                "Only the protection layer differs, so the cause is attributed to it, then proven with a minimal change."),
}

# Example evidence-bundle file tree (mobile page). File names stay as-is.
BUNDLE = {
    "label": ("Example evidence bundle structure", "Example evidence bundle structure"),
    "items": [
        ("artifacts/", ("original builds, never modified", "original builds, never modified")),
        ("hashes.txt", ("a hash for every artifact", "a hash for every artifact")),
        ("logs/", ("launch logs per device state", "launch logs per device state")),
        ("captures/", ("console output and screenshots", "console output and screenshots")),
        ("comparison.md", ("controlled comparison tables", "controlled comparison tables")),
        ("reproduce.sh", ("command sequence to reproduce", "command sequence to reproduce")),
        ("report.pdf", ("sanitized report for vendor follow-up", "sanitized report for vendor follow-up")),
    ],
}

# Microcopy for the animated How We Work layer stack.
FLOW = {
    "token": ("action", "action"),
    "stamp": ("authorized", "authorized"),
    "result": ("recorded as an artifact", "recorded as an artifact"),
}

# Microcopy for the animated awareness programme path.
PATH = {
    "report": ("Report by group", "Report by group"),
}

NOT_FOUND = {
    "title": ("Halaman tidak ditemukan.", "Page not found."),
}
