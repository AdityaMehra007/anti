import os

import win32com.client


def export_docx_to_pdf():
    career_dir = os.path.abspath(os.path.dirname(__file__))
    docx_files = [
        "ADITYA_MEHRA_MASTER_ATS_RESUME.docx",
        "ADITYA_MEHRA_SUPPLY_CHAIN_PROCUREMENT.docx",
        "ADITYA_MEHRA_AI_DATA_OPERATIONS.docx",
    ]

    print("[*] Initializing Microsoft Word COM automation...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    try:
        for docx_name in docx_files:
            docx_path = os.path.join(career_dir, docx_name)
            pdf_path = os.path.join(career_dir, docx_name.replace(".docx", ".pdf"))
            if not os.path.exists(docx_path):
                print(f"[!] Warning: {docx_path} does not exist.")
                continue

            print(f"[*] Converting: {docx_name} -> {os.path.basename(pdf_path)}")
            doc = word.Documents.Open(docx_path)
            # 17 represents wdExportFormatPDF in Word COM
            doc.SaveAs(pdf_path, FileFormat=17)
            doc.Close()
            print(f"[OK] Created: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
    finally:
        word.Quit()
        print("[*] Word Application shutdown complete.")


if __name__ == "__main__":
    export_docx_to_pdf()
