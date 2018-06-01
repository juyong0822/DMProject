import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.io.*;


public class Crawl {

    static final int page_limit = 20;
    static final String location = "..\\CrawlingFiles\\";

    int success = 0;         // crawling success
    int fail1 = 0;           // 2심 없음 fail
    int fail2 = 0;           // 3심 없음 fail

    private String hyperlinkUrl;
    private String nextHyperlinkUrl;
    private String lastHyperlinkUrl;

    private Document sentence3;
    private Document sentence2;
    private Document sentence1;

    void crawling(String keyword) {

        ArrayList<Integer[]> success_list = new ArrayList<>();

        try {
            for(int page = 1; page <= page_limit; page++) {
                String url = "https://casenote.kr/search/?q=" + keyword + "&p=" + page + "&sort=1&cc=0&ct=0";
                Document doc = Jsoup.connect(url).get();
                Elements el = doc.select("div.searched_item");
                Elements sites = el.select("a[href]");

                for (int i = 0; i < sites.size(); i++) {
                    Element site3 = sites.get(i);

                    hyperlinkUrl = site3.attr("href");
                    this.sentence3 = Jsoup.connect("https://casenote.kr" + hyperlinkUrl).get();

                    nextHyperlinkUrl = getHeader3(sentence3);
                    if(nextHyperlinkUrl.equals("")){
                        fail1++;
                        continue;
                    }
                    this.sentence2 = Jsoup.connect("https://casenote.kr" + nextHyperlinkUrl).get();

                    lastHyperlinkUrl = getHeader2(sentence2);
                    if(lastHyperlinkUrl.equals("")){
                        fail2++;
                        continue;
                    }
                    this.sentence1 = Jsoup.connect("https://casenote.kr" + lastHyperlinkUrl).get();

                    String filename3 = keyword + "_" + success + "_" + 3;
                    // String text3 = seperText3(sentence3.text());
                    String text3 = sentence3.text();
                    saveFile(filename3, text3);

                    String filename2 = keyword + "_" + success + "_" + 2;
                    // String text2 = seperText2(sentence2.text());
                    String text2 = sentence2.text();
                    saveFile(filename2, text2);

                    String filename1 = keyword + "_" + success + "_" + 1;
                    // String text1 = seperText1(sentence1.text());
                    String text1 = sentence1.text();
                    saveFile(filename1, text1);

                    Integer[] a = {page, i};
                    success_list.add(a);

                    success++;
                }
                /*
                for (int i = 7; i < 8; i++) {
                    Element site3 = sites.get(i);

                    hyperlinkUrl = site3.attr("href");
                    Document sentence3 = Jsoup.connect("https://casenote.kr" + hyperlinkUrl).get();
                    third = true;

                    nextHyperlinkUrl = getHeader3(sentence3);
                    if(failed)   continue;
                    Document sentence2 = Jsoup.connect("https://casenote.kr" + nextHyperlinkUrl).get();

                    lastHyperlinkUrl = getHeader2(sentence2);
                    if(failed)  continue;
                    if(!third){
                        exception(sentence2);
                    }
                    Document sentence1 = Jsoup.connect("https://casenote.kr" + lastHyperlinkUrl).get();

                    success++;

                    String filename3 = keyword + page + "_" + i + "_" + 3;
                    saveFile3(filename3, sentence3);

                    String filename2 = keyword + page + "_" + i + "_" + 3;
                    saveFile2(filename2, sentence2);

                    String filename1 = keyword + page + "_" + i + "_" + 3;
                    saveFile1(filename1, sentence1);

                    System.out.println();
                    System.out.println(site3.text());
                    System.out.println(sentence3.text());
                    System.out.println(sentence2.text());
                    System.out.println(sentence1.text());
                    Integer[] a = {page, i};
                    success_list.add(a);
                } */
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("keyword : " + keyword + ", success : " + success + ", fail1 = " + fail1 + ", fail2 = " + fail2);
        for(int i = 0; i < success_list.size(); i++)
            System.out.println("page = " + success_list.get(i)[0] + ", i = " + success_list.get(i)[1]);
    }

    String getHeader3(Document document){
        Elements header = document.select("li.hasContent");
        if(header.size() > 3){
            Elements site = header.get(2).select("a[href]");
            if(site.size() != 0) {
                hyperlinkUrl = "https://casenote.kr" + site.attr("href");
                try {
                    this.sentence3 = Jsoup.connect(hyperlinkUrl).get();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return getHeader3(this.sentence3);
            }
        } else if(header.size() < 3){
            return "";
        }
        return header.get(1).select("a[href]").attr("href");
    }

    String getHeader2(Document document){
        return document.select("li.hasContent").get(0).select("a[href]").attr("href");
    }

    Boolean detectText(String originText, String targetText){
        for(int i = 0; i < targetText.length(); i++){
            if(originText.charAt(i) != targetText.charAt((i)))
                return false;
        }
        return true;
    }

    String seperText3(String text){
        String newText = "";
        int index = 0;

        while(index < text.length()){
            if(detectText(text.substring(index), "판시사항")){
                newText += '\n';
                newText += "판시사항";
                newText += '\n';
                index += 4;
            } else if(detectText(text.substring(index), "판결요지")){
                newText += '\n';
                newText += "판결요지";
                newText += '\n';
                index += 4;
            } else if(detectText(text.substring(index), "참조조문")){
                newText += '\n';
                newText += "참조조문";
                newText += '\n';
                index += 4;
            } else if(detectText(text.substring(index), "참조판례")){
                newText += '\n';
                newText += "참조판례";
                newText += '\n';
                index += 4;
            } else if(detectText(text.substring(index), "주 문")){
                newText += '\n';
                newText += "주 문";
                newText += '\n';
                index += 3;
            } else if(detectText(text.substring(index), "이 유")){
                newText += '\n';
                newText += "이 유";
                newText += '\n';
                index += 3;
            }
            newText += text.charAt(index);
            index++;
        }

        return newText;
    }

    String seperText2(String text){
        String newText = "";
        int index = 0;

        while(index < text.length()){
            if(detectText(text.substring(index), "주 문")){
                newText += '\n';
                newText += "주 문";
                newText += '\n';
                index += 3;
            } else if(detectText(text.substring(index), "이 유")){
                newText += '\n';
                newText += "이 유";
                newText += '\n';
                index += 3;
            } else if(detectText(text.substring(index), "1. 항소이유의 요지")){
                newText += '\n';
                newText += "1. 항소이유의 요지";
                newText += '\n';
                index += 11;
            } else if(detectText(text.substring(index), "2. 판단")){
                newText += '\n';
                newText += "2. 판단";
                newText += '\n';
                index += 5;
            } else if(detectText(text.substring(index), "3. 결론")){
                newText += '\n';
                newText += "3. 결론";
                newText += '\n';
                index += 5;
            }
            newText += text.charAt(index);
            index++;
        }

        return newText;
    }

    String seperText1(String text){
        String newText = "";
        int index = 0;

        while(index < text.length()){
            if(detectText(text.substring(index), "주 문")){
                newText += '\n';
                newText += "주 문";
                newText += '\n';
                index += 3;
            } else if(detectText(text.substring(index), "이 유")){
                newText += '\n';
                newText += "이 유";
                newText += '\n';
                index += 3;
            } else if(detectText(text.substring(index), "범죄사실")){
                newText += '\n';
                newText += "범죄사실";
                newText += '\n';
                index += 4;
            } else if(detectText(text.substring(index), "증거의 요지")){
                newText += '\n';
                newText += "증거의 요지";
                newText += '\n';
                index += 6;
            } else if(detectText(text.substring(index), "법령의 적용")){
                newText += '\n';
                newText += "법령의 적용";
                newText += '\n';
                index += 6;
            } else if(detectText(text.substring(index), "양형이유")){
                newText += '\n';
                newText += "양형이유";
                newText += '\n';
                index += 4;
            }
            newText += text.charAt(index);
            index++;
        }

        return newText;
    }

    // saving File
    // of 3rd sentence
    void saveFile(String filename, String text){
        BufferedWriter bw = null;
        try{
            bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(location + filename + ".txt"), StandardCharsets.UTF_8));

            for(int i = 0; i < text.length(); i++){
                bw.write(text.charAt(i));
            }
            bw.close();
        } catch(IOException e){
            e.printStackTrace();
        }
        System.out.println(text);
    }

    /*
    String getHeader3(Document document){
        Elements header = document.select("td.header_name");
        int title3 = 0;
        while(!document.select("td.header_title").get(title3).text().equals("원심판결"))
            title3 += 1;
        Elements site2 = header.get(title3).select("a[href]");
        String nextHyperlinkUrl = site2.attr("href");
        if(nextHyperlinkUrl.equals("")){
            fail1++;
            failed = true;
            return null;
        }
        return nextHyperlinkUrl;
    }

    String getHeader2(Document document){
        Elements header = document.select("td.header_name");
        int title2 = 0;
        String type = "원심판결";
        while(!document.select("td.header_title").get(title2).text().equals(type)) {
            title2 += 1;
            if(title2 == header.size()) {
                title2 = 0;
                type = "환송판결";
            }
        }
        Elements site1 = header.select("a[href]");
        String lastHyperlinkUrl = site1.attr("href");
        if(lastHyperlinkUrl.equals("")){
            fail2++;
            return null;
        }
        return lastHyperlinkUrl;
    }

    */

}
