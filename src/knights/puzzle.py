from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
puzzle0_Asays = And(AKnight, AKnave)
knowledge0 = And(
    Implication(AKnight, puzzle0_Asays),
    Implication(AKnave, Not(puzzle0_Asays)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
puzzle1_Asays = And(AKnave, BKnave)
# puzzle1_Bsays = None
knowledge1 = And(
    Implication(AKnight, puzzle1_Asays),
    Implication(AKnave, Not(puzzle1_Asays)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
puzzle2_Asays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
puzzle2_Bsays = Not(puzzle2_Asays)
knowledge2 = And(
    Implication(AKnight, puzzle2_Asays),
    Implication(AKnave, Not(puzzle2_Asays)),
    Implication(BKnight, puzzle2_Bsays),
    Implication(BKnave, Not(puzzle2_Bsays)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
puzzle3_Asays1 = AKnight
puzzle3_Asays2 = AKnave
puzzle3_Asays = And(
    Or(         # only say one sentence, means that either says part1 or part2
    And(Implication(AKnight, puzzle3_Asays1), Implication(AKnave, Not(puzzle3_Asays1))),    # saying part1
    And(Implication(AKnight, puzzle3_Asays2), Implication(AKnave, Not(puzzle3_Asays2)))     # saying part2
    ),
    Not(And(    # not saying two cases, means that can not say two parts at the same time
    And(Implication(AKnight, puzzle3_Asays1), Implication(AKnave, Not(puzzle3_Asays1))),    # saying part1
    And(Implication(AKnight, puzzle3_Asays2), Implication(AKnave, Not(puzzle3_Asays2)))     # saying part2
    ))
)
puzzle3_Bsays = And(
    Implication(BKnight, And(Implication(AKnight, puzzle3_Asays1), Implication(AKnave, Not(puzzle3_Asays1)))),
    Implication(BKnave, Not(And(Implication(AKnight, puzzle3_Asays1), Implication(AKnave, Not(puzzle3_Asays1))))),
    CKnave
)
puzzle3_Csays = AKnight
knowledge3 = And(
    Implication(AKnight, puzzle3_Asays),
    Implication(AKnave, Not(puzzle3_Asays)),
    Implication(BKnight, puzzle3_Bsays),
    Implication(BKnave, Not(puzzle3_Bsays)),
    Implication(BKnight, puzzle3_Csays),
    Implication(BKnave, Not(puzzle3_Csays)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")
    # print(knowledge3.formula())

if __name__ == "__main__":
    main()
