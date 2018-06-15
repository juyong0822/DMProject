import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.io.*;

public class Main {

    static String[] words = {"상고 교통사고처리특례법", "상고 교통사고처리특례법위반", "상고 교통사고처리특례",
            "상고 교통사고처리", "상고 교통사고", "상고 사고처리특례법위반", " 상고처리특례법위반",
            "상고 특례법위반", "상고 사고처리특례법", "상고 사고처리특례", "상고 사고처리특례 위반",
            "상고 교통사고처리위반", "상고 교통사고위반", "상고 교통사고특례법", "상고 교통사고처리특례법 교통사고",
            "상고 판결 [교통사고처리특례법]", "상고 교통사고위반법", "상고 교통사고법", "상고 교통사고법위반",
            "상고 교통특례법위반", "상고 교통특례법", "상고 교통사고특례위반", "상고 교통사고특례위반법"};

    public static void main(String[] args){
        /*
        Crawl crawl;
        for(int i = 0; i < words.length; i++) {
            crawl = new Crawl();
            crawl.crawling(words[i]);
        }
        */
        try{
            String url1 = "http://glaw.scourt.go.kr/wsjo/panre/sjo100.do?saNo=2007%EB%85%B81189";
            Document doc = Jsoup.connect(url1).get();
            System.out.println(doc);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
