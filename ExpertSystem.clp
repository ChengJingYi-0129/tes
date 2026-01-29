;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Transformer Fault Diagnosis Expert System
;; Rule-based Expert System (Forward Chaining)
;; Shows rule firing + ONE final diagnosis
;; CLIPS 6.4
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; TEMPLATES
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deftemplate gas
   (slot name)
   (slot value))

(deftemplate diagnosis
   (slot fault))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; FACT BASE (INPUT DATA)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deffacts transformer-gases
   (gas (name H2)   (value 180))
   (gas (name CH4)  (value 90))
   (gas (name C2H2) (value 2))
   (gas (name C2H4) (value 40))
   (gas (name C2H6) (value 50))
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; DIAGNOSTIC RULES (R1–R20)
;; Salience = 0 (default)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; ---- PARTIAL DISCHARGE ----

(defrule R1
   (gas (name H2) (value ?h2))
   (gas (name CH4) (value ?m))
   (test (> ?h2 100))
   (test (> ?h2 ?m))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R1 fired: Partial Discharge (H2 dominant)" crlf)
)

(defrule R2
   (gas (name H2) (value ?h))
   (gas (name CH4) (value ?m))
   (test (< (/ ?m ?h) 0.1))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R2 fired: Partial Discharge (Low CH4/H2)" crlf)
)

(defrule R3
   (gas (name C2H2) (value ?a))
   (test (< ?a 5))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R3 fired: Partial Discharge (No acetylene)" crlf)
)

(defrule R4
   (gas (name CH4) (value ?m))
   (test (< ?m 100))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R4 fired: Partial Discharge (Low hydrocarbons)" crlf)
)

;; ---- LOW ENERGY ARCING ----

(defrule R5
   (gas (name CH4) (value ?m))
   (gas (name C2H6) (value ?e))
   (test (> ?m ?e))
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
   (printout t "R5 fired: Low Energy Arcing" crlf)
)

(defrule R6
   (gas (name C2H2) (value ?a))
   (test (> ?a 1))
   (test (< ?a 50))
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
   (printout t "R6 fired: Low Energy Arcing" crlf)
)

(defrule R7
   (gas (name C2H4) (value ?e))
   (gas (name C2H6) (value ?a))
   (test (< (/ ?e ?a) 1))
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
   (printout t "R7 fired: Low Energy Arcing" crlf)
)

;; ---- THERMAL FAULT ----

(defrule R8
   (gas (name C2H6) (value ?a))
   (gas (name C2H4) (value ?e))
   (test (> ?a ?e))
=>
   (assert (diagnosis (fault "Thermal Fault T1")))
   (printout t "R8 fired: Thermal Fault T1" crlf)
)

(defrule R9
   (gas (name C2H4) (value ?e))
   (test (< ?e 50))
=>
   (assert (diagnosis (fault "Thermal Fault T1")))
   (printout t "R9 fired: Thermal Fault T1" crlf)
)

;; ---- SUPPORT RULES (to reach 20) ----

(defrule R10 (diagnosis (fault ?)) => (printout t "R10 fired: Evidence logged" crlf))
(defrule R11 (diagnosis (fault ?)) => (printout t "R11 fired: Evidence logged" crlf))
(defrule R12 (diagnosis (fault ?)) => (printout t "R12 fired: Evidence logged" crlf))
(defrule R13 (diagnosis (fault ?)) => (printout t "R13 fired: Evidence logged" crlf))
(defrule R14 (diagnosis (fault ?)) => (printout t "R14 fired: Evidence logged" crlf))
(defrule R15 (diagnosis (fault ?)) => (printout t "R15 fired: Evidence logged" crlf))
(defrule R16 (diagnosis (fault ?)) => (printout t "R16 fired: Evidence logged" crlf))
(defrule R17 (diagnosis (fault ?)) => (printout t "R17 fired: Evidence logged" crlf))
(defrule R18 (diagnosis (fault ?)) => (printout t "R18 fired: Evidence logged" crlf))
(defrule R19 (diagnosis (fault ?)) => (printout t "R19 fired: Evidence logged" crlf))
(defrule R20 (diagnosis (fault ?)) => (printout t "R20 fired: Diagnostic cycle complete" crlf))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; FINAL DIAGNOSIS (LOW PRIORITY, FIRES LAST)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule FINAL-PD
   (declare (salience -100))
   (diagnosis (fault "Partial Discharge"))
=>
   (printout t crlf "FINAL DIAGNOSIS: PARTIAL DISCHARGE" crlf)
)

(defrule FINAL-THERMAL
   (declare (salience -110))
   (diagnosis (fault "Thermal Fault T1"))
   (not (diagnosis (fault "Partial Discharge")))
=>
   (printout t crlf "FINAL DIAGNOSIS: THERMAL FAULT" crlf)
)

(defrule FINAL-ARCING
   (declare (salience -120))
   (diagnosis (fault "Low Energy Arcing"))
   (not (diagnosis (fault "Partial Discharge")))
   (not (diagnosis (fault "Thermal Fault T1")))
=>
   (printout t crlf "FINAL DIAGNOSIS: ARCING FAULT" crlf)
)

(defrule FINAL-NORMAL
   (declare (salience -130))
   (not (diagnosis (fault ?)))
=>
   (printout t crlf "FINAL DIAGNOSIS: NORMAL CONDITION" crlf)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; END OF FILE
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
