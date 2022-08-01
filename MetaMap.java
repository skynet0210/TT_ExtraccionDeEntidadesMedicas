import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.List;

import gov.nih.nlm.nls.metamap.Ev;
import gov.nih.nlm.nls.metamap.Mapping;
import gov.nih.nlm.nls.metamap.MetaMapApi;
import gov.nih.nlm.nls.metamap.MetaMapApiImpl;
import gov.nih.nlm.nls.metamap.PCM;
import gov.nih.nlm.nls.metamap.Position;
import gov.nih.nlm.nls.metamap.Result;
import gov.nih.nlm.nls.metamap.Utterance;

public class MetaMap {
	
	public static void main(String[] args) throws Exception {
		
		String inputPath = "";
		String outputPath = "";
		
		String options = args[0];
		inputPath = args[1];
		outputPath = args[2];
		
		File directory = new File(outputPath);
        if (! directory.exists()){
            directory.mkdir();
        }
		
		
		MetaMapApi api = new MetaMapApiImpl();
		
		api.setOptions(options);
		
		File inDir=new File(inputPath);
        File[] flist=inDir.listFiles();
        
        Arrays.sort(flist);
        
        for (File f: flist) {
        	
        	String filepath = f.getAbsolutePath();
        	
        	String ofilepath = outputPath + File.separator + f.getName();
        	
        	System.out.println("FILE: " + f.getName());
        	
        	File of = new File(ofilepath);
        	if(of.exists() && !of.isDirectory()) {
        		System.out.println("Done!!!");
        	    continue;
        	}
        	
        	PrintWriter pw = new PrintWriter(new FileWriter(ofilepath));
		
			List<Result> resultList = api.processCitationsFromFile(filepath);
			for (Result result:resultList) {

				int nsent = -1;
				String docID= f.getName().replace(".txt", "");
				for (Utterance utterance: result.getUtteranceList()) {
					System.out.println("");
					System.out.println("");
					System.out.println("");
					System.out.println("Utterance:");
					System.out.println(" Id: " + utterance.getId());
					//System.out.println(" Utterance text: " + utterance.getString());
					//System.out.println(" Position: " + utterance.getPosition());
					utterance.getString();
					String sentence = utterance.getString();
					
					nsent = Integer.parseInt(utterance.getId().split("\\.")[2])-2;
					
					int sentPosIni = utterance.getPosition().getX();
					
					for (PCM pcm: utterance.getPCMList()) {
						
				        for (Mapping map: pcm.getMappingList()) {
				            for (Ev mapEv: map.getEvList()) {
				            	Position pos = mapEv.getPositionalInfo().get(0);
					            String term = utterance.getString().substring(pos.getX()-sentPosIni,
										      pos.getX()+pos.getY()-sentPosIni);
					            int end = pos.getX()+pos.getY();
								pw.write(docID + "\t" + pos.getX() + "\t" +  end  + "\t" + term +
										"\t" + mapEv.getConceptId()+ "\t" + mapEv.getScore()*-1  +
										"\t" + mapEv.getPreferredName() + "\t"
										+ mapEv.getSemanticTypes() + "\t" + mapEv.getSources()
										+ "\n");
								pw.flush();
				              
				          }
				        }
					}
				}
			}
			pw.close();
        }
	}
}
