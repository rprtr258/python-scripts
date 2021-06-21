((defn rainbow [s]
    (doseq [k (map #(-> % (/ 4) Math/cos inc (* (/ (count s) 2)) int) (range 100))]
        (println (apply str (repeat k " ")) s))) "AAAAAAAAAAAAAAAAAAAAAAA")
