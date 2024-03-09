CREATE TABLE IF NOT EXISTS CLIENTES (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  limite INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS TRANSACOES (
  id SERIAL PRIMARY KEY,
  cliente_id INTEGER NOT NULL,
  tipo VARCHAR(1) NOT NULL,
  valor INTEGER NOT NULL,
  descricao VARCHAR(10),
  saldo INTEGER NOT NULL,
  data_transacao TIMESTAMP NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


BEGIN;
  INSERT INTO clientes (nome, limite)
  VALUES
    ('o barato sai caro', 1000 * 100),
    ('zan corp ltda', 800 * 100),
    ('les cruders', 10000 * 100),
    ('padaria joia de cocaia', 100000 * 100),
    ('kid mais', 5000 * 100);
COMMIT;
