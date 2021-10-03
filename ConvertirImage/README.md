## ConvertAllpdftoJpG.sh 

Ce script est une boucle en shell qui doit permettre de convertir tous les pdf d'un répertoire en fichier jpg : 

```bash 
#!/bin/bash

for inputfile in ./*.pdf ; do
    outputfile="${inputfile%.*}.jpg"
    convert  -sharpen 0x4 -verbose -density 150 -trim "$inputfile" -quality 100  -resize 900x900 "$outputfile" &&
    [[ -e "$outputfile" && "$inputfile" != "$outputfile" ]] && rm "$inputfile"
done
```

Quelques petites explications, nous allons utiliser une boucle et un sous programme qui se nomme Imagemagick avec une [documentation](https://imagemagick.org/script/command-line-options.php) et des [exemples](https://legacy.imagemagick.org/Usage/) 

La toute première instruction du fichier déclare qu'il s'agit d'un script shell.
```bash 
#!/bin/bash
```


Voici ce qui se passe ensuite ligne par ligne 
1. On débute une boucle qui déclare que l'on va prendre chaque fichier du répertoire dont l'extension est **pdf** dans une variable _inputfile_ (for inputfile ...;) 
2. **do** débute l'execution de la boucle, pour chaque _inputfile_ on va faire quelque chose 
3. _outputfile="${inputfile%.*}.jpg"_  on récupère le nom du fichier et on le fait suivre d'une extension .jpg 
4. là on utilise la fonction convert d'imagemagick (voir plus  bas) 
5. cette ligne permet d'effacer le fichier original du  répertoire
6. **done**  permet de terminer



A propos de la fonction convert : 
```bash 
convert  
    -sharpen 0x4 
    -verbose 
    -density 150 
    -trim 
    "$inputfile" # le nom de fichier initial 
    -quality 100  
    -resize 900x900 
    "$outputfile" # le nouveau ne fichier 
```
