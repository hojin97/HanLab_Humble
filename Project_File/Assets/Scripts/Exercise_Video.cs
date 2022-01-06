using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Video;

public class Exercise_Video : MonoBehaviour
{
    public VideoPlayer videoPlayer1, videoPlayer2, videoPlayer3;
	public VideoClip dumbbelCurl1, dumbbelCurl2, dumbbelCurl3;
	public VideoClip hammerCurl1, hammerCurl2, hammerCurl3;
	public VideoClip reverseCurl1, reverseCurl2, reverseCurl3;
	public VideoClip tricepsKickback1, tricepsKickback2, tricepsKickback3;
	public Text exercise_name;
	bool playing = false;

	public void Update()
	{
		if (UI_Panel_Manager.exercise == ExerciseType.Dumbbell_curl)
		{
			exercise_name.text = "Dumbbel Curl";
		}
		else if (UI_Panel_Manager.exercise == ExerciseType.Hammer_curl)
		{
			exercise_name.text = "Hammer Curl";
		}
		else if (UI_Panel_Manager.exercise == ExerciseType.Reverse_curl)
		{
			exercise_name.text = "Reverse Curl";
		}
		else if (UI_Panel_Manager.exercise == ExerciseType.Dumbbell_kick_back)
		{
			exercise_name.text = "Triceps Kickback";
		}
		if (playing == true && UI_Panel_Manager.curState == DisplayState.ExerciseChoice){
			playing = false;
		}
		if (playing == false && UI_Panel_Manager.curState == DisplayState.ExerciseVideo){
			playing = true;
			VideoPlay();
		}
	}
	public void VideoPlay(){
        if(UI_Panel_Manager.exercise == ExerciseType.Dumbbell_curl){
			videoPlayer1.clip = dumbbelCurl1;
			videoPlayer2.clip = dumbbelCurl2;
			videoPlayer3.clip = dumbbelCurl3;
			videoPlayer1.Play();
			videoPlayer2.Play();
			videoPlayer3.Play();
		}
		else if (UI_Panel_Manager.exercise == ExerciseType.Hammer_curl)
		{
			videoPlayer1.clip = hammerCurl1;
			videoPlayer2.clip = hammerCurl2;
			videoPlayer3.clip = hammerCurl3;
			videoPlayer1.Play();
			videoPlayer2.Play();
			videoPlayer3.Play();
		}
		else if (UI_Panel_Manager.exercise == ExerciseType.Reverse_curl)
		{
			videoPlayer1.clip = reverseCurl1;
			videoPlayer2.clip = reverseCurl2;
			videoPlayer3.clip = reverseCurl3;
			videoPlayer1.Play();
			videoPlayer2.Play();
			videoPlayer3.Play();
		}
		else if (UI_Panel_Manager.exercise == ExerciseType.Dumbbell_kick_back)
		{
			videoPlayer1.clip = tricepsKickback1;
			videoPlayer2.clip = tricepsKickback2;
			videoPlayer3.clip = tricepsKickback3;
			videoPlayer1.Play();
			videoPlayer2.Play();
			videoPlayer3.Play();
		}
	}
}
