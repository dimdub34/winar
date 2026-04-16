def get_understanding(parameters):
    understanding = [
        dict(
            question="What happens if the Red Player steals ECU from the passive group?",
            propositions=[
                f"The Red Player earns {parameters['STEALING_AMOUNT']} ECU, and the passive group "
                f"loses {parameters['STEALING_LOSS']} ECU.",
                f"The Red Player earns {parameters['STEALING_LOSS']} ECU, and the passive group "
                f"loses {parameters['STEALING_AMOUNT']} ECU.",
                f"The Red Player earns {parameters['STEALING_PENALTY']} ECU, and the passive group "
                f"loses {parameters['REPORTING_COST']} ECU.",
            ],
            solution=0
        ),
        dict(
            question="What happens if the Red Player has stolen ECU and the selected Blue Player reports the Red Player?",
            propositions=[
                f"If the Red player is penalized, they pay a penalty of {parameters['STEALING_PENALTY']} ECU. "
                f"The Blue Player pays a reporting cost of {parameters['REPORTING_COST']} ECU.",
                f"If the Red player is penalized, they pay a penalty of {parameters['STEALING_PENALTY']} ECU. "
                f"The Blue Player pays a reporting cost of {parameters['REPORTING_COST']} ECU and receives "
                f"a reward of {parameters['REPORTING_REWARD']} ECU.",
                "If the Red player is not penalized, the Blue Player pays no reporting cost.",
            ],
            solution=1 if parameters['reward'] else 0,
        ),
        dict(
            question="What happens if one Blue Player reports the Red player and the other Blue player does not?",
            propositions=[
                "Both decisions are implemented.",
                "The Red Player is automatically penalized.",
                "The computer program randomly selects one Blue Player's decision to implement.",
            ],
            solution=2
        ),
    ]

    for i, q in enumerate(understanding, start=1):
        q["question_id"] = i
    return understanding
