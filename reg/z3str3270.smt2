(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () String)
(declare-fun var8 () Bool)
(assert (<= (str.indexof (str.substr var0 var1 var2) (str.substr var3 var4 var5) (str.len var6)) (str.indexof (str.at var7 var1) (str.at var7 var1) (str.to.int "V;k4%w"))))
(assert (not var8))
(assert (> (str.len var0) (str.indexof (str.replace "O7W" var7 var0) (str.at var6 26) (str.len var6))))
(assert (str.contains "go@8w" var3))
(check-sat)