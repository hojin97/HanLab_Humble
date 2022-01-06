import time
import numpy as np

NumOfData=300

def get_input_data(filename):
    input_file = open(filename, 'r', encoding='UTF8')
    Exercise=[]

    for line in input_file:
        line=line.replace('\n','')

        Exercise.append(line)
        #eachline = line.split(', ')  # split by unit automatically
    return Exercise

def makeEx() :

    Health = dict()

    Practice = get_input_data("데이터용_가슴.txt")
    Health['Chest'] = Practice
    Practice = get_input_data("데이터용_등.txt")
    Health['Back'] = Practice
    Practice = get_input_data("데이터용_삼두.txt")
    Health['Triceps'] = Practice
    Practice = get_input_data("데이터용_이두.txt")
    Health['Biceps'] = Practice
    Practice = get_input_data("데이터용_어깨(전체).txt")
    Health['Shoulder_T'] = Practice
    Practice = get_input_data("데이터용_어깨(전).txt")
    Health['Shoulder_F'] = Practice
    Practice = get_input_data("데이터용_어깨(측).txt")
    Health['Shoulder_S'] = Practice
    Practice = get_input_data("데이터용_어깨(후).txt")
    Health['Shoulder_B'] = Practice
    Practice = get_input_data("데이터용_하체.txt")
    Health['Leg'] = Practice

    return Health

def DoPractice(MainList,SubListA=[],SubListB=[],DetList=[]):    # subList always contians Main shoulder and target shoulder or double target shoulder
    TodayPractice=[]
    MainList=np.random.choice(MainList,4,replace=False)

    if len(DetList)!=0:
        DetList=np.random.choice(DetList,2,replace=False)

    if len(SubListA)!=0 and len(SubListB) !=0 and len(DetList)!=0:
        SubListA=np.random.choice(SubListA,2,replace=False)
        SubListB = np.random.choice(SubListB, 2, replace=False)
        DetList=np.random.choice(DetList,2,replace=False)


    for ex in MainList:
        TodayPractice.append(ex)

    for ex in SubListA:
        TodayPractice.append(ex)

    for ex in SubListB:
        TodayPractice.append(ex)

    for ex in DetList:
        TodayPractice.append(ex)

    #print(TodayPractice)
    return TodayPractice

def chooseTarget():

    Letsgo = []

    MainList = ['Chest', 'Back', 'Leg', 'Shoulder', 'Arm']
    SubList = ['Shoulder_T', 'Shoulder_F', 'Shoulder_S', 'Shoulder_B']
    DetList = ['Biceps', 'Triceps']

    MainKey = np.random.choice(MainList,1,replace=False)

    if MainKey == 'Arm':
        Letsgo = DetList
    elif MainKey == 'Shoulder':
        Letsgo = SubList
    else:   # include Main3
        M=list(MainKey)
        Letsgo.append(M)

        tmp = np.random.choice(SubList, 2, replace=False)
        for i in tmp:
            s=[]
            s.append(i)
            Letsgo.append(s)

        tmp = np.random.choice(DetList, 1, replace=False)
        d=list(tmp)
        Letsgo.append(d)

    #print(Letsgo)
    return list(Letsgo)

def generateTransaction(Health):

    total=[]
    global NumOfData
    for count in range(0, NumOfData):

        TodayList=chooseTarget()
        #print(f"today:[{len(TodayList)}]{TodayList}\n")
        if len(TodayList) == 4:   # Shoulder or Main3 is included
                if (['Chest'] in TodayList) or (['Back'] in TodayList) or (['Leg'] in TodayList):    # Main3 is included

                    for ex in TodayList:
                        if (ex == ['Chest']) or (ex == ['Back']) or (ex == ['Leg']):
                            MainList=Health[ex[0]]
                            TodayList.remove(ex)
                        elif (ex == ['Biceps']) or (ex == ['Triceps']):
                            DetList=Health[ex[0]]
                            TodayList.remove(ex)

                    SubListA=Health[TodayList[0][0]]
                    SubListB=Health[TodayList[1][0]]

                    print("*"*30)
                    print(f"big3 included:\nM:{MainList},\nS:{SubListA},\nSB:{SubListB},\nD:{DetList}")
                    print("*"*30)

                    Today=DoPractice(MainList=MainList,SubListA=SubListA,SubListB=SubListB,DetList=DetList)
                    total.append(Today)

                else:
                    #print(f"{type(TodayList)}:{TodayList}")

                    TodayList = np.random.choice(TodayList, 4, replace=False)

                    MainList = Health[TodayList[0]]
                    SubListA = Health[TodayList[1]]
                    SubListB = Health[TodayList[2]]
                    DetList = Health[TodayList[3]]

                    print("*" * 30)
                    print(f"Only Shoulder:\nM:{MainList},\nS:{SubListA},\nSB:{SubListB},\nD:{DetList}")
                    print("*" * 30)

                    Today=DoPractice(MainList=MainList, SubListA=SubListA, SubListB=SubListB, DetList=DetList)
                    total.append(Today)
        else:   # only arm Day
            TodayList = np.random.choice(TodayList, 2, replace=False)

            MainList = Health[TodayList[0]]
            DetList = Health[TodayList[1]]

            print("*" * 30)
            print(f"Only Arm:\nM:{MainList},\nD:{DetList}")
            print("*" * 30)

            Today=DoPractice(MainList=MainList, DetList=DetList)
            total.append(Today)
    print('-'*30)
    print(f"total({len(total)}):\n{total}")
    print('-'*30)
    return total

def output_to_file(filename, Data):
    file = open(filename, 'w')

    for TodayWork in Data:    # the other
        for Ex in TodayWork:
            file.write(Ex+", ")
        file.write("\n")
    file.close()


def main():
    Health = makeEx()  # dictionary which key is Target muscle, Value is name of excercise.
    Data=generateTransaction(Health)
    output_filename = 'WorkOut_Data.txt'
    output_to_file(output_filename, Data)

if __name__ == '__main__':
    main()