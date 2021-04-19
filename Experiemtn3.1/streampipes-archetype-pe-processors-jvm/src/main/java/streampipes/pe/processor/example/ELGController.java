package streampipes.pe.processor.example;

import com.amazonaws.util.json.JSONException;
import com.amazonaws.util.json.JSONObject;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.io.*;

public class ELGController {

    /*  ELG_INFO - Helper class
    * This class holds only two string variables as the JSON representation from the Serve_ELG_info service
    * Attributes:
    *  ELG_ServiceLink; holds the URL for the HTTP request to the specific ELG service
    *  ELG_Key; holds the authentication key for the ELG service
    * */
    private class ELG_Info {
        private String ELG_ServiceLink = "";
        private String ELG_Key = "";

        public String GetServiceLink(){
            return ELG_ServiceLink;
        }

        public String GetKey(){
            return ELG_Key;
        }
    }
    protected ELG_Info mInfo;


    private class response{
        public String type;
        public String content;
        public int score;

    }
    protected  response mResponse;

    //Those two attributes holde the input and output plain text
    private String ELG_InputText = "";
    public void SetInputText(String sInput)
    {
        ELG_InputText = sInput;
    }

    private String ELG_OutPutText = "";
    public String GetOutput()
    {
        return ELG_OutPutText;
    }


    //Runs the ELG services which is related to 'sParam' and returns the true when it successful
    public boolean RunELGService(String sParam){
        if(GetELGService(sParam) == false)
            return false;
        return SendRequest();
    }

    //This mehtods asks the Serve_ELG for the related link and key for the given sParam. Returns false when no sParam is registered
    private boolean GetELGService(String sParam)  {
        System.out.println("Send Reqeust to ELG Serve for Link and Key");
        //Set for Http request
        CloseableHttpClient client = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost("http://localhost:8150");

        String msg = sParam;
        StringEntity entity = null;

        try {
            entity = new StringEntity(msg);
        } catch (UnsupportedEncodingException unsupportedEncodingException) {
            unsupportedEncodingException.printStackTrace();
            return false;
        }

        //send request
        httpPost.setEntity(entity);
        httpPost.setHeader("Content-Type", "text/plain");
        CloseableHttpResponse response = null;

        try {
            response = client.execute(httpPost);
            System.out.println("ELG Serve Execute is Sucess!");
        } catch (
                IOException e) {
            e.printStackTrace();
            return false;
        }
        //read the JSON response
        assert response != null;
        HttpEntity oEntity = response.getEntity();
        InputStream instream = null;
        try {
            instream = oEntity.getContent();
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        String result = convertStreamToString(instream);

        //convert the JSON to ELG_Info object
        mInfo = new ELG_Info();
        JSONObject json = null;
        try {
            json = new JSONObject(result);
            mInfo.ELG_ServiceLink = (String) json.get("ELG_ServiceLink");
            mInfo.ELG_Key = (String) json.get("ELG_Key");
        } catch (JSONException e) {
            e.printStackTrace();
            return false;
        }

        System.out.println("ELG Service link is:"  + mInfo.GetServiceLink());

        try {
            instream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        int nStatusCode = response.getStatusLine().getStatusCode();

        try {
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
            //return false;
        }

        return nStatusCode == 200;
    }

    //This method sends a HTTP reqeust to the ELG service under ELG_Link with plain text in ELG_InputText
    private boolean SendRequest() {
        //prepare Http request
        CloseableHttpClient client = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(mInfo.GetServiceLink());

        String json = ELG_InputText;
        StringEntity entity = null;

        try {
            entity = new StringEntity(json);
        } catch (UnsupportedEncodingException unsupportedEncodingException) {
            unsupportedEncodingException.printStackTrace();
            return false;
        }

        httpPost.setEntity(entity);
        httpPost.setHeader("Authorization", "Bearer " + mInfo.GetKey());
        httpPost.setHeader("Content-Type", "text/plain");

        //send request
        CloseableHttpResponse response = null;
        try {
            System.out.println("Sending this plain text to the ELG service: " + ELG_InputText);
            response = client.execute(httpPost);
            System.out.println("Client Execute is Sucess!");
        } catch (
                IOException e) {
            e.printStackTrace();
            return false;
        }
        System.out.println("Status Code from ELG is:" + response.getStatusLine().getStatusCode());

        //convert response to plain text
        try {
            ELG_OutPutText =  convertStreamToString(response.getEntity().getContent());
            ELG_OutPutText= ELG_OutPutText.replace("{\"response\":{\"type\":\"texts\",\"texts\":[{\"content\":\"","");
            ELG_OutPutText= ELG_OutPutText.replace("\",\"score\":0}]}}","");
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }

// {"response":{"type":"texts","texts":[{"content":"In diesem Beispiel","score":0}]}}
        try {
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return true;
    }



    //helper method for 'GetELGService' and 'SendRequest', convert the inputstream to string
    private static String convertStreamToString(InputStream is) {

        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();

        String line = null;
        try {
            while ((line = reader.readLine()) != null) {
                sb.append(line + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }

}

