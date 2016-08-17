import java.io.*;
import java.util.Properties;

class Canonicalize {
    public static void main(String args[])
            throws FileNotFoundException, IOException {
        InputStream in = args.length > 0 ? new FileInputStream(args[0])
                                         : System.in;
        PrintStream out = args.length > 1 ? new PrintStream(args[1])
                                          : System.out;
        Properties props = new Properties();
        props.load(in);
        props.store(out, "This is a comment.");
    }
}
