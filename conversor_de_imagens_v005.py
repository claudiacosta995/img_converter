import os
from PIL import Image
import msvcrt
import re

"""
As imagens são convertidas para o formato 450x450 ou para YYYxYYY caso a margem maior (YYY) da imagem seja maior que 450.
"""


class ImageConverter():
    def __init__(self, diretorio_entrada_imagens: str = None, diretorio_saida_imagens: str = None):
        self.entrada = diretorio_entrada_imagens
        self.saida = diretorio_saida_imagens
        self.parser()

    def parser(self):
        for img in os.listdir(self.entrada):
            name = re.search(r"(.+)(\.\w+)", img).group(1)
            if self.check_image_with_pil(self.entrada + "\\" + img):
                self.convert_img(self.saida, name, self.entrada + "\\" + img)
                print(self.saida + "\\" + img)

    @staticmethod
    def convert_img(saida, nome_image, img_url):

        image = Image.open(img_url)
        original_size = image.size

        if original_size[0] > original_size[1]:
            aresta = original_size[0]
        else:
            aresta = original_size[1]

        if aresta < 450:
            aresta = 450
        size = (aresta, aresta)

        image.thumbnail(size, Image.ANTIALIAS)
        background = Image.new('RGB', size, (255, 255, 255))
        background.paste(
            image, (int((size[0] - image.size[0]) / 2), int((size[1] - image.size[1]) / 2))
        )
        background.save('{}\\{}.jpeg'.format(saida, nome_image))

    @staticmethod
    def check_image_with_pil(path):
        try:
            Image.open(path)
        except IOError:
            return False
        return True

def get_keypress():
    '''INFO
    This function wastes all the input chars in the buffer and waits for a keypress.
    '''

    while msvcrt.kbhit(): msvcrt.getch()  # EMPTIES THE INPUTS BUFFER
    ans = msvcrt.getch()  # GETS KEYPRESS

    try:
        ans = int(ans)
        print(str(ans) + "...")
        return ans
    except:
        pass

    try:
        ans = ans.decode()  # ATTEMPTS TO DECODE
        ans = ans.lower()
    except:
        print("?...")
        return '?'

    print(str(ans) + "...")
    return ans


def main():
    DIRETORIO_ENTRADA = r"C:\ProjetosPythonGit\img_converter\FOTOS ostopad"
    DIRETORIO_SAIDA = ""

    while True:
        print("Escolha a sua pasta.")
        list_inicial = os.listdir()
        list_of_files = []

        for file in list_inicial:
            var = os.path.isdir(file)
            if os.path.isdir(file):
                list_of_files.append(file)

        for i in range(len(list_of_files)):
            print("|\n|", str(i) + "\t" + str(list_of_files[i]))
        else:
            if not list_of_files: print("|\n|", " \t(No files available in current directory.)")
            print("|\n| X \tExit")
            print("|\n| R \tRefresh")
        # GET KEYPRESS
        print("\n[?] Select an option.")
        ans = get_keypress()

        # KEYPRESS HANDLE

        # CHECK IF INT AND IN RANGE OF AVAILABLE INPUT FILES
        if (isinstance(ans, int)) and ans in range(len(list_of_files)):
            file_input_name = list_of_files[ans]
            print("[i] Using: " + str(file_input_name))
            DIRETORIO_ENTRADA = '.\\{}'.format(file_input_name)
            print("Press ANYTHING to continue...")
            ans = get_keypress()
            break
        elif ans == 'r':  # REFRESH
            pass
        elif ans == 'x':  # CHECK IF EXIT
            exit()
        else:
            print("[X] Invalid file number input.")


    DIRETORIO_SAIDA = ".\\RESULTS_{}".format(file_input_name)
    if not os.path.isdir(DIRETORIO_SAIDA):
        os.mkdir(DIRETORIO_SAIDA)

    qq = ImageConverter(DIRETORIO_ENTRADA, DIRETORIO_SAIDA)

if __name__ == '__main__':
    main()
