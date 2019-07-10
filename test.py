from parse import *

def testCase(play, eOuts, eFirst, eSecond, eThird, eScoreDiff):
    #takes in a play and tests the result 
    gameStatus.clear()
    detailedLine = play.split(',')
    pRes = parseAtBat(detailedLine[1:])
    print(play)
    if (gameStatus.out != eOuts):
        print("Outs:",gameStatus.out, "Expected outs:", eOuts)
        raise AssertionError("Outs do not match")
    elif (gameStatus.first != eFirst):
        print("first:",gameStatus.first, "Expected first:", eFirst)
        raise AssertionError("First does not match")
    elif (gameStatus.second != eSecond):
        print("second:",gameStatus.second, "Expected second:", eSecond)
        raise AssertionError("second does not match")
    elif (gameStatus.third != eThird):
        print("third:",gameStatus.third, "Expected third:", eThird)
        raise AssertionError("third does not match")
    elif (gameStatus.scoreDiff != eScoreDiff):
        print("scoreDiff:",gameStatus.scoreDiff, "Expected scoreDiff:", eScoreDiff)
        raise AssertionError("scoreDiff does not match")
    else:
        print("Test passed\n")

def testInning(plays):
    gameStatus.clear()
    for atBat in plays.split():
        detailedLine = atBat.strip().split(',')
        if(detailedLine[0] != 'play'):continue
        pRes = parseAtBat(detailedLine[1:])
        print(atBat)
        print(gameStatus)
        for p in pRes:
            print(p.toDict())

print('tests strikeout')
ex = 'play,1,0,schwk001,22,BCBFFFS,K'
testCase(ex,eOuts=1,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests double play')
ex = 'play,7,0,backw001,11,FBX,64(1)3/GDP/G6'
testCase(ex,eOuts=2,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests double play where batter is specified')
ex = 'play,7,0,leonj001,01,CX,8(B)84(2)/LDP/L8'
testCase(ex,eOuts=2,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests batter out where a runner progresses')
ex = 'play,7,1,tempg001,00,X,54(B)/BG25/SH.1-2'
testCase(ex,eOuts=1,eFirst=False,eSecond=True,eThird=False,eScoreDiff=0)

print('tests triple play')
ex = 'play,7,1,randw001,00,.>X,1(B)16(2)63(1)/LTP/L1'
testCase(ex,eOuts=3,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests caught stealing where a runner progresses')
ex = 'play,1,0,bayld001,??,,CS2(24).2-3'
testCase(ex,eOuts=1,eFirst=False,eSecond=False,eThird=True,eScoreDiff=0)

print('tests caught stealing where error allow runner to reach safely')
ex = 'play,6,0,beneb001,??,,CS2(2E4).1-3'
testCase(ex,eOuts=0,eFirst=False,eSecond=False,eThird=True,eScoreDiff=0)

print('tests defensive indifference')
ex = 'play,9,0,bencj101,??,,DI.1-2'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=0)

print('tests runner picked off')
ex = 'play,4,0,guerp001,00,22,PO2(14)'
testCase(ex,eOuts=1,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests runner picked off caught stealing')
ex = 'play,6,1,javis001,10,B1,POCS2(1361)'
testCase(ex,eOuts=1,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests batter tagged out at base not normally covered by fielder')
ex = 'play,7,1,tempg001,00,X,54(B)/BG25/SH.1-2'
testCase(ex,eOuts=1,eFirst=False,eSecond=True,eThird=False,eScoreDiff=0)

print('tests 1b runner being forced out. Allows batter to first and runner scores')
ex = 'play,5,0,gileb001,10,BX,54(1)/FO/G5.3-H;B-1'
testCase(ex,eOuts=1,eFirst=True,eSecond=False,eThird=False,eScoreDiff=-1)

print('tests single')
ex = 'play,8,0,pacit001,??,,S7'
testCase(ex,eOuts=0,eFirst=True,eSecond=False,eThird=False,eScoreDiff=0)

print('tests bases loaded clearing double')
ex = 'play,2,1,santn001,12,CFBX,D7/G5.3-H;2-H;1-H'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=3)

print('tests triple with runner on second')
ex = 'play,3,0,raint001,11,CBX,T9/F9LD.2-H'
testCase(ex,eOuts=0,eFirst=False,eSecond=False,eThird=True,eScoreDiff=-1)

print('tests ground rule double with runner scoring')
ex = 'play,3,0,surhb001,10,.BX,DGR/L9LS.2-H'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=-1)

print('tests solo home run')
ex = 'play,8,0,bellg001,21,CBBX,H/L7D'
testCase(ex,eOuts=0,eFirst=False,eSecond=False,eThird=False,eScoreDiff=-1)

print('tests 3 run homerun')
ex = 'play,12,1,bichd001,02,FFFX,HR/F78XD.2-H;1-H'
testCase(ex,eOuts=0,eFirst=False,eSecond=False,eThird=False,eScoreDiff=3)

print('tests inside the park hr')
ex = 'play,4,0,younr001,32,FBFFFBBX,HR9/F9LS.3-H;1-H'
testCase(ex,eOuts=0,eFirst=False,eSecond=False,eThird=False,eScoreDiff=-3)

print('tests error on foul. no changes')
ex = 'play,5,0,murre001,00,F,FLE5/P5F'
testCase(ex,eOuts=0,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests hit by pitch')
ex = 'play,1,1,lansc001,00,H,HP.1-2'
testCase(ex,eOuts=0,eFirst=True,eSecond=True,eThird=False,eScoreDiff=0)

print('tests intentional walk')
ex = 'play,8,0,sciom001,30,B+22.III,IW'
testCase(ex,eOuts=0,eFirst=True,eSecond=False,eThird=False,eScoreDiff=0)

print('tests catchers interference')
ex = 'play,9,1,cruzj002,??,,C/E2.1-2'
testCase(ex,eOuts=0,eFirst=True,eSecond=True,eThird=False,eScoreDiff=0)

print('tests Fielders choice with one out at home. batter is safe')
ex = 'play,4,0,harpb001,22,BBFSFX,FC5/G5.3XH(52)'
testCase(ex,eOuts=1,eFirst=True,eSecond=False,eThird=False,eScoreDiff=0)

print('tests Fielders choice with no outs')
ex = 'play,5,1,jordr001,00,X,FC3/G3S.3-H;1-2'
testCase(ex,eOuts=0,eFirst=True,eSecond=True,eThird=False,eScoreDiff=1)

print('tests force out with batter not implicitly stated')
ex = 'play,2,1,leons001,11,BCX,54(1)/FO/G.3-H;2-3'
testCase(ex,eOuts=1,eFirst=True,eSecond=False,eThird=True,eScoreDiff=1)

print('tests strikeout + runner put out at second')
ex = 'play,4,1,stubf001,32,CBFBBFFS,K/DP.1X2(26)'
testCase(ex,eOuts=2,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests single + throwing error to third. no outs')
ex = 'play,7,0,puckk001,01,CX,S5/G5.1-3(E5/TH)'
testCase(ex,eOuts=0,eFirst=True,eSecond=False,eThird=True,eScoreDiff=0)

print('tests single where batter makes it to second due to throwing error. 2 runs score')
ex = 'play,3,0,fielc001,00,X,S7/L7LD.3-H;2-H;BX2(7E4)'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=-2)

print('tests strikeout where wild pitch leads to batter safe at first')
ex = 'play,13,1,bradj001,22,BCFBS,K+WP.B-1'
testCase(ex,eOuts=0,eFirst=True,eSecond=False,eThird=False,eScoreDiff=0)

print('tests double play where batter is not mentioned')
ex = 'play,6,1,benia002,12,*BSFX,72(3)5(2)/GDP'
testCase(ex,eOuts=2,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests throwing error causing batter to first')
ex = 'play,1,0,gardb001,01,CX,4E1/G'
testCase(ex,eOuts=0,eFirst=True,eSecond=False,eThird=False,eScoreDiff=0)

print('tests stolen base 1st to second')
ex = 'play,6,0,benzt001,11,BSB,SB2'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=0)

print('tests double stolen base no score')
ex = 'play,4,1,waltj001,10,BB,SB3;SB2'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=True,eScoreDiff=0)

print('tests double stolen base with score')
ex = 'play,4,1,shefg001,12,SP1CB,SBH;SB2'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=1)

print('test double play with error. throw out at home. no score')
ex = 'play,1,1,shawt001,00,X,43/G/NDP.1XH(72)(E3/TH)'
testCase(ex,eOuts=2,eFirst=False,eSecond=False,eThird=False,eScoreDiff=0)

print('tests double steal. one unearned run')
ex = 'play,3,1,gereb001,11,BC>B,SBH;SB2.3-H(UR)'
testCase(ex,eOuts=0,eFirst=False,eSecond=True,eThird=False,eScoreDiff=1)

# print('Groundout: 3B/Forceout at 3B; Calderon Scores/Adv on E5 (throw to 1B)/Safe on E2 (catch)/unER; Fisk to 3B')
# ex = 'play,6,0,fiskc001,11,CBX,5(2)/FO/G5.1XH(E5/TH1)(9E2)(UR);B-3'
# testCase(ex,eOuts=1,eFirst=False,eSecond=False,eThird=True,eScoreDiff=1)

print('Reached on E9 (Fly Ball); Rivera out at Hm/RF-3B-SS-C/Adv on E4 (throw to 3B); Grissom to 3B/Adv on throw to Hm')
ex = 'play,9,1,grism001,10,.BX,E9/F.1XH(9562)(E4/TH3);B-3(THH)'
testCase(ex,eOuts=1,eFirst=False,eSecond=False,eThird=True,eScoreDiff=0)

print('test inning')
ex = '''id,SFN200305270
version,2
info,visteam,ARI
info,hometeam,SFN
info,site,SFO03
info,date,2003/05/27
info,number,0
info,starttime,7:15PM
info,daynight,night
info,usedh,false
info,umphome,hirsj901
info,ump1b,bellw901
info,ump2b,welkb901
info,ump3b,danlk901
info,howscored,park
info,pitches,pitches
info,temp,67
info,winddir,tocf
info,windspeed,21
info,fieldcond,unknown
info,precip,unknown
info,sky,sunny
info,timeofgame,232
info,attendance,36693
info,wp,rodrf002
info,lp,mantm001
info,save,
start,womat001,"Tony Womack",0,1,6
start,cinta001,"Alex Cintron",0,2,5
start,gonzl001,"Luis Gonzalez",0,3,7
start,delld001,"David Dellucci",0,4,9
start,gracm001,"Mark Grace",0,5,3
start,spivj001,"Junior Spivey",0,6,4
start,finls001,"Steve Finley",0,7,8
start,barar001,"Rod Barajas",0,8,2
start,kim-b001,"Byung-Hyun Kim",0,9,1
start,grism001,"Marquis Grissom",1,1,8
start,peren001,"Neifi Perez (Diaz)",1,2,6
start,durhr001,"Ray Durham",1,3,4
start,bondb001,"Barry Bonds",1,4,7
start,santb001,"Benito Santiago",1,5,2
start,snowj001,"J.T. Snow",1,6,3
start,alfoe001,"Edgardo Alfonzo",1,7,5
start,cruzj004,"Jose Cruz",1,8,9
start,schmj001,"Jason Schmidt",1,9,1
play,1,0,womat001,02,CFX,43/G
play,1,0,cinta001,32,CBBFBFX,8/F
play,1,0,gonzl001,32,FBFBBFFX,8/F
play,1,1,grism001,32,BCBFBS,K
play,1,1,peren001,00,X,9/F
play,1,1,durhr001,02,CFC,K
play,2,0,delld001,31,CBBBX,T8/F
play,2,0,gracm001,01,CX,3/G
play,2,0,spivj001,12,BFFB,WP.3-H
play,2,0,spivj001,22,BFFB.S,K
play,2,0,finls001,32,FBFBBFB,W
play,2,0,barar001,11,1CBX,8/F
play,2,1,bondb001,22,BFFBC,K
play,2,1,santb001,00,X,S8/L
play,2,1,snowj001,12,BCCX,S8/L.1-2
play,2,1,alfoe001,22,BSCBX,4/P
play,2,1,cruzj004,31,BBBCB,W.2-3;1-2
play,2,1,schmj001,11,BCX,46(1)/FO/G
play,3,0,kim-b001,00,X,S8/G
play,3,0,womat001,01,LX,6(1)3/GDP
play,3,0,cinta001,11,CBX,HR/8/F
play,3,0,gonzl001,10,BX,43/G
play,3,1,grism001,11,BSX,43/G
play,3,1,peren001,01,CX,6/P
play,3,1,durhr001,02,CSFX,43/G
play,4,0,delld001,32,CSBBBFS,K
play,4,0,gracm001,02,FFX,14!3/G
play,4,0,spivj001,22,SBFBS,K
play,4,1,bondb001,00,X,8/F
play,4,1,santb001,32,BBCFBFFB,W
play,4,1,snowj001,12,CFFBC,K
play,4,1,alfoe001,11,BSX,6/L
play,5,0,finls001,12,BFFFS,K
play,5,0,barar001,02,FSFS,K
play,5,0,kim-b001,11,CBX,43/G
play,5,1,cruzj004,32,BFBSFBX,S9/L
play,5,1,schmj001,11,BLX,3/SH/BG.1-2
play,5,1,grism001,12,FBCC,K
play,5,1,peren001,21,BBFX,S9/G.2-H
play,5,1,durhr001,32,BCBB1C>C,K
play,6,0,womat001,22,BBFFX,53/G
play,6,0,cinta001,11,BCX,3/G-
play,6,0,gonzl001,02,CSFX,6/L-
play,6,1,bondb001,02,FCFX,4/P
play,6,1,santb001,01,CX,4/P
play,6,1,snowj001,31,SBBBB,W
play,6,1,alfoe001,10,BX,43/G
play,7,0,delld001,00,X,31/G
play,7,0,gracm001,00,X,3/P
play,7,0,spivj001,32,BBBCCS,K
play,7,1,cruzj004,02,SSFX,S7/L-
play,7,1,schmj001,00,X,34/SH/BG.1-2
play,7,1,grism001,22,CCBBX,13/G+
play,7,1,peren001,00,X,5/P5F
play,8,0,finls001,32,BCBBCX,8/F
play,8,0,barar001,12,CFBX,6/P
play,8,0,kim-b001,00,,NP
sub,baerc001,"Carlos Baerga",0,9,11
play,8,0,baerc001,10,.BX,3!1/G
play,8,1,durhr001,00,,NP
sub,myerm001,"Mike Myers",0,9,1
play,8,1,durhr001,10,.BX,S6/G
play,8,1,bondb001,31,BB1FBB,W.1-2
play,8,1,santb001,00,,NP
sub,koplm001,"Mike Koplove",0,9,1
play,8,1,santb001,00,.X,64(1)/FO/G-.2-3;B-1
play,8,1,snowj001,10,BX,7/SF.3-H
play,8,1,alfoe001,01,CX,64(1)/FO/G
play,9,0,womat001,32,BBBCCFX,5/P5F
play,9,0,cinta001,12,BCFX,31/G
play,9,0,gonzl001,00,H,HP
play,9,0,delld001,10,BX,4!3/G+
play,9,1,cruzj004,00,,NP
sub,mccrq001,"Quinton McCracken",0,3,7
com,"Diamondbacks Luis Gonzalez left the game due to an injured leg"
play,9,1,cruzj004,22,.SBSBS,K
play,9,1,schmj001,00,,NP
sub,galaa001,"Andres Galarraga",1,9,11
play,9,1,galaa001,10,.BX,E6/G+
play,9,1,grism001,00,,NP
sub,river002,"Ruben Rivera (Moreno)",1,9,12
play,9,1,grism001,10,.BX,E9/F.1XH(9562)(E4/TH3);B-3(THH)
com,"$Ruben Rivera had touched 2B and started back to 1B; he"
com,"ran across the infield when the ball was dropped and"
com,"then ran back to touch 2B again; he was nearly thrown"
com,"out at 3B but the throw bounced off Cintron's glove"
play,9,1,peren001,12,BSFFS,K
play,10,0,gracm001,00,,NP
sub,worrt002,"Tim Worrell",1,9,1
play,10,0,gracm001,32,.BBCCBFC,K
play,10,0,spivj001,22,BCCBX,9/F
play,10,0,finls001,22,FBCBFX,43/G
play,10,1,durhr001,00,,NP
sub,orope001,"Eddie Oropesa",0,9,1
play,10,1,durhr001,00,.X,63/G
play,10,1,bondb001,30,BBBB,W
play,10,1,santb001,00,,NP
sub,cinta001,"Alex Cintron",0,2,4
play,10,1,santb001,00,,NP
sub,villo001,"Oscar Villarreal",0,6,1
play,10,1,santb001,00,,NP
sub,willm003,"Matt Williams",0,9,5
play,10,1,santb001,01,...FX,46(1)3/GDP
play,11,0,barar001,20,BBX,6/P
play,11,0,willm003,32,SBFBFBFX,S8/F-
play,11,0,womat001,10,BX,2/P2F
play,11,0,cinta001,00,B,WP.1-2
play,11,0,cinta001,20,B.BX,43/G
play,11,1,snowj001,10,BX,9/F
play,11,1,alfoe001,12,BFCX,8/F
play,11,1,cruzj004,12,BCFS,K
play,12,0,mccrq001,00,,NP
sub,rodrf002,"Felix Rodriguez",1,7,1
play,12,0,mccrq001,00,,NP
sub,felip001,"Pedro Feliz",1,9,5
play,12,0,mccrq001,00,..X,43/G
play,12,0,delld001,22,CBFBC,K
play,12,0,gracm001,00,X,6/P
play,12,1,felip001,01,CX,D7/L+
play,12,1,grism001,01,CX,S8/L.2-3
play,12,1,peren001,31,BBBCX,43/G.1-2
play,12,1,durhr001,02,CFFS,K
play,12,1,bondb001,30,IIII,IW
play,12,1,santb001,00,X,8/L
play,13,0,villo001,00,,NP
sub,bautd001,"Danny Bautista",0,6,11
play,13,0,bautd001,21,.BCBX,13/G
play,13,0,finls001,02,SFX,S8/F-
play,13,0,barar001,22,1BCBFX,9/F
play,13,0,willm003,00,1X,D7/L.1-H
play,13,0,womat001,00,X,63/G
play,13,1,snowj001,00,,NP
sub,mantm001,"Matt Mantei",0,6,1
play,13,1,snowj001,22,.FCBFBFC,K
play,13,1,rodrf002,00,,NP
sub,aurir001,"Rich Aurilia",1,7,11
play,13,1,aurir001,32,.BSCBBB,W
play,13,1,cruzj004,12,BCSFS,K
play,13,1,felip001,31,BBFB>B,W.1-2
play,13,1,grism001,21,FB+1BX,T9/F.2-H;1-H'''
# testInning(ex)
