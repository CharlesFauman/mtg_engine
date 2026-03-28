# %%
# 500.1. A turn consists of five phases, in this order: beginning, precombat main, combat, postcombat
# main, and ending. Each of these phases takes place every turn, even if nothing happens during the
# phase. The beginning, combat, and ending phases are further broken down into steps, which
# proceed in order.
from enum import Enum, auto



BEGINNING = dict(name="beginning")
PRECOMBAT_MAIN = dict(name="precombat main")
COMBAT = dict(name="combat")
POSTCOMBAT_MAIN = dict(name="postcombat main")
ENDING = dict(name="ending")

turn = [BEGINNING, PRECOMBAT_MAIN, COMBAT, POSTCOMBAT_MAIN, ENDING]



# 500.2. A phase or step in which players receive priority ends when the stack is empty and all players
# pass in succession. Simply having the stack become empty doesn’t cause such a phase or step to
# end; all players have to pass in succession with the stack empty. Because of this, each player gets a
# chance to add new things to the stack before that phase or step ends.
STACK = dict(name="stack", contents=[])
PLAYERS = dict(name="players", players=[])

def end_phase_or_step_with_priority():
    assert len(STACK["contents"]) == 0
    for player in PLAYERS["players"]:
        if not player.passed:
            return False
    return True



# 500.3. A step in which no players receive priority ends when all specified actions that take place during
# that step are completed. The only such steps are the untap step (see rule 502) and certain cleanup
# steps (see rule 514).


# 500.4. As a step or phase begins, if there are effects that last until that step or phase, those effects
# expire.
def expire_effects_at_step_or_phase_start(step_or_phase):
    pass

# 500.5. As a step or phase ends, if there are effects that last until the end of that step or phase, those
# effects expire. Then any unspent mana left in a player’s mana pool empties. This is a turn-based
# action that doesn’t use the stack (see rule 703.4q).
def expire_effects_at_step_or_phase_end(step_or_phase):
    pass

# 500.5a Effects that last “until end of combat” expire at the end of the combat phase, not at the
# beginning of the end of combat step.
# 
# 500.5b Effects that last “until end of turn” are subject to special rules; see rule 514.2.
# %%
