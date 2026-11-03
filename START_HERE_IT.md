# AFTERSHOCK — Parti da qui

**La domanda del progetto:** quando automatizzi la risposta a un attacco, quanto danno puoi provocare agli utenti legittimi? E puoi annullare la tua modifica senza cancellare il lavoro di un altro operatore?

È il seguito naturale dei tuoi laboratori: Git/CI/CD → detection → decisione di risposta → controllo dell'impatto → rollback. Qui lavori anche sul confine tra una proposta AI e un'azione autorizzata.

## 1. Guarda subito il risultato

Estrai lo ZIP e apri `DEMO.html` con un doppio clic. Funziona offline, senza installare nulla.

Nel primo scenario prova **Block the source IP**, poi **Block sensitive file paths**. Nel dataset entrambi fermano 100 richieste d'attacco. Il blocco IP nega anche 600 richieste legittime; il controllo sui percorsi nega zero richieste legittime.

Muovi il cursore del budget: stai esplorando una scelta di policy, non lanciando azioni. Apri le evidenze per vedere richieste concrete. Nel terzo scenario nessuna risposta è accettabile con la policy iniziale: il sistema deve ammettere il limite. Nel quarto mancano etichette affidabili per parte del traffico.

Nella sezione rollback passa da **Unrelated operator change** a **Same-control conflict**. I quattro passaggi mostrano stati registrati durante vere transazioni SQLite locali.

## 2. Rigenera la demo da Git Bash

Apri Git Bash nella cartella `aftershock-lab`. Serve Python 3.10 o successivo:

```bash
python --version
python -m aftershock demo
python -m unittest discover -s tests -v
```

Se Windows riconosce solo `py`, sostituisci `python` con `py`. La cartella corrente deve contenere `README.md` e la directory `aftershock`. Non servono pacchetti Python esterni per demo e test.

Apri `output/index.html`. `output/results.json` contiene i risultati da cui è generata la pagina. L'output atteso riporta 4 scenari, 20 replay di azioni e 8 casi di proposta verificati. Questi 8 casi sono scritti apposta per il test: non sono risposte misurate di un modello AI.

## 3. Prova un rollback che conserva una modifica successiva

```bash
python -m aftershock init --db output/preserve.db
python -m aftershock plan --db output/preserve.db --out output/preserve-plan.json
```

Apri `output/preserve-plan.json`. Leggi `proposal`, `evaluation.patch`, i conteggi e i controlli. Copia il valore di `plan_digest` e sostituiscilo a `DIGEST_LETTO`:

```bash
python -m aftershock apply --db output/preserve.db --plan output/preserve-plan.json --approve DIGEST_LETTO
python -m aftershock edit --db output/preserve.db --key config:banner --value '"v2-operator-release"'
python -m aftershock rollback --db output/preserve.db --transaction DIGEST_LETTO
python -m aftershock audit --db output/preserve.db
```

L'identificatore della transazione coincide con il digest del piano. Il controllo sui percorsi torna allo stato precedente, mentre il banner `v2-operator-release` resta. Il rollback riguarda lo stato simulato, non la cronologia Git.

`init` rifiuta un database già inizializzato. Per ripetere l'esercizio scegli un nuovo nome, per esempio `output/preserve2.db`.

## 4. Crea un conflitto vero

Ripeti init e plan usando `output/conflict.db` e `output/conflict-plan.json`. Approva il nuovo digest, poi:

```bash
python -m aftershock edit --db output/conflict.db --key rule:sensitive --value true
python -m aftershock rollback --db output/conflict.db --transaction NUOVO_DIGEST
```

Il rollback viene rifiutato. Perché? Un operatore ha scritto sulla stessa cella dopo l'azione iniziale. Anche se il valore è ancora `true`, la revisione è cambiata: non puoi assumere di essere ancora proprietario di quella modifica. È il punto più interessante da spiegare durante la demo.

Puoi anche provare un'approvazione vecchia: genera un piano, cambia il banner **prima** di applicarlo e tenta l'apply. Il sistema richiede una nuova valutazione.

## 5. Pubblica sul tuo profilo

Crea su GitHub, come `andrebrunii`, una repository vuota chiamata `aftershock-lab`. Non aggiungere README, licenza o .gitignore dal sito: sono già nel pacchetto.

```bash
git init -b main
git status
git add .
git diff --cached --stat
git commit -m "Add response collateral and rollback laboratory"
git remote add origin https://github.com/andrebrunii/aftershock-lab.git
git push -u origin main
```

Controlla la scheda Actions dopo il push. I file `output/`, database, ambiente virtuale e risultati dei tuoi modelli sono esclusi dal versionamento. La demo pre-generata è invece inclusa come documento dimostrativo.

Descrizione About: `Rehearse security responses, measure collateral damage, and test conflict-aware rollback before trusting an AI proposal.`

Topics: `cybersecurity`, `ai-security`, `incident-response`, `python`, `sqlite`, `rollback`, `prompt-injection`, `devsecops`.

## 6. Rendilo tuo con Riccardo

Prima di presentarlo, completate un esercizio di `docs/EXPERIMENTS.md`. Uno dei due cambia una dipendenza o costruisce un caso limite; l'altro deve prevedere il risultato prima di eseguirlo. Documenta un errore iniziale, la correzione e il test che impedisce la regressione. Queste sono prove di comprensione utili in colloquio.

Per la parte LLM effettiva segui `docs/OLLAMA.md`; il modello locale è opzionale. Per il confronto con progetti e paper già esistenti leggi `docs/RESEARCH_IT.md`. Per la presentazione di tre minuti e il testo LinkedIn usa `docs/PORTFOLIO_IT.md`.
