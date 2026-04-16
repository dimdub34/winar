# ======================================================================================================================
#
# Scale Choices
#
# ======================================================================================================================
def get_scale_action():
    return [
        [-2, "Not at all"],
        [-1, "-1"],
        [0, "Moderately"],
        [1, "1"],
        [2, "A great deal"]
    ]


def get_scale_policy():
    return [
        [-2, "Strongly oppose"],
        [-1, "Somewhat oppose"],
        [0, "Neither support nor oppose"],
        [1, "Somewhat support"],
        [2, "Strongly support"]
    ]


def get_scale_certainty():
    return [
        [-2, "Very uncertain"],
        [-1, "Uncertain"],
        [1, "Certain"],
        [2, "Very certain"],
    ]


def get_scale_frequency_info():
    return [
        [5, "Daily"],
        [4, "Twice per week"],
        [3, "Once per week"],
        [2, "Twice per month"],
        [1, "Once per month"],
        [0, "Never"]
    ]


def get_scale_expectations():
    return [
        [-2, "Very unlikely"],
        [-1, "Somewhat unlikely"],
        [1, "Somewhat likely"],
        [2, "Very likely"]
    ]


def get_scale_agreement():
    return [
        [-2, "Strongly disagree"],
        [-1, "Somewhat disagree"],
        [0, "Neither agree nor disagree"],
        [1, "Somewhat agree"],
        [2, "Strongly agree"]
    ]


def get_scale_income():
    return [
        [0, "From 0$ to 1250$"],
        [1, "From 1250$ to 2000$"],
        [2, "From 2000$ to 4000$"],
        [3, "From 4000$ to 6000$"],
        [4, "From 6000$ to 8000$"],
        [5, "From 8000$ to 12,500$"],
        [6, "More than 12,500$"],
        [999, "I prefer not to say"]
    ]


def get_scale_education():
    return [
        [0, "Primary or lower secondary education"],
        [1, "Upper secondary education"],
        [2, "Non-university post-secondary education"],
        [3, "Undergraduate education (bachelor)"],
        [4, "Postgraduate education (Master or PhD)"],
        [999, "I prefer not to say"]
    ]


def get_options_bdm():
    return [
        ['A', 'Option A'],
        ['B', 'Option B']
    ]


# ======================================================================================================================
#
# DYNAMIC CHOICES METHODS
#
# ======================================================================================================================
def climate_exists_choices(player):
    return [
        [True, "Yes"],
        [False, "No"]
    ]


def policy_fight_choices(player):
    return [
        [1, "Yes"],
        [0, "No"],
        [-1, "I don't know/I do not want to answer"]
    ]


def expectations_policy_household_choices(player):
    return [
        [-2, "Lose a lot"],
        [-1, "Lose"],
        [0, "Neither win or lose"],
        [1, "Win"],
        [2, "Win a lot"],
    ]


def agreement_policy_choices(player):
    return get_scale_policy()


def climate_knowledge_choices(player):
    return [
        [0, "Not at all"],
        [1, "A little"],
        [2, "Moderately"],
        [3, "A lot"],
        [4, "A great deal"]
    ]


def info_freq_choices(player):
    return get_scale_frequency_info()


def climate_info_freq_choices(player):
    return get_scale_frequency_info()


def climate_threat_choices(player):
    return [
        [3, "Very serious threat"],
        [2, "Somewhat serious threat"],
        [1, "Not a threat at all"],
        [0, "Don't know"]
    ]


def limit_flying_choices(player): return get_scale_action()


def limit_driving_choices(player): return get_scale_action()


def electric_vehicle_choices(player): return get_scale_action()


def limit_beef_choices(player): return get_scale_action()


def limit_heating_choices(player): return get_scale_action()


def tax_flying_choices(player): return get_scale_policy()


def tax_fossil_choices(player): return get_scale_policy()


def ban_polluting_choices(player): return get_scale_policy()


def subsidy_lowcarbon_choices(player): return get_scale_policy()


def climate_fund_choices(player): return get_scale_policy()


def expectations_droughts_choices(player): return get_scale_expectations()


def expectations_eruptions_choices(player): return get_scale_expectations()


def expectations_sea_choices(player): return get_scale_expectations()


def expectations_agriculture_choices(player): return get_scale_expectations()


def expectations_living_choices(player): return get_scale_expectations()


def expectations_migration_choices(player): return get_scale_expectations()


def expectations_conflicts_choices(player): return get_scale_expectations()


def expectations_extinction_choices(player): return get_scale_expectations()


def expectations_policy_economy_choices(player): return get_scale_agreement()


def expectations_policy_cc_choices(player): return get_scale_agreement()


def income_choices(player): return get_scale_income()


def education_choices(player): return get_scale_education()


def choice_1_choices(player): return get_options_bdm()


def choice_2_choices(player): return get_options_bdm()


def choice_3_choices(player): return get_options_bdm()


def choice_4_choices(player): return get_options_bdm()


def choice_5_choices(player): return get_options_bdm()


def choice_6_choices(player): return get_options_bdm()


def choice_7_choices(player): return get_options_bdm()


# ======================================================================================================================
#
# FIELDS LABELS
#
# ======================================================================================================================
class Lexicon:
    climate_exists_label = "Do you think climate change is a real phenomenon?"
    narrative_elicitation_label = (
        "In your opinion, what explains the facts described in the text before (such as the reported rise in "
        "global temperatures and more extreme weather events)? <br><br>"
        "Please describe the <b>causes</b> of the facts attributed to climate change, and <b>explain</b> "
        "how these causes contribute to these facts and might be connected to each other.  <br><br> "
        "Explain your reasoning in full sentences. "
        "There is no good or wrong answer, respond according to your sincere and personal opinion. <br> "
        "[min. 50 words]")
    narrative_confidence_label = (
        "On a scale from 0 (very unconfident) to 100 (very confident), how confident are you about the explanation "
        "you provided in the previous question?")
    confidence_policy_label = (
        "On a scale from 0 (very unconfident) to 100 (very confident), how confident are you about the answer you "
        "provided in the previous question on what measures and solutions your government should consider to fight "
        "climate change?")
    policy_fight_label = "In your opinion, do you think your country should fight climate change?"
    policy_narrative_label = "Why?"
    expectations_policy_economy_label = "The solution I mentioned would have a positive effect on my country's economy and employment."
    expectations_policy_cc_label = "The solution I mentioned would help limit and/or mitigate the consequences of climate change."
    expectations_policy_household_label = "My household will win or lose financially from the solution I mentioned."
    agreement_policy_label = "Do you support or oppose the solution you provided?"
    climate_knowledge_label = "How knowledgeable do you consider yourself about climate change?"
    rank_coal_label = "Rank of Coal-fired power station"
    rank_gas_label = "Rank of Gas-fired power plant"
    rank_nuclear_label = "Rank of Nuclear power plant"
    info_freq_label = (
        "Over the past 3 months, how often did you acquire information and/or news? <br> For information and "
        "news we refer to national, international, and regional/local news, as well as other news facts.")
    use_tv_label = "Television (e.g., national news, cable news)"
    use_newspapers_label = "Printed Newspapers"
    use_radio_label = "Radio or podcasts"
    use_social_label = "Social media platforms"
    use_online_label = "News media websites or apps"
    use_newsletters_label = "Newsletters or email subscriptions"
    climate_info_freq_label = (
        "Over the past 3 months, how often did you acquire information and/or news about <b>climate change</b>? <br>"
        "For information and news we refer to national, international, and regional/local news, as well as other news facts.")
    use_tv_climate_label = "Television (e.g., national news, cable news)"
    use_newspapers_climate_label = "Printed Newspapers"
    use_radio_climate_label = "Radio or podcasts"
    use_social_climate_label = "Social media platforms"
    use_online_climate_label = "News media websites or apps"
    use_newsletters_climate_label = "Newsletters or email subscriptions"
    climate_threat_label = "Do you think climate change will be a threat to people in your country in the next 20 years?"
    expectations_droughts_label = "Severe droughts and heatwaves"
    expectations_eruptions_label = "More frequent volcanic eruptions"
    expectations_sea_label = "Rising sea levels"
    expectations_agriculture_label = "Lower agricultural production"
    expectations_living_label = "Drop in standards of living"
    expectations_migration_label = "Larger migration flows"
    expectations_conflicts_label = "More armed conflicts"
    expectations_extinction_label = "Extinction of humankind"
    limit_flying_label = "Limit flying"
    limit_driving_label = "Limit driving"
    electric_vehicle_label = "Have an electric vehicle"
    limit_beef_label = "Limit beef consumption"
    limit_heating_label = "Limit heating or cooling your home"
    income_label = (
        "Thinking about your household, what would you estimate is its total net monthly "
        "income on average (after taxes and deductions)? <br> Please include salaries, pensions, family allowances, "
        "unemployment benefits, or any other regular income.")
    education_label = "What is the highest education level that you have achieved?"

    @staticmethod
    def _get_field_label(field_name):
        content = getattr(Lexicon, f"{field_name}_label", None)
        if content:
            return content
        return f"Label for '{field_name}' not found"

    @staticmethod
    def get_fields_labels(field_names: list):
        fields_labels = dict()
        for field in field_names:
            fields_labels[field] = Lexicon._get_field_label(field)
        return fields_labels
