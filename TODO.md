# Incontro prof

Considerazioni su cosa modificare :
devo lavorare sulla decodifica dei file. Il confronto è tra file yuv di partenza e yuv decodifcato ( dal distorto vado a fare la decodifica e la dimensione deve 
essere la stessa dell'originale)
Le misure su cui lavorare sono tutte anche psnr,ssim,ms-ssim e il vmaf chiarament
In uscita sarebbbe ideale avere un csv con tutte le informazioni.
Il j4 nel make non è un problmea
Devo usare più modelli di netflix, non solo il base.

yuv deve essere yuv 420 , devo considere casi particolari 
- video che non sono 1920*1080 devono essere portati in quel formato ( fare il rescaling con l'opzione di ffmpeg)
- video non yuv420 ma yuv diversi

Mi devo ricordare di fare mapping tra container lxc e docker per evitare di fare duplicati all'interno del container


Nuovo flusso

yuv originale + yuv dalla decodifica ---> vmaf : tiro fuori json
questo per esempio deve essere un singolo container
script che per file fifa lancia ogni volta un docker per un singolo file della decodifica ( 1 docker : 1 lavoro su un file fifa particolare)
1. su un fifa + fifa.264  ---> tiro fuori json
2. fifa +fifa.265 ecc ---> tiro fuori json

alla fine metto insieme i json e li devo poi mettere in un csv per le analisi più importanti

Il docker deve essere lanciato con un run personalizzabile o un file di configurazione per scegliere il file o le misure o il modello vmaf

Il primo dataset su cui lavorare è kugud

Ricordarsi 1920*1080

# Mail prof 
- commenti in inglese
## Vmaf
- usare versione v.3.0.0
Per la versione stabile v3.0.0 di VMAF, hai due opzioni:

1. **Clonare il repository e fare checkout del tag**: Questo ti permette di avere l'ultima versione direttamente dal repository di GitHub. Ecco come potrebbe essere aggiunto al Dockerfile:
   ```Dockerfile
   # Clona il repository VMAF e fai checkout del tag v3.0.0
   RUN git clone https://github.com/Netflix/vmaf.git && \
       cd vmaf && \
       git checkout v3.0.0
   ```

2. **Scaricare e includere lo zip**: Se preferisci una riproducibilità perfetta, puoi scaricare la versione zip direttamente da GitHub, tenerla nel progetto e usarla nel Dockerfile. Questo approccio evita problemi se il repository dovesse scomparire. Ecco un esempio di Dockerfile con questa opzione:
   ```Dockerfile
   # Scarica il file zip della versione v3.0.0
   ADD https://github.com/Netflix/vmaf/archive/refs/tags/v3.0.0.zip /tmp/
   RUN unzip /tmp/v3.0.0.zip -d /opt/ && \
       cd /opt/vmaf-3.0.0 && \
       make
   ```

Un suggerimento potrebbe essere quello di lasciare il comando di clonazione commentato nel Dockerfile come backup:
```Dockerfile
# RUN git clone https://github.com/Netflix/vmaf.git && cd vmaf && git checkout v3.0.0
```
## ffmpeg
Per FFmpeg, con la versione stabile v7.0.2, puoi adottare un approccio simile a quello proposto per VMAF. Ecco le due opzioni:

1. **Clonare il repository e fare checkout del tag**: Puoi ottenere la versione direttamente dal repository ufficiale. Ecco come potrebbe essere configurato nel Dockerfile:
   ```Dockerfile
   # Clona il repository FFmpeg e fai checkout del tag v7.0.2
   RUN git clone https://github.com/FFmpeg/FFmpeg.git && \
       cd FFmpeg && \
       git checkout n7.0.2
   ```

2. **Scaricare e includere lo zip**: Per garantire la riproducibilità, puoi scaricare l'archivio zip del tag specifico, includerlo nel tuo progetto e fare il build direttamente. Questo ti protegge nel caso il repository non fosse più disponibile in futuro:
   ```Dockerfile
   # Scarica il file zip della versione v7.0.2
   ADD https://github.com/FFmpeg/FFmpeg/archive/refs/tags/n7.0.2.zip /tmp/
   RUN unzip /tmp/n7.0.2.zip -d /opt/ && \
       cd /opt/FFmpeg-n7.0.2 && \
       ./configure && \
       make && \
       make install
   ```

Anche qui, lasciare il comando di clonazione come commento può essere utile come riferimento o backup:
```Dockerfile
# RUN git clone https://github.com/FFmpeg/FFmpeg.git && cd FFmpeg && git checkout n7.0.2
```

## riproducibilità

- Settare versione di partenza del container 
    - Per esempio ora parto da python:3.9-alpine (ma è una specica versione? non è che è l'ultima alpine con supporto python? dovremmo fissare una versione)
    -  Stessa cosa per il resto dei pacchetti, soprattutto quelli di libreria dei codec che vengono integrati e usati, cioe' x264-dev x265-dev vpx aom ecc. E' vero che il risultato della decodica dovrebbe essere uguale perché standardizzato, ma si sa mai. Dovrebbe essere in grado di mettere tipo x264-dev:150 (per dire ... per specicare una certa versione - guardi cosa le installa e usi le ultime attuali)
    - Il resto (matplotlib panda etc...) ci penseremo poi, ma non e' cosi' fondamentale

## hash
- Dopo la decodifica del file server l'hash dello yuv che esce (es. con
md5sum o sha1sum o qualcosa di simile - cosi' rilasceremo anche il filee con gli hash e chiunque puo' vericare che il risultato sia quello atteso.
- sarebbe bene integrare un check alla ne di tutto il lavoro, che se c'e' l'hash del file lo verica e se non c'e' da' un WARNING - ma lo potremo fare solo a fine lavoro

Integrare il calcolo degli hash nei file YUV dopo la decodifica è un ottimo metodo per garantire che il risultato sia riproducibile e verificabile da chiunque. Ecco il processo da seguire e come potrebbe essere implementato:

### 1. **Calcolo dell'hash dopo la decodifica**
Dopo aver decodificato il file video in YUV, puoi calcolare l'hash (ad esempio con `md5sum` o `sha1sum`). Questo hash garantisce che il file non sia stato alterato, e chiunque esegua il processo può confrontare l'hash per verificare se il risultato è quello atteso.

Esempio in un Dockerfile o script:
```bash
# Decodifica il file video in YUV
ffmpeg -i input.mp4 output.yuv

# Calcola l'hash del file YUV
md5sum output.yuv > output.yuv.md5
```

Oppure, se preferisci `sha1sum`:
```bash
sha1sum output.yuv > output.yuv.sha1
```

### 2. **Verifica dell'hash**
Alla fine del processo, puoi includere un controllo per verificare se l'hash calcolato corrisponde a quello atteso. Puoi farlo con uno script che controlla l'hash generato e quello memorizzato in un file di riferimento. Ad esempio:
```bash
if [ -f "output.yuv.md5" ]; then
    md5sum -c output.yuv.md5
else
    echo "WARNING: No hash file found for verification"
fi
```

Questo script controlla se il file `output.yuv.md5` esiste e, in tal caso, verifica l'integrità del file YUV confrontandolo con l'hash registrato. Se il file hash non è presente, viene mostrato un avviso.

### 3. **Integrazione in un flusso di lavoro**
Integrare questo controllo alla fine di tutto il processo è utile per garantire che i file siano corretti prima di procedere ulteriormente. Puoi aggiungere questo passaggio come fase finale nel tuo Dockerfile o script per assicurarti che il file YUV sia verificato ogni volta che viene eseguita una decodifica.

A questo punto, puoi anche distribuire l'hash insieme ai file YUV per permettere agli altri di verificare i risultati, aumentando la trasparenza e la riproducibilità del processo.

Questa verifica può essere migliorata e automatizzata in seguito, ma l'approccio di base ti consente di iniziare a garantire la correttezza dei risultati.

## vmaf 

### vmaf modelli

- usare 9 modelli : models="vmaf_v0.6.1 vmaf_v0.6.1neg vmaf_oat_v0.6.1 vmaf_oat_v0.6.1neg vmaf_oat_b_v0.6.3
vmaf_b_v0.6.3 vmaf_oat_4k_v0.6.1 vmaf_4k_v0.6.1 vmaf_4k_v0.6.1neg"
- dopo la compilazione devo fare girare l'eseguibile  : 
libvmaf/build/tools/vmaf 
Si lancia come:

`VMAFCOMMAND -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=vmaf_4k_v0.6.1neg `

-r reference 
-d distorto 
-o fille_risultato 
--json voglio un json 
-q non stampa nulla a video 
-m opzione del modello  :  i modelli dovrebbero essere stati integrati all'interno dell'eseguibile quindi senza necessita' di
caricarli da le esterno, comunque se necessario e' possibile usare l'opzione path= come si vede sotto

Il .y4m e' non compresso e contiene un header che gia' dice il formato del le (dimensioni, e tipo di rappresentazione 420 422 444 e n.di bpp)
Prende anche gli .yuv ma in questo caso bisogna dare -w , -h, -p come sotto. 

Salvo indicazioni differenti gli yuv sono 420 (per es. KUGVD sono 420).

Usi dei nomi ragionevoli (anche abbreviati, ma ragionevoli) per il fille di result: per es.
result__KUGVD__PARAMETRICODIFICA__VMAFMODEL.json
dove PARAMETRICODIFICA dipendera' dal dataset (e' una delle cose da passare come parametro al docker,
oltre al resto). 
Per es. in KUGVD potrebbe essere "1280x720_600_x264" (il resto, se tutto uguale, lo 
possiamo tralasciare). Se ha idee migliori non si senta troppo vincolato a queste indicazioni.

Se lancia l'eseguibile vmaf senza comandi vede cosa prende:
Usage: /vmaf/libvmaf/build/tools/vmaf [options]
Supported options:
--reference/-r $path: path to reference .y4m or .yuv
--distorted/-d $path: path to distorted .y4m or .yuv
--width/-w $unsigned: width
--height/-h $unsigned: height
--pixel_format/-p: $string pixel format (420/422/444)
--bitdepth/-b $unsigned: bitdepth (8/10/12/16)
--model/-m $params: model parameters, colon ":" delimited
                          `path=` path to model file 
 
                          `version=` built-in model version 
 
                          `name=` name used in log (optional) 
--output/-o $path: output le
--xml: write output le as XML (default)
--json: write output le as JSON
--csv: write output le as CSV
--sub: write output le as subtitle
--threads $unsigned: number of threads to use
--feature $string: additional feature
--cpumask: $bitmask restrict permitted CPU instruction sets
--gpumask: $bitmask restrict permitted GPU operations
--frame_cnt $unsigned: maximum number of frames to process
--frame_skip_ref $unsigned: skip the rst N frames in reference
--frame_skip_dist $unsigned: skip the rst N frames in distorted
--subsample: $unsigned compute scores only every N frames
--quiet/-q: disable FPS meter when run in a TTY
--no_prediction/-n: no prediction, extract features only
-version/-v: print version and exit

Un esepio per avere il json alla fine /vmaf/libvmaf/build/tools/vmaf -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=vmaf_4k_v0.6.1neg

Per eseguire l'analisi con VMAF e far girare tutti i modelli come hai indicato, puoi costruire uno script o una sequenza di comandi che passano i modelli al comando VMAF uno per volta. Qui c'è un esempio di come puoi impostare la struttura:

### Esempio : 
### Struttura generale del comando VMAF
```bash
VMAFCOMMAND -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=MODEL_VERSION
```

Ogni esecuzione del comando conterrà:
- `-r`: il file video di riferimento non compresso (formato .y4m o .yuv)
- `-d`: il file video distorto non compresso
- `-o`: il file di output JSON, con il nome strutturato secondo il formato richiesto
- `--json`: formato di output come JSON
- `-q`: silenzia l'output sul terminale
- `-m version=MODEL_VERSION`: indica il modello da utilizzare

### Comandi specifici per ogni modello
Dal momento che devi far girare 9 modelli diversi, puoi usare uno script per iterare sui modelli e creare il file di output con un nome adeguato per ciascuno:

Esempio di uno script bash che gestisce i modelli:

```bash
#!/bin/bash

# Variabili per i file
original="original.y4m"  # Sostituisci con il percorso del file di riferimento
distorted="distorted.y4m"  # Sostituisci con il percorso del file distorto
dataset="1280x720_600_x264"  # Parametro di codifica dipendente dal dataset

# Lista dei modelli VMAF da eseguire
models=("vmaf_v0.6.1" "vmaf_v0.6.1neg" "vmaf_oat_v0.6.1" "vmaf_oat_v0.6.1neg"
        "vmaf_oat_b_v0.6.3" "vmaf_b_v0.6.3" "vmaf_oat_4k_v0.6.1"
        "vmaf_4k_v0.6.1" "vmaf_4k_v0.6.1neg")

# Eseguire VMAF per ogni modello
for model in "${models[@]}"; do
    # Creare il nome del file di output
    output="result__KUGVD__${dataset}__${model}.json"
    
    # Comando VMAF
    /libvmaf/build/tools/vmaf -r $original -d $distorted -o $output --json -q -m version=$model
    
    # Controlla se l'esecuzione ha successo
    if [ $? -eq 0 ]; then
        echo "Modello $model completato, output salvato in $output"
    else
        echo "Errore con il modello $model"
    fi
done
```

### Per YUV File
Se usi file .yuv, dovrai aggiungere parametri aggiuntivi per larghezza, altezza e formato pixel. Ecco un esempio:

```bash
/libvmaf/build/tools/vmaf -r reference.yuv -d distorted.yuv -w 1920 -h 1080 -p 420 \
    -o result__KUGVD__${dataset}__${model}.json --json -q -m version=$model
```

### Nome del file di output
Come da te richiesto, i file di output seguiranno questa struttura:
```bash
result__KUGVD__PARAMETRICODIFICA__VMAFMODEL.json
```
Ad esempio:
```bash
result__KUGVD__1280x720_600_x264__vmaf_v0.6.1.json
```

In questo modo, ogni modello produrrà un file JSON separato con i risultati VMAF per l'analisi successiva.

Se hai domande o hai bisogno di modifiche specifiche allo script, fammi sapere!


### secondo passaggio vmaf
Certo! Dopo aver eseguito i vari modelli di VMAF, puoi fare un'ulteriore analisi utilizzando il comando VMAF con alcune feature aggiuntive per calcolare altre metriche di qualità, come PSNR e SSIM. Ecco come puoi procedere.

#### Obiettivo
L'idea è di eseguire il comando VMAF per calcolare metriche aggiuntive, specificando diverse feature, inclusi PSNR e SSIM. Puoi iniziare con una o due feature e verificare che vengano correttamente incluse nel file JSON di output.

#### Comando VMAF con Feature Aggiuntive
Ecco come strutturare il comando VMAF per includere le feature richieste:

```bash
/libvmaf/build/tools/vmaf -r original.y4m -d distorted.y4m -o result_features.json \
--json -q -m version=MODEL_VERSION --feature psnr --feature oat_ssim
```

#### Spiegazione dei parametri
- `--feature`: questo parametro permette di specificare metriche aggiuntive da calcolare. Puoi usarlo più volte per includere diverse misure. Alcune delle feature che hai menzionato sono:
  - `--feature psnr`: calcola il Peak Signal-to-Noise Ratio.
  - `--feature oat_ssim`: calcola l'Ordinary Average (OAT) SSIM.
  - Altre feature come `oat_ms_ssim`, `ciede`, e `psnr_hvs` possono essere aggiunte in seguito, a seconda delle necessità.

#### Esempio di Script Completo
Puoi integrare questa logica nel tuo script, aggiungendo un'ulteriore sezione per eseguire il comando con le feature:

```bash
# Ultimo giro con feature aggiuntive
for model in "vmaf_v0.6.1"; do  # Scegli un modello "a caso" per questo esempio
    output_features="result__KUGVD__${dataset}__${model}__features.json"
    
    /libvmaf/build/tools/vmaf -r $original -d $distorted -o $output_features --json -q -m version=$model \
    --feature psnr --feature oat_ssim
    
    if [ $? -eq 0 ]; then
        echo "Modello $model con feature completato, output salvato in $output_features"
    else
        echo "Errore con il modello $model e le feature aggiuntive"
    fi
done
```

#### Inizio con Solo 1 o 2 Feature
Poiché alcune metriche possono richiedere più tempo per essere calcolate, è sensato iniziare con solo 1 o 2 feature (ad esempio, `psnr` e `oat_ssim`) per verificare che tutto funzioni correttamente. Una volta che sei sicuro che il comando funzioni e che i risultati siano corretti, puoi aggiungere altre feature, come `oat_ms_ssim`, `ciede` e `psnr_hvs`.

#### Controllo del Risultato
Dopo l'esecuzione del comando, controlla il file JSON di output per verificare che le metriche siano state calcolate e siano presenti. Dovresti vedere le metriche PSNR e SSIM insieme ai risultati di VMAF, rendendo il tuo report più completo.

## podman 
A questo punto c'e' da decidere come far funzionare il container docker/podman, cioe' cosa prende come parametri.
- Se e' solo un modo di lanciare VMAF, si potrebbe fare in modo che quando si lancia vengano passati tutti gli  parametri sulla linea di comando direttamente al comando VMAF dentro il container, che dice?

Tipo: podman run --rm miovmaf -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=vmaf_4k_v0.6.1neg

Quindi si sposta la "complessita'" di gestire il dataset ad uno script di shell (o python) al di fuori del container,
anche solo generando le linee di comando da lanciare per fare tutti i tests desiderati.
Aggiornamenti su cosa fare.mdmd 2024-09-26
 / 
Tipo:
python create_vmaf_cmdlines.py DIR_ORIG DIR_PVS VMAF PSNR SSIM etc.....
e questo genera N linee tipo:
podman run --rm miovmaf -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m
version=vmaf_4k_v0.6.1neg
dove in ogni linea c'e' un certo distorted (che si chiama anche PVS), con il corrispondente original (dedotto
direttamente dal nome del le), il le json corrispondente (di nuovo dedotto dal nome del PVS), ecc.
Spero di essermi spiegato.
Dopo che piu' o meno tutto e' in piedi, cerchiamo di gestire il resizing per le PVS che non hanno la stessa
risoluzione dell'original