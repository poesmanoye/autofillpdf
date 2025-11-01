import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

# --- Konfigurasi halaman ---
st.set_page_config(page_title="TASKCARD AUTOFILL TKG", page_icon="logo.png", layout="centered")

st.title("🧾 TASKCARD AUTOFILL TKG")
st.write("Pilih template dan isi data untuk mengisi otomatis PDF task card.")
st.markdown("---")

# --- Lokasi file PDF yang sudah ada di repo ---
page_ranges = {
    "DI BATIK REV 08.pdf": (2, 27),
    "PF BATIK REV 02.pdf": (2, 8),
    "WK BATIK REV 10.pdf": (2, 16),
    "TC DAILY REV 39.pdf": (4, 31),
    "TC PF REV 14.pdf": (2, 8),
}

# --- Dropdown pilih template ---
template_name = st.selectbox(
    "📄 Pilih Template PDF",
    list(page_ranges.keys()),
    index=4
)

# Ambil halaman dari dictionary
start_page, end_page = page_ranges[template_name]
start_page -= 1  # karena index mulai dari 0

# --- Form input data ---
with st.form("pdf_form"):
    st.subheader("✏️ Isi Data")
    col1, col2 = st.columns(2)
    with col1:
        work_order = st.text_input("WORK ORDER NO.")
        ac_reg = st.text_input("A/C REG.")
        ac_msn = st.text_input("A/C MSN.")
    with col2:
        ac_eff = st.text_input("A/C Effectivity")
        operator = st.text_input("OPERATOR")

    submitted = st.form_submit_button("🚀 Generate PDF")

# --- Proses PDF ---
if submitted:
    try:
        # Baca file langsung dari folder GitHub (lokal kalau di laptop)
        template = PdfReader(template_name)
        output = PdfWriter()

        for i, page in enumerate(template.pages):
            if start_page <= i < end_page:
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=A4)
                can.setFont("Helvetica", 9)
                can.drawString(69, 734, work_order)
                can.drawString(149, 734, ac_reg)
                can.drawString(206, 734, ac_msn)
                can.drawString(270, 734, ac_eff)
                can.drawString(360, 734, operator)
                can.save()
                packet.seek(0)
                overlay_pdf = PdfReader(packet)
                page.merge_page(overlay_pdf.pages[0])
            output.add_page(page)

        result = BytesIO()
        output.write(result)
        result.seek(0)

        st.success(f"✅ Berhasil isi otomatis: {template_name} (hal {start_page+1}–{end_page})")
        st.download_button(
            "⬇️ DOWNLOAD TASKCARD",
            result,
            file_name=f"FINAL_{template_name.replace('.pdf', '')}.pdf",
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.error("⚠️ File template tidak ditemukan. Pastikan PDF-nya ada di folder yang sama dengan app.py")

st.markdown("---")
st.caption("Dibuat dengan poesmanoye.teknisi ganteng lampung")
