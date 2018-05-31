import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;


public class Crawl {

    public Crawl(String keyword){
        this.keyword = keyword;

    }

    static String keyword = "상고";

    static final int page_limit = 20;

    static int success = 0;         // crawling success
    static int fail1 = 0;           // 2심 없음 fail
    static int fail2 = 0;           // 3심 없음 fail

    public static void main(String[] args) {

        String hyperlinkUrl;        // 3심 url
        String nextHyperlinkUrl;    // 2심 url
        String lastHyperlinkUrl;    // 1심 url

        ArrayList<Integer[]> success_list = new ArrayList<>();

        try {
            for(int page = 1; page <= page_limit; page++) {
                String url = "https://casenote.kr/search/?q="+keyword+"&p="+page+"&sort=1&cc=0&ct=0";
                Document doc = Jsoup.connect(url).get();
                Elements el = doc.select("div.searched_item");
                Elements sites = el.select("a[href]");

                for (int i = 0; i < sites.size(); i++) {
                    Element site = sites.get(i);
                    hyperlinkUrl = site.attr("href");
                    Document sentence1 = Jsoup.connect("https://casenote.kr" + hyperlinkUrl).get();

                    Elements header1 = sentence1.select("td.header_name");
                    Elements site2 = header1.select("a[href]");
                    nextHyperlinkUrl = site2.attr("href");
                    if(nextHyperlinkUrl == ""){
                        fail1++;
                        continue;
                    }
                    Document sentence2 = Jsoup.connect("https://casenote.kr" + nextHyperlinkUrl).get();

                    Elements header2 = sentence2.select("td.header_name");
                    Elements site3 = header2.select("a[href]");
                    lastHyperlinkUrl = site3.attr("href");
                    if(lastHyperlinkUrl == ""){
                        fail2++;
                        continue;
                    }
                    Document sentence3 = Jsoup.connect("https://casenote.kr" + lastHyperlinkUrl).get();

                    success++;
                    System.out.println();
                    System.out.println(site.text());
                    System.out.println(sentence1.text());
                    System.out.println(sentence2.text());
                    System.out.println(sentence3.text());
                    Integer[] a = {page, i};
                    success_list.add(a);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("success : " + success + ", fail = " + fail1 + ", fail2 = " + fail2);
        for(int i = 0; i < success_list.size(); i++)
            System.out.println("page = " + success_list.get(i)[0] + ", i = " + success_list.get(i)[1]);
    }

}
