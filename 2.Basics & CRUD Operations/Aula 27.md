# Understanding Projection
Em casos cujo o documento que desejamos recuperar contenha dados que não precisamos para a nossa aplicação, ao invés de recuperar tudo e filtrar o que é necessário através do código da nossa aplicação, podemos utilizar a **projeção** para isso:

Utilizando os dados de passageiros, suponhamos que estejamos interessados apenas nos nomes, utilizando o comando `find()` passamos o primeiro argumento como um objeto vazio, pois desejamos encontrar TODOS os nomes de passageiros. Em seguida passamos o argumento que nos permitirá fazer a projeção, como regra, passamos o par de chaves `{}` e dentro dele a chave que desejamos e como valor `1` que significa `inclua os dados que está retornando`

```javascript
db.passengers.find({}, {name: 1})
```

![Projection](Imagens/07.projection.png)

Porém o ID continua sendo retornado, por regra ele é SEMPRE incluido, para excluí-lo devemos explicitamente informar passando a chave `id:` seguido por 0:

```javascript
db.passengers.find({},{name: 1, _id: 0})
```

![Projection](Imagens/08.projection.png)

