//Created by Dagger -- https://github.com/gavazquez
//With the help of ArSi -- https://github.com/arsi-apli

// Please I'm trying to know the CCcam protocol better, I would like to messag you, can you send me your Email Address?
// Mine is ricardoneves93@hotmail.com
package org.cline;

import java.io.IOException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void main(String[] args) throws UnknownHostException, IOException {

        String host = "213.152.164.137";
        int port = 13002;
        String user = "v0862";
        String password = "3302010";
        CcData.SetNodeId();
        List<CcCardData> cards = new ArrayList<>();

        try {
            cards = new CCcamConnector(host, port, user, password).TestCline();
        } catch (Exception e) {
            e.printStackTrace();
        }

        if (!cards.isEmpty()) {
            System.out.println("CCLine is valid");
            for (int i = 0; i < cards.size(); i++) {
                CcCardData card = cards.get(i);
                System.out.println(" caid " + DESUtil.intToHexString(card.getCaId(), 4) + " uphops " + card.getUpHops());

            }
        } else {
            System.out.println("CCLine is NOT valid");
        }
    }
}
