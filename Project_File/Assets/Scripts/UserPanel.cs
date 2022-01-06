using System;
using UnityEngine;
using UnityEngine.UI;
using Debug = UnityEngine.Debug;

public enum User_state
{
    idle,
    breaktime,
    exercising
}

public class UserPanel : MonoBehaviour
{
    public static User_state user_state;

    public Text setText;
    public Text repText;
    public Text stateText;

    private int reps;
    private int sets;
    float period=0;
    public static bool do_raps = false;

    public static double RMS = 0;
    public static double ANG = 0;
    double Y_hat = 1;

    public Image assistant;
    private float assis_alpha = 0;
    private int cnt_wrong_reps = 0;
    

    #region StopWatch
    float timer, fr_timer;
    float milseconds, seconds, minutes;

    [SerializeField] Text TimeText;
    [SerializeField] Text FreetimeText;
    #endregion StopWatch
    void Start()
    {
        initialUI();
        period = 0;
    }

    void initialUI()
    {
        timer = 0;
        fr_timer = 10;
        reps = 0;
        sets = 0;
        setText.text = "Sets: 0 / 5";
        repText.text = "Reps: 0 / 10";
        TimeText.text = "Time: 00:00:00";
    }

    // Update is called once per frame
    void Update()
    {
        if(UI_Panel_Manager.curState == DisplayState.Exercise){
            stateText.text = user_state.ToString();
            period += Time.deltaTime;

            // 쉬는 시간일 때
            if (user_state == User_state.breaktime)
            {
                BreaktimeProcessing();
            }
            else if (user_state == User_state.exercising)
            {
                StopWatch(TimeText);
            }

            // 운동 중일 때
            if (user_state == User_state.exercising)
            {
                // 10회 반복 한 세트가 끝나거나 Space로 강제 1세트 넘기는 경우
                if (reps >= 10 || Input.GetKeyDown(KeyCode.Space))
                {
                    SetProcessing();
                }

                // 2초 마다 운동 유효성 검사
                if (period >= 2f)
                {
                    CheckExerciseValidation();
                }
                setText.text = "Sets: " + sets + " / 5";
                repText.text = "Reps: " + reps + " / 10";
                do_raps = true;
            }

            // 처음 들어온 상태 일 때
            if (user_state == User_state.idle)
            {
                if (Input.GetKeyDown(KeyCode.Space))
                {
                    user_state = User_state.exercising;
                }
            }

            // 세트 수가 5 넘은 경우 (끝난 경우)
            if (sets >= 6)
            {
                UI_Panel_Manager.srGroup(UI_Panel_Manager.End_Panel, UI_Panel_Manager.User_Panel);
                UI_Panel_Manager.curState = DisplayState.End_main;
                initialUI();
            }
            // O 입력 시 reps++
            else if (Input.GetKeyDown(KeyCode.O))
            {
                reps += 1;
            }
        }
    }

    void CheckExerciseValidation(){
        period = 0;

        RMS = (double)(Math.Round(ThalmicMyo.getRMS(), 2));
        ANG = (double)(Math.Round(AngleArc.angle, 2));

        Debug.Log("ANG: " + ANG.ToString());

        Y_hat = formal(RMS, ANG);

        if (Y_hat >= 0.6254)    //6248 , 6254
        {
            RepProcessing();
            //Y_hat = formal(RMS, ANG);
        }
        else{
            cnt_wrong_reps += 1;
		}

        if(cnt_wrong_reps >= 3){
            assis_alpha += 0.2f;
            assistant.color = new Color(255, 255, 255, assis_alpha);
		}
    }

    void RepProcessing()
    {
        reps += 1;
        do_raps = true;
        repText.text = "Reps: " + (reps - 1).ToString() + " /10";

        cnt_wrong_reps = 0;
        assis_alpha = 0;
        assistant.color = new Color(255, 255, 255, 0);
    }

    void BreaktimeProcessing(){
        UI_Panel_Manager.Freetime_Panel.alpha = 1;
        BreaktimeStopWatch(FreetimeText);
        if (fr_timer <= 0f)
        {
            UI_Panel_Manager.Freetime_Panel.alpha = 0;
            fr_timer = 10;
            user_state = User_state.exercising;
        }
    }
    void SetProcessing(){
        sets += 1;
        timer = 0;
        reps = 0;
        user_state = User_state.breaktime;
        TimeText.text = "Time: 00:00:00";
        do_raps = false;
        SaveFile.start = false;
    }

    void StopWatch(Text timeText)
    {
        timer += Time.deltaTime;
        seconds = (int)(timer % 60);
        milseconds = Mathf.Ceil((timer - seconds)*100);
        minutes = (int)((timer / 60) % 60);

        timeText.text = "Time: " + minutes.ToString("00") + ":" + seconds.ToString("00") + ":" + milseconds.ToString("00");
    }

    void BreaktimeStopWatch(Text timeText)
    {
        fr_timer -= Time.deltaTime;
        seconds = (int)(fr_timer % 60);
        milseconds = Mathf.Ceil((fr_timer - seconds) * 100);
        timeText.text = seconds.ToString("00") + " : " + milseconds.ToString("00");
        
        if (fr_timer >= 5f){
            timeText.color = new Color(255, 255, 255);
            timeText.fontStyle = FontStyle.Normal;
        }
        else if (fr_timer >= 3f){
            timeText.color = new Color(255, 255, 0);
            timeText.fontStyle = FontStyle.Bold;
        }
        else{
            timeText.color = new Color(255, 0, 0);
            timeText.fontStyle = FontStyle.BoldAndItalic;
        }
    }

    double sigmoid(double z)
    {
        return 1.0 / (1 + Math.Exp(-1 * z));
    }

    double formal(double RMS, double ANG)
    {
        //Normalize
        if (RMS >= 5.47)
        {
            RMS = (RMS - 5.47) / (90.48);
        }
        else
            RMS = 0;

        if (ANG >= 36.23)
        {
            ANG = (ANG - 36.23) / (141.12);
        }
        else
            ANG = 0;

        //After first layer
        double X1 = 6.01971921 * RMS - 15.7309641 * ANG - 4.82527526;
        double X2 = -7.96912376 * RMS - 11.27525099 * ANG + 0.96991828;
        

        double H1 = sigmoid(X1);
        double H2 = sigmoid(X2);

        double A = 5.18146232 * H1 - 5.8404422 * H2 + 0.5126402;

        double Y_hat = sigmoid(A);

        return Y_hat; 
    }
   
}
