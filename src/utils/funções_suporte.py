def caminho_do_arquivo():
    caminho_py = __file__
    caminho_do_dir = caminho_py.split('\\')
    caminho_de_uso = ('/').join(caminho_do_dir[0:-3])
    return caminho_de_uso