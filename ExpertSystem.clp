;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Transformer Fault Diagnosis Expert System (DGA)
;; Faults: PD, D1, D2, T1, T2, T3, Normal
;; CLIPS 6.4 - Forward Chaining
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
;; FACT BASE (SAMPLE INPUT)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deffacts transformer-gases
   (gas (name H2)   (value 180))
   (gas (name CH4)  (value 90))
   (gas (name C2H2) (value 2))
   (gas (name C2H4) (value 40))
   (gas (name C2H6) (value 50))
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; DIAGNOSTIC RULES
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; ========= PARTIAL DISCHARGE (PD) =========

(defrule R1-PD-H2-Dominant
   (gas (name H2) (value ?h2))
   (gas (name CH4) (value ?m))
   (test (> ?h2 100))
   (test (> ?h2 ?m))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R1 fired: Partial Discharge (H2 dominant)" crlf)
)

(defrule R2-PD-Low-CH4-H2
   (gas (name H2) (value ?h))
   (gas (name CH4) (value ?m))
   (test (< (/ ?m ?h) 0.1))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R2 fired: Partial Discharge (Low CH4/H2)" crlf)
)

(defrule R3-PD-No-Acetylene
   (gas (name H2) (value ?h))
   (gas (name C2H2) (value ?a))
   (test (> ?h 150))
   (test (< ?a 5))
=>
   (assert (diagnosis (fault "Partial Discharge")))
   (printout t "R3 fired: Partial Discharge (No acetylene)" crlf)
)

;; ========= LOW ENERGY ARCING (D1) =========

(defrule R4-D1-Methane-Dominant
   (gas (name CH4) (value ?m))
   (gas (name C2H6) (value ?a))
   (test (> ?m ?a))
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
   (printout t "R4 fired: Low Energy Arcing (CH4 dominant)" crlf)
)

(defrule R5-D1-Low-Acetylene
   (gas (name C2H2) (value ?a))
   (test (> ?a 1))
   (test (< ?a 50))
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
   (printout t "R5 fired: Low Energy Arcing (Low acetylene)" crlf)
)

;; ========= HIGH ENERGY ARCING (D2) =========

(defrule R6-D2-High-Acetylene
   (gas (name C2H2) (value ?a))
   (test (>= ?a 50))
=>
   (assert (diagnosis (fault "High Energy Arcing")))
   (printout t "R6 fired: High Energy Arcing (High acetylene)" crlf)
)

(defrule R7-D2-Acetylene-Dominant
   (gas (name C2H2) (value ?a))
   (gas (name H2) (value ?h))
   (test (> ?a ?h))
=>
   (assert (diagnosis (fault "High Energy Arcing")))
   (printout t "R7 fired: High Energy Arcing (C2H2 dominant)" crlf)
)

;; ========= THERMAL FAULT T1 (<300C) =========

(defrule R8-T1-Ethane-Dominant
   (gas (name C2H6) (value ?a))
   (gas (name C2H4) (value ?e))
   (test (> ?a ?e))
=>
   (assert (diagnosis (fault "Thermal Fault T1")))
   (printout t "R8 fired: Thermal Fault T1 (Ethane dominant)" crlf)
)

(defrule R9-T1-Low-Ethylene
   (gas (name C2H4) (value ?e))
   (test (< ?e 50))
=>
   (assert (diagnosis (fault "Thermal Fault T1")))
   (printout t "R9 fired: Thermal Fault T1 (Low ethylene)" crlf)
)

;; ========= THERMAL FAULT T2 (300–700C) =========

(defrule R10-T2-Ethylene-Dominant
   (gas (name C2H4) (value ?e))
   (gas (name C2H6) (value ?a))
   (test (> ?e ?a))
   (test (> ?e 50))
=>
   (assert (diagnosis (fault "Thermal Fault T2")))
   (printout t "R10 fired: Thermal Fault T2 (Ethylene dominant)" crlf)
)

(defrule R11-T2-Moderate-Ethylene
   (gas (name C2H4) (value ?e))
   (test (> ?e 50))
   (test (< ?e 200))
=>
   (assert (diagnosis (fault "Thermal Fault T2")))
   (printout t "R11 fired: Thermal Fault T2 (Moderate ethylene)" crlf)
)

;; ========= THERMAL FAULT T3 (>700C) =========

(defrule R12-T3-Very-High-Ethylene
   (gas (name C2H4) (value ?e))
   (test (>= ?e 200))
=>
   (assert (diagnosis (fault "Thermal Fault T3")))
   (printout t "R12 fired: Thermal Fault T3 (Very high ethylene)" crlf)
)

(defrule R13-T3-Low-Ethane
   (gas (name C2H6) (value ?a))
   (test (< ?a 20))
=>
   (assert (diagnosis (fault "Thermal Fault T3")))
   (printout t "R13 fired: Thermal Fault T3 (Low ethane)" crlf)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; FINAL DIAGNOSIS (FIRES LAST)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule FINAL-PD
   (declare (salience -100))
   (diagnosis (fault "Partial Discharge"))
=>
   (printout t crlf "FINAL DIAGNOSIS: PARTIAL DISCHARGE" crlf)
)

(defrule FINAL-D2
   (declare (salience -110))
   (diagnosis (fault "High Energy Arcing"))
   (not (diagnosis (fault "Partial Discharge")))
=>
   (printout t crlf "FINAL DIAGNOSIS: HIGH ENERGY ARCING" crlf)
)

(defrule FINAL-D1
   (declare (salience -120))
   (diagnosis (fault "Low Energy Arcing"))
   (not (diagnosis (fault "Partial Discharge")))
   (not (diagnosis (fault "High Energy Arcing")))
=>
   (printout t crlf "FINAL DIAGNOSIS: LOW ENERGY ARCING" crlf)
)

(defrule FINAL-T3
   (declare (salience -130))
   (diagnosis (fault "Thermal Fault T3"))
   (not (diagnosis (fault "Partial Discharge")))
=>
   (printout t crlf "FINAL DIAGNOSIS: THERMAL FAULT T3 (>700C)" crlf)
)

(defrule FINAL-T2
   (declare (salience -140))
   (diagnosis (fault "Thermal Fault T2"))
   (not (diagnosis (fault "Partial Discharge")))
   (not (diagnosis (fault "Thermal Fault T3")))
=>
   (printout t crlf "FINAL DIAGNOSIS: THERMAL FAULT T2 (300-700C)" crlf)
)

(defrule FINAL-T1
   (declare (salience -150))
   (diagnosis (fault "Thermal Fault T1"))
   (not (diagnosis (fault "Partial Discharge")))
   (not (diagnosis (fault "Thermal Fault T3")))
   (not (diagnosis (fault "Thermal Fault T2")))
=>
   (printout t crlf "FINAL DIAGNOSIS: THERMAL FAULT T1 (<300C)" crlf)
)

(defrule FINAL-NORMAL
   (declare (salience -200))
   (not (diagnosis (fault ?)))
=>
   (printout t crlf "FINAL DIAGNOSIS: NORMAL CONDITION" crlf)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; END OF FILE
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
