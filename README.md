# Tesi

Per fare girare  
1. specificare  nel json config.json : 
    - nome immagine docker 
    - cartella dove trovare i video di input di riferimento
    - cartella dove trovare i video distorted
    - cartella dove salvare i risultati
    - cartella dove salvare i file di hash
    - video di interesse
    - versione del modello vmaf di interesse
    - dataset di interesse
2. python3 create_commands.py config.json
3. docker build -t <_nome immagine scelto nel file_>
4. lancio il comando salvato nel file 
5. ottengo un json con i risultati





Lavoro sulla tesi 
1. Docker file 
    - a. docker build -t image_name .
    - b1. Lanciare il container il modalitò interattiva e lanciare da dentro gli script ( riferimento a docker file riserva ) : docker run -it -v /home/roberto/Scaricati/Tesi/Lavoro\ sulla\ tesi/Tesi/Input:/inputs -v /home/roberto/Scaricati/Tesi/Lavoro\ sulla\ tesi/Tesi/Risultato:/
    results image sh ( per ora in Input ho il video su cui lavorare)
    - b2 : Lanciare direttamente gli script dal docker file :  docker run -it   -v /home/roberto/Scaricati/Tesi/Lavoro\ sulla\ tesi/Tesi/Input:/inputs   -v /home/roberto/Scaricati/Tesi/Lavoro\ sulla\ tesi/Tesi/Risultato:/results   image

2. Script che esegue ffmpeg + valutazione con vmaf : run_experiments.sh
3. Analyze.pi per tirare fuori il json che tira fuori vmaf : deve raccogliere  i risultati e lavorarci
- produrre : per esempio differenti temporal pooling methods (media, mediana, media armonica, media geometrica, 95-th percentile, ecc.) 
- produrre i files per fare i grafici con gnuplot  o direttamente i grafici con una libreria python (come per es. matplotlib).


Per trovare le versioni
apt-cache policy <libreria> e ho preso quella candidata (se candidata = installata è stata installata l'ultima)