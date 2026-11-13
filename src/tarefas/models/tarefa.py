from datetime import datetime

from tarefas.models.database import Database


class Tarefa:
    """Provê métodos para armazenar, recuperar e processar os dados das tarefas."""


    def __init__(self, titulo, id=None, data_conclusao=None):
        self.id = id
        self.titulo = titulo
        self.data_conclusao = data_conclusao


    def salvarTarefa(self):
        """Salva a tarefa no banco de dados."""

        sql = 'INSERT INTO tarefa (titulo_tarefa, data_conclusao) VALUES (%s, %s);'
        params = (self.titulo, self.data_conclusao)

        # Gerenciador de contexto (with)
        # Acessa os métodos __enter__ e __exit__ da classe
        with Database() as db:
            db.executar(sql, params)


    @staticmethod
    def listarTarefas() -> list:
        """Retorna uma lista com todas as tarefas cadastradas."""

        sql = '''SELECT id_tarefa, 
        titulo_tarefa, 
        data_conclusao 
        FROM tarefa 
        LIMIT 100;'''

        with Database() as db:
            tarefas_banco = db.executar(sql)

        return tarefas_banco if tarefas_banco else []

    @staticmethod
    def carregarTarefa(id):
        """Carrega uma tarefa do banco e retorna uma instância do modelo."""

        sql = '''SELECT id_tarefa, titulo_tarefa, data_conclusao
        FROM tarefa
        WHERE id_tarefa = %s;'''

        with Database() as db:
            tarefa_banco = db.executar(sql, (id,))

        if not tarefa_banco:
            return None

        # Converte a linha retornada pelo banco em um objeto usado pelo formulário.
        tarefa_banco = tarefa_banco[0]
        return Tarefa(
            id=tarefa_banco["id_tarefa"],
            titulo=tarefa_banco["titulo_tarefa"],
            data_conclusao=tarefa_banco["data_conclusao"],
        )

    def alterarTarefa(self):
        """Atualiza os dados da tarefa no banco de dados."""

        sql = '''UPDATE tarefa
        SET titulo_tarefa = %s, data_conclusao = %s
        WHERE id_tarefa = %s;'''
        # O ID restringe a alteração a esta tarefa.
        params = (self.titulo, self.data_conclusao, self.id)

        with Database() as db:
            db.executar(sql, params)

    @staticmethod
    def apagarTarefa(id):
        sql = 'DELETE FROM tarefa WHERE id_tarefa = %s;'

        # O ID é enviado como parâmetro, sem concatená-lo ao SQL.
        with Database() as db:
            db.executar(sql, (id,))

# Área de testes
tarefa = Tarefa("Estudar Python")
tarefa.salvarTarefa()