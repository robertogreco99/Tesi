# Tesi

Lavoro sulla tesi 
1. Docker file 
    - a. docker build -t image_name .
    - b.docker run -it -v /home/roberto/Scaricati/Tesi/Lavoro\ sulla\ tesi/Tesi/Input:/inputs -v /home/roberto/Scaricati/Tesi/Lavoro\ sulla\ tesi/Tesi/Risultato:/results image sh ( per ora in Input ho il video su cui lavorare)
2. Script che esegue ffmpeg + valutazione con vmaf : run_experiments.sh
3. Analyze.pi per tirare fuori il json che tira fuori vmaf : deve raccogliere  i risultati e lavorarci
- produrre : per esempio differenti temporal pooling methods (media, mediana, media armonica, media geometrica, 95-th percentile, ecc.) 
- produrre i files per fare i grafici con gnuplot  o direttamente i grafici con una libreria python (come per es. matplotlib).
