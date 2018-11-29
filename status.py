class status:
    def __init__(self, ball=0, strike=0, out=0, scoreDiff=0, first=False, second=False, third=False, prevBatter=None):
        self.ball = ball
        self.strike = strike
        self.out = out
        self.scoreDiff = scoreDiff
        self.first = first
        self.second = second
        self.third = third
        self.prevBatter = prevBatter
    def clear(self):
        self.ball = 0
        self.strike = 0
        self.out = 0
        self.scoreDiff = 0
        self.first = False
        self.second = False
        self.third = False
        self.prevBatter = None
    def newInning(self):
        self.ball = 0
        self.strike = 0
        self.out = 0
        self.first = False
        self.second = False
        self.third = False
        self.prevBatter = None
    def newBatter(self):
        self.ball = 0
        self.strike = 0
    def update(self, ball=0, strike=0, out=0, scoreDiff=0, first=False, second=False, third=False, prevBatter=None):
        self.ball = ball
        self.strike = strike
        self.out = out
        self.scoreDiff = scoreDiff
        self.first = first
        self.second = second
        self.third = third
        self.prevBatter = prevBatter
    def duplicateStatus(self):
        return status(self.ball,self.strike,self.out,self.scoreDiff,self.first,self.second,self.third,self.prevBatter)
    def __repr__(self):
        return 'Score:{} Outs:{} First:{} Second:{} Third:{} Count:{}{}'.format(self.scoreDiff,self.out,self.first,self.second,self.third,self.ball,self.strike)
    