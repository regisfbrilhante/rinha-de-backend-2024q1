
DROP TABLE IF EXISTS CLIENTES; 
DROP TABLE IF EXISTS TRANSACOES;

CREATE TABLE CLIENTES (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  limite INTEGER NOT NULL,
  saldo INTEGER DEFAULT 0
);

CREATE TABLE TRANSACOES (
  id SERIAL PRIMARY KEY,
  cliente_id INTEGER NOT NULL,
  valor INTEGER NOT NULL,
  descricao VARCHAR(10),
  data_transacao TIMESTAMP NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


BEGIN;
  INSERT INTO clientes (nome, limite)
  VALUES
    ('o barato sai caro', 100000),
    ('zan corp ltda', 80000),
    ('les cruders', 1000000),
    ('padaria joia de cocaia', 10000000),
    ('kid mais', 500000);
COMMIT;



BEGIN;
  INSERT INTO transacoes (cliente_id, valor, data_transacao) VALUES
    (1, 1000 * 100, '2024-03-08 00:00:00'),
    (2, 800 * 100, '2024-03-08 00:00:00'),
    (3, 10000 * 100, '2024-03-08 00:00:00'),
    (4, 100000 * 100, '2024-03-08 00:00:00'),
    (5, 5000 * 100, '2024-03-08 00:00:00');
END;