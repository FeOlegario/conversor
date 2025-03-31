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
    page.bgcolor = '#9C6675'
    page.window.width = 500
    page.window.height = 460
    page.window.resizable = False
    page.window.maximizable = False
    page.window.center()
    
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Conversor HEIC para PNG", size=24, weight="bold", color="#F1D7C5"),
            ],
            alignment="center",
            horizontal_alignment="center",
        ),
        width=500,
        height=400,
    )

    file_picker = ft.FilePicker()
    progress_bar = ft.ProgressBar(width=400,color='#CA7077',bgcolor='#F0D9C6', border_radius=10, height=20, visible=False)
    progress_text = ft.Text("0% concluído", size=14, color="#F1D7C5", visible=False)
    status_text = ft.Text("Selecione imagens HEIC para converter", size=16, color="#F1D7C5")

    estilo_bt=ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=2),
    bgcolor={
        ft.ControlState.DEFAULT: "#CA7077",
        ft.ControlState.FOCUSED: "#5caee0",
        ft.ControlState.PRESSED: "#764E5D",
    },
    color={
        ft.ControlState.DEFAULT: "#F1D7C5",
        ft.ControlState.PRESSED: ft.colors.WHITE60,
    },
    elevation={
        ft.ControlState.DEFAULT: 3,
        ft.ControlState.HOVERED: 5,
    },
    padding=15,
    text_style={
        ft.ControlState.DEFAULT: ft.TextStyle(
            size=15,
            # weight="w500"
        )
    },
    
)
    
    def clickar_botao(e):
        progress_bar.value = 0
        progress_text.value = "0% concluído"
        progress_bar.visible = True
        progress_text.visible = True
        progress_bar.update()
        progress_text.update()
        file_picker.pick_files(allow_multiple=True)
        progress_text.value = "Iniciando conversão..."
        progress_text.update()


    async def selecionar_arquivos(e: ft.FilePickerResultEvent):
        if e.files:
            progress_bar.visible = True
            progress_text.visible = True
            progress_bar.value = 0
            progress_text.value = "0% concluído"
            progress_bar.update()
            progress_text.update()
            status_text.value = "Iniciando conversão..."
            page.update()
            await processar_imagens(page, e.files, progress_bar, status_text, progress_text)
    
    file_picker.on_result = selecionar_arquivos
    
    btn_escolher = ft.ElevatedButton("Escolher imagens", 
        style=estilo_bt,
        icon="search",
        icon_color="#F1D7C5",
        width=345,
        on_click=clickar_botao
        )
    
    container.content.controls.extend([progress_bar, progress_text, status_text ,btn_escolher, file_picker])
    

    page.add(container)
    
ft.app(target=main)
