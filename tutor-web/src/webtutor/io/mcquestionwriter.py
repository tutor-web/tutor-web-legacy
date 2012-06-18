import codecs
       
class MCQuestionWriter(object):
    numeralMap = dict(zip(('a', 'A', '1'),
                    [[chr(i+97) for i in range(26)],
                     [chr(i+65) for i in range(26)],
                     [str(i+1) for i in range(26)]]))
    
    ansOptList = ['ansOpt%s' % i for i in range(26)]
    
    def __init__( self, outFile='./questions', fileFormat='latex', ansOptFormat='a)' ):
        if not (outFile.endswith('.tex') or outFile.endswith('.txt')):
            if fileFormat == 'latex':
                self.outFile = outFile + ".tex"
            elif fileFormat == 'text':
                self.outFile = outFile + ".txt"
            else:
                raise ValueError('fileFormat must be one of "latex" or "text"')
        self.outFile = outFile
        self.fileFormat = fileFormat
        numerals = MCQuestionWriter.numeralMap[ansOptFormat[0]]
        self.numerals = [num + ansOptFormat[1] for num in numerals]
        self.ansOptNumMap = dict(zip(self.ansOptList, self.numerals))
        
    def questionToString(self, question):
        qOpts = ""
        for i in range(len(question.answerOptions)):
            qOpts += self.numerals[i][0]
            if i in question.answer:
                qOpts += ".true"
            elif i not in question.answer:
                qOpts += ".false"
            qOpts += self.numerals[i][1]
            try:
                optText = question.answerOptions[i].format(**self.ansOptNumMap)
            except (KeyError, IndexError): # This probably means the answer contains LaTeX
                optText = question.answerOptions[i]
            qOpts += " {}\n\n".format(optText)
        qOpts = qOpts[:-2] # Get rid of the trailing newlines
        return '''%ID Qgen-q{id}
%title Qgen-q{id} {title}
%format {format}

{body}

{qOpts}

%Explanation
{explanation}

%==='''.format(format=self.fileFormat, qOpts=qOpts, **question.__dict__)

    def writeQuestionToFile(self, question):
        with codecs.open(self.outFile, mode='w', encoding='utf-8') as outFile:
            outFile.write(self.questionToString(question)+"\n")
            
    def addQuestionToFile(self, question):
        with codecs.open(self.outFile, mode='a', encoding='utf-8') as outFile:
            outFile.write(self.questionToString(question)+"\n")
    
    def writeQuestionsToFile(self, questions):
        with codecs.open(self.outFile, mode='w', encoding='utf-8') as outFile:
            for question in questions:
                outFile.write(self.questionToString(question)+"\n")
    
    def addQuestionsToFile(self, questions):
        with codecs.open(self.outFile, mode='a', encoding='utf-8') as outFile:
            for question in questions:
                outFile.write(self.questionToString(question)+"\n")

    def clearFile(self):
        with codecs.open(self.outFile, mode='w', encoding='utf-8') as outFile:
            pass

