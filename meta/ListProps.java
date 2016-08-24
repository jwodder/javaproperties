import java.io.*;
import java.util.Properties;

class ListProps {
    public static void main(String args[])
            throws FileNotFoundException, IOException {
        InputStream in = args.length > 0 ? new FileInputStream(args[0])
                                         : System.in;
        Properties props = new Properties();
        props.load(in);
        props.list(System.out);
    }
}
