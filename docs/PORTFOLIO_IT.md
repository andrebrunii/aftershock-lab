# Presentare AFTERSHOCK

## Il messaggio principale

«Sto studiando come rendere verificabili le risposte automatiche di sicurezza. Ho un laboratorio che confronta contenimento e danno collaterale e testa un rollback che non cancella modifiche successive.»

È una descrizione proporzionata al progetto. Non dichiarare di aver inventato il digital twin, eliminato la prompt injection o costruito un SOC di produzione.

## Demo di tre minuti

**0:00–0:30 — Il problema.** Apri il primo scenario e chiedi: «Bloccheresti questo IP se fermasse tutte le richieste d'attacco?» Mostra il blocco IP: 100 richieste d'attacco negate, ma anche 600 richieste legittime.

**0:30–1:00 — Il confronto.** Seleziona il controllo sui percorsi: 100 richieste d'attacco negate, nessuna richiesta legittima negata in questo fixture. Apri le evidenze e spiega che la correttezza dipende dal campione e dalle ipotesi.

**1:00–1:30 — Il limite.** Passa all'identità condivisa o al traffico sconosciuto. Mostra che il sistema può rifiutare tutte le opzioni. Una risposta automatica non deve per forza produrre un'azione.

**1:30–2:20 — Il momento tecnico.** Nella sezione rollback mostra prima l'aggiornamento del banner che sopravvive. Poi seleziona il conflitto sullo stesso controllo: il valore sembra uguale, ma la revisione è diversa, quindi il rollback viene rifiutato.

**2:20–3:00 — La verifica.** Mostra un test sulle revisioni, il tuo esperimento personale e un limite rimasto aperto. Se non hai eseguito Ollama, presenta l'adattatore come opzionale e non come un'integrazione LLM già misurata.

## Le domande difficili

- **Perché lo chiami controfattuale?** Confronto l'esito dello stesso workload sotto stati alternativi dentro un modello deterministico. Non inferisco causalità da log reali.
- **Chi decide che una richiesta è malevola?** Le etichette sono assegnate nel fixture sintetico. In un ambiente reale questa è un'incertezza da affrontare separatamente.
- **Perché non basta un prompt che dica al modello di essere prudente?** La proposta non deve avere l'autorità di approvare, eseguire o auto-certificare il proprio impatto.
- **L'hash è un'autorizzazione sicura?** No. Vincola la revisione locale a un contenuto; non autentica un approvatore e non impedisce al proprietario del database di modificarlo.
- **Il rollback risolve l'incidente?** No. Può riaprire l'accesso; è una compensazione della configurazione simulata, non una decisione completa di recovery.
- **Cosa succede con una dipendenza mancante?** Se è un riferimento inesistente il simulatore si ferma; se è omessa dal modello, l'impatto può essere sottostimato. Serve validare il modello contro la realtà.
- **L'hai fatto con AI?** La base è stata preparata con assistenza AI. Descrivi esattamente quali parti hai verificato, corretto ed esteso e mostra gli esperimenti che hai eseguito tu.

## Bozza LinkedIn — dopo verifica e pubblicazione

Un'automazione di sicurezza può fermare l'attacco e, nello stesso momento, bloccare i clienti legittimi.

Sto lavorando a AFTERSHOCK, un laboratorio che mette alla prova proprio questo compromesso: confronta azioni di contenimento sullo stesso traffico sintetico, mostra le richieste danneggiate e verifica se il rollback conserva le modifiche di altri operatori.

Nel primo scenario il blocco di un IP nega tutte le 100 richieste d'attacco, ma anche 600 richieste legittime. Un controllo più preciso cambia il risultato. In altri scenari nessuna azione supera la policy: la risposta corretta è fermarsi e approfondire.

La parte che mi interessa di più è il rollback: un valore uguale non significa necessariamente che nessuno lo abbia modificato nel frattempo.

[AGGIUNGI QUI UN ESPERIMENTO CHE HAI ESEGUITO PERSONALMENTE]

Repository: [INSERISCI IL LINK PUBBLICATO]

#CyberSecurity #AISecurity #IncidentResponse #Python #LearningInPublic

## Prima della candidatura

Completa almeno un esperimento, registra un video breve e verifica la CI nel tuo repository. Allega il link al progetto e una spiegazione di due righe sul problema affrontato. Questo è materiale da discutere con un referente tecnico; il codice da solo non determina assunzione, ruolo o stipendio.
