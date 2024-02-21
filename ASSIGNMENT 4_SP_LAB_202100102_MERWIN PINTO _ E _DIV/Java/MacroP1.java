import java.io.*;
import java.util.*;

public class MacroP1 {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("macro_input.txt"));
        FileWriter macro_name_table = new FileWriter("macro_name_table.txt");
        FileWriter macro_defination_table = new FileWriter("macro_defination_table.txt");
        FileWriter keyword_param_default_table = new FileWriter("keyword_param_default_table.txt");
        FileWriter parameter_name_table = new FileWriter("parameter_name_table.txt");
        FileWriter evntab = new FileWriter("evntab.txt");
        FileWriter seq_symbol_name_table = new FileWriter("seq_symbol_name_table.txt");
        FileWriter seq_symbol_table = new FileWriter("seq_symbol_table.txt");

        LinkedHashMap<String, Integer> parameter_name_tableab = new LinkedHashMap<>();
        String line;
        String Macroname = null;
        int macro_defination_tablep = 1, keyword_param_default_tablep = 0, paramNo = 1, pp = 0, kp = 0, flag = 0;
        boolean evFound = false; 
        boolean labelFound = false;
        int lineIndex = 0;

        while ((line = br.readLine()) != null) 
        {
            lineIndex++;

            String parts[] = line.split("\\s+");
            if (parts[0].equalsIgnoreCase("MACRO")) 
            {
                flag = 1;
                line = br.readLine();
                parts = line.split("\\s+");
                Macroname = parts[0];
                if (parts.length <= 1) 
                {
                    macro_name_table.write(parts[0] + "\t" + pp + "\t" + kp + "\t" + macro_defination_tablep + "\t" + (kp == 0 ? keyword_param_default_tablep : (keyword_param_default_tablep + 1)) + "\n");
                    continue;
                }

                for (int i = 1; i < parts.length; i++) 
                {
                    parts[i] = parts[i].replaceAll("[&,]", "");

                    if (parts[i].contains("=")) 
                    {
                        ++kp;
                        String keywordParam[] = parts[i].split("=");
                        parameter_name_tableab.put(keywordParam[0], paramNo++);

                        if (keywordParam.length == 2) 
                        {
                            keyword_param_default_table.write(keywordParam[0] + "\t" + keywordParam[1] + "\n");
                        } 

                        else 
                        {
                            keyword_param_default_table.write(keywordParam[0] + "\t-\n");
                        }

                    } 

                    else {
                        parameter_name_tableab.put(parts[i], paramNo++);
                        pp++;
                    }
                }
                macro_name_table.write("MN" + "\t \t" + "PP" + "\t" + "KP" + "\t" + "MDT" + "\t" + "KPDT" +"\n");
                macro_name_table.write(parts[0] + "\t" + pp + "\t" + kp + "\t" + macro_defination_tablep + "\t" + (kp == 0 ? keyword_param_default_tablep : (keyword_param_default_tablep + 1)) + "\n");
                keyword_param_default_tablep = keyword_param_default_tablep + kp;

            } 

            else if (parts[0].equalsIgnoreCase("MEND")) 
            {
                macro_defination_table.write(line + "\n");
                flag = kp = pp = 0;
                macro_defination_tablep++;
                paramNo = 1;
                parameter_name_table.write(Macroname + ":\t");
                Iterator<String> itr = parameter_name_tableab.keySet().iterator();
                while (itr.hasNext()) 
                {
                    parameter_name_table.write(itr.next() + "\t");
                }

                parameter_name_table.write("\n");
                parameter_name_tableab.clear();
            } 
            else if (flag == 1) 
            {
                for (int i = 0; i < parts.length; i++) 
                {
                    if (parts[i].contains("&")) 
                    {
                        parts[i] = parts[i].replaceAll("[&,]", "");
                        macro_defination_table.write("(P," + parameter_name_tableab.get(parts[i]) + ")\t");
                    } 

                    else 
                    {
                        macro_defination_table.write(parts[i] + "\t");
                    }
                }
                macro_defination_table.write("\n");
                macro_defination_tablep++;
            } 
            else 
            {

            }

            if (line.contains("LCL")) 
            {
                String[] p = line.split("\\s+"); 

                for (String part : p) 
                {
                    if (part.equals("LCL")) 
                    {
                        continue;
                    }
                    String cleanPart = part.replace("&", "");
                    evntab.write(cleanPart + "\n");
                    evFound = true;
                }
            }

            for (int i = 0; i < parts.length; i++) 
            {
                String part = parts[i].trim();
                if (part.startsWith(".") && part.length() > 1) {
                    seq_symbol_name_table.write(part + "\n");
                    seq_symbol_table.write(lineIndex + 1 + "\n");
                    labelFound = true;
                }
            }
        }

        if (!evFound) {
            evntab.write("No EV found\n");
        }

        if (!labelFound) {
            seq_symbol_name_table.write("No sequencing symbols found\n");
        }

        br.close();
        macro_defination_table.close();
        macro_name_table.close();
        parameter_name_table.close();
        keyword_param_default_table.close();
        evntab.close();
        seq_symbol_name_table.close(); 
        seq_symbol_table.close(); 
        System.out.println("Macro Pass1 Processing done.");
    }
}