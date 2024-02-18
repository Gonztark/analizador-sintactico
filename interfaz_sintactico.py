import tkinter
from tkinter import filedialog
import customtkinter
from lexico import analizar_lexico, reset_lines
from sintactico import parse 

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analizador Sintáctico")
        self.geometry("850x600")

        # Cuadro de texto para la entrada del usuario
        self.texto_entrada = customtkinter.CTkTextbox(self, width=380, height=300)
        self.texto_entrada.grid(row=0, column=0, padx=20, pady=20)
        self.texto_entrada.insert("1.0", "Introduce el código aquí o carga un archivo")
        self.texto_entrada.bind("<FocusIn>", self.on_focus_in)

        # Mostrar resultado
        self.texto_resultado = customtkinter.CTkTextbox(self, width=380, height=300, state="disabled")
        self.texto_resultado.grid(row=0, column=1, padx=20, pady=20)

        # botones
        self.boton_analizar = customtkinter.CTkButton(self, text="Analizar", command=self.analizar)
        self.boton_analizar.grid(row=1, column=1, pady=20)

        self.boton_cargar = customtkinter.CTkButton(self, text="Cargar Archivo", command=self.cargar_archivo)
        self.boton_cargar.grid(row=1, column=0, pady=20)

    def on_focus_in(self, event):
        default_text = "Introduce el código aquí o carga un archivo"
        if self.texto_entrada.get("1.0", "end-1c") == default_text:
            self.texto_entrada.delete("1.0", "end")

    def analizar(self):
        texto_usuario = self.texto_entrada.get("1.0", "end-1c")
        resultado = parse(texto_usuario)
        reset_lines()
        if not resultado.strip():
            resultado = "No hay errores de sintaxis."
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", resultado)
        self.texto_resultado.configure(state="disabled")

    def cargar_archivo(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                self.texto_entrada.configure(state="normal")
                self.texto_entrada.delete("1.0", "end")
                self.texto_entrada.insert("1.0", contenido)
                self.texto_entrada.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
