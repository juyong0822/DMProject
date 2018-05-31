/*

import edu.smu.tspell.wordnet.Synset;
import edu.smu.tspell.wordnet.WordNetDatabase;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;

import edu.stanford.nlp.tagger.maxent.MaxentTagger;

public class QueryModifier {
    final static String CLOSER = " )";
    final static String BM25_SCORER = "#feature:class=scorer.bm25.BM25Iterator( ";
    final static String INTAPP_SCORER = "#feature:class=scorer.termproject.IntappScorer( ";
    static String[] adjectives = {"JJ", "JJR", "JJS"};
    static String[] nouns = {"NN", "NNS", "NNP", "NNPS"};
    static String[] verbs = {"VB", "VBG", "VBN", "VBD", "VBP", "VBZ"};
    static String[] worthypos = {"JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "VB", "VBG", "VBN", "VBD", "VBP", "VBZ"};

    public static String modifyQuery(String query) {
        String modQuery = query;
        StringBuffer sbuff = new StringBuffer();

        String taggerFilename ="res/taggers/wsj-0-18-left3words-nodistsim.tagger";

        MaxentTagger tagger = new MaxentTagger(taggerFilename);

        // stopwords 출처 : http://xpo6.com/download-stop-word-list/
        String[] stopwords = {"instance", "information", "include", "etc.", "i.e.", "interested", "including", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "interested", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"};
        String[] delim = {"!", "#", "%", "&", "@", "`", ":", ";", "-", ".", "<", ">", ",", "~ ", "'"};

        // first, check out that inputed query is not a complex query by checking "#" modifier in the text
        if(query.contains("#")) {
            return query;
        }

        // change query to lower case and replace "-", " "
        String[] tokens = tagger.tagString(query.toLowerCase().replace("-", " ")).split("_|\\s+");

        int numWord = tokens.length/2;

        // word[i]'s pos = pos[i]
        String[] word = new String[numWord];
        String[] pos = new String[numWord];

        for(int i=0; i < numWord; i++){
            word[i] = tokens[2*i];
            pos[i] = tokens[2*i+1];
        }

        for(int i = 0; i < numWord; i++) {

            // replace stopwords from query
            if(Arrays.asList(stopwords).contains(word[i]) || Arrays.asList(delim).contains(word[i])) {
            }
            else {
                // give weight for word whose length is longer than 14
                if(word[i].length() >= 15) sbuff.append("#scale:weight=" + 2.0 * getPosWeight(pos[i]) + "( ");
                else sbuff.append("#scale:weight=" + getPosWeight(pos[i]) + "( ");
                sbuff.append(INTAPP_SCORER);
                sbuff.append(word[i]);
                sbuff.append(CLOSER);
                sbuff.append(CLOSER);
                sbuff.append(" ");

                // give weight for POS n-gram
                if(pos[i].equals("VBG")){
                    int j = i;
                    while(true){
                        j++;
                        if(!Arrays.asList(worthypos).contains(pos[j])) break;
                    }
                    j--;
                    if(i==j) continue;
                    sbuff.append("#scale:weight=" + 5 + "( ");
                    sbuff.append(INTAPP_SCORER);
                    sbuff.append("#od:1( ");
                    for (; i <= j; i++) {
                        sbuff.append(word[i] + " ");
                    }
                    sbuff.append(CLOSER);
                    sbuff.append(CLOSER);
                    sbuff.append(CLOSER);
                    sbuff.append(" ");

                    i = j;
                }
            }

        }

        /* give weight for 2-gram
        for(int ii=0; ii<numWord-1; ii++){
            if(!Arrays.asList(stopwords).contains(word[ii]) && !Arrays.asList(stopwords).contains(word[ii+1]) ){
                sbuff.append("#scale:weight=" + 0.5 + "( ");
                sbuff.append(INTAPP_SCORER);
                sbuff.append("#od:1( ");
                sbuff.append(word[ii] + word[ii+1]);
                sbuff.append(CLOSER);
                sbuff.append(CLOSER);
                sbuff.append(CLOSER);
                sbuff.append(" ");
            }
        }*/
/*
        // give weight for 'united press' if query contains 'new york'
        // for query #5, document 3401
        if(Arrays.asList(word).contains("new") && Arrays.asList(word).contains("york")){
            sbuff.append("#scale:weight=" + 20.0 + "( ");
            sbuff.append(INTAPP_SCORER);
            sbuff.append("#od:1(united press)");
            sbuff.append(CLOSER);
            sbuff.append(CLOSER);
            sbuff.append(" ");
        }

        // split sentences
        String[] sentences = query.toLowerCase().trim().split("\\.");

        // give weight for whole keyword phrase in last sentence
        if(sentences.length >=2){
            String lastSentence = sentences[sentences.length-1];
            String[] keyWords = lastSentence.split(",");
            for(String s : keyWords) {
                sbuff.append("#scale:weight=" + 1.0 + "( ");
                sbuff.append(INTAPP_SCORER);
                sbuff.append("#od:1( " + s);
                sbuff.append(CLOSER);
                sbuff.append(CLOSER);
                sbuff.append(CLOSER);
                sbuff.append(" ");
            }
        }

        if(sbuff.length() > 0) modQuery = sbuff.toString();

        return modQuery;
    }

    // give weight according to POS for each word
    static double getPosWeight(String pos){

        double weight=0.0;

        if(Arrays.asList(nouns).contains(pos)) weight = 3.2;
        else if(Arrays.asList(verbs).contains(pos)) weight = 3.0;
        else if(Arrays.asList(adjectives).contains(pos)) weight = 3.0;
        else weight = 0.5;

        return weight;
    }
*/
    /*  get synonyms of each word from WordNet API
    static String[] getSyn(String word){
        String[] syns ;

        File f = new File(("res/WordNet/2.1/dict"));
        System.setProperty("wordnet.database.dir", f.toString());
        //setting path for the WordNet Directory

        WordNetDatabase database = WordNetDatabase.getFileInstance();
        Synset[] synsets = database.getSynsets(word);
        //  Display the word forms and definitions for synsets retrieved

        if(synsets.length >0){
            ArrayList<String> al = new ArrayList<String>();
            HashSet hs = new HashSet();
            for (int i = 0; i < synsets.length; i++) {
                String[] wordForms = synsets[i].getWordForms();
                for (int j = 0; j < wordForms.length; j++)
                    al.add(wordForms[j]);

                //removing duplicates
                hs.addAll(al);
                al.clear();
                al.addAll(hs);
            }
            syns = al.toArray(new String[0]);
        }
        else{
            syns = new String[0];
        }

        return syns;

    }
    *//*
}

*/