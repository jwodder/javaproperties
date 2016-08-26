import java.io.*;
import java.util.Collections;
import java.util.LinkedList;
import java.util.Properties;

class Properties2JSON {
    public static void main(String args[])
            throws FileNotFoundException, IOException {
        InputStream in = args.length > 0 ? new FileInputStream(args[0])
                                         : System.in;
        PrintStream out = args.length > 1 ? new PrintStream(args[1])
                                          : System.out;
        Properties props = new Properties();
        props.load(in);
        if (props.size() == 0) {
            out.println("{}");
        } else {
            LinkedList<String> keys
                = new LinkedList(props.stringPropertyNames());
            Collections.sort(keys);
            out.println("{");
            boolean first = true;
            for (String k: keys) {
                if (first) {
                    first = false;
                } else {
                    out.println(",");
                }
                out.print("    " + jsonify(k)
                          + ": " + jsonify(props.getProperty(k)));
            }
            out.println("\n}");
        }
    }

    public static String jsonify(String s) {
        // cf. <http://stackoverflow.com/a/1351973/744178>
        StringBuilder sb = new StringBuilder();
        sb.append('"');
        for (char ch: s.toCharArray()) {
            switch (ch) {
                case '"':
                    sb.append("\\\"");
                    break;
                case '\\':
                    sb.append("\\\\");
                    break;
                case '\n':
                    sb.append("\\n");
                    break;
                case '\r':
                    sb.append("\\r");
                    break;
                case '\f':
                    sb.append("\\f");
                    break;
                case '\t':
                    sb.append("\\t");
                    break;
                case '\b':
                    sb.append("\\b");
                    break;
                default:
                    if (ch < 0x20 || ch >= 0x7F) {
                        sb.append(String.format("\\u%04x", (int)ch));
                    } else {
                        sb.append(ch);
                    }
            }
        }
        sb.append('"');
        return sb.toString();
    }
}
