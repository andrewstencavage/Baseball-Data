class pitch:
    def __init__(self, ball, strike, out, scoreDiff, outcome, first, second, third, inning, winningTeam=None, id=None):
        self.ball = ball
        self.strike = strike
        self.out = out
        self.scoreDiff = scoreDiff
        self.outcome = outcome
        self.first = first
        self.second = second
        self.third = third
        self.inning = inning
        self.winningTeam = winningTeam
        self.id= id
    def toDict(self):
        data = {}
        data["ball"] = self.ball
        data["strike"] = self.strike
        data["out"] = self.out
        data["scoreDiff"] = self.scoreDiff
        data["outcome"] = self.outcome
        data["first"] = self.first
        data["second"] = self.second
        data["third"] = self.third
        data["inning"] = self.inning
        data["winningTeam"] = self.winningTeam
        data["id"] = self.id
        return data
    def __repr__(self):
        return 'B {} S {} O {} I {} sD {} 1 {} 2 {} 3 {} wt {}'.format(self.ball,self.strike,self.out,self.inning,self.scoreDiff,self.first,self.second,self.third,self.winningTeam)



#test = pitch(3,2,2,-1,"K",True,False,True,None)
#print(test.toJSON())