;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Transformer Fault Diagnosis Expert System (CORRECTED)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(deftemplate gas (slot name) (slot value))
(deftemplate diagnosis (slot fault))


;; ========= PARTIAL DISCHARGE (PD) =========

(defrule R1-PD-H2-Dominant
   (gas (name H2) (value ?h2))
   (gas (name CH4) (value ?m))
   (test (> ?h2 100))
   (test (> ?h2 ?m))
=>
   (assert (diagnosis (fault "Partial Discharge")))
)

(defrule R2-PD-Low-CH4-H2
   (gas (name H2) (value ?h))
   (gas (name CH4) (value ?m))
   (test (> ?h 10)) ;;
   (test (< (/ ?m ?h) 0.1))
=>
   (assert (diagnosis (fault "Partial Discharge")))
)

(defrule R3-PD-No-Acetylene
   (gas (name H2) (value ?h))
   (gas (name C2H2) (value ?a))
   (test (> ?h 150))
   (test (< ?a 5))
=>
   (assert (diagnosis (fault "Partial Discharge")))
)

;; ========= LOW ENERGY ARCING (D1) =========

(defrule R4-D1-Methane-Dominant
   (gas (name CH4) (value ?m))
   (gas (name C2H6) (value ?a))
   (test (> ?m ?a))
   (test (> ?m 50)) ;; 
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
)

(defrule R5-D1-Low-Acetylene
   (gas (name C2H2) (value ?a))
   (test (> ?a 1))
   (test (< ?a 50))
   (test (> ?a 10)) ;; 
=>
   (assert (diagnosis (fault "Low Energy Arcing")))
)

;; ========= HIGH ENERGY ARCING (D2) =========

(defrule R6-D2-High-Acetylene
   (gas (name C2H2) (value ?a))
   (test (>= ?a 50))
=>
   (assert (diagnosis (fault "High Energy Arcing")))
)

(defrule R7-D2-Acetylene-Dominant
   (gas (name C2H2) (value ?a))
   (gas (name H2) (value ?h))
   (test (> ?a ?h))
   (test (> ?a 10))
=>
   (assert (diagnosis (fault "High Energy Arcing")))
)

;; ========= THERMAL FAULT T1 (<300C) =========

(defrule R8-T1-Ethane-Dominant
   (gas (name C2H6) (value ?a))
   (gas (name C2H4) (value ?e))
   (test (> ?a ?e))
   (test (> ?a 50)) ;; 
=>
   (assert (diagnosis (fault "Thermal Fault T1")))
)


;; ========= THERMAL FAULT T2 (300–700C) =========

(defrule R9-T2-Ethylene-Dominant
   (gas (name C2H4) (value ?e))
   (gas (name C2H6) (value ?a))
   (test (> ?e ?a))
   (test (> ?e 50))
=>
   (assert (diagnosis (fault "Thermal Fault T2")))
)

(defrule R10-T2-Moderate-Ethylene
   (gas (name C2H4) (value ?e))
   (test (> ?e 50))
   (test (< ?e 200))
=>
   (assert (diagnosis (fault "Thermal Fault T2")))
)

;; ========= THERMAL FAULT T3 (>700C) =========

(defrule R11-T3-Very-High-Ethylene
   (gas (name C2H4) (value ?e))
   (test (>= ?e 200))
=>
   (assert (diagnosis (fault "Thermal Fault T3")))
)

