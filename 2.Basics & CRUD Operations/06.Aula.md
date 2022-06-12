# Understanding Databases, Collections & Documents

Em um servidor MongoDB, podemos ter um ou mais bancos de dados, cada banco de dados pode conter uma ou mais coleções, que por sua vez pode conter vários documentos. Documentos são realmente os dados.

> [!tip]
> Coleções podem ser comparadas as tabelas do SQL 

Para inicializar o servidor MongoDB no Linux, basta executar o seguinte comando:
```bash
sudo mongod
```

Esse comando pode receber alguns parâmetros, como por exemplo, `--port` e o número da porta que se deseja inicializar o servidor.

No windows, basta digitar 
```powershell
mongosh
```

Outro parâmetro interessante é `--help` ou simplesmente `-h`

