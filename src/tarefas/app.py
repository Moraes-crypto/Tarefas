from flask import Flask, abort, redirect, render_template, request, url_for

from tarefas.models.database import init_db
from tarefas.models.tarefa import Tarefa

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route('/test')
def test():
    return "Servidor online!"

@app.route('/', methods=["GET", "POST"])
def home():

    if request.method == "POST":
        titulo_form = request.form["tituloTarefa"] # Casa com o nome do input no form
        data_conclusao_form = request.form["dataConclusao"] # Casa com o nome do input no form

        data_corrigida = data_conclusao_form or None

        # Instanciamos uma nova tarefa com os daos recebisdos do form
        tarefa = Tarefa(titulo = titulo_form, data_conclusao = data_corrigida)
        
        # Salvar a tarefa no banco
        tarefa.salvarTarefa()

        return redirect(url_for("home"))

    tarefas = Tarefa.listarTarefas()

    return render_template(
        "base.html",
        titulo_da_pagina = "Minha lista de tarefas", 
        tarefas_da_pagina = tarefas,
        tarefa_em_edicao = None,
        )


# GET carrega a tarefa no formulário; POST recebe e salva os novos valores.
@app.route('/editar/<int:id>', methods=["GET", "POST"])
def editar_tarefa(id):
    if request.method == "POST":
        titulo_form = request.form["tituloTarefa"]
        data_conclusao_form = request.form["dataConclusao"] or None

        # Mantém o ID da URL para alterar somente a tarefa selecionada.
        tarefa = Tarefa(
            id=id,
            titulo=titulo_form,
            data_conclusao=data_conclusao_form,
        )
        tarefa.alterarTarefa()
        return redirect(url_for("home"))

    tarefa = Tarefa.carregarTarefa(id)
    if tarefa is None:
        # Uma tarefa inexistente não pode ser carregada para edição.
        abort(404)

    return render_template(
        "base.html",
        titulo_da_pagina="Minha lista de tarefas",
        tarefas_da_pagina=Tarefa.listarTarefas(),
        tarefa_em_edicao=tarefa,
    )

# A exclusão só acontece por POST, enviado pelo formulário de cada tarefa.
@app.route('/apagar/<int:id>', methods=["POST"])
def apagar_id_especificado(id):
    # Encaminha o ID recebido ao modelo e retorna para a lista.
    Tarefa.apagarTarefa(id)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
