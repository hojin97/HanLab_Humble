using System.Collections;
using System.Collections.Generic;
using UnityEditorInternal;
using UnityEngine;
using UnityEngine.UI;

public enum DisplayState
{
    Start,
    ExerciseChoice,
    ExerciseVideo,
    Before_Measure,
    After_Measure,
    End_main,
    Exercise,
    Before_Recommend,     // 추천 전
    After_Recommend      // 추천 후
}

public enum ExerciseType
{
    Dumbbell_curl,
    Hammer_curl,
    Reverse_curl,
    Dumbbell_kick_back
}

public class UI_Panel_Manager : MonoBehaviour
{
    public CanvasGroup s_p;
    public CanvasGroup ec_p;
    public CanvasGroup ev_p;
    public CanvasGroup m_p;
    public CanvasGroup u_p;
    public CanvasGroup e_p;
    public CanvasGroup r_p;
    public CanvasGroup ft_p;
    public static CanvasGroup Start_Panel;
    public static CanvasGroup ExerciseChoice_Panel;
    public static CanvasGroup ExerciseVideo_Panel;
    public static CanvasGroup Measure_Panel;
    public static CanvasGroup User_Panel;
    public static CanvasGroup End_Panel;
    public static CanvasGroup Recommend_Panel;
    public static CanvasGroup Freetime_Panel;
    public static CanvasGroup None;                 // 아무것도 아님.

    public static DisplayState curState;
    public static ExerciseType exercise;

    public Text UI_state;
    

    public void Start()
    {
        // 패널 초기화
        Start_Panel = s_p;
        ExerciseChoice_Panel = ec_p;
        ExerciseVideo_Panel = ev_p;
        Measure_Panel = m_p;
        User_Panel = u_p;
        End_Panel = e_p;
        Recommend_Panel = r_p;
        Freetime_Panel = ft_p;

        srGroup(Start_Panel, End_Panel);

        // 상태 초기화
        curState = DisplayState.Start;


        // 일단은 덤벨컬만 한다는 가정 하에 진행.
        //exercise = ExerciseType.Dumbbell_curl;
        //exercise = ExerciseType.Dumbbell_kick_back;
    }

	private void Update()
	{
        UI_state.text = curState.ToString();
	}

	public static void srGroup(CanvasGroup c1, CanvasGroup c2)         // 순서대로 1, 0 대입
    {
        c1.alpha = 1;
        c1.interactable = true;
        c1.blocksRaycasts = true;

        c2.alpha = 0;
        c2.interactable = false;
        c2.blocksRaycasts = false;
    }

    public static void onGroup(CanvasGroup c1, CanvasGroup c2)
    {
        c1.alpha = 1;
        c1.interactable = true;
        c1.blocksRaycasts = true;

        c2.interactable = true;
        c2.blocksRaycasts = true;
    }
}
