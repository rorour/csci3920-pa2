package client;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.event.ActionEvent;
import javafx.event.Event;
import javafx.scene.control.*;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;

import java.io.IOException;

public class Controller {
    public Pane paneConnect;
    public Pane paneLogin;
    public Pane paneRegister;
    public TabPane tabPane;
    public Tab tabviewMsg;

    public Label labelConnectStatus;
    public Label labelWelcomeMsg;
    public Label labelCharLength;

    public TextField txtServer;
    public TextField txtPort;
    public TextField txtLoginUser;
    public PasswordField pTxtPassword;
    public TextField txtDisplayName;
    public TextField txtNewUsername;
    public PasswordField pTxtNewPassword;
    public TextField txtSendTo;
    public TextArea txtMsgContent;

    public ListView listIncomingMsg;

    public Button btnConnect;
    public Button btnSendMsg;
    public Button btnLogin;
    public Button btnDisconnect;
    public Button btnNewUser;
    public Button btnSignUp;


    private boolean isConnected;
    private boolean isLoggedIn;
    private String username;
    private Client client;

    private Alert alert;

    public Controller(){
        //update message list here
        isConnected = false;
        isLoggedIn = false;
    }


    public void initialize(){
        //Ensures the right pane is showing on opening app
        if(!isConnected){
            showConnectPane(true);
            showLoginPane(false);
            showRegisterPane(false);
            showMainPane(false);
        }
        //Counts the number of characters the user is typing in textArea and displays count
        this.txtMsgContent.textProperty().addListener(new ChangeListener<String>() {
            @Override
            public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                if(newValue != null){
                    int numOfChar = newValue.length();
                    labelCharLength.setText(String.valueOf(numOfChar));
                    if(numOfChar > 500){
                        labelCharLength.setTextFill(Color.RED);
                    }
                    else{
                        labelCharLength.setTextFill(Color.BLACK);
                    }
                }

            }
        });
        //TODO: tab update
        //listIncomingMsg
        //For the eventual tab implementation for the received messages tab
//        this.lstEnrolledCourse.getSelectionModel().selectedItemProperty().addListener(new ChangeListener<Course>() {
//            @Override
//            public void changed(ObservableValue<? extends Course> observable, Course oldValue, Course newValue) {
//                if(newValue != null){
//                    lstEnrolledStudent.setItems(FXCollections.observableArrayList(newValue.getEnrolledStudents()));
//                }
//            }
//        });
    }


    public void connectToServer(ActionEvent actionEvent) {
        if(!txtServer.getText().isEmpty() && !txtPort.getText().isEmpty()){
            String ip = txtServer.getText();
            int port = Integer.parseInt(txtPort.getText());
            try{
                client = new Client(ip, port);
                client.connect();

                if(client.isConnected()){
                    System.out.println("Connected");
                    String serverMsg = client.receiveMessage(); //TODO causing freeze
                    alert = new Alert(Alert.AlertType.CONFIRMATION, serverMsg);
                    this.isConnected = true;
                }
            }
            catch(IOException ioe){ //if error in receiving msg
                alert = new Alert(Alert.AlertType.ERROR, ioe.getMessage());
            }
        }
        else{
            alert = new Alert(Alert.AlertType.ERROR, "Entries are blank");
            alert.show();
        }

        if(this.isConnected){
            labelConnectStatus.setText("Connected to Server");
            showConnectPane(false);
            showLoginPane(true);
            showRegisterPane(false);
            showMainPane(false);
        }

    }

    public void loginToApp(ActionEvent actionEvent) {
        if(!txtLoginUser.getText().isEmpty() && !pTxtPassword.getText().isEmpty()){
            String login = txtLoginUser.getText();
            String password = pTxtPassword.getText();
            //TODO: login to server here
        }
        else {
            alert = new Alert(Alert.AlertType.ERROR, "Entries are blank");
            alert.show();
        }
        if(isLoggedIn){
            if(!txtLoginUser.getText().isEmpty()){
                this.username = txtLoginUser.getText();
                this.labelWelcomeMsg.setText("Welcome " + this.username + "!");
            }

            showConnectPane(false);
            showLoginPane(false);
            showMainPane(true);
        }
    }

    public void disconnectFromServer(ActionEvent actionEvent) {
    }

    public void sendMessage(ActionEvent actionEvent) {
        if(labelCharLength.getText().length() <= 500){
            //todo: send message
            //todo: clear text once send is successful
            //txtSendTo.clear();
            //txtMsgContent.clear();

        } else {
            alert = new Alert(Alert.AlertType.ERROR, "Message exceeds Max Character Limit");
            alert.show();
        }
    }

    /** Tab Refresh */
    public void viewMessagesUpdate(Event event) {
        //todo update lists in tab with oncoming messages
        //listIncomingMsg
    }

    public void signUpAndLogIn(ActionEvent actionEvent) {
        if(!txtNewUsername.getText().isEmpty() && !pTxtNewPassword.getText().isEmpty()
                && !txtDisplayName.getText().isEmpty())
        {
            String user = txtNewUsername.getText();
            String password = pTxtNewPassword.getText();
            String display = txtDisplayName.getText();
            //todo: login server here
        }
        else {
            alert = new Alert(Alert.AlertType.ERROR, "Entries are blank");
            alert.show();
        }
    }

    public void getToNewUserPane(ActionEvent actionEvent) {
        showConnectPane(false);
        showLoginPane(false);
        showRegisterPane(true);
        showMainPane(false);
    }

    /** Clears message fields after sending the message */
    public void clearMsgFields(){}

    private void showConnectPane(boolean show){
        boolean disable = !show;
        this.paneConnect.setVisible(show);
        this.paneConnect.setDisable(disable);

    }

    private void showLoginPane(boolean show){
        boolean disable = !show;
        this.paneLogin.setVisible(show);
        this.paneLogin.setDisable(disable);
    }

    private void showMainPane(boolean show){
        boolean disable = !show;
        this.tabPane.setVisible(show);
        this.tabPane.setDisable(disable);
    }

    private void showRegisterPane(boolean show){
        boolean disable = !show;
        this.paneRegister.setVisible(show);
        this.paneRegister.setDisable(disable);
    }


}
