using System;
using System.Data;
using UnityEngine;
using UnityEngine.UI;


//using Microsoft.SqlServer.Server;

public class Login : MonoBehaviour
{
	public static SQL sql = new SQL();

	public InputField u_id;
	public InputField u_pw;

	public void btn_login(){
		DataTable dt = sql.sqlSelect("select id from user where id = '"+u_id.text+"' and pw = '"+u_pw.text+"';");

		try
		{
			if (dt.Rows[0][0].ToString() == u_id.text)
			{
				Debug.Log("Login!");
			}
		}
		catch (Exception e){
			Debug.Log("아이디 혹은 비밀번호가 틀렸습니다.");
		}
		
	}

}
