import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

st.set_page_config(page_title="PDF Auto Fill Dashboard", page_icon="🧾", layout="centered")

st.title("🧾 PDF Auto Fill Dashboard")
st.write("Isi data berikut untuk mengisi otomatis file PDF kamu (misal TC PF REV 14)")
st.markdown("---")

with st.form("pdf_form"):
    col1, col2 = st.columns(2)
    with col1:
        work_order = st.text_input("WORK ORDER NO.")
        ac_reg = st.text_input("A/C REG.")
        ac_msn = st.text_input("A/C MSN.")
    with col2:
        ac_eff = st.text_input("A/C Effectivity")
        operator = st.text_input("OPERATOR")
        uploaded_pdf = st.file_uploader("Upload Template PDF", type=["pdf"])
    submitted = st.form_submit_button("🚀 Generate PDF")

if submitted:
    if not uploaded_pdf:
        st.error("⚠️ Tolong upload file PDF template dulu.")
    else:
        template = PdfReader(uploaded_pdf)
        output = PdfWriter()
        for i, page in enumerate(template.pages):
            if 1 <= i < 8:
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

        st.success("✅ PDF berhasil diisi otomatis!")
        st.download_button(
            "⬇️ Download Hasil PDF",
            result,
            file_name="Output_TC_PF_REV14.pdf",
            mime="application/pdf",
        )
