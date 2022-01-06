using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using UnityEngine;
using UnityEngine.UI;

public class Create : MonoBehaviour
{
	public InputField c_id;
	public InputField c_pw;
	public InputField c_name;
	public InputField c_bir;

	public Text err_text;

	bool err_msg = false;
	float period = 0;
	int ch_res;

	public void Btn_ID_Check(){
		DataTable r_dt = Login.sql.sqlSelect("select id from user where id = '" + c_id.text + "';");
		try{
			if(r_dt.Rows[0][0].ToString() == c_id.text){
				Debug.Log("아이디가 이미 존재합니다.");
			}
		}catch(Exception er){
			Debug.Log("아이디 사용이 가능합니다.");
			Canvas_Manager.CanvasGroup_Overview_On(Canvas_Manager.c_panel, Canvas_Manager.d_panel);
		}
	}

	public void Btn_create_account(){
		ch_res = inputfield_type_check();
		if(ch_res == -1){
			err_msg = true;
			period = 0;
			Canvas_Manager.CanvasGroup_Overview_On(Canvas_Manager.c_panel, Canvas_Manager.e_panel);
			err_text.text = "이름 입력이 잘못 되었습니다.";
		}
		else if(ch_res == -2){
			err_msg = true;
			period = 0;
			Canvas_Manager.CanvasGroup_Overview_On(Canvas_Manager.c_panel, Canvas_Manager.e_panel);
			err_text.text = "생일 입력이 잘못 되었습니다.";
		}
		else{
			try
			{
				Login.sql.sqlUpdate("insert into user values('" + c_id.text + "', '" + c_pw.text + "', '" + c_name.text + "', '" + c_bir.text + "');");
				Canvas_Manager.CanvasGroup_On_Off(Canvas_Manager.l_panel, Canvas_Manager.c_panel);
			}
			catch (Exception e)
			{
				Debug.Log(e);
			}
		}
	}

	public void Update()
	{
		period += Time.deltaTime;
		if (err_msg == true && period > 1){
			err_msg = false;
			Canvas_Manager.CanvasGroup_Overview_Off(Canvas_Manager.c_panel, Canvas_Manager.e_panel);
		}
	}

	private int inputfield_type_check(){
		
		if(c_id.readOnly == false){
			return -1;	// 아이디 칸 오류 
		}
		else if (c_name.text.Length > 10){
			return -2;	// 이름 칸 오류
		}
		else if(c_bir.text.Length != 8){
			return -3;  // 생일 칸 오류
		}
		try{
			DateTime date = new DateTime(int.Parse(c_bir.text));
		}
		catch(Exception e){
			return -3;  // 생일 칸 오류
		}
		return 0;	// 정상
	}

	public void Btn_duplicate_yes(){
		Canvas_Manager.CanvasGroup_Overview_Off(Canvas_Manager.c_panel, Canvas_Manager.d_panel);
		c_id.readOnly = true;
	}

	public void Btn_duplicate_no(){
		Canvas_Manager.CanvasGroup_Overview_Off(Canvas_Manager.c_panel, Canvas_Manager.d_panel);
	}
}
