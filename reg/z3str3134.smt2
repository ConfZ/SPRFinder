(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (str.contains (str.at var0 var1) (str.substr var2 var3 var4)))
(assert (< (str.indexof var5 var6 var7) (str.to.int var6)))
(assert (< (str.indexof "5~i/i+""cGa" var5 var4) (str.len var6)))
(assert (str.contains (str.substr var0 var1 var3) (str.substr var0 var1 var3)))
(check-sat)