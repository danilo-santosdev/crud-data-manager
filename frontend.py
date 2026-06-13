import customtkinter as ctk       # biblioteca para visual moderno
import tkinter as tk              # (neste caso) adaptar recursos para janela popup
import ctypes                     # acesso aos recursos do sistema operacional
import sys                        # acesso à variáveis do sistema
import os                         # acesso aos diretórios
import platform
import pathlib 

from backend import InserirDado, SelecionarLinha, SelecionarArquivo, ApagarDados, EditarDado, ExcluirDado   # importando funções externas (arquivo backend.py)

ctk.set_appearance_mode("dark")  # definindo aparência

class GerenciadorIcone:

    _icone_global = None

    @staticmethod
    def aplicar_icone(janela):

        # Detecta diretório base
        if "APPDIR" in os.environ:
            BASE_DIR = pathlib.Path(os.environ["APPDIR"])
        else:
            BASE_DIR = pathlib.Path(__file__).resolve().parent

        sistema = platform.system()

        try:

            # WINDOWS
            if sistema == "Windows":

                icone = BASE_DIR / "assets" / "list.ico"

                if icone.exists():
                    janela.iconbitmap(str(icone))

            # LINUX / MAC
            else:

                icone = BASE_DIR / "assets" / "list.png"

                if icone.exists():

                    if GerenciadorIcone._icone_global is None:

                        GerenciadorIcone._icone_global = tk.PhotoImage(
                            file=str(icone)
                        )

                    janela.iconphoto(
                        True,
                        GerenciadorIcone._icone_global
                    )

            print("Ícone carregado com sucesso!")

        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

class AlertaDados(tk.Toplevel):

    #---------------Bloco para tratar múltiplas janelas---------------
    instancia = None

    @classmethod
    def mostrar(cls, master, mensagem=""):

        if cls.instancia is not None:
            if cls.instancia.winfo_exists():

                cls.instancia.mensagem_alerta.configure(
                    text=mensagem
                )

                cls.instancia.focus_force()
                return cls.instancia

        cls.instancia = cls(master, mensagem)
        return cls.instancia
    #-----------------------------------------------------------------

    def __init__(self, master, mensagem = ""):
        super().__init__(master)

        self.title("Alerta!")
        self.attributes("-topmost", True)
        self.configure(bg="#2C2C2C")

        # Inserir ícone na barra de título:
        GerenciadorIcone.aplicar_icone(self)

        self.mensagem_alerta = ctk.CTkLabel(
            master=self,
            text=mensagem,  # variável que troca de valor (no caso, 'string') a cada situação
            text_color="#FFFFFF"
        )
        self.mensagem_alerta.pack(pady=(30, 2))

        # Ativa barra de título escura (Windows):
        if sys.platform.startswith("win"):
            self.after(10, self.ativar_dark_titlebar_alerta)

        # Configuração para bloquear interface:
        # self.transient(master)
        # self.grab_set()        * no linux esse método não funciona
        self.focus_force()

        self.protocol("WM_DELETE_WINDOW", self.fecha_popup_alerta)  # devolve domínio para janela principal

        # Configuração de tamanho-centralização:
        popup_width, popup_height = 350, 100

        tela_width = self.winfo_screenwidth()
        tela_height = self.winfo_screenheight()
        x = (tela_width // 2) - (popup_width // 2)
        y = (tela_height // 2) - (popup_height // 2)

        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        self.resizable(False, False)

        # Remove minimizar/maximizar (Windows)
        if sys.platform.startswith("win"):
            GWL_STYLE = -16
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style &= ~WS_MINIMIZEBOX
            style &= ~WS_MAXIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            ctypes.windll.user32.SetWindowPos(
                hwnd, 0, 0, 0, 0, 0,
                0x0002 | 0x0001 | 0x0040 | 0x0020
            )

    # Função para alterar barra de título:
    def ativar_dark_titlebar_alerta(self):
        self.update()
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())

        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        valor = ctypes.c_int(1)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(valor),
            ctypes.sizeof(valor)
        )

    def fecha_popup_alerta(self):
        # self.grab_release()
        AlertaDados.instancia = None
        self.destroy()

class PopupSobre(tk.Toplevel):

    #---------------Bloco para tratar múltiplas janelas---------------
    instancia = None

    @classmethod
    def mostrar(cls, master):

        if cls.instancia is not None:
            if cls.instancia.winfo_exists():
                cls.instancia.focus_force()
                return cls.instancia

        cls.instancia = cls(master)
        return cls.instancia
    #-----------------------------------------------------------------

    def __init__(self, master):
        super().__init__(master)

        # Configuração básica da janela popup:
        self.title("Sobre o app")
        self.attributes("-topmost", True)
        self.configure(bg="#2C2C2C")

        # Inserir ícone na barra de título:
        GerenciadorIcone.aplicar_icone(self)

        # Ativa barra de título escura (Windows):
        if sys.platform.startswith("win"):
            self.after(10, self.ativar_dark_titlebar)

        # Configuração para bloquear interface:
        # self.transient(master)
        # self.grab_set()        * no linux esse método não funciona
        self.focus_force()

        self.protocol("WM_DELETE_WINDOW", self.fecha_popup)  # devolve domínio para janela principal

        # Configuração de tamanho-centralização:
        popup_width, popup_height = 350, 180

        tela_width = self.winfo_screenwidth()
        tela_height = self.winfo_screenheight()
        x = (tela_width // 2) - (popup_width // 2)
        y = (tela_height // 2) - (popup_height // 2)

        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        self.resizable(False, False)

        # Remove minimizar/maximizar (Windows)
        if sys.platform.startswith("win"):
            GWL_STYLE = -16
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style &= ~WS_MINIMIZEBOX
            style &= ~WS_MAXIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            ctypes.windll.user32.SetWindowPos(
                hwnd, 0, 0, 0, 0, 0,
                0x0002 | 0x0001 | 0x0040 | 0x0020
            )

        # Conteúdo da janela:
        info = (
            "CRUD de funcionamento básico\n\n"
            "Manipulação de dados sem memória\n"
            "Interface: Python + CustomTkinter\n"
            "Desenvolvedor: Danilo dos Santos Soares\n"
            "Contato: (11) 9 4138-3504\n\n"
            "© 2026 - Todos os direitos reservados."
        )

        label_info = ctk.CTkLabel(
            master=self,
            text=info,
            justify="left",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14)
        )
        label_info.pack(padx=20, pady=20)

    # Função para alterar barra de título:
    def ativar_dark_titlebar(self):
        self.update()
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())

        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        valor = ctypes.c_int(1)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(valor),
            ctypes.sizeof(valor)
        )

    def fecha_popup(self):
        PopupSobre.instancia = None
        self.destroy()

class PopupEditar(tk.Toplevel):

     #---------------Bloco para tratar múltiplas janelas---------------
    instancia = None

    @classmethod
    def mostrar(cls, master, area_dados):

        if cls.instancia is not None:
            if cls.instancia.winfo_exists():
                cls.instancia.focus_force()
                return cls.instancia

        cls.instancia = cls(master, area_dados)
        return cls.instancia
    #-----------------------------------------------------------------

    def __init__(self, master, area_dados):
        super().__init__(master)

        self.area_dados = area_dados  # referencia do textbox

        # Capturando e exibindo valor selecionado:
        selecao = self.area_dados.tag_ranges("selecionado")
        if selecao:
            self.inicio = selecao[0]
            self.fim = selecao[1]
            texto_selecionado = self.area_dados.get(self.inicio, self.fim).strip()
        else:
            texto_selecionado = ""

        # Janela:
        self.title("Editar dado")
        self.attributes("-topmost", True)
        self.configure(bg="#2C2C2C")

        # Aplica ícone:
        GerenciadorIcone.aplicar_icone(self)

        # Conteúdo da janela:
        # -------------------------------------------------------------------
        self.pergunta_editar = ctk.CTkLabel(
            master=self,
            text=f"Digite novo valor para '{texto_selecionado}':",
            text_color="#FFFFFF"
        )
        self.pergunta_editar.pack(pady=(15, 2))

        self.editar_item = ctk.CTkEntry(
            master=self,
            width=250,
            height=28,
            text_color="#000000",
            fg_color="#FFFFFF"
        )
        self.editar_item.pack(pady=2)

        self.btn_editar = ctk.CTkButton(
            master=self,
            width=100,
            height=28,
            text="Editar",
            command=self.executar_edicao
        )
        self.btn_editar.pack(pady=(12, 2))
        # -------------------------------------------------------------------

        self.verificar_texto()

        # Ativando barra própria:
        if sys.platform.startswith("win"):
            self.after(10, self.ativar_dark_titlebar_edit)

        # Bloquear interface:
        # self.transient(master)
        # self.grab_set()         * no linux esse método não funciona
        self.focus_force()

        self.protocol("WM_DELETE_WINDOW", self.fecha_popup_edit)

        # Configuração de tamanho-centralização:
        popup_width, popup_height = 350, 140

        tela_width = self.winfo_screenwidth()
        tela_height = self.winfo_screenheight()
        x = (tela_width // 2) - (popup_width // 2)
        y = (tela_height // 2) - (popup_height // 2)

        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        self.resizable(False, False)

        # Desabilita botões (minimizar-maximizar)
        if sys.platform.startswith("win"):
            GWL_STYLE = -16
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style &= ~WS_MINIMIZEBOX
            style &= ~WS_MAXIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            ctypes.windll.user32.SetWindowPos(
                hwnd, 0, 0, 0, 0, 0,
                0x0002 | 0x0001 | 0x0040 | 0x0020
            )

    # Função da aparência própria:
    def ativar_dark_titlebar_edit(self):
        self.update()
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())

        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        valor = ctypes.c_int(1)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(valor),
            ctypes.sizeof(valor)
        )

    # Função para editar dado:
    def executar_edicao(self):

        novo_texto = self.editar_item.get().strip()

        if not novo_texto:
            return

        if not hasattr(self, "inicio") or not hasattr(self, "fim"):
            print("Nenhum dado selecionado.")
            return

        EditarDado.editar(
            self.area_dados,
            self.inicio,
            self.fim,
            novo_texto
        )

        # Fecha o popup após editar
        self.fecha_popup_edit()

    # Função de interatividade popup editar-interface:
    def fecha_popup_edit(self):
        # self.grab_release()
        PopupEditar.instancia = None
        self.destroy()

    # Verificar texto no TextBox "area_dados":
    def verificar_texto(self):
        if not self.area_dados.get("1.0", "end").strip():
            print("Sem dados para editar.")

class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x450")
        self.title("CRUD BÁSICO")
        self.resizable(True, True)

        # Inserindo ícone:
        GerenciadorIcone.aplicar_icone(self)

        # Contruindo o frame principal:
        self.frame_principal = ctk.CTkFrame(master=self)
        self.frame_principal.place(
            relx=0.5,
            rely=0.5,
            anchor=ctk.CENTER,
            relwidth=0.94,
            relheight=0.94
        )

        # Construindo a grid horizontal:
        self.frame_principal.grid_columnconfigure(0, weight=1)  # espaço esquerdo
        self.frame_principal.grid_columnconfigure(1, weight=3)  # conteúdo
        self.frame_principal.grid_columnconfigure(2, weight=1)  # botões

        # Configurando expansão vertical da área de texto:
        self.frame_principal.grid_rowconfigure(2, weight=1)

        # Título:
        self.titulo = ctk.CTkLabel(
            master=self.frame_principal,
            text="Gravação de Dados:",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=25, weight="bold")
        )
        self.titulo.grid(row=0, column=1, pady=(20, 0), sticky="n")  # colado no topo

        # Entrada de dados:
        self.entrada_dados = ctk.CTkEntry(
            master=self.frame_principal,
            height=28,
            placeholder_text="Entre com os dados aqui...",
            text_color="#000000",
            fg_color="#FFFFFF"
        )
        self.entrada_dados.grid(row=1, column=1, padx=10, pady=(18, 0), sticky="ew")  # expande horizontalmente

        # Área para visualizar dados:
        self.area_dados = ctk.CTkTextbox(
            master=self.frame_principal,
            border_color="#575151",
            border_width=2,
            state="disabled"  # desabilita entrada manual de dados
        )
        self.area_dados.grid(row=2, column=1, padx=10, pady=(18, 20), sticky="nsew")  # todas as direções
        self.area_dados.bind("<Button-1>", lambda event: SelecionarLinha.selecionar(event, self.area_dados))  # ligando evento à função
        self.area_dados.bind("<Motion>", self.alterar_cursor)  # alterar cursor na seleção

        # Remover seleção ao clicar fora do textbox
        self.bind_all("<Button-1>", self.remover_selecao, add="+")
        # add="+" mantém outros binds funcionando normalmente


        # Criando um frame lateral para os botões:
        self.frame_botoes = ctk.CTkFrame(
            master=self.frame_principal,
            fg_color="transparent"
        )
        self.frame_botoes.grid(row=1, column=2, rowspan=2, padx=(0, 40), pady=(15, 0), sticky="n")  # colado no topo

        # Configurando grid interna dos botões:
        self.frame_botoes.grid_columnconfigure(0, weight=1)  # expande horizontalmente dentro do frame

        # Criando botão 1:
        self.btn_1 = ctk.CTkButton(
            master=self.frame_botoes,
            text="Inserir",
            width=100,
            height=28,
            command=self.acao_inserir  
        )
        self.btn_1.grid(row=0, column=0, pady=5, sticky="ew")  # expande horizontalmente

        # Criando botão 2:
        self.btn_2 = ctk.CTkButton(
            master=self.frame_botoes,
            text="Carregar",
            width=100,
            height=28,
            command=self.carregar_dados
        )
        self.btn_2.grid(row=1, column=0, pady=5, sticky="ew")  # expande horizontalmente

        # Criando botão 3:
        self.btn_3 = ctk.CTkButton(
            master=self.frame_botoes,
            text="Editar",
            width=100,
            height=28,
            command=self.acao_editar
        )
        self.btn_3.grid(row=2, column=0, pady=5, sticky="ew")  #  "            "

        # Criando botão 4:
        self.btn_4 = ctk.CTkButton(
            master=self.frame_botoes,
            text="Excluir",
            width=100,
            height=28,
            command=self.acao_excluir
        )
        self.btn_4.grid(row=3, column=0, pady=5, sticky="ew")  #  "            "

        # Criando botão 5:
        self.btn_5 = ctk.CTkButton(
            master=self.frame_botoes,
            text="Limpar",
            width=100,
            height=28,
            command=self.apagar_dados
        )
        self.btn_5.grid(row=4, column=0, pady=5, sticky="ew")  #  "            "

        # Criando um frame para link:
        self.frame_link = ctk.CTkFrame(
            master=self.frame_principal,
            fg_color="transparent"
        )
        self.frame_link.grid(row=2, column=2, sticky="se", padx=15, pady=5)

        # Link para janela de informação
        self.info_sobre = ctk.CTkLabel(
            master=self.frame_link,
            text="Sobre",
            text_color="#999292",
            cursor="hand2",
            font=ctk.CTkFont(size=13)
        )
        self.info_sobre.grid(row=3, column=3, sticky="se", padx=15, pady=5)
        self.info_sobre.bind("<Button-1>", lambda e: PopupSobre.mostrar(self))  # abre janela popup

    # -----------------------------------------------------------------
    # Funções intermediárias para verificar se há dados no TextBox
    # Se não houver dados, abre a janela de alerta (classe AlertaDados)
    # -----------------------------------------------------------------

    def verificar_area_dados(self):
        # Verifica se o textbox está vazio:
        texto = self.area_dados.get("1.0", "end").strip()

        if not texto:
            AlertaDados.mostrar(self, "Não há dados disponíveis.")  # chama janela de alerta
            return False

        return True

    def acao_inserir(self):
        # Verifica se há texto no campo de entrada:
        texto = self.entrada_dados.get().strip()

        if not texto:
            mensagem = "Insira primeiro algum dado."
            AlertaDados.mostrar(self, mensagem)
            return

        InserirDado.inserir(self.entrada_dados, self.area_dados)

    def carregar_dados(self):

        SelecionarArquivo.importar_arquivo(self.area_dados)

    def acao_editar(self):

        texto = self.area_dados.get("1.0", "end").strip()
        selecao = self.area_dados.tag_ranges("selecionado")

        # Não há nenhum dado:
        if not texto:
            mensagem = "Insira primeiro algum dado."
            AlertaDados.mostrar(self, mensagem)
            return

        # Há dados mas não há seleção:
        if not selecao:
            mensagem = "Para editar selecione algum dado."
            AlertaDados.mostrar(self, mensagem)
            return

        PopupEditar.mostrar(self, self.area_dados)

    def acao_excluir(self):

        texto = self.area_dados.get("1.0", "end").strip()
        selecao = self.area_dados.tag_ranges("selecionado")

        # Não há nenhum dado:
        if not texto:
            mensagem = "Não há dados para excluir."
            AlertaDados.mostrar(self, mensagem)
            return

        # Há dados mas não há seleção:
        if not selecao:
            mensagem = "Para excluir selecione algum dado."
            AlertaDados.mostrar(self, mensagem)
            return

        ExcluirDado.excluir(self.area_dados)

    def apagar_dados(self):

        texto = self.area_dados.get("1.0", "end").strip()

        # Não há nenhum dado:
        if not texto:
            mensagem = "Não há dados para limpar."
            AlertaDados.mostrar(self, mensagem)
            return

        ApagarDados.limpar_dados(self.area_dados)

    def remover_selecao(self, event):

            try:
                # Descobre qual widget está exatamente na posição clicada:
                widget_clicado = self.winfo_containing(
                    event.x_root,
                    event.y_root
                )

            except KeyError:
                # Ignora widgets temporários do filedialog
                return

            # Se o clique 'não' foi dentro do area_dados, remove a seleção:
            if (
                widget_clicado is None or
                not str(widget_clicado).startswith(str(self.area_dados))
            ):
                self.area_dados.tag_remove(
                    "selecionado",
                    "1.0",
                    "end"
                )

    def alterar_cursor(self, event):
        # Pega índice da posição atual do mouse:
        index = self.area_dados.index(f"@{event.x},{event.y}")
        linha = index.split(".")[0]

        inicio = f"{linha}.0"
        fim = f"{linha}.0 lineend"

        texto_linha = self.area_dados.get(inicio, fim)

        # Se houver texto na linha, mostra mão:
        if texto_linha.strip():
            self.area_dados.configure(cursor="hand2")
        else:
            self.area_dados.configure(cursor="arrow")
        

if __name__ == "__main__":
    app = Interface()
    app.mainloop()