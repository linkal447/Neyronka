using UnityEngine;
using UnityEngine.Networking;
using System.Collections;


public class AIRequest : MonoBehaviour
{

    public string userText;


    public void SendRequest()
    {
        StartCoroutine(GetGenre());
    }



    IEnumerator GetGenre()
    {

        string json = 
        "{\"text\":\"" 
        + userText 
        + "\"}";


        UnityWebRequest request =
        new UnityWebRequest(
        "http://localhost:5000/predict",
        "POST");


        byte[] body =
        System.Text.Encoding.UTF8.GetBytes(json);


        request.uploadHandler =
        new UploadHandlerRaw(body);


        request.downloadHandler =
        new DownloadHandlerBuffer();


        request.SetRequestHeader(
        "Content-Type",
        "application/json");


        yield return request.SendWebRequest();



        string result =
        request.downloadHandler.text;


        Debug.Log(result);


        if(result.Contains("platformer"))
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene("Platformer");
        }


        if(result.Contains("battle"))
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene("Battle");
        }


        if(result.Contains("farm_shop"))
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene("Farm");
        }

    }
}