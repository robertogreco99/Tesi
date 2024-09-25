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

