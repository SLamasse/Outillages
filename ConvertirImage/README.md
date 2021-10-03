## ConvertAllpdftoJpG.sh 

Ce script est une boucle en shell qui doit permettre de convertir tous les pdf d'un répertoire en fichier jpg : 

```bash 
for inputfile in ./*.pdf ; do
    outputfile="${inputfile%.*}.jpg"
    convert  -sharpen 0x4 -verbose -density 150 -trim "$inputfile" -quality 100  -resize 900x900 "$outputfile" &&
    [[ -e "$outputfile" && "$inputfile" != "$outputfile" ]] && rm "$inputfile"
done
```


