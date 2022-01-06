using System.Data;
using MySql.Data;
using MySql.Data.MySqlClient;

public class SQL
{
    MySqlConnection sqlconn = null;
    private string sqlDBip = "127.0.0.1";
    private string sqlDBname = "humble";
    private string sqlDBid = "root";
    private string sqlDBpw = "autoset";

    private void sqlConnect()
    {
        string sqlDatabase = "Server=" + sqlDBip + ";Database=" + sqlDBname + ";UserId=" + sqlDBid + ";Password=" + sqlDBpw + "";

        //접속 확인하기
        try
        {
            sqlconn = new MySqlConnection(sqlDatabase);
            sqlconn.Open();
            //Debug.Log("SQL의 접속 상태 : " + sqlconn.State); //접속이 되면 OPEN이라고 나타남
        }
        catch (System.Exception msg)
        {
            //Debug.Log(msg);
        }
    }

    private void sqldisConnect()
    {
        sqlconn.Close();
        //Debug.Log("SQL의 접속 상태 : " + sqlconn.State); //접속이 끊기면 Close가 나타남 
    }

    public void sqlUpdate(string allcmd) //함수를 불러올때 명령어에 대한 String을 인자로 받아옴
    {
        sqlConnect();                   //접속

        MySqlCommand dbcmd = new MySqlCommand(allcmd, sqlconn); //명령어를 커맨드에 입력
        dbcmd.ExecuteNonQuery(); //명령어를 SQL에 보냄

        sqldisConnect(); //접속해제
    }

    public DataTable sqlSelect(string sqlcmd)  //리턴 형식을 DataTable로 선언함
    {
        DataTable dt = new DataTable(); //데이터 테이블을 선언함

        sqlConnect();
        MySqlDataAdapter adapter = new MySqlDataAdapter(sqlcmd, sqlconn);
        adapter.Fill(dt); //데이터 테이블에  채워넣기를함
        sqldisConnect();

        return dt; //데이터 테이블을 리턴함
    }

}
