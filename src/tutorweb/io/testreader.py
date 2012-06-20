from mcquestionreader import MCQuestionReader
from testwriter import TestWriter
from tutorweb import MCQuestion
from numpy import random
import re

class TestReader(MCQuestionReader):
    
    @staticmethod
    def _questionsFromLines(lines):
        qLines = []
        questions = []
        # Read lines until the end of a question, at which point
        # process the question, and then empty the qLines list
        for line in lines:
            if line.startswith(r'\item'):
                line = line[5:] # Remove the '\item'
                if len(qLines) != 0:
                    question = TestReader._questionFromLines(qLines)
                    questions.append(question)
                qLines = []
            qLines.append(line)
        # Get the last question
        question = TestReader._questionFromLines(qLines)
        questions.append(question)
        return questions
    
    @staticmethod
    def _questionFromLines(lines):
        answer = [0]
        ansOptPat = re.compile(r'^[a-z]\) (?P<opt>.+)')
        ansOpts = []
        body = ''
        for line in lines:
            line = line.strip()
            m_ansOpt = ansOptPat.search(line)
            if m_ansOpt is not None:
                ansOpt = m_ansOpt.group('opt')
                ansOpts.append(ansOpt)
            else:
                if not re.match('\s+', line) and line != '':
                    body += line.rstrip('\n') + '\n'
        body = body[:-1]
        question = MCQuestion(answerOptions=ansOpts, body=body, answer=answer)
        return question
        
if __name__ == '__main__':
    l = '\n\n-------\n\n'
    reader = TestReader('./outputs/staehluti_lok.tex')
    questions = reader.readAllQuestions()
    for j in range(5):
        writer = TestWriter(outFile=('./outputs/staehluti_lok%s.tex' % j))
        for question in questions:
            question.shuffle()
        random.shuffle(questions)
        writer.writeQuestionsToFile(questions)
        with open(('svor%s' % j), 'w') as outFile:
            for i in range(1,1+len(questions)):
                question = questions[i-1]
                ans = question.answer[0]
                numeral = writer.numerals[ans]
                outFile.write('{}. {}\n'.format(i, numeral))
    