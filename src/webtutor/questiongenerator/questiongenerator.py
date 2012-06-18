from abc import ABCMeta, abstractmethod
from webtutor.random import seed

class QuestionGenerator(object):
    '''
    Abstract base class for *QuestionGenerator classes. These classes generate randomized questions given some input parameters.
    '''

    __metaclass__ = ABCMeta

    def __init__(self, titles=None, bodies=None, answers=None,
                 explanations=None, questionID=0,
                 language='en', randomSeed=None):
        '''
        Constructor.
        Note that bodies
            Input:
            titles       = Titles of the questions, i.e. 'Chain rule', 'Fundamental Theorem of Calculus'.
            bodies       = Bodies of the questions, typically the text that precedes the answers options.
            answers      = The correct answers.
            explanations = Explanations of the answers. Typically appears after the question has been answered.
            questionID   = Starting question ID. Gets incremented each time after a question is generated.
            randomSeed   = The seed used for the random number generator.
        '''
        self.titles = titles
        self.bodies = bodies
        self.answers = answers
        self.explanations = explanations
        self.questionID = questionID
        self.language = language
        self.randomSeed = randomSeed
        if self.randomSeed is not None:
            seed(self.randomSeed)

    def __repr__(self):
        return '''Question titles: {titles!r}
Question bodies: {bodies!r}
Correct answers: {answers!r}
Explanations: {explanations!r}
Question ID: {questionID!r}
Language: {language!r}
Random Seed: {randomSeed!r}'''.format(**self.__dict__)

    @abstractmethod
    def getNextQuestion(self):
        '''
        Generates a new question, and returns it as a Question object. Then increments questionID.
        '''
        pass
    
    