from . import *


class PlayerBot(Bot):
    def play_round(self):
        page_sequence = [
            Instructions,
            InstructionsWaitForAll,
            Understanding,
            UnderstandingWaitForAll,
            GroupRole,
            DecisionTaking,
            EstimationReportingByTaker,
            DecisionReporting,
            DecisionWaitForAll,
            Questionnaire,
            Final,
        ]
        yield Instructions
        yield Submission(Understanding, timeout_happened=True, check_html=False)
        yield GroupRole
        if self.group.active:
            if self.player.taker:
                yield Submission(DecisionTaking, timeout_happened=True)
                yield Submission(EstimationReportingByTaker, timeout_happened=True)
            else:
                yield Submission(DecisionReporting, timeout_happened=True)
        yield Submission(Questionnaire, timeout_happened=True)
        yield Final

