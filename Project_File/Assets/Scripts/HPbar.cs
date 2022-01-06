using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HPbar : MonoBehaviour
{
    [SerializeField]
    private Slider hpBar;

    private float maxHp = 0;  // 최대 hp 상태
    public static float curHp = 0; //현재 hp 상태
    public static int MinusHP = 5;
    private bool start_ex = false;

    float hpRatio = curHp;

    void Start()
    {

    }

    private float period = 0;
    void Update()
    {
        // Debug.Log(UI_Panel_Manager.curState);
        // 시작 안하는 중인데 현재 상태가 운동으로 바뀌면 maxRms 값을 받아 온다.
        if (!start_ex)
        {
            if (UI_Panel_Manager.curState == DisplayState.Exercise)
            {
                start_ex = true;
                maxHp = Measure.maxRms * 120;
                hpBar.value = 1;
                Debug.Log("MAX_hp : " + maxHp);
                SaveFile.start = true;
            }
        }
        else
        {
            period += Time.deltaTime;
            //Debug.Log(period);
            if (Input.GetKeyDown(KeyCode.Space))     // 스페이스바 누르면 INT 측정 시작
            {
                ThalmicMyo.change_CollectFlag();
                curHp = maxHp;
                SaveFile.start = true;
            }

            if (period > 0.1f && ThalmicMyo.collection_flag)    //1차: spacebar keydown이 있을경우 hpBar가 10씩 떨어짐 >> 팔의 움직임을 조건으로 걸어 떨어지는 수치 변경
            {
                period = 0;
                gradient.HP_FLAG = true;
                if (curHp > 0)
                {
                    curHp -= (float)UserPanel.RMS;
                    //Debug.Log("HP : " + HPbar.curHp);
                }
                else
                {
                    curHp = 0;
                }
                hpRatio = (float)curHp / (float)maxHp;
            }
            handleHp();
        }
    }

    private void handleHp()
    {
        //hpBar.value = hpRatio;
        hpBar.value = Mathf.Lerp(hpBar.value, hpRatio, Time.deltaTime * 10);
    }

}