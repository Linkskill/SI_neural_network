
# SI-NeuralNetwork

## Instalação

* Clone o repositório (ou só baixe o .zip e extraia):
```
    git clone https://github.com/GabrielEug2/SI-NeuralNetwork.git
```

* Verifique se você possui o Python 3.6.x ou superior e pip instalados:
```
    python3 -V  # => "Python 3.6.x"
    pip3 -V  # => "pip 10.x.x from (...)/python3.6/site-packages/pip (python 3.6)
```

Caso não estejam instalados:
```
    sudo apt-get install python3
    sudo apt-get install python3-pip
```

* Atualize o pip e instale as bibliotecas necessárias:
```
    pip3 install --upgrade pip
    pip3 install keras numpy
    pip3 install tensorflow  # Veja a solução de problemas abaixo
```

* Instale o [VREP 3.5](http://www.coppeliarobotics.com/downloads.html).

* Copie os seguintes arquivos da sua pasta de instalação do VREP para o diretório atual:
<!---
* vrep.py
* vrepConst.py
Ambos estão localizados em /programming/remoteApiBindings/python/python na pasta da sua instalação do VREP.
-->
* remoteApi.dll (Windows), remoteApi.dylib (MAC) or remoteApi.so (Linux) (localizados em /programming/remoteApiBindings/lib/lib)

---
## Executando

Inicie a simulação no VREP com a cena __CenaKhepheraK3.ttt__.

Rode o script python:
```
    python3 neural_network_k3.py (por enquanto é testing.py)
```

---
## Solução de Problemas

* Se na instalação do tensorflow aparecer
<pre>
    "Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/usr/local/lib/python3.6/dist-packages/tensorflow-1.x.x.dist-info'
    Consider using the `--user` option or check the permissions.
</pre>
Faça como indicado e use a flag --user
```
    pip install --user tensorflow==1.5
```

* Se ao executar aparecer o erro _"Illegal instruction (core dumped)"_, significa que sua CPU não suporta instruções AVX (é o caso do meu notebook). Fazer downgrade para a versão 1.5 do tensorflow resolve o problema:
```
    pip uninstall tensorflow
    pip install tensorflow==1.5
```

---
## Links úteis

* [Configurando a API remota do VREP](http://www.coppeliarobotics.com/helpFiles/en/remoteApiClientSide.htm)
* [Funções da API remota (Python) do VREP](http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm)
---
