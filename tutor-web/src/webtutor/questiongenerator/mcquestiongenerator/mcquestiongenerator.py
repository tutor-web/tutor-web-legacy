from __future__ import division, print_function
from webtutor.questiongenerator import QuestionGenerator
from webtutor.random import sample
from webtutor import MCQuestion, MCQuestionWriter
from numpy import random
import codecs

class MCQuestionGenerator(QuestionGenerator):
    '''
    Multiple Choice Question Generator.
    '''


    def __init__(self, wrongAnswers=None, numCorrect=1, useNAC=False,
                 relativeFreqNAC={'normal':0, 'AOTA':1, 'NOTA':1, 'combo':0},
                 numComboAnswers=2, msgNAC=None, numAnsOptions=3,
                 extraAnswerNAC=True, **kwargs):
        '''
        Constructor:
            Input -
                titles          = Title of the question, i.e. 'Chain rule', 'Fundamental Theorem of Calculus'.
                qBody           = Body of the questions, typically the text that precedes the answers options.
                answers         = A list of correct answers.
                explanations    = An explanations of the answers. Typically appears after the question has been answered.
                questionID      = Starting question ID. Gets incremented each time after a question is generated.
                randomSeed      = The seed used for the random number generator.
                wrongAnswers    = A list of wrong answers.
                numCorrect      = The number of correct answers to include when generating a question.
                useNAC          = Specifies whether to produce NOTA (None of the Above), AOTA (All of the Above), 
                                    and Combo (any combination of 2 or more answers (e.g. 'a) and c) are true')) 
                                    when generating a question.
                relativeFreqNAC = Specifies the relative frequency of the occurrence of AOTA, NOTA, and Combo answers,
                                    when generating a question, defaults to {'normal':0, 'AOTA':1, 'NOTA':1, 'combo':0}, 
                                    i.e., by default, if AOTA/NOTA/Combo is activated, only AOTA/NOTA questions will appear. 
                                    For example, if it is set to {'normal':2, 'AOTA':3, 'NOTA':1, 'combo':4}, 
                                    then AOTA will appear 3 times as often as NOTA, 1.5 times as often as Normal, etc.
                numComboAnswers = Set the number of answers in a Combo answers, (default 2). 
                                    If set to 0, a Combo answers is replaced with NOTA. 
                                    If set to n, where n is the number of answers not including the Combo answers, 
                                    then it is replaced with AOTA
                msgNAC          = Specifies the messages for NOTA, AOTA and Combo answers, defaults to the specified language. 
                                    Changing this does not change the language of the generator. 
                                    For example: 
                                    QGen.msgNAC = {'NOTA':'None correct', 'AOTA':'All correct', 'combo':'{0} and {1} correct'}.
                numAnsOptions   = Specify how many answers options there are, defaults to 3.
                extraAnswerNAC  = Specifies if AOTA/NOTA/Combo appears as an extra answers option, defaults to true. 
                                    For example, if MCQuestionGenerator is set to display 3 answers options and generates 
                                    an AOTA/NOTA/Combo question, it would display 4 answers options including the AOTA/NOTA/Combo
                                     answers if this is set to true, and 3 answers options including the AOTA/NOTA/Combo answers
                                      if this is set to false

        '''
        super(MCQuestionGenerator, self).__init__(**kwargs)
        self.wrongAnswers = wrongAnswers
        self.numCorrect = numCorrect
        self.useNAC = useNAC
        self.relativeFreqNAC = relativeFreqNAC
        self.numComboAnswers = numComboAnswers
        self.msgNAC = msgNAC
        self.numAnsOptions = numAnsOptions
        self.extraAnswerNAC = extraAnswerNAC
        # Set the NAC message
        if self.msgNAC is not None:
            self.NOTAtext  = self.msgNAC['NOTA']
            self.AOTAtext  = self.msgNAC['AOTA']
            self.comboText = self.msgNAC['combo']
        else:
            with codecs.open("./"+self.language+"/AOTA.txt", encoding='utf-8') as AOTAfile,\
                 codecs.open("./"+self.language+"/NOTA.txt", encoding='utf-8') as NOTAfile,\
                 codecs.open("./"+self.language+"/combo.txt", encoding='utf-8') as comboFile:
                self.AOTAtext  = AOTAfile.read()
                self.NOTAtext  = NOTAfile.read()
                self.comboText = comboFile.read()
        # Set the NAC relative frequencies
        self.normalFreq = self.relativeFreqNAC['normal']
        self.AOTAFreq   = self.relativeFreqNAC['AOTA']
        self.NOTAFreq   = self.relativeFreqNAC['NOTA']
        self.comboFreq  = self.relativeFreqNAC['combo']
        # Get the number of questions
        if self.titles is not None:
            self.nQuestions = len(self.titles)
        else:
            self.nQuestions = 0
        # Make sure everything is the same length
        for qList in [self.titles, self.bodies, self.answers, self.explanations, self.wrongAnswers]:
            if qList is not None:
                try:
                    assert(self.nQuestions == len(qList))
                except AssertionError:
                    print('This list is the wrong size:\n\t', qList)
                    raise
        

    def __repr__(self):
        return super(MCQuestionGenerator, self).__repr__() +\
            '''
Wrong answers: {wrongAnswers!r}
Number of correct answers: {numCorrect!r}
Using NOTA/AOTA/Combo: {useNAC!r}
Relative frequency of NAC:
\t Normal: {normalFreq!r}
\t AOTA: {AOTAFreq!r}
\t NOTA: {NOTAFreq!r}
\t Combo: {comboFreq!r}
Number of answers in a combo answer: {numComboAnswers!r}
Text in NAC answers:
\t AOTA: {AOTAtext!r}
\t NOTA: {NOTAtext!r}
\t Combo: {comboText!r}
Number of answer options: {numAnsOptions!r}
NAC appears as an extra answer: {extraAnswerNAC!r}'''.format(**self.__dict__)

    def _makeNormalQuestion(self, nQ):
        nWrong = self.numAnsOptions - self.numCorrect
        # Answer Options = [Wrong Answers] + [Correct Answers]
        wAns = sample(self.wrongAnswers[nQ], size=nWrong)
        cAns = sample(self.answers[nQ], size=self.numCorrect)
        # The correct answers always appear first
        ansOpts = cAns + wAns
        self._nextQuestion.answerOptions = ansOpts
        self._nextQuestion.answer = range(self.numCorrect)
        return self._nextQuestion
    
    def _makeXOTAQuestion(self, nQ, qType):
        nAnsOpts = self.numAnsOptions
        if self.extraAnswerNAC:
            nAnsOpts += 1
        if qType=='AOTA':
                ansList = self.answers[nQ]
                ansText = self.AOTAtext
        elif qType=='NOTA':
            ansList = self.answers[nQ]
            ansText = self.NOTAtext
        else:
            raise ValueError('qType must be one of "NOTA" or "AOTA"')
        # Decide if the XOTA option is the correct answer
        cAnsIndex = random.randint(nAnsOpts)
        # If the correct answer is not the last answer, then
        # the question is a 'normal' question with an extra
        # option at the end
        if cAnsIndex != nAnsOpts - 1:
            # Temporarily modify self.numAnsOptions so
            # _makeNormalQuestion does not make the wrong
            # number of options
            nAnsOptsCopy = self.numAnsOptions
            self.numAnsOptions = nAnsOpts - 1
            question = self._makeNormalQuestion(nQ)
            self.numAnsOptions = nAnsOptsCopy
            question.answerOptions += [ansText]
            return question
        else:  #If the last answer is correct, then XOTA option is correct
            nAns = nAnsOpts - 1
            ansOpts = sample(ansList, size=nAns)
            ansOpts += [ansText]
            self._nextQuestion.answerOptions = ansOpts
            # AOTA/NOTA is the last answer option
            self._nextQuestion.answer = [len(ansOpts) - 1]
            return self._nextQuestion
    
    def _makeAOTAQuestion(self, nQ):
        return self._makeXOTAQuestion(nQ, 'AOTA')
    
    def _makeNOTAQuestion(self, nQ):
        return self._makeXOTAQuestion(nQ, 'NOTA')
    

    def _getComboAnsText(self, cAnsIndices):
        # Get all the answers except the last one
        ansText0 = '{ansOpt%s}' % cAnsIndices[0]
        for i in cAnsIndices[1:-1]:
            ansText0 += ', {ansOpt%s}' % i # Everything except first and last
        ansText1 = '{ansOpt%s}' % cAnsIndices[-1] # Last one
        ansText = self.comboText.format(ansText0, ansText1)
        return ansText

    def _makeComboQuestion(self, nQ):
        nAnsOpts = self.numAnsOptions
        if self.extraAnswerNAC:
            nAnsOpts += 1
        cAnsIndex = random.randint(nAnsOpts)
        # If the correct answer is not the last answer, then
        # the question is a 'normal' question with an extra
        # option at the end
        if cAnsIndex != nAnsOpts - 1:
            # Temporarily modify self.numAnsOptions so
            # _makeNormalQuestion does not make the wrong
            # number of options
            nAnsOptsCopy = self.numAnsOptions
            self.numAnsOptions = nAnsOpts - 1
            question = self._makeNormalQuestion(nQ)
            self.numAnsOptions = nAnsOptsCopy
            # Modify the answer text to indicate random options
            ansOptIndices = sample(range(nAnsOpts-1), self.numComboAnswers)
            ansOptIndices.sort()
            ansText = self._getComboAnsText(ansOptIndices)
            question.answerOptions += [ansText]
            return question
        nAns = nAnsOpts - 1
        nWAns = nAns - self.numComboAnswers
        cAns = sample(self.answers[nQ], self.numComboAnswers)
        wAns = sample(self.wrongAnswers[nQ], nWAns)
        ansOpts = cAns + wAns
        # Shuffle the answer options, keep track of the correct answers
        ansOptsIndices = range(len(ansOpts))
        random.shuffle(ansOptsIndices)
        cAnsIndices = []
        # Find the correct answer indices, they are the first len(cAns) items
        for i in range(len(cAns)):
            cAnsIndices += [ansOptsIndices.index(i)]
        cAnsIndices.sort()
        # Shuffle the answers according to ansOptsIndices
        ansOptsShuffled = list(ansOpts) # Make a copy
        for i in range(len(ansOptsIndices)):
            ansOptsShuffled[i] = ansOpts[ansOptsIndices[i]]
        ansOpts = ansOptsShuffled
        # Modify the answer text to indicate where the correct answers are
        ansText = self._getComboAnsText(cAnsIndices)
        ansOpts += [ansText]
        self._nextQuestion.answerOptions = ansOpts
        self._nextQuestion.answer = [len(ansOpts) - 1]
        return self._nextQuestion

    def _makeQuestion(self, nQ, qType='normal'):
        self._nextQuestion = MCQuestion(ID=self.questionID, title=self.titles[nQ], 
                                  body=self.bodies[nQ], 
                                  explanation=self.explanations[nQ])
        if qType == 'normal':
            return self._makeNormalQuestion(nQ)
        elif qType == 'AOTA':
            return self._makeAOTAQuestion(nQ)
        elif qType == 'NOTA':
            return self._makeNOTAQuestion(nQ)
        elif qType == 'combo':
            return self._makeComboQuestion(nQ)
        else:
            raise ValueError('qType must be one of: "normal", "combo", "NOTA", "AOTA"')

    def getNextQuestion(self):
        # Decide what question set to use
        nQ = random.random_integers(self.nQuestions-1)
        # Decide what kind of question to make
        if self.useNAC:
            # Choose one of AOTA, NOTA, combo or normal based on their frequencies
            freqs = [self.AOTAFreq, self.NOTAFreq, self.comboFreq, self.normalFreq]
            nacToUse = sample(['AOTA', 'NOTA', 'combo', 'normal'], p=freqs)[0]
            question = self._makeQuestion(nQ, qType=nacToUse)
        else:
            question = self._makeQuestion(nQ)
        self.questionID += 1
        return question


if __name__ == '__main__':
    genStrList = lambda txt,n: ['%s %s' % (txt,i+1) for i in range(n)]    
    nQ = 5 # Number of different questions to generate
    nAns = 10 # Number of correct answers to generate
    nWAns = 20 # Number of incorrect answers to generate
    mcQGenOptions = dict(titles = genStrList('Title',nQ), 
                         bodies = genStrList('Bodies',nQ),
                         answers = [genStrList('Correct %s' % (i+1), nAns) for i in range(nQ)],
                         wrongAnswers = [genStrList('Wrong %s' % (i+1), nWAns) for i in range(nQ)],
                         explanations = genStrList('Explanation',nQ),
                         extraAnswerNAC = True,
                         questionID = 42,
                         language = 'is',
                         randomSeed = 4,
                         numCorrect = 2,
                         useNAC = True,
                         relativeFreqNAC = {'normal':0,'NOTA':0,'AOTA':0,'combo':1},
                         numComboAnswers = 3,
                         numAnsOptions = 5)
    mcQGen = MCQuestionGenerator(**mcQGenOptions)
    writer = MCQuestionWriter(outFile='./mcqgentest', fileFormat='latex', ansOptFormat='a)')
    writer.clearFile()
    for i in range(15):
        writer.addQuestionToFile(mcQGen.getNextQuestion())
    
    