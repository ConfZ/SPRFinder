(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (str.contains (str.replace (str.substr var0 var1 var2) (str.substr var3 57 var4) (str.substr "#K" var5 var4)) (str.at (str.at var6 var5) (str.len var7))))
(assert (< (str.len var0) (str.len var6)))
(assert (> (str.len var6) (str.to.int var7)))
(assert (not (str.prefixof var0 var3)))
(check-sat)