(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(assert (<= (str.to.int var0) (str.to.int (str.replace var1 var2 "<Z"))))
(assert (> (str.to.int var3) (str.to.int var0)))
(assert (str.suffixof var3 var2))
(assert (str.contains (str.at var3 152) (str.replace var0 var1 var1)))
(check-sat)