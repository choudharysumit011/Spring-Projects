public class TestSingleton {

    private static volatile TestSingleton testSingleton;

    public static TestSingleton getInstance(){

        if(testSingleton == null){
            synchronized (TestSingleton.class){
                if(testSingleton == null){
                    testSingleton = new TestSingleton();
                }
            }
        }

        return testSingleton;
    }
}
