from __future__ import division
from collections import defaultdict
from collections import Counter
import regex as re
import pandas as pd
import numpy as np
import string

class sigmorphdata:

    def __init__(self):
        self.source=defaultdict(int)
        self.target=defaultdict(int)

    def getData(filename):
        sourceTarget=defaultdict(list)
        sourceList=[]
        targetList=[]
        with open(filename) as f:
            allLines=f.readlines()
        for i,line in enumerate(allLines):
            if('# text' in line):
                line=line[9:].replace(',','').replace('.','')
                swords=re.split(r"\s+(?=[^()]*(?:\(|$))", line)
                for word in swords:
                    sourceList.append(word)
            elif('# translit' in line):
                line=line[13:].replace(',','').replace('.','')
                words=re.split(r"\s+(?=[^()]*(?:\(|$))", line)
                for word in words:
                    targetList.append(word)

        print(len(sourceList))
        print(len(targetList))
        print(len(set(sourceList)))
        print(len(set(targetList)))
        for i in range(len(sourceList)):
            sourceTarget[sourceList[i]]=[]
            sourceTarget[sourceList[i]].append(targetList[i])
            if len(sourceTarget[sourceList[i]])>1:
                print(sourceTarget[sourceList[i]])
        print(len(sourceTarget))

def main():
    sigmorphdata.getData('/home/karthik/SP19/CompLing/SigMorph/MachineTransliteration/UD_Ukrainian-IU/uk_iu-um-train.conllu')

if __name__ == "__main__":
    main()
