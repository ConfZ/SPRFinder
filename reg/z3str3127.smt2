(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.suffixof (str.substr var0 var1 var2) (str.replace var3 var4 var5)))
(assert (str.prefixof (str.substr (str.at var3 0) (str.to.int "WvEV*Ac") (str.indexof var4 var4 var6)) (str.at (str.at var0 var7) (str.to.int var5))))
(assert (str.contains var0 var4))
(assert (< (str.to.int "+XJ!7MB`") (str.len (str.substr var4 var7 var2))))
(check-sat)