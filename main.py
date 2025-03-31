import flet as ft
from pillow_heif import register_heif_opener
from PIL import Image
import os
import asyncio

# Registrar suporte a HEIC no Pillow
register_heif_opener()

def converter_heic_para_png(input_path, output_folder):
    try:
        img = Image.open(input_path)  # Agora o Pillow já suporta HEIC!
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(input_path))[0] + ".png")
        img.save(output_path, "PNG")
        return output_path
    except Exception as e:
        return f"Erro ao converter {input_path}: {e}"

async def processar_imagens(page, files, progress_bar, status_text, progress_text):
    output_folder = os.path.join(os.getcwd(), "imagens_convertidas")
    os.makedirs(output_folder, exist_ok=True)

    total = len(files)
    progress_bar.value = 0  # Resetar a barra de progresso
    progress_text.value = "0% concluído"
    progress_bar.update()
    progress_text.update()
    page.update()
    
    for i, file in enumerate(files):
        status_text.value = f"Convertendo: {file.name}..."
        page.update()
        
        output_path = converter_heic_para_png(file.path, output_folder)
        print(f"Convertido: {output_path}")
        
        # Atualizar a barra de progresso e o texto
        progress_bar.value = (i + 1) / total
        progress_text.value = f"{int((i + 1) / total * 100)}% concluído"
        progress_bar.update()
        progress_text.update()
        page.update()
        
        # Permitir que a interface seja atualizada
        await asyncio.sleep(0.1)
    
    # Finalizar a barra de progresso
    status_text.value = "Conversão concluída!"
    progress_bar.value = 1
    progress_text.value = "100% concluído"
    progress_bar.update()
    progress_text.update()
    page.update()

    # Abrir a pasta automaticamente após a conclusão
    os.startfile(output_folder)

def main(page: ft.Page):
    page.title = "Conversor HEIC para PNG"
    page.window_width = 500
    page.window_height = 400
    


    file_picker = ft.FilePicker()
    progress_bar = ft.ProgressBar(width=400)
    progress_bar.value = 0
    progress_bar.visible = False
    progress_text = ft.Text("0% concluído", size=14, color="gray")
    progress_text.visible = False
    progress_text.visible = False
    status_text = ft.Text("Selecione imagens HEIC para converter", size=16)

    async def selecionar_arquivos(e: ft.FilePickerResultEvent):
        if e.files:
            progress_bar.visible = True
            progress_text.visible = True
            progress_bar.value = 0  # Resetar a barra antes de cada nova conversão
            progress_text.value = "0% concluído"
            progress_bar.update()
            progress_text.update()
            status_text.value = "Iniciando conversão..."
            page.update()
            await processar_imagens(page, e.files, progress_bar, status_text, progress_text)
    
    file_picker.on_result = selecionar_arquivos
    
    btn_escolher = ft.ElevatedButton("Escolher imagens", on_click=lambda _: file_picker.pick_files(allow_multiple=True))


    
    page.add(btn_escolher, progress_bar, progress_text, status_text, file_picker)
    
ft.app(target=main)
