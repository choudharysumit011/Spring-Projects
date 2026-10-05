public class MyHashMap<K,V> {


    Node<K,V>[] buckets;
   int capacity;
   int size;

   public MyHashMap(){
       capacity = 16;
       buckets = new Node[capacity];
       size = 0;

    }

    private int getBucketIndex(K key){

      return Math.abs(key.hashCode()) %capacity;
    }

    public void put(K key, V value){

        int index = getBucketIndex(key);

        Node<K,V> head = buckets[index];

        while(head != null){

            if(head.key.equals(key)){

                head.value = value;
                return;
            }

            head = head.next;
        }

        Node<K,V> newNode = new Node<>(key,value);

        newNode.next = buckets[index];

        buckets[index] = newNode;

        size++;

    }









}
