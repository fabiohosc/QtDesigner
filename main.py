import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
import pymysql
from usuario import Ui_Dialog


class ControleFicha(QDialog):
      def __init__(self):
            super().__init__()
            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
            self.configurar_botoes()

      def configurar_botoes(self):
            self.ui.pb_.clicked.connect(self.acao_Adicionar)
            self.ui.pb_1.clicked.connect(self.acao_Excluir)
            self.ui.pb_2.clicked.connect(self.acao_Atualizar)
            self.ui.pb_3.clicked.connect(self.acao_Localizar)

# Banco de dados
      def conectar_banco(self):
            try:
                  conexao = pymysql.connect(
                        host = "localhost",
                        port = 3307,
                        user = "root",
                        password = "usbw",
                        database = "test",
                        charset = "latin1"
                  )
                  return conexao
            except Exception as e:
                  QMessageBox.critical(self, "Erro de Conexão", f"Não foi possivel conectar ao banco de dados:\n{e}")
                  return None     
###  
      def acao_Adicionar(self):
            nome = self.ui.txt_.text()
            if nome.strip() == "":
                  QMessageBox.warning(self, "Aviso", "Por favor , digite um nome!")
                  return 

            db = self.conectar_banco()
            if db:
                  try:
                        cursor = db.cursor()
                        sql = "INSERT INTO usuarios (nome) VALUES (%s)"
                        cursor.execute(sql, (nome,))
                        db.commit()
                        QMessageBox.information(self, "Sucesso", f"Usuário {nome} adicionado com sucesso!")
                        self.ui.txt_.clear()
                  except Exception as e:
                        QMessageBox.critical(self, "Erro", f"Falha ao adicionar:\n{e}")
###          
      def acao_Excluir(self):
            nome = self.ui.txt_.text()
            if nome.strip() == "":
                  QMessageBox.warning(self, "Aviso", "Digite um nome para ser excluido")
                  return 
            
            db = self.conectar_banco()
            if db:
                  try:
                        cursor = db.cursor()
                        sql = "DELETE FROM usuarios WHERE nome = %s"
                        cursor.execute(sql, (nome,))
                        db.commit()
                  
                        QMessageBox.information(self, "Excluindo", f"Usuário {nome} excluido com sucesso!")
                        self.ui.txt_.clear()
                  except Exception as e:
                        QMessageBox.critical(self, "Erro", f"Falha ao excluir:\n{e}")
###          
      def acao_Atualizar(self):
            nome = self.ui.txt_.text()
            if nome.strip() == "":
                  QMessageBox.warning(self, "Aviso", "Digite um nome para ser atualizar!")
                  return 

            db = self.conectar_banco()
            if db:
                  try:
                        cursor = db.cursor()
                        sql = "UPDATE usuarios SET nome = %s WHERE nome = %s"
                        cursor.execute(sql, (nome,))
                        db.commit()
                        QMessageBox.information(self, "Sucesso", f"Dados do usuário {nome} atualizados!")
                        self.ui.txt_.clear()
                  except Exception as e:
                        QMessageBox.critical(self, "Aviso", f"Falha ao Atualizar: {nome}\n{e}")
###           
      def acao_Localizar(self):
            nome = self.ui.txt_.text()
            if nome.strip() == "":
                  QMessageBox.warning(self, "Aviso", "Digite um nome para ser localizado")
                  return 
            
            db = self.conectar_banco()
            if db:
                  try:
                        cursor = db.cursor()
                        sql = "SELECT*FROM usuarios WHERE nome = %s"
                        cursor.execute(sql, (nome,))
                        resultado = cursor.fetchone()
                        if resultado:
                              QMessageBox.information(self, "Usuário encontrado", f"ID: {resultado[0]}\n", f"Nome: {resultado[1]}\n")
                        else:
                              QMessageBox.warning(self, "Usuário não encontrado", "Usuário não existe!")
                  except Exception as e:
                        QMessageBox.critical(self, "Aviso", f"Falha ao Localizar: {nome}\n{e}")


# 4. Execução do Programa
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ControleFicha()
    window.show()
    sys.exit(app.exec_())
