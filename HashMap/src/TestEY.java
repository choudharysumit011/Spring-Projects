import java.util.Arrays;
import java.util.Comparator;

public class TestEY {

    public static void main(String[] args) {

        String s = "abcbacbb";
        int res = longestSubstring(s);
        System.out.println(res);

        int[] arr = {2,4,5,6,23,45,89};

        int[] resrr = Arrays.stream(arr).boxed()
                .sorted(Comparator.reverseOrder())
                .mapToInt(Integer::intValue)
                .toArray();


        for(int i =0; i< arr.length; i++){

            for(int j = i+1; j<arr.length; j++){
                if(arr[j] > arr[i]){
                    swap(arr, j, i);
                }
            }

        }

        for(int j : arr) {
            System.out.println(j);
        }



    }

    static void swap(int[] arr, int i, int j){
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }



   static int longestSubstring(String s){
        int[] arr = new int[128];

        int left = 0;
        int max =0;
        for(int right = 0; right < s.length(); right++){

            char c = s.charAt(right);
            arr[c]++;

            while (arr[s.charAt(right)] > 1 ){
                arr[s.charAt(left)]--;
                left++;
            }

            max = Math.max(max, right -left +1);
        }

        return max;
    }

}
