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


```bash 
#!/bin/bash
```
Cette première instruction du fichierdéclare qu'il s'agit d'un script shell.

Voici ce qui se passe ensuite ligne par ligne 
1. On débute une boucle qui déclare que l'on va prendre chaque fichier du répertoire dont l'extension est _pdf_ (for...;) 
2. *do* débute l'execution de la boucle
3. 
do #début de la boucle
