import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp

class AnalisisNilaiApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.data_siswa = []  # Menyimpan tuple: (nama, nilai)

        # Layar Utama
        screen = MDScreen()
        layout_utama = MDBoxLayout(orientation='vertical')

        # Top Bar
        toolbar = MDTopAppBar(title="Analisis Nilai Ulangan", elevation=2)
        layout_utama.add_widget(toolbar)

        scroll = MDScrollView()
        content = MDBoxLayout(
            orientation='vertical', 
            padding=dp(16), 
            spacing=dp(12), 
            adaptive_height=True
        )

        # Form Parameter Ulangan
        self.input_mapel = MDTextField(hint_text="Mata Pelajaran (contoh: Matematika)")
        self.input_kkm = MDTextField(hint_text="Batas KKM (contoh: 75)", input_filter='float')
        content.add_widget(self.input_mapel)
        content.add_widget(self.input_kkm)

        # Form Input Siswa
        form_siswa = MDBoxLayout(orientation='horizontal', spacing=dp(8), adaptive_height=True)
        self.input_nama = MDTextField(hint_text="Nama Siswa", size_hint_x=0.6)
        self.input_nilai = MDTextField(hint_text="Nilai", input_filter='float', size_hint_x=0.3)
        btn_tambah = MDIconButton(
            icon="plus-circle", 
            theme_icon_color="Custom", 
            icon_color=self.theme_cls.primary_color,
            on_release=self.tambah_siswa
        )
        form_siswa.add_widget(self.input_nama)
        form_siswa.add_widget(self.input_nilai)
        form_siswa.add_widget(btn_tambah)
        content.add_widget(form_siswa)

        # Tombol Aksi
        btn_box = MDBoxLayout(spacing=dp(8), adaptive_height=True)
        btn_analisis = MDRaisedButton(text="Analisis Data", on_release=self.proses_analisis)
        btn_reset = MDRaisedButton(text="Reset", md_bg_color=(0.8, 0.2, 0.2, 1), on_release=self.reset_data)
        btn_box.add_widget(btn_analisis)
        btn_box.add_widget(btn_reset)
        content.add_widget(btn_box)

        # Area Ringkasan Hasil Analisis
        self.lbl_ringkasan = MDLabel(
            text="Silakan masukkan data siswa dan nilai.", 
            theme_text_color="Secondary",
            adaptive_height=True
        )
        content.add_widget(self.lbl_ringkasan)

        # Daftar Siswa
        self.list_view = MDList()
        content.add_widget(self.list_view)

        scroll.add_widget(content)
        layout_utama.add_widget(scroll)
        screen.add_widget(layout_utama)

        return screen

    def tambah_siswa(self, *args):
        nama = self.input_nama.text.strip()
        nilai_str = self.input_nilai.text.strip()

        if not nama or not nilai_str:
            self.show_alert("Error", "Nama dan Nilai harus diisi.")
            return

        try:
            nilai = float(nilai_str)
            self.data_siswa.append((nama, nilai))
            self.update_list()
            self.input_nama.text = ""
            self.input_nilai.text = ""
        except ValueError:
            self.show_alert("Error", "Format nilai tidak valid.")

    def update_list(self):
        self.list_view.clear_widgets()
        for idx, (nama, nilai) in enumerate(self.data_siswa, start=1):
            item = TwoLineListItem(
                text=f"{idx}. {nama}",
                secondary_text=f"Nilai: {nilai}"
            )
            self.list_view.add_widget(item)

    def proses_analisis(self, *args):
        if not self.data_siswa:
            self.show_alert("Peringatan", "Belum ada data siswa yang diinput.")
            return

        try:
            kkm = float(self.input_kkm.text.strip()) if self.input_kkm.text.strip() else 75.0
        except ValueError:
            kkm = 75.0

        nilai_list = [nilai for _, nilai in self.data_siswa]
        total_siswa = len(nilai_list)
        rata_rata = sum(nilai_list) / total_siswa
        nilai_max = max(nilai_list)
        nilai_min = min(nilai_list)

        tuntas = [s for s in self.data_siswa if s[1] >= kkm]
        remedial = [s for s in self.data_siswa if s[1] < kkm]
        persen_tuntas = (len(tuntas) / total_siswa) * 100

        ringkasan = (
            f"=== HASIL ANALISIS ===\n"
            f"• Mata Pelajaran: {self.input_mapel.text.strip() or 'Umum'}\n"
            f"• Batas KKM: {kkm}\n"
            f"• Jumlah Siswa: {total_siswa}\n"
            f"• Rata-rata: {rata_rata:.2f}\n"
            f"• Nilai Tertinggi: {nilai_max}\n"
            f"• Nilai Terendah: {nilai_min}\n"
            f"• Ketuntasan Klasikal: {persen_tuntas:.1f}%\n"
            f"• Tuntas: {len(tuntas)} siswa | Remedial: {len(remedial)} siswa"
        )
        self.lbl_ringkasan.text = ringkasan

    def reset_data(self, *args):
        self.data_siswa = []
        self.list_view.clear_widgets()
        self.lbl_ringkasan.text = "Data telah direset."

    def show_alert(self, title, message):
        dialog = MDDialog(title=title, text=message, size_hint=(0.8, None))
        dialog.open()

if __name__ == '__main__':
    AnalisisNilaiApp().run()