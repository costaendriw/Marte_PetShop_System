import sqlite3
from typing import List, Tuple

class PetShopDatabase:
    """
    Gerencia as operações de baixo nível com o banco de dados SQLite para o Pet Shop.
    """
    def __init__(self, db_name: str = "petshop.db"):
        self.db_name = db_name
        self._test_data = [
            ("Royal Canin Adult", "cão", "Royal Canin", 15.0, 89.90, 12),
            ("Whiskas Adulto Peixe", "gato", "Whiskas", 3.0, 24.50, 8),
            ("Pedigree Adulto Carne", "cão", "Pedigree", 20.0, 65.00, 15),
            ("Golden Gatos Castrados", "gato", "Golden", 10.1, 78.90, 6),
            ("Hill's Science Diet Adult", "cão", "Hill's", 12.0, 145.00, 4),
            ("Friskies Adulto Frango", "gato", "Friskies", 7.5, 42.80, 20),
            ("Premier Pet Adulto", "cão", "Premier Pet", 15.0, 98.50, 9),
            ("Purina Cat Chow Adulto", "gato", "Purina", 10.1, 68.90, 11),
            ("Eukanuba Puppy", "cão", "Eukanuba", 3.0, 56.00, 7),
            ("Royal Canin Kitten", "gato", "Royal Canin", 4.0, 52.90, 5),
            ("Biofresh Adulto Carne", "cão", "Biofresh", 25.0, 85.00, 3),
            ("Felix Adulto Salmão", "gato", "Felix", 8.0, 39.90, 16),
            ("Dogão Adulto", "cão", "Dogão", 18.0, 45.80, 22),
            ("Whiskas Filhote", "gato", "Whiskas", 1.0, 12.50, 25),
            ("Pedigree Filhote", "cão", "Pedigree", 15.0, 72.00, 8),
            ("Golden Fórmula Adulto", "gato", "Golden", 10.1, 74.90, 10),
            ("Gran Plus Adulto", "cão", "Gran Plus", 20.0, 78.50, 6),
            ("Fancy Feast Adulto", "gato", "Fancy Feast", 3.0, 35.90, 14),
            ("Faro Adulto Premium", "cão", "Faro", 15.0, 95.00, 12),
            ("Purina Pro Plan Gato", "gato", "Purina", 7.5, 89.90, 7),
            ("Champ Adulto", "cão", "Champ", 25.0, 58.90, 18),
            ("Whiskas Sachê Adulto", "gato", "Whiskas", 0.085, 2.50, 150),
            ("Eukanuba Senior", "cão", "Eukanuba", 12.0, 125.00, 4),
            ("Golden Gatos Idosos", "gato", "Golden", 10.1, 82.90, 5),
            ("Baw Waw Adulto", "cão", "Baw Waw", 20.0, 42.00, 30),
            ("Friskies Filhote", "gato", "Friskies", 3.0, 28.90, 12),
            ("Premier Pet Filhote", "cão", "Premier Pet", 10.1, 89.50, 8),
            ("Purina Cat Chow Filhote", "gato", "Purina", 3.0, 35.90, 15),
            ("Hill's Science Diet Senior", "cão", "Hill's", 12.0, 155.00, 3),
            ("Royal Canin Persian", "gato", "Royal Canin", 4.0, 98.90, 6),
            ("Biofresh Senior", "cão", "Biofresh", 15.0, 92.00, 7),
            ("Felix Sachê Frango", "gato", "Felix", 0.085, 2.80, 200),
            ("Dogão Filhote", "cão", "Dogão", 15.0, 52.80, 11),
            ("Whiskas Gatos Idosos", "gato", "Whiskas", 3.0, 28.90, 9),
            ("Pedigree Senior", "cão", "Pedigree", 15.0, 76.00, 13),
            ("Golden Gatos Persas", "gato", "Golden", 10.1, 84.90, 4),
            ("Gran Plus Filhote", "cão", "Gran Plus", 15.0, 85.50, 6),
            ("Fancy Feast Sachê", "gato", "Fancy Feast", 0.085, 3.20, 80),
            ("Faro Premium Senior", "cão", "Faro", 15.0, 105.00, 5),
            ("Purina Pro Plan Senior Gato", "gato", "Purina", 7.5, 95.90, 8),
            ("Champ Filhote", "cão", "Champ", 15.0, 65.90, 14),
            ("Whiskas Temptations", "gato", "Whiskas", 0.18, 8.50, 45),
            ("Eukanuba Large Breed", "cão", "Eukanuba", 15.0, 135.00, 3),
            ("Golden Gatos Siameses", "gato", "Golden", 10.1, 79.90, 7),
            ("Baw Waw Senior", "cão", "Baw Waw", 20.0, 48.00, 16),
            ("Friskies Indoor", "gato", "Friskies", 7.5, 46.80, 10),
            ("Premier Pet Super Premium", "cão", "Premier Pet", 15.0, 125.50, 5),
            ("Purina Cat Chow Sachê", "gato", "Purina", 0.085, 2.90, 120),
            ("Hill's Prescription Diet", "cão", "Hill's", 12.0, 185.00, 2),
            ("Royal Canin Maine Coon", "gato", "Royal Canin", 4.0, 105.90, 4)
        ]
        self.init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Retorna uma conexão ao banco de dados.
        Configura row_factory para acessar colunas por nome.
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row # Permite acessar resultados como dicionários
        return conn

    def init_database(self):
        """Inicializa o banco de dados e cria a tabela 'racoes' se ela não existir."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS racoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        tipo_animal TEXT NOT NULL CHECK (tipo_animal IN ('gato', 'cão')),
                        marca TEXT NOT NULL,
                        peso REAL NOT NULL CHECK (peso > 0),
                        preco REAL NOT NULL CHECK (preco > 0),
                        estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
            print("✅ Banco de dados inicializado com sucesso!")
        except sqlite3.Error as e:
            print(f"❌ Erro ao inicializar o banco de dados: {e}")
    
    def inserir_dados_teste(self):
        """Insere dados de teste no banco de dados se a tabela 'racoes' estiver vazia."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM racoes")
                count = cursor.fetchone()[0]
                
                if count == 0:
                    cursor.executemany('''
                        INSERT INTO racoes (nome, tipo_animal, marca, peso, preco, estoque) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', self._test_data)
                    conn.commit()
                    print(f"✅ {len(self._test_data)} rações inseridas no banco de dados!")
                else:
                    print(f"ℹ️ Banco já possui {count} rações cadastradas.")
        except sqlite3.Error as e:
            print(f"❌ Erro ao inserir dados de teste: {e}")