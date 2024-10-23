package pl.edu.mimuw;



public class InvalidParameters extends Exception{
    public static class InvalidFirstParameter extends InvalidParameters {}
    public static class InvalidSecondParameter extends InvalidParameters {}
    public static class InvalidParameterCount extends InvalidParameters {}
}
