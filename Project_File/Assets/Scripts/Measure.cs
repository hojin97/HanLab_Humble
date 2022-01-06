using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Measure : MonoBehaviour
{
    public Text RMS;
    public Text maxRMS;
    bool isChange = false;

    float period = 0;
    float rms = 0;
    public static float maxRms = 0;

    // Update is called once per frame
    void Update()
    {
        if(UI_Panel_Manager.curState == DisplayState.After_Measure){
            if (Input.GetKeyDown(KeyCode.O))
            {
                UI_Panel_Manager.srGroup(UI_Panel_Manager.User_Panel, UI_Panel_Manager.Measure_Panel);
                UI_Panel_Manager.curState = DisplayState.Exercise;
            }

            period += Time.deltaTime;
            if (period > 0.2f)
            {
                period = 0;
                if (UI_Panel_Manager.curState == DisplayState.After_Measure)
                {
                    rms = ThalmicMyo.getRMS();
                    if (maxRms < rms)
                    {
                        maxRms = rms;
                        isChange = true;
                    }
                    RMS.text = System.Math.Round(rms, 2) + " RMS";

                    if (isChange)
                    {
                        isChange = false;
                        maxRMS.text = "당신의 최대 RMS : " + System.Math.Round(maxRms, 2);
                    }
                }
            }
        }
    }
}
