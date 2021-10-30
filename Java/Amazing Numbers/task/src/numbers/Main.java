package numbers;

import java.util.Arrays;
import java.util.Scanner;

class PropertiesNumber {
    long number;
    String cad;
    char[] digits;

    PropertiesNumber(long number) {
        this.number = number;
        this.cad = String.valueOf(number);
        this.digits = this.cad.toCharArray();
    }

    void setNumber(long newNum) {
        this.number = newNum;
        this.cad = String.valueOf(number);
        this.digits = this.cad.toCharArray();
    }

    boolean isEven() {
        return this.number % 2 == 0;
    }

    boolean isOdd() {
        return this.number % 2 != 0;
    }

    boolean isBuzz() {
        return this.number % 7 == 0 || this.number % 10 == 7;
    }

    boolean isGapful() {
        String aux;
        if (cad.length() >= 3) {
            aux = cad.charAt(0) + String.valueOf(cad.charAt(cad.length() - 1));
            return number % Long.parseLong(aux) == 0;
        }
        return false;
    }

    boolean isDuck() {
        for (char c : this.digits) {
            if (c == '0') {
                return true;
            }
        }
        return false;
    }

    boolean isPalindromic() {
        for (int i = this.digits.length - 1, j = 0; i >= 0; i--, j++) {
            if (this.digits[i] != this.digits[j]) {
                return false;
            }
        }
        return true;
    }

    boolean isSpy() {
        long numsSum = 0;
        long numsPro = 1;
        for (char c : this.digits) {
            numsSum += (int) c - 48;
            numsPro *= (int) c - 48;
        }
        return numsSum == numsPro;
    }

    boolean isSquare() {
        return Math.pow((long) Math.sqrt(this.number), 2) == this.number;
    }

    boolean isSunny() {
        return Math.pow((long) Math.sqrt(this.number + 1), 2) == this.number + 1;
    }

    boolean isJumping() {
        if (digits.length > 1) {
            int num = digits[0] - 48;
            for (int i = 1; i < this.digits.length; i++) {
                if (num + 1 == digits[i] - 48 || num - 1 == digits[i] - 48) {
                    num = digits[i] - 48;
                } else {
                    return false;
                }
            }
        }
        return true;
    }

    boolean isHappy() {
        long sum;
        char[] aux = this.digits.clone();
        do {
            sum = 0L;
            for (char c : aux) {
                sum += Math.pow(c - 48, 2);
            }
            if (sum == 1) {
                return true;
            }
            aux = String.valueOf(sum).toCharArray();
        } while (sum != this.number && sum != 4);
        return false;
    }

    boolean[] getProperties() {
        return new boolean[] {isBuzz(), isDuck(), isPalindromic(), isGapful(),
                isSpy(), isSquare(), isSunny(), isJumping(), isEven(), isOdd(), isHappy(), !isHappy()};
    }

    static void processingArrayNumbers(long start, long tam) {
        PropertiesNumber newNum = new PropertiesNumber(start);
        boolean[] properties;
        for (int i = 0; i < tam; i++) {
            newNum.setNumber(start + i);
            properties = newNum.getProperties();
            displayProperty(start, properties, i);
        }
    }

    static void displayProperty(long start, boolean[] properties, long i) {
        String result;
        System.out.print(start + i);
        result = " is ";
        result += properties[0] ? "buzz, " : "";
        result += properties[1] ? "duck, " : "";
        result += properties[2] ? "palindromic, " : "";
        result += properties[3] ? "gapful, " : "";
        result += properties[4] ? "spy, " : "";
        result += properties[5] ? "square, " : "";
        result += properties[6] ? "sunny, " : "";
        result += properties[7] ? "jumping, " : "";
        result += properties[8] ? "even, " : "";
        result += properties[9] ? "odd, " : "";
        result += properties[10] ? "happy" : "sad";
        System.out.println(result.endsWith(", ") ? result.substring(0, result.length() - 2) : result);
    }

    static void searchProperty(long start, long tam, String property) {
        PropertiesNumber newNum = new PropertiesNumber(start);
        boolean[] properties;
        long i = 0;
        int index;
        if (property.startsWith("-")) {
            property = property.replace("-", "");
            for (int j = 0; j < tam; i++) {
                newNum.setNumber(start + i);
                properties = newNum.getProperties();
                index = ListProperties.valueOf(property).ordinal();
                if (!properties[index]) {
                    j++;
                    displayProperty(start, properties, i);
                }
            }
        } else {
            for (int j = 0; j < tam; i++) {
                newNum.setNumber(start + i);
                properties = newNum.getProperties();
                index = ListProperties.valueOf(property).ordinal();
                if (properties[index]) {
                    j++;
                    displayProperty(start, properties, i);
                }
            }
        }
    }

    static void anyProperty(long start, long tam, String... property) {
        PropertiesNumber newNum = new PropertiesNumber(start);
        boolean[] properties;
        boolean correct = true;
        long i = 0;
        int index;

        for (int j = 0; j < tam; i++) {
            newNum.setNumber(start + i);
            properties = newNum.getProperties();
            for (String S : property) {
                if (S.startsWith("-")) {
                    S = S.replace("-", "");
                    index = ListProperties.valueOf(S.toUpperCase()).ordinal();
                    if (properties[index]) {
                        correct = false;
                        break;
                    }
                } else {
                    index = ListProperties.valueOf(S.toUpperCase()).ordinal();
                    if (!properties[index]){
                        correct = false;
                        break;
                    }
                }
            }
            if (correct) {
                j++;
                displayProperty(start, properties, i);
            }
            correct = true;
        }
    }

}

enum ListProperties {
    BUZZ("", "-BUZZ"),
    DUCK("SPY", "-DUCK"),
    PALINDROMIC("", "-PALINDROMIC"),
    GAPFUL("", "-GAPFUL"),
    SPY("DUCK", "-SPY"),
    SQUARE("SUNNY", "-SQUARE"),
    SUNNY("SQUARE", "-SUNNY"),
    JUMPING("", "-JUMPING"),
    EVEN("ODD", "-EVEN"),
    ODD("EVEN", "-ODD"),
    HAPPY("SAD", "-HAPPY"),
    SAD("HAPPY", "-SAD");

    String exclude;
    String opp;

    ListProperties(String exclude, String opp) {
        this.exclude = exclude;
        this.opp = opp;
    }

    static Boolean evaluateProperty(String name) {
        if (name.startsWith("-")) {
            name = name.replace("-","");
        }
        for (ListProperties p : values()) {
            if (p.name().equals(name)) {
                return true;
            }
        }
        return false;
    }

    static String evaluateRange(String... name) {
        StringBuilder word = new StringBuilder();
        for (String s : name) {
            if (!evaluateProperty(s.toUpperCase())) {
                word.append(s.toUpperCase()).append(" ");
            }
        }
        if (!word.toString().isEmpty()) {
            return word.substring(0, word.length() - 1);
        }
        return "";
    }

    static String exclude(String... name) {
            String aux;
        for (String s : name) {
            if (s.startsWith("-")) {
                s = s.replace("-", "");
                aux = ListProperties.valueOf(s.toUpperCase()).exclude;
                if (!aux.isEmpty()) {
                    if (Arrays.toString(name).toUpperCase().contains("-" + aux)) {
                        return "-" + s.toUpperCase() + " " + "-" + aux;
                    }
                }
            } else {
                aux = ListProperties.valueOf(s.toUpperCase()).opp;
                if (Arrays.toString(name).toUpperCase().contains(aux)) {
                    return s.toUpperCase() + " " + aux;
                }
                aux = ListProperties.valueOf(s.toUpperCase()).exclude;
                if (!aux.isEmpty()) {
                    if (Arrays.toString(name).toUpperCase().contains("-" + aux)) {
                        continue;
                    }
                    if (Arrays.toString(name).toUpperCase().contains(aux)) {
                        return s.toUpperCase() + " " + aux;
                    }
                }
            }
        }
        return "";
    }
}


public class Main {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] numbers;
        boolean check;
        PropertiesNumber firstNumber;
        long start;
        long end;
        String nameProperty;
        String[] list;

        System.out.println("Welcome to Amazing Numbers!");
        menu();
        System.out.println("Enter a request: ");
        numbers = scanner.nextLine().split(" ");

        while (!numbers[0].equals("0")) {
            if (numbers[0].isEmpty()) {
                menu();
                System.out.println("\nEnter a request: ");
                numbers = scanner.nextLine().split(" ");
                continue;
            }
            try {
                start = Long.parseLong(numbers[0]);
            } catch (NumberFormatException nfe) {
                System.out.println("The first parameter should be a natural number or zero.");
                System.out.println("\nEnter a request: ");
                numbers = scanner.nextLine().split(" ");
                continue;
            }
            switch (numbers.length) {
                case 1:
                    if (start > 0) {
                        firstNumber = new PropertiesNumber(start);
                        System.out.println("Properties of " + numbers[0]);
                        System.out.println("buzz: " + firstNumber.isBuzz());
                        System.out.println("duck: " + firstNumber.isDuck());
                        System.out.println("palindromic: " + firstNumber.isPalindromic());
                        System.out.println("gapful: " + firstNumber.isGapful());
                        System.out.println("spy: " + firstNumber.isSpy());
                        System.out.println("square: " + firstNumber.isSquare());
                        System.out.println("sunny: " + firstNumber.isSunny());
                        System.out.println("jumping: " + firstNumber.isJumping());
                        System.out.println("even: " + firstNumber.isEven());
                        System.out.println("odd: " + firstNumber.isOdd());
                        System.out.println("happy: " + firstNumber.isHappy());
                        System.out.println("sad: " + !firstNumber.isHappy());
                    } else {
                        System.out.println("The first parameter should be a natural number or zero.");
                    }
                    break;
                case 2:
                    end = Long.parseLong(numbers[1]);
                    if (start > 0 && end > 0) {
                        PropertiesNumber.processingArrayNumbers(start, end);
                    } else if (start <= 0){
                        System.out.println("The first parameter should be a natural number.");
                    } else {
                        System.out.println("The second parameter should be a natural number.");
                    }
                    break;
                case 3:
                    end = Long.parseLong(numbers[1]);
                    nameProperty = numbers[2].toUpperCase();
                    check = ListProperties.evaluateProperty(nameProperty);
                    if (check) {
                        PropertiesNumber.searchProperty(start, end, nameProperty);
                    } else {
                        System.out.println("The property [" + nameProperty + "]" + " is wrong.");
                        System.out.println("Available properties:" +
                                " [EVEN, ODD, BUZZ, DUCK, PALINDROMIC," +
                                " GAPFUL, SPY, SQUARE, SUNNY, JUMPING, HAPPY, SAD]");
                    }
                    break;
                default:
                    end = Long.parseLong(numbers[1]);
                    list = Arrays.copyOfRange(numbers, 2, numbers.length);
                    nameProperty = ListProperties.evaluateRange(list);
                    if (!nameProperty.isEmpty()) {
                        if (nameProperty.split(" ").length > 1) {
                            System.out.println("The properties [" + nameProperty + "] are wrong");
                        } else {
                            System.out.println("The property [" + nameProperty + "] is wrong");
                        }
                        System.out.println("Available properties:" +
                                " [EVEN, ODD, BUZZ, DUCK, PALINDROMIC," +
                                " GAPFUL, SPY, SQUARE, SUNNY, JUMPING, HAPPY, SAD]");
                        break;
                    }
                    nameProperty = ListProperties.exclude(list);
                    if (!nameProperty.isEmpty()) {
                        System.out.println("The request contains mutually exclusive properties: ["
                                + nameProperty + "]");
                        System.out.println("There are no numbers with these properties.");
                        break;
                    } else {
                        PropertiesNumber.anyProperty(start, end, list);
                    }
                    break;
            }
            System.out.println("\nEnter a request: ");
            numbers = scanner.nextLine().split(" ");
        }
        System.out.println("Goodbye!");
        scanner.close();
    }

    private static void menu() {
        System.out.println("\nSupported requests:");
        System.out.println("- enter a natural number to know its properties;");
        System.out.println("- enter two natural numbers to obtain the properties of the list:");
        System.out.println("  * the first parameter represents a starting number;");
        System.out.println("  * the second parameter shows how many consecutive numbers are to be printed;");
        System.out.println("- two natural numbers and properties to search for;");
        System.out.println("- a property preceded by minus must not be present in numbers;");
        System.out.println("- separate the parameters with one space;");
        System.out.println("- enter 0 to exit\n");
    }
}

