from webtutor.random import seed, sample
from webtutor import Question

class QuestionGenerator(object):
    '''
    Base class for *QuestionGenerator classes. These classes generate randomized questions given some input parameters.
    '''


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
        # These are things that can vary when a new question is selected.
        # For example, a new question will always have a predictable ID,
        # or language, but these will be chosen fresh each iteration.
        self.choices = [self.titles, self.bodies, self.answers, self.explanations]
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

    def _getQChoices(self):
        # Make sure everything is either length 1, or the same length.
        lengths = [len(x) for x in self.choices]
        maxLength = 1
        for l in lengths:
            if l == 1 or l == maxLength:
                continue
            elif l != maxLength:
                if maxLength == 1:
                    maxLength = l
                else: # This means maxLength is not 1, and l is not 1 or the same as maxLength
                    raise ValueError('Lists are inconsistent lengths.')
        for i in range(len(self.choices)):
            c = self.choices[i]
            if len(c) == 1:
                self.choices[i] = [c[0] for x in range(maxLength)]
        self.qChoices = zip(*self.choices)
        return self.qChoices
                

    def getNextQuestion(self):
        '''
        Generates a new question, and returns it as a Question object. Then increments questionID.
        '''
        q = Question()
        self._getQChoices()
        c = sample(self.qChoices)
        q.title = c[0]
        q.body = c[1]
        q.answer = c[2]
        q.explanation = c[3]
        q.id = self.questionID
        self.questionID += 1
        return q
    
    
if __name__ == '__main__':
    n = 10
    titles = ['Title %s' % i for i in range(1)]
    bodies = ['Body %s' % i for i in range(n)]
    answers = ['Answer %s' % i for i in range(n)]
    explanations = ['Explanation %s' % i for i in range(1)]
    qgen = QuestionGenerator(titles, bodies, answers, explanations, 42, 'en', 24)
    for i in range(20):
        print qgen.getNextQuestion(), '\n'
    
    