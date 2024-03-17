CREATE UNLOGGED TABLE IF NOT EXISTS CLIENTES (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  limite INTEGER NOT NULL,
  saldo INTEGER NOT NULL
);

CREATE UNLOGGED TABLE IF NOT EXISTS TRANSACOES (
  id SERIAL PRIMARY KEY,
  cliente_id INTEGER NOT NULL,
  tipo VARCHAR(1) NOT NULL,
  valor INTEGER NOT NULL,
  descricao VARCHAR(10),
  saldo INTEGER NOT NULL DEFAULT 0,
  data_transacao TIMESTAMP NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


BEGIN;
  INSERT INTO clientes (nome, limite, saldo)
  VALUES
    ('o barato sai caro', 1000 * 100, 0),
    ('zan corp ltda', 800 * 100, 0),
    ('les cruders', 10000 * 100, 0),
    ('padaria joia de cocaia', 100000 * 100, 0 ),
    ('kid mais', 5000 * 100, 0);
COMMIT;

CREATE INDEX IF NOT EXISTS idx_cliente_id ON transacoes (cliente_id);
CREATE INDEX IF NOT EXISTS idx_cliente_id_data_transacao ON transacoes (cliente_id, data_transacao);
ALTER TABLE transacoes SET (autovacuum_enabled = false);
ALTER TABLE clientes SET (autovacuum_enabled = false);