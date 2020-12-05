package client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
    private final int port;
    private final String ip;
    private boolean isConnected;

    private Socket serverSocket;
    private PrintWriter output;
    private BufferedReader input;

    public Client(String serverIp, int serverPort){
        this.ip = serverIp;
        this.port = serverPort;
        this.isConnected = false;
    }

    public void connect(){
        System.out.println("Attempting to connect to server...");
        try{
            this.serverSocket = new Socket(this.ip, this.port);
            this.isConnected = true;
            this.output = this.getOutputStream();
            this.input = this.getInputStream();
        } catch(IOException ioe){
            this.input = null;
            this.output = null;
            this.serverSocket = null;
            this.isConnected = false;
        }
    }

    private PrintWriter getOutputStream() throws IOException{
        return new PrintWriter(this.serverSocket.getOutputStream(), true);
    }
    private BufferedReader getInputStream() throws IOException{
        return new BufferedReader(new InputStreamReader(this.serverSocket.getInputStream()));
    }
    public void sendMessage(String msg) throws IOException {
        this.output.println(msg);
    }

    public String receiveMessage() throws IOException {
        String response = this.input.readLine();
        return response;
    }
    public void disconnect(){
        try {
            this.input.close();
        } catch (IOException | NullPointerException e) {
            e.printStackTrace();
        }
        try {
            this.output.close();
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
        try {
            this.serverSocket.close();
        } catch (IOException | NullPointerException e) {
            e.printStackTrace();
        }
        this.isConnected = false;
    }

    public boolean isConnected(){
        return this.isConnected;
    }


}
