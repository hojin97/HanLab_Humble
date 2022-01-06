using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using JetBrains.Annotations;

public class Recommend : MonoBehaviour
{
    public Text text0;
    public Text text1;
    public Text text2;

    string[] readData;

    bool inRecommend = false;

    void Start()
    {
        // 테스트용
        readData = File.ReadAllLines(@"./Assets/Data/H_data_1.txt");
    }

    public string[] pickRandom()
    {
        int randomRange = readData.Length / 2;
        string[] randData = new string[3];

        int randNum = Random.Range(0, randomRange);
        randData[0] = readData[randNum * 2];

        int i = 1;          // 0은 이미 넣음
        while (true)
        {
            randNum = Random.Range(0, randomRange);
            randData[i] = readData[randNum * 2];
            if (i == 1 && !(randData[i].Equals(randData[0])))       // 두 번째꺼 넣는데 같은게 존재안하면
            {
                i += 1;
                continue;
            }
            else if(i == 2 && !(randData[i].Equals(randData[0])) && !(randData[i].Equals(randData[1]))){
                break;
            }
        }

        return randData;
    }
    
    // Update is called once per frame
    void Update()
    {
        if (UI_Panel_Manager.curState == DisplayState.Before_Recommend)
        {
            inRecommend = true;
            UI_Panel_Manager.curState = DisplayState.After_Recommend;
        }

        if (inRecommend)
        {
            inRecommend = false;
            string [] tmpSplit;
            string[] tmpData = {"-", "-", "-"};

            if (UI_Panel_Manager.exercise == ExerciseType.Dumbbell_curl)
                readData = File.ReadAllLines(@"./Assets/Data/H_data_1.txt");
            else if (UI_Panel_Manager.exercise == ExerciseType.Dumbbell_kick_back)
                readData = File.ReadAllLines(@"./Assets/Data/H_data_2.txt");
            
            if (readData.Length < 6)                // 1개의 결과가 2줄씩 존재. 따라서 3개의 결과 이하를 뜻함.
            {
                for (int i=0; i < readData.Length/2; i++)
                {
                    tmpData[i] = readData[i*2];
                }
            }
            else
            {
                tmpData = pickRandom();
            }
            
            for (int i=0; i<3; i++)
            {
                tmpSplit = tmpData[i].Split(',');
                tmpData[i] = "";
                for (int j=0; j < tmpSplit.Length-1; j++)                       // -1을 한 이유는 맨 마지막은 split결과가 마지막은 항상 ""로 존재. (계산이유 없음)
                {
                    tmpData[i] = tmpData[i] + tmpSplit[j] + "\n";
                }
            }
            text0.text = tmpData[0];
            text1.text = tmpData[1];
            text2.text = tmpData[2];
        }
    }
}
