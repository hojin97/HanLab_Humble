using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.UI;
using UnityEngine.UIElements;


public class gradient : MonoBehaviour
{
    public Gradient grad;
    Color col;

    int R, G, B;
    float H, S, V;

    public static bool HP_FLAG = false;

    [Range(0, 1)]
    public float t;

    private UnityEngine.UI.Image img;
    //Slider hpSlider;

    void Start()
    {
        //  hpSlider = GameObject.Find("hpBar").GetComponent<Slider>();
        //  hpSlider.onValueChanged.AddListener(delegate { Update(); });

        img = transform.GetComponent<UnityEngine.UI.Image>();

        // 초기화
        R = 0;
        G = 255;
        B = 0;
    
    }

    void Update()
    {
        if (HP_FLAG)
        {
            if (HPbar.curHp > 70.0)
            {
                R = R + int.Parse((255 / ((100 - 70) / HPbar.MinusHP)).ToString());
                G = 255;
                B = 0;
            }
            else if (HPbar.curHp > 40.0)
            {
                R = 255;
                G = G - int.Parse((255 / ((70 - 40) / HPbar.MinusHP)).ToString());
                B = 0;
            }
            else
            {
                R = 255;
                G = 0;
                B = 0;
            }
            //Debug.Log(R + " " + G + " " + B);
            HP_FLAG = false;
        }

        col = new Color(R, G, B , 1.0F);
        Color.RGBToHSV(col, out H, out S, out V);
        img.color = col;
    }

}