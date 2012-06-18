from mcquestionwriter import MCQuestionWriter


class TestWriter(MCQuestionWriter):
    
        def questionToString(self, question):
            qOpts = ""
            for i in range(len(question.answerOptions)):
                qOpts += self.numerals[i]
                optText = question.answerOptions[i]
                if i in question.answer:
                    optText += ' % CORRECT'
                qOpts += " {}\n\n".format(optText)
            return '''\\item {body}

{qOpts}'''.format(format=self.fileFormat, qOpts=qOpts, **question.__dict__)