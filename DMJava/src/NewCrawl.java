import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.io.*;


public class NewCrawl {

    static final String[] sentence = {"2012도10269", "2010도759", "90도1516", "91도253",
            "2011도7725", "2016도16121", "93도656", "2014도14166", "99도2127", "2010도3436",
            "2009도12671", "2007도4404", "97누20755", "94도1519", "91도711", "2001도2869",
            "2007도9598", "2006도5993", "2010도7009", "96다53451"};

    void enter(){
        try{
            for(int i = 0; i < sentence.length; i++) {
                String url1 = "http://glaw.scourt.go.kr/wsjo/panre/sjo100.do?saNo=2007%EB%85%B81189";
                Document doc = Jsoup.connect(url1).get();
                System.out.println(doc);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
