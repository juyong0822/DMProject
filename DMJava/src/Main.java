
public class Main {

    static String[] words = {"교통사고처리특례법", "교통사고처리특례법위반", "교통사고처리특례", "교통사고처리", "교통사고",
            "사고처리특례법위반", "처리특례법위반", "특례법위반", "사고처리특례법", "사고처리특례", "사고처리특례 위반",
            "교통사고처리위반", "교통사고위반", "교통사고특례법", "교통사고처리특례법 교통사고", "판결 [교통사고처리특례법]",
            "교통사고위반법", "교통사고법", "교통사고법위반", "교통특례법위반", "교통특례법", "교통사고특례위반",
            "교통사고특례위반법"};

    public static void main(String[] args){
        Crawl crawl;
        for(int i = 0; i < words.length; i++) {
            crawl = new Crawl();
            crawl.crawling(words[i]);
        }
    }
}
