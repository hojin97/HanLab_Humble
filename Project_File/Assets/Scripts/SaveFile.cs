using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using System.Diagnostics;
using Debug = UnityEngine.Debug;

public class SaveFile : MonoBehaviour
{
    string filePath;
    bool writeFlag = false;
    float period = 0;
    float period_time = 0.02f;
    int sec = 0;
    int cnt_rps = 0;
    FileStream fs = null;
    StreamWriter sw = null;
    public static bool start = false;

    public bool gd = true;
    public bool st = false;
    public float ti = 0;

    // Start is called before the first frame update
    void Start()
    {
        period = 0;
        writeFlag = false;
        Debug.Log(period_time);
    }

    // Update is called once per frame
    void Update()
    {
        period += Time.deltaTime;
        ti += Time.deltaTime;

        if (Input.GetKeyDown(KeyCode.Space))
        {
            gd = !gd;
            st = true;
        }

        if (st && ti > 2){
            ti = 0;
            gd = !gd;
		}

        if (!gd)
        {
            //Debug.Log("RMS : " + ThalmicMyo.getRMS());
            //Debug.Log("Angle : " + AngleArc.angle);
            if (start && !writeFlag)
            {
                cnt_rps += 1;
                filePath = "./HumbleData/" + DateTime.Now.ToString("MMdd_HHmm_ss")+ "_" + cnt_rps + ".txt";
                fs = new FileStream(filePath, FileMode.Create);
                sw = new StreamWriter(fs);
                writeFlag = true;
            }
        }
        else
        {
            if (writeFlag)
            {
                sw.Close();
                fs.Close();
                sec = 0;
                gd = !gd;
                writeFlag = false;
                UserPanel.do_raps = false;
                Debug.Log("Save");
            }
        }
        
        if (writeFlag && period >= period_time)
        {
            //Debug.Log(period);
            sec += 1;
            period = 0;

            //sw.Write(sec*0.1 + "\t" + ThalmicMyo.getRMS() + "\t" + Math.Round(AngleArc.angle, 2) + "\n");
            sw.Write(sec + "\t" + ThalmicMyo.ED[0] + "\t" + ThalmicMyo.ED[1] + "\t" + ThalmicMyo.ED[2] + "\t" + ThalmicMyo.ED[3] + "\t" + ThalmicMyo.ED[4] + "\t" + ThalmicMyo.ED[5] + "\t" + ThalmicMyo.ED[6] + "\t" + ThalmicMyo.ED[7] + "\t" + Math.Round(AngleArc.angle, 2) + "\n");
        }
    }
}
