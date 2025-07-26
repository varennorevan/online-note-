# Aplikasi Catatan Sederhana dengan Gradio
# Notebook ini membuat interface web untuk menyimpan dan mengelola catatan

# Install dependencies (jalankan cell ini terlebih dahulu)
!pip install gradio

import gradio as gr
import json
import os
from datetime import datetime

# File untuk menyimpan catatan
NOTES_FILE = "catatan.json"

def load_notes():
    """Memuat catatan dari file JSON"""
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_notes(notes):
    """Menyimpan catatan ke file JSON"""
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def add_note(judul, konten):
    """Menambah catatan baru"""
    if not judul.strip() or not konten.strip():
        return "❌ Judul dan konten tidak boleh kosong!", get_notes_display()
    
    notes = load_notes()
    new_note = {
        "id": len(notes) + 1,
        "judul": judul.strip(),
        "konten": konten.strip(),
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(new_note)
    save_notes(notes)
    
    return "✅ Catatan berhasil disimpan!", get_notes_display()

def delete_note(note_id):
    """Menghapus catatan berdasarkan ID"""
    try:
        note_id = int(note_id)
        notes = load_notes()
        notes = [note for note in notes if note["id"] != note_id]
        
        # Update ID untuk konsistensi
        for i, note in enumerate(notes):
            note["id"] = i + 1
            
        save_notes(notes)
        return "✅ Catatan berhasil dihapus!", get_notes_display()
    except:
        return "❌ ID tidak valid!", get_notes_display()

def get_notes_display():
    """Mendapatkan tampilan semua catatan"""
    notes = load_notes()
    if not notes:
        return "📝 Belum ada catatan. Silakan tambah catatan baru!"
    
    display = "📋 **DAFTAR CATATAN**\n\n"
    for note in notes:
        display += f"**ID: {note['id']} | {note['judul']}**\n"
        display += f"📅 {note['waktu']}\n"
        display += f"📄 {note['konten']}\n"
        display += "─" * 50 + "\n\n"
    
    return display

def search_notes(keyword):
    """Mencari catatan berdasarkan kata kunci"""
    if not keyword.strip():
        return get_notes_display()
    
    notes = load_notes()
    keyword = keyword.lower()
    filtered_notes = [
        note for note in notes 
        if keyword in note['judul'].lower() or keyword in note['konten'].lower()
    ]
    
    if not filtered_notes:
        return f"🔍 Tidak ditemukan catatan dengan kata kunci: '{keyword}'"
    
    display = f"🔍 **HASIL PENCARIAN: '{keyword}'**\n\n"
    for note in filtered_notes:
        display += f"**ID: {note['id']} | {note['judul']}**\n"
        display += f"📅 {note['waktu']}\n"
        display += f"📄 {note['konten']}\n"
        display += "─" * 50 + "\n\n"
    
    return display

def clear_all_notes():
    """Menghapus semua catatan"""
    save_notes([])
    return "🗑️ Semua catatan berhasil dihapus!", "📝 Belum ada catatan. Silakan tambah catatan baru!"

# Membuat interface Gradio
with gr.Blocks(title="📝 Aplikasi Catatan", theme=gr.themes.Soft()) as app:
    gr.HTML("<h1 style='text-align: center; color: #2E8B57;'>📝 Aplikasi Catatan Pribadi</h1>")
    gr.HTML("<p style='text-align: center; color: #666;'>Simpan dan kelola catatan Anda dengan mudah</p>")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML("<h3>➕ Tambah Catatan Baru</h3>")
            judul_input = gr.Textbox(
                label="📌 Judul Catatan",
                placeholder="Masukkan judul catatan...",
                lines=1
            )
            konten_input = gr.Textbox(
                label="📝 Isi Catatan",
                placeholder="Tulis catatan Anda di sini...",
                lines=5
            )
            
            with gr.Row():
                add_btn = gr.Button("💾 Simpan Catatan", variant="primary")
                clear_form_btn = gr.Button("🔄 Reset Form")
            
            status_msg = gr.Textbox(
                label="📊 Status",
                interactive=False,
                lines=1
            )
            
            gr.HTML("<h3>🔧 Kelola Catatan</h3>")
            
            with gr.Row():
                search_input = gr.Textbox(
                    label="🔍 Cari Catatan",
                    placeholder="Masukkan kata kunci...",
                    lines=1
                )
                search_btn = gr.Button("🔍 Cari")
            
            with gr.Row():
                delete_input = gr.Textbox(
                    label="🗑️ Hapus Catatan (ID)",
                    placeholder="Masukkan ID catatan...",
                    lines=1
                )
                delete_btn = gr.Button("🗑️ Hapus", variant="secondary")
            
            clear_all_btn = gr.Button("🗑️ Hapus Semua Catatan", variant="stop")
        
        with gr.Column(scale=2):
            gr.HTML("<h3>📋 Daftar Catatan</h3>")
            notes_display = gr.Textbox(
                label="",
                value=get_notes_display(),
                lines=20,
                interactive=False,
                show_label=False
            )
            refresh_btn = gr.Button("🔄 Refresh")
    
    # Event handlers
    add_btn.click(
        fn=add_note,
        inputs=[judul_input, konten_input],
        outputs=[status_msg, notes_display]
    ).then(
        fn=lambda: ("", ""),  # Clear form
        outputs=[judul_input, konten_input]
    )
    
    clear_form_btn.click(
        fn=lambda: ("", "", ""),
        outputs=[judul_input, konten_input, status_msg]
    )
    
    delete_btn.click(
        fn=delete_note,
        inputs=[delete_input],
        outputs=[status_msg, notes_display]
    ).then(
        fn=lambda: "",  # Clear delete input
        outputs=[delete_input]
    )
    
    search_btn.click(
        fn=search_notes,
        inputs=[search_input],
        outputs=[notes_display]
    )
    
    clear_all_btn.click(
        fn=clear_all_notes,
        outputs=[status_msg, notes_display]
    )
    
    refresh_btn.click(
        fn=get_notes_display,
        outputs=[notes_display]
    )
    
    # Auto-refresh saat startup
    app.load(
        fn=get_notes_display,
        outputs=[notes_display]
    )

# Jalankan aplikasi
if __name__ == "__main__":
    print("🚀 Memulai Aplikasi Catatan...")
    print("📝 Interface akan tersedia setelah loading selesai")
    app.launch(
        share=True,  # Membuat link publik
        debug=True,
        server_name="0.0.0.0",
        server_port=7860
    )