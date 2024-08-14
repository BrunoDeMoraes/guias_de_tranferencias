import os

def caminho_do_arquivo():
    caminho_py = __file__
    caminho_do_dir = caminho_py.split('\\')
    caminho_de_uso = ('/').join(caminho_do_dir[0:-3])
    return caminho_de_uso


def checar_pasta_de_guias(url):
    if os.path.exists(url):
        print('pasta Ok')
    else:
        os.makedirs(url)


def inverter_barra(url):
    url_separada = url.split('\\')
    nova_url = ('/').join(url_separada)
    return nova_url