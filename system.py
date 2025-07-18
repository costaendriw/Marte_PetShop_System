import sqlite3
import shutil
from datetime import datetime
from typing import Optional, Dict, Tuple

# --- Constantes (melhorar a legibilidade e manutenção) ---
VALID_ANIMAL_TYPES = ['gato', 'cão']
ANIMAL_ALIAS = {'cao': 'cão'} # Mapeia 'cao' para 'cão'

# Importa a classe do arquivo database.py
from database import PetShopDatabase

class PetShopSystem:
    """
    Implementa a lógica de negócio do sistema Pet Shop, interagindo com o banco de dados.
    """
    def __init__(self, db_name: str = "petshop.db"):
        self.db = PetShopDatabase(db_name)
        self.db.inserir_dados_teste()
    
    def _normalize_animal_type(self, tipo_animal: str) -> Optional[str]:
        """
        Normaliza o tipo de animal (ex: 'cao' para 'cão').
        Retorna o tipo normalizado ou None se inválido.
        """
        lower_tipo = tipo_animal.lower().strip()
        if lower_tipo in ANIMAL_ALIAS:
            return ANIMAL_ALIAS[lower_tipo]
        elif lower_tipo in VALID_ANIMAL_TYPES:
            return lower_tipo
        return None

    def _validate_feed_data(self, data: Dict) -> Tuple[bool, str]:
        """
        Valida um dicionário de dados de ração.
        Retorna uma tupla (booleano de validade, mensagem de erro).
        Atualiza o dicionário 'data' com o tipo de animal normalizado.
        """
        if 'tipo_animal' in data and data['tipo_animal'] is not None:
            normalized_type = self._normalize_animal_type(data['tipo_animal'])
            if normalized_type is None:
                return False, f"Tipo de animal '{data['tipo_animal']}' inválido. Deve ser 'gato' ou 'cão'."
            data['tipo_animal'] = normalized_type # Atualiza o dicionário com o tipo normalizado
            
        if 'peso' in data and data['peso'] is not None and data['peso'] <= 0:
            return False, "Peso deve ser um valor positivo."
        
        if 'preco' in data and data['preco'] is not None and data['preco'] <= 0:
            return False, "Preço deve ser um valor positivo."
        
        if 'estoque' in data and data['estoque'] is not None and data['estoque'] < 0:
            return False, "Estoque não pode ser negativo."
            
        return True, ""

    def cadastrar_racao(self, nome: str, tipo_animal: str, marca: str, 
                         peso: float, preco: float, estoque: int = 0) -> bool:
        """Cadastra uma nova ração no banco de dados."""
        racao_data = {
            'nome': nome.strip(),
            'tipo_animal': tipo_animal.strip(),
            'marca': marca.strip(),
            'peso': peso,
            'preco': preco,
            'estoque': estoque
        }

        valido, mensagem = self._validate_feed_data(racao_data)
        if not valido:
            print(f"❌ {mensagem}")
            return False
        
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO racoes (nome, tipo_animal, marca, peso, preco, estoque)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (racao_data['nome'], racao_data['tipo_animal'], racao_data['marca'], 
                      racao_data['peso'], racao_data['preco'], racao_data['estoque']))
                
                conn.commit()
                produto_id = cursor.lastrowid
            
            print(f"✅ Ração '{racao_data['nome']}' cadastrada com sucesso! ID: {produto_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Erro ao cadastrar ração: {e}")
            return False
            
    def listar_racoes(self, filtro_animal: Optional[str] = None):
        """Lista todas as rações ou filtra por tipo de animal."""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT id, nome, tipo_animal, marca, peso, preco, estoque 
                    FROM racoes 
                '''
                params = []
                
                if filtro_animal:
                    filtro = self._normalize_animal_type(filtro_animal)
                    if filtro is None:
                        print(f"❌ Tipo de animal para filtro '{filtro_animal}' inválido. Deve ser 'gato' ou 'cão'.")
                        return
                    query += "WHERE tipo_animal = ? "
                    params.append(filtro)
                
                query += "ORDER BY nome"
                
                cursor.execute(query, tuple(params))
                racoes = cursor.fetchall() # Retorna objetos sqlite3.Row
            
            if not racoes:
                print("📦 Nenhuma ração encontrada!")
                return
            
            print(f"\n{'='*85}")
            print(f"{'ID':<4} {'Nome':<22} {'Tipo':<6} {'Marca':<15} {'Peso':<8} {'Preço':<10} {'Estoque':<8}")
            print(f"{'='*85}")
            
            for racao in racoes:
                # Acessando por nome da coluna graças ao row_factory
                print(f"{racao['id']:<4} {racao['nome'][:21]:<22} {racao['tipo_animal']:<6} {racao['marca'][:14]:<15} "
                      f"{racao['peso']:<8}kg R${racao['preco']:<9.2f} {racao['estoque']:<8}")
                        
        except sqlite3.Error as e:
            print(f"❌ Erro ao listar rações: {e}")

    def buscar_racao(self, id_produto: int) -> Optional[Dict]:
        """Busca uma ração pelo ID. Retorna um dicionário com os dados ou None se não encontrada."""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, nome, tipo_animal, marca, peso, preco, estoque, data_cadastro
                    FROM racoes WHERE id = ?
                ''', (id_produto,))
                
                resultado = cursor.fetchone() # Retorna um objeto sqlite3.Row
            
            if resultado:
                # Convertendo sqlite3.Row para Dict para consistência, se desejado
                return dict(resultado)
            return None
            
        except sqlite3.Error as e:
            print(f"❌ Erro ao buscar ração: {e}")
            return None
    
    def atualizar_racao(self, id_produto: int, **kwargs) -> bool:
        """Atualiza dados de uma ração. Retorna True se sucesso, False caso contrário."""
        if not self.buscar_racao(id_produto):
            print(f"❌ Ração com ID {id_produto} não encontrada!")
            return False
        
        # Validar todos os campos recebidos antes de construir a query
        valido, mensagem = self._validate_feed_data(kwargs)
        if not valido:
            print(f"❌ {mensagem}")
            return False

        campos_validos = {
            "nome": "nome = ?", "tipo_animal": "tipo_animal = ?", "marca": "marca = ?",
            "peso": "peso = ?", "preco": "preco = ?", "estoque": "estoque = ?"
        }
        
        updates = []
        valores = []
        
        for campo, valor in kwargs.items():
            if campo not in campos_validos:
                print(f"❌ Campo '{campo}' não é válido para atualização e será ignorado!")
                continue 
            
            updates.append(campos_validos[campo])
            valores.append(valor)
        
        if not updates:
            print("❌ Nenhum campo válido para atualizar foi fornecido!")
            return False
        
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                query = f"UPDATE racoes SET {', '.join(updates)} WHERE id = ?"
                valores.append(id_produto)
                
                cursor.execute(query, valores)
                conn.commit()
            
            print(f"✅ Ração ID {id_produto} atualizada com sucesso!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Erro ao atualizar ração: {e}")
            return False
            
    def deletar_racao(self, id_produto: int) -> bool:
        """Deleta uma ração pelo ID. Retorna True se sucesso, False caso contrário."""
        racao = self.buscar_racao(id_produto)
        
        if not racao:
            print(f"❌ Ração com ID {id_produto} não encontrada!")
            return False
        
        confirmacao = input(f"⚠️  Tem certeza que deseja deletar '{racao['nome']}'? (s/N): ").strip()
        
        if confirmacao.lower() != 's':
            print("❌ Operação cancelada!")
            return False
        
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM racoes WHERE id = ?", (id_produto,))
                conn.commit()
            
            print(f"✅ Ração '{racao['nome']}' deletada com sucesso!")
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Erro ao deletar ração: {e}")
            return False
    
    def estatisticas(self):
        """Mostra estatísticas do sistema, como total de rações, valor do estoque, etc."""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM racoes")
                total_racoes = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM racoes WHERE tipo_animal = 'gato'")
                racoes_gatos = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM racoes WHERE tipo_animal = 'cão'")
                racoes_caes = cursor.fetchone()[0]
                
                cursor.execute("SELECT SUM(preco * estoque) FROM racoes")
                valor_total = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT COUNT(*) FROM racoes WHERE estoque = 0")
                sem_estoque = cursor.fetchone()[0]
                
                cursor.execute('SELECT nome, preco FROM racoes ORDER BY preco DESC LIMIT 5')
                mais_caros = cursor.fetchall()
                
                cursor.execute('SELECT nome, estoque FROM racoes ORDER BY estoque DESC LIMIT 5')
                maior_estoque = cursor.fetchall()
            
            print(f"\n📊 ESTATÍSTICAS DO PET SHOP")
            print(f"{'='*45}")
            print(f"Total de rações cadastradas: {total_racoes}")
            print(f"Rações para gatos: {racoes_gatos}")
            print(f"Rações para cães: {racoes_caes}")
            print(f"Valor total do estoque: R$ {valor_total:.2f}")
            print(f"Produtos sem estoque: {sem_estoque}")
            
            print(f"\n💰 TOP 5 PRODUTOS MAIS CAROS:")
            for i, racao in enumerate(mais_caros, 1):
                print(f"{i}. {racao['nome']} - R$ {racao['preco']:.2f}")
            
            print(f"\n📦 TOP 5 PRODUTOS COM MAIOR ESTOQUE:")
            for i, racao in enumerate(maior_estoque, 1):
                print(f"{i}. {racao['nome']} - {racao['estoque']} unidades")
                        
        except sqlite3.Error as e:
            print(f"❌ Erro ao gerar estatísticas: {e}")
    
    def backup_database(self, arquivo_backup: str = None) -> bool:
        """Faz backup do banco de dados. Retorna True se sucesso, False caso contrário."""
        if not arquivo_backup:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_backup = f"backup_petshop_{timestamp}.db"
        
        try:
            shutil.copy2(self.db.db_name, arquivo_backup)
            print(f"✅ Backup criado com sucesso: {arquivo_backup}")
            return True
        except Exception as e:
            print(f"❌ Erro ao fazer backup: {e}")
            return False