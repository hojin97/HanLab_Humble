using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Canvas_Manager : MonoBehaviour
{
    public CanvasGroup Login_Panel;
    public CanvasGroup Create_Panel;
    public CanvasGroup Duplicate_Panel;
    public CanvasGroup Err_Panel;
    public static CanvasGroup l_panel;
    public static CanvasGroup c_panel;
    public static CanvasGroup d_panel;
    public static CanvasGroup e_panel;

    public void Start()
	{
        l_panel = Login_Panel;
        c_panel = Create_Panel;
        d_panel = Duplicate_Panel;
	}

	public static void CanvasGroup_On_Off(CanvasGroup c1, CanvasGroup c2){
        c1.alpha = 1;
        c1.interactable = true;
        c1.blocksRaycasts = true;

        c2.alpha = 0;
        c2.interactable = false;
        c2.blocksRaycasts = false;
	}

    public static void CanvasGroup_Overview_On(CanvasGroup c1, CanvasGroup c2){
        c1.interactable = false;
        c1.blocksRaycasts = false;

        c2.alpha = 1;
        c2.interactable = true;
        c2.blocksRaycasts = true;
	}

    public static void CanvasGroup_Overview_Off(CanvasGroup c1, CanvasGroup c2)
    {
        c1.interactable = true;
        c1.blocksRaycasts = true;

        c2.alpha = 0;
        c2.interactable = false;
        c2.blocksRaycasts = false;
    }
}
