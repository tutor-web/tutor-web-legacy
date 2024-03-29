class Question(object):
    '''
    Base class for *Question classes. 
    *Question objects are usually generated by *QuestionGenerator objects.
    '''

    def __init__(self, ID=0, title=None, body=None, answer=None, explanation=None):
        '''
        Constructor.
        Input -
            ID          = Unique numeric ID.
            title       = Title of the question, e.g. "l'Hopital's rule".
            body        = The main question text.
            answer      = The answers to the question.
            explanation = Explanation of the answers to the question.
        '''
        self.id = ID
        self.title = title
        self.body = body
        self.answer = answer
        self.explanation = explanation

    def __repr__(self):
        return '''ID: {id}
Title: {title!r}
Body: {body!r}
Answer: {answer!r}
Explanation: {explanation!r}'''.format(**self.__dict__)
