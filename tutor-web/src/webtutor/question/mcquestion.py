from question import Question
from numpy import random

class MCQuestion(Question):
    '''
    Multiple Choice Question.
    For this Question, the 'answer' variable should be iterable, 
    and the 'answerOptions' variable should be indexed by its contents.
    '''


    def __init__(self, answerOptions=None, **kwargs):
        '''
        Constructor:
            Input -
                answerOptions = A list of all the possible answers options.
                **kwargs      = Input arguments for the Question superclass constructor.
        '''
        super(MCQuestion, self).__init__(**kwargs)
        self.answerOptions = answerOptions
        
    def shuffle(self):
        indices = range(len(self.answerOptions))
        random.shuffle(indices)
        ansOptsShuffled = list(self.answerOptions) # Make a copy
        ansShuffled = list(self.answer)
        for i in range(len(indices)):
            ansOptsShuffled[i] = self.answerOptions[indices[i]]
        self.answerOptions = ansOptsShuffled
        for i in range(len(self.answer)):
            ansIndex = self.answer[i]
            newAnsIndex = indices.index(ansIndex)
            ansShuffled[i] = newAnsIndex
        self.answer = ansShuffled
        return self
        
    def __repr__(self):
        return super(MCQuestion, self).__repr__() +\
            '''
Answer Options: {answerOptions}'''.format(**self.__dict__)

if __name__ == '__main__':
    q = MCQuestion()
    print q