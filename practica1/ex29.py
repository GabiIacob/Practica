with open("fisier.txt" , "w") as file:
    file.write("Python")

import shutil
shutil.copy("fisier.txt", "ex.txt")