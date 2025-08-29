# Codebook : Jeu Stealing / Taking (`whgame`)

Ce document fournit un codebook en français pour l'application oTree `whgame`, simulant un jeu de prise et de dénonciation au sein d'un groupe actif, avec évaluation normative personnelle et sociale.

## Constantes principales

| Constante | Valeur | Description |
|----------|--------|-------------|
| `STEALING_AMOUNT` | 30 | Gain obtenu en volant |
| `STEALING_LOSS` | 45 | Perte subie collectivement par le groupe Passif |
| `STEALING_PENALTY` | 60 | Pénalité si audit après dénonciation |
| `REPORTING_COST` | 10 | Coût de dénonciation |
| `REPORTING_REWARD` | 45 | Récompense pour dénonciation correcte (si `reward=True`) |
| `AUDIT_PROBABILITY` | 2/3 | Probabilité d’audit en cas de dénonciation |
| `SOCIETY_OPTION_PAYOFF` | 10 | Gain potentiel si norme sociale correctement anticipée |

## Subsession

| Champ | Type | Description |
|-------|------|-------------|
| `reward` | Booléen | Si les dénonciateurs peuvent être récompensés |
| `num_of_takers` | Entier | Nombre total de voleurs (joueurs rouges) |
| `num_of_reporters` | Entier | Nombre de dénonciateurs |
| `society_opinion_majority` | Entier | Opinion majoritaire sur la norme sociale |

## Group

| Champ | Type | Description |
|-------|------|-------------|
| `active` | Booléen | Groupe actif ou passif |
| `taker_has_taken` | Booléen | Si le joueur rouge a volé |
| `selected_reporter` | Int | ID du dénonciateur sélectionné |
| `reporter_has_reported` | Booléen | Si ce dernier a dénoncé |
| `audit_draw` | Float | Résultat du tirage d’audit |
| `taker_audited` | Booléen | Si l’audit a eu lieu |

## Player

### Questions de compréhension

| Champ | Type | Description |
|-------|------|-------------|
| `understanding_faults_q1` à `q4` | Entiers | Fautes par question |
| `understanding_faults_total` | Entier | Somme des fautes |

### Décisions principales

- `taker` : Booléen indiquant si le joueur est le voleur
- `taking_decision` : Booléen, décision de voler ou non
- `estimation_reporting` : Estimation subjective (0–100) de probabilité d’être dénoncé
- `reporting_decision` : Booléen, décision de dénoncer ou non

### Audit et paiements

- `audit_draw` : tirage aléatoire (float)
- `audit` : Booléen si audité
- `payoff_ecu` : Paiement en ECU, calculé selon les règles du jeu

### Éléments qualitatifs

- `taker_motivation`, `reporter_motivation` : Justification des décisions
- `personal_opinion` : Opinion personnelle sur la norme (0–5)
- `society_opinion` : Opinion attribuée à la société (0–5)

## Pages

1. `Instructions` : Introduction
2. `Understanding` : Questionnaire de compréhension
3. `GroupRole` : Attribution des rôles (Rouge/Bleu)
4. `DecisionTaking` : Décision de voler (joueur Rouge)
5. `EstimationReportingByTaker` : Estimation de dénonciation (Rouge)
6. `DecisionReporting` : Dénonciation (joueur Bleu)
7. `Questionnaire` : Justifications et normes
8. `BeforeFinalWaitForAll` : Calcul des paiements
9. `Final` : Page finale avec feedback

---

Ce codebook est destiné à documenter le protocole de l’expérience `whgame` pour le dépôt de données ou un data paper, et faciliter la lecture des variables dans les bases extraites (par exemple via oTree export ou dumpdb).

