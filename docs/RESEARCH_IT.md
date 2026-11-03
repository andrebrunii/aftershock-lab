# AFTERSHOCK — Dossier di ricerca e scelta del progetto

Ricerca svolta il **17 ottobre 2026**. Obiettivo: scegliere un progetto da portfolio coerente con Git/CI/CD, WAF, SOC, Splunk e sicurezza degli agenti AI, realizzabile su un normale PC e difendibile durante una dimostrazione tecnica.

## La conclusione

La direzione scelta è un **laboratorio delle conseguenze della risposta di sicurezza**: confronta l'effetto di più interventi sullo stesso traffico sintetico, conserva esempi concreti di richieste legittime danneggiate e verifica se il rollback può annullare la propria modifica senza cancellare modifiche successive.

Il contributo è un prototipo piccolo e verificabile che rende osservabile un compromesso spesso nascosto nelle demo: fermare il traffico etichettato come attacco non basta per scegliere una risposta. Servono anche informazioni sul danno collaterale, sulla copertura del campione e sulla possibilità di annullare il cambiamento.

**Non è un'invenzione mondiale.** La ricerca ha trovato lavori direttamente vicini all'idea. La formulazione corretta per il portfolio è «ho realizzato e valutato questo laboratorio», non «ho inventato il primo sistema al mondo». L'originalità di un progetto personale può stare nel problema circoscritto, negli esperimenti e nelle scelte implementative, senza una falsa rivendicazione di priorità scientifica.

## Come è stata condotta la ricerca

Sono state effettuate ricerche web con due motori, seguite da consultazione di fonti primarie: repository degli autori, articoli scientifici, documentazione OWASP, AWS, Microsoft e Ollama, e pagine ufficiali Accenture. Query utilizzate, tra le altre:

- `SOC automated remediation counterfactual blast radius simulation agent prompt injection`
- `security incident response digital twin dry run rollback agent`
- `counterfactual rollback SOC agent`
- `Agentic Incident Response through Multiscale Planning with a Digital Twin`
- `compensating transaction concurrent changes`
- `Accenture Cyber Defense Expert SIEM SOAR automation`

È una ricognizione ragionata finalizzata al progetto, non una revisione sistematica esaustiva o una ricerca brevettuale. Le funzionalità dichiarate nei README dei progetti confrontati non sono state tutte riprodotte. Non sono stati eseguiti i loro benchmark. Le pagine di recruiting cambiano: una pagina raggiungibile o indicizzata non prova che una candidatura sia ancora aperta.

## Il confronto con ciò che esiste già

| Fonte primaria | Che cosa copre | Conseguenza per la scelta di AFTERSHOCK |
| --- | --- | --- |
| [AgentDojo, paper e repository][S1] | Valutazione di attacchi e difese contro prompt injection in agenti che usano strumenti | Non chiamare un piccolo set di stringhe malevole un benchmark equivalente. Separare la verifica del contratto dai risultati su un modello reale. |
| [soc-agent, repository dell'autore][S2] | Investigazione SOC, policy, approvazioni, replay e rollback | «Un SOC con AI e approval gate» è già una direzione affollata. Concentrarsi su un esperimento più ristretto e leggibile. |
| [Agentic Incident Response con digital twin, artefatti degli autori][S3] | Generazione e valutazione di azioni di recupero in un ambiente simulato, con componenti LLM e container | Non rivendicare come nuova la simulazione prima della risposta. Scegliere un modello più piccolo, senza GPU o Docker obbligatori, documentandone la minore fedeltà. |
| [CIPHER-A, articolo del 29 agosto 2026][S4] | Valutazione controfattuale delle conseguenze di azioni di incident response | Esiste un precedente diretto alla domanda «che cosa succede se eseguo questa risposta?». AFTERSHOCK non replica né supera i risultati del paper. |
| [Microsoft, Compensating Transaction][S5] | Annullamento degli effetti di operazioni tenendo conto del lavoro concorrente | Un ripristino dell'intero stato può cancellare modifiche valide. Il prototipo deve conservare il prima/dopo delle sole celle toccate. |
| [AWS, rollback safety][S6] | Problemi di sicurezza del rollback durante le distribuzioni | Il percorso inverso deve essere progettato e verificato; non basta un pulsante «undo». |
| [OWASP, Excessive Agency][S7] | Rischi derivanti da eccessive capacità, permessi o autonomia degli agenti | L'LLM propone un identificatore di azione; il codice controlla effetti e autorizzazione. Nessun tool generico o shell. |
| [OWASP, Prompt Injection Prevention][S8] | Confini tra dati non fidati, istruzioni e uso degli strumenti | Una riga di log che dichiara «approvato» resta un dato. Le difese non possono ridursi a una lista di parole vietate. |

### Una cautela metodologica utile

L'articolo CIPHER-A segnala che alcune metriche di confronto con altri lavori sono stime ricavate dagli autori a partire da indicatori pubblicati, non misure indipendenti direttamente confrontabili [S4]. Per questo il progetto non riprende quei numeri per proclamare un miglioramento. I risultati di AFTERSHOCK derivano soltanto dal proprio codice, dai propri scenari e dalle ipotesi dichiarate.

## Perché questa idea e non altre

| Alternativa | Vantaggio | Motivo per non sceglierla come progetto principale |
| --- | --- | --- |
| Chatbot RAG che spiega alert | Semplice da mostrare e pertinente all'AI | Rischia di diventare soprattutto un'interfaccia sopra un modello, con poca verifica delle azioni. |
| Classificatore di prompt injection | Tema attuale | La qualità richiede dataset e valutazione robusti; pochi esempi selezionati non sostengono una percentuale di efficacia. |
| SOC completo con molti agenti | Ampio perimetro funzionale | Più integrazioni da configurare, meno tempo per capire e verificare ciascun componente; precedenti già articolati [S2]. |
| Digital twin di infrastruttura cloud | Maggiore realismo | Requisiti e superficie operativa superiori; può spostare il progetto sul setup anziché sugli esperimenti [S3]. |
| AFTERSHOCK | Una domanda concreta, due fallimenti dimostrabili, codice eseguibile offline | Fedeltà limitata del modello; va presentato come laboratorio, non sistema operativo di risposta. |

Questa valutazione è un giudizio progettuale per il tuo livello e i tuoi strumenti, non una classifica misurata del mercato.

## Collegamento con competenze professionali

La pagina ufficiale Accenture **Cyber Defense Expert**, identificativo R00284999, descrive attività con SIEM, SOAR, EDR e strumenti di automazione per rilevamento e gestione delle minacce [S9]. È un riferimento alle competenze, non una promessa di assunzione né una conferma della disponibilità della posizione in una sede specifica. Alcuni altri URL di annunci consultati hanno restituito errori o un reindirizzamento alla ricerca generale: non sono usati come opportunità verificate.

La mia inferenza è che un prototipo che obbliga a spiegare **efficacia, impatto sul servizio, policy, audit e recupero** offra materiale concreto per un colloquio in questo ambito. Non misura la probabilità di assunzione e non determina una retribuzione.

| Competenza | Evidenza concreta nel repository | Domanda da preparare |
| --- | --- | --- |
| Python e automazione | Motore deterministico, CLI, suite di test | Quali input rifiuti e perché? |
| Incident response | Confronto fra contenimento e traffico legittimo negato | Quando scegli di non automatizzare una risposta? |
| Sicurezza AI | Proposta senza autorità, contratto ristretto, replay indipendente | Perché il modello non può certificare da solo la sicurezza della propria azione? |
| Stato e concorrenza | Transazioni SQLite e controllo delle revisioni | Perché verificare soltanto il valore non basta per il rollback? |
| DevSecOps | Workflow CI, gate statico, evidenze riproducibili | Cosa dimostra la CI e cosa resta fuori? |
| Comunicazione tecnica | Decisioni, limiti e protocollo esperimenti | Come descrivi un risultato senza esagerarne la portata? |

## Le ipotesi che il codice verifica

**H1 — Un alto contenimento può nascondere un danno elevato.** Nel caso dell'IP condiviso, bloccare l'IP nega 100/100 richieste d'attacco e 600/900 richieste legittime. Il controllo sui percorsi nega 100/100 richieste d'attacco e 0/900 legittime. Le etichette sono note perché il dataset è costruito; non sono una stima di produzione.

**H2 — Il sistema deve poter dichiarare che non c'è una risposta accettabile.** Nel caso dell'identità condivisa, ogni azione efficace disponibile blocca anche troppo traffico legittimo. Il risultato corretto con la policy iniziale è l'escalation, non una raccomandazione forzata.

**H3 — «Zero danno noto» non equivale a copertura sufficiente.** Nel caso con traffico non classificato, il controllo ristretto nega anche richieste di esito ignoto. La policy valuta separatamente gli sconosciuti e la percentuale etichettata.

**H4 — Un rollback completo può annullare lavoro valido.** Il test applica il contenimento, registra un aggiornamento del banner da parte di un operatore e poi compensa solo il controllo. Il banner nuovo sopravvive.

**H5 — Anche un valore identico può rappresentare un conflitto.** Un secondo operatore riscrive lo stesso controllo; il valore resta uguale, ma la revisione cambia. Il rollback viene rifiutato. Questo verifica l'autorità sullo stato, non la bontà semantica della decisione dell'operatore.

**H6 — L'autorità non arriva dal testo della proposta.** I casi di test includono approvazione inventata nel testo, riferimenti inesistenti e un campo comando extra. Il contratto e la policy li invalidano o negano. Questo non dimostra che un modello LLM resista alla prompt injection: per quello serve l'esperimento separato [S1, S8, S10].

**Controllo negativo eseguito:** il programma di sensitivity aggiunge richieste legittime proprio a un percorso bloccato dalla risposta «precisa». La policy passa con 18 richieste danneggiate su 918 legittime e fallisce con 19 su 919. Il risultato illustra un confine della policy e smentisce l'idea che quel controllo sia intrinsecamente innocuo. Il CSV e il comando di riproduzione sono inclusi.

## Cosa farebbe davvero crescere il progetto

1. Aggiungere uno scenario progettato da te, con previsione scritta prima dell'esecuzione e risultati anche sfavorevoli.
2. Eseguire coppie di esperimenti con un modello locale: stesso modello e incidente, contesto pulito e contaminato. Salvare anche output invalidi e casi in cui il modello non cambia scelta.
3. Confrontare un caso realistico anonimizzato, autorizzato e sufficientemente rappresentativo con il modello giocattolo. Prima spiegare quali proprietà non sono trasferibili.
4. Estendere il rollback con timeout/TTL e dimostrare la gestione di modifiche concorrenti. Un TTL non risolve da solo i conflitti di proprietà.
5. Aggiungere un adattatore a un ambiente isolato soltanto dopo aver definito idempotenza, precondizioni, verifiche post-azione ed effetti irreversibili.

Il risultato più convincente da raccontare non sarà «ho tante righe di codice». Sarà una decisione del tipo: «pensavo che bastasse ripristinare il vecchio valore; un test con un'altra modifica mi ha mostrato il problema, quindi ho introdotto la verifica delle revisioni».

## Riferimenti primari

I link indicano le fonti originali consultate. Le descrizioni di AFTERSHOCK e i suoi risultati sono separati dai risultati degli autori citati. Non è stato copiato il codice dei progetti confrontati; le loro licenze non sono trasferite a questo repository.

[S1]: https://arxiv.org/abs/2406.13352 "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents"
[S2]: https://github.com/W-Akrabi/soc-agent "soc-agent repository"
[S3]: https://github.com/TaoLi-NYU/Agentic-Incident-Response-ESORICS26 "Agentic Incident Response through Multiscale Planning with a Digital Twin — artifacts"
[S4]: https://doi.org/10.1007/s44163-026-02058-6 "Kizhakel e Pande, 2026, CIPHER-A"
[S5]: https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction "Microsoft — Compensating Transaction Pattern"
[S6]: https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/ "AWS — Ensuring rollback safety during deployments"
[S7]: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ "OWASP — Excessive Agency"
[S8]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html "OWASP — LLM Prompt Injection Prevention"
[S9]: https://www.accenture.com/it-it/careers/jobdetails?id=R00284999_it "Accenture — Cyber Defense Expert"
[S10]: https://docs.ollama.com/capabilities/structured-outputs "Ollama — Structured Outputs"

Ulteriori riferimenti tecnici: [repository originale AgentDojo](https://github.com/ethz-spylab/agentdojo), [API chat Ollama](https://docs.ollama.com/api/chat), [AWS safe deployments](https://aws.amazon.com/it/builders-library/automating-safe-hands-off-deployments/).
