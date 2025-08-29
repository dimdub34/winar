def get_understanding(parameters:dict):
    understanding = [
        dict(
            question="What happens if the Red Player steals ECU from the passive group?",
            propositions=[f"The Red Player earns {parameters['STEALING_AMOUNT']} ECU, and the passive group "
                          f"loses {parameters['STEALING_LOSS']} ECU.",
                          f"The Red Player earns {parameters['STEALING_LOSS']} ECU, and the passive group "
                          f"loses {parameters['STEALING_AMOUNT']} ECU.",
                          f"The Red Player earns {parameters['STEALING_PENALTY']} ECU, and the passive group "
                          f"loses {parameters['REPORTING_COST']} ECU.",
                          "There is no change in anyone’s earnings."
                          ],
            solution=0
        ),
        dict(
            question="What are the consequences if a Blue Player reports the Red Player, and the Red Player has stolen ECU?",
            propositions=[
                f"If the Red player is penalized, he/she pays a penalty of {parameters['STEALING_PENALTY']} ECU, "
                f"and the Blue Player pays a reporting cost of {parameters['REPORTING_COST']} ECU.",
                f"If the Red player is penalized, he/she pays a penalty of {parameters['STEALING_PENALTY']} ECU, "
                f"the Blue Player pays a reporting cost of {parameters['REPORTING_COST']} ECU and receives "
                f"a reward of {parameters['REPORTING_REWARD']} ECU.",
                f"If the Red player is penalized, he/she pays a penalty of {parameters['STEALING_PENALTY']} ECU, "
                f"and the Blue Player pays no reporting cost."
            ],
            solution=1 if parameters['reward'] else 0,
        ),
        dict(
            question="What happens if one Blue Player reports the Red player and the other Blue player does not?",
            propositions=[
                "Both decisions are implemented.",
                "The Red Player is automatically penalized.",
                "The computer program randomly selects one Blue Player’s decision to implement.",
            ],
            solution=2
        ),
        dict(
            question="If the Red Player does not steal ECU, no one incurs additional costs, even if the "
                     "Blue Players decide to report.",
            propositions=[
                "True",
                "False"
            ],
            solution=0,
        ),
    ]

    for i, q in enumerate(understanding):
        q["question_id"] = i + 1

    return understanding
