from assgn3ClauseStructures import *
import sys
# Shea Slade
# sds266
# 11235049

def proveLiterals(goals, proof):
    """
    Purpose: Accepts a list of Literals as an argument and proves the literal
    Preconditions:
        :param goals: List of goals (Literals)
        :param proof: clauses used in proof
    :return: 'False' if not proven, 'True' if proven
    """
    if len(goals) == 0:
        if KB.showProof:
            print("\nClauses used :\n")
            for cl in proof:
                print(cl)
            #return True
        print("yes", end="")
        c = input()
        if c == ';':
            return False
        else:
            return True
    (goal, st) = goals.pop(0)
    for g in st:
        if g.equals(goal):
            return False

    for choicePoint in [clause for clause in KB.clauses if clause.head.equals(goal)]:
        if proveLiterals([(literal, st + [goal]) for literal in choicePoint.body] + goals, proof + [choicePoint]):
            return True
    if len(st) > 1:
        first_goal = Literal(str(st[1])).negate()
        current_goal = Literal(str(goal))
        if first_goal.equals(current_goal):
            if KB.showProof:
                print("\nClauses used :\n")
                for cl in proof:
                    print(cl)
            print("Proved by Rule NA")
            print("yes\n", end="")
            return True

    return False


def isExit(str):
    """
    Purpose: Determines if the exit command was invoked
    Preconditions:
        :param str: A string
    :return: A boolean: 'True' if the exit command was evoked, 'False' otherwise
    """
    return str.strip() == "exit."


def runProgram():
    """
    Purpose: Initialize and run the Theorem Prover
    :return: Return 'True' if Literal is proven, and 'False' otherwise
    """
    version = "v0.1"
    theoremProver = "A Little Logic Theorem Prover"
    #print("\n" + ("*" * 27), "\n*** %s %s ***" % (theoremProver, version), "\n" + ("*" * 27))
    print("\n%s %s " %(theoremProver, version))
    print("To exit the program type: exit.\n")


    # Infinite loop asking for goals to prove, which exits when the user types 'exit.'
    while True:
        g = Literal("goal")
        q = input("|-? ")
        i = len(KB.clauses)

        if isExit(q):
            # print("\n" + ("*" * 52), "\n*%s %s*: session terminated by user..." % (theoremProver, version),
            #       "\n" + ("*" * 52))
            sys.exit()

        if KB.isShowProof(q):
            KB.showProof = True
            print("yes")
            continue
        if KB.isNotShowProof(q):
            KB.showProof = False
            print("yes")
            continue

        KB.clauses.append(Clause(g, Body(q)))
        if not proveLiterals([(g, [])], []):
            print("no")
        del KB.clauses[i:len(KB.clauses)]


if __name__ == '__main__':

    clausesFile = "clauses.txt"

    # Set up command line launching option. If no args, run next section.
    # Add instructions to display for program launch
    if len(sys.argv) >= 2:
        KB = KnowledgeBase(sys.argv[1])
    elif len(sys.argv) == 1:
        print("\n" + "*"*74, "\nSyntax to run the Theorem Prover from the command line is:")
        print("<pythonx.x> assign1Main.py <nameOfTextFile>\n")
        print("example:\npython3 assign2Main.py clauses.txt")
        print("\nThe program will load", clausesFile, "as a default, unless argument presented.")
        print("*"*74, "\n")

        # Creates a KnowledgeBase, reads the file of clauses, prints them and prompts the user for a goal
        KB = KnowledgeBase(clausesFile)
    runProgram()
