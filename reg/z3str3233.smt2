(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.in.re (str.substr var0 var1 148) (re.* (re.* re.allchar))))
(assert (<= (str.len var2) (str.len var3)))
(assert (>= (str.to.int (str.at var4 var5)) (str.to.int (str.substr var4 var6 var7))))
(assert (> (str.len var2) (str.indexof "Yr+&(>CV" "{=A." var6)))
(check-sat)