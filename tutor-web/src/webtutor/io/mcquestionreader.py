import codecs
import re
from webtutor import MCQuestion
from mcquestionwriter import MCQuestionWriter

class MCQuestionReader(object):

    def __init__(self, inFile):
        self.fileName = inFile
        
    @staticmethod
    def stringToQuestion(inStr):
        return MCQuestionReader._questionFromLines(inStr.split('\n'))
        
    @staticmethod
    def stringToQuestions(inStr):
        return MCQuestionReader._questionsFromLines(inStr.split('\n'))
        
    @staticmethod
    def _questionsFromLines(lines):
        qLines = []
        questions = []
        # Read lines until the end of a question, at which point process the
        # question, and then empty the qLines list
        for line in lines:
            qLines.append(line)
            if line.strip() == r'%===':
                question = MCQuestionReader._questionFromLines(qLines)
                questions.append(question)
                qLines = []
        return questions

    @staticmethod
    def _questionFromLines(lines):
    # Get all the tags. Can be scattered throughout the question, not just at the head
        extra = ''
        tagPat = re.compile(r'^%(?:\s+)?(?P<tag>[^\s]+)(?:\s+)?(?P<value>.+)?')
        idPat = re.compile(r'^(?P<extra>[^\d]+)?(?P<ID>\d+)$')
        for line in lines:
            line = line.strip()
            m = tagPat.search(line)
            if m is None:
                tag = value = None
            else:
                tag = m.group('tag')
                value = m.group('value')
            if tag == 'ID':
                m_ID = idPat.search(value)
                ID = int(m_ID.group('ID'))
                extra = m_ID.group('extra') + str(ID)
            if tag == 'title':
                titlePat = re.compile(r'^(?:{})?(?:\s+)?(?P<title>.+)'.format(extra))
                m_title = titlePat.search(value)
                title = m_title.group('title')
            if tag == 'format':
                qFormat = value
        # Get the question body
        body = ''
        qOptPat = re.compile(r'^(?:[a-z]\.)(?P<correct>(true)|(false))(?:\) )(?P<content>.+)$')
        for line in lines:
            if qOptPat.search(line) is not None:
                break
            if not line.lstrip().startswith(r'%'):
                body += line + "\n"
        body = body.strip() # Get rid of leading and trailing newline
        # Get the question options
        qOptNum = 0
        qOpts = []
        qAnswers = []
        for line in lines:
            m_qOpt = qOptPat.search(line)
            if m_qOpt is not None:
                content = m_qOpt.group('content')
                qOpts.append(content)
                correct = m_qOpt.group('correct')
                if correct == 'true':
                    qAnswers.append(qOptNum)
                qOptNum += 1
        # Get the explanation
        explanation = ''
        isExplanation = False
        explStartPat = re.compile(r'^(\s+)?%(\s+)?Explanation')
        qEndPat = re.compile(r'^(\s+)?%(\s+)?===')
        for line in lines:    
            if qEndPat.search(line) is not None:
                break
            if isExplanation:
                explanation += line + "\n"  
            if explStartPat.search(line) is not None:
                isExplanation = True
        explanation = explanation.strip() # Get rid of newlines
        question = MCQuestion(answerOptions = qOpts, title=title, ID=ID, 
                              answer=qAnswers, explanation=explanation,
                              body=body)
        return question

    def readAllQuestions(self):
        with codecs.open(self.fileName, mode='r', encoding='utf-8') as inFile:
            lines = inFile.readlines()
        return self._questionsFromLines(lines)
    
if __name__ == '__main__':
    line = '\n\n-------\n\n'
    reader = MCQuestionReader('mcqgentest')
    questions= reader.readAllQuestions()
    for q in questions:
        print q,line