(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (< (str.indexof (str.substr var0 72 var1) (str.replace "8%yp^7E" var2 var3) (str.to.int var4)) (str.indexof (str.at var4 var5) (str.replace var0 "18o@v2RRk{" var4) (str.indexof var2 var3 var6))))
(assert (> var7 var5))
(assert (>= (str.indexof var0 var4 var1) (str.to.int var4)))
(assert (<= (str.len var2) (str.indexof (str.replace "" var3 var3) (str.substr var0 var1 var7) (str.indexof var4 var3 var5))))
(check-sat)