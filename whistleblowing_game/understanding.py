def get_understanding(parameters, language_code):
    _ = lambda s: s[language_code] if language_code in s else s["en"]

    print(parameters)

    understanding = [
        dict(
            question=_(
                dict(
                    en="What happens if the Red Player steals ECU from the passive group?",
                    fr="Que se passe-t-il si le joueur Rouge vole des ECU au groupe passif ?",
                )),
            propositions=[
                _(dict(
                    en=f"The Red Player earns {parameters['STEALING_AMOUNT']} ECU, and the passive group "
                       f"loses {parameters['STEALING_LOSS']} ECU.",
                    fr=f"Le joueur Rouge gagne {parameters['STEALING_AMOUNT']} ECU, et le groupe passif "
                       f"perd {parameters['STEALING_LOSS']} ECU.",
                )),
                _(dict(
                    en=f"The Red Player earns {parameters['STEALING_LOSS']} ECU, and the passive group "
                       f"loses {parameters['STEALING_AMOUNT']} ECU.",
                    fr=f"Le joueur Rouge gagne {parameters['STEALING_LOSS']} ECU, et le groupe passif "
                       f"perd {parameters['STEALING_AMOUNT']} ECU.",
                )),
                _(dict(
                    en=f"The Red Player earns {parameters['STEALING_PENALTY']} ECU, and the passive group "
                       f"loses {parameters['REPORTING_COST']} ECU.",
                    fr=f"Le joueur Rouge gagne {parameters['STEALING_PENALTY']} ECU, et le groupe passif "
                       f"perd {parameters['REPORTING_COST']} ECU.",
                )),
            ],
            solution=0
        ),
        dict(
            question=_(dict(
                en="What happens if the Red Player has stolen ECU and the selected Blue Player reports the Red Player?",
                fr="Que se passe-t-il si le joueur Rouge a volé des ECU et que le joueur Bleu sélectionné signale le joueur Rouge ?",
            )),
            propositions=[
                _(dict(
                    en=f"If the Red player is penalized, they pay a penalty of {parameters['STEALING_PENALTY']} ECU. "
                       f"The Blue Player pays a reporting cost of {parameters['REPORTING_COST']} ECU.",
                    fr=f"Si le joueur Rouge est pénalisé, il paie une pénalité de {parameters['STEALING_PENALTY']} ECU. "
                       f"Le joueur Bleu paie un coût de signalement de {parameters['REPORTING_COST']} ECU."
                )),
                _(dict(
                    en=f"If the Red player is penalized, they pay a penalty of {parameters['STEALING_PENALTY']} ECU. "
                       f"The Blue Player pays a reporting cost of {parameters['REPORTING_COST']} ECU and receives "
                       f"a reward of {parameters['REPORTING_REWARD']} ECU.",
                    fr=f"Si le joueur Rouge est pénalisé, il paie une pénalité de {parameters['STEALING_PENALTY']} ECU. "
                       f"Le joueur Bleu paie un coût de signalement de {parameters['REPORTING_COST']} ECU et "
                       f"reçoit une récompense de {parameters['REPORTING_REWARD']} ECU."
                )),
                _(dict(
                    en=f"If the Red player is not penalized, the Blue Player pays no reporting cost.",
                    fr=f"Si le joueur Rouge n'est pas pénalisé le joueur Bleu ne paie aucun coût de signalement."
                )),
            ],
            solution=1 if parameters['reward'] else 0,
        ),
        dict(
            question=_(dict(
                en="What happens if one Blue Player reports the Red player and the other Blue player does not?",
                fr="Que se passe-t-il si un joueur Bleu signale le joueur Rouge et que l'autre joueur Bleu ne le signale pas ?",
            )),
            propositions=[
                _(dict(
                    en="Both decisions are implemented.",
                    fr="Les deux décisions sont mises en œuvre.",
                )),
                _(dict(
                    en="The Red Player is automatically penalized.",
                    fr="Le joueur Rouge est automatiquement pénalisé.",
                )),
                _(dict(
                    en="The computer program randomly selects one Blue Player’s decision to implement.",
                    fr="Le programme informatique sélectionne au hasard la décision d'un joueur Bleu à mettre en œuvre.",
                )),
            ],
            solution=2
        ),
    ]

    for i, q in enumerate(understanding, start=1):
        q["question_id"] = i
    return understanding
