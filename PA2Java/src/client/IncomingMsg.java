package client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
//TODO need to finish this class
public class IncomingMsg implements Runnable{
    private Client clientApp;
    private Socket msgSocket;
    private String ip;
    private int port;
    private int backlog;
    private PrintWriter output;
    private BufferedReader input;

    public IncomingMsg(Client clientApp, String ip, int port){
        this.clientApp = clientApp;
        this.ip = ip;
        this.port = port;
        this.backlog = 1;
    }

    public Socket getMsgSocket(){
        return msgSocket;
    }

    private PrintWriter getOutputStream() throws IOException {
        return new PrintWriter(this.msgSocket.getOutputStream(), true);
    }
    private BufferedReader getInputStream() throws IOException{
        return new BufferedReader(new InputStreamReader(this.msgSocket.getInputStream()));
    }


    @Override
    public void run() {
    }
}
