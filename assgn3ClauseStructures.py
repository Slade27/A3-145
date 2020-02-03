import re
# Shea Slade
# sds266
# 11235049

class Literal:
    def __init__(self, str):
        """
        Purpose: Constructor for the Literal Object
        Preconditions:
            :param str: A string representing a literal value
        Postconditions:
            A Literal object is created by breaking the string into its atomic parts
        """
        self.sign = self.parseSign(str)
        self.atom = self.parseAtom(str)

    def __str__(self):
        """
        Purpose: Allows python's native print functionality to print this object
        :return: a formatted string version of the Literal object to print
        """
        return self.toString()

    def toString(self):
        """
        Purpose: Creates a string representation of the object
        :return: a formatted string version of the Literal object
        """
        return str(self.sign) + str(self.atom)

    def equals(self, lit):
        """
        Purpose: Determines whether two literals are equal
        Preconditions:
            :param lit: A literal to check
        :return: A boolean: 'True' if they are equal, 'False' if they are not
        """
        return self.sign == lit.sign and self.atom == lit.atom

    def isTrue(self):
        """
        Purpose: Determines whether the literal is true
        :return: A boolean: 'True' if the literal is true, 'False' otherwise
        """
        return self.sign == "" and self.atom == "true"

    def copy(self):
        """
        Purpose: Creates a copy of itself
        :return: A new exact copy of the original Literal object
        """
        return Literal(self.sign + self.atom)

    def negate(self):
        """
        Purpose: Negates the Literal
        :return: The literal as a negative of itself
        """
        if self.sign == '~':
            self.sign = ''
        else:
            self.sign = '~'
        return self

    def parseSign(self, str):
        """
        Purpose: Accepts a string argument and determines whether the Literal is a negation
        Preconditions:
            :param str: A string representing a Literal
        :return: '~' if a negation is found, '' otherwise
        """
        if str.strip()[0] == '~':
            return '~'
        else:
            return ''

    def parseAtom(self, str):
        """
        Purpose: Accepts a string as an argument and returns the Atomic value of the Literal
        Preconditions:
            :param str: A string representing a literal
        :return: The atomic value of the literal
        """
        s = str.strip()
        if s[0] != '~':
            return re.search("[a-z][a-zA-Z0-9_]*", str.strip()).group()
        else:
            return self.parseAtom(s[1:len(s)])

    def notTrue(lit):
        """
        Purpose: Determines if the Literal object is not true
        Preconditions:
            :param lit: A Literal object to test
        :return: A boolean: 'False' if the literal is true or negative, 'True' otherwise
        """
        return lit.sign != "" or lit.atom != "true"


class Body(list):
    def __init__(self, inp, strType=True):
        """
        Purpose: Constructor for the Body Object inheriting from list. A list of literals.
        Preconditions:
            :param str: A string representing a body
        Postconditions:
            A Body object is created. A List of Literals.
        """
        super().__init__()
        if strType:
            literals = inp.split(",")
            for literal in literals:
                self.append(Literal(literal.strip()))
        else:
            for literal in inp:
                self.append(literal.copy())

    def __str__(self):
        """
        Purpose: Allows python's native print functionality to print this object
        :return: a formatted string version of the Body object to print
        """
        return self.toString()

    def toString(self):
        """
        Purpose: Creates a string representation of the object
        :return: a formatted string version of the Body object
        """
        stringList = []
        for literal in self:
            stringList.append(str(literal))
        return ','.join(stringList)


class Clause:
    def __init__(self, head, body):
        """
        Purpose: A Constructor for a Clause object
        Preconditions:
            :param head: A Literal object representing the head of the clause
            :param body: A Body object representing the body of the clause
        Postconditions:
            Creates a Clause object with the provided head and body
        """
        self.head = head
        self.body = body

    def __str__(self):
        """
        Purpose: Allows python's native print functionality to print this object
        :return: a formatted string version of the Clause object to print
        """
        return self.toString()

    def toString(self):
        """
        Purpose: Creates a string representation of the object
        :return: a formatted string version of the Body object
        """
        build_string = ''
        if self.head.atom != 'true':
            build_string += str(self.head)
            if len(self.body) > 0:
                if self.body[0].atom != 'true':
                    build_string += " <- "
                    build_string += str(self.body)
            build_string += '.'
        return build_string


class KnowledgeBase(object):
    """
    A Class representing a KnowledgeBase of Clauses
    """
    def __init__(self, filename):
        """
        Purpose: A Construct to initialize the Knowledgebase for this theorem
        Preconditions:
            :param filename: A text file with clauses
        Postconditions:
            Creates a KnowledgeBase object and prints the Knowledgebase clauses to the console
        """
        super().__init__()
        self.clauses = [Clause(Literal('true'), [])]
        self.filename = filename
        self.showProof = False

        self.readClauses(filename)
        self.printClauses()

    def __str__(self):
        """
        Purpose: Allows python's native print functionality to print this object
        :return: A string representation of the Knowledgebase Object
        """
        return self.toString()

    def toString(self):
        """
        Purpose: Returns a string representation of the KnowledgeBase object
        :return: A String representation of the KnowledgeBase object
        """
        return 'Filename: ' + str(self.filename) + '\nShowProof: ' + str(self.showProof) + '\n'.join([str(clause) for clause in self.clauses]) + '\n'

    def createClause(self, clause, body=None):
        """
        Purpose: Accepts a string representation of a Clause and creates and returns a Clause object
        Preconditions:
            :param clause: A string representation of a Clause object
        :return: A Clause object created from the string argument repesenting a clause
        """
        ##print(clause)
        if body is None:
            headAndBody = clause.strip().split("<-")
            headLiteral = Literal(headAndBody[0])
            if len(headAndBody) == 1:
                bodyLiterals = Body("true")
            else:
                bodyLiterals = Body(headAndBody[1])
            return Clause(headLiteral, bodyLiterals)
        else:
            return Clause(clause, body)

    def addClause(self, clause, body=None):
        """
        Purpose: Will create a clause, and add that clause to the knowledgebase (KB)
        Preconditions:
            :param clause: A string representation of a clause
        Postconditions:
            Will create a Clause object from the argument, and add that clause to the KB
        """
        # KB should be a special object maybe inheriting from list
        if body is None:
            self.clauses.append(self.createClause(clause))
        else:
            self.clauses.append(self.createClause(clause, body))

    def printClauses(self):
        """
        Purpose: Will accept a Clause object as an argument to print to the console
        Preconditions:
            :param Clauses: A Clause Object
        Postconditions:
            Prints a string representation of the clause object to the console
        """
        print("\n" + "*" * 34, "\n***Knowledgebase Read From File***", "\n" + "*" * 34)
        for clause in self.clauses:
            if clause.body:
                print(clause)

    def readClauses(self, filename):
        """
        Purpose: Reads a text file full of clauses and parses it into clauses
        Preconditions:
            :param filename: The filename to read
        Postconditions: Adds all of the read clauses into the KnowledgeBase object
        """
        f = open(filename, "r")
        string = f.read()
        clauses = string.split(".")
        clauses.pop()  # the preceding split operation always leaves an empty list at the end
        for strClause in clauses:
            clause = self.createClause(strClause)
            self.addClause(strClause)
            self.assertAllContrapositives(clause)

    def assertAllContrapositives(self, clause):
        """
        Purpose: Adds all contrapositives to the Knowledgebase
        Preconditions:
            :param clause: A Clause object
        Postconditions: The contrapositive of the clause argument is added to the Knowledgebase
        """

        new_head = Literal(clause.head.toString()).negate()
        new_body = Body(clause.body.toString())

        for literal in new_body:
            insert = Literal(literal.atom).negate()
            a_body = Body(new_body.toString().replace(literal.toString(), "~"+new_head.atom))

            ##contra = Clause(insert, a_body)
            self.addClause(insert, a_body)
            ##print(contra)





    def isShowProof(self, str):
        """
        Purpose: Returns a boolean representing whether the showproof. command was invoked
        :param str: a string representing the possible showproof. command
        :return: 'True' if showproof. was invoked by the user, 'False' otherwise.
        """
        return str.strip() == "showproof."

    def isNotShowProof(self, str):
        """
        Purpose: Returns a boolean representing whether the noshowproof. command was invoked
        :param str: a string representing the possible noshowproof. command
        :return: 'True' if noshowproof. was invoked by the user, 'False' otherwise.
        """
        return str.strip() == "noshowproof."


if __name__ == '__main__':
    # This main is currently used for basic testing and is only run if
    # classStructures0.py is run directly

    # Test Knowledgebase creation - Should print listing of knowledgebase file
    KB = KnowledgeBase('clauses.txt')

    # Test Literal Printing and Creation
    print('\n**TEST PRINT LITERALS**')
    myLiterala = Literal('~a')
    myLiteralb = Literal('b')
    print('~a', '=', myLiterala)
    print('b', '=', myLiteralb)

    # Test Body Printing and Creation
    print('\n**TEST PRINT BODY**')
    myBodya = Body('~a, b')
    myBodyb = Body('c,d')
    print('~a, b', "=", myBodya)
    print('c, d', "=", myBodyb)

    # Test Clause Printing and Creation
    print('\n**TEST PRINT CLAUSE**')
    myClausea = KB.createClause('a<-~b,c,d.')
    myClauseb = KB.createClause('~f<-b,~c,d.')
    print('\na<-~b,c,d.', '=', myClausea)
    print('~f <- b,  ~c,  d.', '=', myClauseb)