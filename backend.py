# Funções dos botões:
from tkinter import filedialog  # importando recurso do sistema (window file)

class InserirDado():  # inserir = btn_1
    @staticmethod
    def inserir(entrada_dados, area_dados):

        texto = entrada_dados.get().strip()  # captura e remove espaços extras

        # Libera temporariamente para inserção:
        area_dados.configure(state="normal")

        area_dados.insert("end", texto + "\n")  # insere no final

        # Bloqueia novamente após inserir:
        area_dados.configure(state="disabled")

        # Limpa o campo de entrada:
        entrada_dados.delete(0, "end")

        print(f"Inserido: {texto}")

class SelecionarLinha():  # selecionar dado na lista
    @staticmethod
    def selecionar(event, area_dados):
        index = area_dados.index(f"@{event.x},{event.y}")
        linha = index.split(".")[0]

        area_dados.tag_remove("selecionado", "1.0", "end")

        inicio = f"{linha}.0"
        fim_visual = f"{linha}.0 lineend +1c"
        fim_texto = f"{linha}.0 lineend"

        texto_linha = area_dados.get(inicio, fim_texto)

        if not texto_linha.strip():
            return

        area_dados.tag_add("selecionado", inicio, fim_visual)
        area_dados.tag_config(
            "selecionado",
            background="#2258CC",  # marcação da seleção
            foreground="#FFFFFF"
        )

        print("Selecionado:", texto_linha)
        return texto_linha

    @staticmethod
    def limpar_selecao(area_dados):
        area_dados.tag_remove("selecionado", "1.0", "end")

class SelecionarArquivo():  # carregar = btn_2
    @staticmethod
    def importar_arquivo(area_dados):

        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[
                ("Arquivos de texto", "*.txt"),
                ("Arquivos Python", "*.py"),
                ("Todos arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        # Habilita textbox:
        area_dados.configure(state="normal")

        # Limpa conteúdo atual:
        area_dados.delete("1.0", "end")

        # Insere conteúdo novo:
        area_dados.insert("1.0", conteudo)

        # Bloqueia novamente:
        area_dados.configure(state="disabled")

        print(f"Arquivo carregado: {caminho}")

class EditarDado(): # editar = btn_3
    @staticmethod
    def editar(area_dados, inicio, fim, novo_texto):

        # Habilita edição:
        area_dados.configure(state="normal")

        # Remove texto antigo:
        area_dados.delete(inicio, fim)

        # Insere novo texto:
        area_dados.insert(inicio, novo_texto + "\n")

        # Bloqueia novamente:
        area_dados.configure(state="disabled")

        # Remove seleção:
        area_dados.tag_remove("selecionado", "1.0", "end")

        print(f"Editado para: {novo_texto}")

class ExcluirDado():  # excluir = btn_4
    @staticmethod
    def excluir(area_dados):

        ranges = area_dados.tag_ranges("selecionado")

        if not ranges:
            print("Nenhuma linha selecionada.")
            return

        inicio = ranges[0]
        linha = str(inicio).split(".")[0]

        inicio_linha = f"{linha}.0"
        fim_texto = f"{linha}.0 lineend"
        fim_linha = f"{linha}.0 lineend +1c"

        # Captura o texto antes de excluir:
        texto_excluido = area_dados.get(inicio_linha, fim_texto).strip()

        # Habilita temporariamente:
        area_dados.configure(state="normal")

        # Remove a linha inteira:
        area_dados.delete(inicio_linha, fim_linha)

        # Remove tag:
        area_dados.tag_remove("selecionado", "1.0", "end")

        # Desabilita novamente:
        area_dados.configure(state="disabled")

        print(f"Excluído: {texto_excluido}")

class ApagarDados(): # limpar = btn_5
    @staticmethod
    def limpar_dados(area_dados):
        
        # Habilita textbox:
        area_dados.configure(state="normal")

        # Limpa conteúdo:
        area_dados.delete("1.0", "end")

        # Bloqueia novamente:
        area_dados.configure(state="disabled")

        print("Conteúdo apagado.")