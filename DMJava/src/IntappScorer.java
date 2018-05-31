/*

// BSD License (http://www.galagosearch.org/license)

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import org.galagosearch.core.index.PositionIndexReader;
import org.galagosearch.core.retrieval.structured.CountIterator;
import org.galagosearch.core.retrieval.structured.RequiredStatistics;
import org.galagosearch.core.retrieval.structured.ScoringFunctionIterator;
import org.galagosearch.core.util.ExtentArray;
import org.galagosearch.tupleflow.Parameters;

@RequiredStatistics(statistics = {"collectionLength", "documentCount"})
public class IntappScorer extends ScoringFunctionIterator {
    double k_1;
    double b;
    double delta;
    double documentFrequency;
    double documentCount;
    double avgDocumentLength;
    double collectionLength;
    double inverseDocumentFrequency;
    HashMap<Integer, ArrayList<Integer>> termPositionsMap = new HashMap<Integer, ArrayList<Integer>>();
    HashMap<Integer, Long> byteLengthMap = new HashMap<Integer, Long>();
    HashMap<Integer, ArrayList<String>> termListMap = new HashMap<Integer, ArrayList<String>>();

    public IntappScorer(Parameters parameters, CountIterator iterator) throws IOException {
        super(iterator);

        // TODO: here you write your scoring function needed for a query

        documentFrequency = 0;
        documentCount = parameters.get("documentCount", 100000);
        collectionLength = parameters.get("collectionLength", 1000000);
        avgDocumentLength = collectionLength / documentCount;
        //System.out.println(((PositionIndexReader.Iterator) iterator).getRecordString());

        if(iterator instanceof PositionIndexReader.Iterator) {
            while(!iterator.isDone()) {

                ArrayList<String> termList = new ArrayList<String>();

                int document = iterator.document();
                ExtentArray extentArray = ((PositionIndexReader.Iterator) iterator).extents();
                ArrayList<Integer> termPositions = new ArrayList<Integer>();

                for (int i = 0; i < extentArray.getPosition(); ++i) {
                    termPositions.add(extentArray.getBuffer()[i].begin);
                }
                termPositionsMap.put(document, termPositions);
                byteLengthMap.put(document, ((PositionIndexReader.Iterator) iterator).getDocumentByteLength());

                iterator.nextDocument();

            }
        }
        iterator.reset();

        while (!iterator.isDone()) {

            documentFrequency += 1;
            iterator.nextDocument();
        }

        iterator.reset();
        computeInverseDocumentFrequency();
    }

    public void computeInverseDocumentFrequency() {
        double numerator = documentCount - documentFrequency +0.5;
        double denominator = 0.9*documentFrequency +0.5;

        inverseDocumentFrequency = Math.log(numerator / denominator);
    }

    public double score(int document, int length) {
        int count = 0;

        if (iterator.document() == document) {
            count = iterator.count();
        }
        return scoreCount(count, length);
    }

    public double scoreCount(int count, int length) {
        double score=0;
        int document = iterator.document();
        ArrayList<Integer> termPositions = termPositionsMap.get(document);
        ///////////////////////////////////////////////////////////////////////
        // POSSIBLE FEATURES
        // documentFrequency: number of documents that contains the query term
        // documentCount: total number of documents in the collection
        // collectionLength: length of collection
        // avgDocumentLength: average document length
        // termPositions: positions in the document for the query term
        // count: number of term occurrence in the document for the query term
        // length: length of current document

        // TODO: Here you write your scoring function needed for a document

        //  BM25 +
        k_1 = 2.0;
        b = 0.75;
        delta = 1.0;

        double numerator = count * (k_1 + 1);
        double denominator = count + k_1 * (1.0 - b + b * (length/avgDocumentLength));

        score = inverseDocumentFrequency * (numerator / denominator + delta);

        return score;
    }

}

*/